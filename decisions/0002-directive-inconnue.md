# 0002 — Rendu d'une directive inconnue ou en erreur

**Contexte.** Question ouverte de la spec : encadré discret, ou Markdown normal ?
Une directive peut aussi échouer (exception dans `parse`, template cassé).

**Options.** (a) Markdown normal, invisible ; (b) encadré discret contenant le
contenu rendu en Markdown.

**Choix.** (b) pour tous ces cas : le texte reste lisible, et l'encadré signale
discrètement le problème (template `unknown.html` du thème, variante `unknown`).
L'avertissement est aussi remonté dans `Page.warnings` (et `mecha explain`).
À confirmer par l'humain avec la direction visuelle.
