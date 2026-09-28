# figure

**Rôle** : montrer une ou plusieurs images avec leur légende (photo de manip,
schéma, courbe, galerie de billet).

## Syntaxe

```markdown
:::figure
![Le banc de mesure vu de dessus](photos/banc.jpg)
Le banc de mesure, câblé pour la série B.
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `images` (`src`, `alt`) | toutes les images du bloc, dans l'ordre, même au milieu d'une phrase | — |
| `caption` | le reste du texte, rendu en HTML | — |

Variante devinée, un seul signal : **deux images ou plus → `gallery`**.

Avertissements : aucune image ; image sans texte alternatif.

## Variantes

- `default` : images dans la colonne de lecture, légende discrète dessous.
- `wide` : images en largeur de bloc visuel (`max-w-5xl`), pour un schéma ou une
  courbe détaillée. Seulement si demandée (`:::figure{.wide}`).
- `gallery` : images en grille de même ratio (16/9), trois colonnes au plus.
  Devinée à partir de deux images.

## Attributs

Aucun. L'`id` (`#courbe`) permet de renvoyer à la figure : `[voir la figure](#courbe)`.

## Exemples

Voir `examples/` : `nu` (cas nu), `galerie` (devinée), `large` (explicite, avec
`#id`), `mal-ecrit` (image au milieu d'une phrase, sans texte alternatif), `vide`.
