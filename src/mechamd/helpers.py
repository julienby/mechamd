"""Helpers communs pour les directives : lire ce qui est évident dans un contenu.

Chaque helper rend ce qu'il a trouvé et le reste du texte, sans la partie lue.
Ils travaillent sur la source Markdown, ligne par ligne, et ignorent ce qui est
dans un bloc de code.
"""

from __future__ import annotations

import re
import textwrap
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


# --- dates approximatives ------------------------------------------------

MONTHS = {
    "janvier": 1, "janv": 1, "jan": 1,
    "février": 2, "fevrier": 2, "févr": 2, "fevr": 2, "fév": 2, "fev": 2,
    "mars": 3,
    "avril": 4, "avr": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7, "juil": 7,
    "août": 8, "aout": 8,
    "septembre": 9, "sept": 9, "sep": 9,
    "octobre": 10, "oct": 10,
    "novembre": 11, "nov": 11,
    "décembre": 12, "decembre": 12, "déc": 12, "dec": 12,
}  # fmt: skip

_YEAR = r"(?P<y>\d{4})"
_DATE_PATTERNS = [
    re.compile(rf"^{_YEAR}$"),
    re.compile(rf"^{_YEAR}-(?P<m>\d{{1,2}})(?:-(?P<d>\d{{1,2}}))?$"),
    re.compile(rf"^(?P<d>\d{{1,2}})[/.](?P<m>\d{{1,2}})[/.]{_YEAR}$"),
    re.compile(rf"^(?P<m>\d{{1,2}})[/.]{_YEAR}$"),
    re.compile(rf"^(?:(?P<d>\d{{1,2}})(?:er)?\s+)?(?P<mn>[^\W\d_]+)\.?\s+{_YEAR}$"),
]


@dataclass(frozen=True)
class ApproxDate:
    """Une date telle qu'écrite, avec sa forme ISO à la précision connue."""

    text: str
    iso: str
    """`2024`, `2025-03` ou `2026-09-12` : utilisable dans `<time datetime=…>`."""
    precision: str
    """`year`, `month` ou `day`."""


def parse_date(text: str) -> ApproxDate | None:
    """Lit « 2024 », « mars 2025 », « 12 mars 2025 », « 12/09/2026 », « 2026-09-12 »."""
    raw = text.strip()
    for pattern in _DATE_PATTERNS:
        match = pattern.match(raw.lower())
        if match is None:
            continue
        parts = match.groupdict()
        year = int(parts["y"])
        month_name = parts.get("mn")
        if month_name is not None:
            month: int | None = MONTHS.get(month_name)
            if month is None:
                return None
        else:
            month = int(parts["m"]) if parts.get("m") else None
        day = int(parts["d"]) if parts.get("d") else None
        if month is not None and not 1 <= month <= 12:
            return None
        if day is not None and not 1 <= day <= 31:
            return None
        if month is None:
            return ApproxDate(raw, f"{year:04d}", "year")
        if day is None:
            return ApproxDate(raw, f"{year:04d}-{month:02d}", "month")
        return ApproxDate(raw, f"{year:04d}-{month:02d}-{day:02d}", "day")
    return None


# --- listes ---------------------------------------------------------------

_ITEM_RE = re.compile(r"^(?P<indent> {0,3})(?:[-*+]|\d{1,9}[.)])(?:[ \t]+(?P<text>.*))?$")


@dataclass(frozen=True)
class Item:
    """Un élément de liste : sa première ligne, puis la suite (désindentée)."""

    text: str
    body: str
    line: int
    """Ligne de l'élément dans le texte (1-indexée)."""


def split_items(text: str) -> tuple[list[Item], str]:
    """Éléments de premier niveau d'une liste Markdown ; rend (éléments, texte hors liste).

    Les lignes indentées qui suivent un élément forment son `body`. Les lignes non
    indentées qui ne sont pas des éléments sont rendues à part, dans l'ordre.
    """
    items: list[Item] = []
    outside: list[str] = []
    head: str | None = None
    head_line = 0
    body: list[str] = []

    def flush() -> None:
        if head is not None:
            items.append(Item(head.strip(), textwrap.dedent("\n".join(body)).strip(), head_line))

    lines = text.splitlines()
    for k, (line, ok) in enumerate(zip(lines, _outside_code(lines), strict=True)):
        match = _ITEM_RE.match(line) if ok else None
        if match:
            flush()
            head, head_line, body = match.group("text") or "", k + 1, []
        elif head is not None and (not line.strip() or line[:1] in (" ", "\t") or not ok):
            body.append(line)
        else:
            flush()
            head, body = None, []
            outside.append(line)
    flush()
    return items, "\n".join(outside).strip("\n")


# --- ancres ----------------------------------------------------------------


def slugify(text: str) -> str:
    """Ancre lisible : « Salle B204 : bilan » → `salle-b204-bilan` (accents gardés)."""
    words = re.findall(r"[^\W_]+", text.lower())
    return "-".join(words)
