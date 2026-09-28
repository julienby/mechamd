# 0003 — Précisions du contrat `Block` (J0)

**Contexte.** La spec liste les champs de `Block` sans fixer leurs types.

**Choix (à valider par l'humain, contrat).**

- `children` est une liste de `RenderedBlock(name, variant, id, html)` : les
  enfants sont rendus avant le parent, avec la variante fixée par le parent.
- Deux champs en plus, en lecture seule pour les directives : `line` (ligne
  d'ouverture dans le fichier, pour `explain`) et `warnings` (ce que `warn` a
  collecté).
- `md(text)` rend aussi les directives imbriquées dans `text`.
- Les templates reçoivent les données de `parse` et `block` (`name`, `variant`,
  `id`, `attrs`) ; la fonction `root_attrs(block)` écrit les attributs
  obligatoires de l'élément racine (`data-mecha`, `data-variant`, `id`).
