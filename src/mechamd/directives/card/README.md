# card

**Rôle** : un bloc de contenu autonome — un titre, un texte court, parfois une
image et un lien d'action.

## Syntaxe

```markdown
:::card
### Capteur DS18B20
Sonde de température étanche, précision ±0,5 °C.
[Voir la fiche](ds18b20.md)
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `title` | premier titre du bloc (`#` à `######`) | `title=` |
| `image`, `alt` | première image du bloc | `image=` |
| `href`, `action` | lien seul sur la dernière ligne | `href=` (action : « Ouvrir ») |
| `body` | le reste, rendu en HTML | — |

Variante devinée, un seul signal : **une image est présente → `image`**.

## Variantes

- `default` : titre, texte, lien d'action en bas.
- `image` : image en haut (ratio 16/9), puis le texte. Devinée si une image est présente.
- `cover` : image en fond plein cadre, texte par-dessus. Seulement si demandée
  (`:::card{.cover}` ou `::::grid{card=cover}`). Sans image, un fond d'accent la remplace.

Avec un lien, toute la carte est cliquable.

## Attributs

- `title=` : remplace le titre lu dans le contenu.
- `image=` : chemin ou URL de l'image.
- `href=` : cible du lien d'action.

## Exemples

Voir `examples/` : `simple` (cas nu), `image` (devinée), `cover` (explicite,
avec `#id` et `href=`), `mal-ecrit` (variante inconnue, image au milieu du
texte, pas de titre), `vide`.
