# probe

**Rôle** : directive de test du noyau (résolution des variantes, erreurs).

**Syntaxe** : `:::probe` puis du texte.

**Ce qui est deviné** : le mot « alt » en tête du texte → `alt`.

**Variantes** : `default`, `alt`, `fails` (template volontairement cassé).

**Attributs** : `boom=1` fait lever une exception à `parse` ; `guess=x` fait deviner `x`.

**Exemples** : voir `examples/`.
