# PROGRESS.md — journal de l'agent

Légende : ✅ fait · 🔄 en cours · ⏸️ en attente humaine · ⛔ bloqué · ⬜ à faire

## État courant

- Jalon actif : **J2 Build + live**
- Prochaine action : helpers `parse_date` / `split_items`, puis directives `callout`, `timeline`,
  `section`, `grid`, puis compilation CSS, `mecha build`, `mecha serve`.
- En attente humaine : aucune. (CI : laissée dans `ci/`, jugée acceptable par l'humain pour l'instant.)

## J0 — Fondations

- ✅ `SPEC.md` (export de la spec v0.3), `AGENTS.md`, `PROGRESS.md`
- ✅ Dépôt Python : `pyproject.toml` (uv, hatchling), ruff, mypy strict, pytest (couverture ≥ 85 %)
- ✅ Contrat `Block` (`src/mechamd/block.py`) — précisions en ADR 0003, validées
- ✅ Découverte et chargement des directives (projet prioritaire sur fournies)
- ✅ Noyau minimal : frontmatter, Markdown, repérage des directives, résolution des variantes, rendu tolérant
- ✅ Commande `mecha test [directive] [-p projet]`
- ✅ Directive vide de test (`tests/fixtures/project/directives/empty`) qui passe ses exemples
- ⛔ CI GitHub Actions (Python 3.11 à 3.13 : ruff, mypy, pytest, `mecha test`) — workflow écrit dans `ci/github-ci.yml`, mais l'agent ne peut pas pousser dans `.github/workflows/` (jeton sans portée `workflow`). Pour l'activer : `git mv ci/github-ci.yml .github/workflows/ci.yml` (voir `ci/README.md`). En attendant, les vérifications sont lancées en local avant chaque push (3.11, 3.12, 3.13).

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

- ⬜ Helpers `parse_date` (dates approximatives), `split_items`
- ⬜ Directive `callout` (info, tip, warning ; devinée sur le premier mot)
- ⬜ Directive `timeline` (default, compact)
- ⬜ Directive `section` (default, hero)
- ⬜ Directive `grid` (colonnes = nombre d'enfants, 3 au plus ; `cols=`)
- ⬜ Compilation CSS (binaire Tailwind v4 autonome, recompilé seulement si un template change)
- ⬜ `mecha build [dossier] -o dist/`
- ⬜ `mecha serve [dossier]` (Starlette + uvicorn, cache sur mtime, rechargement auto)
- ⬜ Vitrine complète, construite et servie en live

## Décisions

- ADR 0001 — format des exemples (`{variant, data, warnings?}`)
- ADR 0002 — directive inconnue ou en erreur : encadré discret avec le contenu rendu
- ADR 0003 — précisions du contrat `Block` (✅ validée)
- ADR 0004 — direction visuelle du thème default (✅ validée, version de départ)

## Journal

- 2026-09-28 — Création de `AGENTS.md` et `PROGRESS.md` à partir de la spec.
- 2026-09-28 — J0 : noyau minimal, `mecha test`, 29 tests pytest (couverture 99 %), CI écrite.
- 2026-09-28 — CI : push du workflow refusé (jeton sans portée `workflow`) ; fichier livré dans `ci/`.
- 2026-09-28 — J1 : tokens, layout, card, vitrine. Aperçu généré ainsi : Tailwind v4.3 (binaire
  autonome) compile `mecha.css`, `Engine(project="showcase").render_page("index.md")`, CSS et
  images inlinés. Vérifié à l'œil en clair/sombre, 1280 px et 390 px. Arrêt pour validation.
- 2026-09-28 — Validation humaine : contrat `Block` et direction visuelle. J1 terminé avec
  `mecha explain`. Passage à J2.
