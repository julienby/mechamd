"""`mecha serve` : rendu à la requête (bibliothèque standard), cache sur la date de
modification, rechargement automatique du navigateur quand un document ou un template change."""

from __future__ import annotations

import mimetypes
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from mechamd.css import compile_css, fonts_dir
from mechamd.directive import BUILTIN_DIR
from mechamd.engine import THEMES_DIR, Engine

# Le navigateur interroge /_mecha/version chaque seconde et recharge quand la valeur change.
RELOAD_SCRIPT = """<script>
  (async () => {
    let seen = null;
    for (;;) {
      try {
        const version = await (await fetch("/_mecha/version")).text();
        if (seen !== null && version !== seen) location.reload();
        seen = version;
      } catch (e) {}
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  })();
</script>
"""

IGNORED_DIRS = {".mecha", "dist", "__pycache__", ".git"}


@dataclass
class Reply:
    status: int = 200
    content_type: str = "text/html; charset=utf-8"
    body: bytes = b""
    location: str | None = None


def _code_signature(project: Path) -> str:
    """Empreinte des directives et thèmes (Python et templates) du projet et fournis."""
    parts: list[str] = []
    for root in (project / "directives", project / "theme", BUILTIN_DIR, THEMES_DIR):
        if root.is_dir():
            for file in sorted(root.rglob("*")):
                if file.is_file() and file.suffix in {".py", ".html", ".css"}:
                    parts.append(f"{file}:{file.stat().st_mtime_ns}")
    return "|".join(parts)


@dataclass
class Site:
    """L'état du serveur : un moteur, reconstruit quand une directive ou le thème change."""

    project: Path
    reload: bool = True
    _engine: Engine | None = None
    _code: str = ""
    _cache: dict[Path, tuple[int, str]] = field(default_factory=dict)

    @property
    def engine(self) -> Engine:
        code = _code_signature(self.project)
        if self._engine is None or code != self._code:
            self._engine, self._code = Engine(project=self.project), code
            self._cache.clear()
        return self._engine

    def resolve(self, url_path: str) -> Path | None:
        """Chemin d'URL → fichier du projet (`/` → `index.md`, `x.html` → `x.md`)."""
        candidate = (self.project / url_path).resolve()
        if not candidate.is_relative_to(self.project):
            return None
        if candidate.is_dir():
            candidate = candidate / "index.md"
        elif candidate.suffix == ".html" and not candidate.is_file():
            candidate = candidate.with_suffix(".md")
        return candidate if candidate.is_file() else None

    def version(self) -> str:
        """Change dès qu'un fichier du projet, une directive ou un thème est modifié."""
        newest = 0
        for root in (self.project, BUILTIN_DIR, THEMES_DIR):
            for file in root.rglob("*"):
                if file.is_file() and not IGNORED_DIRS.intersection(file.parts):
                    newest = max(newest, file.stat().st_mtime_ns)
        return str(newest)

    def respond(self, raw_path: str) -> Reply:
        """Chemin de la requête (avec ou sans `?query`) → réponse."""
        path = unquote(urlsplit(raw_path).path).lstrip("/")
        if path == "_mecha/mecha.css":
            result = compile_css(self.engine)
            if result.error is not None or result.path is None:
                return Reply(content_type="text/css", body=f"/* {result.error} */".encode())
            return Reply(content_type="text/css", body=result.path.read_bytes())
        if path == "_mecha/version":
            return Reply(content_type="text/plain", body=self.version().encode())
        if path.startswith("_mecha/fonts/"):
            fonts = fonts_dir(self.engine)
            file = fonts / path.removeprefix("_mecha/fonts/") if fonts else None
            if file is None or not file.is_file() or file.resolve().parent != fonts.resolve():
                return Reply(404, "text/plain", b"404")
            return _file(file)
        if path and not path.endswith("/") and (self.project / path).is_dir():
            return Reply(307, location=f"/{path}/")
        file = self.resolve(path)
        if file is None:
            return Reply(404, body=b"<h1>404</h1><p>Page introuvable.</p>")
        if file.suffix == ".md":
            return Reply(body=self.render(file).encode())
        return _file(file)

    def render(self, file: Path) -> str:
        engine = self.engine
        mtime = file.stat().st_mtime_ns
        cached = self._cache.get(file)
        if cached is not None and cached[0] == mtime:
            return cached[1]
        html = engine.render_page(file.relative_to(self.project)).html
        if self.reload:
            html = html.replace("</body>", RELOAD_SCRIPT + "</body>", 1)
        self._cache[file] = (mtime, html)
        return html


def _file(file: Path) -> Reply:
    # `.woff2` écrit en dur : sans /etc/mime.types (image Docker slim), Python ne le connaît pas.
    kind = "font/woff2" if file.suffix == ".woff2" else mimetypes.guess_type(file)[0]
    return Reply(content_type=kind or "application/octet-stream", body=file.read_bytes())


def make_server(
    project: str | Path, host: str, port: int, *, reload: bool = True
) -> ThreadingHTTPServer:
    site = Site(project=Path(project).resolve(), reload=reload)
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            with lock:
                reply = site.respond(self.path)
            self.send_response(reply.status)
            self.send_header("Content-Type", reply.content_type)
            self.send_header("Content-Length", str(len(reply.body)))
            if reply.location:
                self.send_header("Location", reply.location)
            self.end_headers()
            self.wfile.write(reply.body)

        def log_message(self, format: str, *args: object) -> None:
            pass

    return ThreadingHTTPServer((host, port), Handler)


def serve(project: str | Path, host: str, port: int, reload: bool) -> None:  # pragma: no cover
    server = make_server(project, host, port, reload=reload)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
