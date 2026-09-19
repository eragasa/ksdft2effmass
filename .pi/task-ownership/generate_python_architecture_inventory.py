"""Generate the bounded maintained-Python architecture inventory.

The generator is a deterministic, standard-library-only ActionObject. It receives
explicit repository, source, test, documentation, Task, and output paths. It records
syntax and repository evidence without deciding public compatibility, architecture,
or scientific meaning.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | tuple[JsonValue, ...] | dict[str, JsonValue]
type JsonRecord = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class InventoryCommandArguments:
    """Explicit filesystem inputs for one inventory generation."""

    repository_root: Path
    source_root: Path
    test_root: Path
    documentation_root: Path
    task_root: Path
    output: Path

    @classmethod
    def parse(cls, arguments: tuple[str, ...]) -> InventoryCommandArguments:
        """Parse exact required flag/value pairs without ambient path discovery."""
        expected = (
            "--repository-root",
            "--source-root",
            "--test-root",
            "--documentation-root",
            "--task-root",
            "--output",
        )
        if len(arguments) != len(expected) * 2:
            raise ValueError(
                "expected exactly six flag/value pairs: " + " ".join(expected)
            )
        values: dict[str, Path] = {}
        for index in range(0, len(arguments), 2):
            flag = arguments[index]
            if flag not in expected or flag in values:
                raise ValueError(f"unexpected or repeated argument: {flag}")
            values[flag] = Path(arguments[index + 1]).resolve()
        missing = [flag for flag in expected if flag not in values]
        if missing:
            raise ValueError("missing arguments: " + ", ".join(missing))
        return cls(
            repository_root=values["--repository-root"],
            source_root=values["--source-root"],
            test_root=values["--test-root"],
            documentation_root=values["--documentation-root"],
            task_root=values["--task-root"],
            output=values["--output"],
        )


@dataclass(frozen=True, slots=True)
class ParsedPythonModule:
    """One parsed maintained source module and its exact bytes."""

    module: str
    path: Path
    tree: ast.Module
    is_package: bool
    data: bytes


@dataclass(frozen=True, slots=True)
class ConsumerImport:
    """One static import of the maintained package."""

    consumer: str
    line: int
    imported_module: str
    imported_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProposedRoute:
    """One exact compatibility-decision input for a review candidate."""

    candidate_id: str
    route: str
    route_kind: str
    defining_module: str
    defining_symbol: str
    imported_module: str
    imported_name: str | None
    task_ids: tuple[str, ...]
    api_evidence_paths: tuple[str, ...]
    wire_consequence: str
    pickle_consequence: str
    module_consequence: str


@dataclass(frozen=True, slots=True)
class AbstractionInventory:
    """Nominal abstraction definitions and explicit inheritance facts."""

    definitions: tuple[JsonRecord, ...]
    relationships: tuple[JsonRecord, ...]


@dataclass(frozen=True, slots=True)
class PrivateMethodCallInventory:
    """Resolved and unresolved private call-site facts."""

    cross_owner_calls: tuple[JsonRecord, ...]
    unresolved_calls: tuple[JsonRecord, ...]
    methodology: str


@dataclass(frozen=True, slots=True)
class PythonPrivateMethodCallInspector(ast.NodeVisitor):
    """Classify statically resolvable and unresolved private attribute calls."""

    module: str
    path: str
    local_classes: frozenset[str]
    imported_symbols: dict[str, str]
    typed_self_dependencies: dict[tuple[str, str], str]
    cross_owner_calls: list[JsonRecord]
    unresolved_calls: list[JsonRecord]
    class_stack: list[str]
    callable_stack: list[str]

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class while retaining its exact lexical owner."""
        self.class_stack.append(node.name)
        for child in node.body:
            self.visit(child)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit a synchronous callable with an exact caller name."""
        self.callable_stack.append(node.name)
        for child in node.body:
            self.visit(child)
        self.callable_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit an asynchronous callable with an exact caller name."""
        self.callable_stack.append(node.name)
        for child in node.body:
            self.visit(child)
        self.callable_stack.pop()

    def visit_Call(self, node: ast.Call) -> None:
        """Record one non-dunder private attribute call when class-owned."""
        function = node.func
        if (
            self.class_stack
            and self.callable_stack
            and isinstance(function, ast.Attribute)
            and function.attr.startswith("_")
            and not function.attr.startswith("__")
        ):
            receiver = function.value
            caller_class = self.class_stack[-1]
            caller_method = self.callable_stack[-1]
            resolved_owner: str | None = None
            if isinstance(receiver, ast.Name):
                if receiver.id in self.local_classes:
                    resolved_owner = f"{self.module}.{receiver.id}"
                elif receiver.id in self.imported_symbols:
                    resolved_owner = self.imported_symbols[receiver.id]
            elif isinstance(receiver, ast.Call) and isinstance(receiver.func, ast.Name):
                constructor = receiver.func.id
                if constructor in self.local_classes:
                    resolved_owner = f"{self.module}.{constructor}"
                elif constructor in self.imported_symbols:
                    resolved_owner = self.imported_symbols[constructor]
            elif (
                isinstance(receiver, ast.Attribute)
                and isinstance(receiver.value, ast.Name)
                and receiver.value.id == "self"
            ):
                resolved_owner = self.typed_self_dependencies.get(
                    (caller_class, receiver.attr)
                )
            owner_local = (
                isinstance(receiver, ast.Name) and receiver.id in {"self", "cls"}
            ) or (
                isinstance(receiver, ast.Call)
                and isinstance(receiver.func, ast.Name)
                and receiver.func.id == "super"
            )
            if resolved_owner is not None:
                current_owner = f"{self.module}.{caller_class}"
                if resolved_owner != current_owner:
                    self.cross_owner_calls.append(
                        {
                            "path": self.path,
                            "line": node.lineno,
                            "caller_class": caller_class,
                            "caller_method": caller_method,
                            "callee_owner": resolved_owner,
                            "callee_method": function.attr,
                            "receiver_expression": ast.unparse(receiver),
                            "classification": "statically_resolvable_cross_owner",
                        }
                    )
            elif not owner_local:
                self.cross_owner_calls.append(
                    {
                        "path": self.path,
                        "line": node.lineno,
                        "caller_class": caller_class,
                        "caller_method": caller_method,
                        "callee_owner": None,
                        "callee_method": function.attr,
                        "receiver_expression": ast.unparse(receiver),
                        "classification": "cross_owner_owner_unresolved",
                    }
                )
        self.generic_visit(node)


@dataclass(frozen=True, slots=True)
class PythonTypedWireDebtInspector:
    """Inventory erased annotations and cast-through-Any at selected wire owners."""

    repository_root: Path

    def execute(self, modules: tuple[ParsedPythonModule, ...]) -> list[JsonRecord]:
        """Return exact typed-wire debt facts in path and source order."""
        selected = {
            "ksdft2effmass.harness.authority",
            "ksdft2effmass.harness._contract",
        }
        facts: list[JsonRecord] = []
        for parsed in modules:
            if parsed.module not in selected:
                continue
            relative = parsed.path.relative_to(self.repository_root).as_posix()
            for node in ast.walk(parsed.tree):
                if (
                    isinstance(node, ast.ImportFrom)
                    and node.module == "typing"
                    and any(alias.name == "Any" for alias in node.names)
                ):
                    facts.append(
                        {
                            "path": relative,
                            "line": node.lineno,
                            "category": "typing_any_import",
                            "expression": "from typing import Any",
                        }
                    )
                if isinstance(node, ast.Call) and self._is_cast_through_any(node):
                    facts.append(
                        {
                            "path": relative,
                            "line": node.lineno,
                            "category": "cast_through_any",
                            "expression": ast.unparse(node),
                        }
                    )
                for annotation in self._annotations(node):
                    expression = ast.unparse(annotation)
                    names = {
                        child.id
                        for child in ast.walk(annotation)
                        if isinstance(child, ast.Name)
                    }
                    if "Any" in names:
                        facts.append(
                            {
                                "path": relative,
                                "line": annotation.lineno,
                                "category": "any_annotation",
                                "expression": expression,
                            }
                        )
                    if "object" in names:
                        facts.append(
                            {
                                "path": relative,
                                "line": annotation.lineno,
                                "category": "generic_object_annotation",
                                "expression": expression,
                            }
                        )
                    if self._is_erased_mapping(annotation, names):
                        facts.append(
                            {
                                "path": relative,
                                "line": annotation.lineno,
                                "category": "erased_mapping_annotation",
                                "expression": expression,
                            }
                        )
        return sorted(
            facts,
            key=lambda item: (
                str(item["path"]),
                int(str(item["line"])),
                str(item["category"]),
                str(item["expression"]),
            ),
        )

    @staticmethod
    def _is_cast_through_any(node: ast.Call) -> bool:
        return (
            isinstance(node.func, ast.Name)
            and node.func.id == "cast"
            and bool(node.args)
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == "Any"
        )

    @staticmethod
    def _annotations(node: ast.AST) -> tuple[ast.expr, ...]:
        annotation: ast.expr | None = None
        if isinstance(node, (ast.arg, ast.AnnAssign)):
            annotation = node.annotation
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            annotation = node.returns
        return () if annotation is None else (annotation,)

    @staticmethod
    def _is_erased_mapping(annotation: ast.expr, names: set[str]) -> bool:
        mapping_names = {"dict", "Dict", "Mapping", "MutableMapping"}
        outer = annotation
        if isinstance(outer, ast.Name) and outer.id in mapping_names:
            return True
        return bool(mapping_names & names) and bool({"Any", "object"} & names)


