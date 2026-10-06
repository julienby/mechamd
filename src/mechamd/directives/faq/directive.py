"""faq : des questions et leurs réponses, repliables."""

from __future__ import annotations

from typing import Any

from mechamd import Block
from mechamd.helpers import split_items


def parse(block: Block) -> dict[str, Any]:
    items, outside = split_items(block.content)
    if not items:
        block.warn(
            "aucune question : écrire une liste « - question » suivie de sa réponse indentée"
        )
    questions = []
    for item in items:
        if not item.body:
            block.warn(f"« {item.text} » : pas de réponse (l'indenter sous la question)")
        questions.append(
            {"question": item.text, "answer": block.md(item.body) if item.body else ""}
        )
    return {"intro": block.md(outside) if outside.strip() else "", "questions": questions}
