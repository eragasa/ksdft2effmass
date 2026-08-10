"""Independent static parameterization inventory projection."""

from __future__ import annotations

import ast

from .model import PythonTestModuleModel


def parameterized_functions(
    model: PythonTestModuleModel,
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return functions with at least one static ``parametrize`` decorator."""
    return tuple(
        function
        for function in model.functions
        if any(
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "parametrize"
            for decorator in function.decorator_list
        )
    )
