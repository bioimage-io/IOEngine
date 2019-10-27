"""Tests for the bioengine api."""
from bioengine.bioengine import BioEngine

TEST_SCRIPT = """
from bioimage import api

def run():
    api.showMessage('hello')

api.register(type='service', name='test', run=run)
""".strip()


def test_register_api(capsys):
    """Test register an api."""
    ioe = BioEngine()
    ioe.execute(TEST_SCRIPT)

    assert ioe.services
    service = ioe.services[0]
    assert service.type == "service"
    assert service.name == "test"

    service.run()

    captured = capsys.readouterr()
    assert "hello" in captured.out
