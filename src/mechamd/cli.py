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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mecha", description="mechamd : Markdown → pages web.")
    parser.add_argument("--version", action="version", version=f"mechamd {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    test = sub.add_parser("test", help="exécute les exemples d'une ou de toutes les directives")
    test.add_argument("directive", nargs="?", help="nom de la directive (toutes par défaut)")
    test.add_argument("-p", "--project", default=".", help="dossier du projet (défaut : .)")
    test.set_defaults(func=cmd_test)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    code: int = args.func(args)
    return code


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
