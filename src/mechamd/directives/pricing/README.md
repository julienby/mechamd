# pricing

**Rôle** : des offres côte à côte (nom, prix, points, bouton), pour une page produit.

## Syntaxe

```markdown
:::pricing{recommended=Pro}
## Gratuit : 0 €
- Un site

## Pro : 9 € /mois
- Sites illimités
- Domaine perso

[Choisir Pro](https://example.org/pro)
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| une offre | chaque titre `## Nom : prix` | — |
| `amount`, `period` | le prix ; « /mois » à la fin devient la période | — |
| `points` | les puces sous le titre | — |
| `action` | le lien seul sur la dernière ligne de l'offre | — |
| `recommended` | aucune | `recommended=Nom` |

Pas de variante devinée. Colonnes : une par offre, 3 au plus.

Avertissements : aucune offre ; titre sans « : » ; `recommended` sans offre de ce nom.

## Variantes

- `default` : une carte par offre ; l'offre recommandée a un trait et un bouton d'accent.

## Attributs

- `recommended` : nom de l'offre à mettre en avant.

## Exemples

Voir `examples/` : `nu`, `recommande`, `mal-ecrit` (offre sans titre, variante
inconnue), `vide`.
