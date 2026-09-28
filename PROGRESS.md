# PROGRESS.md — journal de l'agent

Légende : ✅ fait · 🔄 en cours · ⏸️ en attente humaine · ⛔ bloqué · ⬜ à faire

## État courant

- Jalon actif : **J0 Fondations** (CI à confirmer sur GitHub)
- Prochaine action : J1, direction visuelle.

## J0 — Fondations

- ✅ `SPEC.md` (export de la spec v0.3), `AGENTS.md`, `PROGRESS.md`
- ✅ Dépôt Python : `pyproject.toml` (uv, hatchling), ruff, mypy strict, pytest (couverture ≥ 85 %)
- ✅ Contrat `Block` (`src/mechamd/block.py`) — précisions en ADR 0003, ⏸️ à valider
- ✅ Découverte et chargement des directives (projet prioritaire sur fournies)
- ✅ Noyau minimal : frontmatter, Markdown, repérage des directives, résolution des variantes, rendu tolérant
- ✅ Commande `mecha test [directive] [-p projet]`
- ✅ Directive vide de test (`tests/fixtures/project/directives/empty`) qui passe ses exemples
- 🔄 CI GitHub Actions (Python 3.11 à 3.13 : ruff, mypy, pytest, `mecha test`) — premier run à vérifier

## J1 — Socle + card

- ⬜ Direction visuelle : `themes/default/tokens.md`
- ⬜ Page vitrine de `card`
- ⬜ Validation humaine de la direction visuelle

## Décisions

- ADR 0001 — format des exemples (`{variant, data, warnings?}`)
- ADR 0002 — directive inconnue ou en erreur : encadré discret avec le contenu rendu
- ADR 0003 — précisions du contrat `Block` (⏸️ validation humaine)

## Journal

- 2026-09-28 — Création de `AGENTS.md` et `PROGRESS.md` à partir de la spec.
- 2026-09-28 — J0 : noyau minimal, `mecha test`, 29 tests pytest (couverture 99 %), CI écrite.
