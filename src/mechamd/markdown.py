"""Configuration de markdown-it : CommonMark + GFM + conteneurs de directives."""

from __future__ import annotations

from functools import cache

from markdown_it import MarkdownIt
from mdit_py_plugins.container import container_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

from mechamd.attrs import is_directive_info

DIRECTIVE_OPEN = "container_directive_open"
DIRECTIVE_CLOSE = "container_directive_close"


def _validate(params: str, *_: object) -> bool:
    return is_directive_info(params)


def create_md() -> MarkdownIt:
    """Un parseur Markdown : HTML brut désactivé, tableaux, barré, cases à cocher."""
    md = MarkdownIt("commonmark", {"html": False, "typographer": False})
    md.enable(["table", "strikethrough"])
    md.use(tasklists_plugin)
    md.use(container_plugin, name="directive", validate=_validate)
    return md


@cache
def _plain() -> MarkdownIt:
    return create_md()


def render_plain(text: str) -> str:
    """Rend du Markdown sans moteur (directives rendues comme de simples `div`)."""
    return str(_plain().render(text))
