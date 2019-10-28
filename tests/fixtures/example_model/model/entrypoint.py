"""Test entrypoint for package."""
from bioengine import api  # pylint: disable=no-name-in-module


def run():
    """Show a message."""
    api.show_message("hello")


api.register(dict(type="service", name="test", run=run))
