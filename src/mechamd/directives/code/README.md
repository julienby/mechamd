# code

**Rôle** : un bloc de code présenté (nom de fichier, bouton « copier »), pour
une commande à recopier ou un extrait de configuration.

## Syntaxe

````markdown
:::code{file=install.sh}
```bash
curl -fsSL https://example.org/install.sh | sh
```
:::
````

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `snippets` | chaque bloc clôturé du contenu | — |
| `title` d'un extrait | `{title=…}` après le langage ; sinon le langage | `file=` (un seul extrait) |

Pas de variante devinée. Plusieurs extraits : empilés, chacun avec son titre
(`bash {title=Linux}`).

Avertissements : aucun bloc de code.

## Variantes

- `default` : cadre sombre, barre de titre, bouton « Copier ».

## Attributs

- `file` : titre de l'extrait quand il n'y en a qu'un.

## Exemples

Voir `examples/` : `nu`, `plusieurs`, `mal-ecrit` (pas de bloc de code), `vide`.
