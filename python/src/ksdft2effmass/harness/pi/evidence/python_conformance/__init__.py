"""Explicit-input Python test-evidence conformance contracts.

The package preserves the established public records and validator while
separating the internal parsed model, parser, profile policy, and independent
rule owners.  Public execute signatures and import paths remain unchanged.
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

# Preserve the accepted defining-module identity after replacing the flat module
# with a cohesive internal package.
for _public in (
    PythonModuleSource,
    PythonConformanceRequest,
    PythonConformanceFinding,
    PythonConformanceResult,
    PythonConformanceValidator,
):
    _public.__module__ = __name__

del _public
