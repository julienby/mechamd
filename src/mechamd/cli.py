"""Ligne de commande `mecha`."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from mechamd import __version__
from mechamd.engine import Engine
from mechamd.testing import run_directive


def cmd_test(args: argparse.Namespace) -> int:
    engine = Engine(project=args.project)
    for error in engine.load_errors:
        print(f"✗ chargement : {error}")
    names = [args.directive] if args.directive else sorted(engine.directives)
    failures = len(engine.load_errors)
    total = passed = 0
    for name in names:
        directive = engine.directives.get(name)
        if directive is None:
            print(f"✗ {name} : directive introuvable")
            failures += 1
            continue
        for result in run_directive(engine, directive):
            total += 1
            if result.ok:
                passed += 1
                print(f"✓ {result.directive}/{result.example}")
            else:
                failures += 1
                print(f"✗ {result.directive}/{result.example}")
                for error in result.errors:
                    print(f"    {error}")
    if not names:
        print("aucune directive à tester")
    print(f"\n{passed}/{total} exemples verts")
    return 1 if failures else 0


def cmd_explain(args: argparse.Namespace) -> int:
    engine = Engine(project=args.project)
    for error in engine.load_errors:
        print(f"! chargement : {error}")
    try:
        page = engine.render_page(args.file)
    except (OSError, ValueError) as exc:
        print(f"✗ {exc}")
        return 1
    print(f"{args.file} — « {page.title} »")
    if not page.blocks:
        print("  aucun bloc de directive")
    for report in page.blocks:
        mark = "" if report.known else "  [non compris]"
        print(f"  ligne {report.line:<4} {report.name} → {report.variant} ({report.reason}){mark}")
        for warning in report.warnings:
            print(f"             ! {warning}")
    other = [w for w in page.warnings if not w.startswith("ligne ")]
    for warning in other:
        print(f"  ! {warning}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    from mechamd.build import build

    report = build(args.project, args.output)
    for warning in report.warnings:
        print(f"! {warning}")
    if report.css_error:
        print(f"✗ CSS : {report.css_error}")
    print(f"{len(report.pages)} pages, {len(report.assets)} fichiers copiés")
    return 1 if report.css_error else 0


def cmd_serve(args: argparse.Namespace) -> int:  # pragma: no cover - lance un serveur
    from mechamd.serve import serve

    print(f"mechamd sert {args.project} sur http://{args.host}:{args.port}/")
    serve(args.project, args.host, args.port, reload=not args.no_reload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mecha", description="mechamd : Markdown → pages web.")
    parser.add_argument("--version", action="version", version=f"mechamd {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    test = sub.add_parser("test", help="exécute les exemples d'une ou de toutes les directives")
    test.add_argument("directive", nargs="?", help="nom de la directive (toutes par défaut)")
    test.add_argument("-p", "--project", default=".", help="dossier du projet (défaut : .)")
    test.set_defaults(func=cmd_test)

    explain = sub.add_parser(
        "explain", help="variante retenue et raison pour chaque bloc, plus les avertissements"
    )
    explain.add_argument("file", help="document mechamd (.md), relatif au projet")
    explain.add_argument("-p", "--project", default=".", help="dossier du projet (défaut : .)")
    explain.set_defaults(func=cmd_explain)

    build = sub.add_parser("build", help="construit un site statique")
    build.add_argument("project", nargs="?", default=".", help="dossier du projet (défaut : .)")
    build.add_argument("-o", "--output", help="dossier de sortie (défaut : <projet>/dist)")
    build.set_defaults(func=cmd_build)

    serve = sub.add_parser("serve", help="rendu live avec rechargement automatique")
    serve.add_argument("project", nargs="?", default=".", help="dossier du projet (défaut : .)")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--no-reload", action="store_true", help="sans rechargement (production)")
    serve.set_defaults(func=cmd_serve)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    code: int = args.func(args)
    return code


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
