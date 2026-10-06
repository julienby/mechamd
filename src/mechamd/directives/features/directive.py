"""features : des points forts en tuiles, titre et phrase."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import split_items

_FEATURE = re.compile(r"^(?P<title>[^:|]+?)\s*[:|]\s*(?P<text>.+)$")


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucun point : écrire une liste « - titre : phrase »")
    features = []
    for item in items:
        match = _FEATURE.match(item.text)
        title, text = (match["title"], match["text"]) if match else (item.text, "")
        if not text and not item.body:
            block.warn(f"« {item.text} » : ajouter « : une phrase » ou un texte indenté")
        description = "\n".join(part for part in (text, item.body) if part)
        features.append(
            {"title": title.strip("*_ "), "text": block.md(description) if description else ""}
        )
    return {"intro": block.md(outside) if outside.strip() else "", "features": features}
