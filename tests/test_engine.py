"""Tests for the bioengine api."""
from bioengine.engine import BioEngine

TEST_SCRIPT = """
from bioengine import api

def run():
    api.showMessage('hello')

api.register(dict(type='service', name='test', run=run))
""".strip()

TEST_CLASS_SCRIPT = """
from bioengine import api

class TestClass:

    def __init__(self):
        self.type = "service"
        self.name = "test"

    def run(self):
        api.showMessage("hello")

api.register(api=TestClass())
""".strip()


def test_register_api(capsys):
    """Test register an api."""
    engine = BioEngine()
    engine.execute(TEST_SCRIPT)

    assert engine.services
    service = engine.services[0]
    assert service.type == "service"
    assert service.name == "test"

    service.run()

    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_register_instance(capsys):
    """Test register a class instance as api."""
    engine = BioEngine()
    engine.execute(TEST_CLASS_SCRIPT)

    assert engine.services
    service = engine.services[0]
    assert service.type == "service"
    assert service.name == "test"

    service.run()

    captured = capsys.readouterr()
    assert "hello" in captured.out
