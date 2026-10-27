"""Canonical development serialization for the smooth four-state realization."""

from __future__ import annotations

import hashlib

from ..definition import (
    CONTINUOUS_ALIGNMENT_METHOD_ID,
    EXPERIMENT_FAMILY_ID,
    FOURIER_CONVENTION_ID,
    FOURIER_NORMALIZATION_ID,
)
from ..serialization import JsonValue, canonical_json_bytes
from .definition import (
    SMOOTH_FOUR_STATE_INPUT_SCHEMA_ID,
    SMOOTH_FOUR_STATE_METHOD_ID,
    SMOOTH_FOUR_STATE_PARENT_ID,
    SMOOTH_FOUR_STATE_RESULT_SCHEMA_ID,
    SMOOTH_FOUR_STATE_VERIFICATION_SCHEMA_ID,
    SmoothFourStateDefinition,
)
from .results import (
    SmoothFourStateHoppingBlockResult,
    SmoothFourStatePointResult,
    SmoothFourStateResult,
)
from .verify import SmoothFourStateVerificationResult


def smooth_four_state_identity_document() -> dict[str, JsonValue]:
    """Return publication-independent non-flat method identities."""
    return {
        "family_id": EXPERIMENT_FAMILY_ID,
        "method_id": SMOOTH_FOUR_STATE_METHOD_ID,
        "parent_model_id": SMOOTH_FOUR_STATE_PARENT_ID,
        "alignment_method_id": CONTINUOUS_ALIGNMENT_METHOD_ID,
        "reciprocal_coordinate_id": "q-equals-k-over-reciprocal-period.v1",
        "fourier_convention_id": FOURIER_CONVENTION_ID,
        "fourier_normalization_id": FOURIER_NORMALIZATION_ID,
        "frame_transport_id": "neighbor-procrustes-with-closure-sewing.v1",
    }


class SmoothFourStateInputSerializer:
    """Encode all controls for one non-flat development calculation."""

    __slots__ = ()

    def serialize(self, definition: SmoothFourStateDefinition) -> bytes:
        """Return canonical input bytes without assigning a retained identity."""
        if type(definition) is not SmoothFourStateDefinition:
            raise TypeError("definition must be SmoothFourStateDefinition")
        return canonical_json_bytes(
            {
                "schema": SMOOTH_FOUR_STATE_INPUT_SCHEMA_ID,
                "identity": smooth_four_state_identity_document(),
                "reciprocal_mesh_size": definition.reciprocal_mesh_size,
                "mesh_rule": "uniform-half-open-centered.v1",
                "amplitudes": list(definition.amplitudes),
                "amplitude_unit": "radian",
                "minimum_external_gap": definition.minimum_external_gap,
                "minimum_transport_singular_value": (
                    definition.minimum_transport_singular_value
                ),
                "frame_absolute_tolerance": definition.frame_absolute_tolerance,
                "harmonic_absolute_degeneracy_tolerance": (
                    definition.harmonic_absolute_degeneracy_tolerance
                ),
                "harmonic_relative_degeneracy_tolerance": (
                    definition.harmonic_relative_degeneracy_tolerance
                ),
                "verification_absolute_tolerance": (
                    definition.verification_absolute_tolerance
                ),
                "parent_hopping_scale": definition.parent_hopping_scale,
                "scope": {
                    "continuous_global_alignment": True,
                    "external_calculator_execution": False,
                    "material_validation": False,
                    "protocol_frozen": False,
                    "provenance_record": False,
                    "retained_run": False,
                },
            }
        )


class SmoothFourStateResultSerializer:
    """Encode qualification, alignment, and finite-Fourier channels."""

    __slots__ = ()

    def serialize(self, result: SmoothFourStateResult) -> bytes:
        """Return canonical result bytes bound to the exact input document."""
        if type(result) is not SmoothFourStateResult:
            raise TypeError("result must be SmoothFourStateResult")
        input_wire = SmoothFourStateInputSerializer().serialize(result.definition)
        return canonical_json_bytes(
            {
                "schema": SMOOTH_FOUR_STATE_RESULT_SCHEMA_ID,
                "identity": smooth_four_state_identity_document(),
                "input_binding": {
                    "schema": SMOOTH_FOUR_STATE_INPUT_SCHEMA_ID,
                    "sha256": hashlib.sha256(input_wire).hexdigest(),
                },
                "qualification": {
                    "minimum_external_gap": result.minimum_external_gap,
                    "minimum_transport_singular_value": (
                        result.minimum_transport_singular_value
                    ),
                    "maximum_transport_procrustes_residual": (
                        result.maximum_transport_procrustes_residual
                    ),
                    "maximum_transport_unitarity_residual": (
                        result.maximum_transport_unitarity_defect
                    ),
                    "maximum_transport_rank_cutoff": (
                        result.maximum_transport_rank_cutoff
                    ),
                    "closure_holonomy_phases": list(result.closure_holonomy_phases),
                    "closure_holonomy_unitarity_residual": (
                        result.closure_holonomy_unitarity_defect
                    ),
                    "maximum_frame_orthonormality_residual": (
                        result.maximum_frame_orthonormality_defect
                    ),
                    "periodic_closure_residual": result.periodic_closure_defect,
                    "maximum_reference_hermiticity_residual": (
                        result.maximum_reference_hermiticity_defect
                    ),
                },
                "points": [_point(point) for point in result.points],
                "interpretation": {
                    "complete_band_equivalence_is_locality_equivalence": False,
                    "finite_mesh_correlations_are_continuum_correlations": False,
                    "flat_parent_residual_locality_identity_assumed": False,
                    "scientific_acceptance": False,
                    "retained_evidence": False,
                },
            }
        )


