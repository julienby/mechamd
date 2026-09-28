# specs

**Rôle** : une fiche de caractéristiques « clé : valeur » (capteur, matériel,
paramètres d'une manip).

## Syntaxe

```markdown
:::specs
### Sonde DS18B20
- Plage : -55 à 125 °C
- Précision : ±0,5 °C
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `title` | premier titre du bloc (`#` à `######`) | `title=` |
| `rows[].key`, `rows[].value` | chaque ligne « clé : valeur » ou « clé \| valeur », avec ou sans puce | — |
| `note` | les autres lignes, rendues en HTML | — |

Le séparateur est le premier `:` ou `|` de la ligne (espaces facultatifs) ; `://`
(une URL) n'en est pas un. La clé perd son gras (`**Poids**`). La valeur reste du
texte simple. Pas de variante devinée.

Avertissement : aucune caractéristique.

## Variantes

- `default` : fiche encadrée, clé à gauche et valeur à droite (empilées sur mobile).
- `inline` : caractéristiques en pastilles, pour quelques paramètres en tête de note.

## Attributs

- `title=` : remplace le titre lu dans le contenu.

## Exemples

Voir `examples/` : `nu` (cas nu), `inline` (explicite, séparateur `|`),
`mal-ecrit` (séparateurs mélangés, clé en gras, URL, `title=`), `vide`.
