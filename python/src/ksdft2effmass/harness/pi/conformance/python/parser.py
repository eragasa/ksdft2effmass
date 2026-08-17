"""Exactly-once AST parser and neutral immutable-fact extractor."""

from __future__ import annotations

import ast
import hashlib
import re
from dataclasses import dataclass

from .model import (
    PythonParameterCaseFact,
    PythonParameterInventoryKind,
    PythonParameterizationFact,
    PythonParameterMutationFact,
    PythonParameterMutationKind,
    PythonTestFunctionFact,
    PythonTestModuleModel,
)


@dataclass(frozen=True, slots=True)
class _ResolvedCases:
    kind: PythonParameterInventoryKind
    name: str | None
    elements: tuple[ast.expr, ...]
    mutations: tuple[PythonParameterMutationFact, ...]


def _assigned_names(target: ast.expr) -> set[str]:
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.List, ast.Tuple)):
        return {name for item in target.elts for name in _assigned_names(item)}
    return set()


def _module_statements(tree: ast.Module) -> tuple[ast.stmt, ...]:
    result: list[ast.stmt] = []

    def visit(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                result.append(child)
                continue
            if isinstance(child, ast.stmt):
                result.append(child)
            visit(child)

    visit(tree)
    return tuple(result)


def _assignments(tree: ast.Module, name: str) -> tuple[ast.Assign | ast.AnnAssign, ...]:
    return tuple(
        statement
        for statement in tree.body
        if (
            isinstance(statement, ast.Assign)
            and any(name in _assigned_names(target) for target in statement.targets)
        )
        or (
            isinstance(statement, ast.AnnAssign)
            and name in _assigned_names(statement.target)
        )
    )


def _named_mutations(
    tree: ast.Module, name: str, assignment: ast.Assign | ast.AnnAssign
) -> tuple[PythonParameterMutationFact, ...]:
    result: list[PythonParameterMutationFact] = []
    for statement in _module_statements(tree):
        if statement is assignment:
            continue
        targets = (
            statement.targets
            if isinstance(statement, ast.Assign)
            else [statement.target]
            if isinstance(statement, (ast.AnnAssign, ast.AugAssign))
            else []
        )
        if any(name in _assigned_names(target) for target in targets):
            kind = (
                PythonParameterMutationKind.AUGMENTED_ASSIGNMENT
                if isinstance(statement, ast.AugAssign)
                else PythonParameterMutationKind.REASSIGNMENT
            )
            result.append(PythonParameterMutationFact(kind))
    mutators = {"append", "clear", "extend", "insert", "reverse", "sort"}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == name
            and node.func.attr in mutators
        ):
            result.append(
                PythonParameterMutationFact(
                    PythonParameterMutationKind.METHOD_CALL, node.func.attr
                )
            )
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == name
                for target in targets
            ):
                result.append(
                    PythonParameterMutationFact(
                        PythonParameterMutationKind.SUBSCRIPT_ASSIGNMENT
                    )
                )
    return tuple(result)


def _resolve_cases(tree: ast.Module, decorator: ast.Call) -> _ResolvedCases:
    values = decorator.args[1] if len(decorator.args) > 1 else None
    if isinstance(values, (ast.List, ast.Tuple)):
        return _ResolvedCases(
            PythonParameterInventoryKind.INLINE, None, tuple(values.elts), ()
        )
    if not isinstance(values, ast.Name):
        return _ResolvedCases(PythonParameterInventoryKind.NON_LITERAL, None, (), ())
    name = values.id
    imported = {
        alias.asname or alias.name.split(".", 1)[0]
        for statement in _module_statements(tree)
        if isinstance(statement, ast.Import)
        for alias in statement.names
    } | {
        alias.asname or alias.name
        for statement in _module_statements(tree)
        if isinstance(statement, ast.ImportFrom)
        for alias in statement.names
    }
    if name in imported:
        return _ResolvedCases(PythonParameterInventoryKind.IMPORTED, name, (), ())
    assignments = _assignments(tree, name)
    if not assignments:
        return _ResolvedCases(PythonParameterInventoryKind.UNRESOLVED, name, (), ())
    if len(assignments) != 1:
        return _ResolvedCases(
            PythonParameterInventoryKind.MULTIPLE_ASSIGNMENTS, name, (), ()
        )
    assignment = assignments[0]
    targets = (
        assignment.targets
        if isinstance(assignment, ast.Assign)
        else [assignment.target]
    )
    if len(targets) != 1 or not isinstance(targets[0], ast.Name):
        return _ResolvedCases(
            PythonParameterInventoryKind.COMPLEX_ASSIGNMENT, name, (), ()
        )
    if assignment.lineno >= decorator.lineno:
        return _ResolvedCases(
            PythonParameterInventoryKind.ASSIGNED_AFTER_DECORATOR, name, (), ()
        )
    value = assignment.value
    if not isinstance(value, (ast.List, ast.Tuple)):
        return _ResolvedCases(
            PythonParameterInventoryKind.NON_LITERAL_ASSIGNMENT, name, (), ()
        )
    if any(isinstance(element, ast.Starred) for element in value.elts):
        return _ResolvedCases(
            PythonParameterInventoryKind.STARRED_EXPANSION, name, (), ()
        )
    return _ResolvedCases(
        PythonParameterInventoryKind.NAMED,
        name,
        tuple(value.elts),
        _named_mutations(tree, name, assignment),
    )


