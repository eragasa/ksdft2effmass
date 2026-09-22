"""Closed immutable records for the task-internal public-import foundation report."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias, TypeVar

JsonScalar: TypeAlias = None | bool | int | float | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonRecord: TypeAlias = dict[str, JsonValue]
EnumValue = TypeVar("EnumValue", bound=StrEnum)


class FoundationModelError(ValueError):
    """Report one invalid closed-report value."""


class InputCategory(StrEnum):
    ACCEPTED_INVENTORY = "accepted_inventory"
    AUTHORITY = "authority"
    EXAMPLE = "example"
    HARNESS_CHECK = "harness_check"
    MAINTAINED_TEST = "maintained_test"
    OTHER_FIRST_PARTY_PYTHON = "other_first_party_python"
    PHASE2_VIEW = "phase2_view"
    PRODUCTION_MODULE = "production_module"
    PUBLIC_DOCUMENTATION = "public_documentation"
    PYTHON_RESOURCE = "python_resource"
    TASK_TOOL = "task_tool"


class ImportKind(StrEnum):
    IMPORT = "import"
    FROM_IMPORT = "from_import"


class BindingKind(StrEnum):
    IMPORT = "import"
    FROM_IMPORT = "from_import"
    DEFINITION = "definition"
    ASSIGNMENT = "assignment"


class SupplementalKind(StrEnum):
    PACKAGE_BINDING = "non_star_package_binding"
    DEEP_IMPORT = "deep_non_initializer_import"


class BindingOriginResolution(StrEnum):
    TRANSITIVE_FIRST_PARTY = "transitive_first_party_binding"


class AuthorityState(StrEnum):
    AMBIGUOUS = "ambiguous"
    RAW_UNADJUDICATED = "raw_unadjudicated"
    UNKNOWN = "unknown"


class ProductionAllResolution(StrEnum):
    ABSENT = "absent"
    DYNAMIC = "dynamic"
    LITERAL = "literal"


class DependencyGraphViewKind(StrEnum):
    LEXICAL = "lexical"
    RUNTIME_UNCONDITIONAL = "runtime_unconditional"
    PACKAGE_FACADE_EXCLUDED = "package_facade_excluded"


class RuntimeObservationView(StrEnum):
    FRESH_INTERPRETER_PACKAGE_ATTRIBUTES = "fresh_interpreter_package_attributes"


class RuntimeFailureKind(StrEnum):
    IMPORT_EXCEPTION = "import_exception"


class ClaimBoundary(StrEnum):
    NEUTRAL_STRUCTURE = (
        "neutral explicit-input structure and bounded runtime observations only"
    )
    SUPPORT_EVIDENCE_LIMIT = "importability, __all__, documentation, tests, and consumer use do not establish support"
    NO_NEW_DISPOSITION = "no new support conclusion or compatibility decision is adjudicated; predecessor neutral fields and supplemental unknown states are retained"
    RUNTIME_VIEW_LIMIT = "fresh-interpreter attributes are environment-bounded and not exhaustive language semantics"
    EVIDENCE_LIMIT = "does not establish numerical verification, scientific validation, uncertainty quantification, release, or human acceptance"


class Phase2LineageRole(StrEnum):
    PRODUCTION_FACTS_TASK = "production_facts_task"
    PRODUCTION_FACTS_OWNERSHIP = "production_facts_ownership"
    PRODUCTION_FACTS_IMPLEMENTATION = "production_facts_implementation"
    DEPENDENCY_GRAPH_TASK = "dependency_graph_task"
    DEPENDENCY_GRAPH_OWNERSHIP = "dependency_graph_ownership"
    DEPENDENCY_GRAPH_IMPLEMENTATION = "dependency_graph_implementation"


@dataclass(frozen=True, slots=True)
class InputIdentity:
    category: InputCategory
    path: str
    byte_count: int
    sha256: str

    def __post_init__(self) -> None:
        if type(self.category) is not InputCategory:
            raise TypeError("category must be InputCategory")
        if type(self.path) is not str or not self.path:
            raise ValueError("path must be nonempty built-in text")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in int")
        if (
            type(self.sha256) is not str
            or len(self.sha256) != 64
            or any(character not in "0123456789abcdef" for character in self.sha256)
        ):
            raise ValueError("sha256 must be lowercase hexadecimal")


@dataclass(frozen=True, slots=True)
class AcceptedInventoryIdentity:
    path: str
    byte_count: int
    sha256: str
    accepted_closeout_commit: str

    def __post_init__(self) -> None:
        if type(self.path) is not str or not self.path:
            raise ValueError("path must be nonempty built-in text")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in int")
        if (
            type(self.sha256) is not str
            or len(self.sha256) != 64
            or any(character not in "0123456789abcdef" for character in self.sha256)
        ):
            raise ValueError("sha256 must be lowercase hexadecimal")
        if (
            type(self.accepted_closeout_commit) is not str
            or len(self.accepted_closeout_commit) != 40
            or any(
                character not in "0123456789abcdef"
                for character in self.accepted_closeout_commit
            )
        ):
            raise ValueError("accepted_closeout_commit must be lowercase hexadecimal")


@dataclass(frozen=True, slots=True)
class PredecessorRoute:
    route: str
    package: str
    exported_name: str
    defining_module: str
    defining_symbol: str
    support_status: str
    compatibility_disposition: str

    def __post_init__(self) -> None:
        for name, value in (
            ("route", self.route),
            ("package", self.package),
            ("exported_name", self.exported_name),
            ("defining_module", self.defining_module),
            ("defining_symbol", self.defining_symbol),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if self.route != f"{self.package}.{self.exported_name}":
            raise ValueError("route must agree with package and exported_name")
        if self.support_status != "unknown_no_exact_accepted_support_evidence":
            raise ValueError("support_status must retain the neutral predecessor state")
        if (
            self.compatibility_disposition
            != "unclassified_pending_bounded_option_b_application"
        ):
            raise ValueError(
                "compatibility_disposition must retain the neutral predecessor state"
            )


@dataclass(frozen=True, slots=True)
class PackageBinding:
    kind: BindingKind
    line: int
    local_name: str
    imported_name: str
    origin: str
    defining_origin: str | None
    origin_resolution: BindingOriginResolution | None

    def __post_init__(self) -> None:
        if type(self.kind) is not BindingKind:
            raise TypeError("kind must be BindingKind")
        if type(self.line) is not int or self.line < 1:
            raise ValueError("line must be a positive built-in int")
        for name, value in (
            ("local_name", self.local_name),
            ("imported_name", self.imported_name),
            ("origin", self.origin),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if (self.defining_origin is None) != (self.origin_resolution is None):
            raise ValueError("defining origin and resolution must occur together")
        if self.defining_origin is not None and (
            type(self.defining_origin) is not str or not self.defining_origin
        ):
            raise ValueError("defining_origin must be nonempty built-in text")
        if (
            self.origin_resolution is not None
            and type(self.origin_resolution) is not BindingOriginResolution
        ):
            raise TypeError("origin_resolution has the wrong type")


@dataclass(frozen=True, slots=True)
class PackageSurface:
    package: str
    initializer_path: str
    initializer_byte_count: int
    initializer_sha256: str
    declares_all: bool
    effective_star_names: tuple[str, ...]
    bindings: tuple[PackageBinding, ...]

    def __post_init__(self) -> None:
        if type(self.package) is not str or not self.package:
            raise ValueError("package must be nonempty built-in text")
        if type(self.initializer_path) is not str or not self.initializer_path:
            raise ValueError("initializer_path must be nonempty built-in text")
        if (
            type(self.initializer_byte_count) is not int
            or self.initializer_byte_count < 0
        ):
            raise ValueError(
                "initializer_byte_count must be a nonnegative built-in int"
            )
        if (
            type(self.initializer_sha256) is not str
            or len(self.initializer_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.initializer_sha256
            )
        ):
            raise ValueError("initializer_sha256 must be lowercase hexadecimal")
        if type(self.declares_all) is not bool:
            raise TypeError("declares_all must be bool")
        if type(self.effective_star_names) is not tuple or any(
            type(name) is not str or not name for name in self.effective_star_names
        ):
            raise TypeError("effective_star_names must contain nonempty str values")
        if len(self.effective_star_names) != len(set(self.effective_star_names)):
            raise ValueError("effective_star_names must be unique")
        if type(self.bindings) is not tuple or any(
            type(binding) is not PackageBinding for binding in self.bindings
        ):
            raise TypeError("bindings must contain PackageBinding values")
        binding_names = tuple(binding.local_name for binding in self.bindings)
        if binding_names != tuple(sorted(set(binding_names))):
            raise ValueError("bindings must be local-name-sorted and unique")
        bindings_by_name = {binding.local_name: binding for binding in self.bindings}
        star_names = set(self.effective_star_names)
        for name in self.effective_star_names:
            binding = bindings_by_name.get(name)
            if (
                binding is None
                or binding.defining_origin is None
                or binding.origin_resolution
                is not BindingOriginResolution.TRANSITIVE_FIRST_PARTY
            ):
                raise ValueError("each effective star name requires an origin pair")
        if any(
            binding.local_name not in star_names
            and (
                binding.defining_origin is not None
                or binding.origin_resolution is not None
            )
            for binding in self.bindings
        ):
            raise ValueError("non-star bindings cannot retain origin pairs")


@dataclass(frozen=True, slots=True)
class ImportObservation:
    consumer_path: str
    line: int
    column: int
    import_kind: ImportKind
    imported_module: str
    imported_name: str | None

    def __post_init__(self) -> None:
        if type(self.consumer_path) is not str or not self.consumer_path:
            raise ValueError("consumer_path must be nonempty built-in text")
        if type(self.line) is not int or self.line < 1:
            raise ValueError("line must be a positive built-in int")
        if type(self.column) is not int or self.column < 0:
            raise ValueError("column must be a nonnegative built-in int")
        if type(self.import_kind) is not ImportKind:
            raise TypeError("import_kind must be ImportKind")
        if type(self.imported_module) is not str or not self.imported_module:
            raise ValueError("imported_module must be nonempty built-in text")
        if self.imported_name is not None and (
            type(self.imported_name) is not str or not self.imported_name
        ):
            raise ValueError("imported_name must be nonempty built-in text or None")
        if (self.import_kind is ImportKind.IMPORT) != (self.imported_name is None):
            raise ValueError("import_kind and imported_name disagree")


@dataclass(frozen=True, slots=True)
class DocumentationCitation:
    path: str
    line: int
    column: int
    route_text: str

    def __post_init__(self) -> None:
        for name, value in (("path", self.path), ("route_text", self.route_text)):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if type(self.line) is not int or self.line < 1:
            raise ValueError("line must be a positive built-in int")
        if type(self.column) is not int or self.column < 0:
            raise ValueError("column must be a nonnegative built-in int")


@dataclass(frozen=True, slots=True)
class AuthorityCitation:
    path: str
    line: int
    column: int
    matched_term: str
    authority_state: AuthorityState

    def __post_init__(self) -> None:
        for name, value in (("path", self.path), ("matched_term", self.matched_term)):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if type(self.line) is not int or self.line < 1:
            raise ValueError("line must be a positive built-in int")
        if type(self.column) is not int or self.column < 0:
            raise ValueError("column must be a nonnegative built-in int")
        if type(self.authority_state) is not AuthorityState:
            raise TypeError("authority_state must be AuthorityState")


@dataclass(frozen=True, slots=True)
class Phase2LineageInput:
    role: Phase2LineageRole
    path: str
    byte_count: int
    sha256: str

    def __post_init__(self) -> None:
        if type(self.role) is not Phase2LineageRole:
            raise TypeError("role must be Phase2LineageRole")
        if type(self.path) is not str or not self.path:
            raise ValueError("path must be nonempty built-in text")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in int")
        if (
            type(self.sha256) is not str
            or len(self.sha256) != 64
            or any(character not in "0123456789abcdef" for character in self.sha256)
        ):
            raise ValueError("sha256 must be lowercase hexadecimal")


@dataclass(frozen=True, slots=True)
class ProductionFactOutput:
    module_name: str
    path: str
    source_sha256: str
    source_byte_count: int
    class_count: int
    callable_count: int
    import_count: int
    call_count: int
    all_syntax_count: int
    effective_all_resolution: ProductionAllResolution
    effective_all_names: tuple[str, ...] | None

    def __post_init__(self) -> None:
        for name, value in (("module_name", self.module_name), ("path", self.path)):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if (
            type(self.source_sha256) is not str
            or len(self.source_sha256) != 64
            or any(
                character not in "0123456789abcdef" for character in self.source_sha256
            )
        ):
            raise ValueError("source_sha256 must be lowercase hexadecimal")
        for count_name, count_value in (
            ("source_byte_count", self.source_byte_count),
            ("class_count", self.class_count),
            ("callable_count", self.callable_count),
            ("import_count", self.import_count),
            ("call_count", self.call_count),
            ("all_syntax_count", self.all_syntax_count),
        ):
            if type(count_value) is not int or count_value < 0:
                raise ValueError(f"{count_name} must be a nonnegative built-in int")
        if type(self.effective_all_resolution) is not ProductionAllResolution:
            raise TypeError("effective_all_resolution has the wrong type")
        if (self.effective_all_resolution is ProductionAllResolution.LITERAL) != (
            self.effective_all_names is not None
        ):
            raise ValueError("literal resolution must exactly retain effective names")
        if self.effective_all_names is not None:
            if type(self.effective_all_names) is not tuple or any(
                type(name) is not str or not name for name in self.effective_all_names
            ):
                raise TypeError(
                    "effective_all_names must contain nonempty built-in str values"
                )
            if len(self.effective_all_names) != len(set(self.effective_all_names)):
                raise ValueError("effective_all_names must be unique")


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source_module: str
    target_module: str

    def __post_init__(self) -> None:
        for name, value in (
            ("source_module", self.source_module),
            ("target_module", self.target_module),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")


@dataclass(frozen=True, slots=True)
class DependencyGraphView:
    view: DependencyGraphViewKind
    node_names: tuple[str, ...]
    edges: tuple[DependencyEdge, ...]
    strongly_connected_components: tuple[tuple[str, ...], ...]
    source_identities: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.view) is not DependencyGraphViewKind:
            raise TypeError("view must be DependencyGraphViewKind")
        if type(self.node_names) is not tuple or any(
            type(name) is not str or not name for name in self.node_names
        ):
            raise TypeError("node_names must contain nonempty built-in str values")
        if self.node_names != tuple(sorted(set(self.node_names))):
            raise ValueError("node_names must be sorted and unique")
        if type(self.edges) is not tuple or any(
            type(edge) is not DependencyEdge for edge in self.edges
        ):
            raise TypeError("edges must contain DependencyEdge values")
        edge_keys = tuple(
            (edge.source_module, edge.target_module) for edge in self.edges
        )
        if edge_keys != tuple(sorted(set(edge_keys))):
            raise ValueError("edges must be sorted with unique endpoints")
        if type(self.strongly_connected_components) is not tuple:
            raise TypeError("strongly_connected_components must be tuple")
        for component in self.strongly_connected_components:
            if type(component) is not tuple or any(
                type(name) is not str or not name for name in component
            ):
                raise TypeError("represented components must contain text tuples")
            if component != tuple(sorted(set(component))) or not component:
                raise ValueError("each represented component must be sorted and unique")
        if self.strongly_connected_components != tuple(
            sorted(self.strongly_connected_components)
        ):
            raise ValueError("represented components must be canonically ordered")
        if type(self.source_identities) is not tuple or any(
            type(identity) is not str
            or len(identity) != 64
            or any(character not in "0123456789abcdef" for character in identity)
            for identity in self.source_identities
        ):
            raise TypeError("source_identities must contain SHA-256 text")
        if self.source_identities != tuple(sorted(set(self.source_identities))):
            raise ValueError("source_identities must be sorted and unique")


@dataclass(frozen=True, slots=True)
class RuntimeDistribution:
    name: str
    version: str

    def __post_init__(self) -> None:
        for name, value in (("name", self.name), ("version", self.version)):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")


@dataclass(frozen=True, slots=True)
class RuntimeEnvironment:
    executable_byte_count: int
    executable_sha256: str
    implementation: str
    version: str
    distributions: tuple[RuntimeDistribution, ...]
    source_root: str
    environment_sha256: str

    def __post_init__(self) -> None:
        if (
            type(self.executable_byte_count) is not int
            or self.executable_byte_count < 0
        ):
            raise ValueError("executable_byte_count must be a nonnegative built-in int")
        for name, value in (
            ("executable_sha256", self.executable_sha256),
            ("environment_sha256", self.environment_sha256),
        ):
            if (
                type(value) is not str
                or len(value) != 64
                or any(character not in "0123456789abcdef" for character in value)
            ):
                raise ValueError(f"{name} must be lowercase hexadecimal")
        for name, value in (
            ("implementation", self.implementation),
            ("version", self.version),
            ("source_root", self.source_root),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if type(self.distributions) is not tuple or any(
            type(item) is not RuntimeDistribution for item in self.distributions
        ):
            raise TypeError("distributions must contain RuntimeDistribution values")
        keys = tuple((item.name, item.version) for item in self.distributions)
        if keys != tuple(sorted(set(keys))):
            raise ValueError("runtime distributions must be sorted and unique")
        if (
            RuntimeEnvironmentIdentitySerializer().execute(self)
            != self.environment_sha256
        ):
            raise ValueError("runtime environment identity disagrees with its fields")


@dataclass(frozen=True, slots=True)
class RuntimeAttribute:
    name: str
    value_type: str
    defining_module: str | None

    def __post_init__(self) -> None:
        for name, value in (("name", self.name), ("value_type", self.value_type)):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if self.defining_module is not None and (
            type(self.defining_module) is not str or not self.defining_module
        ):
            raise ValueError("defining_module must be nonempty built-in text or None")


@dataclass(frozen=True, slots=True)
class RuntimeLoadedFile:
    module_name: str
    path: str
    byte_count: int
    sha256: str

    def __post_init__(self) -> None:
        for name, value in (("module_name", self.module_name), ("path", self.path)):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in int")
        if (
            type(self.sha256) is not str
            or len(self.sha256) != 64
            or any(character not in "0123456789abcdef" for character in self.sha256)
        ):
            raise ValueError("sha256 must be lowercase hexadecimal")


@dataclass(frozen=True, slots=True)
class RuntimeSuccess:
    attributes: tuple[RuntimeAttribute, ...]
    loaded_files: tuple[RuntimeLoadedFile, ...]

    def __post_init__(self) -> None:
        if type(self.attributes) is not tuple or any(
            type(item) is not RuntimeAttribute for item in self.attributes
        ):
            raise TypeError("attributes must contain RuntimeAttribute values")
        attribute_names = tuple(item.name for item in self.attributes)
        if attribute_names != tuple(sorted(set(attribute_names))):
            raise ValueError("runtime attributes must be name-sorted and unique")
        if type(self.loaded_files) is not tuple or any(
            type(item) is not RuntimeLoadedFile for item in self.loaded_files
        ):
            raise TypeError("loaded_files must contain RuntimeLoadedFile values")
        keys = tuple((item.module_name, item.path) for item in self.loaded_files)
        if keys != tuple(sorted(set(keys))):
            raise ValueError("runtime loaded files must be key-sorted and unique")


@dataclass(frozen=True, slots=True)
class RuntimeFailure:
    failure_kind: RuntimeFailureKind
    exception_type: str
    message: str
    loaded_files: tuple[RuntimeLoadedFile, ...]

    def __post_init__(self) -> None:
        if type(self.failure_kind) is not RuntimeFailureKind:
            raise TypeError("failure_kind must be RuntimeFailureKind")
        for name, value in (
            ("exception_type", self.exception_type),
            ("message", self.message),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if type(self.loaded_files) is not tuple or any(
            type(item) is not RuntimeLoadedFile for item in self.loaded_files
        ):
            raise TypeError("loaded_files must contain RuntimeLoadedFile values")
        keys = tuple((item.module_name, item.path) for item in self.loaded_files)
        if keys != tuple(sorted(set(keys))):
            raise ValueError("runtime loaded files must be key-sorted and unique")


RuntimeOutcome: TypeAlias = RuntimeSuccess | RuntimeFailure


@dataclass(frozen=True, slots=True)
class RuntimeObservation:
    package: str
    view: RuntimeObservationView
    environment_sha256: str
    observation: RuntimeOutcome

    def __post_init__(self) -> None:
        if type(self.package) is not str or not self.package:
            raise ValueError("package must be nonempty built-in text")
        if type(self.view) is not RuntimeObservationView:
            raise TypeError("view must be RuntimeObservationView")
        if (
            type(self.environment_sha256) is not str
            or len(self.environment_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.environment_sha256
            )
        ):
            raise ValueError("environment_sha256 must be lowercase hexadecimal")
        if type(self.observation) not in {RuntimeSuccess, RuntimeFailure}:
            raise TypeError("observation has an unsupported outcome type")


@dataclass(frozen=True, slots=True)
class PackageBindingCandidate:
    candidate_key: str
    candidate_kind: SupplementalKind
    support_status: str
    package: str
    binding: PackageBinding

    def __post_init__(self) -> None:
        if type(self.candidate_key) is not str or not self.candidate_key:
            raise ValueError("candidate_key must be nonempty built-in text")
        if self.candidate_kind is not SupplementalKind.PACKAGE_BINDING:
            raise ValueError("candidate_kind must identify a package binding")
        if self.support_status != "unknown":
            raise ValueError("support_status must retain the neutral state")
        if type(self.package) is not str or not self.package:
            raise ValueError("package must be nonempty built-in text")
        if type(self.binding) is not PackageBinding:
            raise TypeError("binding must be PackageBinding")


@dataclass(frozen=True, slots=True)
class DeepImportCandidate:
    candidate_key: str
    candidate_kind: SupplementalKind
    support_status: str
    consumer_path: str
    imported_module: str
    imported_name: str | None

    def __post_init__(self) -> None:
        if type(self.candidate_key) is not str or not self.candidate_key:
            raise ValueError("candidate_key must be nonempty built-in text")
        if self.candidate_kind is not SupplementalKind.DEEP_IMPORT:
            raise ValueError("candidate_kind must identify a deep import")
        if self.support_status != "unknown":
            raise ValueError("support_status must retain the neutral state")
        for name, value in (
            ("consumer_path", self.consumer_path),
            ("imported_module", self.imported_module),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty built-in text")
        if self.imported_name is not None and (
            type(self.imported_name) is not str or not self.imported_name
        ):
            raise ValueError("imported_name must be nonempty built-in text or None")


SupplementalCandidate: TypeAlias = PackageBindingCandidate | DeepImportCandidate


@dataclass(frozen=True, slots=True)
class FoundationSummary:
    input_count: int
    predecessor_route_count: int
    package_surface_count: int
    zero_route_surface_count: int
    consumer_import_count: int
    deep_non_initializer_module_import_count: int
    documentation_citation_count: int
    authority_citation_count: int
    phase2_lineage_input_count: int
    production_fact_output_count: int
    dependency_graph_view_count: int
    supplemental_candidate_count: int
    runtime_package_observation_count: int

    def __post_init__(self) -> None:
        for name, value in (
            ("input_count", self.input_count),
            ("predecessor_route_count", self.predecessor_route_count),
            ("package_surface_count", self.package_surface_count),
            ("zero_route_surface_count", self.zero_route_surface_count),
            ("consumer_import_count", self.consumer_import_count),
            (
                "deep_non_initializer_module_import_count",
                self.deep_non_initializer_module_import_count,
            ),
            ("documentation_citation_count", self.documentation_citation_count),
            ("authority_citation_count", self.authority_citation_count),
            ("phase2_lineage_input_count", self.phase2_lineage_input_count),
            ("production_fact_output_count", self.production_fact_output_count),
            ("dependency_graph_view_count", self.dependency_graph_view_count),
            ("supplemental_candidate_count", self.supplemental_candidate_count),
            (
                "runtime_package_observation_count",
                self.runtime_package_observation_count,
            ),
        ):
            if type(value) is not int or value < 0:
                raise ValueError(f"{name} must be a nonnegative built-in int")


@dataclass(frozen=True, slots=True)
class PublicImportFoundation:
    schema_version: int
    subject_identity: str
    subject_version: str
    input_manifest_schema_version: int
    inputs: tuple[InputIdentity, ...]
    accepted_inventory: AcceptedInventoryIdentity
    predecessor_routes: tuple[PredecessorRoute, ...]
    package_surfaces: tuple[PackageSurface, ...]
    zero_route_surfaces: tuple[str, ...]
    consumer_imports: tuple[ImportObservation, ...]
    deep_imports: tuple[ImportObservation, ...]
    documentation_citations: tuple[DocumentationCitation, ...]
    authority_citations: tuple[AuthorityCitation, ...]
    phase2_lineage_inputs: tuple[Phase2LineageInput, ...]
    production_fact_outputs: tuple[ProductionFactOutput, ...]
    dependency_graph_views: tuple[DependencyGraphView, ...]
    runtime_environment: RuntimeEnvironment
    runtime_observations: tuple[RuntimeObservation, ...]
    supplemental_candidates: tuple[SupplementalCandidate, ...]
    claim_boundaries: tuple[ClaimBoundary, ...]
    summary: FoundationSummary

    def __post_init__(self) -> None:
        if (
            self.schema_version,
            self.subject_identity,
            self.subject_version,
            self.input_manifest_schema_version,
        ) != (1, "ksdft2effmass.python.public-import-foundation", "1", 1):
            raise ValueError("foundation identity is unsupported")
        if type(self.inputs) is not tuple or any(
            type(item) is not InputIdentity for item in self.inputs
        ):
            raise TypeError("inputs must contain InputIdentity values")
        input_keys = tuple((item.category.value, item.path) for item in self.inputs)
        if input_keys != tuple(sorted(input_keys)) or len(
            {item.path for item in self.inputs}
        ) != len(self.inputs):
            raise ValueError("inputs must be category/path-sorted with unique paths")
        if type(self.accepted_inventory) is not AcceptedInventoryIdentity:
            raise TypeError("accepted_inventory has the wrong type")
        if type(self.predecessor_routes) is not tuple or any(
            type(item) is not PredecessorRoute for item in self.predecessor_routes
        ):
            raise TypeError("predecessor_routes must contain PredecessorRoute values")
        predecessor_keys = tuple(item.route for item in self.predecessor_routes)
        if predecessor_keys != tuple(sorted(set(predecessor_keys))):
            raise ValueError("predecessor_routes must be route-sorted and unique")
        if type(self.package_surfaces) is not tuple or any(
            type(item) is not PackageSurface for item in self.package_surfaces
        ):
            raise TypeError("package_surfaces must contain PackageSurface values")
        package_keys = tuple(item.package for item in self.package_surfaces)
        if package_keys != tuple(sorted(set(package_keys))):
            raise ValueError("package_surfaces must be package-sorted and unique")
        if type(self.zero_route_surfaces) is not tuple or any(
            type(item) is not str or not item for item in self.zero_route_surfaces
        ):
            raise TypeError("zero_route_surfaces must contain nonempty text")
        if self.zero_route_surfaces != tuple(sorted(set(self.zero_route_surfaces))):
            raise ValueError("zero_route_surfaces must be sorted and unique")
        for name, values in (
            ("consumer_imports", self.consumer_imports),
            ("deep_imports", self.deep_imports),
        ):
            if type(values) is not tuple or any(
                type(item) is not ImportObservation for item in values
            ):
                raise TypeError(f"{name} must contain ImportObservation values")
            keys = tuple(
                (
                    item.consumer_path,
                    item.line,
                    item.column,
                    item.import_kind.value,
                    item.imported_module,
                    item.imported_name or "",
                )
                for item in values
            )
            if keys != tuple(sorted(set(keys))):
                raise ValueError(f"{name} must be canonically sorted and unique")
        if type(self.documentation_citations) is not tuple or any(
            type(item) is not DocumentationCitation
            for item in self.documentation_citations
        ):
            raise TypeError(
                "documentation_citations must contain DocumentationCitation values"
            )
        documentation_keys = tuple(
            (item.path, item.line, item.column, item.route_text)
            for item in self.documentation_citations
        )
        if documentation_keys != tuple(sorted(set(documentation_keys))):
            raise ValueError(
                "documentation_citations must be canonically sorted and unique"
            )
        if type(self.authority_citations) is not tuple or any(
            type(item) is not AuthorityCitation for item in self.authority_citations
        ):
            raise TypeError("authority_citations must contain AuthorityCitation values")
        authority_keys = tuple(
            (item.path, item.line, item.column, item.matched_term)
            for item in self.authority_citations
        )
        if authority_keys != tuple(sorted(set(authority_keys))):
            raise ValueError(
                "authority_citations must be canonically sorted and unique"
            )
        if type(self.phase2_lineage_inputs) is not tuple or any(
            type(item) is not Phase2LineageInput for item in self.phase2_lineage_inputs
        ):
            raise TypeError(
                "phase2_lineage_inputs must contain Phase2LineageInput values"
            )
        if tuple(item.role for item in self.phase2_lineage_inputs) != tuple(
            Phase2LineageRole
        ):
            raise ValueError("phase2_lineage_inputs must have exact canonical roles")
        if type(self.production_fact_outputs) is not tuple or any(
            type(item) is not ProductionFactOutput
            for item in self.production_fact_outputs
        ):
            raise TypeError(
                "production_fact_outputs must contain ProductionFactOutput values"
            )
        production_keys = tuple(
            item.module_name for item in self.production_fact_outputs
        )
        if production_keys != tuple(sorted(set(production_keys))):
            raise ValueError(
                "production_fact_outputs must be module-name-sorted and unique"
            )
        if type(self.dependency_graph_views) is not tuple or any(
            type(item) is not DependencyGraphView
            for item in self.dependency_graph_views
        ):
            raise TypeError(
                "dependency_graph_views must contain DependencyGraphView values"
            )
        if tuple(item.view for item in self.dependency_graph_views) != tuple(
            DependencyGraphViewKind
        ):
            raise ValueError("dependency_graph_views must have exact canonical views")
        if type(self.runtime_environment) is not RuntimeEnvironment:
            raise TypeError("runtime_environment has the wrong type")
        if type(self.runtime_observations) is not tuple or any(
            type(item) is not RuntimeObservation for item in self.runtime_observations
        ):
            raise TypeError(
                "runtime_observations must contain RuntimeObservation values"
            )
        runtime_keys = tuple(item.package for item in self.runtime_observations)
        if runtime_keys != tuple(sorted(set(runtime_keys))):
            raise ValueError("runtime_observations must be package-sorted and unique")
        if type(self.supplemental_candidates) is not tuple or any(
            type(item) not in {PackageBindingCandidate, DeepImportCandidate}
            for item in self.supplemental_candidates
        ):
            raise TypeError("supplemental_candidates contain an unsupported type")
        candidate_keys = tuple(
            item.candidate_key for item in self.supplemental_candidates
        )
        if candidate_keys != tuple(sorted(set(candidate_keys))):
            raise ValueError(
                "supplemental_candidates must be candidate-key-sorted and unique"
            )
        if type(self.claim_boundaries) is not tuple or any(
            type(item) is not ClaimBoundary for item in self.claim_boundaries
        ):
            raise TypeError("claim_boundaries must contain ClaimBoundary values")
        if self.claim_boundaries != tuple(ClaimBoundary):
            raise ValueError("claim_boundaries must have exact canonical claims")
        if type(self.summary) is not FoundationSummary:
            raise TypeError("summary has the wrong type")
        if (
            len(self.predecessor_routes),
            len(self.package_surfaces),
            len(self.zero_route_surfaces),
            len(self.phase2_lineage_inputs),
            len(self.production_fact_outputs),
            len(self.dependency_graph_views),
            len(self.runtime_observations),
        ) != (985, 35, 10, 6, 216, 3, 35):
            raise ValueError("fixed version-one collection cardinalities disagree")


class FoundationJsonCodec:
    """Own strict decoding and canonical encoding for task-internal JSON."""

    __slots__ = ()

    def decode(self, payload: bytes) -> JsonValue:
        """Decode UTF-8 JSON while rejecting duplicate object keys."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise FoundationModelError("JSON input is not UTF-8") from exc
        if text.startswith("\ufeff"):
            raise FoundationModelError("JSON input must not contain a UTF-8 BOM")
        try:
            value: JsonValue = json.loads(text, object_pairs_hook=self._pairs)
        except json.JSONDecodeError as exc:
            raise FoundationModelError(str(exc)) from exc
        return value

    def encode(self, value: JsonValue) -> bytes:
        """Encode canonical key-sorted UTF-8 JSON plus one LF."""
        try:
            text = json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        except (TypeError, ValueError, UnicodeError) as exc:
            raise FoundationModelError(str(exc)) from exc
        return (text + "\n").encode("utf-8")

    @staticmethod
    def _pairs(pairs: list[tuple[str, JsonValue]]) -> JsonRecord:
        record: JsonRecord = {}
        for key, value in pairs:
            if key in record:
                raise FoundationModelError(f"duplicate JSON key: {key}")
            record[key] = value
        return record


