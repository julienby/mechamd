from pathlib import Path

import pytest

from mechamd import Engine

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def engine() -> Engine:
    return Engine(project=FIXTURES / "project")
