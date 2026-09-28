"""Le moteur : `render(fichier) -> html`.

Le noyau ne connaît aucune directive : il repère les blocs `:::nom{attrs}`,
les confie au module de la directive, résout la variante et rend le template.
"""

from __future__ import annotations

import re
import textwrap
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from frontmatter.default_handlers import YAMLHandler
from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PrefixLoader,
    StrictUndefined,
    select_autoescape,
)
from markdown_it.token import Token
from markupsafe import Markup, escape

from mechamd.attrs import parse_info
from mechamd.block import Block, RenderedBlock
from mechamd.directive import BUILTIN_DIR, Directive, discover
from mechamd.markdown import DIRECTIVE_CLOSE, DIRECTIVE_OPEN, create_md

THEMES_DIR = Path(__file__).parent / "themes"


@dataclass(frozen=True)
class BlockView:
    """Ce que les templates reçoivent sous le nom `block`."""

    name: str
    variant: str
    id: str | None
    attrs: dict[str, str]


@dataclass
class BlockReport:
    """Ce que le moteur a compris d'un bloc (pour `mecha explain` et `mecha test`)."""

    name: str
    line: int
    variant: str
    reason: str
    data: dict[str, Any]
    warnings: list[str] = field(default_factory=list)
    known: bool = True


@dataclass
class Page:
    title: str
    meta: dict[str, Any]
    body: str
    html: str
    blocks: list[BlockReport]
    warnings: list[str]


@dataclass
class _Context:
    lines: list[str]
    offset: int
    record: bool
    reports: list[BlockReport]
    ids: set[str]


def root_attrs(block: BlockView) -> Markup:
    """Attributs obligatoires de l'élément racine d'un template de directive."""
    parts = [
        f'data-mecha="{escape(block.name)}"',
        f'data-variant="{escape(block.variant)}"',
    ]
    if block.id:
        parts.append(f'id="{escape(block.id)}"')
    return Markup(" ".join(parts))


_MD_LINK_RE = re.compile(
    r'(?P<attr>\bhref)="(?![a-zA-Z][a-zA-Z0-9+.-]*:|/|#)(?P<path>[^"#?]*?)\.md(?P<tail>[#?][^"]*)?"'
)


def rewrite_md_links(html: str) -> str:
    """`href="notes/b204.md#x"` → `href="notes/b204.html#x"` (liens relatifs seulement)."""
    return _MD_LINK_RE.sub(lambda m: f'{m["attr"]}="{m["path"]}.html{m["tail"] or ""}"', html)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str, int, list[str]]:
    """Sépare le frontmatter ; rend (meta, corps, lignes avant le corps, avertissements)."""
    handler = YAMLHandler()
    if not handler.detect(text):
        return {}, text, 0, []
    try:
        fm, body = handler.split(text)
        meta = handler.load(fm) or {}
    except Exception as exc:
        return {}, text, 0, [f"frontmatter illisible, ignoré : {exc}"]
    if not isinstance(meta, dict):
        return {}, body, text[: len(text) - len(body)].count("\n"), ["frontmatter ignoré"]
    offset = text[: len(text) - len(body)].count("\n")
    return meta, body, offset, []


def _matching_close(tokens: Sequence[Token], i: int) -> int:
    depth = 0
    for k in range(i, len(tokens)):
        if tokens[k].type == DIRECTIVE_OPEN:
            depth += 1
        elif tokens[k].type == DIRECTIVE_CLOSE:
            depth -= 1
            if depth == 0:
                return k
    return len(tokens) - 1  # pragma: no cover - markdown-it ferme toujours


