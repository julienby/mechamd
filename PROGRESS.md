# PROGRESS.md — journal de l'agent

Légende : ✅ fait · 🔄 en cours · ⏸️ en attente humaine · ⛔ bloqué · ⬜ à faire

## État courant

- Jalon actif : **J0 Fondations**
- Prochaine action : initialiser le dépôt Python (uv, ruff, mypy).

## J0 — Fondations

- ✅ `SPEC.md` (export de la spec v0.3), `AGENTS.md`, `PROGRESS.md`
- ⬜ Dépôt Python : `pyproject.toml` (uv, hatchling), ruff, mypy strict, pytest
- ⬜ Contrat `Block` (`src/mechamd/block.py`)
- ⬜ Découverte et chargement des directives
- ⬜ Commande `mecha test [directive]`
- ⬜ Directive vide de test qui passe ses exemples
- ⬜ CI GitHub Actions (Python 3.11 à 3.13 : ruff, mypy, pytest, `mecha test`)

## J1 — Socle + card

- ⬜ Direction visuelle : `themes/default/tokens.md`
- ⬜ Page vitrine de `card`
- ⬜ Validation humaine de la direction visuelle

## Journal

- 2026-09-28 — Création de `AGENTS.md` et `PROGRESS.md` à partir de la spec.
