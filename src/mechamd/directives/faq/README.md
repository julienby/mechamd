# faq

**Rôle** : une foire aux questions, une question repliable par élément.

## Syntaxe

```markdown
:::faq
- Faut-il installer Python ?
  Non : `install.sh` installe `uv`, qui s'occupe du reste.
- Le site est-il statique ?
  Oui, `mecha build` produit du HTML à héberger n'importe où.
:::
```

## Ce qui est deviné

| Donnée | Source par défaut | Surcharge |
| --- | --- | --- |
| `questions[].question` | le texte de l'élément de liste | — |
| `questions[].answer` | les lignes indentées sous la question, rendues en HTML | — |
| `intro` | le texte hors de la liste, rendu en HTML | — |

Pas de variante devinée. Pour une seule question repliable, utiliser `details`.

Avertissements : aucune question ; question sans réponse (gardée, sans texte).

## Variantes

- `default` : les questions dans un seul bloc, fermées ; un clic ouvre la réponse.

## Attributs

Aucun.

## Exemples

Voir `examples/` : `nu` (cas nu), `intro` (texte avant la liste, réponse sur
plusieurs paragraphes), `mal-ecrit` (question sans réponse, variante inconnue),
`vide`.
