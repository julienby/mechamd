"""quote : une citation et son attribution."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block

# « — Marie Curie », « -- Marie Curie », ou tiret demi-cadratin (\u2013)
_CITE = re.compile(r"^\s*(?:—|\u2013|--)\s*(?P<cite>.+?)\s*$")
_MARK = re.compile(r"^\s*>\s?")


def parse(block: Block) -> dict[str, Any]:
    lines = [_MARK.sub("", line) for line in block.content.strip().splitlines()]
    cite = block.attrs.get("author", "")
    match = _CITE.match(lines[-1]) if lines else None
    if match:
        cite = cite or match["cite"]
        lines = lines[:-1]
    text = "\n".join(lines).strip()
    if not text:
        block.warn("citation vide : écrire le texte, puis « — auteur » sur la dernière ligne")
    return {"text": block.md(text) if text else "", "cite": block.md(cite) if cite else ""}
