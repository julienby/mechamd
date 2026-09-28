# CI à activer

L'agent ne peut pas pousser dans `.github/workflows/` (jeton sans portée
`workflow`). Pour activer la CI, un humain déplace ce fichier :

```sh
mkdir -p .github/workflows && git mv ci/github-ci.yml .github/workflows/ci.yml
```

Les mêmes vérifications se lancent en local :
`uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest && uv run mecha test`.
