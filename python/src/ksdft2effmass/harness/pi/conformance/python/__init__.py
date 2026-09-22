"""Explicit-input Python test-evidence conformance contracts.

The package owns the established public records and validator while separating the
internal parsed model, parser, profile policy, and independent rule owners. Public
execute signatures remain unchanged.
"""

from .validation import (
    PythonConformanceFinding,
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)

__all__ = (
    "PythonModuleSource",
    "PythonConformanceRequest",
    "PythonConformanceFinding",
    "PythonConformanceResult",
    "PythonConformanceValidator",
)

# Bind the public records and action to this owning package rather than the private
# validation module.
for _public in (
    PythonModuleSource,
    PythonConformanceRequest,
    PythonConformanceFinding,
    PythonConformanceResult,
    PythonConformanceValidator,
):
    _public.__module__ = __name__

del _public
