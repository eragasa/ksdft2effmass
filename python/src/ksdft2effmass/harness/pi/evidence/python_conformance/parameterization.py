"""Independent static parameterization inventory projection."""

from __future__ import annotations

import ast

from .model import PythonTestModuleModel, _module_syntax


def parameterized_functions(
    model: PythonTestModuleModel,
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return functions with at least one static ``parametrize`` decorator."""
    _tree, functions = _module_syntax(model)
    return tuple(
        function
        for function in functions
        if any(
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "parametrize"
            for decorator in function.decorator_list
        )
    )
