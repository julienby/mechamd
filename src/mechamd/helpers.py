"""Helpers communs pour les directives : lire ce qui est évident dans un contenu.

Chaque helper rend ce qu'il a trouvé et le reste du texte, sans la partie lue.
Ils travaillent sur la source Markdown, ligne par ligne, et ignorent ce qui est
dans un bloc de code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^\s)>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
_LINK_LINE_RE = re.compile(r"^\s*\[([^\]]+)\]\(\s*<?([^\s)>]+)>?(?:\s+\"[^\"]*\")?\s*\)\s*$")
_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


@dataclass(frozen=True)
class Image:
    src: str
    alt: str


@dataclass(frozen=True)
class Link:
    href: str
    text: str


def _outside_code(lines: list[str]) -> list[bool]:
    """Pour chaque ligne : vrai si elle est hors d'un bloc de code clôturé."""
    flags: list[bool] = []
    fence: str | None = None
    for line in lines:
        match = _FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0] * len(match.group(1))
                flags.append(False)
            else:
                flags.append(True)
        else:
            flags.append(False)
            if match and match.group(1).startswith(fence):
                fence = None
    return flags


def _join(lines: list[str]) -> str:
    return "\n".join(lines).strip("\n")


def first_heading(text: str) -> tuple[str | None, str]:
    """Premier titre (`#` à `######`) : rend (titre, reste)."""
    lines = text.splitlines()
    for k, (line, ok) in enumerate(zip(lines, _outside_code(lines), strict=True)):
        match = _HEADING_RE.match(line) if ok else None
        if match and match.group(2):
            return match.group(2), _join(lines[:k] + lines[k + 1 :])
    return None, text.strip("\n")


def first_image(text: str) -> tuple[Image | None, str]:
    """Première image Markdown : rend (image, reste). Une ligne vidée est retirée."""
    lines = text.splitlines()
    for k, (line, ok) in enumerate(zip(lines, _outside_code(lines), strict=True)):
        match = _IMAGE_RE.search(line) if ok else None
        if match:
            rest = f"{line[: match.start()].rstrip()} {line[match.end() :].lstrip()}".strip()
            new = [*lines[:k], rest] if rest else lines[:k]
            return Image(src=match.group(2), alt=match.group(1)), _join(new + lines[k + 1 :])
    return None, text.strip("\n")


def trailing_link(text: str) -> tuple[Link | None, str]:
    """Lien seul sur la dernière ligne non vide : rend (lien, reste)."""
    lines = text.rstrip().splitlines()
    if not lines or not _outside_code(lines)[-1]:
        return None, text.strip("\n")
    match = _LINK_LINE_RE.match(lines[-1])
    if match is None:
        return None, text.strip("\n")
    return Link(href=match.group(2), text=match.group(1).strip()), _join(lines[:-1])
