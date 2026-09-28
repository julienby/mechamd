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

## Utilisation

```sh
mecha serve mon-site/          # rendu live, rechargement automatique
mecha build mon-site/ -o dist/ # site statique
mecha explain doc.md -p mon-site/  # variante retenue et raison pour chaque bloc
```

Mise en page choisie dans le frontmatter : `layout: article` (défaut, avec
sommaire, date et tags), `page` (sans sommaire ni méta) ou `notes` (compact).
Un projet ajoute un layout dans `theme/layouts/<nom>.html`.

Directives fournies : `card`, `grid`, `callout`, `timeline`, `section` (voir le
`README.md` de chacune dans `src/mechamd/directives/`). La vitrine
(`showcase/index.md`) les montre toutes : `mecha serve showcase`.

## Développement

```sh
uv sync
uv run mecha test      # exemples des directives
uv run pytest          # tests du noyau
uv run ruff check . && uv run mypy
```
