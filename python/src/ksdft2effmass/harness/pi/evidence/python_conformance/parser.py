"""Single-pass parser for explicit Python test-module bytes."""

from __future__ import annotations

import ast

from .model import PythonTestModuleModel


def parse_module(path: str, payload: bytes) -> PythonTestModuleModel:
    """Decode and parse one module exactly once.

    Parameters
    ----------
    path
        Caller-supplied diagnostic path and parser filename.
    payload
        Exact UTF-8 Python source bytes.

    Returns
    -------
    PythonTestModuleModel
        Immutable derived model shared by every rule owner.

    Raises
    ------
    UnicodeError
        If ``payload`` is not UTF-8.
    SyntaxError
        If the decoded source is not valid Python syntax.
    """
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=path)
    functions = tuple(
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )
    return PythonTestModuleModel(
        path,
        source,
        tree,
        ast.get_docstring(tree, clean=False),
        functions,
    )
