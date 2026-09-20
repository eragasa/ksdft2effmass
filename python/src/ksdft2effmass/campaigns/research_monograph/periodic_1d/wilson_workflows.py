"""Read-only retained-wire workflows for Appendix G composite outcomes.

The composite Workflow correlates all typed retained result channels with the exact
version-one input.  The Wannier90 Workflow retains its narrower Wilson-center
correlation role.  Neither Workflow executes a calculation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .composite import (
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)
from .composite_results import (
    Periodic1DCompositeCampaignResult,
    Periodic1DCompositeResultJsonSerializer,
)
from .result_documents import (
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DRetainedResultKind,
)
from .wannier90_results import (
    Periodic1DWannier90CampaignResult,
    Periodic1DWannier90ResultJsonSerializer,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignWorkflowRequest:
    """Provide retained composite input and result bytes for read-only correlation."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty immutable wire payloads."""
        if type(self.input_payload) is not bytes or not self.input_payload:
            raise ValueError("input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignWorkflowResult:
    """Retain correlated composite controls, typed outcomes, and wire identities."""

    definition: Periodic1DCompositeCampaignDefinition
    campaign_result: Periodic1DCompositeCampaignResult
    input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact records, experiment identity, and source identity."""
        if type(self.definition) is not Periodic1DCompositeCampaignDefinition:
            raise TypeError("definition must be Periodic1DCompositeCampaignDefinition")
        if type(self.campaign_result) is not Periodic1DCompositeCampaignResult:
            raise TypeError("campaign_result must be Periodic1DCompositeCampaignResult")
        self.validate_sha256("input_sha256", self.input_sha256)
        self.validate_sha256("result_sha256", self.result_sha256)
        if (
            self.definition.experiment_id
            != self.campaign_result.source_document.record_id
        ):
            raise ValueError(
                "composite input and result experiment identifiers must agree"
            )
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")

    @staticmethod
    def validate_sha256(name: str, value: str) -> None:
        """Require one lowercase SHA-256 hexadecimal identity."""
        if (
            type(value) is not str
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(f"{name} must be lowercase SHA-256 hexadecimal")


class Periodic1DCompositeCampaignWorkflow:
    """Deserialize and correlate every retained composite result channel."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DCompositeCampaignWorkflowRequest
    ) -> Periodic1DCompositeCampaignWorkflowResult:
        """Return typed records after group and provenance correlation."""
        if type(request) is not Periodic1DCompositeCampaignWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DCompositeCampaignWorkflowRequest"
            )
        definition = Periodic1DCompositeCampaignJsonSerializer().deserialize(
            request.input_payload
        )
        campaign_result = Periodic1DCompositeResultJsonSerializer().deserialize(
            request.result_payload
        )
        input_sha256 = hashlib.sha256(request.input_payload).hexdigest()
        self.validate_correlation(definition, campaign_result, input_sha256)
        return Periodic1DCompositeCampaignWorkflowResult(
            definition,
            campaign_result,
            input_sha256,
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def validate_correlation(
        self,
        definition: Periodic1DCompositeCampaignDefinition,
        campaign_result: Periodic1DCompositeCampaignResult,
        input_sha256: str,
    ) -> None:
        """Require group inventories and retained input identity to agree."""
        if definition.experiment_id != campaign_result.source_document.record_id:
            raise ValueError("composite experiment identifiers do not agree")
        expected_groups = tuple(
            (
                group.identifier,
                tuple(range(group.lower_index, group.upper_index + 1)),
            )
            for group in definition.retained_band_groups
        )
        observed_groups = tuple(
            (group.group_id, group.band_indices) for group in campaign_result.groups
        )
        if observed_groups != expected_groups:
            raise ValueError("composite retained band groups do not agree")
        expected_representatives = tuple(
            range(
                -definition.reciprocal_mesh_size // 2,
                definition.reciprocal_mesh_size // 2,
            )
        )
        for group in campaign_result.groups:
            representation = group.hopping_representation
            if (
                len(representation.smooth_reciprocal_hamiltonians.matrices)
                != definition.reciprocal_mesh_size
            ):
                raise ValueError("composite reciprocal mesh sizes do not agree")
            if representation.smooth_hopping_model.representatives != (
                expected_representatives
            ):
                raise ValueError("composite smooth hopping representatives disagree")
            if representation.rough_hopping_model.representatives != (
                expected_representatives
            ):
                raise ValueError("composite rough hopping representatives disagree")
            observed_ranges = tuple(
                result.hopping_range_cells for result in group.range_study
            )
            if observed_ranges != definition.hopping_ranges_cells:
                raise ValueError("composite hopping range inventories do not agree")
            if (
                group.direct_route.hopping_range_cells
                != definition.direct_route_range_cells
            ):
                raise ValueError("composite direct-route ranges do not agree")
            expected_status = (
                "pass"
                if group.isolation.external_minimum_gap
                > definition.external_gap_threshold.magnitude
                else "failed"
            )
            if group.isolation.external_status.value != expected_status:
                raise ValueError("composite external isolation disposition disagrees")
        provenance = Periodic1DCompositeResultJsonSerializer.retained.object_field(
            campaign_result.source_document.root, "provenance"
        )
        observed_input_sha256 = (
            Periodic1DCompositeResultJsonSerializer.retained.string_field(
                provenance, "input_sha256"
            )
        )
        if observed_input_sha256 != input_sha256:
            raise ValueError("composite retained input SHA-256 does not agree")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90CampaignWorkflowRequest:
    """Provide composite controls and one retained Wannier90 result for correlation."""

    composite_input_payload: bytes
    result_payload: bytes
    result_kind: Periodic1DRetainedResultKind

    def __post_init__(self) -> None:
        """Require nonempty bytes and one supported retained Wannier90 kind."""
        if (
            type(self.composite_input_payload) is not bytes
            or not self.composite_input_payload
        ):
            raise ValueError("composite_input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")
        if type(self.result_kind) is not Periodic1DRetainedResultKind:
            raise TypeError("result_kind must be Periodic1DRetainedResultKind")
        if self.result_kind not in {
            Periodic1DRetainedResultKind.WANNIER90,
            Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("result_kind must identify a supported Wannier90 result")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90CampaignWorkflowResult:
    """Retain correlated composite controls, Wilson-center results, and identities."""

    composite_definition: Periodic1DCompositeCampaignDefinition
    campaign_result: Periodic1DWannier90CampaignResult
    composite_input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact records and wire identities."""
        if type(self.composite_definition) is not Periodic1DCompositeCampaignDefinition:
            raise TypeError("composite_definition uses the wrong record type")
        if type(self.campaign_result) is not Periodic1DWannier90CampaignResult:
            raise TypeError("campaign_result uses the wrong result type")
        Periodic1DCompositeCampaignWorkflowResult.validate_sha256(
            "composite_input_sha256", self.composite_input_sha256
        )
        Periodic1DCompositeCampaignWorkflowResult.validate_sha256(
            "result_sha256", self.result_sha256
        )
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")


class Periodic1DWannier90CampaignWorkflow:
    """Correlate retained Wannier90 Wilson-center outcomes with composite controls."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DWannier90CampaignWorkflowRequest
    ) -> Periodic1DWannier90CampaignWorkflowResult:
        """Return typed records after input identity and group correlation."""
        if type(request) is not Periodic1DWannier90CampaignWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DWannier90CampaignWorkflowRequest"
            )
        definition = Periodic1DCompositeCampaignJsonSerializer().deserialize(
            request.composite_input_payload
        )
        campaign_result = Periodic1DWannier90ResultJsonSerializer(
            request.result_kind
        ).deserialize(request.result_payload)
        input_sha256 = hashlib.sha256(request.composite_input_payload).hexdigest()
        self.validate_correlation(definition, campaign_result, input_sha256)
        return Periodic1DWannier90CampaignWorkflowResult(
            definition,
            campaign_result,
            input_sha256,
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def validate_correlation(
        self,
        definition: Periodic1DCompositeCampaignDefinition,
        campaign_result: Periodic1DWannier90CampaignResult,
        input_sha256: str,
    ) -> None:
        """Require retained band groups and composite input identity to agree."""
        expected_groups = tuple(
            (
                group.identifier,
                tuple(range(group.lower_index, group.upper_index + 1)),
            )
            for group in definition.retained_band_groups
        )
        observed_groups = tuple(
            (group.group_id, group.band_indices) for group in campaign_result.groups
        )
        if observed_groups != expected_groups:
            raise ValueError("Wannier90 retained band groups do not agree")
        retained = Periodic1DRetainedResultJsonSerializer(
            campaign_result.source_document.kind
        )
        provenance = retained.object_field(
            campaign_result.source_document.root, "provenance"
        )
        if retained.string_field(provenance, "composite_input_sha256") != input_sha256:
            raise ValueError("Wannier90 composite input SHA-256 does not agree")
