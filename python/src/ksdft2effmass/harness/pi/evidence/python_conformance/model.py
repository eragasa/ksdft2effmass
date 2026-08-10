"""Immutable parsed representation shared by Python evidence rule owners.

The model is an internal derived representation of caller-supplied bytes.  It
owns no filesystem access, evidence policy, persistence, or scientific claim.
The contained AST is created once by :mod:`parser` and treated as read-only by
all rule evaluators.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PythonTestModuleModel:
    """One successfully decoded and parsed Python test module.

    Attributes
    ----------
    path
        Caller-supplied diagnostic path.
    source
        Exact decoded UTF-8 source text.
    tree
        Single AST produced for ``source`` and shared without reparsing.
    module_doc
        Uncleaned module docstring, or ``None``.
    functions
        Top-level synchronous and asynchronous function definitions in source
        order.
    """

    path: str
    source: str
    tree: ast.Module
    module_doc: str | None
    functions: tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]
