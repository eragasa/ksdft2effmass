"""Exact-byte correlation for retained periodic-1D campaign artifacts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from .isolated import (
    Periodic1DIsolatedBandCampaignDefinition,
    Periodic1DIsolatedBandCampaignJsonSerializer,
)
from .isolated_results import (
    Periodic1DIsolatedBandCampaignResult,
    Periodic1DIsolatedBandResultJsonSerializer,
)
from .stress import (
    Periodic1DStressCampaignDefinition,
    Periodic1DStressCampaignJsonSerializer,
)
from .stress_results import (
    Periodic1DStressCampaignResult,
    Periodic1DStressResultJsonSerializer,
)


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignWorkflowRequest:
    """Provide exact retained isolated-band input and result bytes for correlation."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty immutable wire payloads."""
        if type(self.input_payload) is not bytes or not self.input_payload:
            raise ValueError("input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCampaignWorkflowResult:
    """Retain correlated isolated controls, typed outcomes, and source identities."""

    definition: Periodic1DIsolatedBandCampaignDefinition
    campaign_result: Periodic1DIsolatedBandCampaignResult
    input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact result types, identifiers, and SHA-256 correlations."""
        if type(self.definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError(
                "definition must be Periodic1DIsolatedBandCampaignDefinition"
            )
        if type(self.campaign_result) is not Periodic1DIsolatedBandCampaignResult:
            raise TypeError(
                "campaign_result must be Periodic1DIsolatedBandCampaignResult"
            )
        for name, value in (
            ("input_sha256", self.input_sha256),
            ("result_sha256", self.result_sha256),
        ):
            if (
                type(value) is not str
                or len(value) != 64
                or any(character not in "0123456789abcdef" for character in value)
            ):
                raise ValueError(f"{name} must be lowercase SHA-256 hexadecimal")
        if (
            self.definition.experiment_id
            != self.campaign_result.source_document.record_id
        ):
            raise ValueError("definition and result experiment identifiers must agree")
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")


class Periodic1DIsolatedBandCampaignWorkflow:
    """Deserialize and correlate retained isolated-band controls and outcomes.

    This Workflow performs no scientific calculation, filesystem discovery, or
    external execution. It establishes read-only retained-wire compatibility only.
    """

    __slots__ = ()

    result_serializer = Periodic1DIsolatedBandResultJsonSerializer()

    def execute(
        self, request: Periodic1DIsolatedBandCampaignWorkflowRequest
    ) -> Periodic1DIsolatedBandCampaignWorkflowResult:
        """Return typed isolated records after complete available correlation."""
        if type(request) is not Periodic1DIsolatedBandCampaignWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DIsolatedBandCampaignWorkflowRequest"
            )
        definition = Periodic1DIsolatedBandCampaignJsonSerializer().deserialize(
            request.input_payload
        )
        campaign_result = self.result_serializer.deserialize(request.result_payload)
        input_sha256 = hashlib.sha256(request.input_payload).hexdigest()
        self.validate_correlation(definition, campaign_result, input_sha256)
        return Periodic1DIsolatedBandCampaignWorkflowResult(
            definition,
            campaign_result,
            input_sha256,
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def validate_correlation(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        campaign_result: Periodic1DIsolatedBandCampaignResult,
        input_sha256: str,
    ) -> None:
        """Validate every isolated input/result correlation represented in the wire."""
        if definition.experiment_id != campaign_result.source_document.record_id:
            raise ValueError("isolated definition and result identifiers do not agree")
        parent = campaign_result.parent_verification
        if tuple(item.cutoff for item in parent.plane_wave_cutoff_study) != (
            definition.plane_wave_cutoffs
        ):
            raise ValueError("plane-wave cutoff result inventory does not agree")
        finite_difference_points = tuple(
            item.interior_cell_points for item in parent.finite_difference_grid_study
        )
        if finite_difference_points != definition.finite_difference_points:
            raise ValueError("finite-difference result inventory does not agree")
        low_mode_points = tuple(
            item.interior_cell_points for item in parent.common_low_mode_operator_study
        )
        if low_mode_points != definition.finite_difference_points or any(
            item.low_mode_cutoff != definition.common_low_mode_cutoff
            for item in parent.common_low_mode_operator_study
        ):
            raise ValueError("common-low-mode result inventory does not agree")
        weak_strengths = tuple(
            item.potential_strength for item in parent.weak_potential_gap_study
        )
        if weak_strengths != tuple(
            float(value) for value in definition.weak_potential_strengths.magnitude
        ):
            raise ValueError("weak-potential result inventory does not agree")
        reduction = campaign_result.reduction
        expected_coordinates = definition.reciprocal_vector.magnitude * (
            -0.5
            + np.arange(definition.reciprocal_mesh_size, dtype=np.float64)
            / float(definition.reciprocal_mesh_size)
        )
        if not np.array_equal(
            reduction.reciprocal_samples.coordinates.magnitude,
            expected_coordinates,
        ):
            raise ValueError("reciprocal result mesh does not agree")
        expected_representatives = tuple(
            range(
                -definition.reciprocal_mesh_size // 2,
                definition.reciprocal_mesh_size // 2,
            )
        )
        if reduction.hopping_model.representatives != expected_representatives:
            raise ValueError("complete hopping representative inventory does not agree")
        if (
            tuple(item.hopping_range_cells for item in reduction.hopping_range_study)
            != definition.hopping_ranges
        ):
            raise ValueError("hopping-range result inventory does not agree")
        root = campaign_result.source_document.root
        convention = self.result_serializer.retained.object_field(
            root, "dimensionless_convention"
        )
        for field, expected in (
            ("lattice_period", definition.lattice_period.magnitude),
            ("reciprocal_vector", definition.reciprocal_vector.magnitude),
            ("reciprocal_energy", definition.reciprocal_energy.magnitude),
        ):
            observed = self.result_serializer.retained.real_field(convention, field)
            if not np.isclose(observed, expected, rtol=0.0, atol=0.0):
                raise ValueError(f"{field} convention does not agree")
        provenance = self.result_serializer.retained.object_field(root, "provenance")
        if (
            self.result_serializer.retained.string_field(provenance, "input_sha256")
            != input_sha256
        ):
            raise ValueError("result provenance does not authenticate the input bytes")


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignWorkflowRequest:
    """Provide exact retained stress input and result bytes for correlation."""

    input_payload: bytes
    result_payload: bytes

    def __post_init__(self) -> None:
        """Require nonempty immutable wire payloads."""
        if type(self.input_payload) is not bytes or not self.input_payload:
            raise ValueError("input_payload must be nonempty built-in bytes")
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")


@dataclass(frozen=True, slots=True)
class Periodic1DStressCampaignWorkflowResult:
    """Retain correlated typed stress controls, outcomes, and source identities."""

    definition: Periodic1DStressCampaignDefinition
    campaign_result: Periodic1DStressCampaignResult
    input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact result types, identifiers, and SHA-256 correlations."""
        if type(self.definition) is not Periodic1DStressCampaignDefinition:
            raise TypeError("definition must be Periodic1DStressCampaignDefinition")
        if type(self.campaign_result) is not Periodic1DStressCampaignResult:
            raise TypeError("campaign_result must be Periodic1DStressCampaignResult")
        for name, value in (
            ("input_sha256", self.input_sha256),
            ("result_sha256", self.result_sha256),
        ):
            if (
                type(value) is not str
                or len(value) != 64
                or any(character not in "0123456789abcdef" for character in value)
            ):
                raise ValueError(f"{name} must be lowercase SHA-256 hexadecimal")
        if (
            self.definition.experiment_id
            != self.campaign_result.source_document.record_id
        ):
            raise ValueError("definition and result experiment identifiers must agree")
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")


class Periodic1DStressCampaignWorkflow:
    """Deserialize and correlate retained stress controls and typed outcomes.

    This Workflow performs no scientific calculation, filesystem discovery, or
    external execution. It establishes read-only retained-wire compatibility only.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DStressCampaignWorkflowRequest
    ) -> Periodic1DStressCampaignWorkflowResult:
        """Return typed stress records after complete cross-object correlation."""
        if type(request) is not Periodic1DStressCampaignWorkflowRequest:
            raise TypeError("request must be Periodic1DStressCampaignWorkflowRequest")
        definition = Periodic1DStressCampaignJsonSerializer().deserialize(
            request.input_payload
        )
        campaign_result = Periodic1DStressResultJsonSerializer().deserialize(
            request.result_payload
        )
        self.validate_correlation(definition, campaign_result)
        return Periodic1DStressCampaignWorkflowResult(
            definition,
            campaign_result,
            hashlib.sha256(request.input_payload).hexdigest(),
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def validate_correlation(
        self,
        definition: Periodic1DStressCampaignDefinition,
        campaign_result: Periodic1DStressCampaignResult,
    ) -> None:
        """Validate all retained stress inventory and route-control correlations."""
        if definition.experiment_id != campaign_result.source_document.record_id:
            raise ValueError("stress definition and result identifiers do not agree")
        amplitude_strengths = tuple(
            item.potential_strength
            for item in campaign_result.potential_amplitude_stress
        )
        if amplitude_strengths != tuple(
            float(value) for value in definition.potential_strengths.magnitude
        ):
            raise ValueError("potential-amplitude result inventory does not agree")
        for amplitude in campaign_result.potential_amplitude_stress:
            if (
                tuple(item.resolution for item in amplitude.plane_wave_cutoff_study)
                != definition.plane_wave_cutoffs
            ):
                raise ValueError("plane-wave stress cutoff inventory does not agree")
            if (
                tuple(
                    item.resolution for item in amplitude.finite_difference_grid_study
                )
                != definition.finite_difference_points
            ):
                raise ValueError("finite-difference stress inventory does not agree")
        expected_mesh_keys = {
            (float(strength), mesh_size, band_index)
            for strength in definition.potential_strengths.magnitude
            for mesh_size in definition.reciprocal_mesh_sizes
            for band_index in definition.stress_band_indices
        }
        observed_mesh_keys = {
            (item.potential_strength, item.mesh_size, item.band_index)
            for item in campaign_result.mesh_band_and_isolation_stress
        }
        if observed_mesh_keys != expected_mesh_keys or len(
            campaign_result.mesh_band_and_isolation_stress
        ) != len(expected_mesh_keys):
            raise ValueError("mesh/band/isolation result inventory does not agree")
        expected_shape_ids = tuple(
            shape.identifier for shape in definition.potential_shapes
        )
        observed_shape_ids = tuple(
            shape.identifier for shape in campaign_result.potential_shape_stress.cases
        )
        if observed_shape_ids != expected_shape_ids:
            raise ValueError("potential-shape result inventory does not agree")
        gauge = campaign_result.gauge_covariance_stress
        route = campaign_result.route_assumption_stress
        if gauge.mesh_size != definition.route_stress_mesh_size or not np.isclose(
            gauge.potential_strength,
            definition.route_stress_potential_strength.magnitude,
            rtol=0.0,
            atol=0.0,
        ):
            raise ValueError("gauge stress controls do not agree with the definition")
        if (
            route.mesh_size != definition.route_stress_mesh_size
            or route.hopping_range_cells != definition.route_stress_hopping_range_cells
            or not np.isclose(
                route.potential_strength,
                definition.route_stress_potential_strength.magnitude,
                rtol=0.0,
                atol=0.0,
            )
        ):
            raise ValueError("route stress controls do not agree with the definition")
