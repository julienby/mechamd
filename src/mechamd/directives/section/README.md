# section

**Rôle** : une grande partie de page, avec une ancre pour y renvoyer.

## Syntaxe

```markdown
:::section
## Matériel
Trois sondes DS18B20 et une carte BOB.
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `title` | premier titre du bloc | `title=` |
| `anchor` | `#id` du bloc, sinon le titre en ancre (`matériel`) | `#id` |
| `href`, `action` | lien seul sur la dernière ligne | `href=` (action : « Ouvrir ») |
| `image`, `alt` | — (les images du contenu restent dans le texte) | `image=`, `alt=` |
| `body` | le reste, rendu en HTML (directives comprises) | — |

Pas de variante devinée. Une section sans titre ni `#id` n'a pas d'ancre (avertissement).

## Variantes

- `default` : titre ancré, puis le contenu ; accepte des blocs larges (grilles).
- `hero` : grande ouverture de page, titre affiche centré, bouton d'action ;
  avec `image=`, l'image passe en fond sous un voile.

## Attributs

- `title=`, `href=` : remplacent le titre et le lien lus dans le contenu.
- `image=`, `alt=` : image de fond (variante `hero`).

## Exemples

Voir `examples/` : `nu` (cas nu), `hero` (explicite, avec `#id` et action),
`mal-ecrit` (variante inconnue, pas de titre).
