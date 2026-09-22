#!/usr/bin/env python3
"""Fail-closed completion validator for disposition-coverage reconciliation."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from public_import_current_fact_supplement.command import CurrentFactSupplementParser
from python_public_import_foundation_model import (
    ClosedFoundationParser,
    FoundationJsonCodec,
    JsonRecord,
    JsonValue,
)


class OptionKey(Enum):
    """Identify one finite advisory architecture choice."""

    A = "A"
    B = "B"
    C = "C"


class CheckpointKey(Enum):
    """Identify one finite human checkpoint response."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"


class ArchitectureKey(Enum):
    """Identify one finite architecture model."""

    COHORT_OVERLAY = "cohort_adjacent_overlay_dag"
    CENTRAL = "central_coverage_authority"
    SURFACE_SHARDS = "surface_shards_with_join"


class DecisionState(Enum):
    """Represent the human-resolved packet lifecycle."""

    HUMAN_SELECTED = "human_selected"


class MapState(Enum):
    """Represent the selected-map lifecycle."""

    HUMAN_SELECTED = "human_selected_architecture"


class SelectionAuthorityEffect(Enum):
    """Represent the finite authority granted by the two human responses."""

    RECORD_ARCHITECTURE_ONLY = "durable_architecture_selection_only"


class OwnerKind(Enum):
    """Identify a finite planning-owner kind."""

    PREDECESSOR = "accepted_predecessor_cohort"
    OVERLAY = "proposed_supplemental_overlay"


class OwnerKey(Enum):
    """Identify one exact finite predecessor or overlay owner."""

    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    D5 = "D5"
    D6 = "D6"
    D7 = "D7"
    D8 = "D8"
    D9 = "D9"
    D10 = "D10"
    D11 = "D11"
    D12 = "D12"
    D13 = "D13"
    D14 = "D14"
    D15 = "D15"
    D16 = "D16"
    D17 = "D17"
    D18 = "D18"
    D19 = "D19"
    D20 = "D20"
    D21 = "D21"
    S01 = "S01_ANALYSIS_MODEL_SYSTEMS"
    S02 = "S02_RESEARCH_MONOGRAPH_CAMPAIGNS"
    S03 = "S03_WANNIER90"
    S04 = "S04_OPERATOR_SUPPLEMENT"
    S05 = "S05_SERIALIZATION"
    S06 = "S06_SOLID_STATE"


class SurfaceLineage(Enum):
    """Identify a finite surface-lineage kind."""

    ACCEPTED = "accepted_f0_surface"
    SUPPLEMENTAL = "supplemental_surface"


class CandidateResolution(Enum):
    """Represent the sole neutral candidate assignment state."""

    ASSIGNED = "assigned_for_later_neutral_disposition"


@dataclass(frozen=True, slots=True)
class ExpectedOutput:
    """Bind one request output path to its closed schema identity."""

    path: str
    schema_identity: str


@dataclass(frozen=True, slots=True)
class ReconciliationRequest:
    """Represent the immutable non-self-referential decision request."""

    schema_version: int
    task_id: str
    decision_question: str
    authorized_scope: tuple[str, ...]
    authority_inputs: tuple[str, ...]
    completion_criteria: tuple[str, ...]
    expected_outputs: tuple[ExpectedOutput, ...]
    no_mutation_boundary: tuple[str, ...]
    stop_before_implementation: bool

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("request schema version must be one")
        if self.task_id != (
            "python.architecture-refactor.public-import-boundaries."
            "disposition-coverage-reconciliation"
        ):
            raise ValueError("request task identity differs")
        for name, values in (
            ("authorized_scope", self.authorized_scope),
            ("authority_inputs", self.authority_inputs),
            ("completion_criteria", self.completion_criteria),
            ("no_mutation_boundary", self.no_mutation_boundary),
        ):
            if not values or any(
                type(value) is not str or not value for value in values
            ):
                raise ValueError(f"request {name} must contain nonempty text")
            if len(values) != len(set(values)):
                raise ValueError(f"request {name} contains a duplicate")
        if not self.decision_question:
            raise ValueError("request decision question must be nonempty")
        if self.expected_outputs != (
            ExpectedOutput(
                "harness/reports/public-import-boundaries/phase3/"
                "disposition-coverage-architecture-decision.md",
                "architecture-decision-conventions/v1",
            ),
            ExpectedOutput(
                "harness/reports/public-import-boundaries/phase3/"
                "disposition-coverage-reconciliation.json",
                "disposition-coverage-reconciliation/v2",
            ),
        ):
            raise ValueError("request expected outputs differ")
        if self.stop_before_implementation is not True:
            raise ValueError("request must stop before implementation")


@dataclass(frozen=True, slots=True)
class SelectionAuthority:
    """Bind exact human responses to the normalized architecture selection."""

    selection_response: str
    recording_response: str
    selected_option: OptionKey
    selected_architecture: ArchitectureKey
    authority_effect: SelectionAuthorityEffect
    closeout_authorized: bool
    successor_activation_authorized: bool

    def __post_init__(self) -> None:
        if (
            self.selection_response,
            self.recording_response,
            self.selected_option,
            self.selected_architecture,
            self.authority_effect,
            self.closeout_authorized,
            self.successor_activation_authorized,
        ) != (
            "recommendation authorized",
            "continue",
            OptionKey.A,
            ArchitectureKey.COHORT_OVERLAY,
            SelectionAuthorityEffect.RECORD_ARCHITECTURE_ONLY,
            False,
            False,
        ):
            raise ValueError("selection authority trace differs")


@dataclass(frozen=True, slots=True)
class InputIdentity:
    """Bind one authoritative input to exact bytes."""

    path: str
    byte_count: int
    sha256: str

    def __post_init__(self) -> None:
        if not self.path or type(self.byte_count) is not int or self.byte_count < 0:
            raise ValueError("input identity path/count is invalid")
        if re.fullmatch(r"[0-9a-f]{64}", self.sha256) is None:
            raise ValueError("input identity SHA-256 is invalid")


@dataclass(frozen=True, slots=True)
class ArchitectureOption:
    """Represent one closed advisory option."""

    option_key: OptionKey
    architecture_key: ArchitectureKey
    summary: str


@dataclass(frozen=True, slots=True)
class CheckpointChoice:
    """Represent one closed checkpoint choice."""

    choice: CheckpointKey
    summary: str


@dataclass(frozen=True, slots=True)
class ClaimBoundaries:
    """Represent exact neutral conclusion boundaries."""

    assignment_meaning: str
    compatibility_conclusion: str
    public_api_conclusion: str
    publication_conclusion: str
    release_conclusion: str
    scientific_validation_conclusion: str
    support_conclusion: str

    def __post_init__(self) -> None:
        conclusions = (
            self.compatibility_conclusion,
            self.public_api_conclusion,
            self.publication_conclusion,
            self.release_conclusion,
            self.scientific_validation_conclusion,
            self.support_conclusion,
        )
        if conclusions != ("none",) * 6:
            raise ValueError("packet conclusions must remain neutral")
        if self.assignment_meaning != (
            "Planning ownership only; no assignment selects a route disposition or "
            "activates an owner."
        ):
            raise ValueError("assignment meaning must remain neutral")


@dataclass(frozen=True, slots=True)
class CoverageCounts:
    """Represent exact required coverage cardinalities."""

    current_surface_count: int
    owner_count: int
    predecessor_route_count: int
    supplemental_candidate_count: int

    def __post_init__(self) -> None:
        if (
            self.current_surface_count,
            self.owner_count,
            self.predecessor_route_count,
            self.supplemental_candidate_count,
        ) != (47, 27, 985, 471):
            raise ValueError("coverage counts differ from 47/27/985/471")


@dataclass(frozen=True, slots=True)
class CoverageOwner:
    """Represent one explicit owner and prerequisite vector."""

    owner_key: OwnerKey
    owner_kind: OwnerKind
    prerequisite_owner_keys: tuple[OwnerKey, ...]


