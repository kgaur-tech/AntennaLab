"""Domain exceptions for engineering input and model failures."""

from __future__ import annotations


class EngineeringError(ValueError):
    """Base class for user-correctable engineering problems."""


class InvalidEngineeringParameter(EngineeringError):
    """Raised when an engineering input is missing, malformed, or non-physical."""


class UnsupportedFrequencyRange(EngineeringError):
    """Raised when a model cannot support the requested frequency."""


class InvalidGeometry(EngineeringError):
    """Raised when generated geometry is incomplete or non-physical."""


class ModelOutsideValidityRange(EngineeringError):
    """Raised when inputs are outside a model's declared validity envelope."""


class UnsupportedAnalysis(EngineeringError):
    """Raised when an analysis is requested that the model does not implement."""
