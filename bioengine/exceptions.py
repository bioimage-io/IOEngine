"""Provide bioengine exceptions."""


class BioEngineException(Exception):
    """Represent the base BioEngine exception."""


class UnsupportedAPI(BioEngineException):
    """Represent an unsupported api exception."""

    def __init__(self):
        """Set up the exception."""
        super().__init__("Unsupported api export")
