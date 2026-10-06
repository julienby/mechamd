# buttons

**Rôle** : une rangée de boutons (le premier plein, les suivants discrets), sous
un titre ou une accroche.

## Syntaxe

```markdown
:::buttons
[Commencer](start.md)
[Voir le code](https://github.com/julienby/mechamd)
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `links` | chaque ligne `[texte](url)` seule | — |

Pas de variante devinée.

Avertissements : aucun bouton ; ligne qui n'est pas un lien seul (ignorée).

## Variantes

- `default` : alignés à gauche.
- `center` : centrés, pour sous un titre de page d'accueil.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu`, `centre`, `mal-ecrit`, `vide`.
