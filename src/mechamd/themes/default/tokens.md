# Socle visuel — thème `default`

> Statut : **proposition J1, en attente de validation humaine.**

Ce fichier fixe les seules valeurs de style qu'un template peut utiliser.
Une classe Tailwind absente d'ici n'a pas sa place dans un template.
Les valeurs sont appliquées dans `mecha.css` (bloc `@theme` et styles de base).

**Intention** : un carnet de labo soigné, plutôt qu'un wiki. Du papier chaud,
une encre bleu-violet, des titres éditoriaux ; le calme d'une revue, la
densité d'une note. L'espace sépare, les traits restent rares.

## Typographie

| Rôle | Police | Classe | Usage |
| --- | --- | --- | --- |
| Texte | **Inter** (variable) | `font-sans` | corps, listes, interface |
| Titres | **Newsreader** (serif éditorial, optique variable) | `font-serif` | `h1`–`h3`, titres de blocs |
| Code | **JetBrains Mono** | `font-mono` | code, dates techniques |

Échelle (tailles Tailwind, rien d'autre) :

| Niveau | Classe | Graisse | Où |
| --- | --- | --- | --- |
| Affiche | `text-5xl` (`sm:text-6xl`) | `font-medium` serif | titre de page, `section.hero` |
| Titre 1 | `text-4xl` | `font-medium` serif | `h1` de document |
| Titre 2 | `text-3xl` | `font-medium` serif | `h2`, titre de `card.cover` |
| Titre 3 | `text-xl` | `font-semibold` serif | `h3`, titre de `card` |
| Texte | `text-lg` (document), `text-base` (dans un bloc) | `font-normal` | paragraphes |
| Détail | `text-sm` | `font-medium` | liens d'action, légendes, méta |
| Étiquette | `text-xs` + `uppercase tracking-widest` | `font-semibold` | surtitres, badges |

Interlignage : `leading-relaxed` pour le texte, `leading-tight` pour les titres
(`leading-snug` pour `text-xl`). Titres : `tracking-tight` au-dessus de `text-xl`.
Titres en `text-balance`, paragraphes en `text-pretty`.

## Palette

Un neutre chaud, un accent, trois couleurs d'état. Palettes Tailwind par défaut.

| Rôle | Palette | Clair | Sombre |
| --- | --- | --- | --- |
| Fond de page | `stone` | `bg-stone-50` | `dark:bg-stone-950` |
| Surface (bloc) | `stone` / blanc | `bg-white` | `dark:bg-stone-900` |
| Surface discrète | `stone` | `bg-stone-100` | `dark:bg-stone-800/60` |
| Bordure | `stone` | `border-stone-200` | `dark:border-stone-800` |
| Bordure au survol | `indigo` | `border-indigo-300` | `dark:border-indigo-500/50` |
| Texte fort (titres) | `stone` | `text-stone-900` | `dark:text-stone-50` |
| Texte courant | `stone` | `text-stone-700` | `dark:text-stone-300` |
| Texte discret | `stone` | `text-stone-500` | `dark:text-stone-400` |
| Accent (liens, actions) | `indigo` | `text-indigo-700` | `dark:text-indigo-300` |
| Accent plein | `indigo` | `bg-indigo-600` / `text-white` | `dark:bg-indigo-500` |
| Sélection, repères | `indigo` | `bg-indigo-100` | `dark:bg-indigo-500/20` |
| État **info** | `sky` | fond `bg-sky-50`, trait `border-sky-200`, texte `text-sky-900`, icône `text-sky-600` | `dark:bg-sky-950/40`, `dark:border-sky-900`, `dark:text-sky-100`, `dark:text-sky-400` |
| État **tip** | `emerald` | mêmes nuances en `emerald` | mêmes nuances en `emerald` |
| État **warning** | `amber` | mêmes nuances en `amber` | mêmes nuances en `amber` |

Sur image (`card.cover`, `section.hero`) : texte `text-white` / `text-white/80`,
voile `from-stone-950/90 via-stone-950/40 to-stone-950/0`.

Écart assumé avec l'exemple de la spec : `emerald` (et non `amber`) pour
**tip**, `amber` (et non `rose`) pour **warning** — conventions plus
universelles (vert = conseil, ambre = attention). `rose` reste libre pour un
futur état « danger ».

## Espacements

Une seule échelle (unités Tailwind) :

- **entre blocs, marges, gouttières** : `4`, `6`, `8`, `12`, `16` ;
- **à l'intérieur d'un bloc** (entre étiquette, titre, texte) : `1`, `2`, `3` ;
- **rembourrage d'un bloc** : `p-6` (`sm:p-8` pour les blocs larges) ;
- rythme vertical du document : `space-y-6` entre éléments, `mt-16` avant un `h2`,
  `mt-12` avant un `h3`, `my-12` autour d'un bloc visuel.

Hauteurs d'images : ratio `aspect-video` (16/9) ; `card.cover` en `min-h-80`.
Sans image, `card.cover` prend un fond d'accent `bg-linear-to-br from-indigo-600
to-indigo-800` (`dark:from-indigo-500 dark:to-indigo-900`).

## Formes

| Élément | Rayon | Bordure | Ombre |
| --- | --- | --- | --- |
| Bloc (card, callout…) | `rounded-2xl` | `border` fine (couleur « bordure ») | `shadow-sm`, `hover:shadow-md` si cliquable |
| Élément interne (image intérieure, bouton, code) | `rounded-lg` | aucune | aucune |
| Étiquette, badge | `rounded-full` | aucune | aucune |
| Signalement (bloc non compris) | `rounded-2xl` | `border border-dashed border-stone-300` / `dark:border-stone-700` | aucune |

Transitions : `transition` + `duration-200` uniquement, sur couleur, ombre,
bordure. Rien ne bouge sauf un léger `hover:-translate-y-0.5` des cartes cliquables.

## Largeurs

- **Colonne de lecture** : `max-w-2xl` (42 rem, ~70 caractères en `text-lg`),
  centrée — texte, listes, titres, blocs simples (une carte seule, un encadré).
  Pas `max-w-prose` : exprimé en `ch`, il varierait avec la taille de police de
  chaque élément et décalerait titres, tableaux et code.
- **Blocs visuels larges** : `max-w-5xl` — grilles, sections, chronologies.
- **Page** : gouttières `px-4` (mobile) à `px-6` (`sm:`).

## Mode sombre

Chaque couleur a son équivalent sombre ci-dessus ; un template écrit toujours
la paire (`text-stone-700 dark:text-stone-300`). Le mode suit le système, et un
bouton de l'en-tête permet de le forcer (classe `dark` sur `<html>`).

## Règles pour les templates

1. Aucune valeur arbitraire (`text-[13px]`, `#3a7`, `mt-[7px]`…).
2. Un seul élément dominant par bloc (le titre, ou l'image).
3. De l'air plutôt que des bordures : une seule bordure par bloc, jamais de
   séparateur interne si un espacement suffit.
4. Toujours la paire clair/sombre, toujours lisible à 360 px de large.
