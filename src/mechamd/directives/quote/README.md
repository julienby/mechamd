# quote

**Rôle** : une citation et son attribution (auteur, source).

## Syntaxe

```markdown
:::quote
Rien dans la vie n'est à craindre, tout est à comprendre.
— Marie Curie
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `text` | le contenu, rendu en HTML ; les `>` en début de ligne sont retirés | — |
| `cite` | la dernière ligne si elle commence par `—`, `–` ou `--`, rendue en HTML | `author=` |

Pas de variante devinée.

Avertissement : citation vide.

## Variantes

- `default` : citation dans la colonne de lecture, trait d'accent à gauche.
- `pull` : citation mise en exergue, grande et centrée, pour rythmer un billet.

## Attributs

- `author=` : remplace l'attribution lue dans le contenu (Markdown accepté).

## Exemples

Voir `examples/` : `nu` (cas nu), `pull` (explicite, `author=`), `mal-ecrit`
(lignes en `>`, attribution en `--` avec un lien), `vide`.
