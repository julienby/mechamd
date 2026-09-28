# compare

**Rôle** : des options côte à côte (matériel, méthodes, avant/après), une colonne par titre.

## Syntaxe

```markdown
:::compare
### DS18B20
Étanche, bus 1-Wire, ±0,5 °C.

### SHT31
Température et humidité, bus I²C.
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `columns` | un titre ouvre une colonne ; le niveau du premier titre fait foi, les titres plus petits restent dans la colonne | — |
| `intro` | le texte avant le premier titre | — |

Les `#` dans un bloc de code ne sont pas des titres. Colonnes : autant que
d'options, 4 au plus par ligne, une seule sur mobile.

Avertissements : aucune colonne, ou une seule.

## Variantes

- `default` : une carte par option, en grille.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `trois` (intro, sous-titre dans une colonne),
`mal-ecrit` (une seule colonne, code avec `#`, variante inconnue), `vide`.
