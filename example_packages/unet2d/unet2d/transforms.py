"""Provide transforms."""
import torch


class Sigmoid:
    """Represent a sigmoid."""

    def __call__(self, x, y=None):
        """Call sigmoid."""
        return torch.sigmoid(x), y


class NormalizeZeroMeanUnitVariance:
    """Represent a normalized zero mean unit variance."""

    def __init__(self, eps=1e-6):
        """Set up instance."""
        self.eps = eps

    def __call__(self, x, y=None):
        """Call transform."""
        return (x - x.mean()) / (x.std() + self.eps), y


def apply_transforms(transforms, x, y=None):
    """Apply transforms."""
    if not all(callable(trafo) for trafo in transforms):
        raise ValueError("Expect iterable with callables")
    for trafo in transforms:
        x, y = trafo(x, y)
    return x, y
