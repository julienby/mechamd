#!/bin/sh
# Installe mechamd (et uv s'il manque) : curl -LsSf <url de ce fichier> | sh
set -eu

SOURCE="${MECHAMD_SOURCE:-git+https://github.com/julienby/mechamd}"

if ! command -v uv >/dev/null 2>&1; then
  echo "→ installation de uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  PATH="$HOME/.local/bin:$PATH"
fi

uv tool install --force "$SOURCE"

echo
echo "mechamd est installé. Essayez : mecha --help"
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) echo "Ajoutez \$HOME/.local/bin à votre PATH (ou ouvrez un nouveau terminal)." ;;
esac
