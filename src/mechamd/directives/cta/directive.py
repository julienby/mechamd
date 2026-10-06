"""cta : un appel à l'action — titre, phrase, bouton."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import first_heading, trailing_link


def parse(block: Block) -> dict[str, Any]:
    title, rest = first_heading(block.content)
    action, rest = trailing_link(rest)
    if not block.content.strip():
        block.warn("appel à l'action vide : écrire un titre, une phrase et un lien final")
    elif action is None:
        block.warn("pas de bouton : terminer par une ligne « [texte](url) »")
    return {
        "title": title or "",
        "text": block.md(rest) if rest.strip() else "",
        "action": {"href": action.href, "text": action.text} if action else None,
    }
