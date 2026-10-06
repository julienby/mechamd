# cta

**Rôle** : un appel à l'action (titre, phrase, bouton), à placer en fin de page.

## Syntaxe

```markdown
:::cta
## Une question ? Écrivez-moi.
Je réponds en général sous deux jours.

[Envoyer un message](mailto:moi@example.org)
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `title` | le premier titre du contenu | — |
| `action` | le lien seul sur la dernière ligne : `href` et `text` | — |
| `text` | le reste, rendu en HTML | — |

Pas de variante devinée.

Avertissements : contenu vide ; pas de bouton (dernière ligne qui n'est pas un lien seul).

## Variantes

- `default` : bandeau d'accent centré, titre, phrase, un bouton blanc.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `sans-titre` (phrase et bouton), `mal-ecrit`
(pas de bouton, variante inconnue), `vide`.
