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
    module_doc = ast.get_docstring(tree, clean=False)
    evidence_class = next(
        (
            part
            for part in path.split("/")
            if part
            in {
                "software_verification",
                "numerical_verification",
                "scientific_validation",
                "uncertainty_quantification",
            }
        ),
        "software_verification",
    )
    profile_match = __import__("re").search(
        r"(?m)^Evidence profile: (routine|claim_bearing)\s*$", module_doc or ""
    )
    evidence_profile = profile_match.group(1) if profile_match else "claim_bearing"
    sut_assignment = next(
        (
            statement
            for statement in tree.body
            if isinstance(statement, (ast.Assign, ast.AnnAssign))
            and any(
                isinstance(target, ast.Name) and target.id == "SUT"
                for target in (
                    statement.targets
                    if isinstance(statement, ast.Assign)
                    else [statement.target]
                )
            )
        ),
        None,
    )
    sut_value = sut_assignment.value if sut_assignment is not None else None
    if isinstance(sut_value, ast.Name) and not sut_value.id.startswith("_"):
        ownership_kind = "class_owned"
        owner_subject = sut_value.id
    else:
        ownership_kind = "artifact_owned"
        first_line = (module_doc or "").splitlines()[0].strip()
        prefix = {
            "software_verification": "Software verification of ",
            "numerical_verification": "Numerical verification of ",
            "scientific_validation": "Scientific validation of ",
            "uncertainty_quantification": "Uncertainty quantification of ",
        }.get(evidence_class, "")
        owner_subject = first_line.removeprefix(prefix).removesuffix(".")
    return PythonTestModuleModel(
        path,
        source,
        tree,
        module_doc,
        functions,
        evidence_class,
        evidence_profile,
        ownership_kind,
        owner_subject,
    )
