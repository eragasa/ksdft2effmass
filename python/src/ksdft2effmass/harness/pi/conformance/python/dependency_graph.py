"""Explicit-input dependency graph views over accepted production-source facts.

This unsupported implementation sibling derives three separately identified internal
module graphs from caller-supplied immutable production facts and exact module
bindings. The lexical view retains every represented import. The
runtime-unconditional view retains imports outside represented execution contexts and
outside callable owners. The package-facade-excluded view applies the lexical rule
while omitting modules explicitly identified by the caller as package facades.

Every edge retains exact source identity, import syntax, span, and resolution kind.
Strongly connected components are structural results for their named view only; in
particular, a lexical component is not a runtime failure. Direction checks are made
only for explicitly requested observed edges. They pass only with an explicitly
supplied accepted contract matching that exact edge and view, and unrequested edges
receive no universal disposition.

The analyzer performs no filesystem discovery, import execution, source mutation,
repair, package export, or supported-route decision. Its descriptive implementation
classes are intentionally not re-exported as supported package APIs.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath

from .production import (
    PythonProductionImportFact,
    PythonProductionImportKind,
    PythonProductionInspectionResult,
    PythonProductionModuleInspection,
    PythonProductionScopeKind,
)


class PythonDependencyGraphView(StrEnum):
    """Identify one exact dependency graph interpretation."""

    LEXICAL = "lexical"
    RUNTIME_UNCONDITIONAL = "runtime_unconditional"
    PACKAGE_FACADE_EXCLUDED = "package_facade_excluded"


class PythonDependencyResolutionKind(StrEnum):
    """Identify how one import fact resolves to an internal target."""

    DIRECT_IMPORT = "direct_import"
    FROM_FACADE = "from_facade"
    FROM_IMPORTED_SUBMODULE = "from_imported_submodule"


class PythonDependencyDirection(StrEnum):
    """Represent the exact disposition supplied by an accepted contract."""

    ALLOW = "allow"
    PROHIBIT = "prohibit"


class PythonDependencyDirectionStatus(StrEnum):
    """Represent the fail-closed outcome of one explicit direction check."""

    ALLOWED = "allowed"
    PROHIBITED = "prohibited"
    MISSING_CONTRACT = "missing_contract"
    MISMATCHED_CONTRACT = "mismatched_contract"
    EDGE_ABSENT = "edge_absent"


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonDependencyModule:
    """Bind one internal module identity to one exact successful source outcome.

    Parameters
    ----------
    module_name
        Exact dotted Python module identity supplied by the caller.
    is_package_facade
        Exact caller-supplied package-facade identity; no path inference is used.
    input_identity, source_path, source_sha256
        Exact production-fact outcome identity.
    """

    module_name: str
    is_package_facade: bool
    input_identity: str
    source_path: PurePosixPath
    source_sha256: str

    def __post_init__(self) -> None:
        """Require a precise dotted name and exact production source identity."""
        self._require_text(self.module_name, "module_name")
        if any(not part.isidentifier() for part in self.module_name.split(".")):
            raise ValueError("module_name must contain only dotted Python identifiers")
        if type(self.is_package_facade) is not bool:
            raise TypeError("is_package_facade must be a built-in bool")
        self._require_text(self.input_identity, "input_identity")
        if type(self.source_path) is not PurePosixPath:
            raise TypeError("source_path must be PurePosixPath")
        rendered = self.source_path.as_posix()
        if (
            rendered in {"", "."}
            or self.source_path.is_absolute()
            or ".." in self.source_path.parts
            or "\\" in rendered
            or unicodedata.normalize("NFC", rendered) != rendered
        ):
            raise ValueError("source_path must be normalized repository-relative POSIX")
        if type(self.source_sha256) is not str:
            raise TypeError("source_sha256 must be a built-in str")
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256 hexadecimal")

    @staticmethod
    def _require_text(value: str, name: str) -> None:
        """Require normalized nonempty single-line built-in text."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a built-in str")
        if (
            not value
            or "\n" in value
            or "\r" in value
            or unicodedata.normalize("NFC", value) != value
        ):
            raise ValueError(f"{name} must be normalized nonempty single-line text")

    @property
    def source_key(self) -> tuple[str, str, str]:
        """Return the exact successful production-outcome lookup key."""
        return (self.input_identity, self.source_path.as_posix(), self.source_sha256)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyEdgeProvenance:
    """Retain one exact module binding and import contribution to an edge."""

    source: PythonDependencyModule
    import_fact: PythonProductionImportFact
    resolution: PythonDependencyResolutionKind

    def __post_init__(self) -> None:
        """Require exact binding, accepted fact type, and compatible resolution."""
        if type(self.source) is not PythonDependencyModule:
            raise TypeError("source must be PythonDependencyModule")
        if type(self.import_fact) is not PythonProductionImportFact:
            raise TypeError("import_fact must be PythonProductionImportFact")
        if type(self.resolution) is not PythonDependencyResolutionKind:
            raise TypeError("resolution must be PythonDependencyResolutionKind")
        if (self.resolution is PythonDependencyResolutionKind.DIRECT_IMPORT) != (
            self.import_fact.kind is PythonProductionImportKind.IMPORT
        ):
            raise ValueError("resolution kind must agree with import syntax")
        if self.resolution is not PythonDependencyResolutionKind.DIRECT_IMPORT:
            if self.import_fact.kind is not PythonProductionImportKind.FROM_IMPORT:
                raise ValueError("from-import resolution requires from-import syntax")
            if self._from_base() is None:
                raise ValueError("relative import cannot resolve above its package")

    def _from_base(self) -> str | None:
        """Resolve the represented from-import against the exact source binding."""
        fact = self.import_fact
        if fact.relative_level == 0:
            return fact.module or ""
        package = (
            self.source.module_name
            if self.source.is_package_facade
            else self.source.module_name.rpartition(".")[0]
        )
        if not package:
            return None
        parts = package.split(".")
        drop = fact.relative_level - 1
        if drop >= len(parts):
            return None
        anchor = ".".join(parts[: len(parts) - drop])
        return f"{anchor}.{fact.module}" if fact.module else anchor

    @property
    def resolved_target(self) -> str:
        """Return the exact endpoint selected by the retained resolution kind."""
        if self.resolution is PythonDependencyResolutionKind.DIRECT_IMPORT:
            return self.import_fact.name
        base = self._from_base()
        if base is None:
            raise AssertionError("validated provenance requires a from-import base")
        if self.resolution is PythonDependencyResolutionKind.FROM_FACADE:
            return base
        return f"{base}.{self.import_fact.name}" if base else self.import_fact.name

    @property
    def sort_key(
        self,
    ) -> tuple[str, str, str, str, int, int, str, str, str, str, int]:
        """Return canonical complete provenance ordering state."""
        fact = self.import_fact
        return (
            self.source.module_name,
            self.source.input_identity,
            self.source.source_path.as_posix(),
            self.source.source_sha256,
            fact.location.line,
            fact.location.column,
            self.resolution.value,
            fact.kind.value,
            fact.module or "",
            fact.name,
            fact.relative_level,
        )


