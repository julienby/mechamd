# PROGRESS.md — journal de l'agent

Légende : ✅ fait · 🔄 en cours · ⏸️ en attente humaine · ⛔ bloqué · ⬜ à faire

## État courant

- Jalon actif : **J4 — publication** (🔄 en cours)
- Prochaine action : README, push, CI verte.
- En attente humaine : aucune bloquante.

## J0 — Fondations

- ✅ `SPEC.md` (export de la spec v0.3), `AGENTS.md`, `PROGRESS.md`
- ✅ Dépôt Python : `pyproject.toml` (uv, hatchling), ruff, mypy strict, pytest (couverture ≥ 85 %)
- ✅ Contrat `Block` (`src/mechamd/block.py`) — précisions en ADR 0003, validées
- ✅ Découverte et chargement des directives (projet prioritaire sur fournies)
- ✅ Noyau minimal : frontmatter, Markdown, repérage des directives, résolution des variantes, rendu tolérant
- ✅ Commande `mecha test [directive] [-p projet]`
- ✅ Directive vide de test (`tests/fixtures/project/directives/empty`) qui passe ses exemples
- ✅ CI GitHub Actions (Python 3.11 à 3.13 : ruff, mypy, pytest, `mecha test`) — `.github/workflows/ci.yml`

## J1 — Socle + card

- ✅ Direction visuelle proposée : `src/mechamd/themes/default/tokens.md` + `mecha.css` (Tailwind v4) — ADR 0004
- ✅ Layout : en-tête, typographie, sommaire (≥ 3 `##`, grand écran), méta (date, tags), mode sombre
- ✅ Helpers `first_heading`, `first_image`, `trailing_link`
- ✅ Directive `card` : README, 5 exemples verts (simple, image, cover, mal-ecrit, vide), 3 templates
- ✅ Encadré discret pour les blocs non compris (`unknown.html`)
- ✅ Page vitrine `showcase/index.md` (illustrations SVG, les hôtes de photos étant bloqués)
- ✅ Validation humaine de la direction visuelle (« ok pour un début »)
- ✅ `mecha explain fichier.md [-p projet]` : variante, raison, avertissements par bloc
- Piste notée : la raison « devinée » reste générique (la spec cite « image détectée ligne 3 »).
  Donner le détail demanderait que `infer_variant` rende aussi une raison : c'est un changement
  de contrat, donc à proposer à l'humain plutôt qu'à faire seul.

## J2 — Build + live

