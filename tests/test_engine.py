from pathlib import Path

import pytest

from mechamd import Engine
from mechamd.engine import split_frontmatter

from .conftest import FIXTURES


def test_plain_markdown(engine: Engine) -> None:
    page = engine.render_source("# Titre\n\nDu *texte*.\n")
    assert page.title == "Titre"
    assert "<em>texte</em>" in page.body
    assert page.blocks == []
    assert "<title>Titre</title>" in page.html


def test_raw_html_disabled(engine: Engine) -> None:
    page = engine.render_source("<script>alert(1)</script>\n")
    assert "<script>" not in page.body


def test_frontmatter_title_and_line_numbers(engine: Engine) -> None:
    text = "---\ntitle: Suivi B204\ntags: [a]\n---\n\n:::probe\n:::\n"
    page = engine.render_source(text)
    assert page.title == "Suivi B204"
    assert page.meta["tags"] == ["a"]
    assert page.blocks[0].line == 6
    assert page.warnings == ["ligne 6 (probe) : bloc vide"]


def test_bad_frontmatter_is_ignored() -> None:
    meta, body, offset, warnings = split_frontmatter("---\n: [\n---\nx\n")
    assert meta == {} and warnings and offset == 0
    meta, body, offset, warnings = split_frontmatter("---\n- a\n---\nx\n")
    assert meta == {} and body == "\nx\n" and offset == 2


def test_resolution_order(engine: Engine) -> None:
    text = """
::::probe{probe=alt}
:::probe
fils
:::

:::probe{.default}
explicite
:::
::::

:::probe
alt deviné
:::

:::probe{.nope}
alt retombe
:::
"""
    blocks = engine.analyze(text)
    summary = [(b.variant, b.reason) for b in blocks]
    assert summary == [
        ("alt", "fixée par le parent"),
        ("default", "écrite sur le bloc"),
        ("default", "par défaut"),
        ("alt", "devinée"),
        ("alt", "devinée"),
    ]
    assert "inexistante" in blocks[4].warnings[0]


def test_parent_variant_that_does_not_exist(engine: Engine) -> None:
    blocks = engine.analyze("::::probe{probe=zzz}\n:::probe\nfils\n:::\n::::\n")
    assert blocks[0].variant == "default"
    assert "fixée par le parent" in blocks[0].warnings[0]


def test_children_are_rendered_before_parent(engine: Engine) -> None:
    page = engine.render_source("::::probe\n:::probe{#fils}\nfils\n:::\n::::\n")
    parent = page.blocks[-1]
    assert parent.data["children"][0].startswith('<div data-mecha="probe" data-variant="default"')
    assert 'id="fils"' in page.body


def test_unknown_directive_is_displayed(engine: Engine) -> None:
    page = engine.render_source(":::mystere{.x}\nTexte **gardé**.\n:::\n")
    assert "<strong>gardé</strong>" in page.body
    assert 'data-mecha="mystere"' in page.body
    assert page.blocks[0].known is False
    assert "directive inconnue" in page.warnings[0]


@pytest.mark.parametrize(
    ("opening", "message"),
    [
        (":::probe{boom=1}", "erreur dans parse : boum"),
        (":::probe{notdict=1}", "parse doit rendre un dict"),
        (":::probe{.fails}", "erreur dans le template fails.html"),
        (":::probe{guess=crash}", "erreur dans infer_variant"),
    ],
)
def test_errors_never_break_the_page(engine: Engine, opening: str, message: str) -> None:
    page = engine.render_source(f"Avant.\n\n{opening}\ncontenu\n:::\n\nAprès.\n")
    assert "Avant." in page.body and "Après." in page.body
    assert "contenu" in page.body
    assert any(message in w for w in page.warnings)


def test_duplicate_id_warns(engine: Engine) -> None:
    page = engine.render_source(":::probe{#a}\nx\n:::\n\n:::probe{#a}\ny\n:::\n")
    assert any("déjà utilisé" in w for w in page.warnings)


def test_directive_inside_code_fence_is_not_a_block(engine: Engine) -> None:
    page = engine.render_source("```\n:::probe\nx\n:::\n```\n")
    assert page.blocks == []
    assert ":::probe" in page.body


def test_md_helper_renders_nested_directives_without_double_report(engine: Engine) -> None:
    page = engine.render_source("::::empty\n:::probe\nx\n:::\n::::\n")
    assert [b.name for b in page.blocks] == ["probe", "empty"]
    assert page.body.count('data-mecha="probe"') == 1


def test_render_file_is_confined_to_project(tmp_path: Path) -> None:
    (tmp_path / "doc.md").write_text("# Doc\n", encoding="utf-8")
    engine = Engine(project=tmp_path)
    assert "<h1>Doc</h1>" in engine.render("doc.md")
    assert engine.render_page("doc.md").title == "Doc"
    with pytest.raises(ValueError):
        engine.render("../outside.md")


def test_title_falls_back_to_file_name(tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text("texte\n", encoding="utf-8")
    assert Engine(project=tmp_path).render_page("notes.md").title == "notes"


def test_project_directives_override_builtin_and_load_errors() -> None:
    engine = Engine(project=FIXTURES / "broken")
    assert "_ignored" not in engine.directives
    assert len(engine.load_errors) == 4


def test_block_md_without_engine() -> None:
    from mechamd import Block

    assert Block(name="x").md("*a*") == "<p><em>a</em></p>\n"