class RuntimeEnvironmentIdentitySerializer:
    """Serialize one runtime environment into its canonical content identity."""

    __slots__ = ()

    def execute(self, environment: RuntimeEnvironment) -> str:
        """Return the SHA-256 of the canonical represented environment fields."""
        if type(environment) is not RuntimeEnvironment:
            raise TypeError("environment must be RuntimeEnvironment")
        payload: JsonRecord = {
            "distributions": [
                [item.name, item.version] for item in environment.distributions
            ],
            "executable_byte_count": environment.executable_byte_count,
            "executable_sha256": environment.executable_sha256,
            "implementation": environment.implementation,
            "source_root": environment.source_root,
            "version": environment.version,
        }
        encoded = (
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            ).encode()
            + b"\n"
        )
        return hashlib.sha256(encoded).hexdigest()


class ClosedFoundationSerializer:
    """Serialize only validated closed immutable foundation records."""

    __slots__ = ()

    def execute(self, report: PublicImportFoundation) -> JsonRecord:
        """Return the canonical JSON representation of one closed report."""
        if type(report) is not PublicImportFoundation:
            raise TypeError("report must be PublicImportFoundation")
        PublicImportFoundationCrossViewValidator().execute(report)
        return {
            "accepted_inventory": {
                "accepted_closeout_commit": report.accepted_inventory.accepted_closeout_commit,
                "byte_count": report.accepted_inventory.byte_count,
                "path": report.accepted_inventory.path,
                "sha256": report.accepted_inventory.sha256,
            },
            "authority_citations": [
                {
                    "authority_state": item.authority_state.value,
                    "column": item.column,
                    "line": item.line,
                    "matched_term": item.matched_term,
                    "path": item.path,
                }
                for item in report.authority_citations
            ],
            "claim_boundaries": [item.value for item in report.claim_boundaries],
            "consumer_imports": [
                self._import(item) for item in report.consumer_imports
            ],
            "deep_non_initializer_module_imports": [
                self._import(item) for item in report.deep_imports
            ],
            "dependency_graph_views": [
                {
                    "edges": [
                        {
                            "source_module": edge.source_module,
                            "target_module": edge.target_module,
                        }
                        for edge in view.edges
                    ],
                    "node_names": list(view.node_names),
                    "source_identities": list(view.source_identities),
                    "strongly_connected_components": [
                        list(component)
                        for component in view.strongly_connected_components
                    ],
                    "view": view.view.value,
                }
                for view in report.dependency_graph_views
            ],
            "documentation_citations": [
                {
                    "column": item.column,
                    "line": item.line,
                    "path": item.path,
                    "route_text": item.route_text,
                }
                for item in report.documentation_citations
            ],
            "input_manifest": {
                "entries": [
                    {
                        "byte_count": item.byte_count,
                        "category": item.category.value,
                        "path": item.path,
                        "sha256": item.sha256,
                    }
                    for item in report.inputs
                ],
                "schema_version": report.input_manifest_schema_version,
                "subject_identity": "ksdft2effmass.python.public-import-foundation-inputs",
                "subject_version": "1",
            },
            "package_runtime_observations": [
                self._runtime(item) for item in report.runtime_observations
            ],
            "package_surfaces": [
                {
                    "bindings": [self._binding(binding) for binding in item.bindings],
                    "declares_all": item.declares_all,
                    "effective_star_names": list(item.effective_star_names),
                    "initializer_byte_count": item.initializer_byte_count,
                    "initializer_path": item.initializer_path,
                    "initializer_sha256": item.initializer_sha256,
                    "package": item.package,
                }
                for item in report.package_surfaces
            ],
            "phase2_lineage_inputs": [
                {
                    "byte_count": item.byte_count,
                    "path": item.path,
                    "role": item.role.value,
                    "sha256": item.sha256,
                }
                for item in report.phase2_lineage_inputs
            ],
            "predecessor_routes": [
                {
                    "compatibility_disposition": item.compatibility_disposition,
                    "defining_module": item.defining_module,
                    "defining_symbol": item.defining_symbol,
                    "exported_name": item.exported_name,
                    "package": item.package,
                    "route": item.route,
                    "support_status": item.support_status,
                }
                for item in report.predecessor_routes
            ],
            "production_fact_outputs": [
                {
                    "all_syntax_count": item.all_syntax_count,
                    "call_count": item.call_count,
                    "callable_count": item.callable_count,
                    "class_count": item.class_count,
                    "effective_all_names": None
                    if item.effective_all_names is None
                    else list(item.effective_all_names),
                    "effective_all_resolution": item.effective_all_resolution.value,
                    "import_count": item.import_count,
                    "module_name": item.module_name,
                    "path": item.path,
                    "source_byte_count": item.source_byte_count,
                    "source_sha256": item.source_sha256,
                }
                for item in report.production_fact_outputs
            ],
            "runtime_environment": {
                "distributions": [
                    [item.name, item.version]
                    for item in report.runtime_environment.distributions
                ],
                "environment_sha256": report.runtime_environment.environment_sha256,
                "executable_byte_count": report.runtime_environment.executable_byte_count,
                "executable_sha256": report.runtime_environment.executable_sha256,
                "implementation": report.runtime_environment.implementation,
                "source_root": report.runtime_environment.source_root,
                "version": report.runtime_environment.version,
            },
            "schema_version": report.schema_version,
            "subject_identity": report.subject_identity,
            "subject_version": report.subject_version,
            "summary": self._summary(report.summary),
            "supplemental_candidates": [
                self._supplemental(item) for item in report.supplemental_candidates
            ],
            "zero_route_surfaces": list(report.zero_route_surfaces),
        }

    @staticmethod
    def _binding(item: PackageBinding) -> JsonRecord:
        row: JsonRecord = {
            "imported_name": item.imported_name,
            "kind": item.kind.value,
            "line": item.line,
            "local_name": item.local_name,
            "origin": item.origin,
        }
        if item.defining_origin is not None and item.origin_resolution is not None:
            row["defining_origin"] = item.defining_origin
            row["origin_resolution"] = item.origin_resolution.value
        return row

    @staticmethod
    def _import(item: ImportObservation) -> JsonRecord:
        return {
            "column": item.column,
            "consumer_path": item.consumer_path,
            "import_kind": item.import_kind.value,
            "imported_module": item.imported_module,
            "imported_name": item.imported_name,
            "line": item.line,
        }

    @staticmethod
    def _loaded(item: RuntimeLoadedFile) -> JsonRecord:
        return {
            "byte_count": item.byte_count,
            "module_name": item.module_name,
            "path": item.path,
            "sha256": item.sha256,
        }

    def _runtime(self, item: RuntimeObservation) -> JsonRecord:
        if isinstance(item.observation, RuntimeSuccess):
            observation: JsonRecord = {
                "attributes": [
                    {
                        "defining_module": attribute.defining_module,
                        "name": attribute.name,
                        "value_type": attribute.value_type,
                    }
                    for attribute in item.observation.attributes
                ],
                "loaded_files": [
                    self._loaded(loaded) for loaded in item.observation.loaded_files
                ],
                "status": "success",
            }
        else:
            observation = {
                "exception_type": item.observation.exception_type,
                "failure_kind": item.observation.failure_kind.value,
                "loaded_files": [
                    self._loaded(loaded) for loaded in item.observation.loaded_files
                ],
                "message": item.observation.message,
                "status": "failure",
            }
        return {
            "environment_sha256": item.environment_sha256,
            "observation": observation,
            "package": item.package,
            "view": item.view.value,
        }

    def _supplemental(self, item: SupplementalCandidate) -> JsonRecord:
        if isinstance(item, PackageBindingCandidate):
            evidence: JsonRecord = {
                "binding": self._binding(item.binding),
                "package": item.package,
            }
        else:
            evidence = {
                "consumer_path": item.consumer_path,
                "imported_module": item.imported_module,
                "imported_name": item.imported_name,
            }
        return {
            "candidate_key": item.candidate_key,
            "candidate_kind": item.candidate_kind.value,
            "evidence": evidence,
            "support_status": item.support_status,
        }

    @staticmethod
    def _summary(item: FoundationSummary) -> JsonRecord:
        return {
            "authority_citation_count": item.authority_citation_count,
            "consumer_import_count": item.consumer_import_count,
            "deep_non_initializer_module_import_count": item.deep_non_initializer_module_import_count,
            "dependency_graph_view_count": item.dependency_graph_view_count,
            "documentation_citation_count": item.documentation_citation_count,
            "input_count": item.input_count,
            "package_surface_count": item.package_surface_count,
            "phase2_lineage_input_count": item.phase2_lineage_input_count,
            "predecessor_route_count": item.predecessor_route_count,
            "production_fact_output_count": item.production_fact_output_count,
            "runtime_package_observation_count": item.runtime_package_observation_count,
            "supplemental_candidate_count": item.supplemental_candidate_count,
            "zero_route_surface_count": item.zero_route_surface_count,
        }


