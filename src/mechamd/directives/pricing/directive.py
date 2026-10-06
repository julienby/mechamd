"""pricing : des offres côte à côte — nom, prix, points, bouton."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import split_items, trailing_link

_HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(?P<text>.+?)[ \t]*$")
_PRICE = re.compile(r"^(?P<amount>.+?)\s*(?P<period>/\s*\S+)?$")


def _plan(block: Block, heading: str, body: str) -> dict[str, Any]:
    name, sep, price = heading.partition(":")
    if not sep:
        block.warn(f"« {heading} » : écrire « Nom : prix »")
    amount, period = price.strip(), ""
    match = _PRICE.match(amount)
    if match:
        amount, period = match["amount"], (match["period"] or "").replace(" ", "")
    action, rest = trailing_link(body)
    items, _ = split_items(rest)
    return {
        "name": name.strip("*_ "),
        "amount": amount,
        "period": period,
        "points": [
            block.md(item.text).strip().removeprefix("<p>").removesuffix("</p>") for item in items
        ],
        "action": {"href": action.href, "text": action.text} if action else None,
    }


def parse(block: Block) -> dict[str, Any]:
    chunks: list[tuple[str, list[str]]] = []
    for line in block.content.splitlines():
        match = _HEADING.match(line)
        if match:
            chunks.append((match["text"], []))
        elif chunks:
            chunks[-1][1].append(line)
    if not chunks:
        block.warn("aucune offre : écrire un titre « ## Nom : prix » par offre")
    plans = [_plan(block, heading, "\n".join(body)) for heading, body in chunks]
    wanted = block.attrs.get("recommended", "").strip().lower()
    for plan in plans:
        plan["recommended"] = bool(wanted) and plan["name"].lower() == wanted
    if wanted and not any(plan["recommended"] for plan in plans):
        block.warn(f"recommended={wanted} : aucune offre de ce nom")
    return {"plans": plans}
