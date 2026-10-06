"""buttons : une rangée de boutons — le premier plein, les suivants discrets."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block

_LINK = re.compile(r"^\s*(?:[-*+]\s+)?\[([^\]]+)\]\(\s*<?([^\s)>]+)>?(?:\s+\"[^\"]*\")?\s*\)\s*$")


def parse(block: Block) -> dict[str, Any]:
    links = []
    for line in block.content.splitlines():
        match = _LINK.match(line)
        if match:
            links.append({"text": match[1], "href": match[2]})
        elif line.strip():
            block.warn(f"« {line.strip()} » ignoré : une ligne « [texte](url) » par bouton")
    if not links:
        block.warn("aucun bouton : écrire une ligne « [texte](url) » par bouton")
    return {"links": links}
