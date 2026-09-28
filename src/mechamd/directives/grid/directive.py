"""grid : disposer des blocs en colonnes."""

from __future__ import annotations

from typing import Any

from mechamd import Block

MAX_AUTO_COLS = 3
MAX_COLS = 4


def parse(block: Block) -> dict[str, Any]:
    cols = None
    if "cols" in block.attrs:
        raw = block.attrs["cols"]
        if raw.isdigit() and 1 <= int(raw) <= MAX_COLS:
            cols = int(raw)
        else:
            block.warn(f"cols={raw} n'est pas un nombre entre 1 et {MAX_COLS} ; colonnes calculées")
    items = [
        {"name": c.name, "variant": c.variant, "id": c.id, "html": c.html} for c in block.children
    ]
    body = ""
    if not items:
        block.warn("grille sans bloc enfant : le contenu est affiché tel quel")
        body = block.md(block.content) if block.content.strip() else ""
    return {
        "cols": cols or max(1, min(len(items), MAX_AUTO_COLS)),
        "items": items,
        "body": body,
    }
