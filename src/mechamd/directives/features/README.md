# features

**Rôle** : les points forts d'un projet ou d'une offre, une tuile par point.

## Syntaxe

```markdown
:::features
- Sans réglage : le moteur devine la présentation.
- Statique : du HTML à héberger n'importe où.
- Lisible : un fichier Markdown reste un texte.
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `features[].title` | le texte avant `:` ou `\|`, sans le gras | — |
| `features[].text` | le texte après `:` ou `\|`, puis les lignes indentées, rendus en HTML | — |
| `intro` | le texte hors de la liste, rendu en HTML | — |

Les colonnes suivent le nombre de points (1, 2, puis 3 au plus). Pas de variante devinée.
Pour des chiffres, utiliser `stats` ; pour des étapes ordonnées, `steps`.

Avertissements : aucun point ; point sans phrase (gardé, titre seul).

## Variantes

- `default` : une tuile par point (titre, phrase).

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `gras` (titres en gras, texte indenté),
`mal-ecrit` (point sans phrase, variante inconnue), `vide`.
