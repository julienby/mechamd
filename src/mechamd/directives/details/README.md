# details

**Rôle** : un bloc repliable (précision, calcul, journal brut, question de FAQ).

## Syntaxe

```markdown
:::details
### Pourquoi 30 secondes entre deux mesures ?
La constante de temps des sondes est d'environ 10 s.
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `summary` | le premier titre, sinon la première ligne, sinon « Détails » | `summary=` |
| `body` | le reste du contenu, rendu en HTML | — |

Pas de variante devinée. Pour une FAQ, écrire un bloc par question.

Avertissement : rien à replier (contenu vide).

## Variantes

- `default` : fermé ; seul le résumé est visible.
- `open` : ouvert à l'affichage, repliable ensuite.

## Attributs

- `summary=` : texte du résumé cliquable.

## Exemples

Voir `examples/` : `nu` (cas nu), `open` (explicite, `summary=`), `mal-ecrit`
(pas de titre, variante inconnue), `vide`.
