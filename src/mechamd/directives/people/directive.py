"""people : une équipe ou des intervenants — nom, rôle, présentation."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import split_items

_PERSON = re.compile(r"^(?P<name>[^:|—]+?)\s*(?:[:|—]|--)\s*(?P<role>.+)$")


def _initials(name: str) -> str:
    words = re.findall(r"[^\W\d_]+", name)
    return "".join(word[0] for word in words[:2]).upper()


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn("aucune personne : écrire une liste « - Nom : rôle »")
    people = []
    for item in items:
        match = _PERSON.match(item.text)
        name, role = (match["name"], match["role"]) if match else (item.text, "")
        name = name.strip("*_ ")
        if not role:
            block.warn(f"« {item.text} » : écrire « Nom : rôle »")
        people.append(
            {
                "name": name,
                "role": role,
                "initials": _initials(name),
                "bio": block.md(item.body) if item.body else "",
            }
        )
    return {"intro": block.md(outside) if outside.strip() else "", "people": people}