@dataclass(frozen=True, slots=True)
class SurfaceAssignment:
    """Assign one current package surface exactly once."""

    surface_key: str
    owner_key: OwnerKey
    lineage: SurfaceLineage


@dataclass(frozen=True, slots=True)
class PredecessorAssignment:
    """Preserve one predecessor route in its accepted cohort."""

    route_key: str
    owner_key: OwnerKey
    accepted_cohort: OwnerKey


@dataclass(frozen=True, slots=True)
class CandidateAssignment:
    """Assign one separately keyed candidate to later neutral disposition."""

    candidate_key: str
    owner_key: OwnerKey
    resolution: CandidateResolution


@dataclass(frozen=True, slots=True)
class ProposedCoverageMap:
    """Represent the human-selected exact-key architecture map."""

    architecture_key: ArchitectureKey
    map_state: MapState
    owners: tuple[CoverageOwner, ...]
    surface_assignments: tuple[SurfaceAssignment, ...]
    predecessor_route_assignments: tuple[PredecessorAssignment, ...]
    supplemental_candidate_assignments: tuple[CandidateAssignment, ...]

    def __post_init__(self) -> None:
        if (
            self.architecture_key is not ArchitectureKey.COHORT_OVERLAY
            or self.map_state is not MapState.HUMAN_SELECTED
        ):
            raise ValueError("selected map must represent human-selected Option A")
        owner_keys = tuple(owner.owner_key for owner in self.owners)
        expected_owners = tuple(OwnerKey)
        if owner_keys != expected_owners:
            raise ValueError("owner records are not in exact canonical order")
        owner_set = set(owner_keys)
        graph: dict[OwnerKey, tuple[OwnerKey, ...]] = {}
        for owner in self.owners:
            expected_kind = (
                OwnerKind.PREDECESSOR
                if owner.owner_key.value.startswith("D")
                else OwnerKind.OVERLAY
            )
            if owner.owner_kind is not expected_kind:
                raise ValueError(f"owner kind differs: {owner.owner_key}")
            if len(owner.prerequisite_owner_keys) != len(
                set(owner.prerequisite_owner_keys)
            ):
                raise ValueError(f"owner prerequisites duplicate: {owner.owner_key}")
            if not set(owner.prerequisite_owner_keys) <= owner_set:
                raise ValueError(f"owner prerequisite is unknown: {owner.owner_key}")
            graph[owner.owner_key] = owner.prerequisite_owner_keys
        self.assert_acyclic(graph)
        self._assert_keys(
            tuple(item.surface_key for item in self.surface_assignments),
            47,
            "surface assignments",
        )
        self._assert_keys(
            tuple(item.route_key for item in self.predecessor_route_assignments),
            985,
            "predecessor assignments",
        )
        self._assert_keys(
            tuple(
                item.candidate_key for item in self.supplemental_candidate_assignments
            ),
            471,
            "candidate assignments",
        )
        if (
            any(item.owner_key not in owner_set for item in self.surface_assignments)
            or any(
                item.owner_key not in owner_set
                for item in self.predecessor_route_assignments
            )
            or any(
                item.owner_key not in owner_set
                for item in self.supplemental_candidate_assignments
            )
        ):
            raise ValueError("an assignment names an unknown owner")
        if any(
            item.owner_key != item.accepted_cohort
            for item in self.predecessor_route_assignments
        ):
            raise ValueError("predecessor owner differs from accepted cohort")
        if any(
            item.owner_key.value.startswith("D")
            for item in self.supplemental_candidate_assignments
        ):
            raise ValueError("supplemental candidate was folded into a D cohort")

    @staticmethod
    def assert_acyclic(graph: dict[OwnerKey, tuple[OwnerKey, ...]]) -> None:
        """Reject a prerequisite cycle in one closed owner graph."""
        pending = dict(graph)
        complete: set[OwnerKey] = set()
        while pending:
            ready = tuple(
                key
                for key, prerequisites in pending.items()
                if set(prerequisites) <= complete
            )
            if not ready:
                raise ValueError("owner prerequisite graph contains a cycle")
            for key in ready:
                complete.add(key)
                del pending[key]

    @staticmethod
    def _assert_keys(keys: tuple[str, ...], count: int, label: str) -> None:
        if len(keys) != count or len(set(keys)) != count:
            raise ValueError(f"{label} do not provide exact unique coverage")
        if keys != tuple(sorted(keys)):
            raise ValueError(f"{label} are not canonically ordered")


@dataclass(frozen=True, slots=True)
class ReconciliationPacket:
    """Represent the complete closed advisory packet."""

    schema_version: int
    subject_identity: str
    decision_document_path: str
    decision_state: DecisionState
    request: ReconciliationRequest
    request_sha256: str
    input_identities: tuple[InputIdentity, ...]
    counts: CoverageCounts
    options: tuple[ArchitectureOption, ...]
    checkpoint: tuple[CheckpointChoice, ...]
    recommended_option: OptionKey
    selected_option: OptionKey
    selection_authority: SelectionAuthority
    claim_boundaries: ClaimBoundaries
    proposed_map: ProposedCoverageMap

    def __post_init__(self) -> None:
        if (self.schema_version, self.subject_identity) != (
            2,
            "python-public-import-disposition-coverage-reconciliation",
        ):
            raise ValueError("packet identity is unsupported")
        if self.decision_document_path != self.request.expected_outputs[0].path:
            raise ValueError("decision document path differs from request")
        if re.fullmatch(r"[0-9a-f]{64}", self.request_sha256) is None:
            raise ValueError("request SHA-256 is invalid")
        expected_options = (
            ArchitectureOption(
                OptionKey.A,
                ArchitectureKey.COHORT_OVERLAY,
                "Retain D1-D21 for predecessor lineage and add six separately keyed domain overlays for all supplemental surfaces and candidates.",
            ),
            ArchitectureOption(
                OptionKey.B,
                ArchitectureKey.CENTRAL,
                "Retain D1-D21 for predecessor lineage and place all supplemental coverage in one serial central owner before disposition work.",
            ),
            ArchitectureOption(
                OptionKey.C,
                ArchitectureKey.SURFACE_SHARDS,
                "Retain D1-D21 for predecessor lineage and create one supplemental shard per affected surface, reconciled by a serial coverage join.",
            ),
        )
        if self.options != expected_options:
            raise ValueError("options must be exact ordered A/B/C architectures")
        expected_checkpoint = (
            CheckpointChoice(
                CheckpointKey.A, "Cohort-adjacent supplemental overlay DAG"
            ),
            CheckpointChoice(
                CheckpointKey.B, "Single central supplemental coverage authority"
            ),
            CheckpointChoice(
                CheckpointKey.C,
                "Surface-sharded supplemental packets with integration join",
            ),
            CheckpointChoice(CheckpointKey.D, "Reconsider or defer"),
        )
        if self.checkpoint != expected_checkpoint:
            raise ValueError("checkpoint must be exact ordered A/B/C/D")
        if (
            self.decision_state is not DecisionState.HUMAN_SELECTED
            or self.recommended_option is not OptionKey.A
            or self.selected_option is not OptionKey.A
            or self.selection_authority.selected_option is not self.selected_option
            or self.selection_authority.selected_architecture
            is not self.proposed_map.architecture_key
        ):
            raise ValueError(
                "selected, recommended, authority, and map states contradict"
            )
        if self.counts != CoverageCounts(
            current_surface_count=len(self.proposed_map.surface_assignments),
            owner_count=len(self.proposed_map.owners),
            predecessor_route_count=len(
                self.proposed_map.predecessor_route_assignments
            ),
            supplemental_candidate_count=len(
                self.proposed_map.supplemental_candidate_assignments
            ),
        ):
            raise ValueError("summary counts are not derived from the map")


