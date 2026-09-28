"""figure : une ou plusieurs images avec leur légende."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import first_image

HINT = "écrire ![description](chemin)"


def parse(block: Block) -> dict[str, Any]:
    images = []
    image, rest = first_image(block.content)
    while image is not None:
        if not image.alt:
            block.warn(f"image « {image.src} » sans texte alternatif : {HINT}")
        images.append({"src": image.src, "alt": image.alt})
        image, rest = first_image(rest)
    if not images:
        block.warn(f"aucune image : {HINT}")
    return {"images": images, "caption": block.md(rest) if rest.strip() else ""}


def infer_variant(data: dict[str, Any]) -> str | None:
    return "gallery" if len(data["images"]) > 1 else None
