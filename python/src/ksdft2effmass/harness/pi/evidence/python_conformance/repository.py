"""Independent repository-conformance projections over parsed module models."""

from __future__ import annotations

from .model import PythonTestModuleModel


def function_counts(model: PythonTestModuleModel) -> tuple[int, int]:
    """Return top-level test and helper counts without source reparsing."""
    tests = sum(function.startswith("test_") for function in model.function_names)
    return tests, len(model.function_names) - tests
