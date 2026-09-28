"""links : une liste de liens commentés, avec leur domaine."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlsplit

from mechamd import Block
from mechamd.helpers import split_items

# « [titre](url) », « <https://…> » ou « https://… » en tête d'élément
_MD_LINK = re.compile(r"^\[(?P<title>[^\]]+)\]\(\s*(?P<href>[^)\s]+)\s*\)")
_BARE = re.compile(r"^<?(?P<href>https?://[^\s>]+)>?")
# séparateur avant la description : « : », « | », « — », « -- » ou tiret demi-cadratin
_SEP = re.compile(r"^\s*(?:[:|—\u2013]|--)?\s*")


def _domain(href: str) -> str:
    host = urlsplit(href).hostname or ""
    return host.removeprefix("www.")


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucun lien : écrire une liste « - [titre](url) : description »")
    links = []
    for item in items:
        match = _MD_LINK.match(item.text) or _BARE.match(item.text)
        if match:
            href = match["href"]
            title = match.groupdict().get("title") or href.split("://", 1)[1]
            rest = _SEP.sub("", item.text[match.end() :], count=1)
        else:
            block.warn(f"« {item.text} » : pas de lien (écrire « [titre](url) : description »)")
            href, title, rest = "", item.text, ""
        description = "\n".join(part for part in (rest, item.body) if part)
        links.append(
            {
                "title": title.removeprefix("www.").rstrip("/"),
                "href": href,
                "domain": _domain(href),
                "description": block.md(description) if description else "",
            }
        )
    return {"intro": block.md(outside) if outside.strip() else "", "links": links}
