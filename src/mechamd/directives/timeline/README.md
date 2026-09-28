# timeline

**Rôle** : une chronologie, écrite comme une liste de notes datées.

## Syntaxe

```markdown
:::timeline
- 2024 : Création du labo
- mars 2025 : Premier prototype BOB
- 12/09/2026 : Déploiement en salle B204
  Trois capteurs, deux semaines de mesure.
:::
```

## Ce qui est deviné

- Chaque élément de liste est `date : titre` ; le séparateur est `:` ou `|`.
- Dates reconnues (affichées comme écrites) : « 2024 », « mars 2025 »,
  « 1er août 2026 », « 12/09/2026 », « 09/2026 », « 2026-09-12 ».
- Une ligne indentée sous un élément devient sa description.
- Un élément sans date reconnue reste affiché, avec un avertissement.
- Le texte hors de la liste s'affiche en introduction.

Pas de variante devinée.

## Variantes

- `default` : chronologie verticale, un repère par date, titres en avant.
- `compact` : une ligne par date, pour les listes longues.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `compact` (explicite, séparateur `|`),
`mal-ecrit` (texte hors liste, élément sans date, titre manquant).
