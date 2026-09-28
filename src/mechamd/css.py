"""Compilation du CSS avec le binaire autonome Tailwind CSS v4 (sans Node).

Tailwind scanne les templates des directives et du thème, jamais les documents :
écrire un document ne demande aucune recompilation. Le CSS n'est recompilé que
si un template ou une feuille du thème change (signature des fichiers).
"""

from __future__ import annotations

import hashlib
import os
import platform
import shutil
import stat
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from mechamd.engine import Engine

TAILWIND_VERSION = "v4.3.3"
RELEASES = "https://github.com/tailwindlabs/tailwindcss/releases/download"


@dataclass
class CssResult:
    path: Path
    compiled: bool
    """Vrai si le CSS vient d'être recompilé (faux s'il était à jour)."""
    error: str | None = None


def cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache"
    return Path(base) / "mechamd"


def _asset_name() -> str | None:
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch = {"x86_64": "x64", "amd64": "x64", "arm64": "arm64", "aarch64": "arm64"}.get(machine)
    if arch is None:
        return None
    if system == "linux":
        return f"tailwindcss-linux-{arch}"
    if system == "darwin":
        return f"tailwindcss-macos-{arch}"
    if system == "windows" and arch == "x64":
        return "tailwindcss-windows-x64.exe"
    return None


def find_tailwind(download: bool = True) -> Path | None:
    """Le binaire Tailwind : `$MECHA_TAILWIND`, puis le cache, sinon téléchargé une fois."""
    configured = os.environ.get("MECHA_TAILWIND")
    if configured:
        return Path(configured)
    cached = cache_dir() / f"tailwindcss-{TAILWIND_VERSION}"
    if cached.is_file():
        return cached
    asset = _asset_name()
    if not download or asset is None:
        return None
    cached.parent.mkdir(parents=True, exist_ok=True)
    tmp = cached.with_suffix(".part")
    try:
        with urllib.request.urlopen(f"{RELEASES}/{TAILWIND_VERSION}/{asset}", timeout=60) as r:
            tmp.write_bytes(r.read())
    except OSError:
        tmp.unlink(missing_ok=True)
        return None
    tmp.chmod(tmp.stat().st_mode | stat.S_IEXEC)
    tmp.replace(cached)
    return cached


def sources(engine: Engine) -> list[Path]:
    """Dossiers que Tailwind doit scanner : templates des directives et thèmes."""
    dirs = [d.templates_dir for d in engine.directives.values()]
    dirs += [d for d in engine.theme_dirs if d.is_dir()]
    return dirs


def signature(engine: Engine) -> str:
    """Empreinte des templates et feuilles de style : change quand l'un d'eux change."""
    digest = hashlib.sha256(TAILWIND_VERSION.encode())
    for root in sources(engine):
        for file in sorted(root.rglob("*")):
            if file.suffix in {".html", ".css"} and file.is_file():
                info = file.stat()
                digest.update(f"{file}:{info.st_mtime_ns}:{info.st_size}".encode())
    return digest.hexdigest()


def input_css(engine: Engine) -> str:
    """Feuille d'entrée : la feuille du thème, plus une source par dossier de templates."""
    theme_css = next(d / "mecha.css" for d in engine.theme_dirs if (d / "mecha.css").is_file())
    lines = [f'@import "{theme_css.as_posix()}";']
    lines += [f'@source "{d.as_posix()}";' for d in sources(engine)]
    return "\n".join(lines) + "\n"


def compile_css(engine: Engine, out: Path | None = None, *, force: bool = False) -> CssResult:
    """Compile le CSS du projet dans `.mecha/mecha.css` (ou `out`) s'il n'est pas à jour."""
    work = engine.project / ".mecha"
    target = out or work / "mecha.css"
    sig = signature(engine)
    sig_file = target.with_name(target.name + ".sig")
    if not force and target.is_file() and sig_file.is_file() and sig_file.read_text() == sig:
        return CssResult(target, compiled=False)

    binary = find_tailwind()
    if binary is None:
        return CssResult(target, False, "binaire Tailwind introuvable (définir MECHA_TAILWIND)")
    work.mkdir(parents=True, exist_ok=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    entry = work / "input.css"
    entry.write_text(input_css(engine), encoding="utf-8")
    try:
        proc = subprocess.run(
            [str(binary), "-i", str(entry), "-o", str(target), "--minify"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return CssResult(target, False, f"Tailwind n'a pas pu être lancé : {exc}")
    if proc.returncode != 0 or not target.is_file():
        return CssResult(target, False, f"Tailwind a échoué : {proc.stderr.strip()[-500:]}")
    sig_file.write_text(sig)
    return CssResult(target, compiled=True)


def copy_css(result: CssResult, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(result.path, dest)
