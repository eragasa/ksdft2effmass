#!/usr/bin/env python3
"""Fail-closed completion validator for the D1 geometry/sampling disposition."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass, replace
from enum import StrEnum
from pathlib import Path
from typing import TypeVar

from public_import_current_fact_supplement.command import CurrentFactSupplementParser
from python_public_import_foundation_model import (
    ClosedFoundationParser,
    FoundationJsonCodec,
    JsonRecord,
    JsonValue,
    PackageSurface,
    PredecessorRoute,
)

DispositionEnum = TypeVar("DispositionEnum", bound=StrEnum)


class SupportDisposition(StrEnum):
    """Represent one finite route-support conclusion."""

    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"
    UNRESOLVED = "unresolved"


class CompatibilityDisposition(StrEnum):
    """Represent one finite compatibility conclusion."""

    PRESERVE = "preserve"
    DEPRECATE = "deprecate"
    ALIAS = "alias"
    RETIRE = "retire"
    UNRESOLVED = "unresolved"


class BehaviorDisposition(StrEnum):
    """Represent one independent observable compatibility behavior."""

    RETAIN = "retain"
    REMOVE = "remove"
    PRESERVE_OWNER_ROUTE = "preserve_owner_route"
    NO_REPLACEMENT = "no_replacement"
    NO_WARNING_OR_FAILURE_CHANGE = "no_warning_or_failure_change"
    EMIT_DEPRECATION_WARNING = "emit_deprecation_warning"
    PRESERVE_IDENTITY_AND_GLOBAL_LOOKUP = "preserve_identity_and_global_lookup"
    IDENTITY_NOT_AVAILABLE = "identity_not_available"
    INDEFINITE = "indefinite"
    IMMEDIATE_ON_AUTHORIZED_IMPLEMENTATION = "immediate_on_authorized_implementation"
    NO_MIGRATION = "no_migration"
    USE_REPLACEMENT = "use_replacement"
    UNTIL_CONSUMERS_MIGRATE_AND_SEPARATE_REVIEW = (
        "until_consumers_migrate_and_separate_review"
    )
    NO_FAILURE_WHILE_ROUTE_RETAINED = "no_failure_while_route_retained"
    ATTRIBUTE_AND_IMPORT_FAILURE = "attribute_and_import_failure"
    UNRESOLVED = "unresolved"


class DecisionEffectState(StrEnum):
    """Distinguish a final normalized outcome from explicit reconsideration."""

    FINAL = "final_disposition"
    DEFER = "defer_and_leave_unresolved"


class DecisionReason(StrEnum):
    """Identify why a route required a human decision packet."""

    MISSING_EXACT_PACKAGE_ROUTE_AUTHORITY = "missing_exact_package_route_authority"
    NON_PRESERVE_ACCEPTED_ALIAS = "non_preserve_accepted_alias"


class DecisionState(StrEnum):
    """Represent the human-resolved decision-packet lifecycle."""

    HUMAN_SELECTED = "human_selected"


class RouteCohort(StrEnum):
    """Identify one exact cohort covered by the human D1 response."""

    ELECTRONIC_STRUCTURE_PACKAGE_ROOT = "electronic_structure_package_root"
    STRUCTURES_PACKAGE_ROOT = "structures_package_root"
    PERIODIC_COMPATIBILITY = "periodic_compatibility"


class SelectionAuthorityEffect(StrEnum):
    """Represent the bounded effect of the human D1 response."""

    ROUTE_DISPOSITIONS_ONLY = "route_dispositions_only"


class OverlayArchitecture(StrEnum):
    """Identify the accepted supplemental coverage architecture."""

    OPTION_A = "cohort_adjacent_overlay_dag"


@dataclass(frozen=True, slots=True)
class InputIdentity:
    """Bind one authority input to exact repository bytes."""

    path: str
    byte_count: int
    sha256: str

    def __post_init__(self) -> None:
        if type(self.path) is not str or not self.path:
            raise ValueError("input path must be nonempty text")
        if type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("input byte count must be a nonnegative int")
        if re.fullmatch(r"[0-9a-f]{64}", self.sha256) is None:
            raise ValueError("input SHA-256 must be lowercase hexadecimal")


@dataclass(frozen=True, slots=True)
class ExpectedOutput:
    """Bind the selected Task to its sole D1 report contract."""

    path: str
    schema_identity: str


@dataclass(frozen=True, slots=True)
class DispositionRequest:
    """Represent the stable non-self-referential selected-Task request."""

    schema_version: int
    task_id: str
    objective: str
    authority_reference_paths: tuple[str, ...]
    authorized_scope: tuple[str, ...]
    completion_criteria: tuple[str, ...]
    exclusions: tuple[str, ...]
    expected_output: ExpectedOutput
    stop_before_implementation: bool

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("request schema version must be one")
        if self.task_id != GeometrySamplingConstants.TASK_ID:
            raise ValueError("request task ID differs")
        if type(self.objective) is not str or not self.objective:
            raise ValueError("request objective must be nonempty text")
        for label, values in (
            ("authority references", self.authority_reference_paths),
            ("scope", self.authorized_scope),
            ("criteria", self.completion_criteria),
            ("exclusions", self.exclusions),
        ):
            if not values or any(
                type(value) is not str or not value for value in values
            ):
                raise ValueError(f"request {label} must contain nonempty text")
            if len(values) != len(set(values)):
                raise ValueError(f"request {label} contains duplicates")
        if self.expected_output != ExpectedOutput(
            GeometrySamplingConstants.REPORT,
            "python-public-import-geometry-sampling-disposition/v2",
        ):
            raise ValueError("request output contract differs")
        if self.stop_before_implementation is not True:
            raise ValueError("request must stop before implementation")


@dataclass(frozen=True, slots=True)
class InitializerIdentity:
    """Preserve one accepted package initializer identity."""

    path: str
    byte_count: int
    sha256: str


@dataclass(frozen=True, slots=True)
class ExactCitation:
    """Cite an exact content-identified authority statement."""

    path: str
    locator: str
    authority_statement: str

    def __post_init__(self) -> None:
        for value in (self.path, self.locator, self.authority_statement):
            if type(value) is not str or not value:
                raise ValueError("citation fields must be nonempty text")


@dataclass(frozen=True, slots=True)
class CompatibilityBehavior:
    """Represent orthogonal observable compatibility behavior."""

    all_membership: BehaviorDisposition
    explicit_binding: BehaviorDisposition
    deep_route_behavior: BehaviorDisposition
    replacement_behavior: BehaviorDisposition
    replacement_route: str | None
    warning_behavior: BehaviorDisposition
    identity_module_global_lookup: BehaviorDisposition
    duration_or_retirement_condition: BehaviorDisposition
    consumer_migration: BehaviorDisposition
    specified_failure: BehaviorDisposition

    def __post_init__(self) -> None:
        values = (
            self.all_membership,
            self.explicit_binding,
            self.deep_route_behavior,
            self.replacement_behavior,
            self.warning_behavior,
            self.identity_module_global_lookup,
            self.duration_or_retirement_condition,
            self.consumer_migration,
            self.specified_failure,
        )
        if any(type(value) is not BehaviorDisposition for value in values):
            raise TypeError("compatibility behavior uses an open disposition")
        if self.replacement_route is not None and (
            type(self.replacement_route) is not str or not self.replacement_route
        ):
            raise ValueError("replacement route must be nonempty text or null")
        if (self.replacement_behavior is BehaviorDisposition.USE_REPLACEMENT) != (
            self.replacement_route is not None
        ):
            raise ValueError("replacement behavior and route differ")
        if self.replacement_behavior is BehaviorDisposition.NO_REPLACEMENT and (
            self.replacement_route is not None
        ):
            raise ValueError("no-replacement behavior cannot name a route")


@dataclass(frozen=True, slots=True)
class DecisionOption:
    """Represent one selectable route outcome and its complete normalized effect."""

    option_id: str
    effect_state: DecisionEffectState
    support: SupportDisposition
    compatibility: CompatibilityDisposition
    compatibility_behavior: CompatibilityBehavior

    def __post_init__(self) -> None:
        if type(self.option_id) is not str or not self.option_id:
            raise ValueError("decision option ID must be nonempty text")
        if type(self.effect_state) is not DecisionEffectState:
            raise TypeError("decision effect state is open")
        if type(self.support) is not SupportDisposition:
            raise TypeError("decision support effect is open")
        if type(self.compatibility) is not CompatibilityDisposition:
            raise TypeError("decision compatibility effect is open")
        if type(self.compatibility_behavior) is not CompatibilityBehavior:
            raise TypeError("decision compatibility behavior is not closed")
        behavior_values = (
            self.compatibility_behavior.all_membership,
            self.compatibility_behavior.explicit_binding,
            self.compatibility_behavior.deep_route_behavior,
            self.compatibility_behavior.replacement_behavior,
            self.compatibility_behavior.warning_behavior,
            self.compatibility_behavior.identity_module_global_lookup,
            self.compatibility_behavior.duration_or_retirement_condition,
            self.compatibility_behavior.consumer_migration,
            self.compatibility_behavior.specified_failure,
        )
        if self.effect_state is DecisionEffectState.DEFER:
            if (
                self.support is not SupportDisposition.UNRESOLVED
                or self.compatibility is not CompatibilityDisposition.UNRESOLVED
                or any(
                    value is not BehaviorDisposition.UNRESOLVED
                    for value in behavior_values
                )
                or self.compatibility_behavior.replacement_route is not None
            ):
                raise ValueError(
                    "defer option must explicitly leave every field unresolved"
                )
        elif (
            self.support is SupportDisposition.UNRESOLVED
            or self.compatibility is CompatibilityDisposition.UNRESOLVED
            or any(value is BehaviorDisposition.UNRESOLVED for value in behavior_values)
        ):
            raise ValueError(
                "final decision option leaves a normalized field unresolved"
            )


@dataclass(frozen=True, slots=True)
class DecisionPacket:
    """Present one complete human-selected route decision."""

    packet_id: str
    route: str
    reason: DecisionReason
    decision_state: DecisionState
    selected_option_id: str
    question: str
    options: tuple[DecisionOption, ...]
    required_authority: tuple[str, ...]
    current_constraints: tuple[str, ...]
    implementation_authorized: bool

    def __post_init__(self) -> None:
        if self.packet_id != f"decision:{self.route}":
            raise ValueError("decision packet ID must derive from its route")
        if type(self.reason) is not DecisionReason:
            raise TypeError("decision reason is open")
        if self.decision_state is not DecisionState.HUMAN_SELECTED:
            raise ValueError("D1 decision packet must be human selected")
        if len(self.options) < 2 or any(
            type(value) is not DecisionOption for value in self.options
        ):
            raise ValueError("decision options are incomplete")
        option_ids = tuple(value.option_id for value in self.options)
        if len(option_ids) != len(set(option_ids)):
            raise ValueError("decision options duplicate IDs")
        selected = tuple(
            option
            for option in self.options
            if option.option_id == self.selected_option_id
        )
        if (
            len(selected) != 1
            or selected[0].effect_state is not DecisionEffectState.FINAL
        ):
            raise ValueError("decision packet must select one final option")
        for label, values in (
            ("required authority", self.required_authority),
            ("constraints", self.current_constraints),
        ):
            if len(values) < 2 or any(
                type(value) is not str or not value for value in values
            ):
                raise ValueError(f"decision {label} is incomplete")
            if len(values) != len(set(values)):
                raise ValueError(f"decision {label} duplicates values")
        if type(self.question) is not str or not self.question:
            raise ValueError("decision question must be nonempty")
        if self.implementation_authorized is not False:
            raise ValueError("decision packet cannot authorize implementation")

    def selected_option(self) -> DecisionOption:
        """Return the uniquely selected normalized option."""
        return next(
            option
            for option in self.options
            if option.option_id == self.selected_option_id
        )


@dataclass(frozen=True, slots=True)
class NormalizedCohortChoice:
    """Bind one selected option to one exact D1 route cohort."""

    cohort: RouteCohort
    route_count: int
    selected_option_id: str


@dataclass(frozen=True, slots=True)
class DispositionSelectionAuthority:
    """Preserve the human response separately from normalized cohort choices."""

    verbatim_human_response: str
    normalized_choices: tuple[NormalizedCohortChoice, ...]
    authority_effect: SelectionAuthorityEffect
    source_or_documentation_implementation_authorized: bool
    successor_activation_authorized: bool
    final_task_acceptance_authorized: bool
    commit_or_push_authorized: bool
    dependency_change_authorized: bool
    scientific_claim_authorized: bool
    release_or_publication_authorized: bool

    def __post_init__(self) -> None:
        if self.verbatim_human_response != "accept the recommend d1 route dispositions":
            raise ValueError("verbatim human D1 response differs")
        if self.normalized_choices != (
            NormalizedCohortChoice(
                RouteCohort.ELECTRONIC_STRUCTURE_PACKAGE_ROOT,
                2,
                "support_and_preserve_package_root_route",
            ),
            NormalizedCohortChoice(
                RouteCohort.PERIODIC_COMPATIBILITY,
                14,
                "accept_existing_alias_disposition_without_source_change",
            ),
            NormalizedCohortChoice(
                RouteCohort.STRUCTURES_PACKAGE_ROOT,
                12,
                "unsupported_identity_preserving_alias_to_owner",
            ),
        ):
            raise ValueError("normalized D1 cohort choices differ")
        if (
            self.authority_effect
            is not SelectionAuthorityEffect.ROUTE_DISPOSITIONS_ONLY
        ):
            raise ValueError("D1 selection authority effect differs")
        exclusions = (
            self.source_or_documentation_implementation_authorized,
            self.successor_activation_authorized,
            self.final_task_acceptance_authorized,
            self.commit_or_push_authorized,
            self.dependency_change_authorized,
            self.scientific_claim_authorized,
            self.release_or_publication_authorized,
        )
        if any(exclusions):
            raise ValueError("D1 route decision exceeds its lifecycle exclusions")


@dataclass(frozen=True, slots=True)
class RouteDisposition:
    """Represent one predecessor route and its orthogonal D1 dispositions."""

    route: str
    package: str
    exported_name: str
    predecessor_defining_module: str
    predecessor_defining_symbol: str
    predecessor_support_status: str
    predecessor_compatibility_disposition: str
    predecessor_lineage: str
    direct_origin: str
    defining_origin: str
    initializer: InitializerIdentity
    support: SupportDisposition
    support_authority: tuple[ExactCitation, ...]
    support_documentation: tuple[ExactCitation, ...]
    compatibility: CompatibilityDisposition
    compatibility_behavior: CompatibilityBehavior
    compatibility_authority: tuple[ExactCitation, ...]
    decision_packet_id: str | None

    def __post_init__(self) -> None:
        for value in (
            self.route,
            self.package,
            self.exported_name,
            self.predecessor_defining_module,
            self.predecessor_defining_symbol,
            self.predecessor_support_status,
            self.predecessor_compatibility_disposition,
            self.predecessor_lineage,
            self.direct_origin,
            self.defining_origin,
        ):
            if type(value) is not str or not value:
                raise ValueError("route lineage fields must be nonempty text")
        if self.route != f"{self.package}.{self.exported_name}":
            raise ValueError("route does not agree with package and exported name")
        if type(self.initializer) is not InitializerIdentity:
            raise TypeError("initializer identity is not closed")
        if type(self.support) is not SupportDisposition:
            raise TypeError("support disposition is open")
        if type(self.compatibility) is not CompatibilityDisposition:
            raise TypeError("compatibility disposition is open")
        if type(self.compatibility_behavior) is not CompatibilityBehavior:
            raise TypeError("compatibility behavior is not closed")
        if any(type(item) is not ExactCitation for item in self.support_authority):
            raise TypeError("support authority citations are not closed")
        if any(type(item) is not ExactCitation for item in self.support_documentation):
            raise TypeError("support documentation citations are not closed")
        if any(
            type(item) is not ExactCitation for item in self.compatibility_authority
        ):
            raise TypeError("compatibility authority citations are not closed")
        if self.support is SupportDisposition.UNRESOLVED:
            if self.support_authority:
                raise ValueError("unresolved support cannot claim sufficient authority")
        elif not self.support_authority or not self.support_documentation:
            raise ValueError("resolved support needs authority and documentation")
        if (
            self.compatibility is not CompatibilityDisposition.UNRESOLVED
            and not self.compatibility_authority
        ):
            raise ValueError("resolved compatibility needs accepted authority")


@dataclass(frozen=True, slots=True)
class SupplementalOverlayContext:
    """Reference accepted Option A without applying a D1 candidate disposition."""

    architecture: OverlayArchitecture
    reconciliation_path: str
    reconciliation_sha256: str
    d1_owner_key: str
    overlay_owner_keys: tuple[str, ...]
    supplemental_candidates_on_d1_surfaces: tuple[str, ...]
    disposition_applied: bool

    def __post_init__(self) -> None:
        if self.architecture is not OverlayArchitecture.OPTION_A:
            raise ValueError("supplemental context must reference accepted Option A")
        if self.d1_owner_key != "D1":
            raise ValueError("D1 owner key differs")
        if self.overlay_owner_keys != (
            "S01_ANALYSIS_MODEL_SYSTEMS",
            "S02_RESEARCH_MONOGRAPH_CAMPAIGNS",
            "S03_WANNIER90",
            "S04_OPERATOR_SUPPLEMENT",
            "S05_SERIALIZATION",
            "S06_SOLID_STATE",
        ):
            raise ValueError("Option A overlay owner keys differ")
        if self.supplemental_candidates_on_d1_surfaces:
            raise ValueError("D1 surfaces unexpectedly contain supplemental candidates")
        if self.disposition_applied is not False:
            raise ValueError("D1 cannot disposition supplemental candidates")


@dataclass(frozen=True, slots=True)
class ClaimBoundaries:
    """Keep the D1 result within software/public-contract decision support."""

    dependency_acceptance: str
    implementation_completion: str
    numerical_verification: str
    publication: str
    release: str
    scientific_validation: str
    uncertainty_quantification: str

    def __post_init__(self) -> None:
        if (
            self.dependency_acceptance,
            self.implementation_completion,
            self.numerical_verification,
            self.publication,
            self.release,
            self.scientific_validation,
            self.uncertainty_quantification,
        ) != ("none",) * 7:
            raise ValueError("D1 claim boundaries must remain neutral")


@dataclass(frozen=True, slots=True)
class FocusedProbeResult:
    """Record exact rejection labels and the decoded cross-view regression path."""

    rejected_labels: tuple[str, ...]
    origin_decoded_then_reconstruction_rejected: bool


@dataclass(frozen=True, slots=True)
class DispositionSummary:
    """Record cardinalities derived from the route matrix."""

    route_count: int
    surface_count: int
    supported_count: int
    unsupported_count: int
    support_unresolved_count: int
    preserve_count: int
    deprecate_count: int
    alias_count: int
    retire_count: int
    compatibility_unresolved_count: int
    decision_packet_count: int


@dataclass(frozen=True, slots=True)
class GeometrySamplingDisposition:
    """Represent the complete closed D1 disposition matrix."""

    schema_version: int
    subject_identity: str
    request: DispositionRequest
    request_sha256: str
    input_identities: tuple[InputIdentity, ...]
    surfaces: tuple[str, ...]
    routes: tuple[RouteDisposition, ...]
    decision_packets: tuple[DecisionPacket, ...]
    selection_authority: DispositionSelectionAuthority
    supplemental_overlay_context: SupplementalOverlayContext
    claim_boundaries: ClaimBoundaries
    summary: DispositionSummary

    def __post_init__(self) -> None:
        if (self.schema_version, self.subject_identity) != (
            2,
            "python-public-import-geometry-sampling-disposition",
        ):
            raise ValueError("D1 artifact identity differs")
        if re.fullmatch(r"[0-9a-f]{64}", self.request_sha256) is None:
            raise ValueError("request identity is invalid")
        if self.surfaces != GeometrySamplingConstants.SURFACES:
            raise ValueError("D1 surfaces differ")
        route_keys = tuple(item.route for item in self.routes)
        if route_keys != tuple(sorted(route_keys)) or len(set(route_keys)) != 28:
            raise ValueError("D1 routes must be 28 unique sorted keys")
        if {item.package for item in self.routes} != set(self.surfaces):
            raise ValueError("D1 route package coverage differs")
        packet_ids = tuple(item.packet_id for item in self.decision_packets)
        if packet_ids != tuple(sorted(packet_ids)) or len(packet_ids) != len(
            set(packet_ids)
        ):
            raise ValueError("decision packets must be sorted and unique")
        expected_packet_ids = {item.decision_packet_id for item in self.routes}
        if None in expected_packet_ids:
            raise ValueError("selected route lacks a decision packet")
        if set(packet_ids) != expected_packet_ids:
            raise ValueError("decision packet closure differs from route triggers")
        if {item.route for item in self.decision_packets} != {
            item.route for item in self.routes if item.decision_packet_id is not None
        }:
            raise ValueError("decision packet route closure differs")
        packets_by_id = {item.packet_id: item for item in self.decision_packets}
        for route in self.routes:
            if route.decision_packet_id is None:
                raise ValueError("selected D1 route lacks a decision packet")
            selected = packets_by_id[route.decision_packet_id].selected_option()
            if (
                route.support,
                route.compatibility,
                route.compatibility_behavior,
            ) != (
                selected.support,
                selected.compatibility,
                selected.compatibility_behavior,
            ):
                raise ValueError("selected option and normalized route outcome differ")
        cohort_counts: dict[tuple[RouteCohort, str], int] = {}
        for packet in self.decision_packets:
            route = next(item for item in self.routes if item.route == packet.route)
            cohort = (
                RouteCohort.ELECTRONIC_STRUCTURE_PACKAGE_ROOT
                if route.package == "ksdft2effmass.electronic_structure"
                else RouteCohort.PERIODIC_COMPATIBILITY
                if route.package == "ksdft2effmass.periodic"
                else RouteCohort.STRUCTURES_PACKAGE_ROOT
            )
            key = (cohort, packet.selected_option_id)
            cohort_counts[key] = cohort_counts.get(key, 0) + 1
        expected_cohorts = {
            (choice.cohort, choice.selected_option_id): choice.route_count
            for choice in self.selection_authority.normalized_choices
        }
        if cohort_counts != expected_cohorts:
            raise ValueError("packet selections differ from normalized cohort choices")
        expected_summary = DispositionSummary(
            route_count=len(self.routes),
            surface_count=len(self.surfaces),
            supported_count=sum(
                item.support is SupportDisposition.SUPPORTED for item in self.routes
            ),
            unsupported_count=sum(
                item.support is SupportDisposition.UNSUPPORTED for item in self.routes
            ),
            support_unresolved_count=sum(
                item.support is SupportDisposition.UNRESOLVED for item in self.routes
            ),
            preserve_count=sum(
                item.compatibility is CompatibilityDisposition.PRESERVE
                for item in self.routes
            ),
            deprecate_count=sum(
                item.compatibility is CompatibilityDisposition.DEPRECATE
                for item in self.routes
            ),
            alias_count=sum(
                item.compatibility is CompatibilityDisposition.ALIAS
                for item in self.routes
            ),
            retire_count=sum(
                item.compatibility is CompatibilityDisposition.RETIRE
                for item in self.routes
            ),
            compatibility_unresolved_count=sum(
                item.compatibility is CompatibilityDisposition.UNRESOLVED
                for item in self.routes
            ),
            decision_packet_count=len(self.decision_packets),
        )
        if self.summary != expected_summary:
            raise ValueError("D1 summary is not derived from routes")
        if expected_summary != DispositionSummary(28, 3, 16, 12, 0, 2, 0, 26, 0, 0, 28):
            raise ValueError("D1 disposition counts differ")


class GeometrySamplingConstants:
    """Own exact task-local paths and finite D1 surface constants."""

    TASK_ID = "python.architecture-refactor.public-import-boundaries.geometry-sampling-disposition"
    TASK = "tasks/software/python.architecture-refactor.public-import-boundaries.geometry-sampling-disposition.json"
    PARENT = "tasks/software/python.architecture-refactor.public-import-boundaries.json"
    PHASE_FOUR = "tasks/software/python.architecture-refactor.module-decomposition.json"
    OWNERSHIP = ".pi/task-ownership/python.architecture-refactor.public-import-boundaries.geometry-sampling-disposition.json"
    VALIDATOR = ".pi/task-ownership/validate_python_public_import_geometry_sampling_disposition.py"
    REPORT = "harness/reports/public-import-boundaries/phase3/geometry-sampling.json"
    FOUNDATION = "harness/reports/public-import-boundaries/phase3/foundation.json"
    SUPPLEMENT = (
        "harness/reports/public-import-boundaries/phase3/current-fact-supplement.json"
    )
    RECONCILIATION = "harness/reports/public-import-boundaries/phase3/disposition-coverage-reconciliation.json"
    SURFACES = (
        "ksdft2effmass.electronic_structure",
        "ksdft2effmass.periodic",
        "ksdft2effmass.structures",
    )
    RECORDED_PHASE_THREE_TASK_IDS = (
        "python.architecture-refactor.public-import-boundaries",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.adversarial-validation",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.aggregate-verification",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.closed-domain-contract",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.initializer-acquisition-closure",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.lifecycle-validator-correction",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.runtime-file-completeness",
        "python.architecture-refactor.public-import-boundaries.current-fact-foundation.typed-domain-construction",
        "python.architecture-refactor.public-import-boundaries.current-fact-supplement",
        "python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation",
        TASK_ID,
    )
    INPUT_PATHS = (
        "AGENTS.md",
        ".pi/task-ownership/python.architecture-refactor.public-import-boundaries.geometry-sampling-disposition.json",
        "docs/api/periodic-records.rst",
        "docs/architecture/migration/v1-to-v2/implementation/periodic-contract-verification.md",
        "docs/architecture/migration/v1-to-v2/index.md",
        "docs/architecture/v2/index.md",
        "docs/architecture/v2/ksdft2effmass/periodic/index.md",
        "docs/architecture/v2/ksdft2effmass/structures-package-boundary-decision.md",
        "docs/architecture/v2/ksdft2effmass/structures/index.md",
        "docs/architecture/v2/ksdft2effmass/structures/periodic.md",
        "docs/architecture/v2/repository-layout.md",
        "docs/development/source-documentation.rst",
        "harness/reports/public-import-boundaries/phase3/current-fact-supplement.json",
        "harness/reports/public-import-boundaries/phase3/disposition-coverage-reconciliation.json",
        "harness/reports/public-import-boundaries/phase3/foundation.json",
        "harness/reports/python-public-import-boundaries-plan.md",
        "tasks/software/migration.v2.periodic.json",
        "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.json",
        "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json",
        "tasks/software/python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation.json",
        "tasks/software/python.architecture-refactor.public-import-boundaries.geometry-sampling-disposition.json",
        "tasks/software/python.architecture-refactor.public-import-boundaries.json",
    )


class DispositionRequestSerializer:
    """Own canonical request representation and identity."""

    __slots__ = ()

    def value(self, request: DispositionRequest) -> JsonRecord:
        """Represent a closed stable request as JSON."""
        return {
            "authority_reference_paths": list(request.authority_reference_paths),
            "authorized_scope": list(request.authorized_scope),
            "completion_criteria": list(request.completion_criteria),
            "exclusions": list(request.exclusions),
            "expected_output": {
                "path": request.expected_output.path,
                "schema_identity": request.expected_output.schema_identity,
            },
            "objective": request.objective,
            "schema_version": request.schema_version,
            "stop_before_implementation": request.stop_before_implementation,
            "task_id": request.task_id,
        }

    def identity(self, request: DispositionRequest) -> str:
        """Return the SHA-256 of canonical request bytes."""
        payload = FoundationJsonCodec().encode(self.value(request))
        return hashlib.sha256(payload).hexdigest()


class SelectedTaskRequestAdapter:
    """Adapt a selected Task JSON encoding to its immutable request projection."""

    __slots__ = ()

    def decode(self, payload: bytes) -> DispositionRequest:
        """Parse the exact Task shape while excluding mutable lifecycle fields."""
        root = self._closed(
            FoundationJsonCodec().decode(payload),
            {
                "archived_source",
                "authority_reference_paths",
                "authorized_scope",
                "completion_criteria",
                "exclusions",
                "explicit_activation_required",
                "external_prerequisite_ids",
                "intake_path",
                "objective",
                "parent_task_id",
                "schema_version",
                "status",
                "status_detail",
                "superseded_by_task_ids",
                "task_id",
                "task_prerequisite_ids",
                "title",
            },
            "selected Task",
        )
        if (
            root["schema_version"] != 3
            or root["explicit_activation_required"] is not True
        ):
            raise ValueError("selected Task version or activation contract differs")
        if root["status"] != "closed_human_accepted_pass":
            raise ValueError("D1 Task must be human-accepted and closed")
        return DispositionRequest(
            schema_version=1,
            task_id=self._text(root["task_id"], "task ID"),
            objective=self._text(root["objective"], "objective"),
            authority_reference_paths=self._texts(
                root["authority_reference_paths"], "authority references"
            ),
            authorized_scope=self._texts(root["authorized_scope"], "authorized scope"),
            completion_criteria=self._texts(
                root["completion_criteria"], "completion criteria"
            ),
            exclusions=self._texts(root["exclusions"], "exclusions"),
            expected_output=ExpectedOutput(
                GeometrySamplingConstants.REPORT,
                "python-public-import-geometry-sampling-disposition/v2",
            ),
            stop_before_implementation=True,
        )

    def run_drift_probes(
        self, payload: bytes, expected_identity: str
    ) -> tuple[str, ...]:
        """Reject focused stable-request mutations independently."""
        value = self._closed(
            FoundationJsonCodec().decode(payload),
            {
                "archived_source",
                "authority_reference_paths",
                "authorized_scope",
                "completion_criteria",
                "exclusions",
                "explicit_activation_required",
                "external_prerequisite_ids",
                "intake_path",
                "objective",
                "parent_task_id",
                "schema_version",
                "status",
                "status_detail",
                "superseded_by_task_ids",
                "task_id",
                "task_prerequisite_ids",
                "title",
            },
            "selected Task",
        )
        probes: list[tuple[str, JsonRecord]] = []
        for label, key in (
            ("objective", "objective"),
            ("scope", "authorized_scope"),
            ("authority", "authority_reference_paths"),
            ("exclusion", "exclusions"),
        ):
            candidate = dict(value)
            original = candidate[key]
            if type(original) is list:
                candidate[key] = [*original, f"probe-{label}"]
            else:
                candidate[key] = f"{original} probe"
            probes.append((label, candidate))
        rejected: list[str] = []
        for label, candidate in probes:
            request = self.decode(FoundationJsonCodec().encode(candidate))
            if DispositionRequestSerializer().identity(request) == expected_identity:
                raise ValueError(f"request drift probe was accepted: {label}")
            rejected.append(label)
        return tuple(rejected)

    @staticmethod
    def _closed(value: JsonValue, keys: set[str], label: str) -> JsonRecord:
        if type(value) is not dict or set(value) != keys:
            raise ValueError(f"{label} fields differ")
        return value

    @staticmethod
    def _text(value: JsonValue, label: str) -> str:
        if type(value) is not str or not value:
            raise ValueError(f"{label} must be nonempty text")
        return value

    @classmethod
    def _texts(cls, value: JsonValue, label: str) -> tuple[str, ...]:
        if type(value) is not list:
            raise ValueError(f"{label} must be an array")
        return tuple(cls._text(item, label) for item in value)


@dataclass(frozen=True, slots=True)
class AcceptedD1Facts:
    """Expose only accepted D1 lineage and current-origin facts."""

    routes: tuple[PredecessorRoute, ...]
    foundation_surfaces: tuple[PackageSurface, ...]
    supplement_surfaces: tuple[PackageSurface, ...]
    current_origins: tuple[tuple[str, str, str], ...]
    supplemental_candidate_keys: tuple[str, ...]


class AcceptedD1FactAdapter:
    """Adapt F0 and supplement through their existing closed typed parsers."""

    __slots__ = ()

    def execute(
        self, foundation_payload: bytes, supplement_payload: bytes
    ) -> AcceptedD1Facts:
        """Return the exact 28-route D1 projection after cross-view validation."""
        foundation = ClosedFoundationParser().execute(
            FoundationJsonCodec().decode(foundation_payload)
        )
        supplement = CurrentFactSupplementParser().decode(supplement_payload)
        if foundation.predecessor_routes != supplement.predecessor_routes:
            raise ValueError("F0 and supplement predecessor lineage differ")
        routes = tuple(
            item
            for item in foundation.predecessor_routes
            if item.package in GeometrySamplingConstants.SURFACES
        )
        f_surfaces = tuple(
            item
            for item in foundation.package_surfaces
            if item.package in GeometrySamplingConstants.SURFACES
        )
        s_surfaces = tuple(
            item
            for item in supplement.predecessor_package_observations
            if item.package in GeometrySamplingConstants.SURFACES
        )
        if (
            routes != tuple(sorted(routes, key=lambda item: item.route))
            or len(routes) != 28
        ):
            raise ValueError("accepted D1 predecessor projection differs")
        if f_surfaces != s_surfaces or len(f_surfaces) != 3:
            raise ValueError("accepted D1 initializer views differ")
        route_keys = {item.route for item in routes}
        origins = tuple(
            (item.route, item.direct_origin, item.defining_origin)
            for item in supplement.current_routes
            if item.route in route_keys
        )
        if tuple(key for key, _, _ in origins) != tuple(sorted(route_keys)):
            raise ValueError("current D1 route-origin coverage differs")
        candidates = tuple(
            item.candidate_key
            for item in supplement.supplemental_candidates
            if item.route.package in GeometrySamplingConstants.SURFACES
        )
        if candidates:
            raise ValueError("D1 surfaces unexpectedly gained supplemental candidates")
        return AcceptedD1Facts(routes, f_surfaces, s_surfaces, origins, candidates)


class OptionAContextAdapter:
    """Adapt the accepted reconciliation to narrow supplemental-exclusion context."""

    __slots__ = ()

    def execute(self, payload: bytes) -> SupplementalOverlayContext:
        """Validate selected Option A without propagating reconciliation JSON."""
        root = self._record(FoundationJsonCodec().decode(payload), "reconciliation")
        if root.get("schema_version") != 2:
            raise ValueError("reconciliation schema differs")
        if (
            root.get("subject_identity")
            != "python-public-import-disposition-coverage-reconciliation"
        ):
            raise ValueError("reconciliation subject differs")
        if (
            root.get("decision_state") != "human_selected"
            or root.get("selected_option") != "A"
        ):
            raise ValueError("reconciliation Option A is not human selected")
        proposed = self._record(root.get("proposed_map"), "proposed map")
        if proposed.get("architecture_key") != OverlayArchitecture.OPTION_A.value:
            raise ValueError("reconciliation architecture differs")
        if proposed.get("map_state") != "human_selected_architecture":
            raise ValueError("reconciliation map is not selected")
        owners_value = proposed.get("owners")
        if type(owners_value) is not list:
            raise ValueError("reconciliation owners must be an array")
        owner_keys: list[str] = []
        for value in owners_value:
            owner = self._record(value, "coverage owner")
            key = owner.get("owner_key")
            if type(key) is not str:
                raise ValueError("coverage owner key must be text")
            owner_keys.append(key)
        overlay_keys = tuple(key for key in owner_keys if key.startswith("S"))
        return SupplementalOverlayContext(
            architecture=OverlayArchitecture.OPTION_A,
            reconciliation_path=GeometrySamplingConstants.RECONCILIATION,
            reconciliation_sha256=hashlib.sha256(payload).hexdigest(),
            d1_owner_key="D1",
            overlay_owner_keys=overlay_keys,
            supplemental_candidates_on_d1_surfaces=(),
            disposition_applied=False,
        )

    @staticmethod
    def _record(value: JsonValue | None, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise ValueError(f"{label} must be an object")
        return value


class DispositionAuthority:
    """Own exact accepted citations and route-specific D1 adjudication policy."""

    __slots__ = ()

    def route(
        self,
        predecessor: PredecessorRoute,
        surface: PackageSurface,
        direct_origin: str,
        defining_origin: str,
    ) -> RouteDisposition:
        """Apply only conclusions fixed by exact accepted authority."""
        initializer = InitializerIdentity(
            surface.initializer_path,
            surface.initializer_byte_count,
            surface.initializer_sha256,
        )
        lineage = "accepted_f0_predecessor_route_retained_by_supplement"
        if predecessor.package == "ksdft2effmass.electronic_structure":
            replacement = (
                "ksdft2effmass.electronic_structure.sampling."
                f"{predecessor.exported_name}"
            )
            behavior = self._unresolved_behavior(replacement)
            return RouteDisposition(
                predecessor.route,
                predecessor.package,
                predecessor.exported_name,
                predecessor.defining_module,
                predecessor.defining_symbol,
                predecessor.support_status,
                predecessor.compatibility_disposition,
                lineage,
                direct_origin,
                defining_origin,
                initializer,
                SupportDisposition.UNRESOLVED,
                (),
                (
                    self._citation(
                        "docs/api/periodic-records.rst",
                        "Electronic reciprocal-space sampling",
                        f"The maintained API page documents {predecessor.route}, but documentation alone does not accept that exact package-root route.",
                    ),
                ),
                CompatibilityDisposition.UNRESOLVED,
                behavior,
                (
                    self._citation(
                        "tasks/software/migration.v2.periodic.json",
                        "status_detail and authorized_scope[4]",
                        "The accepted implementation owner is electronic_structure.sampling; it does not adjudicate package-root compatibility behavior.",
                    ),
                    self._citation(
                        "docs/architecture/v2/repository-layout.md",
                        "Package ownership: ksdft2effmass.electronic_structure",
                        "Package responsibility does not accept either exact electronic_structure package-root symbol route.",
                    ),
                ),
                f"decision:{predecessor.route}",
            )
        if predecessor.package == "ksdft2effmass.periodic":
            replacement = self._replacement(predecessor.exported_name)
            support_authority = (
                self._citation(
                    "tasks/software/migration.v2.periodic.json",
                    "status_detail and authorized_scope[4]",
                    "The human-accepted migration retains periodic as an identity-preserving compatibility surface.",
                ),
                self._citation(
                    "docs/architecture/migration/v1-to-v2/implementation/periodic-contract-verification.md",
                    "Compatibility disposition",
                    "The exact former public inventory is thirteen retained exports plus ReciprocalLatticeCompatibilityValidator.",
                ),
            )
            documentation = (
                self._citation(
                    "docs/api/periodic-records.rst",
                    "opening compatibility paragraph",
                    "The maintained API page documents periodic as the temporary former public inventory compatibility route.",
                ),
                self._citation(
                    "docs/architecture/v2/ksdft2effmass/periodic/index.md",
                    "compatibility package",
                    "The maintained package page documents the identity-preserving replacement owners.",
                ),
            )
            compatibility_authority = (
                self._citation(
                    "docs/architecture/v2/ksdft2effmass/structures-package-boundary-decision.md",
                    "Migration and compatibility",
                    "The existing periodic public import remains a bounded compatibility surface and gains no new behavior.",
                ),
                self._citation(
                    "docs/architecture/migration/v1-to-v2/index.md",
                    "Package ownership map: ksdft2effmass.periodic",
                    "The accepted disposition is split and move with a temporary identity-preserving compatibility import.",
                ),
            )
            behavior = CompatibilityBehavior(
                BehaviorDisposition.RETAIN,
                BehaviorDisposition.RETAIN,
                BehaviorDisposition.PRESERVE_OWNER_ROUTE,
                BehaviorDisposition.USE_REPLACEMENT,
                replacement,
                BehaviorDisposition.NO_WARNING_OR_FAILURE_CHANGE,
                BehaviorDisposition.PRESERVE_IDENTITY_AND_GLOBAL_LOOKUP,
                BehaviorDisposition.UNTIL_CONSUMERS_MIGRATE_AND_SEPARATE_REVIEW,
                BehaviorDisposition.USE_REPLACEMENT,
                BehaviorDisposition.NO_FAILURE_WHILE_ROUTE_RETAINED,
            )
            return RouteDisposition(
                predecessor.route,
                predecessor.package,
                predecessor.exported_name,
                predecessor.defining_module,
                predecessor.defining_symbol,
                predecessor.support_status,
                predecessor.compatibility_disposition,
                lineage,
                direct_origin,
                defining_origin,
                initializer,
                SupportDisposition.SUPPORTED,
                support_authority,
                documentation,
                CompatibilityDisposition.ALIAS,
                behavior,
                compatibility_authority,
                f"decision:{predecessor.route}",
            )
        behavior = self._unresolved_behavior(
            f"ksdft2effmass.structures.periodic.{predecessor.exported_name}"
        )
        return RouteDisposition(
            predecessor.route,
            predecessor.package,
            predecessor.exported_name,
            predecessor.defining_module,
            predecessor.defining_symbol,
            predecessor.support_status,
            predecessor.compatibility_disposition,
            lineage,
            direct_origin,
            defining_origin,
            initializer,
            SupportDisposition.UNRESOLVED,
            (),
            (
                self._citation(
                    "docs/api/periodic-records.rst",
                    "Periodic crystal geometry",
                    "Maintained public documentation names structures.periodic, not the predecessor structures package-root route.",
                ),
                self._citation(
                    "docs/architecture/v2/ksdft2effmass/structures/index.md",
                    "initial public surface",
                    "The namespace page identifies structures.periodic as the initial public surface without adjudicating package-root re-exports.",
                ),
            ),
            CompatibilityDisposition.UNRESOLVED,
            behavior,
            (
                self._citation(
                    "tasks/software/migration.v2.periodic.json",
                    "status_detail and authorized_scope[4]",
                    "The accepted defining owner and replacement route are structures.periodic; this does not adjudicate the package-root compatibility behaviors.",
                ),
                self._citation(
                    "docs/architecture/v2/ksdft2effmass/structures-package-boundary-decision.md",
                    "Selected architecture",
                    "The accepted architecture fixes the structures.periodic owner while leaving the predecessor package-root route without an exact disposition.",
                ),
            ),
            f"decision:{predecessor.route}",
        )

    def packet(self, route: RouteDisposition) -> DecisionPacket:
        """Build one complete human-selected packet with normalized effects."""
        if route.package == "ksdft2effmass.periodic":
            return DecisionPacket(
                f"decision:{route.route}",
                route.route,
                DecisionReason.NON_PRESERVE_ACCEPTED_ALIAS,
                DecisionState.HUMAN_SELECTED,
                "accept_existing_alias_disposition_without_source_change",
                f"Accept the complete existing alias disposition for {route.route}, or explicitly defer it for reconsideration?",
                (
                    DecisionOption(
                        "accept_existing_alias_disposition_without_source_change",
                        DecisionEffectState.FINAL,
                        route.support,
                        route.compatibility,
                        route.compatibility_behavior,
                    ),
                    self._defer_option(
                        "defer_and_reconsider_route_specific_compatibility"
                    ),
                ),
                (
                    "human acceptance of one normalized reviewed D1 route outcome",
                    "separate authority before any warning, retirement, failure, or source mutation",
                ),
                (
                    f"accepted replacement owner is {route.compatibility_behavior.replacement_route}",
                    "same object identity, __module__, global lookup, and defining owner currently remain preserved",
                    "D1 itself introduces no warning or removal",
                    "retirement remains conditional on consumer migration and separate review unless a later decision supersedes it",
                ),
                False,
            )
        replacement = route.compatibility_behavior.replacement_route
        if replacement is None:
            raise ValueError(
                "missing-authority packet requires an accepted owner route"
            )
        return DecisionPacket(
            f"decision:{route.route}",
            route.route,
            DecisionReason.MISSING_EXACT_PACKAGE_ROUTE_AUTHORITY,
            DecisionState.HUMAN_SELECTED,
            (
                "support_and_preserve_package_root_route"
                if route.package == "ksdft2effmass.electronic_structure"
                else "unsupported_identity_preserving_alias_to_owner"
            ),
            f"Which complete support and compatibility outcome should govern {route.route}?",
            (
                DecisionOption(
                    "support_and_preserve_package_root_route",
                    DecisionEffectState.FINAL,
                    SupportDisposition.SUPPORTED,
                    CompatibilityDisposition.PRESERVE,
                    self._preserve_behavior(),
                ),
                DecisionOption(
                    "unsupported_identity_preserving_alias_to_owner",
                    DecisionEffectState.FINAL,
                    SupportDisposition.UNSUPPORTED,
                    CompatibilityDisposition.ALIAS,
                    self._alias_behavior(replacement),
                ),
                DecisionOption(
                    "unsupported_deprecation_to_owner",
                    DecisionEffectState.FINAL,
                    SupportDisposition.UNSUPPORTED,
                    CompatibilityDisposition.DEPRECATE,
                    self._deprecation_behavior(replacement),
                ),
                DecisionOption(
                    "unsupported_retirement_in_favor_of_owner",
                    DecisionEffectState.FINAL,
                    SupportDisposition.UNSUPPORTED,
                    CompatibilityDisposition.RETIRE,
                    self._retirement_behavior(replacement),
                ),
                self._defer_option("defer_and_leave_every_disposition_unresolved"),
            ),
            (
                "human selection of one normalized route-specific public-contract outcome",
                "synchronized maintained public documentation for the selected exact route status",
                "separate implementation authority for any initializer, consumer, warning, or failure change",
            ),
            (
                f"accepted defining owner route is {replacement}",
                "importability and __all__ membership do not establish support",
                "absence of exact authority cannot establish unsupported or retirement",
                "D1 records the human-selected route disposition and authorizes no mutation",
            ),
            False,
        )

    def selected_route(
        self, route: RouteDisposition, packet: DecisionPacket
    ) -> RouteDisposition:
        """Apply one human-selected packet to its normalized route outcome."""
        selected = packet.selected_option()
        if route.package == "ksdft2effmass.periodic":
            return route
        decision_citation = self._citation(
            GeometrySamplingConstants.TASK,
            "status_detail: human D1 route-disposition decision",
            (
                "The exact human response selects "
                f"{packet.selected_option_id} for {route.route}; it records only the "
                "route disposition and does not authorize implementation or final acceptance."
            ),
        )
        return replace(
            route,
            support=selected.support,
            support_authority=(decision_citation,),
            compatibility=selected.compatibility,
            compatibility_behavior=selected.compatibility_behavior,
            compatibility_authority=(
                *route.compatibility_authority,
                decision_citation,
            ),
        )

    @staticmethod
    def _preserve_behavior() -> CompatibilityBehavior:
        return CompatibilityBehavior(
            BehaviorDisposition.RETAIN,
            BehaviorDisposition.RETAIN,
            BehaviorDisposition.PRESERVE_OWNER_ROUTE,
            BehaviorDisposition.NO_REPLACEMENT,
            None,
            BehaviorDisposition.NO_WARNING_OR_FAILURE_CHANGE,
            BehaviorDisposition.PRESERVE_IDENTITY_AND_GLOBAL_LOOKUP,
            BehaviorDisposition.INDEFINITE,
            BehaviorDisposition.NO_MIGRATION,
            BehaviorDisposition.NO_WARNING_OR_FAILURE_CHANGE,
        )

    @staticmethod
    def _alias_behavior(replacement: str) -> CompatibilityBehavior:
        return CompatibilityBehavior(
            BehaviorDisposition.RETAIN,
            BehaviorDisposition.RETAIN,
            BehaviorDisposition.PRESERVE_OWNER_ROUTE,
            BehaviorDisposition.USE_REPLACEMENT,
            replacement,
            BehaviorDisposition.NO_WARNING_OR_FAILURE_CHANGE,
            BehaviorDisposition.PRESERVE_IDENTITY_AND_GLOBAL_LOOKUP,
            BehaviorDisposition.UNTIL_CONSUMERS_MIGRATE_AND_SEPARATE_REVIEW,
            BehaviorDisposition.USE_REPLACEMENT,
            BehaviorDisposition.NO_FAILURE_WHILE_ROUTE_RETAINED,
        )

    @staticmethod
    def _deprecation_behavior(replacement: str) -> CompatibilityBehavior:
        return CompatibilityBehavior(
            BehaviorDisposition.RETAIN,
            BehaviorDisposition.RETAIN,
            BehaviorDisposition.PRESERVE_OWNER_ROUTE,
            BehaviorDisposition.USE_REPLACEMENT,
            replacement,
            BehaviorDisposition.EMIT_DEPRECATION_WARNING,
            BehaviorDisposition.PRESERVE_IDENTITY_AND_GLOBAL_LOOKUP,
            BehaviorDisposition.UNTIL_CONSUMERS_MIGRATE_AND_SEPARATE_REVIEW,
            BehaviorDisposition.USE_REPLACEMENT,
            BehaviorDisposition.NO_FAILURE_WHILE_ROUTE_RETAINED,
        )

    @staticmethod
    def _retirement_behavior(replacement: str) -> CompatibilityBehavior:
        return CompatibilityBehavior(
            BehaviorDisposition.REMOVE,
            BehaviorDisposition.REMOVE,
            BehaviorDisposition.PRESERVE_OWNER_ROUTE,
            BehaviorDisposition.USE_REPLACEMENT,
            replacement,
            BehaviorDisposition.NO_WARNING_OR_FAILURE_CHANGE,
            BehaviorDisposition.IDENTITY_NOT_AVAILABLE,
            BehaviorDisposition.IMMEDIATE_ON_AUTHORIZED_IMPLEMENTATION,
            BehaviorDisposition.USE_REPLACEMENT,
            BehaviorDisposition.ATTRIBUTE_AND_IMPORT_FAILURE,
        )

    @staticmethod
    def _unresolved_behavior(replacement: str) -> CompatibilityBehavior:
        return CompatibilityBehavior(
            BehaviorDisposition.UNRESOLVED,
            BehaviorDisposition.UNRESOLVED,
            BehaviorDisposition.PRESERVE_OWNER_ROUTE,
            BehaviorDisposition.USE_REPLACEMENT,
            replacement,
            BehaviorDisposition.UNRESOLVED,
            BehaviorDisposition.UNRESOLVED,
            BehaviorDisposition.UNRESOLVED,
            BehaviorDisposition.UNRESOLVED,
            BehaviorDisposition.UNRESOLVED,
        )

    @staticmethod
    def _defer_option(option_id: str) -> DecisionOption:
        return DecisionOption(
            option_id,
            DecisionEffectState.DEFER,
            SupportDisposition.UNRESOLVED,
            CompatibilityDisposition.UNRESOLVED,
            CompatibilityBehavior(
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
                None,
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
                BehaviorDisposition.UNRESOLVED,
            ),
        )

    @staticmethod
    def _replacement(name: str) -> str:
        owner = (
            "ksdft2effmass.electronic_structure.sampling"
            if name in {"KPointSampling", "KPointWeightNormalization"}
            else "ksdft2effmass.structures.periodic"
        )
        return f"{owner}.{name}"

    @staticmethod
    def _citation(path: str, locator: str, statement: str) -> ExactCitation:
        return ExactCitation(path, locator, statement)


class GeometrySamplingDispositionAssembler:
    """Assemble the expected D1 artifact from explicit accepted inputs."""

    __slots__ = ("repository_root",)

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def execute(self) -> GeometrySamplingDisposition:
        """Return a deterministic closed artifact without mutating the repository."""
        request = SelectedTaskRequestAdapter().decode(
            (self.repository_root / GeometrySamplingConstants.TASK).read_bytes()
        )
        facts = AcceptedD1FactAdapter().execute(
            (self.repository_root / GeometrySamplingConstants.FOUNDATION).read_bytes(),
            (self.repository_root / GeometrySamplingConstants.SUPPLEMENT).read_bytes(),
        )
        origins = {
            route: (direct, defining)
            for route, direct, defining in facts.current_origins
        }
        surfaces = {surface.package: surface for surface in facts.foundation_surfaces}
        authority = DispositionAuthority()
        provisional_routes = tuple(
            authority.route(item, surfaces[item.package], *origins[item.route])
            for item in facts.routes
        )
        packets = tuple(
            sorted(
                (
                    authority.packet(route)
                    for route in provisional_routes
                    if route.decision_packet_id is not None
                ),
                key=lambda item: item.packet_id,
            )
        )
        packets_by_route = {packet.route: packet for packet in packets}
        routes = tuple(
            authority.selected_route(route, packets_by_route[route.route])
            for route in provisional_routes
        )
        selection_authority = DispositionSelectionAuthority(
            "accept the recommend d1 route dispositions",
            (
                NormalizedCohortChoice(
                    RouteCohort.ELECTRONIC_STRUCTURE_PACKAGE_ROOT,
                    2,
                    "support_and_preserve_package_root_route",
                ),
                NormalizedCohortChoice(
                    RouteCohort.PERIODIC_COMPATIBILITY,
                    14,
                    "accept_existing_alias_disposition_without_source_change",
                ),
                NormalizedCohortChoice(
                    RouteCohort.STRUCTURES_PACKAGE_ROOT,
                    12,
                    "unsupported_identity_preserving_alias_to_owner",
                ),
            ),
            SelectionAuthorityEffect.ROUTE_DISPOSITIONS_ONLY,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        )
        identities = tuple(
            self._identity(path) for path in GeometrySamplingConstants.INPUT_PATHS
        )
        overlay = OptionAContextAdapter().execute(
            (
                self.repository_root / GeometrySamplingConstants.RECONCILIATION
            ).read_bytes()
        )
        return GeometrySamplingDisposition(
            2,
            "python-public-import-geometry-sampling-disposition",
            request,
            DispositionRequestSerializer().identity(request),
            identities,
            GeometrySamplingConstants.SURFACES,
            routes,
            packets,
            selection_authority,
            overlay,
            ClaimBoundaries("none", "none", "none", "none", "none", "none", "none"),
            DispositionSummary(28, 3, 16, 12, 0, 2, 0, 26, 0, 0, 28),
        )

    def _identity(self, path: str) -> InputIdentity:
        payload = (self.repository_root / path).read_bytes()
        return InputIdentity(path, len(payload), hashlib.sha256(payload).hexdigest())


class GeometrySamplingDispositionSerializer:
    """Own canonical serialization of the closed D1 artifact."""

    __slots__ = ()

    def encode(self, artifact: GeometrySamplingDisposition) -> bytes:
        """Encode one validated artifact as canonical UTF-8 JSON."""
        return FoundationJsonCodec().encode(self.value(artifact))

    def value(self, artifact: GeometrySamplingDisposition) -> JsonRecord:
        """Represent one validated artifact without erased domain containers."""
        decision_values: list[JsonValue] = [
            self._packet(item) for item in artifact.decision_packets
        ]
        identity_values: list[JsonValue] = [
            {
                "byte_count": item.byte_count,
                "path": item.path,
                "sha256": item.sha256,
            }
            for item in artifact.input_identities
        ]
        route_values: list[JsonValue] = [self._route(item) for item in artifact.routes]
        return {
            "claim_boundaries": {
                "dependency_acceptance": artifact.claim_boundaries.dependency_acceptance,
                "implementation_completion": artifact.claim_boundaries.implementation_completion,
                "numerical_verification": artifact.claim_boundaries.numerical_verification,
                "publication": artifact.claim_boundaries.publication,
                "release": artifact.claim_boundaries.release,
                "scientific_validation": artifact.claim_boundaries.scientific_validation,
                "uncertainty_quantification": artifact.claim_boundaries.uncertainty_quantification,
            },
            "decision_packets": decision_values,
            "input_identities": identity_values,
            "request": DispositionRequestSerializer().value(artifact.request),
            "request_sha256": artifact.request_sha256,
            "routes": route_values,
            "schema_version": artifact.schema_version,
            "selection_authority": {
                "authority_effect": artifact.selection_authority.authority_effect.value,
                "commit_or_push_authorized": artifact.selection_authority.commit_or_push_authorized,
                "dependency_change_authorized": artifact.selection_authority.dependency_change_authorized,
                "final_task_acceptance_authorized": artifact.selection_authority.final_task_acceptance_authorized,
                "normalized_choices": [
                    {
                        "cohort": choice.cohort.value,
                        "route_count": choice.route_count,
                        "selected_option_id": choice.selected_option_id,
                    }
                    for choice in artifact.selection_authority.normalized_choices
                ],
                "release_or_publication_authorized": artifact.selection_authority.release_or_publication_authorized,
                "scientific_claim_authorized": artifact.selection_authority.scientific_claim_authorized,
                "source_or_documentation_implementation_authorized": artifact.selection_authority.source_or_documentation_implementation_authorized,
                "successor_activation_authorized": artifact.selection_authority.successor_activation_authorized,
                "verbatim_human_response": artifact.selection_authority.verbatim_human_response,
            },
            "subject_identity": artifact.subject_identity,
            "summary": {
                "alias_count": artifact.summary.alias_count,
                "compatibility_unresolved_count": artifact.summary.compatibility_unresolved_count,
                "decision_packet_count": artifact.summary.decision_packet_count,
                "deprecate_count": artifact.summary.deprecate_count,
                "preserve_count": artifact.summary.preserve_count,
                "retire_count": artifact.summary.retire_count,
                "route_count": artifact.summary.route_count,
                "support_unresolved_count": artifact.summary.support_unresolved_count,
                "supported_count": artifact.summary.supported_count,
                "surface_count": artifact.summary.surface_count,
                "unsupported_count": artifact.summary.unsupported_count,
            },
            "supplemental_overlay_context": {
                "architecture": artifact.supplemental_overlay_context.architecture.value,
                "d1_owner_key": artifact.supplemental_overlay_context.d1_owner_key,
                "disposition_applied": artifact.supplemental_overlay_context.disposition_applied,
                "overlay_owner_keys": list(
                    artifact.supplemental_overlay_context.overlay_owner_keys
                ),
                "reconciliation_path": artifact.supplemental_overlay_context.reconciliation_path,
                "reconciliation_sha256": artifact.supplemental_overlay_context.reconciliation_sha256,
                "supplemental_candidates_on_d1_surfaces": list(
                    artifact.supplemental_overlay_context.supplemental_candidates_on_d1_surfaces
                ),
            },
            "surfaces": list(artifact.surfaces),
        }

    def _route(self, item: RouteDisposition) -> JsonRecord:
        return {
            "compatibility": item.compatibility.value,
            "compatibility_authority": [
                self._citation(value) for value in item.compatibility_authority
            ],
            "compatibility_behavior": self._behavior(item.compatibility_behavior),
            "decision_packet_id": item.decision_packet_id,
            "defining_origin": item.defining_origin,
            "direct_origin": item.direct_origin,
            "exported_name": item.exported_name,
            "initializer": {
                "byte_count": item.initializer.byte_count,
                "path": item.initializer.path,
                "sha256": item.initializer.sha256,
            },
            "package": item.package,
            "predecessor_compatibility_disposition": item.predecessor_compatibility_disposition,
            "predecessor_defining_module": item.predecessor_defining_module,
            "predecessor_defining_symbol": item.predecessor_defining_symbol,
            "predecessor_lineage": item.predecessor_lineage,
            "predecessor_support_status": item.predecessor_support_status,
            "route": item.route,
            "support": item.support.value,
            "support_authority": [
                self._citation(value) for value in item.support_authority
            ],
            "support_documentation": [
                self._citation(value) for value in item.support_documentation
            ],
        }

    @staticmethod
    def _citation(item: ExactCitation) -> JsonRecord:
        return {
            "authority_statement": item.authority_statement,
            "locator": item.locator,
            "path": item.path,
        }

    @staticmethod
    def _behavior(item: CompatibilityBehavior) -> JsonRecord:
        return {
            "all_membership": item.all_membership.value,
            "consumer_migration": item.consumer_migration.value,
            "deep_route_behavior": item.deep_route_behavior.value,
            "duration_or_retirement_condition": item.duration_or_retirement_condition.value,
            "explicit_binding": item.explicit_binding.value,
            "identity_module_global_lookup": item.identity_module_global_lookup.value,
            "replacement_behavior": item.replacement_behavior.value,
            "replacement_route": item.replacement_route,
            "specified_failure": item.specified_failure.value,
            "warning_behavior": item.warning_behavior.value,
        }

    @classmethod
    def _packet(cls, item: DecisionPacket) -> JsonRecord:
        return {
            "current_constraints": list(item.current_constraints),
            "decision_state": item.decision_state.value,
            "implementation_authorized": item.implementation_authorized,
            "options": [cls._option(option) for option in item.options],
            "packet_id": item.packet_id,
            "question": item.question,
            "reason": item.reason.value,
            "required_authority": list(item.required_authority),
            "route": item.route,
            "selected_option_id": item.selected_option_id,
        }

    @classmethod
    def _option(cls, item: DecisionOption) -> JsonRecord:
        return {
            "compatibility": item.compatibility.value,
            "compatibility_behavior": cls._behavior(item.compatibility_behavior),
            "effect_state": item.effect_state.value,
            "option_id": item.option_id,
            "support": item.support.value,
        }


class GeometrySamplingDispositionParser:
    """Convert D1 JSON bytes immediately into frozen closed domain records."""

    __slots__ = ()

    def decode(self, payload: bytes) -> GeometrySamplingDisposition:
        """Reject duplicate keys, unknown fields, open variants, and relation defects."""
        root = self._closed(
            FoundationJsonCodec().decode(payload),
            {
                "claim_boundaries",
                "decision_packets",
                "input_identities",
                "request",
                "request_sha256",
                "routes",
                "schema_version",
                "selection_authority",
                "subject_identity",
                "summary",
                "supplemental_overlay_context",
                "surfaces",
            },
            "artifact",
        )
        artifact = GeometrySamplingDisposition(
            self._integer(root["schema_version"], "schema version"),
            self._text(root["subject_identity"], "subject identity"),
            self._request(root["request"]),
            self._sha(root["request_sha256"], "request SHA-256"),
            tuple(
                self._input(item, index)
                for index, item in enumerate(
                    self._array(root["input_identities"], "input identities")
                )
            ),
            self._texts(root["surfaces"], "surfaces"),
            tuple(
                self._route(item, index)
                for index, item in enumerate(self._array(root["routes"], "routes"))
            ),
            tuple(
                self._packet(item, index)
                for index, item in enumerate(
                    self._array(root["decision_packets"], "decision packets")
                )
            ),
            self._selection_authority(root["selection_authority"]),
            self._overlay(root["supplemental_overlay_context"]),
            self._claims(root["claim_boundaries"]),
            self._summary(root["summary"]),
        )
        if (
            DispositionRequestSerializer().identity(artifact.request)
            != artifact.request_sha256
        ):
            raise ValueError("embedded request identity differs")
        citation_paths = {
            citation.path
            for route in artifact.routes
            for citation in (
                *route.support_authority,
                *route.support_documentation,
                *route.compatibility_authority,
            )
        }
        identity_paths = {item.path for item in artifact.input_identities}
        if not citation_paths <= identity_paths:
            raise ValueError("a route citation lacks an exact input identity")
        return artifact

    def run_probes(
        self, payload: bytes, expected: GeometrySamplingDisposition
    ) -> FocusedProbeResult:
        """Reject malformed mutations, including decoded cross-view drift."""
        original = self._closed(
            FoundationJsonCodec().decode(payload),
            {
                "claim_boundaries",
                "decision_packets",
                "input_identities",
                "request",
                "request_sha256",
                "routes",
                "schema_version",
                "selection_authority",
                "subject_identity",
                "summary",
                "supplemental_overlay_context",
                "surfaces",
            },
            "artifact",
        )
        probes: list[tuple[str, bytes]] = []
        probes.append(
            (
                "duplicate-key",
                payload.replace(
                    b'{"claim_boundaries":',
                    b'{"schema_version":1,"claim_boundaries":',
                    1,
                ),
            )
        )
        extra = dict(original)
        extra["unknown"] = "probe"
        probes.append(("closed-root", FoundationJsonCodec().encode(extra)))
        routes = self._records(original["routes"], "routes")
        missing = dict(original)
        missing_routes: list[JsonValue] = list(routes[:-1])
        missing["routes"] = missing_routes
        probes.append(("route-coverage", FoundationJsonCodec().encode(missing)))
        origin_routes = [dict(item) for item in routes]
        origin_routes[0]["defining_origin"] = "ksdft2effmass.wrong.Symbol"
        origin = dict(original)
        origin_values: list[JsonValue] = list(origin_routes)
        origin["routes"] = origin_values
        probes.append(("origin-cross-view", FoundationJsonCodec().encode(origin)))
        authority_routes = [dict(item) for item in routes]
        for item in authority_routes:
            if item.get("support") == "supported":
                item["support_authority"] = []
                break
        authority = dict(original)
        authority_values: list[JsonValue] = list(authority_routes)
        authority["routes"] = authority_values
        probes.append(
            ("authority-sufficiency", FoundationJsonCodec().encode(authority))
        )
        packet = dict(original)
        packet_values: list[JsonValue] = list(
            self._records(original["decision_packets"], "packets")[:-1]
        )
        packet["decision_packets"] = packet_values
        probes.append(("decision-closure", FoundationJsonCodec().encode(packet)))
        selection_value = self._closed(
            original["selection_authority"],
            {
                "authority_effect",
                "commit_or_push_authorized",
                "dependency_change_authorized",
                "final_task_acceptance_authorized",
                "normalized_choices",
                "release_or_publication_authorized",
                "scientific_claim_authorized",
                "source_or_documentation_implementation_authorized",
                "successor_activation_authorized",
                "verbatim_human_response",
            },
            "selection authority",
        )
        response_mutated = dict(selection_value)
        response_mutated["verbatim_human_response"] = "recommendation authorized"
        response = dict(original)
        response["selection_authority"] = response_mutated
        probes.append(("human-response-drift", FoundationJsonCodec().encode(response)))
        cohort_mutated = dict(selection_value)
        cohort_choices: list[JsonValue] = [
            dict(item)
            for item in self._records(
                selection_value["normalized_choices"], "normalized choices"
            )
        ]
        first_choice = cohort_choices[0]
        if type(first_choice) is not dict:
            raise ValueError("normalized choice probe is not an object")
        first_choice["selected_option_id"] = (
            "unsupported_identity_preserving_alias_to_owner"
        )
        cohort_mutated["normalized_choices"] = cohort_choices
        cohort = dict(original)
        cohort["selection_authority"] = cohort_mutated
        probes.append(("cohort-choice-drift", FoundationJsonCodec().encode(cohort)))
        packet_drift = dict(original)
        selected_packets: list[JsonValue] = [
            dict(item)
            for item in self._records(original["decision_packets"], "packets")
        ]
        first_packet = selected_packets[0]
        if type(first_packet) is not dict:
            raise ValueError("decision packet probe is not an object")
        first_packet["selected_option_id"] = (
            "unsupported_identity_preserving_alias_to_owner"
        )
        packet_drift["decision_packets"] = selected_packets
        probes.append(
            ("packet-selection-drift", FoundationJsonCodec().encode(packet_drift))
        )
        outcome = dict(original)
        outcome_routes: list[JsonValue] = [dict(item) for item in routes]
        first_route = outcome_routes[0]
        if type(first_route) is not dict:
            raise ValueError("route outcome probe is not an object")
        first_route["support"] = "unsupported"
        outcome["routes"] = outcome_routes
        probes.append(("selected-outcome-drift", FoundationJsonCodec().encode(outcome)))
        overlay_value = self._closed(
            original["supplemental_overlay_context"],
            {
                "architecture",
                "d1_owner_key",
                "disposition_applied",
                "overlay_owner_keys",
                "reconciliation_path",
                "reconciliation_sha256",
                "supplemental_candidates_on_d1_surfaces",
            },
            "overlay",
        )
        overlay_mutated = dict(overlay_value)
        overlay_mutated["disposition_applied"] = True
        overlay = dict(original)
        overlay["supplemental_overlay_context"] = overlay_mutated
        probes.append(("supplemental-exclusion", FoundationJsonCodec().encode(overlay)))
        rejected: list[str] = []
        origin_decoded_then_rejected = False
        for label, candidate in probes:
            try:
                parsed = self.decode(candidate)
            except (TypeError, ValueError, UnicodeError):
                rejected.append(label)
                continue
            if parsed != expected:
                rejected.append(label)
                if label == "origin-cross-view":
                    origin_decoded_then_rejected = True
                continue
            raise ValueError(f"focused malformed probe was accepted: {label}")
        return FocusedProbeResult(tuple(rejected), origin_decoded_then_rejected)

    def _request(self, value: JsonValue) -> DispositionRequest:
        row = self._closed(
            value,
            {
                "authority_reference_paths",
                "authorized_scope",
                "completion_criteria",
                "exclusions",
                "expected_output",
                "objective",
                "schema_version",
                "stop_before_implementation",
                "task_id",
            },
            "request",
        )
        output = self._closed(
            row["expected_output"], {"path", "schema_identity"}, "expected output"
        )
        return DispositionRequest(
            self._integer(row["schema_version"], "request version"),
            self._text(row["task_id"], "request task ID"),
            self._text(row["objective"], "request objective"),
            self._texts(row["authority_reference_paths"], "request authority"),
            self._texts(row["authorized_scope"], "request scope"),
            self._texts(row["completion_criteria"], "request criteria"),
            self._texts(row["exclusions"], "request exclusions"),
            ExpectedOutput(
                self._text(output["path"], "output path"),
                self._text(output["schema_identity"], "output schema"),
            ),
            self._boolean(
                row["stop_before_implementation"], "stop before implementation"
            ),
        )

    def _input(self, value: JsonValue, index: int) -> InputIdentity:
        row = self._closed(value, {"byte_count", "path", "sha256"}, f"input[{index}]")
        return InputIdentity(
            self._text(row["path"], "input path"),
            self._nonnegative(row["byte_count"], "input bytes"),
            self._sha(row["sha256"], "input SHA"),
        )

    def _route(self, value: JsonValue, index: int) -> RouteDisposition:
        row = self._closed(
            value,
            {
                "compatibility",
                "compatibility_authority",
                "compatibility_behavior",
                "decision_packet_id",
                "defining_origin",
                "direct_origin",
                "exported_name",
                "initializer",
                "package",
                "predecessor_compatibility_disposition",
                "predecessor_defining_module",
                "predecessor_defining_symbol",
                "predecessor_lineage",
                "predecessor_support_status",
                "route",
                "support",
                "support_authority",
                "support_documentation",
            },
            f"route[{index}]",
        )
        initializer = self._closed(
            row["initializer"], {"byte_count", "path", "sha256"}, "initializer"
        )
        behavior = self._closed(
            row["compatibility_behavior"],
            {
                "all_membership",
                "consumer_migration",
                "deep_route_behavior",
                "duration_or_retirement_condition",
                "explicit_binding",
                "identity_module_global_lookup",
                "replacement_behavior",
                "replacement_route",
                "specified_failure",
                "warning_behavior",
            },
            "compatibility behavior",
        )
        return RouteDisposition(
            self._text(row["route"], "route"),
            self._text(row["package"], "package"),
            self._text(row["exported_name"], "exported name"),
            self._text(row["predecessor_defining_module"], "predecessor module"),
            self._text(row["predecessor_defining_symbol"], "predecessor symbol"),
            self._text(row["predecessor_support_status"], "predecessor support"),
            self._text(
                row["predecessor_compatibility_disposition"],
                "predecessor compatibility",
            ),
            self._text(row["predecessor_lineage"], "lineage"),
            self._text(row["direct_origin"], "direct origin"),
            self._text(row["defining_origin"], "defining origin"),
            InitializerIdentity(
                self._text(initializer["path"], "initializer path"),
                self._nonnegative(initializer["byte_count"], "initializer bytes"),
                self._sha(initializer["sha256"], "initializer SHA"),
            ),
            self._enum(SupportDisposition, row["support"], "support"),
            self._citations(row["support_authority"], "support authority"),
            self._citations(row["support_documentation"], "support documentation"),
            self._enum(CompatibilityDisposition, row["compatibility"], "compatibility"),
            self._behavior(behavior, "route compatibility behavior"),
            self._citations(row["compatibility_authority"], "compatibility authority"),
            self._optional_text(row["decision_packet_id"], "decision packet ID"),
        )

    def _packet(self, value: JsonValue, index: int) -> DecisionPacket:
        row = self._closed(
            value,
            {
                "current_constraints",
                "decision_state",
                "implementation_authorized",
                "options",
                "packet_id",
                "question",
                "reason",
                "required_authority",
                "route",
                "selected_option_id",
            },
            f"packet[{index}]",
        )
        return DecisionPacket(
            self._text(row["packet_id"], "packet ID"),
            self._text(row["route"], "packet route"),
            self._enum(DecisionReason, row["reason"], "decision reason"),
            self._enum(DecisionState, row["decision_state"], "decision state"),
            self._text(row["selected_option_id"], "selected option ID"),
            self._text(row["question"], "decision question"),
            tuple(
                self._option(item, option_index)
                for option_index, item in enumerate(
                    self._array(row["options"], "decision options")
                )
            ),
            self._texts(row["required_authority"], "required authority"),
            self._texts(row["current_constraints"], "constraints"),
            self._boolean(
                row["implementation_authorized"], "implementation authorized"
            ),
        )

    def _option(self, value: JsonValue, index: int) -> DecisionOption:
        row = self._closed(
            value,
            {
                "compatibility",
                "compatibility_behavior",
                "effect_state",
                "option_id",
                "support",
            },
            f"decision option[{index}]",
        )
        return DecisionOption(
            self._text(row["option_id"], "decision option ID"),
            self._enum(
                DecisionEffectState, row["effect_state"], "decision effect state"
            ),
            self._enum(SupportDisposition, row["support"], "decision support"),
            self._enum(
                CompatibilityDisposition,
                row["compatibility"],
                "decision compatibility",
            ),
            self._behavior(
                row["compatibility_behavior"], "decision compatibility behavior"
            ),
        )

    def _behavior(self, value: JsonValue, label: str) -> CompatibilityBehavior:
        row = self._closed(
            value,
            {
                "all_membership",
                "consumer_migration",
                "deep_route_behavior",
                "duration_or_retirement_condition",
                "explicit_binding",
                "identity_module_global_lookup",
                "replacement_behavior",
                "replacement_route",
                "specified_failure",
                "warning_behavior",
            },
            label,
        )
        return CompatibilityBehavior(
            self._enum(BehaviorDisposition, row["all_membership"], "all membership"),
            self._enum(
                BehaviorDisposition, row["explicit_binding"], "explicit binding"
            ),
            self._enum(BehaviorDisposition, row["deep_route_behavior"], "deep route"),
            self._enum(BehaviorDisposition, row["replacement_behavior"], "replacement"),
            self._optional_text(row["replacement_route"], "replacement route"),
            self._enum(BehaviorDisposition, row["warning_behavior"], "warning"),
            self._enum(
                BehaviorDisposition,
                row["identity_module_global_lookup"],
                "identity",
            ),
            self._enum(
                BehaviorDisposition,
                row["duration_or_retirement_condition"],
                "duration",
            ),
            self._enum(BehaviorDisposition, row["consumer_migration"], "migration"),
            self._enum(BehaviorDisposition, row["specified_failure"], "failure"),
        )

    def _selection_authority(self, value: JsonValue) -> DispositionSelectionAuthority:
        row = self._closed(
            value,
            {
                "authority_effect",
                "commit_or_push_authorized",
                "dependency_change_authorized",
                "final_task_acceptance_authorized",
                "normalized_choices",
                "release_or_publication_authorized",
                "scientific_claim_authorized",
                "source_or_documentation_implementation_authorized",
                "successor_activation_authorized",
                "verbatim_human_response",
            },
            "selection authority",
        )
        choices = tuple(
            self._normalized_choice(item, index)
            for index, item in enumerate(
                self._array(row["normalized_choices"], "normalized choices")
            )
        )
        return DispositionSelectionAuthority(
            self._text(row["verbatim_human_response"], "verbatim human response"),
            choices,
            self._enum(
                SelectionAuthorityEffect,
                row["authority_effect"],
                "selection authority effect",
            ),
            self._boolean(
                row["source_or_documentation_implementation_authorized"],
                "source or documentation implementation authority",
            ),
            self._boolean(
                row["successor_activation_authorized"],
                "successor activation authority",
            ),
            self._boolean(
                row["final_task_acceptance_authorized"],
                "final task acceptance authority",
            ),
            self._boolean(row["commit_or_push_authorized"], "commit or push authority"),
            self._boolean(
                row["dependency_change_authorized"], "dependency change authority"
            ),
            self._boolean(
                row["scientific_claim_authorized"], "scientific claim authority"
            ),
            self._boolean(
                row["release_or_publication_authorized"],
                "release or publication authority",
            ),
        )

    def _normalized_choice(
        self, value: JsonValue, index: int
    ) -> NormalizedCohortChoice:
        row = self._closed(
            value,
            {"cohort", "route_count", "selected_option_id"},
            f"normalized choice[{index}]",
        )
        return NormalizedCohortChoice(
            self._enum(RouteCohort, row["cohort"], "route cohort"),
            self._nonnegative(row["route_count"], "route count"),
            self._text(row["selected_option_id"], "selected option ID"),
        )

    def _overlay(self, value: JsonValue) -> SupplementalOverlayContext:
        row = self._closed(
            value,
            {
                "architecture",
                "d1_owner_key",
                "disposition_applied",
                "overlay_owner_keys",
                "reconciliation_path",
                "reconciliation_sha256",
                "supplemental_candidates_on_d1_surfaces",
            },
            "overlay",
        )
        return SupplementalOverlayContext(
            self._enum(
                OverlayArchitecture, row["architecture"], "overlay architecture"
            ),
            self._text(row["reconciliation_path"], "reconciliation path"),
            self._sha(row["reconciliation_sha256"], "reconciliation SHA"),
            self._text(row["d1_owner_key"], "D1 owner"),
            self._texts(row["overlay_owner_keys"], "overlay owners"),
            self._texts(row["supplemental_candidates_on_d1_surfaces"], "D1 candidates"),
            self._boolean(row["disposition_applied"], "disposition applied"),
        )

    def _claims(self, value: JsonValue) -> ClaimBoundaries:
        row = self._closed(
            value,
            {
                "dependency_acceptance",
                "implementation_completion",
                "numerical_verification",
                "publication",
                "release",
                "scientific_validation",
                "uncertainty_quantification",
            },
            "claim boundaries",
        )
        return ClaimBoundaries(
            *(
                self._text(row[key], key)
                for key in (
                    "dependency_acceptance",
                    "implementation_completion",
                    "numerical_verification",
                    "publication",
                    "release",
                    "scientific_validation",
                    "uncertainty_quantification",
                )
            )
        )

    def _summary(self, value: JsonValue) -> DispositionSummary:
        row = self._closed(
            value,
            {
                "alias_count",
                "compatibility_unresolved_count",
                "decision_packet_count",
                "deprecate_count",
                "preserve_count",
                "retire_count",
                "route_count",
                "support_unresolved_count",
                "supported_count",
                "surface_count",
                "unsupported_count",
            },
            "summary",
        )
        return DispositionSummary(
            *(
                self._nonnegative(row[key], key)
                for key in (
                    "route_count",
                    "surface_count",
                    "supported_count",
                    "unsupported_count",
                    "support_unresolved_count",
                    "preserve_count",
                    "deprecate_count",
                    "alias_count",
                    "retire_count",
                    "compatibility_unresolved_count",
                    "decision_packet_count",
                )
            )
        )

    def _citations(self, value: JsonValue, label: str) -> tuple[ExactCitation, ...]:
        return tuple(self._citation(item, label) for item in self._array(value, label))

    def _citation(self, value: JsonValue, label: str) -> ExactCitation:
        row = self._closed(value, {"authority_statement", "locator", "path"}, label)
        return ExactCitation(
            self._text(row["path"], "citation path"),
            self._text(row["locator"], "citation locator"),
            self._text(row["authority_statement"], "authority statement"),
        )

    @staticmethod
    def _closed(value: JsonValue, keys: set[str], label: str) -> JsonRecord:
        if type(value) is not dict or set(value) != keys:
            raise ValueError(f"{label} fields differ")
        return value

    @staticmethod
    def _array(value: JsonValue, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise ValueError(f"{label} must be an array")
        return value

    @classmethod
    def _records(cls, value: JsonValue, label: str) -> list[JsonRecord]:
        records: list[JsonRecord] = []
        for item in cls._array(value, label):
            if type(item) is not dict:
                raise ValueError(f"{label} must contain objects")
            records.append(item)
        return records

    @staticmethod
    def _text(value: JsonValue, label: str) -> str:
        if type(value) is not str or not value:
            raise ValueError(f"{label} must be nonempty text")
        return value

    @classmethod
    def _optional_text(cls, value: JsonValue, label: str) -> str | None:
        if value is None:
            return None
        return cls._text(value, label)

    @classmethod
    def _texts(cls, value: JsonValue, label: str) -> tuple[str, ...]:
        return tuple(cls._text(item, label) for item in cls._array(value, label))

    @staticmethod
    def _integer(value: JsonValue, label: str) -> int:
        if type(value) is not int:
            raise ValueError(f"{label} must be an int")
        return value

    @classmethod
    def _nonnegative(cls, value: JsonValue, label: str) -> int:
        number = cls._integer(value, label)
        if number < 0:
            raise ValueError(f"{label} must be nonnegative")
        return number

    @classmethod
    def _sha(cls, value: JsonValue, label: str) -> str:
        text = cls._text(value, label)
        if re.fullmatch(r"[0-9a-f]{64}", text) is None:
            raise ValueError(f"{label} must be SHA-256 text")
        return text

    @staticmethod
    def _boolean(value: JsonValue, label: str) -> bool:
        if type(value) is not bool:
            raise ValueError(f"{label} must be a bool")
        return value

    @classmethod
    def _enum(
        cls,
        enum_type: type[DispositionEnum],
        value: JsonValue,
        label: str,
    ) -> DispositionEnum:
        text = cls._text(value, label)
        try:
            return enum_type(text)
        except ValueError as exc:
            raise ValueError(f"{label} has an unsupported value") from exc


@dataclass(frozen=True, slots=True)
class GeometrySamplingLifecycle:
    """Expose the bounded selected-task lifecycle projection."""

    active_task_id: str | None
    receipt_ids: tuple[str, ...]
    automatic_activation: bool
    task_status: str
    task_detail: str
    parent_status: str
    parent_detail: str
    phase_four_status: str


class GeometrySamplingLifecycleAdapter:
    """Parse selected-task and parent lifecycle without open JSON propagation."""

    __slots__ = ()

    def execute(
        self,
        selection_payload: bytes,
        task_payload: bytes,
        parent_payload: bytes,
        phase_four_payload: bytes,
    ) -> GeometrySamplingLifecycle:
        """Return the exact lifecycle fields required by D1 validation."""
        codec = FoundationJsonCodec()
        selection = self._record(codec.decode(selection_payload), "selection")
        task = self._record(codec.decode(task_payload), "task")
        parent = self._record(codec.decode(parent_payload), "parent")
        phase_four = self._record(codec.decode(phase_four_payload), "Phase 4")
        active = selection.get("active_task_id")
        if active is not None and type(active) is not str:
            raise ValueError("active task ID must be text or null")
        receipts = selection.get("explicit_activation_receipt_ids")
        if type(receipts) is not list or any(
            type(item) is not str for item in receipts
        ):
            raise ValueError("selection receipts differ")
        automatic = selection.get("automatic_successor_activation")
        if type(automatic) is not bool:
            raise ValueError("automatic activation must be bool")
        status = self._text(task.get("status"), "task status")
        detail = self._text(task.get("status_detail"), "task detail")
        parent_status = self._text(parent.get("status"), "parent status")
        parent_detail = self._text(parent.get("status_detail"), "parent detail")
        phase_four_status = self._text(phase_four.get("status"), "Phase 4 status")
        return GeometrySamplingLifecycle(
            active,
            tuple(self._text(item, "selection receipt") for item in receipts),
            automatic,
            status,
            detail,
            parent_status,
            parent_detail,
            phase_four_status,
        )

    def validate_successors_inactive(self, task_graph_payload: bytes) -> None:
        """Reject a recorded D2+ disposition, overlay, mutation, or implementation."""
        root = self._record(
            FoundationJsonCodec().decode(task_graph_payload), "task graph"
        )
        nodes = root.get("nodes")
        if type(nodes) is not list:
            raise ValueError("task graph nodes must be an array")
        prefix = "python.architecture-refactor.public-import-boundaries"
        observed: set[str] = set()
        for index, value in enumerate(nodes):
            node = self._record(value, f"task graph node[{index}]")
            task_id = self._text(node.get("task_id"), "task graph task ID")
            if task_id == prefix or task_id.startswith(f"{prefix}."):
                observed.add(task_id)
        expected = set(GeometrySamplingConstants.RECORDED_PHASE_THREE_TASK_IDS)
        if observed != expected:
            extra = sorted(observed - expected)
            missing = sorted(expected - observed)
            raise ValueError(
                f"Phase 3 recorded successor set differs: extra={extra}, missing={missing}"
            )

    @staticmethod
    def _record(value: JsonValue, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise ValueError(f"{label} must be an object")
        return value

    @staticmethod
    def _text(value: JsonValue | None, label: str) -> str:
        if type(value) is not str or not value:
            raise ValueError(f"{label} must be nonempty text")
        return value


@dataclass(frozen=True, slots=True)
class GeometrySamplingDispositionCompletionValidator:
    """Own all deterministic no-argument D1 completion gates."""

    repository_root: Path

    def execute(self) -> int:
        """Validate artifact, drift, lifecycle, ownership, projections, and tooling."""
        try:
            self._validate_permitted_delta()
            report_payload = (
                self.repository_root / GeometrySamplingConstants.REPORT
            ).read_bytes()
            parser = GeometrySamplingDispositionParser()
            artifact = parser.decode(report_payload)
            if (
                GeometrySamplingDispositionSerializer().encode(artifact)
                != report_payload
            ):
                raise ValueError("D1 report bytes are not canonical")
            expected = GeometrySamplingDispositionAssembler(
                self.repository_root
            ).execute()
            if artifact != expected:
                raise ValueError("D1 report differs from accepted-input reconstruction")
            for identity in artifact.input_identities:
                payload = (self.repository_root / identity.path).read_bytes()
                if (
                    len(payload) != identity.byte_count
                    or hashlib.sha256(payload).hexdigest() != identity.sha256
                ):
                    raise ValueError(f"authority input drift: {identity.path}")
            task_payload = (
                self.repository_root / GeometrySamplingConstants.TASK
            ).read_bytes()
            request = SelectedTaskRequestAdapter().decode(task_payload)
            if (
                request != artifact.request
                or DispositionRequestSerializer().identity(request)
                != artifact.request_sha256
            ):
                raise ValueError("live stable Task request differs")
            facts = AcceptedD1FactAdapter().execute(
                (
                    self.repository_root / GeometrySamplingConstants.FOUNDATION
                ).read_bytes(),
                (
                    self.repository_root / GeometrySamplingConstants.SUPPLEMENT
                ).read_bytes(),
            )
            if tuple(item.route for item in facts.routes) != tuple(
                item.route for item in artifact.routes
            ):
                raise ValueError("accepted D1 route keys differ")
            self._validate_lifecycle()
            probes = parser.run_probes(report_payload, expected)
            drift = SelectedTaskRequestAdapter().run_drift_probes(
                task_payload, artifact.request_sha256
            )
            expected_probe_labels = (
                "duplicate-key",
                "closed-root",
                "route-coverage",
                "origin-cross-view",
                "authority-sufficiency",
                "decision-closure",
                "human-response-drift",
                "cohort-choice-drift",
                "packet-selection-drift",
                "selected-outcome-drift",
                "supplemental-exclusion",
            )
            if (
                probes.rejected_labels != expected_probe_labels
                or not probes.origin_decoded_then_reconstruction_rejected
                or len(drift) != 4
            ):
                raise ValueError("focused probe regression assertion failed")
            print("focused D1 probes rejected: " + "; ".join(probes.rejected_labels))
            print(
                "origin-cross-view regression: decoder accepted mutation; accepted-input reconstruction rejected it"
            )
            print("stable request drift probes rejected: " + "; ".join(drift))
            print(
                f"canonical D1 artifact: {len(report_payload)} bytes sha256={hashlib.sha256(report_payload).hexdigest()}"
            )
        except (OSError, TypeError, ValueError, UnicodeError) as exc:
            return self._fail(f"closed geometry/sampling validation failed: {exc}")
        interpreter = self.repository_root / "python/.venv/bin/python"
        commands: tuple[tuple[str | Path, ...], ...] = (
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-task-ownership",
                "--repository-root",
                self.repository_root,
                "--task",
                GeometrySamplingConstants.TASK_ID,
                "--task-record",
                self.repository_root / GeometrySamplingConstants.TASK,
                "--ownership-manifest",
                self.repository_root / GeometrySamplingConstants.OWNERSHIP,
            ),
            (interpreter, "-m", "ruff", "check", GeometrySamplingConstants.VALIDATOR),
            (
                interpreter,
                "-m",
                "ruff",
                "format",
                "--check",
                GeometrySamplingConstants.VALIDATOR,
            ),
            (
                interpreter,
                "-m",
                "mypy",
                "--strict",
                GeometrySamplingConstants.VALIDATOR,
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "harness-projection",
                "--repository-root",
                self.repository_root,
                "check",
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-harness",
                "--repository-root",
                self.repository_root,
            ),
            ("git", "-C", self.repository_root, "diff", "--check"),
        )
        environment = {
            **os.environ,
            "MYPYPATH": f"{self.repository_root / '.pi/task-ownership'}:{self.repository_root / 'python/src'}",
        }
        for command in commands:
            if self._run(command, environment) != 0:
                return 1
        print("geometry/sampling disposition completion validation passed")
        return 0

    def _validate_lifecycle(self) -> None:
        adapter = GeometrySamplingLifecycleAdapter()
        state = adapter.execute(
            (self.repository_root / "harness/task-selection.json").read_bytes(),
            (self.repository_root / GeometrySamplingConstants.TASK).read_bytes(),
            (self.repository_root / GeometrySamplingConstants.PARENT).read_bytes(),
            (self.repository_root / GeometrySamplingConstants.PHASE_FOUR).read_bytes(),
        )
        if state != GeometrySamplingLifecycle(
            None,
            (),
            False,
            "closed_human_accepted_pass",
            state.task_detail,
            "deferred_between_children",
            state.parent_detail,
            "inactive",
        ):
            raise ValueError("accepted D1 closeout lifecycle differs")
        exact_acceptance = (
            "responded exactly `recommendation authorized` to the immediately pending "
            "recommendation `Accept D1 and authorize managed administrative closeout. "
            "Keep all successors and automatic activation inactive.`"
        )
        normalized_closeout = (
            "The exact response is preserved separately from the normalized closeout "
            "decision: accept the reviewed D1 route-disposition result and authorize "
            "one validated non-amended managed administrative closeout commit on `dev`"
        )
        required = (
            "accept the recommend d1 route dispositions",
            "All 28 decision packets are now `human_selected`",
            exact_acceptance,
            normalized_closeout,
            "D1 is `closed_human_accepted_pass`",
            "D2–D21, S01–S06, M1, implementation children, V1, and Phase 4 remain inactive",
            "automatic successor activation remains false",
        )
        if any(fragment not in state.task_detail for fragment in required):
            raise ValueError("accepted D1 Task detail is incomplete")
        if any(
            fragment not in state.parent_detail
            for fragment in (
                exact_acceptance,
                normalized_closeout,
                "D1 is `closed_human_accepted_pass`",
                "D2–D21, S01–S06, M1, implementation children, V1, and Phase 4 remain inactive",
            )
        ):
            raise ValueError("accepted D1 parent detail is incomplete")
        adapter.validate_successors_inactive(
            (self.repository_root / "harness/task-graph.json").read_bytes()
        )

    def _validate_permitted_delta(self) -> None:
        permitted = {
            GeometrySamplingConstants.OWNERSHIP,
            GeometrySamplingConstants.VALIDATOR,
            GeometrySamplingConstants.REPORT,
            "harness/state/harness-control.sql",
            "harness/state/harness-control.sqlite3",
            "harness/state/projection-manifest.json",
            "harness/task-graph.json",
            "harness/task-selection.json",
            GeometrySamplingConstants.TASK,
            GeometrySamplingConstants.PARENT,
        }
        completed = subprocess.run(
            (
                "git",
                "-C",
                str(self.repository_root),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ),
            check=False,
            capture_output=True,
            env={"LANG": "C", "LC_ALL": "C", "PATH": os.defpath},
        )
        if completed.returncode != 0:
            raise ValueError("cannot inspect working-tree delta")
        observed: set[str] = set()
        for line in completed.stdout.decode("utf-8").splitlines():
            if (
                len(line) < 4
                or line[2] != " "
                or line[0] not in {" ", "?"}
                or " -> " in line[3:]
            ):
                raise ValueError("working-tree record is staged, renamed, or malformed")
            observed.add(line[3:])
        unexpected = observed - permitted
        if unexpected:
            raise ValueError(
                f"working-tree path is outside ownership: {min(unexpected)}"
            )

    def _run(self, command: tuple[str | Path, ...], environment: dict[str, str]) -> int:
        completed = subprocess.run(
            tuple(str(value) for value in command),
            cwd=self.repository_root,
            env=environment,
            check=False,
        )
        if completed.returncode != 0:
            print(
                f"completion command failed: {' '.join(str(value) for value in command)}",
                file=sys.stderr,
            )
        return completed.returncode

    @staticmethod
    def _fail(message: str) -> int:
        print(message, file=sys.stderr)
        return 1


def main() -> int:
    """Adapt the process entry point required by Python execution."""
    if len(sys.argv) != 1:
        print(
            "geometry/sampling disposition validator takes no arguments",
            file=sys.stderr,
        )
        return 1
    return GeometrySamplingDispositionCompletionValidator(
        Path(__file__).resolve().parents[2]
    ).execute()


if __name__ == "__main__":
    raise SystemExit(main())
