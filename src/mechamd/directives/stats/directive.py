"""stats : quelques chiffres clés en tuiles."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import split_items

_STAT = re.compile(r"^(?P<value>[^:|]+?)\s*[:|]\s*(?P<label>.+)$")


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucun chiffre : écrire une liste « - valeur : libellé »")
    stats = []
    for item in items:
        match = _STAT.match(item.text)
        if match:
            value, label = match["value"], match["label"]
        else:
            block.warn(f"« {item.text} » : écrire « valeur : libellé »")
            value, label = item.text, ""
        detail = block.md(item.body) if item.body else ""
        stats.append({"value": value.strip("*_ "), "label": label, "detail": detail})
    return {"intro": block.md(outside) if outside.strip() else "", "stats": stats}