@dataclass(frozen=True, slots=True)
class PythonArchitectureInventoryGenerator:
    """Generate one deterministic architecture inventory from explicit inputs."""

    arguments: InventoryCommandArguments

    LONG_MODULE: int = 500
    LONG_CLASS: int = 300
    LONG_METHOD: int = 100

    def execute(self) -> None:
        """Generate canonical inventory JSON at the configured output path."""
        self._validate_paths()
        modules = self._parse_modules()
        module_names = frozenset(parsed.module for parsed in modules)
        package_names = frozenset(
            parsed.module for parsed in modules if parsed.is_package
        )
        inventory = self._inventory(modules, module_names, package_names)
        self.arguments.output.parent.mkdir(parents=True, exist_ok=True)
        self.arguments.output.write_text(
            json.dumps(inventory, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _validate_paths(self) -> None:
        repository_root = self.arguments.repository_root
        for path in (
            self.arguments.source_root,
            self.arguments.test_root,
            self.arguments.documentation_root,
            self.arguments.task_root,
        ):
            if not path.is_dir() or not path.is_relative_to(repository_root):
                raise ValueError(f"input root is missing or outside repository: {path}")
        output_text = str(self.arguments.output)
        output_is_allowed = self.arguments.output.is_relative_to(
            repository_root
        ) or output_text.startswith(("/private/", "/tmp/"))
        # Completion validation uses an isolated operating-system temporary path.
        if not output_is_allowed:
            raise ValueError("output must be repository-confined or temporary")

    def _parse_modules(self) -> tuple[ParsedPythonModule, ...]:
        parsed: list[ParsedPythonModule] = []
        for path in sorted(self.arguments.source_root.rglob("*.py")):
            data = path.read_bytes()
            parsed.append(
                ParsedPythonModule(
                    module=self._module_name(path),
                    path=path,
                    tree=ast.parse(data, filename=str(path)),
                    is_package=path.name == "__init__.py",
                    data=data,
                )
            )
        return tuple(parsed)

    def _module_name(self, path: Path) -> str:
        relative = path.relative_to(self.arguments.source_root.parent).with_suffix("")
        parts = list(relative.parts)
        if parts[-1] == "__init__":
            parts.pop()
        return ".".join(parts)

    @staticmethod
    def _span(
        node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> int:
        line = int(node.lineno)
        end_line = int(getattr(node, "end_lineno", line))
        return end_line - line + 1

    @classmethod
    def _expression_name(cls, node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            prefix = cls._expression_name(node.value)
            return f"{prefix}.{node.attr}" if prefix else node.attr
        if isinstance(node, ast.Subscript):
            return cls._expression_name(node.value)
        return ast.unparse(node)

    @classmethod
    def _decorators(
        cls, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
    ) -> tuple[JsonValue, ...]:
        return tuple(cls._expression_name(item) for item in node.decorator_list)

    @staticmethod
    def _resolve_from(
        module: str, is_package: bool, imported_module: str | None, level: int
    ) -> str:
        package = module if is_package else module.rpartition(".")[0]
        if level == 0:
            return imported_module or ""
        relative = "." * level + (imported_module or "")
        return importlib.util.resolve_name(relative, package)

    @staticmethod
    def _declared_all(tree: ast.Module) -> list[str] | None:
        for node in tree.body:
            value: ast.expr | None = None
            if isinstance(node, ast.Assign):
                value = (
                    node.value
                    if any(
                        isinstance(target, ast.Name) and target.id == "__all__"
                        for target in node.targets
                    )
                    else None
                )
            elif isinstance(node, ast.AnnAssign):
                value = (
                    node.value
                    if isinstance(node.target, ast.Name) and node.target.id == "__all__"
                    else None
                )
            if isinstance(value, (ast.List, ast.Tuple)):
                names: list[str] = []
                for element in value.elts:
                    if not isinstance(element, ast.Constant) or not isinstance(
                        element.value, str
                    ):
                        return None
                    names.append(element.value)
                return names
            if value is not None:
                return None
        return None

    @staticmethod
    def _top_level_bindings(tree: ast.Module) -> list[str]:
        names: set[str] = set()
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                names.add(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    names.add(alias.asname or alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name != "*":
                        names.add(alias.asname or alias.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    if isinstance(target, ast.Name):
                        names.add(target.id)
        return sorted(names)

    @classmethod
    def _walk_classes(
        cls, nodes: list[ast.stmt], prefix: str = ""
    ) -> list[tuple[str, ast.ClassDef]]:
        classes: list[tuple[str, ast.ClassDef]] = []
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                qualified = f"{prefix}.{node.name}" if prefix else node.name
                classes.append((qualified, node))
                classes.extend(cls._walk_classes(node.body, qualified))
        return classes

    def _imported_symbol_aliases(self, parsed: ParsedPythonModule) -> dict[str, str]:
        aliases: dict[str, str] = {}
        for node in parsed.tree.body:
            if isinstance(node, ast.ImportFrom):
                try:
                    base = self._resolve_from(
                        parsed.module, parsed.is_package, node.module, node.level
                    )
                except ImportError, ValueError:
                    continue
                for alias in node.names:
                    if alias.name != "*":
                        aliases[alias.asname or alias.name] = f"{base}.{alias.name}"
        return aliases

    def _scan_imports(
        self, parsed: ParsedPythonModule, consumer: str
    ) -> list[ConsumerImport]:
        records: list[ConsumerImport] = []
        for node in ast.walk(parsed.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "ksdft2effmass" or alias.name.startswith(
                        "ksdft2effmass."
                    ):
                        records.append(
                            ConsumerImport(consumer, node.lineno, alias.name, ())
                        )
            elif isinstance(node, ast.ImportFrom):
                try:
                    target = self._resolve_from(
                        parsed.module, parsed.is_package, node.module, node.level
                    )
                except ImportError, ValueError:
                    continue
                if target == "ksdft2effmass" or target.startswith("ksdft2effmass."):
                    records.append(
                        ConsumerImport(
                            consumer,
                            node.lineno,
                            target,
                            tuple(sorted(alias.name for alias in node.names)),
                        )
                    )
        return records

    def _scan_test_imports(self) -> list[ConsumerImport]:
        records: list[ConsumerImport] = []
        for path in sorted(self.arguments.test_root.rglob("*.py")):
            tree = ast.parse(path.read_bytes(), filename=str(path))
            consumer = path.relative_to(self.arguments.repository_root).as_posix()
            parsed = ParsedPythonModule(consumer, path, tree, False, b"")
            records.extend(self._scan_imports(parsed, consumer))
        return records

    def _package_export_origins(
        self, parsed: ParsedPythonModule
    ) -> dict[str, tuple[str, str]]:
        origins: dict[str, tuple[str, str]] = {}
        for node in parsed.tree.body:
            if isinstance(node, ast.ImportFrom):
                try:
                    base = self._resolve_from(
                        parsed.module, True, node.module, node.level
                    )
                except ImportError, ValueError:
                    continue
                for alias in node.names:
                    bound = alias.asname or alias.name
                    origins[bound] = (base, alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    bound = alias.asname or alias.name.split(".")[0]
                    origins[bound] = (alias.name, alias.name.rpartition(".")[2])
            elif isinstance(
                node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                origins[node.name] = (parsed.module, node.name)
        return origins

    def _inventory(
        self,
        parsed_modules: tuple[ParsedPythonModule, ...],
        module_names: frozenset[str],
        package_names: frozenset[str],
    ) -> JsonRecord:
        modules: list[JsonRecord] = []
        top_callables: list[JsonRecord] = []
        private_classes: list[JsonRecord] = []
        private_methods: list[JsonRecord] = []
        long_modules: list[JsonRecord] = []
        long_classes: list[JsonRecord] = []
        long_methods: list[JsonRecord] = []
        exports: list[JsonRecord] = []
        export_routes: list[JsonRecord] = []
        identities: list[JsonRecord] = []
        edge_counts: Counter[tuple[str, str]] = Counter()
        source_imports: list[ConsumerImport] = []
        class_definitions: dict[str, JsonRecord] = {}
        module_aliases: dict[str, dict[str, str]] = {}
        dunder_method_count = 0
        aggregate_hasher = hashlib.sha256()

        for parsed in parsed_modules:
            relative = parsed.path.relative_to(
                self.arguments.repository_root
            ).as_posix()
            line_count = len(parsed.data.splitlines())
            digest = hashlib.sha256(parsed.data).hexdigest()
            identity: JsonRecord = {
                "module": parsed.module,
                "path": relative,
                "bytes": len(parsed.data),
                "lines": line_count,
                "sha256": digest,
            }
            identities.append(identity)
            aggregate_hasher.update(relative.encode())
            aggregate_hasher.update(b"\0")
            aggregate_hasher.update(digest.encode())
            aggregate_hasher.update(b"\n")

            direct_classes = [
                node for node in parsed.tree.body if isinstance(node, ast.ClassDef)
            ]
            direct_callables = [
                node
                for node in parsed.tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            all_classes = self._walk_classes(parsed.tree.body)
            aliases = self._imported_symbol_aliases(parsed)
            module_aliases[parsed.module] = aliases
            method_count = 0
            private_method_count = 0

            for class_name, class_node in all_classes:
                full_name = f"{parsed.module}.{class_name}"
                bases = tuple(self._expression_name(base) for base in class_node.bases)
                abstract_methods: list[str] = []
                class_record: JsonRecord = {
                    "module": parsed.module,
                    "symbol": class_name,
                    "path": relative,
                    "line": class_node.lineno,
                    "end_line": class_node.end_lineno,
                    "lines": self._span(class_node),
                    "bases": bases,
                    "decorators": self._decorators(class_node),
                }
                if self._span(class_node) >= self.LONG_CLASS:
                    long_classes.append(class_record)
                if (
                    "." not in class_name
                    and class_node.name.startswith("_")
                    and not class_node.name.startswith("__")
                ):
                    private_classes.append(class_record)
                for child in class_node.body:
                    if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    method_count += 1
                    decorators = self._decorators(child)
                    method: JsonRecord = {
                        "module": parsed.module,
                        "class": class_name,
                        "symbol": child.name,
                        "path": relative,
                        "line": child.lineno,
                        "end_line": child.end_lineno,
                        "lines": self._span(child),
                        "kind": (
                            "async"
                            if isinstance(child, ast.AsyncFunctionDef)
                            else "function"
                        ),
                        "decorators": decorators,
                    }
                    if any(
                        str(name).split(".")[-1] == "abstractmethod"
                        for name in decorators
                    ):
                        abstract_methods.append(child.name)
                    if child.name.startswith("__") and child.name.endswith("__"):
                        dunder_method_count += 1
                    elif child.name.startswith("_"):
                        private_methods.append(method)
                        private_method_count += 1
                    if self._span(child) >= self.LONG_METHOD:
                        long_methods.append(method)
                class_definitions[full_name] = {
                    "module": parsed.module,
                    "symbol": class_name,
                    "bases": bases,
                    "line": class_node.lineno,
                    "abstract_methods": tuple(sorted(abstract_methods)),
                }

            for node in direct_callables:
                top_callables.append(
                    {
                        "module": parsed.module,
                        "symbol": node.name,
                        "path": relative,
                        "line": node.lineno,
                        "end_line": node.end_lineno,
                        "lines": self._span(node),
                        "kind": (
                            "async"
                            if isinstance(node, ast.AsyncFunctionDef)
                            else "function"
                        ),
                        "underscore_prefixed": node.name.startswith("_"),
                        "decorators": self._decorators(node),
                    }
                )

            module_record: JsonRecord = {
                "module": parsed.module,
                "path": relative,
                "package": (
                    parsed.module
                    if parsed.is_package
                    else parsed.module.rpartition(".")[0]
                ),
                "is_package": parsed.is_package,
                "lines": line_count,
                "bytes": len(parsed.data),
                "top_level_classes": len(direct_classes),
                "all_classes_including_nested": len(all_classes),
                "top_level_callables": len(direct_callables),
                "methods": method_count,
                "single_underscore_private_methods": private_method_count,
            }
            modules.append(module_record)
            if line_count >= self.LONG_MODULE:
                long_modules.append(module_record)

            if parsed.is_package:
                declared = self._declared_all(parsed.tree)
                bindings = self._top_level_bindings(parsed.tree)
                effective = (
                    declared
                    if declared is not None
                    else [name for name in bindings if not name.startswith("_")]
                )
                origins = self._package_export_origins(parsed)
                exports.append(
                    {
                        "package": parsed.module,
                        "path": relative,
                        "declares_all": declared is not None,
                        "declared_all": (None if declared is None else tuple(declared)),
                        "declared_all_count": (
                            len(declared) if declared is not None else None
                        ),
                        "effective_star_exports": tuple(effective),
                    }
                )
                for name in effective:
                    origin_module, origin_symbol = origins.get(
                        name, (parsed.module, name)
                    )
                    export_routes.append(
                        {
                            "route": f"{parsed.module}.{name}",
                            "package": parsed.module,
                            "exported_name": name,
                            "defining_module": origin_module,
                            "defining_symbol": origin_symbol,
                            "evidence_status": "syntactic_export_only",
                        }
                    )

            source_imports.extend(self._scan_imports(parsed, parsed.module))
            self._collect_dependency_edges(parsed, module_names, edge_counts)

        test_imports = self._scan_test_imports()
        export_routes = self._enrich_export_routes(
            export_routes, source_imports, test_imports
        )
        consumer_inventory = self._consumer_inventory(
            source_imports, test_imports, package_names
        )
        package_metrics = self._package_metrics(modules, exports, package_names)
        edges: list[JsonRecord] = [
            {
                "from_module": source,
                "to_module": target,
                "import_statement_count": count,
            }
            for (source, target), count in sorted(edge_counts.items())
        ]
        cycles = self._cycles(module_names, edge_counts)
        abstractions = self._abstractions(class_definitions, module_aliases)
        private_calls = self._private_calls(parsed_modules)
        resolved_private_calls = tuple(
            item
            for item in private_calls.cross_owner_calls
            if item["classification"] == "statically_resolvable_cross_owner"
        )
        owner_unresolved_private_calls = tuple(
            item
            for item in private_calls.cross_owner_calls
            if item["classification"] == "cross_owner_owner_unresolved"
        )
        typed_debt = PythonTypedWireDebtInspector(
            self.arguments.repository_root
        ).execute(parsed_modules)
        route_matrix = self._route_matrix(source_imports, test_imports)
        managed_candidate_overlaps = self._managed_candidate_overlaps()

        summary: JsonRecord = {
            "module_count": len(modules),
            "package_count": len(package_names),
            "physical_lines": sum(int(str(item["lines"])) for item in modules),
            "source_bytes": sum(int(str(item["bytes"])) for item in modules),
            "top_level_class_count": sum(
                int(str(item["top_level_classes"])) for item in modules
            ),
            "all_class_count_including_nested": sum(
                int(str(item["all_classes_including_nested"])) for item in modules
            ),
            "top_level_callable_count": len(top_callables),
            "underscore_top_level_class_count": len(private_classes),
            "single_underscore_private_method_count": len(private_methods),
            "dunder_method_count": dunder_method_count,
            "long_module_count": len(long_modules),
            "long_class_count": len(long_classes),
            "long_method_count": len(long_methods),
            "package_export_name_count_sum": sum(
                len(item["effective_star_exports"])
                for item in exports
                if isinstance(item["effective_star_exports"], tuple)
            ),
            "static_internal_dependency_edge_count": len(edges),
            "static_internal_dependency_cycle_count": len(cycles),
            "protocol_count": sum(
                item["kind"] == "protocol" for item in abstractions.definitions
            ),
            "abstract_base_class_count": sum(
                item["kind"] == "abstract_base_class"
                for item in abstractions.definitions
            ),
            "deterministic_cross_owner_private_call_count": len(
                private_calls.cross_owner_calls
            ),
            "statically_resolvable_cross_owner_private_call_count": len(
                resolved_private_calls
            ),
            "cross_owner_owner_unresolved_call_count": len(
                owner_unresolved_private_calls
            ),
            "unresolved_private_receiver_call_count": len(
                private_calls.unresolved_calls
            ),
            "strict_typed_wire_debt_fact_count": len(typed_debt),
            "proposed_route_decision_input_count": len(route_matrix),
            "individual_export_route_decision_input_count": len(export_routes),
        }
        aggregate_digest = aggregate_hasher.hexdigest()
        return {
            "schema_version": 2,
            "inventory_id": f"sha256:{aggregate_digest}",
            "scope": {
                "repository_root": ".",
                "maintained_source_root": self._relative(self.arguments.source_root),
                "test_consumer_root": self._relative(self.arguments.test_root),
                "documentation_consumer_root": self._relative(
                    self.arguments.documentation_root
                ),
                "task_evidence_root": self._relative(self.arguments.task_root),
                "included_glob": "**/*.py",
                "excluded": (
                    "__pycache__/**",
                    "*.pyc",
                    "tests/docs/tasks from production metrics",
                ),
            },
            "methodology": self._methodology(),
            "policy_selection": {
                "verbatim_human_response": "recommendation authorized",
                "normalized_selection": "option_b",
                "supported_import_rule": (
                    "Curate deliberate package and subpackage export routes one by "
                    "one using accepted contract evidence and synchronized public "
                    "documentation; importability and __all__ alone are insufficient."
                ),
                "top_level_class_rule": (
                    "Use descriptive non-underscore implementation class names "
                    "without inferring supported API status unless deliberately "
                    "exported and accepted."
                ),
                "private_method_rule": (
                    "Permit owner-local private mechanical methods; prohibit "
                    "cross-object private calls and private ownership of public, "
                    "scientific, or numerical policy; do not mechanically rename "
                    "private methods."
                ),
                "route_classification_status": (
                    "unclassified_pending_bounded_option_b_application"
                ),
            },
            "summary": summary,
            "source_identities": {
                "aggregate_sha256": aggregate_digest,
                "files": tuple(identities),
            },
            "module_metrics": tuple(modules),
            "package_metrics": tuple(package_metrics),
            "top_level_callables": tuple(top_callables),
            "underscore_prefixed_top_level_classes": tuple(private_classes),
            "private_methods": tuple(private_methods),
            "long_owners": {
                "modules": tuple(long_modules),
                "classes": tuple(long_classes),
                "methods": tuple(long_methods),
            },
            "package_exports": tuple(exports),
            "export_routes": tuple(export_routes),
            "consumer_imports": tuple(consumer_inventory),
            "static_internal_dependencies": {
                "edges": tuple(edges),
                "cycles": tuple(tuple(component) for component in cycles),
            },
            "private_method_calls": {
                "methodology": private_calls.methodology,
                "deterministic_cross_owner_calls": private_calls.cross_owner_calls,
                "statically_resolvable_cross_owner_calls": resolved_private_calls,
                "cross_owner_owner_unresolved_calls": owner_unresolved_private_calls,
                "unresolved_dynamic_or_aliased_calls": private_calls.unresolved_calls,
            },
            "abstractions": {
                "definitions": abstractions.definitions,
                "explicit_inheritance_relationships": abstractions.relationships,
            },
            "strict_typed_wire_debt": {
                "scope": (
                    "ksdft2effmass.harness.authority",
                    "ksdft2effmass.harness._contract",
                ),
                "facts": tuple(typed_debt),
            },
            "proposed_route_matrix": tuple(route_matrix),
            "managed_candidate_overlaps": tuple(managed_candidate_overlaps),
        }

    def _relative(self, path: Path) -> str:
        return path.relative_to(self.arguments.repository_root).as_posix()

    def _collect_dependency_edges(
        self,
        parsed: ParsedPythonModule,
        module_names: frozenset[str],
        edge_counts: Counter[tuple[str, str]],
    ) -> None:
        for node in ast.walk(parsed.tree):
            targets: set[str] = set()
            if isinstance(node, ast.Import):
                targets.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                try:
                    base = self._resolve_from(
                        parsed.module, parsed.is_package, node.module, node.level
                    )
                except ImportError, ValueError:
                    continue
                # Exact dual-edge rule: a maintained facade is an edge, and every
                # imported name resolving to a maintained submodule is another edge.
                if base in module_names:
                    targets.add(base)
                for alias in node.names:
                    candidate = f"{base}.{alias.name}"
                    if candidate in module_names:
                        targets.add(candidate)
            for target in sorted(targets):
                if target in module_names and target != parsed.module:
                    edge_counts[(parsed.module, target)] += 1

    @staticmethod
    def _consumer_inventory(
        source_imports: list[ConsumerImport],
        test_imports: list[ConsumerImport],
        package_names: frozenset[str],
    ) -> list[JsonRecord]:
        groups: dict[str, tuple[set[str], set[str], set[str]]] = {}
        for domain, records in (("source", source_imports), ("test", test_imports)):
            for record in records:
                source, tests, names = groups.setdefault(
                    record.imported_module, (set(), set(), set())
                )
                if domain == "source":
                    source.add(record.consumer)
                else:
                    tests.add(record.consumer)
                names.update(record.imported_names)
        return [
            {
                "imported_module": imported,
                "source_consumer_count": len(group[0]),
                "source_consumers": tuple(sorted(group[0])),
                "test_consumer_count": len(group[1]),
                "test_consumers": tuple(sorted(group[1])),
                "imported_names": tuple(sorted(group[2])),
                "is_deep_module_import": imported not in package_names,
            }
            for imported, group in sorted(groups.items())
        ]

    def _enrich_export_routes(
        self,
        export_routes: list[JsonRecord],
        source_imports: list[ConsumerImport],
        test_imports: list[ConsumerImport],
    ) -> list[JsonRecord]:
        route_names = frozenset(str(item["route"]) for item in export_routes)
        documentation_index = self._exact_route_text_index(
            route_names, self.arguments.documentation_root, frozenset({".md", ".rst"})
        )
        accepted_task_index = self._accepted_task_support_index(route_names)
        enriched: list[JsonRecord] = []
        for item in export_routes:
            route = str(item["route"])
            package = str(item["package"])
            exported_name = str(item["exported_name"])
            documentation_evidence = documentation_index.get(route, [])
            accepted_task_evidence = accepted_task_index.get(route, [])
            accepted_documentation_evidence = [
                evidence
                for evidence in documentation_evidence
                if str(evidence["path"]).startswith("docs/api/")
                and bool(evidence["explicit_support_language"])
            ]
            accepted_support_evidence = [
                *accepted_task_evidence,
                *accepted_documentation_evidence,
            ]
            enriched.append(
                {
                    **item,
                    "maintained_source_consumers": tuple(
                        self._exact_export_consumers(
                            package, exported_name, source_imports
                        )
                    ),
                    "maintained_test_consumers": tuple(
                        self._exact_export_consumers(
                            package, exported_name, test_imports
                        )
                    ),
                    "exact_documentation_evidence": tuple(documentation_evidence),
                    "accepted_support_evidence": tuple(accepted_support_evidence),
                    "support_status": (
                        "accepted_support_evidence_found"
                        if accepted_support_evidence
                        else "unknown_no_exact_accepted_support_evidence"
                    ),
                    "compatibility_consequences": {
                        "wire": (
                            "Unknown from export syntax; inspect the defining "
                            "contract before changing this route."
                        ),
                        "pickle": (
                            "Changing the defining module may change pickle/global "
                            "lookup; no pickle contract is inferred."
                        ),
                        "module_identity": (
                            f"Current defining identity is {item['defining_module']}."
                        ),
                    },
                    "compatibility_disposition": (
                        "unclassified_pending_bounded_option_b_application"
                    ),
                    "evidence_caveat": (
                        "Absence of exact evidence means unknown, not unsupported. "
                        "Only exact qualified or same-line from-import forms count."
                    ),
                }
            )
        return enriched

    @staticmethod
    def _exact_export_consumers(
        package: str,
        exported_name: str,
        imports: list[ConsumerImport],
    ) -> list[JsonRecord]:
        return [
            {
                "consumer": item.consumer,
                "line": item.line,
            }
            for item in imports
            if item.imported_module == package and exported_name in item.imported_names
        ]

    def _exact_route_text_index(
        self,
        route_names: frozenset[str],
        root: Path,
        suffixes: frozenset[str],
    ) -> dict[str, list[JsonRecord]]:
        index: dict[str, list[JsonRecord]] = {}
        qualified_pattern = re.compile(r"ksdft2effmass(?:\.[A-Za-z_][A-Za-z0-9_]*)+")
        import_pattern = re.compile(
            r"\bfrom\s+(ksdft2effmass(?:\.[A-Za-z_][A-Za-z0-9_]*)*)"
            r"\s+import\s+([A-Za-z_][A-Za-z0-9_]*)"
        )
        for path in sorted(root.rglob("*")):
            if path.suffix not in suffixes or not path.is_file():
                continue
            relative = path.relative_to(self.arguments.repository_root).as_posix()
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                matched_routes = {
                    match.group(0)
                    for match in qualified_pattern.finditer(line)
                    if match.group(0) in route_names
                }
                for match in import_pattern.finditer(line):
                    candidate = f"{match.group(1)}.{match.group(2)}"
                    if candidate in route_names:
                        matched_routes.add(candidate)
                lowered = line.lower()
                explicit_support = "supported" in lowered and (
                    "import" in lowered or "public" in lowered
                )
                for route in sorted(matched_routes):
                    index.setdefault(route, []).append(
                        {
                            "path": relative,
                            "line": line_number,
                            "matched_route": route,
                            "explicit_support_language": explicit_support,
                        }
                    )
        return index

    def _accepted_task_support_index(
        self, route_names: frozenset[str]
    ) -> dict[str, list[JsonRecord]]:
        index: dict[str, list[JsonRecord]] = {}
        for path in sorted(self.arguments.task_root.glob("*.json")):
            task_text = path.read_text(encoding="utf-8")
            status = self._task_text_field(task_text, "status", path)
            if "human_accepted" not in status and status != "completed":
                continue
            task_id = self._task_text_field(task_text, "task_id", path)
            for line_number, line in enumerate(task_text.splitlines(), start=1):
                lowered = line.lower()
                if "supported" not in lowered or (
                    "import" not in lowered and "public" not in lowered
                ):
                    continue
                for route in sorted(route_names):
                    package, _, exported_name = route.rpartition(".")
                    exact_from = f"from {package} import {exported_name}"
                    if route not in line and exact_from not in line:
                        continue
                    index.setdefault(route, []).append(
                        {
                            "task_id": task_id,
                            "status": status,
                            "path": path.relative_to(
                                self.arguments.repository_root
                            ).as_posix(),
                            "line": line_number,
                            "matched_route": route,
                        }
                    )
        return index

    @staticmethod
    def _package_metrics(
        modules: list[JsonRecord],
        exports: list[JsonRecord],
        package_names: frozenset[str],
    ) -> list[JsonRecord]:
        records: list[JsonRecord] = []
        for package in sorted(package_names):
            members = [
                item
                for item in modules
                if isinstance(item, dict)
                and (
                    item["module"] == package
                    or str(item["module"]).startswith(package + ".")
                )
            ]
            direct = [
                item
                for item in members
                if item["module"] == package
                or str(item["module"]).rpartition(".")[0] == package
            ]
            export = next(
                item
                for item in exports
                if isinstance(item, dict) and item["package"] == package
            )
            effective = export["effective_star_exports"]
            records.append(
                {
                    "package": package,
                    "recursive_module_count": len(members),
                    "direct_module_count": len(direct),
                    "recursive_lines": sum(int(str(item["lines"])) for item in members),
                    "recursive_top_level_classes": sum(
                        int(str(item["top_level_classes"])) for item in members
                    ),
                    "recursive_top_level_callables": sum(
                        int(str(item["top_level_callables"])) for item in members
                    ),
                    "recursive_methods": sum(
                        int(str(item["methods"])) for item in members
                    ),
                    "declared_all_count": export["declared_all_count"],
                    "effective_star_export_count": (
                        len(effective) if isinstance(effective, list) else 0
                    ),
                }
            )
        return records

    @staticmethod
    def _cycles(
        module_names: frozenset[str],
        edge_counts: Counter[tuple[str, str]],
    ) -> list[list[str]]:
        adjacency: dict[str, list[str]] = {module: [] for module in module_names}
        reverse_adjacency: dict[str, list[str]] = {
            module: [] for module in module_names
        }
        for source, target in edge_counts:
            adjacency[source].append(target)
            reverse_adjacency[target].append(source)
        for source, targets in adjacency.items():
            adjacency[source] = sorted(set(targets))
            reverse_adjacency[source] = sorted(set(reverse_adjacency[source]))

        visited: set[str] = set()
        finish_order: list[str] = []
        for start in sorted(module_names):
            if start in visited:
                continue
            visited.add(start)
            traversal: list[tuple[str, int]] = [(start, 0)]
            while traversal:
                vertex, neighbor_index = traversal[-1]
                neighbors = adjacency[vertex]
                if neighbor_index < len(neighbors):
                    target = neighbors[neighbor_index]
                    traversal[-1] = (vertex, neighbor_index + 1)
                    if target not in visited:
                        visited.add(target)
                        traversal.append((target, 0))
                else:
                    traversal.pop()
                    finish_order.append(vertex)

        assigned: set[str] = set()
        components: list[list[str]] = []
        for start in reversed(finish_order):
            if start in assigned:
                continue
            assigned.add(start)
            component: list[str] = []
            traversal = [(start, 0)]
            while traversal:
                vertex, neighbor_index = traversal[-1]
                if neighbor_index == 0:
                    component.append(vertex)
                neighbors = reverse_adjacency[vertex]
                if neighbor_index < len(neighbors):
                    target = neighbors[neighbor_index]
                    traversal[-1] = (vertex, neighbor_index + 1)
                    if target not in assigned:
                        assigned.add(target)
                        traversal.append((target, 0))
                else:
                    traversal.pop()
            if len(component) > 1:
                components.append(sorted(component))
        return sorted(components, key=lambda component: (len(component), component))

    @staticmethod
    def _abstractions(
        class_definitions: dict[str, JsonRecord],
        module_aliases: dict[str, dict[str, str]],
    ) -> AbstractionInventory:
        definitions: list[JsonRecord] = []
        abstract_symbols: set[str] = set()
        for full_name, item in sorted(class_definitions.items()):
            bases_value = item["bases"]
            bases: tuple[JsonValue, ...] = (
                bases_value if isinstance(bases_value, tuple) else ()
            )
            tails = {str(base).split(".")[-1] for base in bases}
            abstract_methods = item["abstract_methods"]
            kind: str | None = None
            if "Protocol" in tails:
                kind = "protocol"
            elif "ABC" in tails or (
                isinstance(abstract_methods, tuple) and abstract_methods
            ):
                kind = "abstract_base_class"
            if kind is not None:
                abstract_symbols.add(full_name)
                definitions.append({"class": full_name, "kind": kind, **item})
        relationships: list[JsonRecord] = []
        for full_name, item in sorted(class_definitions.items()):
            module = str(item["module"])
            bases_value = item["bases"]
            bases = bases_value if isinstance(bases_value, tuple) else ()
            for base_value in bases:
                base = str(base_value)
                candidates = [f"{module}.{base}"]
                alias = module_aliases[module].get(base.split(".")[0])
                if alias is not None:
                    suffix = base.split(".", 1)[1] if "." in base else ""
                    candidates.append(f"{alias}.{suffix}" if suffix else alias)
                for candidate in candidates:
                    if candidate in abstract_symbols:
                        relationships.append(
                            {
                                "subclass": full_name,
                                "abstraction": candidate,
                                "relationship": "explicit_inheritance",
                            }
                        )
                        break
        return AbstractionInventory(tuple(definitions), tuple(relationships))

    def _private_calls(
        self, parsed_modules: tuple[ParsedPythonModule, ...]
    ) -> PrivateMethodCallInventory:
        cross_owner: list[JsonRecord] = []
        unresolved: list[JsonRecord] = []
        for parsed in parsed_modules:
            local_classes = frozenset(
                node.name for node in parsed.tree.body if isinstance(node, ast.ClassDef)
            )
            imported_symbols = self._imported_symbol_aliases(parsed)
            inspector = PythonPrivateMethodCallInspector(
                module=parsed.module,
                path=parsed.path.relative_to(self.arguments.repository_root).as_posix(),
                local_classes=local_classes,
                imported_symbols=imported_symbols,
                typed_self_dependencies=self._typed_self_dependencies(
                    parsed, local_classes, imported_symbols
                ),
                cross_owner_calls=cross_owner,
                unresolved_calls=unresolved,
                class_stack=[],
                callable_stack=[],
            )
            inspector.visit(parsed.tree)
        return PrivateMethodCallInventory(
            methodology=(
                "Cross-owner means a ClassName._method call whose ClassName resolves "
                "to a maintained local or explicitly imported class different from "
                "the lexical caller class. Direct constructor receivers and typed "
                "self dependencies are resolved. self/cls/super calls are owner-local "
                "and omitted. A proven non-self receiver with unknown exact owner is "
                "deterministic cross_owner_owner_unresolved debt."
            ),
            cross_owner_calls=tuple(
                sorted(cross_owner, key=self._private_call_sort_key)
            ),
            unresolved_calls=tuple(sorted(unresolved, key=self._private_call_sort_key)),
        )

    def _typed_self_dependencies(
        self,
        parsed: ParsedPythonModule,
        local_classes: frozenset[str],
        imported_symbols: dict[str, str],
    ) -> dict[tuple[str, str], str]:
        dependencies: dict[tuple[str, str], str] = {}
        for class_node in parsed.tree.body:
            if not isinstance(class_node, ast.ClassDef):
                continue
            for callable_node in class_node.body:
                if not isinstance(
                    callable_node, (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    continue
                parameter_owners: dict[str, str] = {}
                for parameter in (
                    *callable_node.args.posonlyargs,
                    *callable_node.args.args,
                    *callable_node.args.kwonlyargs,
                ):
                    if parameter.annotation is None:
                        continue
                    annotation = self._expression_name(parameter.annotation)
                    owner = self._resolved_class_owner(
                        annotation, parsed.module, local_classes, imported_symbols
                    )
                    if owner is not None:
                        parameter_owners[parameter.arg] = owner
                for node in ast.walk(callable_node):
                    if not isinstance(node, ast.Assign):
                        continue
                    if not isinstance(node.value, ast.Name):
                        continue
                    owner = parameter_owners.get(node.value.id)
                    if owner is None:
                        continue
                    for target in node.targets:
                        if (
                            isinstance(target, ast.Attribute)
                            and isinstance(target.value, ast.Name)
                            and target.value.id == "self"
                        ):
                            dependencies[(class_node.name, target.attr)] = owner
        return dependencies

    @staticmethod
    def _resolved_class_owner(
        annotation: str,
        module: str,
        local_classes: frozenset[str],
        imported_symbols: dict[str, str],
    ) -> str | None:
        if annotation in local_classes:
            return f"{module}.{annotation}"
        return imported_symbols.get(annotation)

    @staticmethod
    def _private_call_sort_key(item: JsonRecord) -> tuple[str, int]:
        return str(item["path"]), int(str(item["line"]))

    def _route_specs(self) -> tuple[ProposedRoute, ...]:
        workflows_tasks = (
            "migration.v2.workflows.persistence",
            "migration.v2.workflows.workflow-run",
        )
        qe_tasks = (
            "migration.v2.integration.quantumespresso",
            "migration.v2.calculators.quantum-espresso-contracts",
            "migration.v2.calculators.quantum-espresso-contracts.boundary-decision",
            "migration.v2.calculators.quantum-espresso-contracts.contract-verification",
            (
                "migration.v2.calculators.quantum-espresso-contracts.simulation-and-executor-bindings"
            ),
            "migration.v2.calculators.quantum-espresso-contracts.task-contracts",
            "quantumespresso.simulations.integration",
        )
        return (
            ProposedRoute(
                "C1",
                "ksdft2effmass.workflows.WorkflowRunSerializer",
                "package_reexport",
                "ksdft2effmass.workflows.persistence",
                "WorkflowRunSerializer",
                "ksdft2effmass.workflows",
                "WorkflowRunSerializer",
                workflows_tasks,
                (
                    "docs/api/workflows.rst",
                    "docs/concepts/workflow-run-persistence.rst",
                ),
                (
                    "Exact versioned WorkflowRun bytes and decode failures must "
                    "remain unchanged."
                ),
                (
                    "Moving the defining class changes pickle/global lookup unless "
                    "compatibility is supplied; no pickle contract is established "
                    "here."
                ),
                (
                    "Changing the defining module changes __module__; retaining the "
                    "facade alone does not preserve it."
                ),
            ),
            ProposedRoute(
                "C2",
                "ksdft2effmass.workflows.runs.replay._WorkflowRunStructureValidator",
                "private_deep_import",
                "ksdft2effmass.workflows.runs.replay",
                "_WorkflowRunStructureValidator",
                "ksdft2effmass.workflows.runs.replay",
                "_WorkflowRunStructureValidator",
                workflows_tasks,
                ("docs/architecture/v2/ksdft2effmass/workflows/persistence.md",),
                (
                    "Validation issue ordering and persistence/replay structural "
                    "outcomes are observable and must remain unchanged."
                ),
                (
                    "No pickle contract is established; moving the class would "
                    "still change global identity."
                ),
                (
                    "Architecture v2 fixes this private owner in runs/replay.py and "
                    "says there is no extra structural module."
                ),
            ),
            ProposedRoute(
                "C3",
                "ksdft2effmass.workflows.__all__",
                "package_export_set",
                "ksdft2effmass.workflows",
                "__all__",
                "ksdft2effmass.workflows",
                None,
                workflows_tasks,
                ("docs/api/workflows.rst",),
                (
                    "Individual exported serializers/results may own versioned wire "
                    "contracts."
                ),
                (
                    "Removing a reexport can break pickle lookup only where callers "
                    "serialized the facade-qualified object; no aggregate pickle "
                    "contract is inferred."
                ),
                (
                    "The current facade has 230 literal exports; each accepted "
                    "route needs separate disposition."
                ),
            ),
            ProposedRoute(
                "C3",
                "ksdft2effmass.harness.__all__",
                "package_export_set",
                "ksdft2effmass.harness",
                "__all__",
                "ksdft2effmass.harness",
                None,
                ("migration.v2.harness.decisions-authority",),
                ("docs/api/harness-adapters.rst",),
                (
                    "Harness serializers include accepted wire behavior that cannot "
                    "be inferred from the facade alone."
                ),
                (
                    "Facade removal can affect qualified lookup; no blanket pickle "
                    "contract is inferred."
                ),
                "The current facade has 135 literal exports.",
            ),
            ProposedRoute(
                "C3",
                "ksdft2effmass.integration.quantum_espresso.__all__",
                "package_export_set",
                "ksdft2effmass.integration.quantum_espresso",
                "__all__",
                "ksdft2effmass.integration.quantum_espresso",
                None,
                qe_tasks,
                (
                    (
                        "docs/architecture/v2/ksdft2effmass/integration/quantum_espresso/index.md"
                    ),
                ),
                (
                    "QE serializers and native result records include accepted wire "
                    "behavior."
                ),
                (
                    "Facade removal can affect qualified lookup; no blanket pickle "
                    "contract is inferred."
                ),
                "The current facade has 134 literal exports.",
            ),
            ProposedRoute(
                "C3",
                "ksdft2effmass.workflows.runs.__all__",
                "package_export_set",
                "ksdft2effmass.workflows.runs",
                "__all__",
                "ksdft2effmass.workflows.runs",
                None,
                workflows_tasks,
                ("docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md",),
                "Run records participate in WorkflowRun serialization.",
                (
                    "Moving defining records can change pickle/global identity; no "
                    "pickle contract is inferred."
                ),
                "The current runs facade has 116 literal exports.",
            ),
            *tuple(
                ProposedRoute(
                    "C4",
                    f"ksdft2effmass.integration.quantum_espresso.{symbol}",
                    "package_reexport",
                    "ksdft2effmass.integration.quantum_espresso.effects",
                    symbol,
                    "ksdft2effmass.integration.quantum_espresso",
                    symbol,
                    qe_tasks,
                    (
                        (
                            "docs/architecture/v2/ksdft2effmass/calculators/quantum-espresso-local-execution-contract.md"
                        ),
                    ),
                    (
                        "Artifact/snapshot/terminal representations and serializer "
                        "bytes must remain unchanged where defined."
                    ),
                    (
                        "A defining-module move changes pickle/global identity "
                        "unless explicitly preserved; no pickle contract is "
                        "inferred."
                    ),
                    (
                        "A module split changes __module__ even if the QE facade "
                        "route remains."
                    ),
                )
                for symbol in (
                    "QuantumEspressoInputStager",
                    "QuantumEspressoWorkspaceSnapshotter",
                    "QuantumEspressoNativeOutputCollector",
                    "QuantumEspressoTerminalRecordPublisher",
                )
            ),
            ProposedRoute(
                "C5",
                "ksdft2effmass.harness.DevelopmentAuthorityContextResolver",
                "package_reexport",
                "ksdft2effmass.harness.authority",
                "DevelopmentAuthorityContextResolver",
                "ksdft2effmass.harness",
                "DevelopmentAuthorityContextResolver",
                ("migration.v2.harness.decisions-authority",),
                (
                    (
                        "docs/architecture/migration/v1-to-v2/implementation/harness/decisions-authority.md"
                    ),
                ),
                (
                    "Accepted authority wire fields and exact response behavior "
                    "must be preserved."
                ),
                (
                    "A defining-module move changes pickle/global identity unless "
                    "explicitly preserved; no pickle contract is inferred."
                ),
                (
                    "Typed boundary repair must preserve __module__ unless "
                    "separately accepted."
                ),
            ),
            ProposedRoute(
                "C6",
                "ksdft2effmass.harness.cli.run",
                "framework_entrypoint_reexport",
                "ksdft2effmass.harness.cli.main",
                "run",
                "ksdft2effmass.harness.cli",
                "run",
                ("python.architecture-refactor.architecture-conformance",),
                (),
                "No wire consequence identified.",
                "No pickle contract is established.",
                (
                    "Framework/package entrypoint identity must remain a minimal "
                    "typed adapter."
                ),
            ),
            ProposedRoute(
                "C7",
                (
                    "ksdft2effmass.campaigns._plane_wave_study -> "
                    "ksdft2effmass.petrinet.colored"
                ),
                "internal_dependency_edge",
                "ksdft2effmass.campaigns._plane_wave_study",
                "module import",
                "ksdft2effmass.petrinet.colored",
                None,
                ("migration.v2.calculators.plane-wave-study-contracts",),
                ("docs/architecture/v2/repository-layout.md",),
                (
                    "No direct wire consequence; changing the edge can change "
                    "constructed Workflow/Petri-net values."
                ),
                "No pickle contract is established.",
                (
                    "Dependency direction is an architecture surface, not a "
                    "supported import classification."
                ),
            ),
            ProposedRoute(
                "C8",
                "ksdft2effmass.workflows.runs.TaskAttempt",
                "package_reexport",
                "ksdft2effmass.workflows.runs.records",
                "TaskAttempt",
                "ksdft2effmass.workflows.runs",
                "TaskAttempt",
                workflows_tasks,
                ("docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md",),
                "TaskAttempt is embedded in serialized WorkflowRun history.",
                (
                    "Moving the defining record changes pickle/global identity "
                    "unless explicitly preserved; no pickle contract is inferred."
                ),
                (
                    "A records-family split changes __module__ even if the runs "
                    "facade remains."
                ),
            ),
            ProposedRoute(
                "C9",
                "ksdft2effmass.analysis._parameter_study.ParameterStudyRefiner",
                "private_deep_import",
                "ksdft2effmass.analysis._parameter_study",
                "ParameterStudyRefiner",
                "ksdft2effmass.analysis._parameter_study",
                "ParameterStudyRefiner",
                ("migration.v2.calculators.plane-wave-study-contracts",),
                ("docs/architecture/v2/ksdft2effmass/plane-wave-parameter-studies.md",),
                "No wire format is established by the ABC itself.",
                (
                    "Changing ABC identity can affect subclass pickle/global "
                    "lookup; no pickle contract is inferred."
                ),
                (
                    "Protocol/ABC replacement changes nominal typing, runtime "
                    "construction, and __module__ identity."
                ),
            ),
            ProposedRoute(
                "C10",
                "ksdft2effmass.workflows.persistence.WorkflowRunSerializer._encode",
                "exported_class_private_method",
                "ksdft2effmass.workflows.persistence",
                "WorkflowRunSerializer._encode",
                "ksdft2effmass.workflows",
                "WorkflowRunSerializer",
                workflows_tasks,
                ("docs/development/source-documentation.rst",),
                (
                    "The private method implements accepted WorkflowRun encoding; "
                    "behavior and bytes cannot change silently."
                ),
                (
                    "Methods are not independent pickle globals under the ordinary "
                    "class contract."
                ),
                (
                    "Renaming to a public method changes the exported class member "
                    "surface; package __all__ cannot control it."
                ),
            ),
        )

    def _route_matrix(
        self,
        source_imports: list[ConsumerImport],
        test_imports: list[ConsumerImport],
    ) -> list[JsonRecord]:
        records: list[JsonRecord] = []
        for route in self._route_specs():
            source_consumers = self._route_import_consumers(route, source_imports)
            test_consumers = self._route_import_consumers(route, test_imports)
            doc_consumers = self._documentation_consumers(route)
            task_evidence: list[JsonRecord] = []
            for task_id in route.task_ids:
                path = self.arguments.task_root / f"{task_id}.json"
                if not path.is_file():
                    raise ValueError(f"route evidence Task is missing: {path}")
                task_text = path.read_text(encoding="utf-8")
                recorded_id = self._task_text_field(task_text, "task_id", path)
                status = self._task_text_field(task_text, "status", path)
                if recorded_id != task_id:
                    raise ValueError(f"Task identity mismatch: {path}")
                task_evidence.append(
                    {
                        "task_id": task_id,
                        "path": path.relative_to(
                            self.arguments.repository_root
                        ).as_posix(),
                        "status": status,
                        "classification": (
                            "accepted_task_evidence"
                            if "human_accepted" in status or status == "completed"
                            else "task_evidence_without_human_acceptance"
                        ),
                    }
                )
            api_evidence: tuple[JsonRecord, ...] = tuple(
                {
                    "path": path,
                    "classification": (
                        "api_or_architecture_evidence_not_self_executing"
                    ),
                }
                for path in route.api_evidence_paths
            )
            records.append(
                {
                    "candidate_id": route.candidate_id,
                    "route": route.route,
                    "route_kind": route.route_kind,
                    "defining_module": route.defining_module,
                    "defining_symbol": route.defining_symbol,
                    "maintained_source_consumers": tuple(source_consumers),
                    "maintained_test_consumers": tuple(test_consumers),
                    "maintained_documentation_consumers": tuple(doc_consumers),
                    "accepted_task_or_api_evidence": (
                        tuple(task_evidence) + api_evidence
                    ),
                    "compatibility_consequences": {
                        "wire": route.wire_consequence,
                        "pickle": route.pickle_consequence,
                        "module_identity": route.module_consequence,
                    },
                    "compatibility_disposition": (
                        "unclassified_pending_bounded_option_b_application"
                    ),
                    "documentation_evidence_limitation": (
                        "Only the exact qualified route or exact same-line from-import "
                        "form is matched; bare-symbol occurrences are excluded."
                    ),
                    "evidence_caveat": (
                        "Presence is evidence only. This row does not classify the "
                        "route as supported, private, deprecated, or removable. "
                        + (
                            "This package-set row is inventory context only and cannot "
                            "govern any individual export disposition."
                            if route.route_kind == "package_export_set"
                            else ""
                        )
                    ),
                }
            )
        return records

    def _managed_candidate_overlaps(self) -> list[JsonRecord]:
        specifications = (
            (
                "C10",
                "migration.v2.harness.compiler",
                (
                    "Compiler private-call facts must consume the accepted compiler "
                    "result and cannot redefine compiler contracts."
                ),
            ),
            (
                "C10",
                "migration.v2.harness.conformance",
                (
                    "Parser, ownership, and strict-conformance private-call facts "
                    "must consume the accepted conformance result."
                ),
            ),
            (
                "C10",
                "migration.v2.workflows.control-ingress",
                (
                    "Dispatch private-call facts remain governed by the accepted "
                    "Workflow control-ingress result."
                ),
            ),
        )
        records: list[JsonRecord] = []
        for candidate_id, task_id, consequence in specifications:
            path = self.arguments.task_root / f"{task_id}.json"
            task_text = path.read_text(encoding="utf-8")
            recorded_id = self._task_text_field(task_text, "task_id", path)
            status = self._task_text_field(task_text, "status", path)
            if recorded_id != task_id:
                raise ValueError(f"Task identity mismatch: {path}")
            records.append(
                {
                    "candidate_id": candidate_id,
                    "task_id": task_id,
                    "path": path.relative_to(self.arguments.repository_root).as_posix(),
                    "status": status,
                    "authority_consequence": consequence,
                }
            )
        return records

    @staticmethod
    def _task_text_field(task_text: str, field: str, path: Path) -> str:
        pattern = re.compile(rf'"{re.escape(field)}"\s*:\s*"([^"\\]*)"')
        matches = pattern.findall(task_text)
        if len(matches) != 1:
            raise ValueError(f"Task must contain one plain-string {field}: {path}")
        return matches[0]

    @staticmethod
    def _route_import_consumers(
        route: ProposedRoute, imports: list[ConsumerImport]
    ) -> list[JsonRecord]:
        consumers: list[JsonRecord] = []
        for item in imports:
            if item.imported_module != route.imported_module:
                continue
            if (
                route.route_kind == "internal_dependency_edge"
                and item.consumer != route.defining_module
            ):
                continue
            if route.imported_name is not None and route.imported_name not in (
                item.imported_names
            ):
                continue
            consumers.append(
                {
                    "consumer": item.consumer,
                    "line": item.line,
                    "imported_names": tuple(item.imported_names),
                }
            )
        return sorted(
            consumers,
            key=lambda item: (str(item["consumer"]), int(str(item["line"]))),
        )

    def _documentation_consumers(self, route: ProposedRoute) -> list[JsonRecord]:
        needles = {route.route}
        if route.imported_name is not None:
            needles.add(f"from {route.imported_module} import {route.imported_name}")
        consumers: list[JsonRecord] = []
        for path in sorted(self.arguments.documentation_root.rglob("*")):
            if path.suffix not in {".md", ".rst"} or not path.is_file():
                continue
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                matched = sorted(needle for needle in needles if needle in line)
                if matched:
                    consumers.append(
                        {
                            "path": path.relative_to(
                                self.arguments.repository_root
                            ).as_posix(),
                            "line": line_number,
                            "matched": tuple(matched),
                        }
                    )
        return consumers

    def _methodology(self) -> JsonRecord:
        return {
            "generator": ".pi/task-ownership/generate_python_architecture_inventory.py",
            "parser": (
                "Python standard-library ast under the canonical Python 3.14 "
                "project interpreter"
            ),
            "canonical_serialization": (
                "json.dumps(indent=2, sort_keys=True) plus one trailing newline"
            ),
            "ordering": (
                "path inventories are lexical; definitions preserve deterministic "
                "module/source order; explicitly aggregated records use documented "
                "lexical keys"
            ),
            "line_measure": (
                "physical lines are len(read_bytes().splitlines()); AST spans are "
                "inclusive lineno..end_lineno"
            ),
            "top_level_callable_rule": (
                "direct module-body FunctionDef and AsyncFunctionDef nodes"
            ),
            "private_name_rule": (
                "single-leading-underscore and non-dunder only; dunder methods are "
                "counted separately"
            ),
            "export_rule": (
                "literal list/tuple __all__ is decoded from string constants; "
                "packages without literal __all__ use non-underscore top-level AST "
                "bindings; this is syntax evidence only"
            ),
            "export_origin_rule": (
                "top-level import aliases identify defining module/symbol; locally "
                "defined bindings remain package-owned; unresolved assignments "
                "retain the package as origin"
            ),
            "dependency_rule": (
                "Every static Import/ImportFrom anywhere in the AST contributes edges. "
                "For from FACADE import NAME, FACADE contributes an edge when it is a "
                "maintained module and FACADE.NAME contributes a second edge when it "
                "is also a maintained submodule. This dual facade/submodule rule is "
                "intentional. TYPE_CHECKING, conditional, local, and optional imports "
                "remain lexical edges; dynamic imports are not inferred."
            ),
            "cycle_rule": (
                "Kosaraju-style two-pass strongly connected components over the "
                "exact lexical edge set: finish order on the forward graph, then "
                "components on the reverse graph; self edges are excluded"
            ),
            "abstraction_rule": (
                "direct Protocol or ABC/abstractmethod declarations and statically "
                "resolvable explicit inheritance only; structural satisfaction is "
                "not inferred"
            ),
            "consumer_rule": (
                "exact static ksdft2effmass imports from maintained source/tests; "
                "documentation consumers require an exact qualified route or exact "
                "same-line from-import form; bare-symbol substrings are excluded"
            ),
            "cross_private_call_rule": (
                "ClassName._method, ClassName()._method, and typed self-dependency "
                "calls resolve through local/imported class symbols; self/cls/super "
                "calls are omitted; a proven non-self receiver with unknown owner is "
                "deterministic cross_owner_owner_unresolved debt"
            ),
            "typed_wire_debt_rule": (
                "AST facts for typing.Any imports, Any annotations, cast(Any,...), "
                "object annotations, and dict/Mapping annotations erased by "
                "Any/object in harness.authority and harness._contract"
            ),
            "source_identity_rule": (
                "per-file SHA-256; aggregate SHA-256 updates path + NUL + file "
                "SHA-256 + newline in lexical path order"
            ),
            "thresholds_are_review_signals_not_defects": {
                "module_lines_at_least": self.LONG_MODULE,
                "class_ast_span_at_least": self.LONG_CLASS,
                "method_ast_span_at_least": self.LONG_METHOD,
            },
            "reproduction_command": (
                "python/.venv/bin/python",
                ".pi/task-ownership/generate_python_architecture_inventory.py",
                "--repository-root",
                ".",
                "--source-root",
                "python/src/ksdft2effmass",
                "--test-root",
                "python/tests",
                "--documentation-root",
                "docs",
                "--task-root",
                "tasks/software",
                "--output",
                "harness/reports/python-architecture-inventory.json",
            ),
        }


def main() -> int:
    """Adapt the exact command-line entry point to the generator ActionObject."""
    try:
        arguments = InventoryCommandArguments.parse(tuple(sys.argv[1:]))
        PythonArchitectureInventoryGenerator(arguments).execute()
    except (OSError, ValueError, SyntaxError) as error:
        print(f"inventory generation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
