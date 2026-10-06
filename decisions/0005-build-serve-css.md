# 0005 — Build, serveur live et CSS

> Partie serveur (Starlette, SSE, watchfiles) remplacée par l'ADR 0009.

**Contexte.** J2 : `mecha build`, `mecha serve`, compilation Tailwind sans Node.

**Choix.**

- **Tailwind** : binaire autonome v4 épinglé (`TAILWIND_VERSION`), cherché dans
  `$MECHA_TAILWIND`, puis `~/.cache/mechamd/`, sinon téléchargé une fois depuis
  les releases GitHub. Il scanne les dossiers `templates/` des directives et les
  thèmes, jamais les documents. Le CSS compilé vit dans `<projet>/.mecha/` avec
  une signature des templates : pas de recompilation tant qu'aucun ne change.
  Sans binaire, le build écrit quand même les pages et signale l'erreur (code 1).
- **Liens** : les liens relatifs vers `x.md` sont réécrits en `x.html` dans la
  page rendue ; le serveur accepte les deux. Chaque page connaît son chemin vers
  la racine du site (`page.root`), pour que le site marche aussi ouvert en local.
- **Contenu d'un projet** : tous les fichiers, sauf `directives/`, `theme/`,
  `dist/`, le dossier de sortie et les dossiers cachés. Les `.md` deviennent des
  pages, le reste est copié tel quel.
- **Serveur** : Starlette ; rendu à la requête avec cache sur la date de
  modification ; moteur reconstruit quand une directive ou le thème change ;
  rechargement du navigateur par Server-Sent Events (`watchfiles`), désactivable
  avec `--no-reload` pour la production.
