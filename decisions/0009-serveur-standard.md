# 0009 — Serveur de développement sur la bibliothèque standard

**Contexte.** `mecha serve` reposait sur Starlette, uvicorn et watchfiles (trois
dépendances, plus `httpx2` pour les tests). Moins il y a de dépendances, plus le
projet évolue vite et s'installe simplement.

**Options.**

1. Garder Starlette + uvicorn + watchfiles.
2. `http.server` (`ThreadingHTTPServer`) ; rechargement par sondage : la page
   interroge `/_mecha/version` chaque seconde, la valeur change quand un fichier
   du projet, d'une directive ou du thème change.

**Choix (humain, 2026-10-06).** Option 2. Dépendances d'exécution : 7 → 4
(markdown-it-py, mdit-py-plugins, python-frontmatter, jinja2). `httpx2` disparaît
du développement. `mecha serve` est un serveur de développement ; la production
passe par `mecha build` et un hébergement statique. La logique de réponse
(`Site.respond`) est testée sans réseau, plus un test HTTP réel.

Remplace la partie « serveur » de l'ADR 0005.
