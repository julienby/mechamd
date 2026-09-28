# 0004 — Direction visuelle du thème default (proposition J1)

**Statut** : ✅ validée par l'humain le 2026-09-28 (« ok pour un début ») ; à affiner à l'usage.

**Contexte.** La spec demande de figer typographie, palette, espacements,
formes, largeurs et mode sombre avant toute directive (`tokens.md`).

**Choix proposés.**

- Inter (texte) + Newsreader (titres, serif éditorial) + JetBrains Mono (code).
- Neutre `stone` (chaud, « papier ») plutôt que `slate` ; accent `indigo`.
- États : `sky` (info), `emerald` (tip), `amber` (warning) — écart avec
  l'exemple de la spec (amber/rose), pour suivre les conventions vert = conseil,
  ambre = attention.
- Colonne de lecture `max-w-2xl` et non `max-w-prose` (en `ch`, elle variait
  selon la taille de police de chaque élément et décalait titres et tableaux).
- Mode sombre par classe `dark` sur `<html>` : suit le système, bouton pour forcer.
- Polices chargées depuis Google Fonts en v0 (le plus simple) ; les héberger
  dans le thème sera à décider avant la publication (J4), pour le hors-ligne.
- Icônes : quelques SVG en ligne dans les templates (flèche, lune, soleil), au
  trait façon Lucide ; pas de jeu d'icônes intégré en v0.
