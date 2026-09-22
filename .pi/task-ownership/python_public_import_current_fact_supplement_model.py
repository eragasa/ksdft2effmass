"""Closed immutable records for the task-internal current-fact supplement."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import TypeAlias

from python_public_import_foundation_model import (
    AuthorityCitation,
    DependencyGraphView,
    DependencyGraphViewKind,
    DocumentationCitation,
    FoundationJsonCodec,
    ImportObservation,
    JsonValue,
    PackageSurface,
    PredecessorRoute,
    ProductionFactOutput,
    PublicImportFoundation,
    RuntimeEnvironment,
    RuntimeObservation,
)

JsonObject: TypeAlias = dict[str, JsonValue]


class SupplementFormatError(ValueError):
    """Report one deterministic supplement format or relation defect."""


class SupplementOperation(StrEnum):
    """Identify one exact command operation."""

    ACQUIRE = "acquire"
    GENERATE = "generate"


class InputVariant(StrEnum):
    """Identify the immutable source of one selected input."""

    TARGET_TREE = "TargetTreeInput"
    BASE_TREE = "BaseTreeInput"
    ACCEPTED_F0 = "AcceptedF0Input"
    TASK_TOOL = "TaskToolInput"


class DeltaStatus(StrEnum):
    """Represent the no-rename delta status."""

    ADDED = "Added"
    DELETED = "Deleted"
    MODIFIED = "Modified"


class DeltaTouch(StrEnum):
    """Represent which fixed post-F0 intervals touched a path."""

    MERGE_ONLY = "merge_only"
    POST_MERGE_ONLY = "post_merge_only"
    BOTH = "merge_and_post_merge"


class SelectionCategory(StrEnum):
    """Identify one exact authored input category."""

    ACCEPTED_F0 = "accepted_f0"
    ACCEPTED_INVENTORY = "accepted_inventory"
    ARCHITECTURE_DOCUMENTATION = "architecture_documentation"
    AUTHORITY = "authority"
    CALCULATION_CONTEXT = "calculation_context"
    CALCULATION_DOCUMENTATION = "calculation_documentation"
    CHECKPOINT = "checkpoint"
    CONFORMANCE_INVENTORY = "conformance_inventory"
    EXAMPLE = "example"
    HARNESS_CHECK = "harness_check"
    HARNESS_STATE = "harness_state"
    HARNESS_TASK_GRAPH = "harness_task_graph"
    LICENSE_CONTEXT = "license_context"
    MAINTAINED_TEST = "maintained_test"
    OTHER_FIRST_PARTY_PYTHON = "other_first_party_python"
    PHASE2_VIEW = "phase2_view"
    PRODUCTION_MODULE = "production_module"
    PUBLIC_DOCUMENTATION = "public_documentation"
    PUBLICATION_CONTEXT = "publication_context"
    PYTHON_ENVIRONMENT = "python_environment"
    PYTHON_RESOURCE = "python_resource"
    TASK_AUTHORITY = "task_authority"
    TASK_TOOL = "task_tool"
    TEST_RESOURCE = "test_resource"


class MaterialityCategory(StrEnum):
    """Partition every measured delta path exactly once."""

    CONFORMANCE_INVENTORY = "conformance_inventory"
    CHECKPOINT = "checkpoint"
    CALCULATION_PYTHON = "calculation_python"
    CALCULATION_DOCUMENTATION = "calculation_documentation"
    CALCULATION_CONTEXT = "calculation_context"
    PUBLIC_DOCUMENTATION = "public_documentation"
    ARCHITECTURE_DOCUMENTATION = "architecture_documentation"
    PUBLICATION_CONTEXT = "publication_context"
    HARNESS_STATE = "harness_state"
    HARNESS_TASK_GRAPH = "harness_task_graph"
    PRODUCTION_MODULE = "production_module"
    MAINTAINED_TEST = "maintained_test"
    TEST_RESOURCE = "test_resource"
    PYTHON_ENVIRONMENT = "python_environment"
    TASK_AUTHORITY = "task_authority"
    LICENSE_CONTEXT = "license_context"


class ExtractionRole(StrEnum):
    """Describe a closed neutral use of one selected input."""

    AUTHORITY = "authority_citation"
    CONSUMER = "python_consumer"
    DELTA_IDENTITY = "delta_identity"
    DOCUMENTATION = "documentation_citation"
    F0_LINEAGE = "accepted_f0_lineage"
    IDENTITY_ONLY = "identity_only"
    PRODUCTION = "production_fact"
    RUNTIME = "runtime_source"
    TASK_TOOL = "task_tool"


@dataclass(frozen=True, slots=True)
class SelectionEntry:
    """Represent one authored canonical selection row."""

    variant: InputVariant
    category: SelectionCategory
    roles: tuple[ExtractionRole, ...]
    path: PurePosixPath

    def __post_init__(self) -> None:
        if type(self.variant) is not InputVariant:
            raise TypeError("variant must be InputVariant")
        if type(self.category) is not SelectionCategory:
            raise TypeError("category must be SelectionCategory")
        if type(self.roles) is not tuple or not self.roles:
            raise ValueError("roles must be a nonempty tuple")
        if any(type(role) is not ExtractionRole for role in self.roles):
            raise TypeError("roles must contain ExtractionRole values")
        if self.roles != tuple(sorted(set(self.roles), key=lambda item: item.value)):
            raise ValueError("roles must be sorted and unique")
        if ExtractionRole.IDENTITY_ONLY in self.roles and self.roles != (
            ExtractionRole.IDENTITY_ONLY,
        ):
            raise ValueError("identity_only must be the sole extraction role")
        RepositoryPath.require(self.path)

    @property
    def sort_key(self) -> tuple[str, str, str]:
        """Return canonical path-first ordering."""
        return self.path.as_posix(), self.variant.value, self.category.value


@dataclass(frozen=True, slots=True)
class PresentTreeEntry:
    """Identify one present Git tree entry without embedding payload bytes."""

    mode: str
    blob_oid: str
    sha256: str
    byte_count: int

    def __post_init__(self) -> None:
        if self.mode not in {"100644", "100755"}:
            raise ValueError("only regular-file Git modes are supported")
        Identity.require_hex(self.blob_oid, 40, "blob_oid")
        Identity.require_hex(self.sha256, 64, "sha256")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("byte_count must be a nonnegative built-in int")


@dataclass(frozen=True, slots=True)
class AbsentTreeEntry:
    """Represent one intentionally absent tree side."""

    state: str = "absent"

    def __post_init__(self) -> None:
        if self.state != "absent":
            raise ValueError("absent entry state must be absent")


TreeEntry: TypeAlias = PresentTreeEntry | AbsentTreeEntry


@dataclass(frozen=True, slots=True)
class DeltaLedgerEntry:
    """Represent one exact no-rename base-to-target path change."""

    path: PurePosixPath
    status: DeltaStatus
    base: TreeEntry
    target: TreeEntry
    touch: DeltaTouch
    category: MaterialityCategory
    extraction_roles: tuple[ExtractionRole, ...]
    identity_only_reason: str | None

    def __post_init__(self) -> None:
        RepositoryPath.require(self.path)
        if type(self.status) is not DeltaStatus:
            raise TypeError("status must be DeltaStatus")
        if type(self.base) not in {PresentTreeEntry, AbsentTreeEntry}:
            raise TypeError("base must be a closed tree-entry variant")
        if type(self.target) not in {PresentTreeEntry, AbsentTreeEntry}:
            raise TypeError("target must be a closed tree-entry variant")
        expected_presence = {
            DeltaStatus.ADDED: (False, True),
            DeltaStatus.DELETED: (True, False),
            DeltaStatus.MODIFIED: (True, True),
        }[self.status]
        actual_presence = (
            type(self.base) is PresentTreeEntry,
            type(self.target) is PresentTreeEntry,
        )
        if actual_presence != expected_presence:
            raise ValueError("delta status and tree-side presence disagree")
        if type(self.touch) is not DeltaTouch:
            raise TypeError("touch must be DeltaTouch")
        if type(self.category) is not MaterialityCategory:
            raise TypeError("category must be MaterialityCategory")
        if self.extraction_roles != tuple(
            sorted(set(self.extraction_roles), key=lambda item: item.value)
        ):
            raise ValueError("extraction roles must be sorted and unique")
        identity_only = ExtractionRole.IDENTITY_ONLY in self.extraction_roles
        if identity_only != (self.identity_only_reason is not None):
            raise ValueError("identity-only role and reason must occur together")
        if self.identity_only_reason is not None and (
            type(self.identity_only_reason) is not str or not self.identity_only_reason
        ):
            raise ValueError("identity-only reason must be nonempty text")


@dataclass(frozen=True, slots=True)
class ManifestInput:
    """Bind one selected source to exact content and snapshot location."""

    selection: SelectionEntry
    tree_entry: PresentTreeEntry
    snapshot_path: PurePosixPath | None

    def __post_init__(self) -> None:
        if type(self.selection) is not SelectionEntry:
            raise TypeError("selection must be SelectionEntry")
        if type(self.tree_entry) is not PresentTreeEntry:
            raise TypeError("tree_entry must be PresentTreeEntry")
        if self.snapshot_path is not None:
            RepositoryPath.require(self.snapshot_path)


@dataclass(frozen=True, slots=True)
class CommitTopology:
    """Bind the exact measured Git topology."""

    base_commit: str
    base_tree: str
    merge_commit: str
    merge_tree: str
    merge_parents: tuple[str, str]
    target_commit: str
    target_tree: str
    target_parent: str
    name_status_lf_sha256: str
    name_status_nul_sha256: str
    shortstat_insertions: int
    shortstat_deletions: int

    def __post_init__(self) -> None:
        for name, value in (
            ("base_commit", self.base_commit),
            ("base_tree", self.base_tree),
            ("merge_commit", self.merge_commit),
            ("merge_tree", self.merge_tree),
            ("target_commit", self.target_commit),
            ("target_tree", self.target_tree),
            ("target_parent", self.target_parent),
        ):
            Identity.require_hex(value, 40, name)
        if type(self.merge_parents) is not tuple or len(self.merge_parents) != 2:
            raise ValueError("merge_parents must contain exactly two commit IDs")
        for parent in self.merge_parents:
            Identity.require_hex(parent, 40, "merge_parent")
        Identity.require_hex(self.name_status_lf_sha256, 64, "name_status_lf_sha256")
        Identity.require_hex(self.name_status_nul_sha256, 64, "name_status_nul_sha256")
        if (self.shortstat_insertions, self.shortstat_deletions) != (129391, 21234):
            raise ValueError("shortstat counts disagree with the fixed interval")


@dataclass(frozen=True, slots=True)
class AcquisitionManifest:
    """Represent the complete immutable acquisition boundary."""

    schema_version: int
    subject_identity: str
    topology: CommitTopology
    selection_sha256: str
    inputs: tuple[ManifestInput, ...]
    delta_ledger: tuple[DeltaLedgerEntry, ...]

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("manifest schema_version must be 1")
        if (
            self.subject_identity
            != "ksdft2effmass.python.public-import-current-fact-supplement-inputs"
        ):
            raise ValueError("manifest subject identity is unsupported")
        Identity.require_hex(self.selection_sha256, 64, "selection_sha256")
        if self.inputs != tuple(
            sorted(self.inputs, key=lambda item: item.selection.sort_key)
        ):
            raise ValueError("manifest inputs are not canonically ordered")
        input_paths = tuple(item.selection.path.as_posix() for item in self.inputs)
        if len(input_paths) != len(set(input_paths)):
            raise ValueError("manifest input paths must be unique")
        ledger_paths = tuple(item.path.as_posix() for item in self.delta_ledger)
        if ledger_paths != tuple(sorted(set(ledger_paths))):
            raise ValueError("delta ledger paths must be sorted and unique")
        added = sum(item.status is DeltaStatus.ADDED for item in self.delta_ledger)
        deleted = sum(item.status is DeltaStatus.DELETED for item in self.delta_ledger)
        modified = sum(
            item.status is DeltaStatus.MODIFIED for item in self.delta_ledger
        )
        if (len(self.delta_ledger), added, modified, deleted) != (565, 419, 145, 1):
            raise ValueError("delta ledger cardinality is not 565/A419/M145/D1")


@dataclass(frozen=True, slots=True)
class CurrentRouteObservation:
    """Represent one current effective-star route."""

    route: str
    package: str
    exported_name: str
    direct_origin: str
    defining_origin: str
    predecessor_route: bool

    def __post_init__(self) -> None:
        for name, value in (
            ("route", self.route),
            ("package", self.package),
            ("exported_name", self.exported_name),
            ("direct_origin", self.direct_origin),
            ("defining_origin", self.defining_origin),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be nonempty text")
        if self.route != f"{self.package}.{self.exported_name}":
            raise ValueError("current route key is inconsistent")
        if type(self.predecessor_route) is not bool:
            raise TypeError("predecessor_route must be bool")


@dataclass(frozen=True, slots=True)
class SupplementalRouteCandidate:
    """Represent one current route absent from accepted F0 lineage."""

    candidate_key: str
    route: CurrentRouteObservation
    support_status: str = "unknown"
    compatibility_disposition: str = "unclassified"

    def __post_init__(self) -> None:
        if self.candidate_key != f"current-route:{self.route.route}":
            raise ValueError("supplemental candidate key disagrees with route")
        if (
            self.support_status != "unknown"
            or self.compatibility_disposition != "unclassified"
        ):
            raise ValueError("supplemental candidate must remain neutral")
        if self.route.predecessor_route:
            raise ValueError("predecessor routes cannot be supplemental candidates")


@dataclass(frozen=True, slots=True)
class ZeroBoundaryTransition:
    """Represent one accepted-empty surface that is currently nonempty."""

    package: str
    predecessor_state: str
    current_state: str
    current_route_keys: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.package != "ksdft2effmass.campaigns":
            raise ValueError("only the campaigns transition is authorized")
        if (
            self.predecessor_state != "accepted_empty"
            or self.current_state != "nonempty"
        ):
            raise ValueError("zero-boundary transition states are unsupported")
        if self.current_route_keys != (
            "ksdft2effmass.campaigns.PlaneWaveParameterStudyCompiler",
        ):
            raise ValueError("campaigns transition route is unexpected")


@dataclass(frozen=True, slots=True)
class SupplementSummary:
    """Contain counts derived from the represented records."""

    delta_path_count: int
    added_path_count: int
    modified_path_count: int
    deleted_path_count: int
    production_module_count: int
    package_surface_count: int
    predecessor_route_count: int
    current_route_count: int
    supplemental_candidate_count: int
    accepted_zero_lineage_count: int
    current_empty_surface_count: int
    zero_boundary_transition_count: int


@dataclass(frozen=True, slots=True)
class CurrentFactSupplement:
    """Represent the complete neutral current-fact supplement."""

    schema_version: int
    subject_identity: str
    subject_version: str
    manifest_sha256: str
    topology: CommitTopology
    delta_ledger: tuple[DeltaLedgerEntry, ...]
    predecessor_routes: tuple[PredecessorRoute, ...]
    predecessor_package_observations: tuple[PackageSurface, ...]
    current_production_modules: tuple[ProductionFactOutput, ...]
    current_package_surfaces: tuple[PackageSurface, ...]
    current_routes: tuple[CurrentRouteObservation, ...]
    supplemental_candidates: tuple[SupplementalRouteCandidate, ...]
    accepted_zero_boundary_lineages: tuple[str, ...]
    current_empty_surfaces: tuple[str, ...]
    zero_boundary_transitions: tuple[ZeroBoundaryTransition, ...]
    consumer_imports: tuple[ImportObservation, ...]
    documentation_citations: tuple[DocumentationCitation, ...]
    authority_citations: tuple[AuthorityCitation, ...]
    dependency_graph_views: tuple[DependencyGraphView, ...]
    runtime_environment: RuntimeEnvironment
    runtime_observations: tuple[RuntimeObservation, ...]
    claim_boundaries: tuple[str, ...]
    summary: SupplementSummary

    def __post_init__(self) -> None:
        if (self.schema_version, self.subject_identity, self.subject_version) != (
            1,
            "ksdft2effmass.python.public-import-current-fact-supplement",
            "1",
        ):
            raise ValueError("supplement identity is unsupported")
        Identity.require_hex(self.manifest_sha256, 64, "manifest_sha256")
        expected = SupplementSummary(
            delta_path_count=len(self.delta_ledger),
            added_path_count=sum(
                item.status is DeltaStatus.ADDED for item in self.delta_ledger
            ),
            modified_path_count=sum(
                item.status is DeltaStatus.MODIFIED for item in self.delta_ledger
            ),
            deleted_path_count=sum(
                item.status is DeltaStatus.DELETED for item in self.delta_ledger
            ),
            production_module_count=len(self.current_production_modules),
            package_surface_count=len(self.current_package_surfaces),
            predecessor_route_count=len(self.predecessor_routes),
            current_route_count=len(self.current_routes),
            supplemental_candidate_count=len(self.supplemental_candidates),
            accepted_zero_lineage_count=len(self.accepted_zero_boundary_lineages),
            current_empty_surface_count=len(self.current_empty_surfaces),
            zero_boundary_transition_count=len(self.zero_boundary_transitions),
        )
        if self.summary != expected:
            raise ValueError("supplement summary is not derived from records")
        required = (565, 419, 145, 1, 320, 47, 985, 1456, 471, 10, 9, 1)
        observed = tuple(
            expected.__getattribute__(name) for name in expected.__dataclass_fields__
        )
        if observed != required:
            raise ValueError(f"supplement cardinalities disagree: {observed}")
        predecessor_keys = tuple(item.route for item in self.predecessor_routes)
        current_keys = tuple(item.route for item in self.current_routes)
        if len(predecessor_keys) != len(set(predecessor_keys)) or not set(
            predecessor_keys
        ).issubset(current_keys):
            raise ValueError("predecessor route lineage is not retained")
        candidate_keys = tuple(
            item.route.route for item in self.supplemental_candidates
        )
        if set(candidate_keys) != set(current_keys) - set(predecessor_keys):
            raise ValueError(
                "supplemental routes do not close the current route universe"
            )
        current_by_route = {item.route: item for item in self.current_routes}
        if any(
            candidate.route != current_by_route[candidate.route.route]
            for candidate in self.supplemental_candidates
        ):
            raise ValueError("supplemental candidate route differs from current route")
        if any(not value for value in self.claim_boundaries):
            raise ValueError("claim boundaries must be nonempty")
        self._require_sorted_unique(
            tuple(item.route for item in self.predecessor_routes),
            "predecessor routes",
        )
        self._require_sorted_unique(
            tuple(item.package for item in self.predecessor_package_observations),
            "predecessor packages",
        )
        self._require_sorted_unique(
            tuple(item.path for item in self.current_production_modules),
            "production modules",
        )
        self._require_sorted_unique(
            tuple(item.package for item in self.current_package_surfaces),
            "current package surfaces",
        )
        self._require_sorted_unique(current_keys, "current routes")
        self._require_sorted_unique(
            tuple(item.candidate_key for item in self.supplemental_candidates),
            "supplemental candidates",
        )
        self._require_sorted_unique(
            self.accepted_zero_boundary_lineages, "accepted zero lineages"
        )
        self._require_sorted_unique(self.current_empty_surfaces, "empty surfaces")
        self._require_sorted_unique(
            tuple(item.package for item in self.runtime_observations),
            "runtime observations",
        )
        expected_empty = tuple(
            item.package
            for item in self.current_package_surfaces
            if not item.effective_star_names
        )
        if self.current_empty_surfaces != expected_empty:
            raise ValueError("current empty surfaces are not derived from surfaces")
        expected_routes = self._derived_routes()
        if self.current_routes != expected_routes:
            raise ValueError("current routes are not derived from package surfaces")
        transitioned = tuple(
            package
            for package in self.accepted_zero_boundary_lineages
            if package not in set(self.current_empty_surfaces)
        )
        if transitioned != tuple(
            item.package for item in self.zero_boundary_transitions
        ):
            raise ValueError("zero-boundary transitions are not derived")
        self._require_occurrence_order()

    def _derived_routes(self) -> tuple[CurrentRouteObservation, ...]:
        predecessor_keys = {item.route for item in self.predecessor_routes}
        rows: list[CurrentRouteObservation] = []
        for surface in self.current_package_surfaces:
            bindings = {item.local_name: item for item in surface.bindings}
            for name in surface.effective_star_names:
                binding = bindings[name]
                if binding.defining_origin is None:
                    raise ValueError("effective-star binding lacks defining origin")
                route = f"{surface.package}.{name}"
                rows.append(
                    CurrentRouteObservation(
                        route=route,
                        package=surface.package,
                        exported_name=name,
                        direct_origin=binding.origin,
                        defining_origin=binding.defining_origin,
                        predecessor_route=route in predecessor_keys,
                    )
                )
        return tuple(sorted(rows, key=lambda item: item.route))

    def _require_occurrence_order(self) -> None:
        consumer_keys = tuple(
            (
                item.consumer_path,
                item.line,
                item.column,
                item.import_kind.value,
                item.imported_module,
                item.imported_name or "",
            )
            for item in self.consumer_imports
        )
        if consumer_keys != tuple(sorted(set(consumer_keys))):
            raise ValueError("consumer imports must be canonically sorted and unique")
        documentation_keys = tuple(
            (item.path, item.line, item.column, item.route_text)
            for item in self.documentation_citations
        )
        if documentation_keys != tuple(sorted(set(documentation_keys))):
            raise ValueError(
                "documentation citations must be canonically sorted and unique"
            )
        authority_keys = tuple(
            (item.path, item.line, item.column, item.matched_term)
            for item in self.authority_citations
        )
        if authority_keys != tuple(sorted(set(authority_keys))):
            raise ValueError(
                "authority citations must be canonically sorted and unique"
            )
        if tuple(item.view for item in self.dependency_graph_views) != tuple(
            DependencyGraphViewKind
        ):
            raise ValueError("dependency graph views must follow the closed view order")

    @staticmethod
    def _require_sorted_unique(keys: tuple[str, ...], label: str) -> None:
        if keys != tuple(sorted(set(keys))):
            raise ValueError(f"{label} must be canonically sorted and unique")


@dataclass(frozen=True, slots=True)
class CurrentFactSupplementCrossViewValidator:
    """Validate report agreement with exact manifest and accepted F0 lineage."""

    def execute(
        self,
        report: CurrentFactSupplement,
        manifest: AcquisitionManifest,
        manifest_sha256: str,
        foundation: PublicImportFoundation,
    ) -> None:
        """Require complete identity, lineage, role, and coverage closure."""
        if report.manifest_sha256 != manifest_sha256:
            raise SupplementFormatError("report manifest identity mismatch")
        if (
            report.topology != manifest.topology
            or report.delta_ledger != manifest.delta_ledger
        ):
            raise SupplementFormatError(
                "report topology or ledger differs from manifest"
            )
        if report.predecessor_routes != foundation.predecessor_routes:
            raise SupplementFormatError("predecessor routes differ from accepted F0")
        if report.predecessor_package_observations != foundation.package_surfaces:
            raise SupplementFormatError("predecessor packages differ from accepted F0")
        if report.accepted_zero_boundary_lineages != foundation.zero_route_surfaces:
            raise SupplementFormatError(
                "zero-boundary lineages differ from accepted F0"
            )
        inputs = {item.selection.path.as_posix(): item for item in manifest.inputs}
        if len(inputs) != len(manifest.inputs):
            raise SupplementFormatError("manifest input paths are not unique")
        for manifest_input in manifest.inputs:
            identity_only = manifest_input.selection.roles == (
                ExtractionRole.IDENTITY_ONLY,
            )
            if identity_only != (manifest_input.snapshot_path is None):
                raise SupplementFormatError(
                    "input role and snapshot materialization disagree"
                )
            self._require_role_consumption(manifest_input)
        production_paths = tuple(
            item.path for item in report.current_production_modules
        )
        selected_production = tuple(
            sorted(
                item.selection.path.as_posix()
                for item in manifest.inputs
                if ExtractionRole.PRODUCTION in item.selection.roles
            )
        )
        if production_paths != selected_production:
            raise SupplementFormatError(
                "production coverage differs from selected inputs"
            )
        expected_packages = tuple(
            path for path in selected_production if path.endswith("/__init__.py")
        )
        if (
            tuple(item.initializer_path for item in report.current_package_surfaces)
            != expected_packages
        ):
            raise SupplementFormatError(
                "package coverage differs from production inputs"
            )
        for production in report.current_production_modules:
            production_input = inputs[production.path]
            if (
                production.source_sha256 != production_input.tree_entry.sha256
                or production.source_byte_count
                != production_input.tree_entry.byte_count
            ):
                raise SupplementFormatError(
                    "production identity differs from selected input"
                )
        for surface in report.current_package_surfaces:
            initializer_input = inputs[surface.initializer_path]
            if (
                surface.initializer_sha256 != initializer_input.tree_entry.sha256
                or surface.initializer_byte_count
                != initializer_input.tree_entry.byte_count
            ):
                raise SupplementFormatError(
                    "package initializer identity differs from selected input"
                )
        self._require_occurrence_roles(report, inputs)
        if tuple(item.package for item in report.runtime_observations) != tuple(
            item.package for item in report.current_package_surfaces
        ):
            raise SupplementFormatError(
                "runtime coverage differs from package surfaces"
            )
        if any(
            item.environment_sha256 != report.runtime_environment.environment_sha256
            for item in report.runtime_observations
        ):
            raise SupplementFormatError("runtime environment identity mismatch")
        self._require_runtime_loaded_file_identities(report, inputs)
        ledger_by_path = {item.path.as_posix(): item for item in manifest.delta_ledger}
        for path, ledger in ledger_by_path.items():
            ledger_input = inputs.get(path)
            if ledger_input is None:
                raise SupplementFormatError("delta path is absent from selection")
            if ledger.extraction_roles != ledger_input.selection.roles:
                raise SupplementFormatError(
                    "delta and selection extraction roles disagree"
                )
            expected_source = (
                ledger.base if ledger.status is DeltaStatus.DELETED else ledger.target
            )
            if expected_source != ledger_input.tree_entry:
                raise SupplementFormatError(
                    "delta and selected source identities disagree"
                )
        for delta in manifest.delta_ledger:
            if (
                delta.category is MaterialityCategory.TEST_RESOURCE
                or delta.status is DeltaStatus.DELETED
            ) and (
                delta.extraction_roles != (ExtractionRole.IDENTITY_ONLY,)
                or delta.identity_only_reason is None
            ):
                raise SupplementFormatError(
                    "unconsumed delta path is not identity-only"
                )

    @staticmethod
    def _require_runtime_loaded_file_identities(
        report: CurrentFactSupplement, inputs: dict[str, ManifestInput]
    ) -> None:
        target_prefix = "target-source:"
        environment_prefix = "environment-file:"
        for runtime in report.runtime_observations:
            for loaded in runtime.observation.loaded_files:
                if loaded.path.startswith(target_prefix):
                    selected_path = (
                        f"python/src/{loaded.path.removeprefix(target_prefix)}"
                    )
                    selected = inputs.get(selected_path)
                    if (
                        selected is None
                        or selected.selection.variant is not InputVariant.TARGET_TREE
                        or ExtractionRole.PRODUCTION not in selected.selection.roles
                        or loaded.sha256 != selected.tree_entry.sha256
                        or loaded.byte_count != selected.tree_entry.byte_count
                    ):
                        raise SupplementFormatError(
                            "runtime target-source identity differs from selected input"
                        )
                elif loaded.path.startswith(environment_prefix):
                    if loaded.path != f"{environment_prefix}{loaded.sha256}":
                        raise SupplementFormatError(
                            "runtime environment-file marker differs from represented identity"
                        )
                else:
                    raise SupplementFormatError(
                        "runtime loaded-file identity marker is unsupported"
                    )

    @staticmethod
    def _require_role_consumption(item: ManifestInput) -> None:
        path = item.selection.path.as_posix()
        roles = item.selection.roles
        if roles == (ExtractionRole.IDENTITY_ONLY,):
            return
        if ExtractionRole.PRODUCTION in roles and (
            roles != (ExtractionRole.PRODUCTION, ExtractionRole.RUNTIME)
            or not path.startswith("python/src/")
            or not path.endswith(".py")
        ):
            raise SupplementFormatError("production/runtime role is not consumable")
        if ExtractionRole.CONSUMER in roles and not path.endswith(".py"):
            raise SupplementFormatError("consumer role requires Python input")
        if ExtractionRole.DOCUMENTATION in roles and not path.endswith((".md", ".rst")):
            raise SupplementFormatError("documentation role requires maintained prose")
        if (
            ExtractionRole.F0_LINEAGE in roles
            and path
            != "harness/reports/public-import-boundaries/phase3/foundation.json"
        ):
            raise SupplementFormatError(
                "F0 lineage role must identify accepted foundation"
            )
        if (
            ExtractionRole.TASK_TOOL in roles
            and item.selection.variant is not InputVariant.TASK_TOOL
        ):
            raise SupplementFormatError("task-tool role and source variant disagree")
        recognized = {
            ExtractionRole.AUTHORITY,
            ExtractionRole.CONSUMER,
            ExtractionRole.DOCUMENTATION,
            ExtractionRole.F0_LINEAGE,
            ExtractionRole.PRODUCTION,
            ExtractionRole.RUNTIME,
            ExtractionRole.TASK_TOOL,
        }
        if any(role not in recognized for role in roles):
            raise SupplementFormatError("non-identity extraction role is not consumed")

    @staticmethod
    def _require_occurrence_roles(
        report: CurrentFactSupplement, inputs: dict[str, ManifestInput]
    ) -> None:
        for consumer in report.consumer_imports:
            consumer_input = inputs.get(consumer.consumer_path)
            if consumer_input is None or not any(
                role in consumer_input.selection.roles
                for role in (
                    ExtractionRole.CONSUMER,
                    ExtractionRole.PRODUCTION,
                    ExtractionRole.TASK_TOOL,
                )
            ):
                raise SupplementFormatError(
                    "consumer occurrence lacks selected role owner"
                )
        for documentation in report.documentation_citations:
            documentation_input = inputs.get(documentation.path)
            if (
                documentation_input is None
                or ExtractionRole.DOCUMENTATION
                not in documentation_input.selection.roles
            ):
                raise SupplementFormatError(
                    "documentation occurrence lacks selected role owner"
                )
        for authority in report.authority_citations:
            authority_input = inputs.get(authority.path)
            if (
                authority_input is None
                or ExtractionRole.AUTHORITY not in authority_input.selection.roles
            ):
                raise SupplementFormatError(
                    "authority occurrence lacks selected role owner"
                )


class RepositoryPath:
    """Own normalized repository-relative path checks."""

    __slots__ = ()

    @staticmethod
    def require(path: PurePosixPath) -> None:
        """Require one normalized repository-relative POSIX path."""
        if type(path) is not PurePosixPath:
            raise TypeError("path must be PurePosixPath")
        rendered = path.as_posix()
        if (
            rendered in {"", "."}
            or path.is_absolute()
            or ".." in path.parts
            or "\\" in rendered
        ):
            raise ValueError("path must be normalized repository-relative POSIX")


class Identity:
    """Own exact hexadecimal identity checks."""

    __slots__ = ()

    @staticmethod
    def require_hex(value: str, length: int, label: str) -> None:
        """Require lowercase hexadecimal text of an exact length."""
        if (
            type(value) is not str
            or len(value) != length
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(
                f"{label} must be {length}-character lowercase hexadecimal"
            )

    @staticmethod
    def sha256(payload: bytes) -> str:
        """Return the SHA-256 identity of exact bytes."""
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        return hashlib.sha256(payload).hexdigest()


class SelectionSerializer:
    """Own canonical selection TSV parsing and serialization."""

    __slots__ = ()

    def decode(self, payload: bytes) -> tuple[SelectionEntry, ...]:
        """Decode a complete authored selection without path discovery."""
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SupplementFormatError("selection is not UTF-8") from exc
        rows: list[SelectionEntry] = []
        for number, line in enumerate(text.splitlines(), start=1):
            if number == 1 and line == "variant\tcategory\troles\tpath":
                continue
            fields = line.split("\t")
            if len(fields) != 4:
                raise SupplementFormatError(f"selection line {number} has four fields")
            roles = tuple(
                sorted(
                    (ExtractionRole(value) for value in fields[2].split(",")),
                    key=lambda item: item.value,
                )
            )
            rows.append(
                SelectionEntry(
                    variant=InputVariant(fields[0]),
                    category=SelectionCategory(fields[1]),
                    roles=roles,
                    path=PurePosixPath(fields[3]),
                )
            )
        ordered = tuple(sorted(rows, key=lambda item: item.sort_key))
        if not ordered or tuple(rows) != ordered:
            raise SupplementFormatError("selection rows must be canonically ordered")
        paths = tuple(row.path.as_posix() for row in rows)
        if len(paths) != len(set(paths)):
            raise SupplementFormatError("selection paths must be unique")
        return ordered

    def encode(self, entries: tuple[SelectionEntry, ...]) -> bytes:
        """Encode canonical selection bytes."""
        if entries != tuple(sorted(entries, key=lambda item: item.sort_key)):
            raise SupplementFormatError("selection rows must be canonically ordered")
        lines = ["variant\tcategory\troles\tpath"]
        lines.extend(
            f"{entry.variant.value}\t{entry.category.value}\t{','.join(role.value for role in entry.roles)}\t{entry.path.as_posix()}"
            for entry in entries
        )
        return ("\n".join(lines) + "\n").encode("utf-8")


class SupplementJsonCodec:
    """Reuse the accepted strict duplicate-key JSON codec."""

    __slots__ = ()

    def decode(self, payload: bytes) -> JsonValue:
        """Decode strict JSON bytes."""
        return FoundationJsonCodec().decode(payload)

    def encode(self, value: JsonValue) -> bytes:
        """Encode canonical JSON bytes."""
        return FoundationJsonCodec().encode(value)
