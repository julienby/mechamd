import mimetypes
import os
import stat
import threading
import urllib.request
from pathlib import Path

import pytest

from mechamd import Engine
from mechamd.build import build
from mechamd.cli import main
from mechamd.css import CssResult, compile_css, find_tailwind, input_css, signature
from mechamd.engine import rewrite_md_links
from mechamd.serve import Site, make_server

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
    assert (dist / "_mecha" / "fonts" / "inter-latin-wght-normal.woff2").is_file()
    assert "fonts.googleapis.com" not in home
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


def test_serve(site: Path, tailwind: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Sans /etc/mime.types (image Docker slim), Python ne connaît pas `.woff2`.
    monkeypatch.setattr(mimetypes, "_db", mimetypes.MimeTypes())
    app = Site(site.resolve())
    home = app.respond("/")
    assert home.status == 200 and b"Accueil" in home.body
    assert b"_mecha/version" in home.body
    assert app.respond("/index.html").body == home.body  # servi depuis le cache
    assert b"B204" in app.respond("/notes/b204.html?x=1").body
    assert app.respond("/notes/b204.md").status == 200
    redirect = app.respond("/notes")
    assert redirect.status == 307 and redirect.location == "/notes/"
    assert b"Notes" in app.respond("/notes/").body
    assert app.respond("/photos/a.svg").body == b"<svg/>"
    assert app.respond("/photos/a.svg").content_type == "image/svg+xml"
    assert app.respond("/absent.html").status == 404
    assert app.respond("/../../etc/passwd").status == 404
    assert app.respond("//etc/passwd").status == 404
    css = app.respond("/_mecha/mecha.css")
    assert css.status == 200 and css.body == b"/* css */\n"
    font = app.respond("/_mecha/fonts/inter-latin-wght-normal.woff2")
    assert font.status == 200 and font.content_type == "font/woff2"
    assert app.respond("/_mecha/fonts/absent.woff2").status == 404
    assert app.respond("/_mecha/fonts/..").status == 404


def test_serve_picks_up_changes(site: Path, tailwind: Path) -> None:
    app = Site(site.resolve(), reload=False)
    assert b"_mecha/version" not in app.respond("/").body
    before = app.respond("/_mecha/version").body
    page = site / "index.md"
    page.write_text("# Changé\n")
    os.utime(page, ns=(1, 2))
    assert "Changé" in app.respond("/").body.decode()
    assert app.respond("/_mecha/version").body == before  # mtime ancien : même version
    page.write_text("# Encore\n")
    assert app.respond("/_mecha/version").body != before


def test_serve_over_http(site: Path, tailwind: Path) -> None:
    server = make_server(site, "127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}"
        with urllib.request.urlopen(f"{url}/") as response:
            assert response.status == 200 and b"Accueil" in response.read()
    finally:
        server.shutdown()
        server.server_close()


def test_serve_css_error(site: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mechamd.serve.compile_css", failed)
    css = Site(site.resolve()).respond("/_mecha/mecha.css")
    assert css.status == 200 and b"pas de binaire" in css.body
