# grid

**Rôle** : disposer des blocs (des cartes le plus souvent) en colonnes.

## Syntaxe

Le conteneur prend plus de `:` que ses enfants.

```markdown
::::grid
:::card
### DS18B20
Sonde étanche, ±0,5 °C.
:::

:::card
### SHT31
Température et humidité.
:::
::::
```

## Ce qui est deviné

- Nombre de colonnes = nombre de blocs enfants, 3 au plus (surcharge : `cols=`, de 1 à 4).
- Sur mobile, une seule colonne ; deux sur tablette.
- `card=cover` (ou tout `<directive>=<variante>`) fixe la variante des enfants,
  sauf ceux qui précisent la leur.

## Variantes

- `default` : colonnes de même largeur, gouttière `gap-6`, largeur `max-w-5xl`.

## Attributs

- `cols=` : nombre de colonnes sur grand écran (1 à 4).
- `<directive>=<variante>` : variante des enfants (rang 2 de la résolution).

## Exemples

Voir `examples/` : `nu` (cas nu, 2 colonnes devinées), `cover` (`cols=3 card=cover`,
un enfant garde sa variante), `mal-ecrit` (`cols` illisible, pas d'enfant).
