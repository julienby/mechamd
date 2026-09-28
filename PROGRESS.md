# PROGRESS.md — journal de l'agent

Légende : ✅ fait · 🔄 en cours · ⏸️ en attente humaine · ⛔ bloqué · ⬜ à faire

## État courant

- Jalon actif : **J1 Socle + card** — ⏸️ **en attente de validation de la direction visuelle**
- Prochaine action (après validation) : ajuster les tokens selon les retours, puis
  `mecha explain`, finalisation du layout, et clôture de J1.
- En attente humaine : activer la CI (`ci/README.md`), valider ADR 0003 et 0004.

## J0 — Fondations

- ✅ `SPEC.md` (export de la spec v0.3), `AGENTS.md`, `PROGRESS.md`
- ✅ Dépôt Python : `pyproject.toml` (uv, hatchling), ruff, mypy strict, pytest (couverture ≥ 85 %)
- ✅ Contrat `Block` (`src/mechamd/block.py`) — précisions en ADR 0003, ⏸️ à valider
- ✅ Découverte et chargement des directives (projet prioritaire sur fournies)
- ✅ Noyau minimal : frontmatter, Markdown, repérage des directives, résolution des variantes, rendu tolérant
- ✅ Commande `mecha test [directive] [-p projet]`
- ✅ Directive vide de test (`tests/fixtures/project/directives/empty`) qui passe ses exemples
- ⛔ CI GitHub Actions (Python 3.11 à 3.13 : ruff, mypy, pytest, `mecha test`) — workflow écrit dans `ci/github-ci.yml`, mais l'agent ne peut pas pousser dans `.github/workflows/` (jeton sans portée `workflow`). ⏸️ Un humain doit le déplacer (voir `ci/README.md`). Vérifications locales vertes sur Python 3.11.

## J1 — Socle + card

- ✅ Direction visuelle proposée : `src/mechamd/themes/default/tokens.md` + `mecha.css` (Tailwind v4) — ADR 0004
- ✅ Layout : en-tête, typographie, sommaire (≥ 3 `##`, grand écran), méta (date, tags), mode sombre
- ✅ Helpers `first_heading`, `first_image`, `trailing_link`
- ✅ Directive `card` : README, 5 exemples verts (simple, image, cover, mal-ecrit, vide), 3 templates
- ✅ Encadré discret pour les blocs non compris (`unknown.html`)
- ✅ Page vitrine `showcase/index.md` (illustrations SVG, les hôtes de photos étant bloqués)
- ⏸️ Validation humaine de la direction visuelle (aperçu publié en artifact privé)
- ⬜ `mecha explain fichier.md`
- ⬜ Helpers `parse_date`, `split_items` (utiles à timeline, J2)

## Décisions

- ADR 0001 — format des exemples (`{variant, data, warnings?}`)
- ADR 0002 — directive inconnue ou en erreur : encadré discret avec le contenu rendu
- ADR 0003 — précisions du contrat `Block` (⏸️ validation humaine)
- ADR 0004 — direction visuelle du thème default (⏸️ validation humaine)

## Journal

- 2026-09-28 — Création de `AGENTS.md` et `PROGRESS.md` à partir de la spec.
- 2026-09-28 — J0 : noyau minimal, `mecha test`, 29 tests pytest (couverture 99 %), CI écrite.
- 2026-09-28 — CI : push du workflow refusé (jeton sans portée `workflow`) ; fichier livré dans `ci/`.
- 2026-09-28 — J1 : tokens, layout, card, vitrine. Aperçu généré ainsi : Tailwind v4.3 (binaire
  autonome) compile `mecha.css`, `Engine(project="showcase").render_page("index.md")`, CSS et
  images inlinés. Vérifié à l'œil en clair/sombre, 1280 px et 390 px. Arrêt pour validation.
