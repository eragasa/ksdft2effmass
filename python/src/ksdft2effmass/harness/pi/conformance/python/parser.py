"""Exactly-once AST parser and neutral immutable-fact extractor."""

from __future__ import annotations

import ast
import hashlib
import re
from dataclasses import dataclass

from .model import (
    PythonCallableFact,
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


class _PythonModuleFactExtractor:
    """Extract legacy evidence facts through one explicit parser owner."""

    @staticmethod
    def _assigned_names(target: ast.expr) -> set[str]:
        if isinstance(target, ast.Name):
            return {target.id}
        if isinstance(target, (ast.List, ast.Tuple)):
            return {
                name
                for item in target.elts
                for name in _PythonModuleFactExtractor._assigned_names(item)
            }
        return set()

    @staticmethod
    def _module_statements(tree: ast.Module) -> tuple[ast.stmt, ...]:
        result: list[ast.stmt] = []

        def visit(node: ast.AST) -> None:
            for child in ast.iter_child_nodes(node):
                if isinstance(
                    child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    result.append(child)
                    continue
                if isinstance(child, ast.stmt):
                    result.append(child)
                visit(child)

        visit(tree)
        return tuple(result)

    @staticmethod
    def _assignments(
        tree: ast.Module, name: str
    ) -> tuple[ast.Assign | ast.AnnAssign, ...]:
        return tuple(
            statement
            for statement in tree.body
            if (
                isinstance(statement, ast.Assign)
                and any(
                    name in _PythonModuleFactExtractor._assigned_names(target)
                    for target in statement.targets
                )
            )
            or (
                isinstance(statement, ast.AnnAssign)
                and name in _PythonModuleFactExtractor._assigned_names(statement.target)
            )
        )

    @staticmethod
    def _named_mutations(
        tree: ast.Module, name: str, assignment: ast.Assign | ast.AnnAssign
    ) -> tuple[PythonParameterMutationFact, ...]:
        result: list[PythonParameterMutationFact] = []
        for statement in _PythonModuleFactExtractor._module_statements(tree):
            if statement is assignment:
                continue
            targets = (
                statement.targets
                if isinstance(statement, ast.Assign)
                else [statement.target]
                if isinstance(statement, (ast.AnnAssign, ast.AugAssign))
                else []
            )
            if any(
                name in _PythonModuleFactExtractor._assigned_names(target)
                for target in targets
            ):
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
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
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

    @staticmethod
    def _resolve_cases(tree: ast.Module, decorator: ast.Call) -> _ResolvedCases:
        values = decorator.args[1] if len(decorator.args) > 1 else None
        if isinstance(values, (ast.List, ast.Tuple)):
            return _ResolvedCases(
                PythonParameterInventoryKind.INLINE, None, tuple(values.elts), ()
            )
        if not isinstance(values, ast.Name):
            return _ResolvedCases(
                PythonParameterInventoryKind.NON_LITERAL, None, (), ()
            )
        name = values.id
        imported = {
            alias.asname or alias.name.split(".", 1)[0]
            for statement in _PythonModuleFactExtractor._module_statements(tree)
            if isinstance(statement, ast.Import)
            for alias in statement.names
        } | {
            alias.asname or alias.name
            for statement in _PythonModuleFactExtractor._module_statements(tree)
            if isinstance(statement, ast.ImportFrom)
            for alias in statement.names
        }
        if name in imported:
            return _ResolvedCases(PythonParameterInventoryKind.IMPORTED, name, (), ())
        assignments = _PythonModuleFactExtractor._assignments(tree, name)
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
            _PythonModuleFactExtractor._named_mutations(tree, name, assignment),
        )

    @staticmethod
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

    @staticmethod
    def _parameterization(
        tree: ast.Module, decorator: ast.Call
    ) -> PythonParameterizationFact:
        resolution = _PythonModuleFactExtractor._resolve_cases(tree, decorator)
        ids_node = next(
            (keyword.value for keyword in decorator.keywords if keyword.arg == "ids"),
            None,
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
            tuple(
                _PythonModuleFactExtractor._case_fact(item)
                for item in resolution.elements
            ),
            ids_present,
            ids_are_sequence,
            ids_are_literals,
            ids,
            resolution.mutations,
        )

    @staticmethod
    def _literal_strings(tree: ast.Module, name: str) -> tuple[str, ...] | None:
        assignments = _PythonModuleFactExtractor._assignments(tree, name)
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

    @staticmethod
    def _contains_export_surface(node: ast.AST) -> bool:
        """Return whether ``node`` references a package ``__all__`` surface."""
        return any(
            isinstance(child, ast.Attribute) and child.attr == "__all__"
            for child in ast.walk(node)
        )

    @staticmethod
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
                for name in _PythonModuleFactExtractor._value_names(value)
            }
        return {
            name
            for child in ast.iter_child_nodes(node)
            for name in _PythonModuleFactExtractor._value_names(child)
        }

    _LEXICAL_SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)

    @staticmethod
    def _scope_nodes(scope: ast.AST) -> tuple[ast.AST, ...]:
        """Return descendants owned by ``scope`` without entering nested scopes."""
        nodes: list[ast.AST] = []

        def visit(node: ast.AST) -> None:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, _PythonModuleFactExtractor._LEXICAL_SCOPES):
                    continue
                nodes.append(child)
                visit(child)

        visit(scope)
        return tuple(nodes)

    @staticmethod
    def _nested_scopes(scope: ast.AST) -> tuple[ast.AST, ...]:
        """Return directly nested lexical scopes in source traversal order."""
        nested: list[ast.AST] = []

        def visit(node: ast.AST) -> None:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, _PythonModuleFactExtractor._LEXICAL_SCOPES):
                    nested.append(child)
                else:
                    visit(child)

        visit(scope)
        return tuple(nested)

    @staticmethod
    def _represents_export(node: ast.AST, inventory_names: set[str]) -> bool:
        return _PythonModuleFactExtractor._contains_export_surface(node) or bool(
            _PythonModuleFactExtractor._value_names(node) & inventory_names
        )

    @staticmethod
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
                if value is not None and _PythonModuleFactExtractor._represents_export(
                    value, names
                ):
                    names.update(
                        name
                        for target in targets
                        for name in _PythonModuleFactExtractor._assigned_names(target)
                    )
            for node in nodes:
                if not isinstance(node, ast.Compare):
                    continue
                operands = (node.left, *node.comparators)
                for left, right in zip(operands, operands[1:], strict=False):
                    if _PythonModuleFactExtractor._represents_export(left, names):
                        names.update(_PythonModuleFactExtractor._value_names(right))
                    if _PythonModuleFactExtractor._represents_export(right, names):
                        names.update(_PythonModuleFactExtractor._value_names(left))
            changed = len(names) != prior
        return names

    @staticmethod
    def _is_export_length(node: ast.AST, inventory_names: set[str]) -> bool:
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "len"
            and len(node.args) == 1
            and not node.keywords
        ):
            return False
        return _PythonModuleFactExtractor._represents_export(
            node.args[0], inventory_names
        )

    @staticmethod
    def _numeric_export_count_assertion_lines(tree: ast.Module) -> tuple[int, ...]:
        """Return numeric export assertions with lexical alias propagation."""
        lines: set[int] = set()

        def visit(scope: ast.AST, inherited_names: set[str]) -> None:
            nodes = _PythonModuleFactExtractor._scope_nodes(scope)
            inventory_names = _PythonModuleFactExtractor._export_inventory_names(
                nodes, inherited_names
            )
            lines.update(
                node.lineno
                for node in nodes
                if isinstance(node, ast.Assert)
                and any(
                    _PythonModuleFactExtractor._is_export_length(child, inventory_names)
                    for child in ast.walk(node.test)
                )
            )
            for nested in _PythonModuleFactExtractor._nested_scopes(scope):
                visit(nested, inventory_names)

        visit(tree, set())
        return tuple(sorted(lines))