def _case_fact(item: ast.expr) -> PythonParameterCaseFact:
    is_param = (
        isinstance(item, ast.Call)
        and isinstance(item.func, ast.Attribute)
        and item.func.attr == "param"
    )
    direct = bool(
        is_param
        and isinstance(item, ast.Call)
        and isinstance(item.func, ast.Attribute)
        and isinstance(item.func.value, ast.Name)
        and item.func.value.id == "pytest"
    )
    id_values = (
        tuple(keyword.value for keyword in item.keywords if keyword.arg == "id")
        if isinstance(item, ast.Call)
        else ()
    )
    literal: str | None = None
    if len(id_values) == 1 and isinstance(id_values[0], ast.Constant):
        candidate = id_values[0].value
        if isinstance(candidate, str):
            literal = candidate
    return PythonParameterCaseFact(is_param, direct, len(id_values), literal)


def _parameterization(
    tree: ast.Module, decorator: ast.Call
) -> PythonParameterizationFact:
    resolution = _resolve_cases(tree, decorator)
    ids_node = next(
        (keyword.value for keyword in decorator.keywords if keyword.arg == "ids"), None
    )
    ids_present = ids_node is not None
    ids_are_sequence = isinstance(ids_node, (ast.List, ast.Tuple))
    ids_elements = (
        tuple(ids_node.elts) if isinstance(ids_node, (ast.List, ast.Tuple)) else ()
    )
    ids_are_literals = ids_are_sequence and all(
        isinstance(item, ast.Constant) and isinstance(item.value, str)
        for item in ids_elements
    )
    ids = (
        tuple(
            item.value
            for item in ids_elements
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        )
        if ids_are_literals
        else ()
    )
    return PythonParameterizationFact(
        resolution.kind,
        resolution.name,
        tuple(_case_fact(item) for item in resolution.elements),
        ids_present,
        ids_are_sequence,
        ids_are_literals,
        ids,
        resolution.mutations,
    )


def _literal_strings(tree: ast.Module, name: str) -> tuple[str, ...] | None:
    assignments = _assignments(tree, name)
    if len(assignments) != 1 or not isinstance(
        assignments[0].value, (ast.Tuple, ast.List)
    ):
        return None
    value = assignments[0].value
    strings = tuple(
        item.value
        for item in value.elts
        if isinstance(item, ast.Constant) and isinstance(item.value, str)
    )
    return (
        strings
        if len(strings) == len(value.elts)
        and all(strings)
        and len(strings) == len(set(strings))
        else None
    )


def _contains_export_surface(node: ast.AST) -> bool:
    """Return whether ``node`` references a package ``__all__`` surface."""
    return any(
        isinstance(child, ast.Attribute) and child.attr == "__all__"
        for child in ast.walk(node)
    )


def _value_names(node: ast.AST) -> set[str]:
    """Return value names while excluding names used only as call targets."""
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, ast.Attribute):
        return set()
    if isinstance(node, ast.Call):
        return {
            name
            for value in (*node.args, *(item.value for item in node.keywords))
            for name in _value_names(value)
        }
    return {
        name for child in ast.iter_child_nodes(node) for name in _value_names(child)
    }


_LEXICAL_SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def _scope_nodes(scope: ast.AST) -> tuple[ast.AST, ...]:
    """Return descendants owned by ``scope`` without entering nested scopes."""
    nodes: list[ast.AST] = []

    def visit(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, _LEXICAL_SCOPES):
                continue
            nodes.append(child)
            visit(child)

    visit(scope)
    return tuple(nodes)


def _nested_scopes(scope: ast.AST) -> tuple[ast.AST, ...]:
    """Return directly nested lexical scopes in source traversal order."""
    nested: list[ast.AST] = []

    def visit(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, _LEXICAL_SCOPES):
                nested.append(child)
            else:
                visit(child)

    visit(scope)
    return tuple(nested)


def _represents_export(node: ast.AST, inventory_names: set[str]) -> bool:
    return _contains_export_surface(node) or bool(_value_names(node) & inventory_names)