@dataclass(frozen=True, slots=True, order=True, kw_only=True)
class PythonDependencyGraphNode:
    """Represent one module node under one named graph view."""

    view: PythonDependencyGraphView
    module_name: str

    def __post_init__(self) -> None:
        """Require an exact view and dotted module identity."""
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        if type(self.module_name) is not str:
            raise TypeError("module_name must be a built-in str")
        if (
            not self.module_name
            or unicodedata.normalize("NFC", self.module_name) != self.module_name
        ):
            raise ValueError("module_name must be normalized nonempty text")
        if any(not part.isidentifier() for part in self.module_name.split(".")):
            raise ValueError("module_name must contain only dotted Python identifiers")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyGraphEdge:
    """Represent one internal module edge and all exact contributing imports."""

    view: PythonDependencyGraphView
    source_module: str
    target_module: str
    provenance: tuple[PythonDependencyEdgeProvenance, ...]

    def __post_init__(self) -> None:
        """Require a non-self edge with canonical nonempty provenance."""
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        for name, value in (
            ("source_module", self.source_module),
            ("target_module", self.target_module),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be normalized nonempty text")
            if any(not part.isidentifier() for part in value.split(".")):
                raise ValueError(f"{name} must contain dotted Python identifiers")
        if self.source_module == self.target_module:
            raise ValueError("dependency edges must connect distinct modules")
        if (
            type(self.provenance) is not tuple
            or not self.provenance
            or any(
                type(item) is not PythonDependencyEdgeProvenance
                for item in self.provenance
            )
        ):
            raise TypeError("provenance must be a nonempty provenance tuple")
        if len(set(self.provenance)) != len(self.provenance):
            raise ValueError("provenance contributions must be unique")
        if self.provenance != tuple(
            sorted(self.provenance, key=lambda item: item.sort_key)
        ):
            raise ValueError("provenance must be in canonical order")
        if any(
            item.source.module_name != self.source_module
            or item.resolved_target != self.target_module
            for item in self.provenance
        ):
            raise ValueError("provenance must resolve to the exact edge endpoints")

    @property
    def sort_key(self) -> tuple[str, str, str]:
        """Return canonical view and endpoint ordering state."""
        return (self.view.value, self.source_module, self.target_module)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyStronglyConnectedComponent:
    """Represent one deterministic strongly connected component for one view."""

    view: PythonDependencyGraphView
    module_names: tuple[str, ...]

    def __post_init__(self) -> None:
        """Require one exact view and a nonempty sorted unique module tuple."""
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        if (
            type(self.module_names) is not tuple
            or not self.module_names
            or any(type(name) is not str for name in self.module_names)
        ):
            raise TypeError("module_names must be a nonempty tuple of str values")
        if self.module_names != tuple(sorted(set(self.module_names))):
            raise ValueError("module_names must be sorted and unique")

    @property
    def sort_key(self) -> tuple[str, tuple[str, ...]]:
        """Return canonical view and member ordering state."""
        return (self.view.value, self.module_names)


class PythonDependencyGraphStructureValidator:
    """Validate exact graph/SCC agreement and derive canonical SCC partitions."""

    __slots__ = ()

    def execute(self, result: PythonDependencyGraphViewResult) -> None:
        """Reject a represented SCC partition that disagrees with exact edges."""
        expected = self.components(
            result.view,
            tuple(node.module_name for node in result.nodes),
            result.edges,
        )
        if result.strongly_connected_components != expected:
            raise ValueError(
                "strongly_connected_components must equal the exact graph SCCs"
            )

    def components(
        self,
        view: PythonDependencyGraphView,
        module_names: tuple[str, ...],
        edges: tuple[PythonDependencyGraphEdge, ...],
    ) -> tuple[PythonDependencyStronglyConnectedComponent, ...]:
        """Return a canonical Kosaraju two-pass SCC partition."""
        adjacency: dict[str, list[str]] = {name: [] for name in module_names}
        reverse: dict[str, list[str]] = {name: [] for name in module_names}
        for edge in edges:
            adjacency[edge.source_module].append(edge.target_module)
            reverse[edge.target_module].append(edge.source_module)
        ordered_adjacency = {
            name: tuple(sorted(set(targets))) for name, targets in adjacency.items()
        }
        ordered_reverse = {
            name: tuple(sorted(set(targets))) for name, targets in reverse.items()
        }
        visited: set[str] = set()
        finish: list[str] = []
        for module_name in module_names:
            self._finish_visit(module_name, ordered_adjacency, visited, finish)
        assigned: set[str] = set()
        members_by_component: list[tuple[str, ...]] = []
        for module_name in reversed(finish):
            if module_name in assigned:
                continue
            members: list[str] = []
            self._component_visit(module_name, ordered_reverse, assigned, members)
            members_by_component.append(tuple(sorted(members)))
        return tuple(
            PythonDependencyStronglyConnectedComponent(view=view, module_names=members)
            for members in sorted(members_by_component)
        )

    def _finish_visit(
        self,
        module_name: str,
        adjacency: dict[str, tuple[str, ...]],
        visited: set[str],
        finish: list[str],
    ) -> None:
        """Append one depth-first finish order using canonical neighbors."""
        if module_name in visited:
            return
        visited.add(module_name)
        for target in adjacency[module_name]:
            self._finish_visit(target, adjacency, visited, finish)
        finish.append(module_name)

    def _component_visit(
        self,
        module_name: str,
        reverse: dict[str, tuple[str, ...]],
        assigned: set[str],
        members: list[str],
    ) -> None:
        """Collect one reverse-graph component using canonical neighbors."""
        if module_name in assigned:
            return
        assigned.add(module_name)
        members.append(module_name)
        for target in reverse[module_name]:
            self._component_visit(target, reverse, assigned, members)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyGraphViewResult:
    """Represent deterministic nodes, edges, and SCCs for one named view."""

    view: PythonDependencyGraphView
    nodes: tuple[PythonDependencyGraphNode, ...]
    edges: tuple[PythonDependencyGraphEdge, ...]
    strongly_connected_components: tuple[
        PythonDependencyStronglyConnectedComponent, ...
    ]

    def __post_init__(self) -> None:
        """Require exact view attribution and canonical closed collections."""
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        if type(self.nodes) is not tuple or any(
            type(node) is not PythonDependencyGraphNode for node in self.nodes
        ):
            raise TypeError("nodes must contain PythonDependencyGraphNode values")
        if any(node.view is not self.view for node in self.nodes):
            raise ValueError("every node must name the result view")
        if self.nodes != tuple(sorted(self.nodes, key=lambda node: node.module_name)):
            raise ValueError("nodes must be in canonical order")
        if len({node.module_name for node in self.nodes}) != len(self.nodes):
            raise ValueError("nodes must have unique module identities")
        if type(self.edges) is not tuple or any(
            type(edge) is not PythonDependencyGraphEdge for edge in self.edges
        ):
            raise TypeError("edges must contain PythonDependencyGraphEdge values")
        if any(edge.view is not self.view for edge in self.edges):
            raise ValueError("every edge must name the result view")
        if self.edges != tuple(sorted(self.edges, key=lambda edge: edge.sort_key)):
            raise ValueError("edges must be in canonical order")
        edge_endpoints = tuple(
            (edge.source_module, edge.target_module) for edge in self.edges
        )
        if len(set(edge_endpoints)) != len(edge_endpoints):
            raise ValueError("edges must have unique endpoint pairs")
        node_names = frozenset(node.module_name for node in self.nodes)
        if any(
            edge.source_module not in node_names or edge.target_module not in node_names
            for edge in self.edges
        ):
            raise ValueError("every edge endpoint must belong to the result nodes")
        components = self.strongly_connected_components
        if type(components) is not tuple or any(
            type(component) is not PythonDependencyStronglyConnectedComponent
            for component in components
        ):
            raise TypeError("strongly_connected_components contains an invalid type")
        if any(component.view is not self.view for component in components):
            raise ValueError("every component must name the result view")
        if components != tuple(sorted(components, key=lambda item: item.sort_key)):
            raise ValueError("strongly_connected_components must be canonical")
        flattened = tuple(
            module for component in components for module in component.module_names
        )
        if frozenset(flattened) != node_names or len(flattened) != len(node_names):
            raise ValueError("strongly_connected_components must partition all nodes")
        PythonDependencyGraphStructureValidator().execute(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonAcceptedDependencyContract:
    """Represent one supplied accepted disposition for one exact view and edge."""

    contract_identity: str
    view: PythonDependencyGraphView
    source_module: str
    target_module: str
    direction: PythonDependencyDirection

    def __post_init__(self) -> None:
        """Require exact normalized identity, view, endpoints, and disposition."""
        if type(self.contract_identity) is not str:
            raise TypeError("contract_identity must be a built-in str")
        if (
            not self.contract_identity
            or "\n" in self.contract_identity
            or "\r" in self.contract_identity
            or unicodedata.normalize("NFC", self.contract_identity)
            != self.contract_identity
        ):
            raise ValueError("contract_identity must be normalized single-line text")
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        for name, value in (
            ("source_module", self.source_module),
            ("target_module", self.target_module),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be normalized nonempty text")
            if any(not part.isidentifier() for part in value.split(".")):
                raise ValueError(f"{name} must contain dotted Python identifiers")
        if self.source_module == self.target_module:
            raise ValueError("dependency contracts must govern a distinct-module edge")
        if type(self.direction) is not PythonDependencyDirection:
            raise TypeError("direction must be PythonDependencyDirection")


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyDirectionCheck:
    """Request enforcement for one exact graph edge and optional accepted contract."""

    view: PythonDependencyGraphView
    source_module: str
    target_module: str
    accepted_contract: PythonAcceptedDependencyContract | None

    def __post_init__(self) -> None:
        """Require exact check fields without treating a missing contract as valid."""
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        for name, value in (
            ("source_module", self.source_module),
            ("target_module", self.target_module),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be normalized nonempty text")
            if any(not part.isidentifier() for part in value.split(".")):
                raise ValueError(f"{name} must contain dotted Python identifiers")
        if self.source_module == self.target_module:
            raise ValueError("direction checks must identify a distinct-module edge")
        if self.accepted_contract is not None and (
            type(self.accepted_contract) is not PythonAcceptedDependencyContract
        ):
            raise TypeError(
                "accepted_contract must be PythonAcceptedDependencyContract or None"
            )

    @property
    def sort_key(self) -> tuple[str, str, str, str]:
        """Return canonical check ordering state."""
        contract_identity = (
            ""
            if self.accepted_contract is None
            else self.accepted_contract.contract_identity
        )
        return (
            self.view.value,
            self.source_module,
            self.target_module,
            contract_identity,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyDirectionResult:
    """Represent one fail-closed result for one explicitly requested edge check."""

    view: PythonDependencyGraphView
    source_module: str
    target_module: str
    accepted_contract: PythonAcceptedDependencyContract | None
    edge: PythonDependencyGraphEdge | None
    status: PythonDependencyDirectionStatus

    def __post_init__(self) -> None:
        """Require exact check attribution and compatible status/contract state."""
        if type(self.view) is not PythonDependencyGraphView:
            raise TypeError("view must be PythonDependencyGraphView")
        for name, value in (
            ("source_module", self.source_module),
            ("target_module", self.target_module),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value or unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be normalized nonempty text")
            if any(not part.isidentifier() for part in value.split(".")):
                raise ValueError(f"{name} must contain dotted Python identifiers")
        if self.accepted_contract is not None and (
            type(self.accepted_contract) is not PythonAcceptedDependencyContract
        ):
            raise TypeError(
                "accepted_contract must be PythonAcceptedDependencyContract or None"
            )
        if self.edge is not None and type(self.edge) is not PythonDependencyGraphEdge:
            raise TypeError("edge must be PythonDependencyGraphEdge or None")
        if self.edge is not None and (
            self.edge.view is not self.view
            or self.edge.source_module != self.source_module
            or self.edge.target_module != self.target_module
        ):
            raise ValueError("retained edge must match direction result identity")
        if type(self.status) is not PythonDependencyDirectionStatus:
            raise TypeError("status must be PythonDependencyDirectionStatus")
        if self.source_module == self.target_module:
            raise ValueError("direction results must identify a distinct-module edge")
        if (self.status is PythonDependencyDirectionStatus.MISSING_CONTRACT) != (
            self.accepted_contract is None
        ):
            raise ValueError("missing-contract status must match contract absence")
        contract = self.accepted_contract
        if contract is None:
            return
        exact_contract = (
            contract.view is self.view
            and contract.source_module == self.source_module
            and contract.target_module == self.target_module
        )
        if self.status is PythonDependencyDirectionStatus.MISMATCHED_CONTRACT:
            if exact_contract:
                raise ValueError("mismatched-contract status requires a mismatch")
            return
        if not exact_contract:
            raise ValueError("non-mismatch status requires an exact edge contract")
        if self.status is PythonDependencyDirectionStatus.ALLOWED and (
            contract.direction is not PythonDependencyDirection.ALLOW
        ):
            raise ValueError("allowed status requires an allow contract")
        if self.status is PythonDependencyDirectionStatus.PROHIBITED and (
            contract.direction is not PythonDependencyDirection.PROHIBIT
        ):
            raise ValueError("prohibited status requires a prohibit contract")
        if (
            self.status
            in {
                PythonDependencyDirectionStatus.ALLOWED,
                PythonDependencyDirectionStatus.PROHIBITED,
            }
            and self.edge is None
        ):
            raise ValueError("passing or prohibited status requires an observed edge")
        if (
            self.status is PythonDependencyDirectionStatus.EDGE_ABSENT
            and self.edge is not None
        ):
            raise ValueError("edge-absent status cannot retain an observed edge")

    @property
    def passed(self) -> bool:
        """Return whether exact contract explicitly allows the retained edge."""
        return (
            self.status is PythonDependencyDirectionStatus.ALLOWED
            and self.edge is not None
        )

    @property
    def sort_key(self) -> tuple[str, str, str, str]:
        """Return canonical result ordering state."""
        identity = (
            ""
            if self.accepted_contract is None
            else self.accepted_contract.contract_identity
        )
        return (self.view.value, self.source_module, self.target_module, identity)


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyGraphRequest:
    """Represent exact immutable graph inputs and explicitly requested checks."""

    production_facts: PythonProductionInspectionResult
    modules: tuple[PythonDependencyModule, ...]
    direction_checks: tuple[PythonDependencyDirectionCheck, ...]

    def __post_init__(self) -> None:
        """Require exact facts, one binding per success, and unique explicit checks."""
        if type(self.production_facts) is not PythonProductionInspectionResult:
            raise TypeError("production_facts must be PythonProductionInspectionResult")
        if type(self.modules) is not tuple or any(
            type(module) is not PythonDependencyModule for module in self.modules
        ):
            raise TypeError("modules must contain PythonDependencyModule values")
        module_names = tuple(module.module_name for module in self.modules)
        if len(set(module_names)) != len(module_names):
            raise ValueError("module bindings must have unique module names")
        source_keys = tuple(module.source_key for module in self.modules)
        if len(set(source_keys)) != len(source_keys):
            raise ValueError("module bindings must have unique source identities")
        successful_keys = tuple(
            (
                module.input_identity,
                module.path.as_posix(),
                module.source_sha256,
            )
            for module in self.production_facts.modules
            if module.facts is not None and module.source_sha256 is not None
        )
        if len(set(successful_keys)) != len(successful_keys):
            raise ValueError(
                "successful production facts have ambiguous duplicate identities"
            )
        if frozenset(source_keys) != frozenset(successful_keys):
            raise ValueError(
                "module bindings must exactly cover successful production facts"
            )
        if type(self.direction_checks) is not tuple or any(
            type(check) is not PythonDependencyDirectionCheck
            for check in self.direction_checks
        ):
            raise TypeError(
                "direction_checks must contain PythonDependencyDirectionCheck values"
            )
        check_keys = tuple(check.sort_key for check in self.direction_checks)
        if len(set(check_keys)) != len(check_keys):
            raise ValueError("direction checks must be unique")
        contracts_by_identity: dict[str, PythonAcceptedDependencyContract] = {}
        directions_by_edge: dict[
            tuple[PythonDependencyGraphView, str, str], PythonDependencyDirection
        ] = {}
        for check in self.direction_checks:
            contract = check.accepted_contract
            if contract is None:
                continue
            existing = contracts_by_identity.get(contract.contract_identity)
            if existing is not None and existing != contract:
                raise ValueError(
                    "one accepted contract identity must map to one exact payload"
                )
            contracts_by_identity[contract.contract_identity] = contract
            edge_identity = (
                contract.view,
                contract.source_module,
                contract.target_module,
            )
            existing_direction = directions_by_edge.get(edge_identity)
            if (
                existing_direction is not None
                and existing_direction is not contract.direction
            ):
                raise ValueError(
                    "one exact dependency edge cannot have opposing contracts"
                )
            directions_by_edge[edge_identity] = contract.direction


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonDependencyGraphResult:
    """Represent all named graph views and explicit direction-check outcomes."""

    views: tuple[PythonDependencyGraphViewResult, ...]
    direction_results: tuple[PythonDependencyDirectionResult, ...]

    def __post_init__(self) -> None:
        """Require exact three-view closure and canonical direction results."""
        if type(self.views) is not tuple or any(
            type(view) is not PythonDependencyGraphViewResult for view in self.views
        ):
            raise TypeError("views must contain PythonDependencyGraphViewResult values")
        expected = tuple(PythonDependencyGraphView)
        if tuple(view.view for view in self.views) != expected:
            raise ValueError("views must contain the exact canonical three-view tuple")
        if type(self.direction_results) is not tuple or any(
            type(result) is not PythonDependencyDirectionResult
            for result in self.direction_results
        ):
            raise TypeError(
                "direction_results must contain PythonDependencyDirectionResult values"
            )
        if self.direction_results != tuple(
            sorted(self.direction_results, key=lambda item: item.sort_key)
        ):
            raise ValueError("direction_results must be in canonical order")
        result_keys = tuple(result.sort_key for result in self.direction_results)
        if len(set(result_keys)) != len(result_keys):
            raise ValueError("direction_results must be unique")
        views_by_identity = {view.view: view for view in self.views}
        contracts_by_identity: dict[str, PythonAcceptedDependencyContract] = {}
        directions_by_edge: dict[
            tuple[PythonDependencyGraphView, str, str], PythonDependencyDirection
        ] = {}
        for result in self.direction_results:
            contract = result.accepted_contract
            if contract is not None:
                existing = contracts_by_identity.get(contract.contract_identity)
                if existing is not None and existing != contract:
                    raise ValueError(
                        "one result contract identity must map to one exact payload"
                    )
                contracts_by_identity[contract.contract_identity] = contract
                contract_edge = (
                    contract.view,
                    contract.source_module,
                    contract.target_module,
                )
                existing_direction = directions_by_edge.get(contract_edge)
                if (
                    existing_direction is not None
                    and existing_direction is not contract.direction
                ):
                    raise ValueError(
                        "one result dependency edge cannot have opposing contracts"
                    )
                directions_by_edge[contract_edge] = contract.direction
            selected = views_by_identity[result.view]
            edge_exists = any(
                edge.source_module == result.source_module
                and edge.target_module == result.target_module
                for edge in selected.edges
            )
            if result.edge is not None and result.edge not in selected.edges:
                raise ValueError(
                    "retained direction edge must belong to its graph view"
                )
            if edge_exists != (result.edge is not None):
                raise ValueError(
                    "an observed direction edge and exact provenance must be retained"
                )
            if (
                result.status
                in {
                    PythonDependencyDirectionStatus.ALLOWED,
                    PythonDependencyDirectionStatus.PROHIBITED,
                }
                and not edge_exists
            ):
                raise ValueError("passing or prohibited direction edge must exist")
            if (
                result.status is PythonDependencyDirectionStatus.EDGE_ABSENT
                and edge_exists
            ):
                raise ValueError("edge-absent direction result requires an absent edge")


class PythonDependencyGraphAnalyzer:
    """Derive named graphs and enforce only exact requested edge contracts."""

    __slots__ = ()

    def execute(
        self, request: PythonDependencyGraphRequest
    ) -> PythonDependencyGraphResult:
        """Derive all three views from exact facts without discovery or mutation."""
        if type(request) is not PythonDependencyGraphRequest:
            raise TypeError("request must be PythonDependencyGraphRequest")
        module_by_name = {module.module_name: module for module in request.modules}
        inspection_by_key = {
            (
                inspection.input_identity,
                inspection.path.as_posix(),
                inspection.source_sha256 or "",
            ): inspection
            for inspection in request.production_facts.modules
            if inspection.facts is not None and inspection.source_sha256 is not None
        }
        lexical = self._edge_provenance(
            tuple(sorted(request.modules, key=lambda item: item.module_name)),
            module_by_name,
            inspection_by_key,
            runtime_unconditional=False,
        )
        runtime = self._edge_provenance(
            tuple(sorted(request.modules, key=lambda item: item.module_name)),
            module_by_name,
            inspection_by_key,
            runtime_unconditional=True,
        )
        views = (
            self._view_result(
                PythonDependencyGraphView.LEXICAL,
                tuple(sorted(module_by_name)),
                lexical,
            ),
            self._view_result(
                PythonDependencyGraphView.RUNTIME_UNCONDITIONAL,
                tuple(sorted(module_by_name)),
                runtime,
            ),
            self._view_result(
                PythonDependencyGraphView.PACKAGE_FACADE_EXCLUDED,
                tuple(
                    sorted(
                        name
                        for name, module in module_by_name.items()
                        if not module.is_package_facade
                    )
                ),
                lexical,
            ),
        )
        results = tuple(
            sorted(
                (
                    self._direction_result(check, views)
                    for check in request.direction_checks
                ),
                key=lambda item: item.sort_key,
            )
        )
        return PythonDependencyGraphResult(views=views, direction_results=results)

    def _edge_provenance(
        self,
        modules: tuple[PythonDependencyModule, ...],
        module_by_name: dict[str, PythonDependencyModule],
        inspection_by_key: dict[tuple[str, str, str], PythonProductionModuleInspection],
        *,
        runtime_unconditional: bool,
    ) -> dict[tuple[str, str], tuple[PythonDependencyEdgeProvenance, ...]]:
        """Collect exact internal edge provenance under one import-selection rule."""
        collected: dict[tuple[str, str], list[PythonDependencyEdgeProvenance]] = {}
        for module in modules:
            inspection_value = inspection_by_key[module.source_key]
            if type(inspection_value) is not PythonProductionModuleInspection:
                raise TypeError("inspection lookup contains an invalid value")
            facts = inspection_value.facts
            if facts is None or inspection_value.source_sha256 is None:
                raise AssertionError("module binding requires successful facts")
            for import_fact in facts.imports:
                if runtime_unconditional and not self._is_runtime_unconditional(
                    import_fact
                ):
                    continue
                for target, resolution in self._targets(
                    module, import_fact, module_by_name
                ):
                    if target == module.module_name:
                        continue
                    provenance = PythonDependencyEdgeProvenance(
                        source=module,
                        import_fact=import_fact,
                        resolution=resolution,
                    )
                    collected.setdefault((module.module_name, target), []).append(
                        provenance
                    )
        return {
            edge: tuple(sorted(items, key=lambda item: item.sort_key))
            for edge, items in collected.items()
        }

    @staticmethod
    def _is_runtime_unconditional(import_fact: PythonProductionImportFact) -> bool:
        """Return whether represented syntax is unconditional during module loading."""
        return not import_fact.contexts and not any(
            owner.kind is PythonProductionScopeKind.CALLABLE
            for owner in import_fact.owners
        )

    def _targets(
        self,
        source: PythonDependencyModule,
        import_fact: PythonProductionImportFact,
        module_by_name: dict[str, PythonDependencyModule],
    ) -> tuple[tuple[str, PythonDependencyResolutionKind], ...]:
        """Resolve exact maintained-module targets using the accepted dual-edge rule."""
        if import_fact.kind is PythonProductionImportKind.IMPORT:
            if import_fact.name in module_by_name:
                return (
                    (
                        import_fact.name,
                        PythonDependencyResolutionKind.DIRECT_IMPORT,
                    ),
                )
            return ()
        base = self._from_base(source, import_fact)
        if base is None:
            return ()
        targets: list[tuple[str, PythonDependencyResolutionKind]] = []
        if base in module_by_name:
            targets.append((base, PythonDependencyResolutionKind.FROM_FACADE))
        candidate = f"{base}.{import_fact.name}" if base else import_fact.name
        if candidate in module_by_name:
            targets.append(
                (
                    candidate,
                    PythonDependencyResolutionKind.FROM_IMPORTED_SUBMODULE,
                )
            )
        return tuple(targets)

    @staticmethod
    def _from_base(
        source: PythonDependencyModule, import_fact: PythonProductionImportFact
    ) -> str | None:
        """Resolve one relative from-import against explicit module/facade identity."""
        if import_fact.relative_level == 0:
            return import_fact.module or ""
        package = (
            source.module_name
            if source.is_package_facade
            else source.module_name.rpartition(".")[0]
        )
        if not package:
            return None
        parts = package.split(".")
        drop = import_fact.relative_level - 1
        if drop >= len(parts):
            return None
        anchor = ".".join(parts[: len(parts) - drop])
        if import_fact.module:
            return f"{anchor}.{import_fact.module}"
        return anchor

    def _view_result(
        self,
        view: PythonDependencyGraphView,
        module_names: tuple[str, ...],
        provenance: dict[tuple[str, str], tuple[PythonDependencyEdgeProvenance, ...]],
    ) -> PythonDependencyGraphViewResult:
        """Construct one canonical view and deterministic SCC partition."""
        included = frozenset(module_names)
        nodes = tuple(
            PythonDependencyGraphNode(view=view, module_name=name)
            for name in module_names
        )
        edges = tuple(
            sorted(
                (
                    PythonDependencyGraphEdge(
                        view=view,
                        source_module=source,
                        target_module=target,
                        provenance=items,
                    )
                    for (source, target), items in provenance.items()
                    if source in included and target in included
                ),
                key=lambda edge: edge.sort_key,
            )
        )
        components = PythonDependencyGraphStructureValidator().components(
            view, module_names, edges
        )
        return PythonDependencyGraphViewResult(
            view=view,
            nodes=nodes,
            edges=edges,
            strongly_connected_components=components,
        )

    @staticmethod
    def _direction_result(
        check: PythonDependencyDirectionCheck,
        views: tuple[PythonDependencyGraphViewResult, ...],
    ) -> PythonDependencyDirectionResult:
        """Evaluate only one requested edge against its exact supplied contract."""
        view = next(result for result in views if result.view is check.view)
        edge = next(
            (
                item
                for item in view.edges
                if item.source_module == check.source_module
                and item.target_module == check.target_module
            ),
            None,
        )
        edge_exists = edge is not None
        contract = check.accepted_contract
        if contract is None:
            status = PythonDependencyDirectionStatus.MISSING_CONTRACT
        elif (
            contract.view is not check.view
            or contract.source_module != check.source_module
            or contract.target_module != check.target_module
        ):
            status = PythonDependencyDirectionStatus.MISMATCHED_CONTRACT
        elif not edge_exists:
            status = PythonDependencyDirectionStatus.EDGE_ABSENT
        elif contract.direction is PythonDependencyDirection.ALLOW:
            status = PythonDependencyDirectionStatus.ALLOWED
        else:
            status = PythonDependencyDirectionStatus.PROHIBITED
        return PythonDependencyDirectionResult(
            view=check.view,
            source_module=check.source_module,
            target_module=check.target_module,
            accepted_contract=contract,
            edge=edge,
            status=status,
        )
