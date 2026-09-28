# AGENTS.md — règles pour les agents qui travaillent sur mechamd

mechamd transforme du Markdown avec directives (`:::nom{attrs}`) en pages web
Tailwind. La référence est `SPEC.md` ; ce fichier en extrait ce qu'un agent doit
appliquer à chaque tâche.

## Avant d'agir

1. Lire `SPEC.md`, `PROGRESS.md`, `src/mechamd/themes/default/tokens.md` et le
   `README.md` de la directive concernée.
2. Repérer la tâche dans `PROGRESS.md` ; la marquer « en cours ».

## Règles

1. **Exemples d'abord.** Écrire l'exemple `examples/x.md` et son
   `examples/x.data.json`, puis implémenter.
2. **Ne jamais modifier le noyau pour une directive.** Si le contrat `Block` ne
   suffit pas : écrire une ADR dans `decisions/` et s'arrêter sur ce point.
3. **Respecter le socle visuel.** Aucune valeur de style hors `tokens.md`
   (pas de `text-[13px]`, pas de `#3a7`, pas de couleur hors palette).
4. **Toujours l'option la plus simple.** Si c'était une vraie décision, la noter
   en ADR courte (contexte, options, choix).
5. **Petits commits** au format Conventional Commits (`feat:`, `fix:`, `docs:`,
   `test:`, `chore:`, `ci:`, `refactor:`). Une PR par tâche, fusion seulement si
   la CI est verte.
6. **Trois tentatives au plus.** Après 3 tentatives sans CI verte : marquer la
   tâche « bloquée » dans `PROGRESS.md` (avec la raison) et passer à la suivante.
7. **Tenir `PROGRESS.md` à jour** à chaque étape : fait, en cours, bloqué,
   prochaine action.

## Escalade humaine (s'arrêter et demander)

- validation de la direction visuelle (J1) ;
- toute modification du contrat `Block` ou de l'ordre de résolution des variantes ;
- publication sur PyPI.

## Vérifications locales avant chaque push

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv run mecha test
```

## Procédure : ajouter une directive

1. Copier `src/mechamd/directives/card/` comme point de départ (ou un dossier
   `directives/` du projet pour une directive locale).
2. Écrire le `README.md` au format fixe : **Rôle** (une phrase), **Syntaxe**
   (exemple minimal), **Ce qui est deviné**, **Variantes** (nom + une phrase),
   **Attributs**, **Exemples** (renvoi vers `examples/`).
3. Écrire 3 exemples : le cas nu, un cas avec variante explicite, un cas « mal
   écrit » qui doit rester lisible.
4. Implémenter `parse`, `infer_variant` si utile, puis les templates (trois
   variantes au plus, `default.html` obligatoire).
5. Ajouter l'exemple à la page vitrine (`showcase/`) ; `mecha test` vert ; PR.

## Contrat d'une directive (rappel)

```text
directives/<nom>/
  README.md
  directive.py        # parse(block) -> dict ; infer_variant(data) -> str | None (optionnelle)
  templates/default.html  (+ un template par variante)
  examples/<cas>.md + <cas>.data.json
```

- `parse` rend des données simples (textes, nombres, listes, HTML déjà rendu),
  jamais du HTML de présentation. Utiliser `block.md()` et les helpers de
  `mechamd.helpers`. Signaler les problèmes avec `block.warn()`, ne jamais lever
  d'exception pour une entrée mal écrite.
- `infer_variant` : un ou deux signaux évidents au plus, documentés dans le README.
- Templates : racine avec `data-mecha="<nom>"`, `data-variant="<variante>"` et
  l'`id` s'il existe ; HTML sémantique ; `dark:` partout ; mobile correct ;
  aucune logique hors affichage conditionnel simple.
- `x.data.json` : `{"variant": ..., "data": {...}}` et, si utile,
  `"warnings": [...]`. Ces tests portent sur ce que la directive a compris, pas
  sur le HTML.

## Lessons

- 2026-09-28 — Un style global du texte cible seulement le contenu écrit par l'auteur, jamais le HTML des composants. (erreur observée : deux fois, les styles de listes puis de citations du texte ont déformé des templates)
- 2026-09-28 — Une valeur n'a qu'une source de vérité ; les autres endroits la lisent au lieu de la recopier. (erreur observée : version du paquet écrite en deux endroits, une seule mise à jour)
