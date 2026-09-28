from typing import Any

from mechamd import Block


def parse(block: Block) -> dict[str, Any]:
    if block.attrs.get("boom"):
        raise RuntimeError("boum")
    if block.attrs.get("notdict"):
        return "pas un dict"  # type: ignore[return-value]
    text = block.content.strip()
    if not text:
        block.warn("bloc vide")
    return {
        "text": text,
        "children": [c.html for c in block.children],
        "guess": block.attrs.get("guess") or ("alt" if text.startswith("alt") else None),
    }


def infer_variant(data: dict[str, Any]) -> str | None:
    if data["guess"] == "crash":
        raise ValueError("devinette cassée")
    guess: str | None = data["guess"]
    return guess
