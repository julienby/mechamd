"""specs : une fiche de caractéristiques « clé : valeur »."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import first_heading

# « clé : valeur » ou « clé | valeur », puce facultative ; « :// » (URL) n'est pas un séparateur.
_ROW = re.compile(r"^\s*(?:[-*+]\s+)?(?P<key>[^:|]+?)\s*(?::(?!//)|\|)\s*(?P<value>.+?)\s*$")


def parse(block: Block) -> dict[str, Any]:
    title, rest = first_heading(block.content)
    rows = []
    note = []
    for line in rest.splitlines():
        match = _ROW.match(line)
        if match:
            rows.append({"key": match["key"].strip("*_ "), "value": match["value"]})
        else:
            note.append(line)
    if not rows:
        block.warn("aucune caractéristique : écrire une ligne « clé : valeur » par caractéristique")
    text = "\n".join(note)
    return {
        "title": block.attrs.get("title") or title,
        "rows": rows,
        "note": block.md(text) if text.strip() else "",
    }
