"""compare : des options côte à côte, une colonne par titre."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block

# « ## Titre » ou « ## Titre ## »
_HEADING = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)(?:\s+#+)?\s*$")
# ouverture ou fermeture d'un bloc de code : ``` ou ~~~
_FENCE = re.compile(r"^\s*(```|~~~)")


def _columns(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Coupe le texte à chaque titre du niveau du premier ; ignore le code."""
    intro: list[str] = []
    columns: list[tuple[str, list[str]]] = []
    level = 0
    fence = ""
    for line in text.splitlines():
        match = None if fence else _HEADING.match(line)
        if match and (not level or len(match["level"]) <= level):
            level = level or len(match["level"])
            columns.append((match["title"], []))
            continue
        fence_match = _FENCE.match(line)
        if fence_match:
            fence = "" if fence == fence_match[1] else fence or fence_match[1]
        (columns[-1][1] if columns else intro).append(line)
    return "\n".join(intro), [(title, "\n".join(body)) for title, body in columns]


def parse(block: Block) -> dict[str, Any]:
    intro, columns = _columns(block.content)
    if len(columns) < 2:
        count = "aucune colonne" if not columns else "une seule colonne"
        block.warn(f"{count} : écrire un titre par option comparée")
    return {
        "intro": block.md(intro) if intro.strip() else "",
        "columns": [
            {"title": title, "body": block.md(body) if body.strip() else ""}
            for title, body in columns
        ],
    }
