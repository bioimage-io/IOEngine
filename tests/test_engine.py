"""Tests for the bioengine api."""
from pathlib import Path

import pytest

from bioengine.engine import BioEngine

TEST_SCRIPT = """
from bioengine import api

def run():
    api.show_message('hello')

api.register(dict(type='service', name='test', run=run))
""".strip()

TEST_CLASS_SCRIPT = """
from bioengine import api

class TestClass:

    def __init__(self):
        self.type = "service"
        self.name = "test"

    def run(self):
        api.show_message("hello")

api.register(api=TestClass())
""".strip()


@pytest.mark.parametrize("test_script", [TEST_SCRIPT, TEST_CLASS_SCRIPT])
def test_register_api(test_script, capsys):
    """Test register an api."""
    engine = BioEngine()
    engine.execute(test_script)

    assert engine.services
    service = engine.services[0]
    assert service.type == "service"
    assert service.name == "test"

    service.run()

    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_load_package(capsys):
    """Test load a package to register an api."""
    fixture_dir = Path(__file__).parent.resolve() / "fixtures"
    package_dir = fixture_dir / "example_model"
    engine = BioEngine()
    engine.load_package(package_dir)

    assert engine.services
    service = engine.services[0]
    assert service.type == "service"
    assert service.name == "test"

    service.run()

    captured = capsys.readouterr()
    assert "hello" in captured.out
