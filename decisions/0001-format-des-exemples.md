# 0001 — Format des exemples de directive

**Contexte.** La spec dit que `x.data.json` contient « la sortie attendue de
`parse` et la variante retenue », sans fixer la forme.

**Options.** (a) le dictionnaire de `parse` seul, variante dans le nom du
fichier ; (b) un objet `{variant, data}` ; (c) une liste de blocs par exemple.

**Choix.** (b), avec une clé `warnings` facultative (comparée seulement si
présente) pour tester les cas « mal écrits ». Un exemple contient un bloc de la
directive ; seul le premier est comparé. `mecha test` vérifie aussi que le HTML
rendu porte `data-mecha="<nom>"`.

**Complément (J2, `grid`).** Un conteneur rend le HTML de ses enfants dans ses
données (`items: [{name, variant, id, html}]`). Pour que retoucher un template
d'enfant ne casse pas les exemples du conteneur, `mecha test` ignore toute clé
`html` dans la comparaison ; le `.data.json` peut l'omettre.