class Engine:
    """Moteur mechamd pour un projet (dossier contenant documents et `directives/`)."""

    def __init__(self, project: str | Path | None = None, theme: str = "default") -> None:
        self.project = Path(project if project is not None else ".").resolve()
        self.directives: dict[str, Directive]
        self.directives, self.load_errors = discover([self.project / "directives", BUILTIN_DIR])
        self.md = create_md()
        self.theme_dirs = [self.project / "theme", THEMES_DIR / theme]
        theme_dirs = self.theme_dirs
        self.jinja = Environment(
            loader=ChoiceLoader(
                [
                    FileSystemLoader([d for d in theme_dirs if d.is_dir()]),
                    PrefixLoader(
                        {n: FileSystemLoader(d.templates_dir) for n, d in self.directives.items()}
                    ),
                ]
            ),
            autoescape=select_autoescape(default=True, default_for_string=True),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.jinja.globals["root_attrs"] = root_attrs

    # --- API publique -------------------------------------------------

    def render(self, path: str | Path) -> str:
        """Rend un fichier du projet en page HTML complète."""
        return self.render_page(path).html

    def render_page(self, path: str | Path) -> Page:
        file = self._confine(path)
        depth = len(file.relative_to(self.project).parts) - 1
        return self.render_source(
            file.read_text(encoding="utf-8"), name=file.stem, root="../" * depth
        )

    def render_source(self, text: str, *, name: str = "", root: str = "") -> Page:
        """Rend un texte mechamd (frontmatter + Markdown + directives).

        `root` est le chemin relatif de la page vers la racine du site (`../` par niveau).
        Les liens relatifs vers des `.md` sont réécrits en `.html`.
        """
        meta, body, offset, warnings = split_frontmatter(text)
        ctx = _Context(lines=body.splitlines(), offset=offset, record=True, reports=[], ids=set())
        tokens = self.md.parse(body)
        content = self._render_tokens(tokens, 0, len(tokens), ctx, {})
        h1 = _first_h1(tokens)
        title = str(meta.get("title") or h1 or name or "Sans titre")
        ctx.reports.sort(key=lambda r: r.line)  # enfants rendus avant leur parent
        for report in ctx.reports:
            warnings.extend(f"ligne {report.line} ({report.name}) : {w}" for w in report.warnings)
        layout = self.jinja.get_template("layout.html")
        html = layout.render(
            page={
                "title": title,
                "meta": meta,
                "warnings": warnings,
                "has_h1": h1 is not None,
                "toc": _toc(tokens),
                "root": root,
            },
            content=Markup(content),
        )
        return Page(title, meta, content, rewrite_md_links(html), ctx.reports, warnings)

    def analyze(self, text: str) -> list[BlockReport]:
        """Ce que le moteur comprend de chaque bloc (sans produire la page)."""
        return self.render_source(text).blocks

    # --- rendu --------------------------------------------------------

    def _confine(self, path: str | Path) -> Path:
        file = (self.project / path).resolve()
        if not file.is_relative_to(self.project):
            raise ValueError(f"chemin hors du projet : {path}")
        return file

    def _render_fragment(self, text: str, parent_ctx: _Context) -> str:
        ctx = _Context(
            lines=text.splitlines(), offset=0, record=False, reports=[], ids=parent_ctx.ids
        )
        tokens = self.md.parse(text)
        return self._render_tokens(tokens, 0, len(tokens), ctx, {})

    def _render_tokens(
        self,
        tokens: Sequence[Token],
        start: int,
        end: int,
        ctx: _Context,
        parent_attrs: dict[str, str],
    ) -> str:
        out: list[str] = []
        i = start
        while i < end:
            if tokens[i].type == DIRECTIVE_OPEN:
                close = _matching_close(tokens, i)
                out.append(self._render_directive(tokens, i, close, ctx, parent_attrs).html)
                i = close + 1
            else:
                k = i
                while k < end and tokens[k].type != DIRECTIVE_OPEN:
                    k += 1
                out.append(self.md.renderer.render(list(tokens[i:k]), self.md.options, {}))
                i = k
        return "".join(out)

    def _render_directive(
        self,
        tokens: Sequence[Token],
        i: int,
        close: int,
        ctx: _Context,
        parent_attrs: dict[str, str],
    ) -> RenderedBlock:
        opening = tokens[i]
        info = parse_info(opening.info)
        start, end = opening.map or (0, 0)
        content = textwrap.dedent("\n".join(ctx.lines[start + 1 : end]))
        block = Block(
            name=info.name,
            variant=info.variant,
            id=info.id,
            attrs=info.attrs,
            content=content,
            line=ctx.offset + start + 1,
            warnings=list(info.warnings),
            _render_md=lambda text: self._render_fragment(text, ctx),
        )
        if block.id and ctx.record:
            if block.id in ctx.ids:
                block.warn(f"id « {block.id} » déjà utilisé dans le document")
            ctx.ids.add(block.id)

        directive = self.directives.get(block.name)
        if directive is None:
            block.warn(f"directive inconnue : « {block.name} »")
            inner = self._render_tokens(tokens, i + 1, close, ctx, block.attrs)
            return self._fallback(block, inner, ctx, reason="directive inconnue")

        block.children = self._children(tokens, i, close, ctx, block.attrs)
        try:
            data = directive.parse(block)
            if not isinstance(data, dict):
                raise TypeError(f"parse doit rendre un dict, pas {type(data).__name__}")
        except Exception as exc:
            block.warn(f"erreur dans parse : {exc}")
            inner = self._render_fragment(block.content, ctx)
            return self._fallback(block, inner, ctx, reason="erreur dans parse")

        variant, reason = self.resolve(directive, block, data, parent_attrs)
        view = BlockView(block.name, variant, block.id, block.attrs)
        try:
            template = self.jinja.get_template(f"{block.name}/{variant}.html")
            html = template.render(**data, block=view)
        except Exception as exc:
            block.warn(f"erreur dans le template {variant}.html : {exc}")
            inner = self._render_fragment(block.content, ctx)
            return self._fallback(block, inner, ctx, reason="erreur de template")
        self._record(ctx, block, variant, reason, data)
        return RenderedBlock(block.name, variant, block.id, html)

    def _children(
        self,
        tokens: Sequence[Token],
        i: int,
        close: int,
        ctx: _Context,
        attrs: dict[str, str],
    ) -> list[RenderedBlock]:
        children: list[RenderedBlock] = []
        k = i + 1
        while k < close:
            if tokens[k].type == DIRECTIVE_OPEN:
                child_close = _matching_close(tokens, k)
                children.append(self._render_directive(tokens, k, child_close, ctx, attrs))
                k = child_close + 1
            else:
                k += 1
        return children

    def _fallback(self, block: Block, inner: str, ctx: _Context, reason: str) -> RenderedBlock:
        self._record(ctx, block, "unknown", reason, {}, known=False)
        view = BlockView(block.name, "unknown", block.id, block.attrs)
        html = self.jinja.get_template("unknown.html").render(
            block=view, reason=reason, body=Markup(inner)
        )
        return RenderedBlock(block.name, "unknown", block.id, html)

    def _record(
        self,
        ctx: _Context,
        block: Block,
        variant: str,
        reason: str,
        data: dict[str, Any],
        known: bool = True,
    ) -> None:
        if ctx.record:
            ctx.reports.append(
                BlockReport(block.name, block.line, variant, reason, data, block.warnings, known)
            )

    # --- variantes ----------------------------------------------------

    def resolve(
        self,
        directive: Directive,
        block: Block,
        data: dict[str, Any],
        parent_attrs: dict[str, str],
    ) -> tuple[str, str]:
        """Résout la variante d'un bloc ; rend (variante, raison).

        Ordre : 1. écrite sur le bloc, 2. fixée par le parent, 3. devinée, sinon `default`.
        Une variante demandée mais inexistante retombe sur le rang 3, avec un avertissement.
        """
        available = directive.variants

        def check(variant: str, source: str) -> bool:
            if variant in available:
                return True
            block.warn(
                f"variante « {variant} » ({source}) inexistante ; "
                f"disponibles : {', '.join(available)}"
            )
            return False

        if block.variant and check(block.variant, "écrite sur le bloc"):
            return block.variant, "écrite sur le bloc"
        from_parent = parent_attrs.get(block.name)
        if from_parent and not block.variant and check(from_parent, "fixée par le parent"):
            return from_parent, "fixée par le parent"
        if directive.infer_variant is not None:
            try:
                guessed = directive.infer_variant(data)
            except Exception as exc:
                block.warn(f"erreur dans infer_variant : {exc}")
                guessed = None
            if guessed and check(guessed, "devinée"):
                return guessed, "devinée"
        return "default", "par défaut"


def _first_h1(tokens: Sequence[Token]) -> str | None:
    for k, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag == "h1" and token.level == 0:
            return tokens[k + 1].content
    return None


def _toc(tokens: Sequence[Token]) -> list[dict[str, str]]:
    """Titres `##` du document (hors blocs) pour le sommaire."""
    return [
        {"id": str(token.attrs.get("id", "")), "text": tokens[k + 1].content}
        for k, token in enumerate(tokens)
        if token.type == "heading_open" and token.tag == "h2" and token.level == 0
    ]
