"""Le contrat `Block` : ce que le noyau confie à une directive.

Ce module est le contrat entre le noyau et les directives. Toute modification
demande une validation humaine (voir AGENTS.md, « Escalade humaine »).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RenderedBlock:
    """Un bloc enfant déjà rendu, tel qu'un conteneur le reçoit dans `children`."""

    name: str
    variant: str
    id: str | None
    html: str


@dataclass
class Block:
    """Un bloc de directive repéré dans le document.

    Champs publics (le contrat) :

    - `name` : nom de la directive (`"card"`) ;
    - `variant` : variante écrite sur le bloc (`.cover`), ou `None` ;
    - `id` : ancre `#id` du bloc, ou `None` ;
    - `attrs` : attributs `clé=valeur` (chaînes) ;
    - `content` : source Markdown brute du contenu ;
    - `children` : blocs enfants déjà rendus (conteneurs de directives) ;
    - `md(text)` : Markdown → HTML ;
    - `warn(msg)` : signale un problème sans interrompre le rendu.
    """

    name: str
    variant: str | None = None
    id: str | None = None
    attrs: dict[str, str] = field(default_factory=dict)
    content: str = ""
    children: list[RenderedBlock] = field(default_factory=list)
    line: int = 1
    """Ligne (1-indexée) de l'ouverture du bloc dans le fichier source."""
    warnings: list[str] = field(default_factory=list)
    _render_md: Callable[[str], str] | None = field(default=None, repr=False, compare=False)

    def md(self, text: str) -> str:
        """Rend du Markdown (directives comprises) en HTML."""
        if self._render_md is None:
            from mechamd.markdown import render_plain

            return render_plain(text)
        return self._render_md(text)

    def warn(self, msg: str) -> None:
        """Signale un problème ; le rendu continue."""
        self.warnings.append(msg)