def _export_inventory_names(
    nodes: tuple[ast.AST, ...], inherited_names: set[str]
) -> set[str]:
    """Resolve direct, compared, and transitively assigned export inventories."""
    names = set(inherited_names)
    names.update(
        alias.asname or alias.name
        for node in nodes
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
        if alias.name == "__all__"
    )
    changed = True
    while changed:
        prior = len(names)
        for node in nodes:
            value: ast.expr | None
            targets: list[ast.expr]
            if isinstance(node, ast.Assign):
                value = node.value
                targets = node.targets
            elif isinstance(node, ast.AnnAssign):
                value = node.value
                targets = [node.target]
            else:
                continue
            if value is not None and _represents_export(value, names):
                names.update(
                    name for target in targets for name in _assigned_names(target)
                )
        for node in nodes:
            if not isinstance(node, ast.Compare):
                continue
            operands = (node.left, *node.comparators)
            for left, right in zip(operands, operands[1:], strict=False):
                if _represents_export(left, names):
                    names.update(_value_names(right))
                if _represents_export(right, names):
                    names.update(_value_names(left))
        changed = len(names) != prior
    return names


def _is_export_length(node: ast.AST, inventory_names: set[str]) -> bool:
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "len"
        and len(node.args) == 1
        and not node.keywords
    ):
        return False
    return _represents_export(node.args[0], inventory_names)


def _numeric_export_count_assertion_lines(tree: ast.Module) -> tuple[int, ...]:
    """Return numeric export assertions with lexical alias propagation."""
    lines: set[int] = set()

    def visit(scope: ast.AST, inherited_names: set[str]) -> None:
        nodes = _scope_nodes(scope)
        inventory_names = _export_inventory_names(nodes, inherited_names)
        lines.update(
            node.lineno
            for node in nodes
            if isinstance(node, ast.Assert)
            and any(
                _is_export_length(child, inventory_names)
                for child in ast.walk(node.test)
            )
        )
        for nested in _nested_scopes(scope):
            visit(nested, inventory_names)

    visit(tree, set())
    return tuple(sorted(lines))


def parse_module(path: str, payload: bytes) -> PythonTestModuleModel:
    """Decode and parse ``payload`` exactly once, then discard the AST."""
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=path)
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
    match = re.search(
        r"(?m)^Evidence profile: (routine|claim_bearing)\s*$", module_doc or ""
    )
    evidence_profile = match.group(1) if match else "claim_bearing"
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
    sut_name = sut_value.id if isinstance(sut_value, ast.Name) else None
    ownership_kind = (
        "class_owned"
        if sut_name is not None and not sut_name.startswith("_")
        else "artifact_owned"
    )
    if ownership_kind == "class_owned":
        owner_subject = sut_name or ""
    else:
        first_line = (module_doc or "").splitlines()[0].strip()
        prefix = {
            "software_verification": "Software verification of ",
            "numerical_verification": "Numerical verification of ",
            "scientific_validation": "Scientific validation of ",
            "uncertainty_quantification": "Uncertainty quantification of ",
        }.get(evidence_class, "")
        owner_subject = first_line.removeprefix(prefix).removesuffix(".")
    functions = tuple(
        PythonTestFunctionFact(
            node.name,
            node.lineno,
            ast.get_docstring(node, clean=False) or "",
            any(
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Name)
                and child.func.id == "SUT"
                for child in ast.walk(node)
            ),
            any(
                isinstance(child, ast.Subscript)
                and isinstance(child.value, ast.Name)
                and child.value.id == "SUT"
                for child in ast.walk(node)
            ),
            any(
                isinstance(child, ast.Subscript)
                and isinstance(child.value, ast.Attribute)
                and isinstance(child.value.value, ast.Name)
                and child.value.value.id == "SUT"
                and child.value.attr == "__members__"
                for child in ast.walk(node)
            ),
            any(
                isinstance(child, (ast.For, ast.AsyncFor, ast.While))
                for child in ast.walk(node)
            ),
            tuple(
                _parameterization(tree, decorator)
                for decorator in node.decorator_list
                if isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "parametrize"
            ),
        )
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )
    imported_names = tuple(
        sorted(
            alias.asname or alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        )
    )
    return PythonTestModuleModel(
        path,
        source,
        payload,
        hashlib.sha256(payload).hexdigest(),
        len(payload),
        module_doc,
        functions,
        evidence_class,
        evidence_profile,
        ownership_kind,
        owner_subject,
        sut_name,
        imported_names,
        _literal_strings(tree, "EQUALITY_FIELDS"),
        _literal_strings(tree, "FROZEN_FIELDS"),
        _numeric_export_count_assertion_lines(tree),
    )
