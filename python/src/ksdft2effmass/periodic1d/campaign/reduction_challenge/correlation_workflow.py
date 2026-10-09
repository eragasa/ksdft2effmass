"""Read-only correlation Workflow for retained reduction-challenge outcomes.

The Workflow decodes exact historical schema-one input and result wires, authenticates
the result's declared input digest against the supplied input bytes, checks shared
experiment identity and ordered inventories, and retains both content digests. It
performs no numerical reconstruction, filesystem discovery, scientific validation, or
uncertainty analysis.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ..serialization import Periodic1DCampaignJsonDecoder
from .definition import (
    Periodic1DReductionChallengeCampaignDefinition,
    Periodic1DReductionChallengeCampaignJsonSerializer,
)
from .results import (
    Periodic1DReductionChallengeCampaignResult,
    Periodic1DReductionChallengeResultJsonSerializer,
)


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignWorkflowRequest:
    """Provide exact historical input and result bytes for correlation.

    Parameters
    ----------
    input_payload, result_payload
        Nonempty exact built-in :class:`bytes` values. The Workflow neither discovers
        files nor normalizes caller-supplied representations.

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
        """Require two nonempty immutable wire representations."""
        for name, value in (
            ("input_payload", self.input_payload),
            ("result_payload", self.result_payload),
        ):
            if type(value) is not bytes:
                raise TypeError(f"{name} must be built-in bytes")
            if not value:
                raise ValueError(f"{name} must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeCampaignWorkflowResult:
    """Retain typed controls, outcomes, and exact wire-content identities.

    Parameters
    ----------
    definition
        Typed version-one challenge controls.
    campaign_result
        Complete immutable result wire and typed challenge channels.
    input_sha256, result_sha256
        Lowercase SHA-256 identities calculated from the exact supplied bytes.

    Raises
    ------
    TypeError
        If either typed record or digest has the wrong exact representation.
    ValueError
        If digest syntax, experiment identity, or result source identity disagrees.

    Notes
    -----
    SHA-256 establishes content identity only. This Result does not prove authorship,
    historical execution, repository provenance, decoded correctness, numerical
    reproduction, convergence, scientific validation, UQ, or acceptance.
    """

    definition: Periodic1DReductionChallengeCampaignDefinition
    campaign_result: Periodic1DReductionChallengeCampaignResult
    input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact records and their intrinsic identity correlations."""
        self._check_args_record_types()
        self._check_args_content_identities()
        self._check_args_experiment_identity()

    def _check_args_record_types(self) -> None:
        """Require exact definition and campaign-result representations."""
        if type(self.definition) is not Periodic1DReductionChallengeCampaignDefinition:
            raise TypeError(
                "definition must be Periodic1DReductionChallengeCampaignDefinition"
            )
        if type(self.campaign_result) is not Periodic1DReductionChallengeCampaignResult:
            raise TypeError(
                "campaign_result must be Periodic1DReductionChallengeCampaignResult"
            )

    def _check_args_content_identities(self) -> None:
        """Require valid digests and bind the result digest to source bytes."""
        decoder = Periodic1DCampaignJsonDecoder()
        decoder.sha256(self.input_sha256, "input_sha256")
        decoder.sha256(self.result_sha256, "result_sha256")
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")

    def _check_args_experiment_identity(self) -> None:
        """Require input and result records to identify one experiment."""
        if (
            self.definition.experiment_id
            != self.campaign_result.source_document.record_id
        ):
            raise ValueError("definition and result experiment identifiers must agree")


class Periodic1DReductionChallengeCampaignWorkflow:
    """Deserialize and correlate retained reduction-challenge documents.

    This stateless Workflow owns deterministic operation order only. It does not retain
    request state, execute the historical producer, reinterpret expected trends as
    criteria, or collapse discretization, sampling, gauge, and reduction errors.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DReductionChallengeCampaignWorkflowRequest
    ) -> Periodic1DReductionChallengeCampaignWorkflowResult:
        """Return typed records after complete available wire correlation.

        Parameters
        ----------
        request
            Exact caller-supplied input and result bytes.

        Returns
        -------
        Periodic1DReductionChallengeCampaignWorkflowResult
            Correlated typed records and exact content identities.

        Raises
        ------
        TypeError
            If ``request`` or a decoded field has the wrong exact representation.
        ValueError
            If strict schemas, intrinsic values, ordered inventories, controls,
            experiment identities, or provenance correlations disagree.
        OverflowError
            If a retained diagnostic cannot be represented as finite binary64.
        """
        if type(request) is not Periodic1DReductionChallengeCampaignWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DReductionChallengeCampaignWorkflowRequest"
            )
        campaign_result = (
            Periodic1DReductionChallengeResultJsonSerializer().deserialize(
                request.result_payload
            )
        )
        input_sha256 = hashlib.sha256(request.input_payload).hexdigest()
        self._check_input_content_identity(campaign_result, input_sha256)
        definition = Periodic1DReductionChallengeCampaignJsonSerializer().deserialize(
            request.input_payload
        )
        self._check_correlation(definition, campaign_result)
        return Periodic1DReductionChallengeCampaignWorkflowResult(
            definition,
            campaign_result,
            input_sha256,
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def _check_correlation(
        self,
        definition: Periodic1DReductionChallengeCampaignDefinition,
        campaign_result: Periodic1DReductionChallengeCampaignResult,
    ) -> None:
        """Require identities and every ordered challenge inventory to agree."""
        if definition.experiment_id != campaign_result.source_document.record_id:
            raise ValueError("challenge experiment identifiers do not agree")
        self._check_amplitude_inventories(definition, campaign_result)
        self._check_mesh_band_inventory(definition, campaign_result)
        self._check_shape_inventory(definition, campaign_result)
        self._check_route_controls(definition, campaign_result)

    @staticmethod
    def _check_input_content_identity(
        campaign_result: Periodic1DReductionChallengeCampaignResult,
        input_sha256: str,
    ) -> None:
        """Authenticate supplied input bytes against the result's declared digest."""
        serializer = Periodic1DReductionChallengeResultJsonSerializer
        provenance = serializer.retained.object_field(
            campaign_result.source_document.root, "provenance"
        )
        declared = serializer.retained.string_field(provenance, "input_sha256")
        if declared != input_sha256:
            raise ValueError(
                "retained input SHA-256 does not match supplied input bytes"
            )

    @staticmethod
    def _check_amplitude_inventories(
        definition: Periodic1DReductionChallengeCampaignDefinition,
        campaign_result: Periodic1DReductionChallengeCampaignResult,
    ) -> None:
        """Require amplitude and discretization inventories to preserve order."""
        observed_strengths = tuple(
            item.potential_strength for item in campaign_result.potential_amplitude
        )
        expected_strengths = tuple(
            float(value) for value in definition.potential_strengths.magnitude
        )
        if observed_strengths != expected_strengths:
            raise ValueError("potential-amplitude result inventory does not agree")
        for amplitude in campaign_result.potential_amplitude:
            if (
                tuple(item.resolution for item in amplitude.plane_wave_cutoff_study)
                != definition.plane_wave_cutoffs
            ):
                raise ValueError("plane-wave cutoff inventory does not agree")
            if (
                tuple(
                    item.resolution for item in amplitude.finite_difference_grid_study
                )
                != definition.finite_difference_points
            ):
                raise ValueError("finite-difference point inventory does not agree")

    @staticmethod
    def _check_mesh_band_inventory(
        definition: Periodic1DReductionChallengeCampaignDefinition,
        campaign_result: Periodic1DReductionChallengeCampaignResult,
    ) -> None:
        """Require the complete ordered amplitude/mesh/band Cartesian product."""
        expected = tuple(
            (float(strength), mesh_size, band_index)
            for strength in definition.potential_strengths.magnitude
            for mesh_size in definition.reciprocal_mesh_sizes
            for band_index in definition.challenged_band_indices
        )
        observed = tuple(
            (item.potential_strength, item.mesh_size, item.band_index)
            for item in campaign_result.mesh_band_isolation
        )
        if observed != expected:
            raise ValueError("mesh/band/isolation result inventory does not agree")

    @staticmethod
    def _check_shape_inventory(
        definition: Periodic1DReductionChallengeCampaignDefinition,
        campaign_result: Periodic1DReductionChallengeCampaignResult,
    ) -> None:
        """Require named potential-shape result order to match input order."""
        expected = tuple(shape.identifier for shape in definition.potential_shapes)
        observed = tuple(
            shape.identifier for shape in campaign_result.potential_shapes.cases
        )
        if observed != expected:
            raise ValueError("potential-shape result inventory does not agree")
        expected_gap_count = definition.compared_band_count
        if any(
            len(shape.minimum_adjacent_gaps) != expected_gap_count
            for shape in campaign_result.potential_shapes.cases
        ):
            raise ValueError(
                "potential-shape gap inventories must match compared-band count"
            )

    @staticmethod
    def _check_route_controls(
        definition: Periodic1DReductionChallengeCampaignDefinition,
        campaign_result: Periodic1DReductionChallengeCampaignResult,
    ) -> None:
        """Require gauge and route results to use declared exact controls."""
        gauge = campaign_result.gauge_covariance
        route = campaign_result.route_assumptions
        expected_strength = definition.route_challenge_potential_strength.magnitude
        if (
            gauge.mesh_size != definition.route_challenge_mesh_size
            or gauge.potential_strength != expected_strength
        ):
            raise ValueError("gauge challenge controls do not agree")
        if (
            route.mesh_size != definition.route_challenge_mesh_size
            or route.hopping_range_cells
            != definition.route_challenge_hopping_range_cells
            or route.potential_strength != expected_strength
        ):
            raise ValueError("route challenge controls do not agree")
