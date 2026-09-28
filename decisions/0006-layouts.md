# 0006 — Layouts de page

**Contexte.** La spec prévoit un champ de frontmatter `layout: article | page |
notes`, « fourni par le thème ». Jusqu'ici, un seul gabarit `layout.html`
servait toutes les pages.

**Options.**

1. Un seul `layout.html` avec des `{% if page.layout == … %}`.
2. Un gabarit commun `base.html` et un fichier par layout dans `layouts/`,
   qui l'étend (`{% extends "base.html" %}`, bloc `main`).

**Choix.** Option 2 : chaque layout se lit seul, et un projet ajoute un layout
en déposant `theme/layouts/<nom>.html` (ou remplace `theme/base.html`), sans
toucher au moteur.

- `base.html` : `<head>`, en-tête, pied, mode sombre ; `data-layout` sur `<body>`.
- `article` (défaut) : sommaire, date et tags, colonne de lecture.
- `page` : ni sommaire, ni date, ni tags (accueil, vitrine).
- `notes` : date et tags en une ligne, pas de sommaire, rythme resserré
  (classe `mecha-compact`).
- Layout inconnu : `article` est utilisé, avec un avertissement.

Écart avec SPEC.md (§ Thème) : le gabarit n'est plus `layout.html` mais
`base.html` + `layouts/`.
