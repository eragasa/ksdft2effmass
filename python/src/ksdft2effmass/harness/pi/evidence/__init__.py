"""Explicit-input evidence identifier and Python conformance contracts.

The subpackage groups immutable evidence-domain records and fieldless actions.
It performs no repository discovery, filesystem access, pytest collection, or
scientific acceptance. Project-local wrappers own repository and command
integration.
"""

from .python_conformance import (
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
