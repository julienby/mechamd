"""`mecha build` : un dossier de documents → un site statique, déployable sans Python."""

from __future__ import annotations

import shutil
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

from mechamd.css import compile_css, copy_css, fonts_dir
from mechamd.engine import Engine

# Dossiers d'un projet qui ne sont pas du contenu.
SKIP_DIRS = {"directives", "theme", "dist", "node_modules", "__pycache__"}


@dataclass
class BuildReport:
    pages: list[Path] = field(default_factory=list)
    assets: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    css_error: str | None = None


def content_files(project: Path, out: Path) -> Iterator[Path]:
    """Fichiers de contenu du projet (documents et ressources), hors dossiers techniques."""
    for path in sorted(project.rglob("*")):
        rel = path.relative_to(project)
        if any(part.startswith(".") or part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if rel.name.startswith(".") or path.is_dir() or path.is_relative_to(out):
            continue
        yield path


def page_output(rel: Path) -> Path:
    """`notes/b204.md` → `notes/b204.html`."""
    return rel.with_suffix(".html")


def build(project: str | Path, out: str | Path | None = None) -> BuildReport:
    engine = Engine(project=project)
    target = Path(out).resolve() if out is not None else engine.project / "dist"
    report = BuildReport(warnings=[f"chargement : {e}" for e in engine.load_errors])

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    for path in content_files(engine.project, target):
        rel = path.relative_to(engine.project)
        if path.suffix == ".md":
            page = engine.render_page(rel)
            dest = target / page_output(rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page.html, encoding="utf-8")
            report.pages.append(rel)
            report.warnings.extend(f"{rel} : {w}" for w in page.warnings)
        else:
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            report.assets.append(rel)

    css = compile_css(engine)
    if css.error is None:
        copy_css(css, target / "_mecha" / "mecha.css")
    else:
        report.css_error = css.error
    fonts = fonts_dir(engine)
    if fonts is not None:
        shutil.copytree(fonts, target / "_mecha" / "fonts", dirs_exist_ok=True)
    return report
