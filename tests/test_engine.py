"""Tests for the bioengine api."""
from bioengine.engine import BioEngine

TEST_SCRIPT = """
from bioengine import api

def run():
    api.showMessage('hello')

api.register(type='service', name='test', run=run)
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
