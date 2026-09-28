import os
import stat
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from mechamd import Engine
from mechamd.build import build
from mechamd.cli import main
from mechamd.css import CssResult, compile_css, find_tailwind, input_css, signature
from mechamd.engine import rewrite_md_links
from mechamd.serve import create_app

FAKE_TAILWIND = """#!/bin/sh
# faux Tailwind : écrit le fichier -o et compte ses appels
while [ "$#" -gt 0 ]; do
  case "$1" in -o) out="$2"; shift;; esac
  shift
done
echo "/* css */" > "$out"
echo x >> "$(dirname "$0")/calls"
"""


@pytest.fixture
def tailwind(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    binary = tmp_path / "bin" / "tailwindcss"
    binary.parent.mkdir()
    binary.write_text(FAKE_TAILWIND)
    binary.chmod(binary.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("MECHA_TAILWIND", str(binary))
    return binary


@pytest.fixture
def site(tmp_path: Path) -> Path:
    project = tmp_path / "site"
    (project / "notes").mkdir(parents=True)
    (project / "photos").mkdir()
    (project / ".cache").mkdir()
    (project / "index.md").write_text(
        "# Accueil\n\n[Notes](notes/b204.md#mesures)\n\n:::card\n### Carte\n:::\n"
    )
    (project / "notes" / "b204.md").write_text("# B204\n\n## Mesures\n\n[Retour](../index.md)\n")
    (project / "notes" / "index.md").write_text("# Notes\n")
    (project / "photos" / "a.svg").write_text("<svg/>")
    (project / ".cache" / "x.md").write_text("caché")
    return project


def calls(tailwind: Path) -> int:
    file = tailwind.parent / "calls"
    return len(file.read_text().splitlines()) if file.exists() else 0


def failed(engine: Engine) -> CssResult:
    return CssResult(engine.project / "x.css", False, "pas de binaire")


def test_rewrite_md_links() -> None:
    html = '<a href="a/b.md#x"><a href="https://x.org/a.md"><a href="/a.md"><a href="#t.md">'
    assert rewrite_md_links(html) == (
        '<a href="a/b.html#x"><a href="https://x.org/a.md"><a href="/a.md"><a href="#t.md">'
    )


def test_css_compiled_once_then_cached(site: Path, tailwind: Path) -> None:
    engine = Engine(project=site)
    assert "@import" in input_css(engine) and "card/templates" in input_css(engine)
    first = compile_css(engine)
    assert first.error is None and first.compiled
    assert compile_css(engine).compiled is False
    assert calls(tailwind) == 1
    # une directive locale ajoute un template : la signature change, on recompile
    before = signature(engine)
    local = site / "directives" / "note"
    (local / "templates").mkdir(parents=True)
    (local / "templates" / "default.html").write_text("<p {{ root_attrs(block) }}></p>")
    (local / "directive.py").write_text("def parse(block):\n    return {}\n")
    engine = Engine(project=site)
    assert signature(engine) != before
    assert compile_css(engine).compiled
    assert calls(tailwind) == 2


def test_css_errors(site: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    failing = tmp_path / "fail.sh"
    failing.write_text("#!/bin/sh\necho boum >&2\nexit 1\n")
    failing.chmod(0o755)
    monkeypatch.setenv("MECHA_TAILWIND", str(failing))
    assert "boum" in (compile_css(Engine(project=site)).error or "")
    monkeypatch.setenv("MECHA_TAILWIND", str(tmp_path / "absent"))
    assert "lancé" in (compile_css(Engine(project=site)).error or "")
    monkeypatch.delenv("MECHA_TAILWIND")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "vide"))
    assert find_tailwind(download=False) is None
    monkeypatch.setattr("mechamd.css.find_tailwind", lambda: None)
    assert "introuvable" in (compile_css(Engine(project=site)).error or "")


def test_find_tailwind_uses_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from mechamd.css import TAILWIND_VERSION

    monkeypatch.delenv("MECHA_TAILWIND", raising=False)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    cached = tmp_path / "mechamd" / f"tailwindcss-{TAILWIND_VERSION}"
    cached.parent.mkdir()
    cached.write_text("")
    assert find_tailwind() == cached


def test_build(site: Path, tailwind: Path, capsys: pytest.CaptureFixture[str]) -> None:
    report = build(site)
    dist = site / "dist"
    assert sorted(str(p) for p in report.pages) == ["index.md", "notes/b204.md", "notes/index.md"]
    assert [str(p) for p in report.assets] == ["photos/a.svg"]
    home = (dist / "index.html").read_text()
    assert 'href="notes/b204.html#mesures"' in home
    assert 'href="_mecha/mecha.css"' in home
    assert "EventSource" not in home
    note = (dist / "notes" / "b204.html").read_text()
    assert 'href="../_mecha/mecha.css"' in note and 'href="../index.html"' in note
    assert (dist / "_mecha" / "mecha.css").read_text() == "/* css */\n"
    assert not (dist / ".cache").exists()
    # reconstruire ne reprend pas dist/ comme contenu
    assert main(["build", str(site)]) == 0
    assert "3 pages, 1 fichiers copiés" in capsys.readouterr().out


def test_build_reports_css_error(
    site: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    (site / "doc.md").write_text(":::inconnue\n:::\n")
    monkeypatch.setattr("mechamd.build.compile_css", failed)
    assert main(["build", str(site), "-o", str(tmp_path / "out")]) == 1
    out = capsys.readouterr().out
    assert "✗ CSS : pas de binaire" in out and "directive inconnue" in out
    assert (tmp_path / "out" / "doc.html").is_file()


def test_serve(site: Path, tailwind: Path) -> None:
    client = TestClient(create_app(site))
    home = client.get("/")
    assert home.status_code == 200 and "Accueil" in home.text
    assert "EventSource" in home.text
    assert client.get("/index.html").text == home.text  # servi depuis le cache
    assert "B204" in client.get("/notes/b204.html").text
    assert client.get("/notes/b204.md").status_code == 200
    redirect = client.get("/notes", follow_redirects=False)
    assert redirect.status_code == 307 and redirect.headers["location"] == "/notes/"
    assert "Notes" in client.get("/notes/").text
    assert client.get("/photos/a.svg").text == "<svg/>"
    assert client.get("/absent.html").status_code == 404
    assert client.get("/../../etc/passwd").status_code == 404
    css = client.get("/_mecha/mecha.css")
    assert css.status_code == 200 and css.text == "/* css */\n"


def test_serve_picks_up_changes(site: Path, tailwind: Path) -> None:
    client = TestClient(create_app(site, reload=False))
    assert "EventSource" not in client.get("/").text
    page = site / "index.md"
    page.write_text("# Changé\n")
    os.utime(page, ns=(1, 2))
    assert "Changé" in client.get("/").text


def test_serve_css_error(site: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mechamd.serve.compile_css", failed)
    css = TestClient(create_app(site)).get("/_mecha/mecha.css")
    assert css.status_code == 200 and "pas de binaire" in css.text
