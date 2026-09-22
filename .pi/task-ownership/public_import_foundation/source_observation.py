"""Static source observations for public-import foundation generation."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TypeAlias

from python_public_import_foundation_model import (
    BindingKind,
    ImportKind,
    ImportObservation,
    InputCategory,
    PackageBinding,
)

from public_import_foundation.input_snapshot import (
    FoundationFormatError,
    FoundationInputManifest,
)

DefiningBindingTable: TypeAlias = tuple[
    tuple[str, tuple[tuple[str, str, str], ...]], ...
]


@dataclass(frozen=True, slots=True)
class PythonConsumerImportInspector:
    """Extract neutral first-party import syntax from explicit Python bytes."""

    def execute(self, path: str, payload: bytes) -> tuple[ImportObservation, ...]:
        """Return canonically ordered imports targeting ksdft2effmass."""
        try:
            tree = ast.parse(payload, filename=path)
        except (SyntaxError, UnicodeError) as exc:
            raise FoundationFormatError(
                f"cannot parse selected Python consumer {path}: {exc}"
            ) from exc
        records: list[ImportObservation] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "ksdft2effmass" or alias.name.startswith(
                        "ksdft2effmass."
                    ):
                        records.append(
                            ImportObservation(
                                consumer_path=path,
                                line=node.lineno,
                                column=node.col_offset,
                                import_kind=ImportKind.IMPORT,
                                imported_module=alias.name,
                                imported_name=None,
                            )
                        )
            elif (
                isinstance(node, ast.ImportFrom)
                and node.level == 0
                and node.module is not None
                and (
                    node.module == "ksdft2effmass"
                    or node.module.startswith("ksdft2effmass.")
                )
            ):
                for alias in node.names:
                    records.append(
                        ImportObservation(
                            consumer_path=path,
                            line=node.lineno,
                            column=node.col_offset,
                            import_kind=ImportKind.FROM_IMPORT,
                            imported_module=node.module,
                            imported_name=alias.name,
                        )
                    )
        return tuple(
            sorted(
                records,
                key=lambda record: (
                    record.consumer_path,
                    record.line,
                    record.column,
                    record.import_kind.value,
                    record.imported_module,
                    record.imported_name or "",
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class PythonInitializerInspector:
    """Extract neutral package bindings and literal star-export state."""

    def execute(
        self, module_name: str, path: str, payload: bytes
    ) -> tuple[bool, tuple[str, ...], tuple[PackageBinding, ...]]:
        """Return initializer state or fail on dynamic export behavior."""
        try:
            tree = ast.parse(payload, filename=path)
        except (SyntaxError, UnicodeError) as exc:
            raise FoundationFormatError(
                f"cannot parse initializer {path}: {exc}"
            ) from exc
        bindings: dict[str, PackageBinding] = {}
        declared_all: list[str] | None = None
        allowed_all_targets: set[int] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    local_name = alias.asname or alias.name.split(".")[0]
                    bindings[local_name] = PackageBinding(
                        kind=BindingKind.IMPORT,
                        line=node.lineno,
                        local_name=local_name,
                        imported_name=alias.name,
                        origin=alias.name,
                        defining_origin=None,
                        origin_resolution=None,
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module == "__future__" and node.level == 0:
                    continue
                origin_prefix = self._absolute_import_module(module_name, node)
                for alias in node.names:
                    if alias.name == "*":
                        raise FoundationFormatError(
                            f"star import is unrepresentable in {path}"
                        )
                    local_name = alias.asname or alias.name
                    bindings[local_name] = PackageBinding(
                        kind=BindingKind.FROM_IMPORT,
                        line=node.lineno,
                        local_name=local_name,
                        imported_name=alias.name,
                        origin=f"{origin_prefix}.{alias.name}",
                        defining_origin=None,
                        origin_resolution=None,
                    )
            elif isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                bindings[node.name] = PackageBinding(
                    kind=BindingKind.DEFINITION,
                    line=node.lineno,
                    local_name=node.name,
                    imported_name=node.name,
                    origin=f"{module_name}.{node.name}",
                    defining_origin=None,
                    origin_resolution=None,
                )
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    if not isinstance(target, ast.Name):
                        continue
                    if target.id == "__all__":
                        allowed_all_targets.add(id(target))
                        declared_all = self._literal_names(node.value, path)
                    else:
                        bindings[target.id] = PackageBinding(
                            kind=BindingKind.ASSIGNMENT,
                            line=node.lineno,
                            local_name=target.id,
                            imported_name=target.id,
                            origin=f"{module_name}.{target.id}",
                            defining_origin=None,
                            origin_resolution=None,
                        )
            elif (
                isinstance(node, ast.AugAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == "__all__"
            ):
                allowed_all_targets.add(id(node.target))
                if declared_all is None or not isinstance(node.op, ast.Add):
                    raise FoundationFormatError(f"dynamic __all__ state in {path}")
                declared_all.extend(self._literal_names(node.value, path))
        self._reject_unhandled_all_operations(tree, allowed_all_targets, path)
        effective_names = () if declared_all is None else tuple(declared_all)
        if len(effective_names) != len(set(effective_names)):
            raise FoundationFormatError(f"duplicate __all__ name in {path}")
        return (
            declared_all is not None,
            effective_names,
            tuple(bindings[name] for name in sorted(bindings)),
        )

    @staticmethod
    def _absolute_import_module(module_name: str, node: ast.ImportFrom) -> str:
        if node.level == 0:
            if node.module is None:
                raise FoundationFormatError("absolute from-import requires a module")
            return node.module
        parts = module_name.split(".")
        retained = len(parts) - node.level + 1
        if retained < 1:
            raise FoundationFormatError("relative import escapes the package")
        base = parts[:retained]
        if node.module:
            base.extend(node.module.split("."))
        return ".".join(base)

    @staticmethod
    def _reject_unhandled_all_operations(
        tree: ast.Module, allowed_targets: set[int], path: str
    ) -> None:
        """Reject every unrepresented export-state mutation or escape."""
        for node in ast.walk(tree):
            if (
                isinstance(node, (ast.Assign, ast.AnnAssign))
                and node.value is not None
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id in {"globals", "vars"}
                and not node.value.args
                and not node.value.keywords
            ):
                raise FoundationFormatError(
                    f"namespace alias can mutate __all__ in {path}"
                )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Call)
                and isinstance(node.func.value.func, ast.Name)
                and node.func.value.func.id in {"globals", "vars"}
                and not node.func.value.args
                and not node.func.value.keywords
                and (
                    (
                        node.func.attr == "update"
                        and any(keyword.arg == "__all__" for keyword in node.keywords)
                    )
                    or (
                        node.func.attr == "__setitem__"
                        and bool(node.args)
                        and isinstance(node.args[0], ast.Constant)
                        and node.args[0].value == "__all__"
                    )
                )
            ):
                raise FoundationFormatError(
                    f"namespace call can mutate __all__ in {path}"
                )
            if (
                isinstance(node, ast.Subscript)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id in {"globals", "vars"}
                and not node.value.args
                and not node.value.keywords
                and isinstance(node.slice, ast.Constant)
                and node.slice.value == "__all__"
            ):
                raise FoundationFormatError(
                    f"indirect __all__ access is unrepresentable in {path}"
                )
            if (
                isinstance(node, (ast.Assign, ast.AnnAssign))
                and node.value is not None
                and any(
                    isinstance(value, ast.Name) and value.id == "__all__"
                    for value in ast.walk(node.value)
                )
                and not any(
                    isinstance(target, ast.Name) and target.id == "__all__"
                    for target in (
                        node.targets if isinstance(node, ast.Assign) else [node.target]
                    )
                )
            ):
                raise FoundationFormatError(
                    f"aliased __all__ access is unrepresentable in {path}"
                )
            if isinstance(node, ast.Name) and node.id == "__all__":
                if isinstance(node.ctx, ast.Load):
                    raise FoundationFormatError(
                        f"unrepresented __all__ load or escape in {path}"
                    )
                if (
                    isinstance(node.ctx, (ast.Store, ast.Del))
                    and id(node) not in allowed_targets
                ):
                    raise FoundationFormatError(
                        f"unrepresented __all__ assignment in {path}"
                    )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "__all__"
            ):
                raise FoundationFormatError(f"unrepresented __all__ mutation in {path}")
            if (
                isinstance(node, ast.Subscript)
                and isinstance(node.value, ast.Name)
                and node.value.id == "__all__"
                and isinstance(node.ctx, (ast.Store, ast.Del))
            ):
                raise FoundationFormatError(f"unrepresented __all__ mutation in {path}")

    @staticmethod
    def _literal_names(value: ast.expr | None, path: str) -> list[str]:
        if not isinstance(value, (ast.List, ast.Tuple)):
            raise FoundationFormatError(f"dynamic or unrepresentable __all__ in {path}")
        names: list[str] = []
        for element in value.elts:
            if not isinstance(element, ast.Constant) or type(element.value) is not str:
                raise FoundationFormatError(f"nonliteral __all__ member in {path}")
            names.append(element.value)
        return names


@dataclass(frozen=True, slots=True)
class PythonDefiningOriginResolver:
    """Resolve first-party re-export chains from explicit selected source bytes."""

    @staticmethod
    def execute(
        manifest: FoundationInputManifest, payloads: dict[str, bytes]
    ) -> DefiningBindingTable:
        modules: dict[str, dict[str, tuple[str, str]]] = {}
        for entry in manifest.entries:
            if entry.category is not InputCategory.PRODUCTION_MODULE:
                continue
            path = entry.path.as_posix()
            module_name, is_facade = PythonDefiningOriginResolver.module_name(path)
            try:
                tree = ast.parse(payloads[path], filename=path)
            except (SyntaxError, UnicodeError) as exc:
                raise FoundationFormatError(
                    f"cannot resolve bindings in {path}: {exc}"
                ) from exc
            bindings: dict[str, tuple[str, str]] = {}
            for node in tree.body:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        local = alias.asname or alias.name.split(".")[0]
                        bindings[local] = ("import", alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module == "__future__" and node.level == 0:
                        continue
                    origin = PythonDefiningOriginResolver._absolute_module(
                        module_name, is_facade, node
                    )
                    for alias in node.names:
                        if alias.name != "*":
                            bindings[alias.asname or alias.name] = (
                                "from_import",
                                f"{origin}.{alias.name}",
                            )
                elif isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    bindings[node.name] = ("definition", f"{module_name}.{node.name}")
                elif isinstance(node, ast.TypeAlias) and isinstance(
                    node.name, ast.Name
                ):
                    bindings[node.name.id] = (
                        "definition",
                        f"{module_name}.{node.name.id}",
                    )
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = (
                        node.targets if isinstance(node, ast.Assign) else [node.target]
                    )
                    for target in targets:
                        if isinstance(target, ast.Name) and target.id != "__all__":
                            bindings[target.id] = (
                                "assignment",
                                f"{module_name}.{target.id}",
                            )
            modules[module_name] = bindings
        return tuple(
            (
                module_name,
                tuple(
                    (name, kind, target)
                    for name, (kind, target) in sorted(bindings.items())
                ),
            )
            for module_name, bindings in sorted(modules.items())
        )

    @staticmethod
    def module_name(path: str) -> tuple[str, bool]:
        prefix = "python/src/"
        if not path.startswith(prefix) or not path.endswith(".py"):
            raise FoundationFormatError(f"invalid production module path: {path}")
        relative = path[len(prefix) : -3]
        is_facade = relative.endswith("/__init__")
        if is_facade:
            relative = relative.removesuffix("/__init__")
        return relative.replace("/", "."), is_facade

    @staticmethod
    def resolve(
        direct_target: str,
        binding_table: DefiningBindingTable,
    ) -> str:
        modules = {
            module_name: {name: (kind, target) for name, kind, target in bindings}
            for module_name, bindings in binding_table
        }
        current = direct_target
        visited: set[str] = set()
        while True:
            if current in visited:
                raise FoundationFormatError(f"cyclic defining origin: {current}")
            visited.add(current)
            if current in modules:
                return current
            matching = sorted(
                (name for name in modules if current.startswith(f"{name}.")),
                key=len,
                reverse=True,
            )
            if not matching:
                return current
            module_name = matching[0]
            suffix = current[len(module_name) + 1 :]
            if "." in suffix:
                return current
            binding = modules[module_name].get(suffix)
            if binding is None:
                raise FoundationFormatError(f"missing defining origin: {current}")
            kind, target = binding
            if kind in {"definition", "assignment"}:
                return target
            current = target

    @staticmethod
    def _absolute_module(
        module_name: str, is_facade: bool, node: ast.ImportFrom
    ) -> str:
        if node.level == 0:
            if node.module is None:
                raise FoundationFormatError("absolute from-import requires a module")
            return node.module
        package = module_name.split(".") if is_facade else module_name.split(".")[:-1]
        retained = len(package) - node.level + 1
        if retained < 1:
            raise FoundationFormatError("relative import escapes the package")
        parts = package[:retained]
        if node.module:
            parts.extend(node.module.split("."))
        return ".".join(parts)
