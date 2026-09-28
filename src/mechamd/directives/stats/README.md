# stats

**Rôle** : quelques chiffres clés mis en avant (bilan de manip, résumé de billet).

## Syntaxe

```markdown
:::stats
- 48 h : d'acquisition
- 3 : sondes DS18B20
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `stats[].value`, `stats[].label` | chaque élément de liste « valeur : libellé » ou « valeur \| libellé » | — |
| `stats[].detail` | les lignes indentées sous l'élément, rendues en HTML | — |
| `intro` | le texte hors liste, rendu en HTML | — |

Le séparateur est le premier `:` ou `|`. La valeur perd son gras (`**12**`).
Un élément sans séparateur devient une valeur sans libellé. Pas de variante devinée.

Avertissements : aucun chiffre ; élément sans séparateur.

## Variantes

- `default` : une tuile par chiffre ; autant de colonnes que de chiffres, 4 au plus
  (une seule sur mobile).

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `texte` (intro, détail, séparateur `|`),
`mal-ecrit` (puces mélangées, gras, élément sans séparateur, variante inconnue),
`vide`.
