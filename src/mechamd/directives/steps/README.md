# steps

**Rôle** : une procédure en étapes numérotées (installer, flasher, monter une manip).

## Syntaxe

```markdown
:::steps
1. Brancher la carte en USB
2. Lancer le flash
3. Vérifier la LED verte
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `steps[].title` | chaque élément de liste (`1.`, `1)`, `-`, `*`), rendu en HTML | — |
| `steps[].body` | les lignes indentées sous l'élément (texte, code, image) | — |
| `intro` | le texte hors de la liste | — |

La numérotation est toujours recalculée : `1.`, `-` ou `1)` donnent le même rendu.
Pas de variante devinée.

Avertissement : aucune étape.

## Variantes

- `default` : une pastille numérotée par étape, le détail dessous.
- `compact` : numéros discrets et étapes resserrées, pour une check-list de manip.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu, avec intro et code), `compact` (explicite),
`mal-ecrit` (marqueurs mélangés, variante inconnue), `vide`.
