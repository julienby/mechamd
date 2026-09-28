"""Exécution des exemples d'une directive : `examples/x.md` contre `x.data.json`.

Chaque exemple contient un bloc de la directive. On compare ce que la directive
a compris (données de `parse` et variante retenue), jamais le HTML. La clé
`warnings` n'est comparée que si elle est présente dans le `.data.json`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mechamd.directive import Directive
from mechamd.engine import Engine


@dataclass
class ExampleResult:
    directive: str
    example: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def actual_for(engine: Engine, directive: Directive, example: Path) -> dict[str, Any] | None:
    """Ce que le moteur comprend du premier bloc de la directive dans l'exemple.

    La clé `html` contient le corps de page rendu (pour les vérifications du contrat).
    """
    page = engine.render_source(example.read_text(encoding="utf-8"), name=example.stem)
    for report in page.blocks:
        if report.name == directive.name:
            return {
                "variant": report.variant,
                "data": report.data,
                "warnings": report.warnings,
                "html": page.body,
            }
    return None


def run_example(engine: Engine, directive: Directive, example: Path) -> ExampleResult:
    result = ExampleResult(directive.name, example.stem)
    expected_file = example.with_suffix(".data.json")
    if not expected_file.is_file():
        result.errors.append(f"{expected_file.name} manquant")
        return result
    try:
        expected = json.loads(expected_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.errors.append(f"{expected_file.name} illisible : {exc}")
        return result
    actual = actual_for(engine, directive, example)
    if actual is None:
        result.errors.append(f"aucun bloc « {directive.name} » dans {example.name}")
        return result
    keys = ["variant", "data"] + (["warnings"] if "warnings" in expected else [])
    for key in keys:
        if expected.get(key) != actual[key]:
            result.errors.append(
                f"{key} : attendu {_dump(expected.get(key))}, obtenu {_dump(actual[key])}"
            )
    if f'data-mecha="{directive.name}"' not in actual["html"]:
        result.errors.append(f'le HTML rendu ne porte pas data-mecha="{directive.name}"')
    return result


def run_directive(engine: Engine, directive: Directive) -> list[ExampleResult]:
    examples = directive.examples()
    if not examples:
        return [ExampleResult(directive.name, "-", ["aucun exemple dans examples/"])]
    return [run_example(engine, directive, ex) for ex in examples]


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
