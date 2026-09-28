"""Découverte et chargement des directives (un dossier par directive)."""

from __future__ import annotations

import hashlib
import importlib.util
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from mechamd.block import Block

BUILTIN_DIR = Path(__file__).parent / "directives"

ParseFn = Callable[[Block], dict[str, Any]]
InferFn = Callable[[dict[str, Any]], str | None]


class DirectiveError(Exception):
    """Une directive ne respecte pas le contrat (dossier mal formé)."""


@dataclass
class Directive:
    name: str
    path: Path
    parse: ParseFn
    infer_variant: InferFn | None

    @property
    def templates_dir(self) -> Path:
        return self.path / "templates"

    @property
    def examples_dir(self) -> Path:
        return self.path / "examples"

    @property
    def variants(self) -> list[str]:
        """Variantes disponibles : une par template (`default` en tête)."""
        names = sorted(p.stem for p in self.templates_dir.glob("*.html"))
        return sorted(names, key=lambda n: n != "default")

    def examples(self) -> list[Path]:
        return sorted(self.examples_dir.glob("*.md"))


def _load_module(path: Path, name: str) -> ModuleType:
    digest = hashlib.sha1(str(path).encode()).hexdigest()[:8]
    spec = importlib.util.spec_from_file_location(f"mechamd_directive_{name}_{digest}", path)
    if spec is None or spec.loader is None:  # pragma: no cover - chemin toujours valide
        raise DirectiveError(f"{name} : impossible de charger {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_directive(path: Path) -> Directive:
    """Charge le dossier d'une directive et vérifie le contrat minimal."""
    name = path.name
    source = path / "directive.py"
    if not source.is_file():
        raise DirectiveError(f"{name} : directive.py manquant")
    if not (path / "templates" / "default.html").is_file():
        raise DirectiveError(f"{name} : templates/default.html manquant")
    module = _load_module(source, name.replace("-", "_"))
    parse = getattr(module, "parse", None)
    if not callable(parse):
        raise DirectiveError(f"{name} : directive.py doit définir parse(block)")
    infer = getattr(module, "infer_variant", None)
    return Directive(
        name=name,
        path=path,
        parse=parse,
        infer_variant=infer if callable(infer) else None,
    )


def discover(dirs: Iterable[Path]) -> tuple[dict[str, Directive], list[str]]:
    """Découvre les directives ; le premier dossier qui fournit un nom gagne.

    Rend les directives et la liste des erreurs de chargement (jamais levées :
    une directive cassée est ignorée, ses blocs s'affichent comme inconnus).
    """
    found: dict[str, Directive] = {}
    errors: list[str] = []
    for root in dirs:
        if not root.is_dir():
            continue
        for path in sorted(root.iterdir()):
            if not path.is_dir() or path.name.startswith(("_", ".")) or path.name in found:
                continue
            try:
                found[path.name] = load_directive(path)
            except Exception as exc:
                errors.append(
                    str(exc) if isinstance(exc, DirectiveError) else f"{path.name} : {exc}"
                )
    return found, errors
