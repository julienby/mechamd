# people

**Rôle** : une équipe, des intervenants ou des auteurs : nom, rôle, courte présentation.

## Syntaxe

```markdown
:::people
- Camille Durand : biologiste
  Responsable des manips.
- Alex Martin : électronicien
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `people[].name` | le texte avant `:`, `\|` ou `—`, sans le gras | — |
| `people[].role` | le texte après le séparateur | — |
| `people[].initials` | les initiales des deux premiers mots du nom (pastille) | — |
| `people[].bio` | les lignes indentées, rendues en HTML | — |
| `intro` | le texte hors de la liste, rendu en HTML | — |

Les colonnes suivent le nombre de personnes (1, 2, puis 3 au plus). Pas de variante devinée.

Avertissements : aucune personne ; personne sans rôle (gardée, nom seul).

## Variantes

- `default` : une carte par personne, pastille d'initiales.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `bio` (présentations indentées, séparateur `|`),
`mal-ecrit` (nom seul, variante inconnue), `vide`.
