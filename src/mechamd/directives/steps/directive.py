"""steps : une procédure en étapes numérotées."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import split_items


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucune étape : écrire une liste « 1. étape »")
    steps = [
        {"title": block.md(item.text), "body": block.md(item.body) if item.body else ""}
        for item in items
    ]
    return {"intro": block.md(outside) if outside.strip() else "", "steps": steps}
