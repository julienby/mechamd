from typing import Any

from mechamd import Block


def parse(block: Block) -> dict[str, Any]:
    return {"body": block.md(block.content)}
