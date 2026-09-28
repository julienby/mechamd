"""timeline : une chronologie écrite comme une liste « date : titre »."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import parse_date, split_items

_SEPARATORS = re.compile(r"[:|]")


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucun élément : écrire une liste « - date : titre »")
    parsed = []
    for item in items:
        date = title = None
        for match in _SEPARATORS.finditer(item.text):
            found = parse_date(item.text[: match.start()])
            if found is not None:
                date, title = found, item.text[match.end() :].strip()
                break
        if date is None:
            block.warn(f"ligne {block.line + item.line} : date non reconnue dans « {item.text} »")
        parsed.append(
            {
                "date": date.text if date else None,
                "datetime": date.iso if date else None,
                "title": title if date else item.text,
                "body": block.md(item.body) if item.body else "",
            }
        )
    return {"intro": block.md(outside) if outside.strip() else "", "items": parsed}