class ReconciliationRequestSerializer:
    """Own exact request representation, encoding, and identity."""

    __slots__ = ()

    def encode(self, request: ReconciliationRequest) -> bytes:
        """Encode one request into canonical non-self-referential bytes."""
        value: JsonRecord = {
            "authority_inputs": list(request.authority_inputs),
            "authorized_scope": list(request.authorized_scope),
            "completion_criteria": list(request.completion_criteria),
            "decision_question": request.decision_question,
            "expected_outputs": [
                {"path": item.path, "schema_identity": item.schema_identity}
                for item in request.expected_outputs
            ],
            "no_mutation_boundary": list(request.no_mutation_boundary),
            "schema_version": request.schema_version,
            "stop_before_implementation": request.stop_before_implementation,
            "task_id": request.task_id,
        }
        return FoundationJsonCodec().encode(value)

    def identity(self, request: ReconciliationRequest) -> str:
        """Return the SHA-256 of one closed request projection."""
        return hashlib.sha256(self.encode(request)).hexdigest()


class SelectedTaskRequestAdapter:
    """Convert the live selected Task into its stable immutable request projection."""

    __slots__ = ()

    def decode(self, payload: bytes) -> ReconciliationRequest:
        """Decode exact Task bytes while excluding mutable lifecycle fields."""
        value = FoundationJsonCodec().decode(payload)
        task = self._closed(
            value,
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
        if task["schema_version"] != 3:
            raise ValueError("selected Task schema version differs")
        return ReconciliationRequest(
            schema_version=1,
            task_id=self._text(task["task_id"], "task_id"),
            decision_question=self._text(task["objective"], "objective"),
            authorized_scope=self._texts(task["authorized_scope"], "authorized_scope"),
            authority_inputs=self._texts(
                task["authority_reference_paths"], "authority_reference_paths"
            ),
            completion_criteria=self._texts(
                task["completion_criteria"], "completion_criteria"
            ),
            expected_outputs=(
                ExpectedOutput(
                    "harness/reports/public-import-boundaries/phase3/"
                    "disposition-coverage-architecture-decision.md",
                    "architecture-decision-conventions/v1",
                ),
                ExpectedOutput(
                    "harness/reports/public-import-boundaries/phase3/"
                    "disposition-coverage-reconciliation.json",
                    "disposition-coverage-reconciliation/v2",
                ),
            ),
            no_mutation_boundary=self._texts(task["exclusions"], "exclusions"),
            stop_before_implementation=True,
        )

    def run_drift_probes(self, payload: bytes, expected_sha256: str) -> tuple[str, ...]:
        """Prove stable request-field drift changes the request identity."""
        value = FoundationJsonCodec().decode(payload)
        root = self._closed(
            value,
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
        probes: tuple[tuple[str, str], ...] = (
            ("objective", "decision-question drift"),
            ("authorized_scope", "scope drift"),
            ("authority_reference_paths", "authority-input drift"),
            ("exclusions", "no-mutation drift"),
        )
        rejected: list[str] = []
        codec = FoundationJsonCodec()
        serializer = ReconciliationRequestSerializer()
        for field, label in probes:
            mutation: JsonRecord = dict(root)
            current = mutation[field]
            if type(current) is str:
                mutation[field] = current + " DRIFT"
            elif type(current) is list:
                mutation[field] = [*current, f"synthetic {label}"]
            else:
                raise ValueError(f"request probe field has wrong type: {field}")
            candidate = self.decode(codec.encode(mutation))
            if serializer.identity(candidate) == expected_sha256:
                raise ValueError(f"request drift escaped identity: {label}")
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
        return tuple(cls._text(item, f"{label} item") for item in value)


class ReconciliationPacketSerializer:
    """Own typed packet serialization."""

    __slots__ = ()

    def encode(self, packet: ReconciliationPacket) -> bytes:
        """Encode one closed packet into canonical JSON bytes."""
        value: JsonRecord = {
            "checkpoint": [
                {"choice": item.choice.value, "summary": item.summary}
                for item in packet.checkpoint
            ],
            "claim_boundaries": {
                "assignment_meaning": packet.claim_boundaries.assignment_meaning,
                "compatibility_conclusion": packet.claim_boundaries.compatibility_conclusion,
                "public_api_conclusion": packet.claim_boundaries.public_api_conclusion,
                "publication_conclusion": packet.claim_boundaries.publication_conclusion,
                "release_conclusion": packet.claim_boundaries.release_conclusion,
                "scientific_validation_conclusion": packet.claim_boundaries.scientific_validation_conclusion,
                "support_conclusion": packet.claim_boundaries.support_conclusion,
            },
            "counts": {
                "current_surface_count": packet.counts.current_surface_count,
                "owner_count": packet.counts.owner_count,
                "predecessor_route_count": packet.counts.predecessor_route_count,
                "supplemental_candidate_count": packet.counts.supplemental_candidate_count,
            },
            "decision_document_path": packet.decision_document_path,
            "decision_state": packet.decision_state.value,
            "input_identities": [
                {
                    "byte_count": item.byte_count,
                    "path": item.path,
                    "sha256": item.sha256,
                }
                for item in packet.input_identities
            ],
            "options": [
                {
                    "architecture_key": item.architecture_key.value,
                    "option_key": item.option_key.value,
                    "summary": item.summary,
                }
                for item in packet.options
            ],
            "proposed_map": {
                "architecture_key": packet.proposed_map.architecture_key.value,
                "map_state": packet.proposed_map.map_state.value,
                "owners": [
                    {
                        "owner_key": item.owner_key.value,
                        "owner_kind": item.owner_kind.value,
                        "prerequisite_owner_keys": [
                            prerequisite.value
                            for prerequisite in item.prerequisite_owner_keys
                        ],
                    }
                    for item in packet.proposed_map.owners
                ],
                "predecessor_route_assignments": [
                    {
                        "accepted_cohort": item.accepted_cohort.value,
                        "owner_key": item.owner_key.value,
                        "route_key": item.route_key,
                    }
                    for item in packet.proposed_map.predecessor_route_assignments
                ],
                "supplemental_candidate_assignments": [
                    {
                        "candidate_key": item.candidate_key,
                        "owner_key": item.owner_key.value,
                        "resolution": item.resolution.value,
                    }
                    for item in packet.proposed_map.supplemental_candidate_assignments
                ],
                "surface_assignments": [
                    {
                        "lineage": item.lineage.value,
                        "owner_key": item.owner_key.value,
                        "surface_key": item.surface_key,
                    }
                    for item in packet.proposed_map.surface_assignments
                ],
            },
            "recommended_option": packet.recommended_option.value,
            "selected_option": packet.selected_option.value,
            "selection_authority": {
                "authority_effect": packet.selection_authority.authority_effect.value,
                "closeout_authorized": packet.selection_authority.closeout_authorized,
                "recording_response": packet.selection_authority.recording_response,
                "selected_architecture": packet.selection_authority.selected_architecture.value,
                "selected_option": packet.selection_authority.selected_option.value,
                "selection_response": packet.selection_authority.selection_response,
                "successor_activation_authorized": packet.selection_authority.successor_activation_authorized,
            },
            "request": FoundationJsonCodec().decode(
                ReconciliationRequestSerializer().encode(packet.request)
            ),
            "request_sha256": packet.request_sha256,
            "schema_version": packet.schema_version,
            "subject_identity": packet.subject_identity,
        }
        return FoundationJsonCodec().encode(value)


class ReconciliationPacketParser:
    """Decode recursive JSON only here into the closed reconciliation domain."""

    __slots__ = ()

    def decode(self, payload: bytes) -> ReconciliationPacket:
        """Decode canonical packet bytes and reject malformed nested records."""
        value = FoundationJsonCodec().decode(payload)
        packet = self._packet(value)
        if ReconciliationPacketSerializer().encode(packet) != payload:
            raise ValueError("reconciliation packet is not canonical")
        if ReconciliationRequestSerializer().identity(packet.request) != (
            packet.request_sha256
        ):
            raise ValueError("request identity differs from closed request bytes")
        return packet

    def run_malformed_probes(self, payload: bytes) -> tuple[str, ...]:
        """Reject nested, discriminant, duplicate, ordering, and relation defects."""
        root = self._closed(
            FoundationJsonCodec().decode(payload),
            self._root_keys(),
            "packet",
        )
        probes: list[tuple[str, JsonRecord]] = []
        unknown_nested = self._copy_root(root)
        owners = self._records(unknown_nested["proposed_map"], "owners")
        owners[0]["unknown"] = "field"
        probes.append(("unknown nested owner field", unknown_nested))
        bad_discriminant = self._copy_root(root)
        options = self._records(bad_discriminant, "options")
        options[0]["option_key"] = "Z"
        probes.append(("unknown option discriminant", bad_discriminant))
        duplicate = self._copy_root(root)
        proposed = self._closed(
            duplicate["proposed_map"], self._map_keys(), "proposed_map"
        )
        assignments = self._array(
            proposed["supplemental_candidate_assignments"], "candidate assignments"
        )
        proposed["supplemental_candidate_assignments"] = [
            *assignments,
            assignments[0],
        ]
        probes.append(("duplicate candidate assignment", duplicate))
        ordering = self._copy_root(root)
        order_map = self._closed(
            ordering["proposed_map"], self._map_keys(), "proposed_map"
        )
        surfaces = self._array(order_map["surface_assignments"], "surface assignments")
        order_map["surface_assignments"] = [surfaces[1], surfaces[0], *surfaces[2:]]
        probes.append(("noncanonical assignment ordering", ordering))
        relation = self._copy_root(root)
        relation_map = self._closed(
            relation["proposed_map"], self._map_keys(), "proposed_map"
        )
        relation_candidates = self._records(
            relation_map, "supplemental_candidate_assignments"
        )
        relation_candidates[0]["owner_key"] = "D1"
        probes.append(("cross-record candidate owner", relation))
        request_unknown = self._copy_root(root)
        request = self._closed(
            request_unknown["request"], self._request_keys(), "request"
        )
        request["unknown"] = "field"
        probes.append(("unknown request field", request_unknown))
        rejected: list[str] = []
        codec = FoundationJsonCodec()
        for label, mutation in probes:
            try:
                self.decode(codec.encode(mutation))
            except (TypeError, ValueError):
                rejected.append(label)
            else:
                raise ValueError(f"malformed packet probe was accepted: {label}")
        try:
            self.decode(b'{"schema_version":2,"schema_version":2}\n')
        except ValueError:
            rejected.append("duplicate JSON key")
        else:
            raise ValueError("duplicate JSON key probe was accepted")
        return tuple(rejected)

    def run_decision_state_probes(self, payload: bytes) -> tuple[str, ...]:
        """Reject contradictory selected, recommended, checkpoint, and map states."""
        root = self._closed(
            FoundationJsonCodec().decode(payload), self._root_keys(), "packet"
        )
        probes: list[tuple[str, JsonRecord]] = []
        decision = self._copy_root(root)
        decision["decision_state"] = "proposed_not_selected"
        probes.append(("contradictory decision lifecycle", decision))
        selected = self._copy_root(root)
        selected["selected_option"] = "B"
        probes.append(("selected option contradicts authority", selected))
        recommended = self._copy_root(root)
        recommended["recommended_option"] = "B"
        probes.append(("recommendation contradicts selection", recommended))
        checkpoint = self._copy_root(root)
        choices = self._records(checkpoint, "checkpoint")
        choices[0]["summary"] = choices[1]["summary"]
        probes.append(("checkpoint contradicts selected A", checkpoint))
        authority = self._copy_root(root)
        authority_record = self._closed(
            authority["selection_authority"],
            {
                "authority_effect",
                "closeout_authorized",
                "recording_response",
                "selected_architecture",
                "selected_option",
                "selection_response",
                "successor_activation_authorized",
            },
            "selection_authority",
        )
        authority_record["selected_option"] = "B"
        probes.append(("authority trace contradicts selection", authority))
        map_state = self._copy_root(root)
        proposed = self._closed(
            map_state["proposed_map"], self._map_keys(), "proposed_map"
        )
        proposed["map_state"] = "recommended_proposal_not_selected"
        probes.append(("map lifecycle contradicts selection", map_state))
        codec = FoundationJsonCodec()
        rejected: list[str] = []
        for label, mutation in probes:
            try:
                self.decode(codec.encode(mutation))
            except (TypeError, ValueError):
                rejected.append(label)
            else:
                raise ValueError(f"decision-state probe was accepted: {label}")
        return tuple(rejected)

    def _packet(self, value: JsonValue) -> ReconciliationPacket:
        root = self._closed(value, self._root_keys(), "packet")
        request = self._request(root["request"])
        proposed = self._map(root["proposed_map"])
        packet = ReconciliationPacket(
            schema_version=self._integer(root["schema_version"], "schema_version"),
            subject_identity=self._text(root["subject_identity"], "subject_identity"),
            decision_document_path=self._text(
                root["decision_document_path"], "decision_document_path"
            ),
            decision_state=DecisionState(
                self._text(root["decision_state"], "decision_state")
            ),
            request=request,
            request_sha256=self._sha(root["request_sha256"], "request_sha256"),
            input_identities=tuple(
                self._input(item, index)
                for index, item in enumerate(
                    self._array(root["input_identities"], "input_identities")
                )
            ),
            counts=self._counts(root["counts"]),
            options=tuple(
                self._option(item, index)
                for index, item in enumerate(self._array(root["options"], "options"))
            ),
            checkpoint=tuple(
                self._checkpoint(item, index)
                for index, item in enumerate(
                    self._array(root["checkpoint"], "checkpoint")
                )
            ),
            recommended_option=OptionKey(
                self._text(root["recommended_option"], "recommended_option")
            ),
            selected_option=OptionKey(
                self._text(root["selected_option"], "selected_option")
            ),
            selection_authority=self._selection_authority(root["selection_authority"]),
            claim_boundaries=self._claims(root["claim_boundaries"]),
            proposed_map=proposed,
        )
        return packet

    def _request(self, value: JsonValue) -> ReconciliationRequest:
        record = self._closed(value, self._request_keys(), "request")
        return ReconciliationRequest(
            schema_version=self._integer(record["schema_version"], "request schema"),
            task_id=self._text(record["task_id"], "request task_id"),
            decision_question=self._text(
                record["decision_question"], "decision_question"
            ),
            authorized_scope=self._texts(
                record["authorized_scope"], "authorized_scope"
            ),
            authority_inputs=self._texts(
                record["authority_inputs"], "authority_inputs"
            ),
            completion_criteria=self._texts(
                record["completion_criteria"], "completion_criteria"
            ),
            expected_outputs=tuple(
                self._output(item, index)
                for index, item in enumerate(
                    self._array(record["expected_outputs"], "expected_outputs")
                )
            ),
            no_mutation_boundary=self._texts(
                record["no_mutation_boundary"], "no_mutation_boundary"
            ),
            stop_before_implementation=self._boolean(
                record["stop_before_implementation"], "stop_before_implementation"
            ),
        )

    def _selection_authority(self, value: JsonValue) -> SelectionAuthority:
        record = self._closed(
            value,
            {
                "authority_effect",
                "closeout_authorized",
                "recording_response",
                "selected_architecture",
                "selected_option",
                "selection_response",
                "successor_activation_authorized",
            },
            "selection_authority",
        )
        return SelectionAuthority(
            selection_response=self._text(
                record["selection_response"], "selection_response"
            ),
            recording_response=self._text(
                record["recording_response"], "recording_response"
            ),
            selected_option=OptionKey(
                self._text(record["selected_option"], "authority selected_option")
            ),
            selected_architecture=ArchitectureKey(
                self._text(record["selected_architecture"], "selected_architecture")
            ),
            authority_effect=SelectionAuthorityEffect(
                self._text(record["authority_effect"], "authority_effect")
            ),
            closeout_authorized=self._boolean(
                record["closeout_authorized"], "closeout_authorized"
            ),
            successor_activation_authorized=self._boolean(
                record["successor_activation_authorized"],
                "successor_activation_authorized",
            ),
        )

    def _map(self, value: JsonValue) -> ProposedCoverageMap:
        record = self._closed(value, self._map_keys(), "proposed_map")
        return ProposedCoverageMap(
            architecture_key=ArchitectureKey(
                self._text(record["architecture_key"], "map architecture_key")
            ),
            map_state=MapState(self._text(record["map_state"], "map_state")),
            owners=tuple(
                self._owner(item, index)
                for index, item in enumerate(self._array(record["owners"], "owners"))
            ),
            surface_assignments=tuple(
                self._surface(item, index)
                for index, item in enumerate(
                    self._array(record["surface_assignments"], "surface_assignments")
                )
            ),
            predecessor_route_assignments=tuple(
                self._predecessor(item, index)
                for index, item in enumerate(
                    self._array(
                        record["predecessor_route_assignments"],
                        "predecessor_route_assignments",
                    )
                )
            ),
            supplemental_candidate_assignments=tuple(
                self._candidate(item, index)
                for index, item in enumerate(
                    self._array(
                        record["supplemental_candidate_assignments"],
                        "supplemental_candidate_assignments",
                    )
                )
            ),
        )

    def _input(self, value: JsonValue, index: int) -> InputIdentity:
        record = self._closed(
            value, {"byte_count", "path", "sha256"}, f"input[{index}]"
        )
        return InputIdentity(
            path=self._text(record["path"], "input path"),
            byte_count=self._integer(record["byte_count"], "input byte_count"),
            sha256=self._sha(record["sha256"], "input sha256"),
        )

    def _option(self, value: JsonValue, index: int) -> ArchitectureOption:
        record = self._closed(
            value, {"architecture_key", "option_key", "summary"}, f"option[{index}]"
        )
        return ArchitectureOption(
            option_key=OptionKey(self._text(record["option_key"], "option_key")),
            architecture_key=ArchitectureKey(
                self._text(record["architecture_key"], "architecture_key")
            ),
            summary=self._text(record["summary"], "option summary"),
        )

    def _checkpoint(self, value: JsonValue, index: int) -> CheckpointChoice:
        record = self._closed(value, {"choice", "summary"}, f"checkpoint[{index}]")
        return CheckpointChoice(
            choice=CheckpointKey(self._text(record["choice"], "choice")),
            summary=self._text(record["summary"], "checkpoint summary"),
        )

    def _claims(self, value: JsonValue) -> ClaimBoundaries:
        keys = {
            "assignment_meaning",
            "compatibility_conclusion",
            "public_api_conclusion",
            "publication_conclusion",
            "release_conclusion",
            "scientific_validation_conclusion",
            "support_conclusion",
        }
        record = self._closed(value, keys, "claim_boundaries")
        return ClaimBoundaries(
            assignment_meaning=self._text(
                record["assignment_meaning"], "assignment_meaning"
            ),
            compatibility_conclusion=self._text(
                record["compatibility_conclusion"], "compatibility_conclusion"
            ),
            public_api_conclusion=self._text(
                record["public_api_conclusion"], "public_api_conclusion"
            ),
            publication_conclusion=self._text(
                record["publication_conclusion"], "publication_conclusion"
            ),
            release_conclusion=self._text(
                record["release_conclusion"], "release_conclusion"
            ),
            scientific_validation_conclusion=self._text(
                record["scientific_validation_conclusion"],
                "scientific_validation_conclusion",
            ),
            support_conclusion=self._text(
                record["support_conclusion"], "support_conclusion"
            ),
        )

    def _counts(self, value: JsonValue) -> CoverageCounts:
        keys = {
            "current_surface_count",
            "owner_count",
            "predecessor_route_count",
            "supplemental_candidate_count",
        }
        record = self._closed(value, keys, "counts")
        return CoverageCounts(
            current_surface_count=self._integer(
                record["current_surface_count"], "current_surface_count"
            ),
            owner_count=self._integer(record["owner_count"], "owner_count"),
            predecessor_route_count=self._integer(
                record["predecessor_route_count"], "predecessor_route_count"
            ),
            supplemental_candidate_count=self._integer(
                record["supplemental_candidate_count"], "supplemental_candidate_count"
            ),
        )

    def _owner(self, value: JsonValue, index: int) -> CoverageOwner:
        record = self._closed(
            value,
            {"owner_key", "owner_kind", "prerequisite_owner_keys"},
            f"owner[{index}]",
        )
        return CoverageOwner(
            owner_key=OwnerKey(self._text(record["owner_key"], "owner_key")),
            owner_kind=OwnerKind(self._text(record["owner_kind"], "owner_kind")),
            prerequisite_owner_keys=tuple(
                OwnerKey(value)
                for value in self._texts(
                    record["prerequisite_owner_keys"],
                    "prerequisite_owner_keys",
                )
            ),
        )

    def _surface(self, value: JsonValue, index: int) -> SurfaceAssignment:
        record = self._closed(
            value, {"lineage", "owner_key", "surface_key"}, f"surface[{index}]"
        )
        return SurfaceAssignment(
            surface_key=self._text(record["surface_key"], "surface_key"),
            owner_key=OwnerKey(self._text(record["owner_key"], "surface owner_key")),
            lineage=SurfaceLineage(self._text(record["lineage"], "surface lineage")),
        )

    def _predecessor(self, value: JsonValue, index: int) -> PredecessorAssignment:
        record = self._closed(
            value,
            {"accepted_cohort", "owner_key", "route_key"},
            f"predecessor[{index}]",
        )
        return PredecessorAssignment(
            route_key=self._text(record["route_key"], "route_key"),
            owner_key=OwnerKey(self._text(record["owner_key"], "route owner_key")),
            accepted_cohort=OwnerKey(
                self._text(record["accepted_cohort"], "accepted_cohort")
            ),
        )

    def _candidate(self, value: JsonValue, index: int) -> CandidateAssignment:
        record = self._closed(
            value, {"candidate_key", "owner_key", "resolution"}, f"candidate[{index}]"
        )
        return CandidateAssignment(
            candidate_key=self._text(record["candidate_key"], "candidate_key"),
            owner_key=OwnerKey(self._text(record["owner_key"], "candidate owner_key")),
            resolution=CandidateResolution(
                self._text(record["resolution"], "candidate resolution")
            ),
        )

    def _output(self, value: JsonValue, index: int) -> ExpectedOutput:
        record = self._closed(value, {"path", "schema_identity"}, f"output[{index}]")
        return ExpectedOutput(
            path=self._text(record["path"], "output path"),
            schema_identity=self._text(record["schema_identity"], "schema identity"),
        )

    @staticmethod
    def _root_keys() -> set[str]:
        return {
            "checkpoint",
            "claim_boundaries",
            "counts",
            "decision_document_path",
            "decision_state",
            "input_identities",
            "options",
            "proposed_map",
            "recommended_option",
            "selected_option",
            "selection_authority",
            "request",
            "request_sha256",
            "schema_version",
            "subject_identity",
        }

    @staticmethod
    def _map_keys() -> set[str]:
        return {
            "architecture_key",
            "map_state",
            "owners",
            "predecessor_route_assignments",
            "supplemental_candidate_assignments",
            "surface_assignments",
        }

    @staticmethod
    def _request_keys() -> set[str]:
        return {
            "authority_inputs",
            "authorized_scope",
            "completion_criteria",
            "decision_question",
            "expected_outputs",
            "no_mutation_boundary",
            "schema_version",
            "stop_before_implementation",
            "task_id",
        }

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
    def _texts(cls, value: JsonValue, label: str) -> tuple[str, ...]:
        return tuple(cls._text(item, label) for item in cls._array(value, label))

    @staticmethod
    def _text(value: JsonValue, label: str) -> str:
        if type(value) is not str or not value:
            raise ValueError(f"{label} must be nonempty text")
        return value

    @staticmethod
    def _integer(value: JsonValue, label: str) -> int:
        if type(value) is not int:
            raise ValueError(f"{label} must be an integer")
        return value

    @staticmethod
    def _boolean(value: JsonValue, label: str) -> bool:
        if type(value) is not bool:
            raise ValueError(f"{label} must be a boolean")
        return value

    @classmethod
    def _sha(cls, value: JsonValue, label: str) -> str:
        text = cls._text(value, label)
        if re.fullmatch(r"[0-9a-f]{64}", text) is None:
            raise ValueError(f"{label} must be a SHA-256")
        return text

    @classmethod
    def _copy_root(cls, root: JsonRecord) -> JsonRecord:
        copied: JsonRecord = dict(root)
        proposed = cls._closed(root["proposed_map"], cls._map_keys(), "proposed_map")
        copied["proposed_map"] = {
            key: list(value) if type(value) is list else value
            for key, value in proposed.items()
        }
        copied["options"] = [
            dict(
                cls._closed(
                    item, {"architecture_key", "option_key", "summary"}, "option"
                )
            )
            for item in cls._array(root["options"], "options")
        ]
        copied["checkpoint"] = [
            dict(cls._closed(item, {"choice", "summary"}, "checkpoint"))
            for item in cls._array(root["checkpoint"], "checkpoint")
        ]
        copied["request"] = dict(
            cls._closed(root["request"], cls._request_keys(), "request")
        )
        copied["selection_authority"] = dict(
            cls._closed(
                root["selection_authority"],
                {
                    "authority_effect",
                    "closeout_authorized",
                    "recording_response",
                    "selected_architecture",
                    "selected_option",
                    "selection_response",
                    "successor_activation_authorized",
                },
                "selection_authority",
            )
        )
        return copied

    @classmethod
    def _records(cls, value: JsonValue, key: str) -> list[JsonRecord]:
        parent = (
            value
            if type(value) is dict
            else cls._closed(value, cls._map_keys(), "proposed_map")
        )
        rows = cls._array(parent[key], key)
        records = [
            dict(cls._closed(row, set(row) if type(row) is dict else set(), key))
            for row in rows
        ]
        represented: list[JsonValue] = []
        represented.extend(records)
        parent[key] = represented
        return records


@dataclass(frozen=True, slots=True)
class AcceptedCoverageFacts:
    """Expose only exact typed projections required from accepted reports."""

    accepted_surfaces: tuple[str, ...]
    current_surfaces: tuple[str, ...]
    predecessor_routes: tuple[tuple[str, str], ...]
    supplemental_candidates: tuple[tuple[str, str, str], ...]


class AcceptedCoverageFactAdapter:
    """Adapt accepted closed F0 and supplement records to narrow coverage facts."""

    __slots__ = ()

    def execute(
        self, foundation_payload: bytes, supplement_payload: bytes
    ) -> AcceptedCoverageFacts:
        """Parse accepted reports through their existing closed typed parsers."""
        foundation = ClosedFoundationParser().execute(
            FoundationJsonCodec().decode(foundation_payload)
        )
        supplement = CurrentFactSupplementParser().decode(supplement_payload)
        if foundation.predecessor_routes != supplement.predecessor_routes:
            raise ValueError("accepted predecessor records differ across F0/supplement")
        facts = AcceptedCoverageFacts(
            accepted_surfaces=tuple(
                item.package for item in foundation.package_surfaces
            ),
            current_surfaces=tuple(
                item.package for item in supplement.current_package_surfaces
            ),
            predecessor_routes=tuple(
                (item.route, item.package) for item in supplement.predecessor_routes
            ),
            supplemental_candidates=tuple(
                (item.candidate_key, item.route.package, item.route.route)
                for item in supplement.supplemental_candidates
            ),
        )
        if tuple(key for key, _, _ in facts.supplemental_candidates) != tuple(
            sorted(key for key, _, _ in facts.supplemental_candidates)
        ):
            raise ValueError("accepted supplemental candidate projection is unordered")
        predecessor_keys = {key for key, _ in facts.predecessor_routes}
        candidate_routes = {route for _, _, route in facts.supplemental_candidates}
        if predecessor_keys & candidate_routes:
            raise ValueError("supplemental route aliases predecessor lineage")
        return facts


@dataclass(frozen=True, slots=True)
class ReconciliationLifecycleState:
    """Expose only closed selected-task lifecycle facts."""

    active_task_id: str | None
    activation_receipt_ids: tuple[str, ...]
    automatic_successor_activation: bool
    task_status: str
    task_status_detail: str
    parent_status: str
    parent_status_detail: str


class ReconciliationLifecycleAdapter:
    """Convert selection and Task encodings into one closed lifecycle record."""

    __slots__ = ()

    def execute(
        self, selection_payload: bytes, task_payload: bytes, parent_payload: bytes
    ) -> ReconciliationLifecycleState:
        """Decode exact lifecycle inputs and expose their required projection."""
        codec = FoundationJsonCodec()
        selection = self._closed(
            codec.decode(selection_payload),
            {
                "active_task_id",
                "automatic_successor_activation",
                "explicit_activation_receipt_ids",
                "schema_version",
            },
            "task selection",
        )
        task = self._task(codec.decode(task_payload), "selected Task")
        parent = self._task(codec.decode(parent_payload), "parent Task")
        if selection["schema_version"] != 1:
            raise ValueError("task selection schema version differs")
        return ReconciliationLifecycleState(
            active_task_id=self._optional_text(
                selection["active_task_id"], "active_task_id"
            ),
            activation_receipt_ids=self._texts(
                selection["explicit_activation_receipt_ids"],
                "explicit_activation_receipt_ids",
            ),
            automatic_successor_activation=self._boolean(
                selection["automatic_successor_activation"],
                "automatic_successor_activation",
            ),
            task_status=self._text(task["status"], "selected Task status"),
            task_status_detail=self._text(
                task["status_detail"], "selected Task status_detail"
            ),
            parent_status=self._text(parent["status"], "parent Task status"),
            parent_status_detail=self._text(
                parent["status_detail"], "parent Task status_detail"
            ),
        )

    @classmethod
    def _task(cls, value: JsonValue, label: str) -> JsonRecord:
        return cls._closed(
            value,
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
            label,
        )

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
    def _optional_text(cls, value: JsonValue, label: str) -> str | None:
        if value is None:
            return None
        return cls._text(value, label)

    @classmethod
    def _texts(cls, value: JsonValue, label: str) -> tuple[str, ...]:
        if type(value) is not list:
            raise ValueError(f"{label} must be an array")
        return tuple(cls._text(item, label) for item in value)

    @staticmethod
    def _boolean(value: JsonValue, label: str) -> bool:
        if type(value) is not bool:
            raise ValueError(f"{label} must be a boolean")
        return value


@dataclass(frozen=True, slots=True)
class DispositionCoverageReconciliationCompletionValidator:
    """Own deterministic artifact, lifecycle, and repository completion gates."""

    repository_root: Path

    TASK_ID = "python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation"
    DOCUMENT = "harness/reports/public-import-boundaries/phase3/disposition-coverage-architecture-decision.md"
    PACKET = "harness/reports/public-import-boundaries/phase3/disposition-coverage-reconciliation.json"
    TASK = "tasks/software/python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation.json"

    def execute(self) -> int:
        """Run every no-argument completion gate and fail closed."""
        try:
            self._validate_permitted_delta()
            task_payload = (self.repository_root / self.TASK).read_bytes()
            request_adapter = SelectedTaskRequestAdapter()
            live_request = request_adapter.decode(task_payload)
            packet_payload = (self.repository_root / self.PACKET).read_bytes()
            parser = ReconciliationPacketParser()
            packet = parser.decode(packet_payload)
            if packet.request != live_request:
                raise ValueError(
                    "packet request projection differs from live selected Task"
                )
            if (
                ReconciliationRequestSerializer().identity(live_request)
                != packet.request_sha256
            ):
                raise ValueError("live selected Task request identity differs")
            facts = AcceptedCoverageFactAdapter().execute(
                (
                    self.repository_root
                    / "harness/reports/public-import-boundaries/phase3/foundation.json"
                ).read_bytes(),
                (
                    self.repository_root
                    / "harness/reports/public-import-boundaries/phase3/current-fact-supplement.json"
                ).read_bytes(),
            )
            self._validate_inputs(packet)
            self._validate_coverage(packet, facts)
            self._validate_markdown(packet)
            self._validate_control_state()
            malformed = parser.run_malformed_probes(packet_payload)
            decision_state = parser.run_decision_state_probes(packet_payload)
            drift = request_adapter.run_drift_probes(
                task_payload, packet.request_sha256
            )
            if len(malformed) != 7 or len(decision_state) != 6 or len(drift) != 4:
                raise ValueError("focused probe cardinalities differ")
            print("malformed packet probes rejected: " + "; ".join(malformed))
            print("decision-state probes rejected: " + "; ".join(decision_state))
            print("request drift probes rejected: " + "; ".join(drift))
        except (OSError, TypeError, ValueError, UnicodeError) as exc:
            return self._fail(f"closed reconciliation validation failed: {exc}")
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
                self.TASK_ID,
                "--task-record",
                self.repository_root / self.TASK,
                "--ownership-manifest",
                self.repository_root
                / ".pi/task-ownership/python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation.json",
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "check",
                ".pi/task-ownership/validate_python_public_import_disposition_coverage_reconciliation.py",
            ),
            (
                interpreter,
                "-m",
                "ruff",
                "format",
                "--check",
                ".pi/task-ownership/validate_python_public_import_disposition_coverage_reconciliation.py",
            ),
            (
                interpreter,
                "-m",
                "mypy",
                "--strict",
                ".pi/task-ownership/validate_python_public_import_disposition_coverage_reconciliation.py",
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
        print("disposition-coverage reconciliation completion validation passed")
        return 0

    def _validate_inputs(self, packet: ReconciliationPacket) -> None:
        expected = (
            (
                "AGENTS.md",
                35349,
                "72146e726e4251437a14e9ac0cf8c16db2750e8daa471f1a0fe03499697d3a9a",
            ),
            (
                ".pi/skills/develop-architecture-decision/SKILL.md",
                3228,
                "bfc8e7a41f98a162fb80581b59b7c0e7cd66dcf5ade426cadb74d07055ad0928",
            ),
            (
                ".pi/skills/develop-architecture-decision/references/architecture-decision-conventions.md",
                4880,
                "132b81f4f5c32b2d8de49bf1c0c3e08c184e578ded32b9330b3ee7b82255a66d",
            ),
            (
                "harness/reports/python-public-import-boundaries-plan.md",
                30016,
                "65d8ed73355ec07f134643e9d1590c65464a7a0e5ec6955744812a1e809561a0",
            ),
            (
                "harness/reports/public-import-boundaries/phase3/foundation.json",
                3908387,
                "3da51677747741fc0088d2f31f1359e6e8280bd1555ef514409ccfb5879f9e61",
            ),
            (
                "harness/reports/public-import-boundaries/phase3/current-fact-supplement.json",
                5742970,
                "56fb7e16f87b5a7d70af5048a336e18da45f1101cd15f6db1949eac809a037a9",
            ),
            (
                "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.json",
                18790,
                "3eefffeb3b35196265f83ba2206cf76af10dd13dbdcd907b3da39bf0ca8f3ecf",
            ),
            (
                "tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json",
                13389,
                "56a1490249c079ff79f777383b47b79e6dafe966195c7d7a0a6962f66296f164",
            ),
            (
                "tasks/software/python.architecture-refactor.public-import-boundaries.json",
                13585,
                "771e66e72a905aa9260690213ddceeffcf037a28e33f8b8c9861a22fff2b9766",
            ),
        )
        observed = tuple(
            (item.path, item.byte_count, item.sha256)
            for item in packet.input_identities
        )
        if observed != expected:
            raise ValueError("authoritative input ledger differs")
        for item in packet.input_identities:
            payload = (self.repository_root / item.path).read_bytes()
            if (
                len(payload) != item.byte_count
                or hashlib.sha256(payload).hexdigest() != item.sha256
            ):
                raise ValueError(f"authoritative input identity mismatch: {item.path}")

    def _validate_coverage(
        self, packet: ReconciliationPacket, facts: AcceptedCoverageFacts
    ) -> None:
        proposed = packet.proposed_map
        self._validate_prerequisites(proposed)
        accepted = set(facts.accepted_surfaces)
        surfaces = {item.surface_key: item for item in proposed.surface_assignments}
        if set(surfaces) != set(facts.current_surfaces):
            raise ValueError("current surface coverage differs")
        for key, assignment in surfaces.items():
            if key in accepted:
                if (
                    assignment.lineage is not SurfaceLineage.ACCEPTED
                    or assignment.owner_key != self._accepted_surface_owner(key)
                ):
                    raise ValueError(f"accepted surface assignment differs: {key}")
            elif (
                assignment.lineage is not SurfaceLineage.SUPPLEMENTAL
                or assignment.owner_key != self._supplement_owner(key)
            ):
                raise ValueError(f"supplemental surface assignment differs: {key}")
        predecessors = {
            item.route_key: item for item in proposed.predecessor_route_assignments
        }
        if set(predecessors) != {route for route, _ in facts.predecessor_routes}:
            raise ValueError("predecessor coverage differs")
        for route, package in facts.predecessor_routes:
            if predecessors[route].accepted_cohort != self._accepted_cohort(package):
                raise ValueError(f"accepted predecessor cohort changed: {route}")
        candidates = {
            item.candidate_key: item
            for item in proposed.supplemental_candidate_assignments
        }
        if set(candidates) != {key for key, _, _ in facts.supplemental_candidates}:
            raise ValueError("supplemental candidate coverage differs")
        for key, package, _ in facts.supplemental_candidates:
            if candidates[key].owner_key != self._supplement_owner(package):
                raise ValueError(f"supplemental owner differs: {key}")

    @staticmethod
    def _validate_prerequisites(proposed: ProposedCoverageMap) -> None:
        expected: dict[str, tuple[str, ...]] = {
            "D1": (),
            "D2": ("D1",),
            "D3": (),
            "D4": (),
            "D5": (),
            "D6": (),
            "D7": (),
            "D8": ("D6", "D7"),
            "D9": ("D6", "D7"),
            "D10": ("D8", "D9"),
            "D11": ("D1", "D2", "D3", "D4", "D10"),
            "D12": ("D1", "D2", "D4"),
            "D13": ("D1", "D2", "D4", "D10", "D12"),
            "D14": ("D10", "D11", "D13"),
            "D15": (),
            "D16": (),
            "D17": ("D15", "D16"),
            "D18": ("D15", "D16", "D17"),
            "D19": ("D18",),
            "D20": ("D16",),
            "D21": (),
            "S01_ANALYSIS_MODEL_SYSTEMS": ("D1", "D3", "D4", "D11"),
            "S02_RESEARCH_MONOGRAPH_CAMPAIGNS": (
                "D10",
                "D11",
                "D12",
                "D13",
                "D14",
                "S01_ANALYSIS_MODEL_SYSTEMS",
            ),
            "S03_WANNIER90": ("D1", "D2", "D4", "D10"),
            "S04_OPERATOR_SUPPLEMENT": ("D3",),
            "S05_SERIALIZATION": ("D6",),
            "S06_SOLID_STATE": ("D1", "D2", "D3", "D4"),
        }
        observed = {
            owner.owner_key.value: tuple(
                prerequisite.value for prerequisite in owner.prerequisite_owner_keys
            )
            for owner in proposed.owners
        }
        if observed != expected:
            raise ValueError("owner prerequisite vectors differ from proposed map")

    def _validate_markdown(self, packet: ReconciliationPacket) -> None:
        text = (self.repository_root / self.DOCUMENT).read_text(encoding="utf-8")
        headings = tuple(line for line in text.splitlines() if line.startswith("## "))
        expected = (
            "## Problem",
            "## Observed current behavior",
            "## Decision requirements",
            "## Option A",
            "## Option B",
            "## Option C",
            "## Three-option comparison",
            "## Recommendation",
            "## Deferred questions",
            "## Human decision required",
        )
        if headings != expected:
            raise ValueError("decision document level-two headings differ")
        facets = (
            "Conceptual model",
            "Authority",
            "Ownership/dependency",
            "Runtime/dispatch",
            "Migration",
            "Reversibility",
            "Failures",
            "Complexity",
            "Maintenance",
            "Context-window consequences",
            "Future compatibility",
            "Advantage",
            "Risk",
        )
        for option, successor in (("A", "B"), ("B", "C"), ("C", None)):
            start = text.index(f"## Option {option}")
            end = (
                text.index(f"## Option {successor}")
                if successor is not None
                else text.index("## Three-option comparison")
            )
            section = text[start:end]
            for facet in facets:
                if section.count(f"**{facet}**") != 1:
                    raise ValueError(f"Option {option} facet differs: {facet}")
        if (
            text[
                text.index("## Recommendation") : text.index("## Deferred questions")
            ].count("Recommend **Option")
            != 1
        ):
            raise ValueError("decision document recommendation count differs")
        if (
            packet.request_sha256 not in text
            or "non-self-referential request projection" not in text
        ):
            raise ValueError("Markdown does not bind the exact request identity")
        for label in (
            "Observed fact",
            "Inference",
            "Human choice",
            "Implementation consequence",
            "Deferred question",
        ):
            if f"**{label}:**" not in text:
                raise ValueError(f"claim label missing: {label}")
        checkpoint = text[text.index("## Human decision required") :]
        if (
            "responded exactly `recommendation authorized`" not in checkpoint
            or "responded exactly `continue`" not in checkpoint
            or "A/B/C/D boundary is resolved as A" not in checkpoint
            or "final task acceptance and closeout remain separate" not in checkpoint
        ):
            raise ValueError("Markdown lacks exact selected-decision authority trace")
        for choice in (
            "A — Cohort-adjacent supplemental overlay DAG",
            "B — Single central supplemental coverage authority",
            "C — Surface-sharded supplemental packets with integration join",
            "D — Reconsider or defer",
        ):
            if checkpoint.count(choice) != 1:
                raise ValueError("A/B/C/D checkpoint differs")

    def _validate_control_state(self) -> None:
        state = ReconciliationLifecycleAdapter().execute(
            (self.repository_root / "harness/task-selection.json").read_bytes(),
            (self.repository_root / self.TASK).read_bytes(),
            (
                self.repository_root
                / "tasks/software/python.architecture-refactor.public-import-boundaries.json"
            ).read_bytes(),
        )
        if state.automatic_successor_activation is not False:
            raise ValueError("automatic successor activation must remain false")
        if state.active_task_id == self.TASK_ID:
            if state.activation_receipt_ids != (f"human-selection.{self.TASK_ID}",):
                raise ValueError("selected lifecycle receipt differs")
            if state.task_status != "planning":
                raise ValueError("selected Task must remain planning")
        elif state.active_task_id is None:
            if state.activation_receipt_ids:
                raise ValueError("closed lifecycle receipts must be empty")
            if state.task_status != "closed_human_accepted_pass":
                raise ValueError("unselected Task must be human-accepted and closed")
            if "responded exactly `accepted`" not in state.task_status_detail:
                raise ValueError("closed Task lacks exact acceptance authority")
        else:
            raise ValueError("selection names an unsupported Task")
        if (
            "The operator responded exactly `recommendation authorized`"
            not in state.task_status_detail
            or "AR-01" not in state.task_status_detail
            or "AR-02" not in state.task_status_detail
        ):
            raise ValueError("Task detail lacks exact correction authority/result")
        authority_trace = (
            "The operator first selected the recommendation with exact response "
            "`recommendation authorized` and then responded exactly `continue`"
        )
        if authority_trace not in state.task_status_detail:
            raise ValueError("selected Task lacks Option A authority trace")
        if state.parent_status != "deferred_between_children":
            raise ValueError("parent must remain deferred")
        if authority_trace not in state.parent_status_detail:
            raise ValueError("parent Task lacks Option A authority trace")

    def _validate_permitted_delta(self) -> None:
        permitted = {
            ".pi/task-ownership/python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation.json",
            ".pi/task-ownership/validate_python_public_import_disposition_coverage_reconciliation.py",
            self.DOCUMENT,
            self.PACKET,
            "harness/state/harness-control.sql",
            "harness/state/harness-control.sqlite3",
            "harness/state/projection-manifest.json",
            "harness/task-graph.json",
            "harness/task-selection.json",
            self.TASK,
            "tasks/software/python.architecture-refactor.public-import-boundaries.json",
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
        lines = completed.stdout.decode("utf-8").splitlines()
        observed: set[str] = set()
        for line in lines:
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

    @staticmethod
    def _accepted_cohort(package: str) -> OwnerKey:
        cohorts = {
            "D1": {
                "ksdft2effmass.electronic_structure",
                "ksdft2effmass.periodic",
                "ksdft2effmass.structures",
            },
            "D2": {"ksdft2effmass.ksdft", "ksdft2effmass.ksdft.pw"},
            "D3": {"ksdft2effmass.operators"},
            "D4": {"ksdft2effmass.units"},
            "D5": {"ksdft2effmass.provenance"},
            "D6": {"ksdft2effmass.persistence"},
            "D7": {"ksdft2effmass.petrinet.colored"},
            "D8": {"ksdft2effmass.workflows.control"},
            "D9": {"ksdft2effmass.workflows.runs"},
            "D10": {"ksdft2effmass.workflows"},
            "D11": {"ksdft2effmass.analysis"},
            "D12": {"ksdft2effmass.calculators.dft.pw"},
            "D13": {
                "ksdft2effmass.integration.quantum_espresso",
                "ksdft2effmass.integration.quantum_espresso.qexsd",
            },
            "D14": {"ksdft2effmass.application"},
            "D15": {"ksdft2effmass.harness.pi.resources"},
            "D16": {
                "ksdft2effmass.harness.pi.conformance",
                "ksdft2effmass.harness.pi.conformance.python",
            },
            "D17": {"ksdft2effmass.harness.pi"},
            "D18": {"ksdft2effmass.harness.pi.local"},
            "D19": {"ksdft2effmass.harness.cli"},
            "D20": {"ksdft2effmass.harness"},
        }
        for cohort, packages in cohorts.items():
            if package in packages:
                return OwnerKey(cohort)
        raise ValueError(f"predecessor package lacks cohort: {package}")

    @classmethod
    def _accepted_surface_owner(cls, package: str) -> OwnerKey:
        zero = {
            "ksdft2effmass",
            "ksdft2effmass.calculators",
            "ksdft2effmass.calculators.dft",
            "ksdft2effmass.campaigns",
            "ksdft2effmass.harness.pi.dbcontrol",
            "ksdft2effmass.harness.pi.local.control",
            "ksdft2effmass.harness.pi.local.dbcontrol",
            "ksdft2effmass.harness.pi.wire",
            "ksdft2effmass.integration",
            "ksdft2effmass.petrinet",
        }
        return OwnerKey.D21 if package in zero else cls._accepted_cohort(package)

    @staticmethod
    def _supplement_owner(package: str) -> OwnerKey:
        if package == "ksdft2effmass.analysis" or package.startswith(
            "ksdft2effmass.analysis.model_systems"
        ):
            return OwnerKey.S01
        if package == "ksdft2effmass.campaigns" or package.startswith(
            "ksdft2effmass.campaigns.research_monograph"
        ):
            return OwnerKey.S02
        owners = {
            "ksdft2effmass.integration.wannier90": OwnerKey.S03,
            "ksdft2effmass.operators": OwnerKey.S04,
            "ksdft2effmass.serialization": OwnerKey.S05,
            "ksdft2effmass.solid_state": OwnerKey.S06,
        }
        if package not in owners:
            raise ValueError(f"supplemental package lacks owner: {package}")
        return owners[package]

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
    """Adapt the no-argument process entry point."""
    if len(sys.argv) != 1:
        print("completion validator takes no arguments", file=sys.stderr)
        return 1
    return DispositionCoverageReconciliationCompletionValidator(
        Path(__file__).resolve().parents[2]
    ).execute()


if __name__ == "__main__":
    raise SystemExit(main())
