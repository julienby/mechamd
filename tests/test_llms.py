from pathlib import Path

import pytest

from mechamd.cli import main
from mechamd.engine import Engine
from mechamd.llms import generate

from .conftest import FIXTURES

ROOT = Path(__file__).parent.parent


def test_llms_txt_is_fresh(tmp_path: Path) -> None:
    # Si ce test échoue : `uv run mecha llms > llms.txt`.
    assert generate(Engine(project=tmp_path)) == (ROOT / "llms.txt").read_text(encoding="utf-8")


def test_project_directives_first_and_headings_shifted() -> None:
    text = generate(Engine(project=FIXTURES / "project"))
    assert text.startswith("# mechamd\n")
    assert text.index("\n## empty\n") < text.index("\n## card\n")
    assert "\n### Syntaxe\n" in text  # `## Syntaxe` du README de card
    assert "\n### Capteur DS18B20\n" in text  # titre dans un bloc de code : inchangé
    assert "\n#### Capteur DS18B20\n" not in text


def test_mecha_llms(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["llms", "-p", str(FIXTURES / "project")]) == 0
    assert "\n## empty\n" in capsys.readouterr().out