class _PythonStrictSyntaxFactExtractor:
    """Extract strict-typing and callable-placement facts from one parsed module."""

    __slots__ = ()
    _ERASED_CONTAINERS = frozenset(
        {
            "dict",
            "frozenset",
            "list",
            "set",
            "tuple",
            "builtins.dict",
            "builtins.frozenset",
            "builtins.list",
            "builtins.set",
            "builtins.tuple",
            "typing.AbstractSet",
            "typing.Callable",
            "typing.Collection",
            "typing.Container",
            "typing.Dict",
            "typing.FrozenSet",
            "typing.Iterable",
            "typing.Iterator",
            "typing.List",
            "typing.Mapping",
            "typing.MutableMapping",
            "typing.MutableSequence",
            "typing.MutableSet",
            "typing.Sequence",
            "typing.Set",
            "typing.Tuple",
            "collections.abc.Callable",
            "collections.abc.Collection",
            "collections.abc.Container",
            "collections.abc.Iterable",
            "collections.abc.Iterator",
            "collections.abc.Mapping",
            "collections.abc.MutableMapping",
            "collections.abc.MutableSequence",
            "collections.abc.MutableSet",
            "collections.abc.Sequence",
            "collections.abc.Set",
        }
    )
    _TWO_ARGUMENT_CONTAINERS = frozenset(
        {
            "dict",
            "builtins.dict",
            "typing.Dict",
            "typing.Mapping",
            "typing.MutableMapping",
            "collections.abc.Mapping",
            "collections.abc.MutableMapping",
        }
    )

    @staticmethod
    def _qualified_name(node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = _PythonStrictSyntaxFactExtractor._qualified_name(node.value)
            return None if base is None else f"{base}.{node.attr}"
        return None

    @staticmethod
    def _module_bound_names(tree: ast.Module) -> frozenset[str]:
        names: set[str] = set()
        for statement in tree.body:
            if isinstance(statement, ast.Assign):
                names.update(
                    name
                    for target in statement.targets
                    for name in _PythonModuleFactExtractor._assigned_names(target)
                )
            elif isinstance(statement, (ast.AnnAssign, ast.AugAssign)):
                names.update(
                    _PythonModuleFactExtractor._assigned_names(statement.target)
                )
            elif isinstance(
                statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                names.add(statement.name)
        return frozenset(names)

    @classmethod
    def _aliases(cls, tree: ast.Module) -> dict[str, str]:
        aliases: dict[str, str] = {}
        for statement in tree.body:
            if isinstance(statement, ast.Import):
                for alias in statement.names:
                    local_name = alias.asname or alias.name.split(".", 1)[0]
                    aliases[local_name] = alias.name if alias.asname else local_name
            elif isinstance(statement, ast.ImportFrom) and statement.module is not None:
                for alias in statement.names:
                    aliases[alias.asname or alias.name] = (
                        f"{statement.module}.{alias.name}"
                    )
        for name in cls._module_bound_names(tree):
            aliases[name] = ""
        return aliases

    @staticmethod
    def _resolved_name(name: str | None, aliases: dict[str, str]) -> str | None:
        if name is None:
            return None
        head, separator, tail = name.partition(".")
        if separator and head not in aliases:
            return None
        resolved = aliases.get(head, head)
        if resolved == "":
            return None
        return resolved if not separator else f"{resolved}.{tail}"

    @classmethod
    def _decorator_name(cls, decorator: ast.expr, aliases: dict[str, str]) -> str:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        return cls._resolved_name(cls._qualified_name(target), aliases) or ""

    @classmethod
    def _callables(
        cls, tree: ast.Module, aliases: dict[str, str]
    ) -> tuple[PythonCallableFact, ...]:
        facts: list[PythonCallableFact] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                facts.append(
                    PythonCallableFact(
                        node.name,
                        node.lineno,
                        None,
                        tuple(
                            cls._decorator_name(item, aliases)
                            for item in node.decorator_list
                        ),
                        ast.get_docstring(node, clean=False) is not None,
                    )
                )
            elif isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(
                node.value, ast.Lambda
            ):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    for name in sorted(
                        _PythonModuleFactExtractor._assigned_names(target)
                    ):
                        facts.append(
                            PythonCallableFact(
                                name,
                                node.lineno,
                                None,
                                (),
                                False,
                            )
                        )
            elif isinstance(node, ast.ClassDef):
                for member in node.body:
                    if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        facts.append(
                            PythonCallableFact(
                                member.name,
                                member.lineno,
                                node.name,
                                tuple(
                                    cls._decorator_name(item, aliases)
                                    for item in member.decorator_list
                                ),
                                ast.get_docstring(member, clean=False) is not None,
                            )
                        )
        return tuple(sorted(facts, key=lambda fact: (fact.line, fact.name)))

    @staticmethod
    def _parsed_annotation(
        annotation: ast.AST, line: int
    ) -> tuple[ast.AST, int] | None:
        if not (isinstance(annotation, ast.Constant) and type(annotation.value) is str):
            return annotation, line
        try:
            return ast.parse(annotation.value, mode="eval").body, line
        except SyntaxError:
            return None

    @staticmethod
    def _parsed_type_comment(
        text: str, line: int, *, function: bool
    ) -> tuple[ast.AST, int] | None:
        try:
            if function:
                return ast.parse(text, mode="func_type"), line
            return ast.parse(text, mode="eval").body, line
        except SyntaxError:
            return None

    @classmethod
    def _annotations(cls, tree: ast.Module) -> tuple[tuple[ast.AST, int], ...]:
        annotations: list[tuple[ast.AST, int]] = []
        for node in ast.walk(tree):
            value: tuple[ast.AST, int] | None = None
            if isinstance(node, ast.arg) and node.annotation is not None:
                value = cls._parsed_annotation(node.annotation, node.lineno)
            elif isinstance(node, ast.AnnAssign):
                value = cls._parsed_annotation(node.annotation, node.lineno)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns is not None:
                    value = cls._parsed_annotation(node.returns, node.lineno)
                if node.type_comment is not None:
                    comment = cls._parsed_type_comment(
                        node.type_comment, node.lineno, function=True
                    )
                    if comment is not None:
                        annotations.append(comment)
            elif isinstance(
                node, (ast.Assign, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)
            ):
                if node.type_comment is not None:
                    value = cls._parsed_type_comment(
                        node.type_comment, node.lineno, function=False
                    )
            if value is not None:
                annotations.append(value)
        return tuple(annotations)

    @classmethod
    def _contains_name(
        cls,
        annotation: ast.AST,
        aliases: dict[str, str],
        accepted: frozenset[str],
    ) -> bool:
        for node in ast.walk(annotation):
            if isinstance(node, (ast.Name, ast.Attribute)):
                name = cls._resolved_name(cls._qualified_name(node), aliases)
                if name in accepted:
                    return True
            elif isinstance(node, ast.Constant) and type(node.value) is str:
                parsed = cls._parsed_annotation(node, node.lineno)
                if (
                    parsed is not None
                    and not isinstance(parsed[0], ast.Constant)
                    and cls._contains_name(parsed[0], aliases, accepted)
                ):
                    return True
        return False

    @classmethod
    def _contains_erased_container(
        cls,
        annotation: ast.AST,
        aliases: dict[str, str],
        parameterized_target: bool = False,
    ) -> bool:
        if isinstance(annotation, ast.Constant) and type(annotation.value) is str:
            parsed = cls._parsed_annotation(annotation, annotation.lineno)
            return (
                parsed is not None
                and not isinstance(parsed[0], ast.Constant)
                and cls._contains_erased_container(
                    parsed[0], aliases, parameterized_target
                )
            )
        if isinstance(annotation, ast.Subscript):
            target = cls._resolved_name(cls._qualified_name(annotation.value), aliases)
            argument_count = (
                len(annotation.slice.elts)
                if isinstance(annotation.slice, ast.Tuple)
                else 1
            )
            if target in cls._TWO_ARGUMENT_CONTAINERS and argument_count != 2:
                return True
            return cls._contains_erased_container(
                annotation.value, aliases, True
            ) or cls._contains_erased_container(annotation.slice, aliases)
        if isinstance(annotation, (ast.Name, ast.Attribute)):
            name = cls._resolved_name(cls._qualified_name(annotation), aliases)
            return not parameterized_target and name in cls._ERASED_CONTAINERS
        return any(
            cls._contains_erased_container(child, aliases)
            for child in ast.iter_child_nodes(annotation)
        )

    @classmethod
    def _any_reference_lines(
        cls, tree: ast.Module, aliases: dict[str, str]
    ) -> tuple[int, ...]:
        lines = {
            node.lineno
            for node in ast.walk(tree)
            if isinstance(node, (ast.Name, ast.Attribute))
            and cls._resolved_name(cls._qualified_name(node), aliases) == "typing.Any"
        }
        lines.update(
            statement.lineno
            for statement in tree.body
            if isinstance(statement, ast.ImportFrom)
            and statement.module == "typing"
            and any(alias.name == "Any" for alias in statement.names)
        )
        lines.update(
            line
            for annotation, line in cls._annotations(tree)
            if cls._contains_name(annotation, aliases, frozenset({"typing.Any"}))
        )
        return tuple(sorted(lines))

    @classmethod
    def _cast_any_lines(
        cls, tree: ast.Module, aliases: dict[str, str]
    ) -> tuple[int, ...]:
        lines = {
            node.lineno
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and cls._resolved_name(cls._qualified_name(node.func), aliases)
            == "typing.cast"
            and bool(node.args)
            and cls._contains_name(node.args[0], aliases, frozenset({"typing.Any"}))
        }
        return tuple(sorted(lines))

    @classmethod
    def execute(
        cls, tree: ast.Module
    ) -> tuple[
        tuple[PythonCallableFact, ...],
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
    ]:
        """Return complete strict-policy facts without retaining the AST."""
        aliases = cls._aliases(tree)
        annotations = cls._annotations(tree)
        any_lines = cls._any_reference_lines(tree, aliases)
        object_names = (
            frozenset({"builtins.object"})
            if "object" in cls._module_bound_names(tree)
            else frozenset({"builtins.object", "object"})
        )
        object_lines = tuple(
            sorted(
                {
                    line
                    for annotation, line in annotations
                    if cls._contains_name(annotation, aliases, object_names)
                }
            )
        )
        erased_lines = tuple(
            sorted(
                {
                    line
                    for annotation, line in annotations
                    if cls._contains_erased_container(annotation, aliases)
                }
            )
        )
        return (
            cls._callables(tree, aliases),
            any_lines,
            cls._cast_any_lines(tree, aliases),
            object_lines,
            erased_lines,
        )


class PythonTestModuleParser:
    """Parse Python test evidence into immutable neutral facts."""

    __slots__ = ()

    @staticmethod
    def execute(path: str, payload: bytes) -> PythonTestModuleModel:
        """Decode and parse ``payload`` exactly once, then discard the AST."""
        source = payload.decode("utf-8")
        tree = ast.parse(source, filename=path, type_comments=True)
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
            lines = (module_doc or "").splitlines()
            first_line = lines[0].strip() if lines else ""
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
                    _PythonModuleFactExtractor._parameterization(tree, decorator)
                    for decorator in node.decorator_list
                    if isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Attribute)
                    and decorator.func.attr == "parametrize"
                ),
            )
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        (
            callables,
            any_reference_lines,
            cast_any_lines,
            object_annotation_lines,
            erased_container_annotation_lines,
        ) = _PythonStrictSyntaxFactExtractor.execute(tree)
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
            _PythonModuleFactExtractor._literal_strings(tree, "EQUALITY_FIELDS"),
            _PythonModuleFactExtractor._literal_strings(tree, "FROZEN_FIELDS"),
            _PythonModuleFactExtractor._numeric_export_count_assertion_lines(tree),
            callables,
            any_reference_lines,
            cast_any_lines,
            object_annotation_lines,
            erased_container_annotation_lines,
        )
