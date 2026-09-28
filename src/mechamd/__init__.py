"""mechamd : du Markdown avec directives vers des pages web Tailwind."""

from importlib.metadata import version

from mechamd.block import Block, RenderedBlock
from mechamd.engine import BlockReport, Engine, Page

__all__ = ["Block", "BlockReport", "Engine", "Page", "RenderedBlock"]
__version__ = version("mechamd")
