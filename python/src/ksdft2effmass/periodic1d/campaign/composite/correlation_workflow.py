"""Read-only correlation Workflow for retained composite campaign outcomes.

The Workflow decodes the exact input and result wires, checks their shared identity and
ordered retained-band inventories, and retains both content digests. It performs no
calculation, filesystem discovery, scientific validation, or uncertainty analysis.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ..serialization import Periodic1DCampaignJsonDecoder
from .definition import (
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)
from .results import (
    Periodic1DCompositeCampaignResult,
    Periodic1DCompositeResultJsonSerializer,
)


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignWorkflowRequest:
    """Provide retained composite bytes for read-only correlation.

    Parameters
    ----------
    input_payload
        Exact nonempty schema-one composite input bytes.
    result_payload
        Exact nonempty retained composite result bytes.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`.
    ValueError
        If either exact byte representation is empty.
    """

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty immutable wire payloads."""
        for name, value in (
            ("input_payload", self.input_payload),
            ("result_payload", self.result_payload),
        ):
            if type(value) is not bytes:
                raise TypeError(f"{name} must be built-in bytes")
            if not value:
                raise ValueError(f"{name} must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeCampaignWorkflowResult:
    """Retain correlated composite controls, outcomes, and wire identities.

    Parameters
    ----------
    definition
        Typed campaign controls and explicit parent-qualified retention definitions.
    campaign_result
        Complete immutable source document and ordered typed campaign outcomes.
    input_sha256, result_sha256
        Lowercase SHA-256 content identities of the exact request wires.

    Raises
    ------
    TypeError
        If either typed record has the wrong exact semantic type.
    ValueError
        If digests, experiment identity, or result-source identity disagree.

    Notes
    -----
    SHA-256 values establish exact content identity only. This Result does not prove
    authorship, historical execution, repository provenance, decoded scientific
    correctness, convergence, validation, uncertainty quantification, or acceptance.
    """

    definition: Periodic1DCompositeCampaignDefinition
    campaign_result: Periodic1DCompositeCampaignResult
    input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact records and their identity correlations."""
        self._check_args_record_types()
        self._check_args_content_identities()
        self._check_args_experiment_correlation()

    def _check_args_record_types(self) -> None:
        """Require exact definition and campaign-result representations."""
        if type(self.definition) is not Periodic1DCompositeCampaignDefinition:
            raise TypeError("definition must be Periodic1DCompositeCampaignDefinition")
        if type(self.campaign_result) is not Periodic1DCompositeCampaignResult:
            raise TypeError("campaign_result must be Periodic1DCompositeCampaignResult")

    def _check_args_content_identities(self) -> None:
        """Require valid wire digests and bind the result digest to its source bytes."""
        decoder = Periodic1DCampaignJsonDecoder()
        decoder.sha256(self.input_sha256, "input_sha256")
        decoder.sha256(self.result_sha256, "result_sha256")
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")

    def _check_args_experiment_correlation(self) -> None:
        """Require input and result records to identify the same experiment."""
        if (
            self.definition.experiment_id
            != self.campaign_result.source_document.record_id
        ):
            raise ValueError(
                "composite input and result experiment identifiers must agree"
            )


class Periodic1DCompositeCampaignWorkflow:
    """Deserialize and correlate every retained composite result channel.

    The Workflow owns deterministic operation order only. It does not retain mutable
    state, discover files, execute the historical calculation, reconstruct unavailable
    arrays, or apply a scientific acceptance policy.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DCompositeCampaignWorkflowRequest
    ) -> Periodic1DCompositeCampaignWorkflowResult:
        """Return typed records after group and content-identity correlation.

        Parameters
        ----------
        request
            Exact input and result bytes supplied by the caller.

        Returns
        -------
        Periodic1DCompositeCampaignWorkflowResult
            Correlated typed records and exact wire-content identities.

        Raises
        ------
        TypeError
            If ``request`` or a decoded field has the wrong exact representation.
        ValueError
            If schema, intrinsic values, group inventories, controls, or source
            identities disagree.
        """
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
        self._check_correlation(definition, campaign_result, input_sha256)
        return Periodic1DCompositeCampaignWorkflowResult(
            definition,
            campaign_result,
            input_sha256,
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def _check_correlation(
        self,
        definition: Periodic1DCompositeCampaignDefinition,
        campaign_result: Periodic1DCompositeCampaignResult,
        input_sha256: str,
    ) -> None:
        """Require group inventories and retained input identity to agree.

        Parameters
        ----------
        definition
            Typed input controls owning the expected group and route inventories.
        campaign_result
            Typed retained result owning observed groups and provenance fields.
        input_sha256
            Content identity calculated directly from the supplied input bytes.

        Raises
        ------
        ValueError
            If any identity, group, mesh, range, isolation, or provenance correlation
            disagrees.
        """
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