- ✅ Helpers `parse_date` (dates approximatives), `split_items`, `slugify`
- ✅ Directive `callout` (default/info, tip, warning ; devinée sur le premier mot) — 5 exemples
- ✅ Directive `timeline` (default, compact) — 3 exemples
- ✅ Directive `section` (default, hero) — 3 exemples
- ✅ Directive `grid` (colonnes = nombre d'enfants, 3 au plus ; `cols=` de 1 à 4) — 3 exemples
- ✅ Compilation CSS (binaire Tailwind v4.3.3 autonome, cache par signature des templates) — ADR 0005
- ✅ `mecha build [dossier] -o dist/` (liens `.md` → `.html`, chemins relatifs, ressources copiées)
- ✅ `mecha serve [dossier]` (Starlette + uvicorn, cache sur mtime, moteur rechargé si une
  directive change, rechargement du navigateur par SSE, `--no-reload` pour la production)
- ✅ Vitrine complète : construite par `mecha build`, servie et rechargée en live (vérifié à la main),
  aperçu mis à jour dans l'artifact privé
- ✅ Toutes les directives vertes : 19/19 exemples ; 48 tests pytest (couverture 98 %) sur 3.11–3.13

- ✅ Frontmatter `layout:` (`article`, `page`, `notes`) : `base.html` + `layouts/` — ADR 0006

Pistes notées pour plus tard :
- les titres des `section` n'apparaissent pas dans le sommaire (seuls les `##` du document) ;
- ~~polices chargées depuis Google Fonts~~ : hébergées dans le thème (J4).

## J3 — Catalogue

- ✅ `figure` (default, wide, gallery ; galerie devinée à 2 images) — 5 exemples
- ✅ `steps` (default, compact) — 4 exemples
- ✅ `specs` (default, inline ; séparateur `:` ou `|`) — 4 exemples
- ✅ `stats` (default ; colonnes = nombre de chiffres, 4 au plus) — 4 exemples
- ✅ `quote` (default, pull ; attribution sur la dernière ligne « — auteur ») — 4 exemples
- ✅ `details` (default fermé, open ; résumé = premier titre, `summary=` ou première ligne) — 4 exemples
- ✅ `todo` (default ; `[ ]`/`[x]`, avancement fait/total) — 4 exemples
- ✅ `links` (default ; `[titre](url) : description` ou URL nue, domaine affiché) — 4 exemples
- ✅ `compare` (default ; une colonne par titre, 4 au plus par ligne) — 4 exemples

## J4 — Publication

- ✅ Licence MIT, métadonnées du paquet (0.1.0)
- ✅ Polices hébergées dans le thème (woff2 latin Fontsource, OFL ; servies sous `_mecha/fonts/`)
- ✅ `mecha llms [-p projet]` et `llms.txt` (test de fraîcheur : régénérer si un README change)
- ✅ Test en conteneur vierge (`python:3.12-slim` : wheel, `mecha build`, `mecha serve`, 3 × HTTP 200)
- ✅ Workflow de publication `publish.yml` (tag `v*` = version, build, garde-fou, Trusted Publishing)
- ⏸️ Publication sur PyPI (humain)

## Décisions

- ADR 0001 — format des exemples (`{variant, data, warnings?}`)
- ADR 0002 — directive inconnue ou en erreur : encadré discret avec le contenu rendu
- ADR 0003 — précisions du contrat `Block` (✅ validée)
- ADR 0004 — direction visuelle du thème default (✅ validée, version de départ)
- ADR 0005 — build, serveur live et compilation CSS
- ADR 0006 — layouts de page (`base.html` + `layouts/`)
- ADR 0007 — publication : licence MIT, polices hébergées, PyPI par workflow sur tag

## Journal

- 2026-09-28 — Création de `AGENTS.md` et `PROGRESS.md` à partir de la spec.
- 2026-09-28 — J0 : noyau minimal, `mecha test`, 29 tests pytest (couverture 99 %), CI écrite.
- 2026-09-28 — CI : push du workflow refusé (jeton sans portée `workflow`) ; fichier livré dans `ci/`.
- 2026-09-28 — CI activée : workflow déplacé dans `.github/workflows/`.
- 2026-09-28 — J1 : tokens, layout, card, vitrine. Aperçu généré ainsi : Tailwind v4.3 (binaire
  autonome) compile `mecha.css`, `Engine(project="showcase").render_page("index.md")`, CSS et
  images inlinés. Vérifié à l'œil en clair/sombre, 1280 px et 390 px. Arrêt pour validation.
- 2026-09-28 — Validation humaine : contrat `Block` et direction visuelle. J1 terminé avec
  `mecha explain`. Passage à J2.
- 2026-09-28 — J2 : callout, timeline, section, grid ; CSS Tailwind, `mecha build`, `mecha serve`.
  Correction : les styles de listes du texte s'appliquaient aux listes des templates (timeline).
- 2026-09-28 — Layouts `article`, `page`, `notes` choisis par le frontmatter ; version de départ,
  à affiner.
- 2026-09-28 — J3 lot 1 : figure, steps, specs, stats, ajoutées à la vitrine.
- 2026-09-28 — J3 lot 2 : quote, details, todo, links, compare, ajoutées à la vitrine.
- 2026-09-28 — Vérification visuelle du lot 2 (clair, sombre, 390 px). Corrections : double trait
  des citations (style de `blockquote` limité au texte), barre d'avancement de `todo` en `div`
  (le `<progress>` natif est cassé par le reset Tailwind), intro de `compare` dans la colonne de lecture.
- 2026-09-28 — J4 : licence MIT, version 0.1.0. Polices hébergées dans le thème, plus aucun appel
  à Google Fonts ; vérifié dans le navigateur (5 polices chargées depuis `_mecha/fonts/`).
- 2026-09-28 — J4 : `mecha llms`. Test en conteneur vierge : deux défauts trouvés et corrigés
  (`--version` affichait 0.0.1 ; police servie en `application/octet-stream` faute de `/etc/mime.types`).
