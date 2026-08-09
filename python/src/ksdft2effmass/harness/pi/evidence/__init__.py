"""Explicit-input evidence identifier and Python conformance contracts.

The subpackage groups immutable evidence-domain records and fieldless actions.
It performs no repository discovery, filesystem access, pytest collection, or
scientific acceptance. Project-local wrappers own repository and command
integration.
"""

from .identifiers import IdentifierAuditor, IdentifierAuditResult, IdentifierOccurrence
from .python_conformance import (
    PythonConformanceFinding,
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)

__all__ = (
    "IdentifierOccurrence",
    "IdentifierAuditResult",
    "PythonModuleSource",
    "PythonConformanceRequest",
    "PythonConformanceFinding",
    "PythonConformanceResult",
    "IdentifierAuditor",
    "PythonConformanceValidator",
)
