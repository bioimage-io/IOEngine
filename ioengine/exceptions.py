"""Provide ioengine exceptions."""


class IOEngineException(Exception):
    """Represent the base IOEngine exception."""


class UnsupportedAPI(IOEngineException):
    """Represent an unsupported api exception."""

    def __init__(self):
        """Set up the exception."""
        super().__init__("Unsupported api export")
