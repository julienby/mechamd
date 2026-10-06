"""code : un bloc de code présenté — nom de fichier, bouton « copier »."""

from __future__ import annotations

import re
from typing import Any

from mechamd import Block

_FENCE = re.compile(
    r"^ {0,3}(?P<fence>`{3,}|~{3,})[ \t]*(?P<lang>[\w+#.-]*)[ \t]*(?:\{(?P<attrs>[^}]*)\})?[ \t]*\n"
    r"(?P<code>.*?)^ {0,3}(?P=fence)[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
_TITLE = re.compile(r"title=(?:\"([^\"]*)\"|(\S+))")


def parse(block: Block) -> dict[str, Any]:
    snippets = []
    for match in _FENCE.finditer(block.content):
        title = _TITLE.search(match["attrs"] or "")
        snippets.append(
            {
                "title": (title[1] or title[2]) if title else "",
                "lang": match["lang"],
                "code": match["code"].rstrip("\n"),
            }
        )
    if not snippets:
        block.warn("aucun code : écrire un bloc clôturé par trois accents graves")
    elif len(snippets) == 1 and not snippets[0]["title"]:
        snippets[0]["title"] = block.attrs.get("file", "")
    return {"snippets": snippets}
