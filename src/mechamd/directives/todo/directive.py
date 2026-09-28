"""todo : une liste de tâches cochées ou non, avec l'avancement."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import split_items

# « [ ] tâche », « [x] tâche », « [X] tâche », « [] tâche »
_BOX = re.compile(r"^\[(?P<mark>[ xX]?)\]\s*(?P<text>.*)$")


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucune tâche : écrire une liste « - [ ] tâche »")
    tasks = []
    for item in items:
        match = _BOX.match(item.text)
        if match:
            done, text = match["mark"] in ("x", "X"), match["text"]
        else:
            block.warn(f"« {item.text} » : pas de case, comptée à faire (écrire « - [ ] tâche »)")
            done, text = False, item.text
        detail = block.md(item.body) if item.body else ""
        tasks.append({"done": done, "text": block.md(text), "detail": detail})
    return {
        "intro": block.md(outside) if outside.strip() else "",
        "items": tasks,
        "done": sum(task["done"] for task in tasks),
        "total": len(tasks),
    }
