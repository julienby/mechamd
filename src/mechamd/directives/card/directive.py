"""card : un bloc de contenu autonome (titre, image, texte, lien d'action)."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import first_heading, first_image, trailing_link

DEFAULT_ACTION = "Ouvrir"


def parse(block: Block) -> dict[str, Any]:
    image, rest = first_image(block.content)
    title, rest = first_heading(rest)
    link, rest = trailing_link(rest)
    if not block.content.strip():
        block.warn("carte vide")

    href = block.attrs.get("href") or (link.href if link else None)
    action = link.text if link else (DEFAULT_ACTION if href else None)
    return {
        "title": block.attrs.get("title") or title,
        "image": block.attrs.get("image") or (image.src if image else None),
        "alt": image.alt if image else "",
        "href": href,
        "action": action,
        "body": block.md(rest) if rest.strip() else "",
    }


def infer_variant(data: dict[str, Any]) -> str | None:
    return "image" if data["image"] else None
