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

## Quelle directive pour quelle intention

| Je veux… | Directive |
| --- | --- |
| un grand titre d'accueil, une zone de page | `section` (`.hero`) |
| des projets, des articles à parcourir | `card` dans un `grid` |
| quelques chiffres clés | `stats` |
| les points forts d'une offre | `features` |
| une équipe, des auteurs | `people` |
| des questions et réponses | `faq` (une seule : `details`) |
| des étapes à suivre | `steps` |
| un déroulé daté | `timeline` |
| une fiche technique (clé : valeur) | `specs` |
| comparer deux options | `compare` |
| une remarque, un conseil, un avertissement | `callout` |
| une citation, un témoignage | `quote` |
| des images | `figure` |
| des liens commentés | `links` |
| une liste de tâches | `todo` |
| inviter à agir (contact, essai) | `cta` |
| comparer des offres, des tarifs | `pricing` |
| un extrait de code ou une commande copiable | `code` |
| des boutons d'action (liens) | `buttons` (`.center`) |

## Construire une page

1. Un fichier `.md` par page ; frontmatter `title`, et `layout: page` pour un accueil
   (`article` par défaut). `layout: landing` (titre affiche + `lead:`) pour une page
   de vente, `layout: docs` (sommaire latéral) pour une documentation. `nav:`
   (`libellé: lien`) ajoute un menu à l'en-tête.
2. Écrire d'abord le texte en Markdown ; ajouter une directive seulement quand elle
   apporte une forme.
3. Commencer par la forme nue (`:::stats` sans attribut) : le moteur devine.
   N'ajouter `.variante` ou `clé=valeur` que pour corriger.
4. Page d'accueil type : `section.hero` (titre + lien), `stats` ou `features`, une
   `section` avec un `grid` de `card`, `faq`, puis `cta` en dernier.
5. Une liste de directive s'écrit « - élément : précision » ; le détail se met en
   lignes indentées dessous.
6. Lier les autres pages avec `[texte](autre.md)` : le lien devient `.html` à la
   construction.
7. Vérifier avec `mecha explain page.md` (variante retenue et avertissements par
   bloc), puis `mecha build`.

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
