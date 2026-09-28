# links

**Rôle** : une liste de liens commentés (bibliographie, ressources, « à lire »).

## Syntaxe

```markdown
:::links
- [Fiche DS18B20](https://www.analog.com/…) : la sonde, précision et câblage
- https://docs.platformio.org/
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `links[].href` | le lien en tête d'élément : `[titre](url)`, `<url>` ou URL nue | — |
| `links[].title` | le texte du lien, sinon l'URL sans `https://` ni `www.` | — |
| `links[].domain` | l'hôte de l'URL, sans `www.` ; vide pour un lien relatif | — |
| `links[].description` | le texte après `:`, `\|`, `—` ou `--`, et les lignes indentées, rendus en HTML | — |
| `intro` | le texte hors de la liste (un titre, par exemple), rendu en HTML | — |

Pas de variante devinée.

Avertissements : aucun lien ; élément sans lien (gardé, affiché sans lien).

## Variantes

- `default` : les liens dans un bloc, titre en couleur d'accent, domaine en regard.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `url-nue` (URL nue, lien relatif, titre en
intro), `mal-ecrit` (`<url>`, séparateurs `--` et `|`, élément sans lien,
variante inconnue), `vide`.
