---
title: Vitrine mechamd
date: 2026-09-28
tags: [vitrine, thème default]
---

La référence visuelle du projet. Chaque directive y montre chacune de ses
variantes ; on juge le rendu ici, à l'œil, en clair et en sombre (bouton en
haut à droite), sur grand écran et sur mobile.

## Typographie

Le texte courant est en **Inter**, les titres en *Newsreader*. Une colonne de
lecture d'environ soixante-cinq caractères, un interlignage généreux, et des
[liens discrets mais visibles](#typographie). Le `code en ligne` reste lisible
sans crier.

- Trois sondes DS18B20 fixées à 2 cm de la paroi ;
- une mesure toutes les 30 secondes ;
- deux semaines d'acquisition en salle B204.

> Le beau vient des templates, pas de l'auteur.

| Sonde | Position | Écart moyen |
| --- | --- | --- |
| S1 | porte | +0,4 °C |
| S2 | fenêtre | −1,1 °C |
| S3 | centre | +0,1 °C |

```python
engine = Engine(project="mon-site/")
html = engine.render("content/manip-b204.md")
```

## card

Un bloc de contenu autonome. Sans aucun attribut, mechamd choisit la variante
à partir du contenu.

### default — cas général

Titre, texte, lien d'action en bas ; toute la carte est cliquable.

:::card
### Capteur DS18B20
Sonde de température étanche, précision ±0,5 °C, bus 1-Wire. Idéale pour
les mesures longues en milieu humide.
[Voir la fiche](#card)
:::

### default — sans lien

:::card
### Note du 12 septembre
Recalibrage des trois sondes après le déménagement du banc. Écart résiduel
inférieur à **0,2 °C** sur S1 et S3 ; S2 à surveiller.
:::

### image — devinée

Une image dans le contenu suffit à choisir la variante `image`.

:::card
![Courbe de température sur deux semaines](photos/courbe.svg)
### Installation en B204
Trois sondes fixées à 2 cm de la paroi, relevé toutes les 30 secondes.
[Voir les mesures](#card)
:::

### cover — demandée explicitement

:::card{.cover}
![Relevé topographique de la salle](photos/salle.svg)
## Salle B204
Deux semaines de mesures, trois capteurs, une carte thermique complète.
[Ouvrir le suivi](#card)
:::

### cover — sans image

:::card{.cover}
## Prototype BOB
Un fond d'accent remplace l'image absente.
:::

### image — texte long et image claire

:::card
![Carte électronique du prototype](photos/prototype.svg)
### Premier prototype BOB, mars 2025
Carte d'acquisition à base d'ESP32, trois entrées 1-Wire, alimentation par
batterie. Le boîtier imprimé en PETG tient dans la main ; l'autonomie mesurée
atteint neuf jours avec une mesure toutes les 30 secondes.
:::

## Ce qui n'est pas compris

Une directive inconnue ou mal écrite ne casse jamais la page : son texte
s'affiche dans un encadré discret.

:::galerie{cols=4}
Cette directive n'existe pas encore. Son **contenu** reste lisible.
:::