class ClosedFoundationParser:
    """Convert one recursive JSON representation into closed immutable records."""

    __slots__ = ()

    def execute(self, value: JsonValue) -> PublicImportFoundation:
        root = self._record(value, "foundation")
        self._keys(
            root,
            {
                "accepted_inventory",
                "authority_citations",
                "claim_boundaries",
                "consumer_imports",
                "deep_non_initializer_module_imports",
                "dependency_graph_views",
                "documentation_citations",
                "input_manifest",
                "package_runtime_observations",
                "package_surfaces",
                "phase2_lineage_inputs",
                "predecessor_routes",
                "production_fact_outputs",
                "runtime_environment",
                "schema_version",
                "subject_identity",
                "subject_version",
                "summary",
                "supplemental_candidates",
                "zero_route_surfaces",
            },
            "foundation",
        )
        manifest = self._record(root["input_manifest"], "input_manifest")
        self._keys(
            manifest,
            {"entries", "schema_version", "subject_identity", "subject_version"},
            "input_manifest",
        )
        if (
            manifest["schema_version"] != 1
            or manifest["subject_identity"]
            != "ksdft2effmass.python.public-import-foundation-inputs"
            or manifest["subject_version"] != "1"
        ):
            raise FoundationModelError("input manifest identity is unsupported")
        inputs = tuple(
            self._input(item, index)
            for index, item in enumerate(self._array(manifest["entries"], "entries"))
        )
        accepted = self._accepted(root["accepted_inventory"])
        routes = tuple(
            self._route(item, index)
            for index, item in enumerate(
                self._array(root["predecessor_routes"], "routes")
            )
        )
        packages = tuple(
            self._package(item, index)
            for index, item in enumerate(
                self._array(root["package_surfaces"], "packages")
            )
        )
        consumers = tuple(
            self._import(item, index, "consumer")
            for index, item in enumerate(
                self._array(root["consumer_imports"], "consumers")
            )
        )
        deep = tuple(
            self._import(item, index, "deep")
            for index, item in enumerate(
                self._array(root["deep_non_initializer_module_imports"], "deep")
            )
        )
        docs = tuple(
            self._documentation(item, index)
            for index, item in enumerate(
                self._array(root["documentation_citations"], "documentation")
            )
        )
        authority = tuple(
            self._authority(item, index)
            for index, item in enumerate(
                self._array(root["authority_citations"], "authority")
            )
        )
        lineage = tuple(
            self._lineage(item, index)
            for index, item in enumerate(
                self._array(root["phase2_lineage_inputs"], "lineage")
            )
        )
        production = tuple(
            self._production(item, index)
            for index, item in enumerate(
                self._array(root["production_fact_outputs"], "production")
            )
        )
        graphs = tuple(
            self._graph(item, index)
            for index, item in enumerate(
                self._array(root["dependency_graph_views"], "graphs")
            )
        )
        runtime_environment = self._runtime_environment(root["runtime_environment"])
        runtime = tuple(
            self._runtime_observation(item, index)
            for index, item in enumerate(
                self._array(root["package_runtime_observations"], "runtime")
            )
        )
        supplemental = tuple(
            self._supplemental(item, index)
            for index, item in enumerate(
                self._array(root["supplemental_candidates"], "supplemental")
            )
        )
        claims = tuple(
            self._enum(ClaimBoundary, item, "claim")
            for item in self._array(root["claim_boundaries"], "claims")
        )
        zero = tuple(
            self._text(item, "zero route")
            for item in self._array(root["zero_route_surfaces"], "zero routes")
        )
        summary = self._summary(root["summary"])
        report = PublicImportFoundation(
            schema_version=self._integer(root["schema_version"], "schema_version"),
            subject_identity=self._text(root["subject_identity"], "subject_identity"),
            subject_version=self._text(root["subject_version"], "subject_version"),
            input_manifest_schema_version=self._integer(
                manifest["schema_version"], "manifest schema"
            ),
            inputs=inputs,
            accepted_inventory=accepted,
            predecessor_routes=routes,
            package_surfaces=packages,
            zero_route_surfaces=zero,
            consumer_imports=consumers,
            deep_imports=deep,
            documentation_citations=docs,
            authority_citations=authority,
            phase2_lineage_inputs=lineage,
            production_fact_outputs=production,
            dependency_graph_views=graphs,
            runtime_environment=runtime_environment,
            runtime_observations=runtime,
            supplemental_candidates=supplemental,
            claim_boundaries=claims,
            summary=summary,
        )
        self._cross_validate(report)
        return report

    def _input(self, value: JsonValue, index: int) -> InputIdentity:
        row = self._closed(
            value, {"byte_count", "category", "path", "sha256"}, f"input[{index}]"
        )
        return InputIdentity(
            self._enum(InputCategory, row["category"], "category"),
            self._text(row["path"], "path"),
            self._nonnegative(row["byte_count"], "byte_count"),
            self._sha(row["sha256"], "sha256"),
        )

    def _accepted(self, value: JsonValue) -> AcceptedInventoryIdentity:
        row = self._closed(
            value,
            {"accepted_closeout_commit", "byte_count", "path", "sha256"},
            "accepted_inventory",
        )
        return AcceptedInventoryIdentity(
            self._text(row["path"], "path"),
            self._nonnegative(row["byte_count"], "byte_count"),
            self._sha(row["sha256"], "sha256"),
            self._hex(row["accepted_closeout_commit"], "commit", 40),
        )

    def _route(self, value: JsonValue, index: int) -> PredecessorRoute:
        row = self._closed(
            value,
            {
                "compatibility_disposition",
                "defining_module",
                "defining_symbol",
                "exported_name",
                "package",
                "route",
                "support_status",
            },
            f"route[{index}]",
        )
        return PredecessorRoute(
            *(
                self._text(row[key], key)
                for key in (
                    "route",
                    "package",
                    "exported_name",
                    "defining_module",
                    "defining_symbol",
                    "support_status",
                    "compatibility_disposition",
                )
            )
        )

    def _binding(self, value: JsonValue, label: str) -> PackageBinding:
        row = self._record(value, label)
        base = {"imported_name", "kind", "line", "local_name", "origin"}
        if set(row) == base:
            defining = resolution = None
        elif set(row) == base | {"defining_origin", "origin_resolution"}:
            defining = self._text(row["defining_origin"], "defining_origin")
            resolution = self._enum(
                BindingOriginResolution,
                row["origin_resolution"],
                "origin_resolution",
            )
        else:
            raise FoundationModelError(f"{label} has invalid fields")
        return PackageBinding(
            self._enum(BindingKind, row["kind"], "kind"),
            self._positive(row["line"], "line"),
            self._text(row["local_name"], "local_name"),
            self._text(row["imported_name"], "imported_name"),
            self._text(row["origin"], "origin"),
            defining,
            resolution,
        )

    def _package(self, value: JsonValue, index: int) -> PackageSurface:
        row = self._closed(
            value,
            {
                "bindings",
                "declares_all",
                "effective_star_names",
                "initializer_byte_count",
                "initializer_path",
                "initializer_sha256",
                "package",
            },
            f"package[{index}]",
        )
        declares = row["declares_all"]
        if type(declares) is not bool:
            raise FoundationModelError("declares_all must be bool")
        return PackageSurface(
            self._text(row["package"], "package"),
            self._text(row["initializer_path"], "initializer_path"),
            self._nonnegative(row["initializer_byte_count"], "byte_count"),
            self._sha(row["initializer_sha256"], "sha256"),
            declares,
            tuple(
                self._text(item, "star name")
                for item in self._array(row["effective_star_names"], "star names")
            ),
            tuple(
                self._binding(item, "binding")
                for item in self._array(row["bindings"], "bindings")
            ),
        )

    def _import(self, value: JsonValue, index: int, prefix: str) -> ImportObservation:
        row = self._closed(
            value,
            {
                "column",
                "consumer_path",
                "import_kind",
                "imported_module",
                "imported_name",
                "line",
            },
            f"{prefix}[{index}]",
        )
        name = row["imported_name"]
        return ImportObservation(
            self._text(row["consumer_path"], "consumer_path"),
            self._positive(row["line"], "line"),
            self._nonnegative(row["column"], "column"),
            self._enum(ImportKind, row["import_kind"], "kind"),
            self._text(row["imported_module"], "module"),
            None if name is None else self._text(name, "name"),
        )

    def _documentation(self, value: JsonValue, index: int) -> DocumentationCitation:
        row = self._closed(
            value, {"column", "line", "path", "route_text"}, f"documentation[{index}]"
        )
        return DocumentationCitation(
            self._text(row["path"], "path"),
            self._positive(row["line"], "line"),
            self._nonnegative(row["column"], "column"),
            self._text(row["route_text"], "route_text"),
        )

    def _authority(self, value: JsonValue, index: int) -> AuthorityCitation:
        row = self._closed(
            value,
            {"authority_state", "column", "line", "matched_term", "path"},
            f"authority[{index}]",
        )
        state = self._enum(AuthorityState, row["authority_state"], "authority_state")
        return AuthorityCitation(
            self._text(row["path"], "path"),
            self._positive(row["line"], "line"),
            self._nonnegative(row["column"], "column"),
            self._text(row["matched_term"], "matched_term"),
            state,
        )

    def _lineage(self, value: JsonValue, index: int) -> Phase2LineageInput:
        row = self._closed(
            value, {"byte_count", "path", "role", "sha256"}, f"lineage[{index}]"
        )
        return Phase2LineageInput(
            self._enum(Phase2LineageRole, row["role"], "role"),
            self._text(row["path"], "path"),
            self._nonnegative(row["byte_count"], "byte_count"),
            self._sha(row["sha256"], "sha256"),
        )

    def _production(self, value: JsonValue, index: int) -> ProductionFactOutput:
        keys = {
            "all_syntax_count",
            "call_count",
            "callable_count",
            "class_count",
            "effective_all_names",
            "effective_all_resolution",
            "import_count",
            "module_name",
            "path",
            "source_byte_count",
            "source_sha256",
        }
        row = self._closed(value, keys, f"production[{index}]")
        names_value = row["effective_all_names"]
        names = (
            None
            if names_value is None
            else tuple(
                self._text(item, "all name")
                for item in self._array(names_value, "all names")
            )
        )
        return ProductionFactOutput(
            module_name=self._text(row["module_name"], "module_name"),
            path=self._text(row["path"], "path"),
            source_sha256=self._sha(row["source_sha256"], "sha256"),
            source_byte_count=self._nonnegative(row["source_byte_count"], "byte_count"),
            class_count=self._nonnegative(row["class_count"], "class_count"),
            callable_count=self._nonnegative(row["callable_count"], "callable_count"),
            import_count=self._nonnegative(row["import_count"], "import_count"),
            call_count=self._nonnegative(row["call_count"], "call_count"),
            all_syntax_count=self._nonnegative(
                row["all_syntax_count"], "all_syntax_count"
            ),
            effective_all_resolution=self._enum(
                ProductionAllResolution,
                row["effective_all_resolution"],
                "resolution",
            ),
            effective_all_names=names,
        )

    def _graph(self, value: JsonValue, index: int) -> DependencyGraphView:
        row = self._closed(
            value,
            {
                "edges",
                "node_names",
                "source_identities",
                "strongly_connected_components",
                "view",
            },
            f"graph[{index}]",
        )
        edges = tuple(
            DependencyEdge(
                self._text(edge["source_module"], "source"),
                self._text(edge["target_module"], "target"),
            )
            for item in self._array(row["edges"], "edges")
            for edge in [self._closed(item, {"source_module", "target_module"}, "edge")]
        )
        components = tuple(
            tuple(
                self._text(name, "component name")
                for name in self._array(item, "component")
            )
            for item in self._array(row["strongly_connected_components"], "components")
        )
        return DependencyGraphView(
            self._enum(DependencyGraphViewKind, row["view"], "view"),
            tuple(
                self._text(item, "node")
                for item in self._array(row["node_names"], "nodes")
            ),
            edges,
            components,
            tuple(
                self._sha(item, "source identity")
                for item in self._array(row["source_identities"], "source identities")
            ),
        )

    def _runtime_environment(self, value: JsonValue) -> RuntimeEnvironment:
        row = self._closed(
            value,
            {
                "distributions",
                "environment_sha256",
                "executable_byte_count",
                "executable_sha256",
                "implementation",
                "source_root",
                "version",
            },
            "runtime_environment",
        )
        distributions = tuple(
            self._distribution(item)
            for item in self._array(row["distributions"], "distributions")
        )
        return RuntimeEnvironment(
            self._nonnegative(row["executable_byte_count"], "byte_count"),
            self._sha(row["executable_sha256"], "sha256"),
            self._text(row["implementation"], "implementation"),
            self._text(row["version"], "version"),
            distributions,
            self._text(row["source_root"], "source_root"),
            self._sha(row["environment_sha256"], "environment_sha256"),
        )

    def _distribution(self, value: JsonValue) -> RuntimeDistribution:
        pair = self._array(value, "distribution")
        if len(pair) != 2:
            raise FoundationModelError("distribution must contain exactly two fields")
        return RuntimeDistribution(
            self._text(pair[0], "distribution name"),
            self._text(pair[1], "distribution version"),
        )

    def _loaded(self, value: JsonValue) -> RuntimeLoadedFile:
        row = self._closed(
            value, {"byte_count", "module_name", "path", "sha256"}, "loaded file"
        )
        return RuntimeLoadedFile(
            self._text(row["module_name"], "module_name"),
            self._text(row["path"], "path"),
            self._nonnegative(row["byte_count"], "byte_count"),
            self._sha(row["sha256"], "sha256"),
        )

    def _runtime_observation(self, value: JsonValue, index: int) -> RuntimeObservation:
        row = self._closed(
            value,
            {"environment_sha256", "observation", "package", "view"},
            f"runtime[{index}]",
        )
        observation = self._record(row["observation"], "observation")
        status = self._text(observation.get("status"), "status")
        if status == "success":
            self._keys(
                observation,
                {"attributes", "loaded_files", "status"},
                "success observation",
            )
            attributes = tuple(
                RuntimeAttribute(
                    self._text(attribute["name"], "name"),
                    self._text(attribute["value_type"], "value_type"),
                    None
                    if attribute["defining_module"] is None
                    else self._text(attribute["defining_module"], "defining_module"),
                )
                for item in self._array(observation["attributes"], "attributes")
                for attribute in [
                    self._closed(
                        item, {"defining_module", "name", "value_type"}, "attribute"
                    )
                ]
            )
            outcome: RuntimeOutcome = RuntimeSuccess(
                attributes,
                tuple(
                    self._loaded(item)
                    for item in self._array(observation["loaded_files"], "loaded_files")
                ),
            )
        elif status == "failure":
            self._keys(
                observation,
                {"exception_type", "failure_kind", "loaded_files", "message", "status"},
                "failure observation",
            )
            outcome = RuntimeFailure(
                self._enum(
                    RuntimeFailureKind,
                    observation["failure_kind"],
                    "failure_kind",
                ),
                self._text(observation["exception_type"], "exception_type"),
                self._text(observation["message"], "message"),
                tuple(
                    self._loaded(item)
                    for item in self._array(observation["loaded_files"], "loaded_files")
                ),
            )
        else:
            raise FoundationModelError("runtime status is invalid")
        return RuntimeObservation(
            self._text(row["package"], "package"),
            self._enum(RuntimeObservationView, row["view"], "view"),
            self._sha(row["environment_sha256"], "environment_sha256"),
            outcome,
        )

    def _supplemental(self, value: JsonValue, index: int) -> SupplementalCandidate:
        row = self._closed(
            value,
            {"candidate_key", "candidate_kind", "evidence", "support_status"},
            f"supplemental[{index}]",
        )
        key = self._text(row["candidate_key"], "candidate_key")
        kind = self._enum(SupplementalKind, row["candidate_kind"], "candidate_kind")
        if self._text(row["support_status"], "support_status") != "unknown":
            raise FoundationModelError("supplemental support status must be unknown")
        evidence = self._record(row["evidence"], "evidence")
        if kind is SupplementalKind.PACKAGE_BINDING:
            self._keys(evidence, {"binding", "package"}, "package evidence")
            return PackageBindingCandidate(
                key,
                kind,
                "unknown",
                self._text(evidence["package"], "package"),
                self._binding(evidence["binding"], "binding"),
            )
        self._keys(
            evidence,
            {"consumer_path", "imported_module", "imported_name"},
            "deep evidence",
        )
        name = evidence["imported_name"]
        return DeepImportCandidate(
            key,
            kind,
            "unknown",
            self._text(evidence["consumer_path"], "consumer_path"),
            self._text(evidence["imported_module"], "imported_module"),
            None if name is None else self._text(name, "imported_name"),
        )

    def _summary(self, value: JsonValue) -> FoundationSummary:
        keys = {
            "authority_citation_count",
            "consumer_import_count",
            "deep_non_initializer_module_import_count",
            "dependency_graph_view_count",
            "documentation_citation_count",
            "input_count",
            "package_surface_count",
            "phase2_lineage_input_count",
            "predecessor_route_count",
            "production_fact_output_count",
            "runtime_package_observation_count",
            "supplemental_candidate_count",
            "zero_route_surface_count",
        }
        row = self._closed(value, keys, "summary")
        return FoundationSummary(
            *(
                self._nonnegative(row[key], key)
                for key in (
                    "input_count",
                    "predecessor_route_count",
                    "package_surface_count",
                    "zero_route_surface_count",
                    "consumer_import_count",
                    "deep_non_initializer_module_import_count",
                    "documentation_citation_count",
                    "authority_citation_count",
                    "phase2_lineage_input_count",
                    "production_fact_output_count",
                    "dependency_graph_view_count",
                    "supplemental_candidate_count",
                    "runtime_package_observation_count",
                )
            )
        )

    def _cross_validate(self, report: PublicImportFoundation) -> None:
        PublicImportFoundationCrossViewValidator().execute(report)

    @staticmethod
    def _record(value: JsonValue | None, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise FoundationModelError(f"{label} must be an object")
        return value

    @staticmethod
    def _array(value: JsonValue, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise FoundationModelError(f"{label} must be an array")
        return value

    @classmethod
    def _closed(cls, value: JsonValue, keys: set[str], label: str) -> JsonRecord:
        row = cls._record(value, label)
        cls._keys(row, keys, label)
        return row

    @staticmethod
    def _keys(row: JsonRecord, keys: set[str], label: str) -> None:
        if set(row) != keys:
            raise FoundationModelError(f"{label} has invalid fields")

    @staticmethod
    def _text(value: JsonValue | None, label: str) -> str:
        if type(value) is not str or not value:
            raise FoundationModelError(f"{label} must be nonempty text")
        return value

    @classmethod
    def _enum(
        cls, enum_type: type[EnumValue], value: JsonValue, label: str
    ) -> EnumValue:
        text = cls._text(value, label)
        try:
            return enum_type(text)
        except ValueError as exc:
            raise FoundationModelError(f"{label} has an unsupported value") from exc

    @staticmethod
    def _integer(value: JsonValue, label: str) -> int:
        if type(value) is not int:
            raise FoundationModelError(f"{label} must be int")
        return value

    @classmethod
    def _nonnegative(cls, value: JsonValue, label: str) -> int:
        result = cls._integer(value, label)
        if result < 0:
            raise FoundationModelError(f"{label} must be nonnegative")
        return result

    @classmethod
    def _positive(cls, value: JsonValue, label: str) -> int:
        result = cls._integer(value, label)
        if result < 1:
            raise FoundationModelError(f"{label} must be positive")
        return result

    @classmethod
    def _hex(cls, value: JsonValue, label: str, length: int) -> str:
        result = cls._text(value, label)
        if len(result) != length or any(
            character not in "0123456789abcdef" for character in result
        ):
            raise FoundationModelError(f"{label} must be lowercase hexadecimal")
        return result

    @classmethod
    def _sha(cls, value: JsonValue, label: str) -> str:
        return cls._hex(value, label, 64)


class PublicImportFoundationCrossViewValidator:
    """Validate cohesive agreement among independently valid foundation records."""

    __slots__ = ()

    def execute(self, report: PublicImportFoundation) -> None:
        accepted = report.accepted_inventory
        if (
            accepted.path != "harness/reports/python-architecture-inventory.json"
            or accepted.byte_count != 2_980_876
            or accepted.sha256
            != "fb180c5d8aa9ecd33a319d03a5795ab24343d9b2b553acac580ec452b5795c7e"
            or accepted.accepted_closeout_commit
            != "f5ce3e981880fdfa336aa781664595b61a829557"
        ):
            raise FoundationModelError("accepted inventory anchor is unsupported")
        if len(report.inputs) != len(
            {item.path for item in report.inputs}
        ) or report.inputs != tuple(
            sorted(report.inputs, key=lambda item: (item.category.value, item.path))
        ):
            raise FoundationModelError("inputs must be unique and category/path sorted")
        input_by_path = {item.path: item for item in report.inputs}
        accepted_input = input_by_path.get(accepted.path)
        if (
            accepted_input is None
            or accepted_input.category is not InputCategory.ACCEPTED_INVENTORY
            or accepted_input.sha256 != accepted.sha256
            or accepted_input.byte_count != accepted.byte_count
        ):
            raise FoundationModelError(
                "accepted inventory identity disagrees with its selected input"
            )
        if report.predecessor_routes != tuple(
            sorted(report.predecessor_routes, key=lambda item: item.route)
        ) or len({item.route for item in report.predecessor_routes}) != len(
            report.predecessor_routes
        ):
            raise FoundationModelError("predecessor routes must be unique and sorted")
        route_pairs = {
            (item.package, item.exported_name) for item in report.predecessor_routes
        }
        star_pairs = {
            (item.package, name)
            for item in report.package_surfaces
            for name in item.effective_star_names
        }
        if (
            len(report.predecessor_routes) != 985
            or len(route_pairs) != 985
            or route_pairs != star_pairs
        ):
            raise FoundationModelError("predecessor and star routes disagree")
        if any(
            item.support_status != "unknown_no_exact_accepted_support_evidence"
            or item.compatibility_disposition
            != "unclassified_pending_bounded_option_b_application"
            for item in report.predecessor_routes
        ):
            raise FoundationModelError("predecessor state is not neutral")
        package_names = {item.package for item in report.package_surfaces}
        if report.package_surfaces != tuple(
            sorted(report.package_surfaces, key=lambda item: item.package)
        ):
            raise FoundationModelError("package surfaces must be sorted")
        routes_by_pair = {
            (item.package, item.exported_name): item
            for item in report.predecessor_routes
        }
        production_by_module = {
            item.module_name: item for item in report.production_fact_outputs
        }
        for package in report.package_surfaces:
            if len(package.effective_star_names) != len(
                set(package.effective_star_names)
            ):
                raise FoundationModelError("effective star names must be unique")
            bindings = {item.local_name: item for item in package.bindings}
            if len(bindings) != len(package.bindings) or package.bindings != tuple(
                sorted(package.bindings, key=lambda item: item.local_name)
            ):
                raise FoundationModelError("package bindings must be unique and sorted")
            star_names = set(package.effective_star_names)
            for name in package.effective_star_names:
                binding = bindings.get(name)
                route = routes_by_pair.get((package.package, name))
                if binding is None or route is None:
                    raise FoundationModelError(
                        "star binding origin resolution disagrees"
                    )
                terminal_module, separator, terminal_symbol = (
                    binding.defining_origin or ""
                ).rpartition(".")
                if (
                    binding.origin != f"{route.defining_module}.{route.defining_symbol}"
                    or not separator
                    or terminal_module not in production_by_module
                    or terminal_symbol != binding.imported_name
                    or binding.origin_resolution
                    is not BindingOriginResolution.TRANSITIVE_FIRST_PARTY
                ):
                    raise FoundationModelError(
                        "star binding origin resolution disagrees"
                    )
            for name, binding in bindings.items():
                if name not in star_names and (
                    binding.defining_origin is not None
                    or binding.origin_resolution is not None
                ):
                    raise FoundationModelError(
                        "non-star binding cannot retain defining-origin fields"
                    )
        if (
            len(package_names) != 35
            or set(report.zero_route_surfaces)
            != package_names - {item.package for item in report.predecessor_routes}
            or len(report.zero_route_surfaces) != 10
            or report.zero_route_surfaces != tuple(sorted(report.zero_route_surfaces))
        ):
            raise FoundationModelError("zero-route surfaces disagree")
        expected_deep = tuple(
            item
            for item in report.consumer_imports
            if item.imported_module not in package_names
        )
        if report.deep_imports != expected_deep:
            raise FoundationModelError("deep-import view disagrees with consumers")
        production_by_path = {
            item.path: item for item in report.production_fact_outputs
        }
        selected_production_paths = {
            item.path
            for item in report.inputs
            if item.category is InputCategory.PRODUCTION_MODULE
        }
        if (
            len(report.production_fact_outputs) != 216
            or len(production_by_module) != 216
            or len(production_by_path) != 216
            or set(production_by_path) != selected_production_paths
        ):
            raise FoundationModelError(
                "production-fact outputs must bijectively cover 216 selected modules"
            )
        for output in report.production_fact_outputs:
            source = input_by_path.get(output.path)
            if (
                source is None
                or source.category is not InputCategory.PRODUCTION_MODULE
                or self._module_name(output.path) != output.module_name
                or source.sha256 != output.source_sha256
                or source.byte_count != output.source_byte_count
                or (output.effective_all_resolution is ProductionAllResolution.LITERAL)
                != (output.effective_all_names is not None)
            ):
                raise FoundationModelError("production-fact output identity disagrees")
        expected_sources = tuple(
            sorted(item.source_sha256 for item in report.production_fact_outputs)
        )
        for view in report.dependency_graph_views:
            if (
                view.source_identities != expected_sources
                or len(view.node_names) != len(set(view.node_names))
                or view.node_names != tuple(sorted(view.node_names))
            ):
                raise FoundationModelError("graph source or node identities disagree")
            if any(
                edge.source_module not in view.node_names
                or edge.target_module not in view.node_names
                for edge in view.edges
            ):
                raise FoundationModelError("graph edge endpoint is absent")
            edge_keys = tuple(
                (edge.source_module, edge.target_module) for edge in view.edges
            )
            if edge_keys != tuple(sorted(set(edge_keys))):
                raise FoundationModelError("graph edges must be unique and sorted")
            flattened = tuple(
                name
                for component in view.strongly_connected_components
                for name in component
            )
            if len(flattened) != len(set(flattened)) or set(flattened) != set(
                view.node_names
            ):
                raise FoundationModelError("graph components must partition nodes")
            self._validate_sccs(view)
        citation_keys = tuple(
            (item.path, item.line, item.column, item.route_text)
            for item in report.documentation_citations
        )
        authority_keys = tuple(
            (item.path, item.line, item.column, item.matched_term)
            for item in report.authority_citations
        )
        consumer_keys = tuple(
            (
                item.consumer_path,
                item.line,
                item.column,
                item.import_kind.value,
                item.imported_module,
                item.imported_name or "",
            )
            for item in report.consumer_imports
        )
        for keys, label in (
            (citation_keys, "documentation citations"),
            (authority_keys, "authority citations"),
            (consumer_keys, "consumer imports"),
        ):
            if keys != tuple(sorted(keys)) or len(keys) != len(set(keys)):
                raise FoundationModelError(f"{label} must be unique and sorted")
        if len({item.candidate_key for item in report.supplemental_candidates}) != len(
            report.supplemental_candidates
        ) or report.supplemental_candidates != tuple(
            sorted(report.supplemental_candidates, key=lambda item: item.candidate_key)
        ):
            raise FoundationModelError(
                "supplemental candidates must be unique and sorted"
            )
        environment = report.runtime_environment
        if any(
            item.environment_sha256 != environment.environment_sha256
            for item in report.runtime_observations
        ):
            raise FoundationModelError("runtime environment identity disagrees")
        if tuple(item.package for item in report.runtime_observations) != tuple(
            sorted(package_names)
        ):
            raise FoundationModelError("runtime observations do not cover packages")
        expected_summary = FoundationSummary(
            len(report.inputs),
            len(report.predecessor_routes),
            len(report.package_surfaces),
            len(report.zero_route_surfaces),
            len(report.consumer_imports),
            len(report.deep_imports),
            len(report.documentation_citations),
            len(report.authority_citations),
            len(report.phase2_lineage_inputs),
            len(report.production_fact_outputs),
            len(report.dependency_graph_views),
            len(report.supplemental_candidates),
            len(report.runtime_observations),
        )
        if report.summary != expected_summary:
            raise FoundationModelError("summary/body counts disagree")
        if tuple(view.view for view in report.dependency_graph_views) != tuple(
            DependencyGraphViewKind
        ):
            raise FoundationModelError("dependency graph views are incomplete")
        if report.claim_boundaries != tuple(ClaimBoundary):
            raise FoundationModelError("claim boundaries are incomplete or reordered")
        if tuple(item.role for item in report.phase2_lineage_inputs) != tuple(
            Phase2LineageRole
        ):
            raise FoundationModelError("Phase 2 lineage roles are incomplete")
        expected_lineage = {
            Phase2LineageRole.PRODUCTION_FACTS_TASK: (
                "tasks/software/python.architecture-refactor.architecture-conformance.production-facts.json",
                InputCategory.PHASE2_VIEW,
            ),
            Phase2LineageRole.PRODUCTION_FACTS_OWNERSHIP: (
                ".pi/task-ownership/python.architecture-refactor.architecture-conformance.production-facts.json",
                InputCategory.PHASE2_VIEW,
            ),
            Phase2LineageRole.PRODUCTION_FACTS_IMPLEMENTATION: (
                "python/src/ksdft2effmass/harness/pi/conformance/python/production.py",
                InputCategory.PRODUCTION_MODULE,
            ),
            Phase2LineageRole.DEPENDENCY_GRAPH_TASK: (
                "tasks/software/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
                InputCategory.PHASE2_VIEW,
            ),
            Phase2LineageRole.DEPENDENCY_GRAPH_OWNERSHIP: (
                ".pi/task-ownership/python.architecture-refactor.architecture-conformance.dependency-graph-views.json",
                InputCategory.PHASE2_VIEW,
            ),
            Phase2LineageRole.DEPENDENCY_GRAPH_IMPLEMENTATION: (
                "python/src/ksdft2effmass/harness/pi/conformance/python/dependency_graph.py",
                InputCategory.PRODUCTION_MODULE,
            ),
        }
        for lineage in report.phase2_lineage_inputs:
            expected_path, expected_category = expected_lineage[lineage.role]
            selected = input_by_path.get(lineage.path)
            if (
                lineage.path != expected_path
                or selected is None
                or selected.category is not expected_category
                or selected.sha256 != lineage.sha256
                or selected.byte_count != lineage.byte_count
            ):
                raise FoundationModelError(
                    "Phase 2 lineage identity disagrees with its selected input"
                )

    @staticmethod
    def _module_name(path: str) -> str:
        prefix = "python/src/"
        if not path.startswith(prefix) or not path.endswith(".py"):
            raise FoundationModelError(f"invalid production module path: {path}")
        relative = path[len(prefix) : -3].removesuffix("/__init__")
        module_name = relative.replace("/", ".")
        if not module_name or any(
            not part.isidentifier() for part in module_name.split(".")
        ):
            raise FoundationModelError(f"invalid production module identity: {path}")
        return module_name

    @classmethod
    def _validate_sccs(cls, view: DependencyGraphView) -> None:
        adjacency: dict[str, tuple[str, ...]] = {
            name: tuple(
                edge.target_module for edge in view.edges if edge.source_module == name
            )
            for name in view.node_names
        }
        reachable = {name: cls._reachable(name, adjacency) for name in view.node_names}
        component_by_name = {
            name: index
            for index, component in enumerate(view.strongly_connected_components)
            for name in component
        }
        for source in view.node_names:
            for target in view.node_names:
                mutually_reachable = (
                    target in reachable[source] and source in reachable[target]
                )
                represented_together = (
                    component_by_name[source] == component_by_name[target]
                )
                if mutually_reachable != represented_together:
                    raise FoundationModelError(
                        "represented components disagree with mutual reachability"
                    )

    @staticmethod
    def _reachable(
        source: str, adjacency: dict[str, tuple[str, ...]]
    ) -> frozenset[str]:
        pending = [source]
        visited: set[str] = set()
        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            pending.extend(adjacency[current])
        return frozenset(visited)
