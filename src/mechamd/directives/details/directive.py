"""details : un bloc repliable, fermé par défaut."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import first_heading

DEFAULT_SUMMARY = "Détails"


def parse(block: Block) -> dict[str, Any]:
    summary = block.attrs.get("summary")
    rest = block.content.strip()
    if not summary:
        summary, rest = first_heading(rest)
    if not summary and rest:
        summary, _, rest = rest.partition("\n")
    rest = rest.strip()
    if not rest:
        block.warn("rien à replier : écrire un titre, puis le texte")
    return {
        "summary": summary.strip() if summary else DEFAULT_SUMMARY,
        "body": block.md(rest) if rest else "",
    }
