"""section : une grande partie de page, avec son ancre."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import first_heading, slugify, trailing_link

DEFAULT_ACTION = "Ouvrir"


def parse(block: Block) -> dict[str, Any]:
    title, rest = first_heading(block.content)
    title = block.attrs.get("title") or title
    link, rest = trailing_link(rest)
    anchor = block.id or (slugify(title) if title else None) or None
    if anchor is None:
        block.warn("section sans titre : ajouter un titre `##` ou un #id pour avoir une ancre")
    href = block.attrs.get("href") or (link.href if link else None)
    return {
        "title": title,
        "anchor": anchor,
        "image": block.attrs.get("image"),
        "alt": block.attrs.get("alt", ""),
        "href": href,
        "action": link.text if link else (DEFAULT_ACTION if href else None),
        "body": block.md(rest) if rest.strip() else "",
    }
