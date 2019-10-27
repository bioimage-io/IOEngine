"""Provide bioengine exceptions."""


class BioEngineException(Exception):
    """Represent the base BioEngine exception."""


class PackageNotFound(BioEngineException):
    """Represent an unsupported api exception."""

    def __init__(self, package_id):
        """Set up the exception."""
        super().__init__(f"Package {package_id} not found")


class UnsupportedAPI(BioEngineException):
    """Represent an unsupported api exception."""

    def __init__(self):
        """Set up the exception."""
        super().__init__("Unsupported api export")