class SmoothFourStateVerificationSerializer:
    """Encode independent non-flat reconstruction evidence."""

    __slots__ = ()

    def serialize(self, verification: SmoothFourStateVerificationResult) -> bytes:
        """Return canonical verification bytes bound to one member result."""
        if type(verification) is not SmoothFourStateVerificationResult:
            raise TypeError("verification must be SmoothFourStateVerificationResult")
        if type(verification.experiment_result) is not SmoothFourStateResult:
            raise TypeError(
                "verification must contain one SmoothFourStateResult; "
                "parent-family serialization is a separate contract"
            )
        result_wire = SmoothFourStateResultSerializer().serialize(
            verification.experiment_result
        )
        return canonical_json_bytes(
            {
                "schema": SMOOTH_FOUR_STATE_VERIFICATION_SCHEMA_ID,
                "identity": smooth_four_state_identity_document(),
                "result_binding": {
                    "schema": SMOOTH_FOUR_STATE_RESULT_SCHEMA_ID,
                    "sha256": hashlib.sha256(result_wire).hexdigest(),
                },
                "passes": verification.passes,
                "absolute_tolerance": verification.absolute_tolerance,
                "maximum_absolute_discrepancy": (verification.maximum_absolute_defect),
                "claim_boundary": (
                    "Passing establishes development reconstruction of sampled "
                    "non-flat channels only; it does not freeze a protocol, create "
                    "provenance, retain evidence, or establish material validity."
                ),
            }
        )


def _point(value: SmoothFourStatePointResult) -> dict[str, JsonValue]:
    """Encode one directly sampled amplitude and its complete block inventory."""
    maximum = value.harmonic_maximum
    return {
        "amplitude": value.amplitude,
        "maximum_band_discrepancy": value.maximum_band_defect,
        "splitting_scale": value.splitting_scale,
        "continuous_alignment": {
            "harmonic_offset": maximum.harmonic.offset,
            "harmonic_cosine_coefficient": maximum.harmonic.cosine_coefficient,
            "harmonic_sine_coefficient": maximum.harmonic.sine_coefficient,
            "harmonic_order": maximum.harmonic.harmonic_order,
            "fundamental_interval_start": (maximum.harmonic.fundamental_interval_start),
            "status": maximum.status.value,
            "harmonic_amplitude": maximum.amplitude,
            "applied_degeneracy_cutoff": maximum.applied_degeneracy_cutoff,
            "canonical_maximizing_angle": maximum.canonical_maximizing_argument,
            "maximum_value": maximum.maximum_value,
        },
        "finite_mesh": {
            "maximum_correlation": value.discrete_maximum_correlation,
            "minimum_operator_threshold": value.minimum_operator_threshold,
            "exact_spectrum_joint_operator_threshold": (
                value.exact_spectrum_joint_operator_threshold
            ),
            "minimum_loss_reconstruction_residual": (
                value.minimum_loss_reconstruction_defect
            ),
            "reference_nonzero_hopping_weight": (
                value.reference_nonzero_hopping_weight
            ),
            "comparison_nonzero_hopping_weight": (
                value.comparison_nonzero_hopping_weight
            ),
            "reference_parseval_residual": value.reference_parseval_defect,
            "comparison_parseval_residual": value.comparison_parseval_defect,
            "hopping_blocks": [_block(item) for item in value.hopping_blocks],
        },
    }


def _block(value: SmoothFourStateHoppingBlockResult) -> dict[str, JsonValue]:
    """Encode one cyclic finite-mesh displacement."""
    return {
        "displacement": value.displacement,
        "reference_normalized_squared_frobenius_norm": (
            value.reference_normalized_squared_frobenius_norm
        ),
        "comparison_normalized_squared_frobenius_norm": (
            value.comparison_normalized_squared_frobenius_norm
        ),
    }


__all__ = [
    "SmoothFourStateInputSerializer",
    "SmoothFourStateResultSerializer",
    "SmoothFourStateVerificationSerializer",
    "smooth_four_state_identity_document",
]
