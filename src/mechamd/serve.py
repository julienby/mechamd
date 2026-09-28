"""`mecha serve` : rendu à la requête (Starlette), cache sur la date de modification,
rechargement automatique du navigateur quand un document ou un template change."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from pathlib import Path

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import (
    FileResponse,
    HTMLResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
)
from starlette.routing import Route

from mechamd.css import compile_css, fonts_dir
from mechamd.directive import BUILTIN_DIR
from mechamd.engine import THEMES_DIR, Engine

RELOAD_SCRIPT = """<script>
  (() => {
    const events = new EventSource("/_mecha/events");
    events.onmessage = () => location.reload();
  })();
</script>
"""


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


def create_app(project: str | Path = ".", *, reload: bool = True) -> Starlette:
    site = Site(project=Path(project).resolve(), reload=reload)

    async def page(request: Request) -> Response:
        url_path = request.path_params.get("path", "")
        if url_path and not url_path.endswith("/") and (site.project / url_path).is_dir():
            return RedirectResponse(f"/{url_path}/")
        file = site.resolve(url_path)
        if file is None:
            return HTMLResponse("<h1>404</h1><p>Page introuvable.</p>", status_code=404)
        if file.suffix == ".md":
            return HTMLResponse(site.render(file))
        return FileResponse(file)

    async def css(request: Request) -> Response:
        result = await asyncio.to_thread(compile_css, site.engine)
        if result.error is not None:
            return Response(f"/* {result.error} */", media_type="text/css")
        return FileResponse(result.path, media_type="text/css")

    async def font(request: Request) -> Response:
        fonts = fonts_dir(site.engine)
        file = fonts / request.path_params["name"] if fonts else None
        if file is None or not file.is_file():
            return Response("404", status_code=404)
        # Écrit en dur : sans /etc/mime.types (image Docker slim), Python ne connaît pas `.woff2`.
        return FileResponse(file, media_type="font/woff2" if file.suffix == ".woff2" else None)

    async def events(request: Request) -> Response:
        return StreamingResponse(_changes(site, request), media_type="text/event-stream")

    routes = [
        Route("/_mecha/mecha.css", css),
        Route("/_mecha/fonts/{name}", font),
        Route("/_mecha/events", events),
        Route("/", page),
        Route("/{path:path}", page),
    ]
    return Starlette(routes=routes)


async def _changes(site: Site, request: Request) -> AsyncIterator[str]:  # pragma: no cover
    """Flux SSE : un message à chaque changement de fichier du projet ou des thèmes."""
    from watchfiles import awatch

    stop = asyncio.Event()
    watched = [site.project, BUILTIN_DIR, THEMES_DIR]
    yield ": connecté\n\n"
    async for _ in awatch(*watched, stop_event=stop, watch_filter=_watch_filter):
        if await request.is_disconnected():
            stop.set()
            break
        yield "data: reload\n\n"


def _watch_filter(change: object, path: str) -> bool:  # pragma: no cover
    parts = Path(path).parts
    return not any(p in {".mecha", "dist", "__pycache__", ".git"} for p in parts)


def serve(project: str | Path, host: str, port: int, reload: bool) -> None:  # pragma: no cover
    import uvicorn

    app = create_app(project, reload=reload)
    uvicorn.run(app, host=host, port=port, log_level="warning")
