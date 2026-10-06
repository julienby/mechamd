# 0008 — Pas de publication sur PyPI, outillage allégé

**Contexte.** L'ADR 0007 prévoyait une publication sur PyPI par Trusted Publishing.
PyPI n'apporte que `pip install mechamd` ; l'outil est utilisé par son auteur,
et la publication ajoute un workflow, un environnement GitHub, un éditeur de
confiance et une version irréversible.

**Options.**

1. Publier sur PyPI (ADR 0007).
2. Installer depuis GitHub (`uv tool install git+https://...`).

**Choix (humain, 2026-10-06).** Option 2. Le workflow `publish.yml` est supprimé,
la publication n'est plus une escalade humaine. L'outillage de développement est
allégé dans le même mouvement : plus de mypy ni de seuil de couverture, CI sur
Python 3.12 seul. Restent ruff, pytest et `mecha test`. `httpx2` reste, car les
tests du serveur utilisent `starlette.testclient`.

Reste valable de l'ADR 0007 : licence MIT, polices hébergées dans le thème.
