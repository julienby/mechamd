# mechamd

mechamd transforme des notes Markdown spontanées en beaux documents web :
pages de doc, billets de blog, fiches de suivi d'expérience, doc de laboratoire.

```markdown
:::card
### Capteur DS18B20
Sonde de température étanche, précision ±0,5 °C.
[Voir la fiche](ds18b20.md)
:::
```

Voir [`SPEC.md`](SPEC.md) pour la spécification, [`AGENTS.md`](AGENTS.md) pour
les règles de contribution et [`PROGRESS.md`](PROGRESS.md) pour l'avancement.

## Installation

```sh
uv tool install git+https://github.com/julienby/mechamd
# sans installer : uvx --from git+https://github.com/julienby/mechamd mecha build mon-site/
```

Au premier `build` ou `serve`, mechamd télécharge le binaire Tailwind CSS (réseau requis une fois).

## Utilisation

```sh
mecha serve mon-site/          # rendu live, rechargement automatique
mecha build mon-site/ -o dist/ # site statique
mecha explain doc.md -p mon-site/  # variante retenue et raison pour chaque bloc
mecha llms -p mon-site/        # syntaxe et directives, à donner à un LLM
```

[`llms.txt`](llms.txt) contient la syntaxe et le README de chaque directive fournie.

Mise en page choisie dans le frontmatter : `layout: article` (défaut, avec
sommaire, date et tags), `page` (sans sommaire ni méta) ou `notes` (compact).
Un projet ajoute un layout dans `theme/layouts/<nom>.html`.

Directives fournies : `card`, `grid`, `callout`, `timeline`, `section`, `figure`,
`steps`, `specs`, `stats`, `quote`, `details`, `todo`, `links`, `compare` (voir le `README.md` de chacune dans
`src/mechamd/directives/`). La vitrine
(`showcase/index.md`) les montre toutes : `mecha serve showcase`.

## Développement

```sh
uv sync
uv run mecha test      # exemples des directives
uv run pytest          # tests du noyau
uv run ruff check .
uv run mecha llms > llms.txt   # après un changement de README de directive
```

## Versions

Mettre à jour `version` dans `pyproject.toml`, CI verte, puis `git tag vX.Y.Z && git push origin vX.Y.Z`.
mechamd n'est pas publié sur PyPI (ADR 0008).
