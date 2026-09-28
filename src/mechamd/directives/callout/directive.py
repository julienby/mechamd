"""callout : un encadré d'information (info, astuce, attention)."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block
from mechamd.helpers import first_heading

# Premier mot reconnu → (étiquette affichée, variante devinée)
LABELS: dict[str, tuple[str, str | None]] = {
    "astuce": ("Astuce", "tip"),
    "attention": ("Attention", "warning"),
    "note": ("Note", None),
    "info": ("Info", None),
}

# « Attention : », « **Attention** : », « **Attention :** », « attention: »
_LABEL_RE = re.compile(
    r"^\s*(?P<strong>\*\*|__)?(?P<word>[^\W\d_]+)\s*(?P=strong)?\s*:\s*(?P=strong)?\s*"
)


def parse(block: Block) -> dict[str, Any]:
    title, rest = first_heading(block.content)
    label = kind = None
    match = _LABEL_RE.match(rest)
    if match and match.group("word").lower() in LABELS:
        label, kind = LABELS[match.group("word").lower()]
        rest = rest[match.end() :]
        rest = rest[:1].upper() + rest[1:]
    if not rest.strip() and not title:
        block.warn("encadré vide")
    return {
        "label": label,
        "kind": kind,
        "title": title,
        "body": block.md(rest) if rest.strip() else "",
    }


def infer_variant(data: dict[str, Any]) -> str | None:
    kind: str | None = data["kind"]
    return kind
