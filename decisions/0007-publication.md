# 0007 — Licence, polices et publication

> Partie publication PyPI remplacée par l'ADR 0008.

**Contexte.** J4 publie mechamd sur PyPI. Il faut une licence, un rendu qui
marche hors-ligne, et une façon de publier sans jeton sur un poste.

**Options.**

1. Licence : MIT ou Apache-2.0.
2. Polices : Google Fonts (réseau à chaque page) ou fichiers dans le thème.
3. Publication : `uv publish` à la main avec un jeton, ou workflow GitHub sur tag
   avec Trusted Publishing.

**Choix (humain, 2026-09-28).**

- Licence **MIT** : la plus simple et la plus connue.
- Polices **hébergées dans le thème** : `themes/default/fonts/`, woff2 variables
  (sous-ensemble latin, Fontsource 5.3.0), licence OFL jointe. Le build les copie
  dans `_mecha/fonts/`, le serveur les sert à la même adresse. Plus de requête
  vers Google.
- **Workflow sur tag `v*`** (`.github/workflows/publish.yml`) : build, test du
  wheel installé, puis `uv publish` par Trusted Publishing. L'humain configure
  l'éditeur sur pypi.org et pousse le tag.
