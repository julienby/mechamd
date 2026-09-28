# PROGRESS.md — journal de l'agent

Légende : ✅ fait · 🔄 en cours · ⏸️ en attente humaine · ⛔ bloqué · ⬜ à faire

## État courant

- Jalon actif : **J2 terminé** — prochain : J3 (catalogue, directives ajoutées par agents)
- Prochaine action : attendre les retours de l'humain sur la vitrine complète, puis ouvrir J3.
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
- polices chargées depuis Google Fonts : à héberger dans le thème avant J4 (hors-ligne).

## Décisions

- ADR 0001 — format des exemples (`{variant, data, warnings?}`)
- ADR 0002 — directive inconnue ou en erreur : encadré discret avec le contenu rendu
- ADR 0003 — précisions du contrat `Block` (✅ validée)
- ADR 0004 — direction visuelle du thème default (✅ validée, version de départ)
- ADR 0005 — build, serveur live et compilation CSS
- ADR 0006 — layouts de page (`base.html` + `layouts/`)

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
