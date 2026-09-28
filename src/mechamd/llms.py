"""`llms.txt` : la syntaxe mechamd et le README de chaque directive, pour un LLM (llmstxt.org)."""

from __future__ import annotations

from mechamd.directive import BUILTIN_DIR
from mechamd.engine import Engine

INTRO = """\
# mechamd

> mechamd transforme du Markdown avec directives (`:::nom{attrs}`) en pages web soignées.
> Le cas normal est une directive sans attribut : le moteur devine la présentation.

## Syntaxe

Un document est un fichier `.md` ordinaire : frontmatter optionnel (`title`, `date`,
`tags`, `layout: article | page | notes`), Markdown, et des directives conteneurs :

```markdown
:::nom{.variante #id clé=valeur}
contenu Markdown
:::
```

- Pour imbriquer, le parent prend plus de `:` que ses enfants (`::::grid` contient des `:::card`).
- `.variante` choisit une présentation ; `#id` pose une ancre ; `clé=valeur` règle la directive.
- Variante retenue : celle écrite sur le bloc, sinon celle fixée par le parent
  (`::::grid{card=cover}`), sinon celle devinée, sinon `default`.
  Une variante demandée mais inexistante retombe sur la variante devinée, avec un avertissement.
- Une directive inconnue ou mal écrite ne casse pas la page : son contenu reste lisible.

Les sections suivantes sont les README des directives disponibles.
"""


def shift_headings(markdown: str) -> str:
    """Descend chaque titre d'un niveau, sauf dans les blocs de code."""
    lines = []
    in_code = False
    for line in markdown.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        elif not in_code and line.startswith("#"):
            line = "#" + line
        lines.append(line)
    return "\n".join(lines)


def generate(engine: Engine) -> str:
    """Directives du projet d'abord, puis directives fournies ; ordre alphabétique."""
    directives = sorted(
        engine.directives.values(), key=lambda d: (d.path.is_relative_to(BUILTIN_DIR), d.name)
    )
    parts = [INTRO]
    for directive in directives:
        readme = directive.path / "README.md"
        if readme.is_file():
            parts.append(shift_headings(readme.read_text(encoding="utf-8").strip()) + "\n")
    return "\n".join(parts)
