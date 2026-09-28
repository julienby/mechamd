"""Lecture de la ligne d'ouverture d'une directive : `nom{.variante #id clé=valeur}`."""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass, field

NAME_RE = re.compile(r"^[A-Za-z][\w-]*")
_KEY_RE = re.compile(r"^[A-Za-z_][\w-]*$")


@dataclass
class Info:
    name: str
    variant: str | None = None
    id: str | None = None
    attrs: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def is_directive_info(params: str) -> bool:
    """Vrai si la ligne après `:::` commence par un nom de directive."""
    return NAME_RE.match(params.strip()) is not None


def parse_info(params: str) -> Info:
    """Découpe `card{.cover #x titre="Mon titre"}` ; tolérant, ne lève jamais."""
    text = params.strip()
    match = NAME_RE.match(text)
    if match is None:  # pragma: no cover - filtré par is_directive_info
        return Info(name="", warnings=[f"nom de directive illisible : {text!r}"])
    info = Info(name=match.group(0).lower())
    rest = text[match.end() :].strip()
    if not rest:
        return info
    if not rest.startswith("{"):
        info.warnings.append(f"texte ignoré après le nom : {rest!r}")
        return info
    end = rest.rfind("}")
    if end == -1:
        info.warnings.append("accolade fermante manquante dans les attributs")
        inner = rest[1:]
    else:
        inner = rest[1:end]
        if rest[end + 1 :].strip():
            info.warnings.append(f"texte ignoré après les attributs : {rest[end + 1 :].strip()!r}")
    _parse_attrs(inner, info)
    return info


def _parse_attrs(inner: str, info: Info) -> None:
    try:
        parts = shlex.split(inner, posix=True)
    except ValueError:
        info.warnings.append("guillemet non fermé dans les attributs")
        parts = inner.replace('"', " ").replace("'", " ").split()
    for part in parts:
        if part.startswith(".") and len(part) > 1:
            if info.variant is None:
                info.variant = part[1:]
            else:
                info.warnings.append(f"une seule variante par bloc : {part!r} ignorée")
        elif part.startswith("#") and len(part) > 1:
            if info.id is None:
                info.id = part[1:]
            else:
                info.warnings.append(f"un seul id par bloc : {part!r} ignoré")
        elif "=" in part:
            key, value = part.split("=", 1)
            if _KEY_RE.match(key):
                info.attrs[key] = value
            else:
                info.warnings.append(f"attribut illisible : {part!r}")
        else:
            info.warnings.append(f"attribut illisible : {part!r}")
