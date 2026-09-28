# callout

**Rôle** : un encadré d'information qui se détache du texte — une note, une astuce, une mise en garde.

## Syntaxe

```markdown
:::callout
Attention : recalibrer la sonde après chaque déplacement.
:::
```

## Ce qui est deviné

| Donnée | Source |
| --- | --- |
| `label` | premier mot suivi de « : » s'il est connu : Astuce, Attention, Note, Info (gras toléré) |
| `title` | premier titre du bloc, facultatif |
| `body` | le reste, rendu en HTML (première lettre mise en majuscule après l'étiquette) |

Variante devinée, un seul signal : **le premier mot**. « Astuce » → `tip`,
« Attention » → `warning` ; sinon l'aspect d'information (`default`).

## Variantes

- `default` / `info` : information neutre (bleu ciel).
- `tip` : astuce, conseil (vert).
- `warning` : attention, précaution (ambre).

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `attention` et `astuce` (devinés), `explicite`
(`.tip` sans mot-clé), `mal-ecrit` (variante inconnue, étiquette collée, minuscule).
