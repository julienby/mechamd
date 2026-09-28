import pytest

from mechamd.cli import main

from .conftest import FIXTURES


def test_mecha_test_green(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["test", "-p", str(FIXTURES / "project")]) == 0
    out = capsys.readouterr().out
    assert "✓ empty/nu" in out
    assert "✓ card/simple" in out  # directives fournies aussi
    assert "✗" not in out


def test_mecha_test_single_directive(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["test", "empty", "-p", str(FIXTURES / "project")]) == 0
    assert "1/1" in capsys.readouterr().out


def test_mecha_test_unknown_directive(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["test", "nope", "-p", str(FIXTURES / "project")]) == 1
    assert "introuvable" in capsys.readouterr().out


def test_mecha_test_reports_failures(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["test", "-p", str(FIXTURES / "broken")]) == 1
    out = capsys.readouterr().out
    assert "directive.py manquant" in out
    assert "a.data.json manquant" in out
    assert "illisible" in out
    assert "aucun exemple" in out
    assert "aucun bloc" in out
    assert 'variant : attendu "autre"' in out


def test_mecha_test_builtin_directives(
    capsys: pytest.CaptureFixture[str], tmp_path: object
) -> None:
    assert main(["test", "-p", str(tmp_path)]) == 0
    assert "✗" not in capsys.readouterr().out


def test_mecha_test_without_directives(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch, tmp_path: object
) -> None:
    monkeypatch.setattr("mechamd.engine.BUILTIN_DIR", FIXTURES / "nothing")
    assert main(["test", "-p", str(tmp_path)]) == 0
    assert "aucune directive" in capsys.readouterr().out
