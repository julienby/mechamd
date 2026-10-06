# Tuto : un site portfolio avec mechamd

Résultat : un site statique (HTML + CSS) de quelques pages, qui se publie
n'importe où. Compter 10 minutes. Le site de départ de ce tuto est
`../portfolio` (à côté de ce dépôt) ; refaire le même chemin pour un autre site.

## 1. Installer (une fois)

```sh
curl -LsSf https://raw.githubusercontent.com/julienby/mechamd/main/install.sh | sh
mecha --version
```

Le premier `build` ou `serve` télécharge le binaire Tailwind CSS (réseau requis
une fois).

## 2. Créer le site

```sh
mecha new portfolio        # crée portfolio/index.md
mkdir portfolio/projets    # une page par projet, dans ce dossier
```

Règle de base : **un fichier `.md` = une page**. `projets/mechamd.md` donne
`projets/mechamd.html`. Les liens entre pages s'écrivent vers le `.md`
(`[fiche](projets/mechamd.md)`) : le build les convertit.

## 3. Écrire les pages

Chaque page commence par un en-tête :

```markdown
---
title: Mon titre
layout: page
---
```

Puis du Markdown ordinaire. Pour une mise en forme, un bloc `:::directive` :

| Je veux… | Directive |
| --- | --- |
| une grande ouverture de page | `:::section{.hero}` |
| des chiffres clés | `:::stats` (lignes `- 48 h : d'acquisition`) |
| des cartes en colonnes | `::::grid` contenant des `:::card` |
| une fiche clé : valeur | `:::specs` |
| une procédure numérotée | `:::steps` |
| un encadré | `:::callout` (« Astuce : … », « Attention : … ») |
| des liens commentés | `:::links` |
| une image avec légende | `:::figure` |

La liste complète et la syntaxe de chacune : `mecha llms` (ou la vitrine
`showcase/` du dépôt). Le moteur devine la présentation ; n'ajouter `.variante`
que pour la forcer.

Trois pièges vus en pratique :

- **Imbrication** : le parent prend plus de `:` que ses enfants
  (`::::grid` contient des `:::card`).
- **Ancres** : `:::section{#projets}` crée l'ancre, `[Voir](#projets)` y renvoie.
- **Rien ne casse** : une directive mal écrite reste lisible. `mecha explain
  index.md` montre la variante retenue pour chaque bloc, et les avertissements.

## 4. Voir le résultat

```sh
mecha serve portfolio      # http://127.0.0.1:8000/ — la page se recharge à chaque enregistrement
mecha explain index.md -p portfolio
```

## 5. Générer le site statique

```sh
mecha build portfolio      # résultat dans portfolio/dist/
```

`dist/` contient tout : copier ce dossier sur n'importe quel hébergement
statique (GitHub Pages, Netlify, un serveur web, un dossier partagé).
Les images et fichiers placés à côté des `.md` sont copiés tels quels.

## 6. Refaire un autre site

```sh
mecha new autre-site && mecha serve autre-site
```

Pour demander à un LLM d'écrire les pages : lui donner la sortie de
`mecha llms` ; elle décrit toute la syntaxe.

## Pièges d'outillage

- Depuis un autre dépôt, `uv --directory <dépôt> run mecha new portfolio`
  crée le dossier **dans** `<dépôt>`, pas dans le dossier courant. Utiliser
  `mecha` installé, ou un chemin absolu.
- Le port 8000 est parfois pris : `mecha serve portfolio --port 8791`.
