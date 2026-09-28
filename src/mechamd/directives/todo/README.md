# todo

**Rôle** : une liste de tâches, cochées ou non, avec l'avancement (fait / total).

## Syntaxe

```markdown
:::todo
- [x] Commander les sondes
- [ ] Poser en salle B204
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `items` | les éléments de liste ; `[x]` ou `[X]` = fait, `[ ]` ou `[]` = à faire | — |
| `items[].detail` | les lignes indentées sous la tâche, rendues en HTML | — |
| `intro` | le texte hors de la liste, rendu en HTML | — |
| `done`, `total` | comptés sur les cases | — |

Pas de variante devinée.

Avertissements : aucune tâche ; élément sans case (compté à faire).

## Variantes

- `default` : tâches dans un bloc, barre d'avancement en tête.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `intro` (texte, détail, lien), `mal-ecrit`
(puces mêlées, `[X]`, `[]`, élément sans case, variante inconnue), `vide`.
