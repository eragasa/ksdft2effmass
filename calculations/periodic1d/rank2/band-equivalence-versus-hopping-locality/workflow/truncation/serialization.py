"""Canonical development serialization for dense truncation calculations."""

from __future__ import annotations

import hashlib

from ..definition import EXPERIMENT_FAMILY_ID
from ..nonflat.definition import SMOOTH_FOUR_STATE_PARENT_ID
from ..serialization import JsonValue, canonical_json_bytes
from .definition import (
    SMOOTH_FOUR_STATE_TRUNCATION_INPUT_SCHEMA_ID,
    SMOOTH_FOUR_STATE_TRUNCATION_METHOD_ID,
    SMOOTH_FOUR_STATE_TRUNCATION_RESULT_SCHEMA_ID,
    SMOOTH_FOUR_STATE_TRUNCATION_VERIFICATION_SCHEMA_ID,
    SmoothFourStateTruncationDefinition,
)
from .results import (
    SmoothFourStateTruncationPointResult,
    SmoothFourStateTruncationRangeResult,
    SmoothFourStateTruncationResult,
)
from .verify import (
    SmoothFourStateTruncationRangeDecision,
    SmoothFourStateTruncationVerificationResult,
)


def truncation_identity_document() -> dict[str, JsonValue]:
    """Return method identities without assigning a frozen experiment version."""
    return {
        "family_id": EXPERIMENT_FAMILY_ID,
        "method_id": SMOOTH_FOUR_STATE_TRUNCATION_METHOD_ID,
        "parent_model_id": SMOOTH_FOUR_STATE_PARENT_ID,
        "reciprocal_coordinate_id": "q-equals-k-over-reciprocal-period.v1",
        "finite_fourier_id": "centered-finite-cyclic-fourier.v1",
        "ordinary_lattice_conversion_id": "remove-centered-nyquist-block.v1",
        "range_rule_id": "symmetric-ordinary-integer-displacements.v1",
    }


class SmoothFourStateTruncationInputSerializer:
    """Encode all development controls without implying protocol freeze."""

    __slots__ = ()

    def serialize(self, definition: SmoothFourStateTruncationDefinition) -> bytes:
        """Return one canonical truncation input document."""
        if type(definition) is not SmoothFourStateTruncationDefinition:
            raise TypeError("definition must be SmoothFourStateTruncationDefinition")
        model = definition.model
        return canonical_json_bytes(
            {
                "schema": SMOOTH_FOUR_STATE_TRUNCATION_INPUT_SCHEMA_ID,
                "identity": truncation_identity_document(),
                "model": {
                    "reciprocal_mesh_size": model.reciprocal_mesh_size,
                    "amplitudes": list(model.amplitudes),
                    "amplitude_unit": "radian",
                    "minimum_external_gap": model.minimum_external_gap,
                    "minimum_transport_singular_value": (
                        model.minimum_transport_singular_value
                    ),
                    "frame_absolute_tolerance": model.frame_absolute_tolerance,
                    "harmonic_absolute_degeneracy_tolerance": (
                        model.harmonic_absolute_degeneracy_tolerance
                    ),
                    "harmonic_relative_degeneracy_tolerance": (
                        model.harmonic_relative_degeneracy_tolerance
                    ),
                    "verification_absolute_tolerance": (
                        model.verification_absolute_tolerance
                    ),
                    "parent_hopping_scale": model.parent_hopping_scale,
                },
                "maximum_ranges": list(definition.maximum_ranges),
                "dense_integer_inventory": (definition.has_dense_integer_inventory),
                "evaluation_mesh_size": definition.evaluation_mesh_size,
                "evaluation_mesh_rule": "deterministic-shifted-disjoint-mesh.v1",
                "scope": {
                    "external_calculator_execution": False,
                    "material_validation": False,
                    "protocol_frozen": False,
                    "provenance_record": False,
                    "retained_run": False,
                },
            }
        )


class SmoothFourStateTruncationResultSerializer:
    """Encode conversion, truncation, matrix, and spectral channels."""

    __slots__ = ()

    def serialize(self, result: SmoothFourStateTruncationResult) -> bytes:
        """Return one canonical development result bound to exact input bytes."""
        if type(result) is not SmoothFourStateTruncationResult:
            raise TypeError("result must be SmoothFourStateTruncationResult")
        input_wire = SmoothFourStateTruncationInputSerializer().serialize(
            result.definition
        )
        return canonical_json_bytes(
            {
                "schema": SMOOTH_FOUR_STATE_TRUNCATION_RESULT_SCHEMA_ID,
                "identity": truncation_identity_document(),
                "input_binding": {
                    "schema": SMOOTH_FOUR_STATE_TRUNCATION_INPUT_SCHEMA_ID,
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
                "evaluation": {
                    "coordinate_offset": result.evaluation_coordinate_offset,
                    "minimum_construction_evaluation_separation": (
                        result.minimum_construction_evaluation_separation
                    ),
                },
                "points": [_point(point) for point in result.points],
                "interpretation": {
                    "conversion_interpolation_and_truncation_are_separate": True,
                    "hamiltonian_and_spectral_decisions_are_separate": True,
                    "scientific_acceptance": False,
                    "retained_evidence": False,
                },
            }
        )


class SmoothFourStateTruncationVerificationSerializer:
    """Encode independent reconstruction and range decisions."""

    __slots__ = ()

    def serialize(
        self, verification: SmoothFourStateTruncationVerificationResult
    ) -> bytes:
        """Return canonical verification bytes bound to the result document."""
        if type(verification) is not SmoothFourStateTruncationVerificationResult:
            raise TypeError(
                "verification must be SmoothFourStateTruncationVerificationResult"
            )
        result_wire = SmoothFourStateTruncationResultSerializer().serialize(
            verification.experiment_result
        )
        return canonical_json_bytes(
            {
                "schema": SMOOTH_FOUR_STATE_TRUNCATION_VERIFICATION_SCHEMA_ID,
                "identity": truncation_identity_document(),
                "result_binding": {
                    "schema": SMOOTH_FOUR_STATE_TRUNCATION_RESULT_SCHEMA_ID,
                    "sha256": hashlib.sha256(result_wire).hexdigest(),
                },
                "passes": verification.passes,
                "absolute_tolerance": verification.absolute_tolerance,
                "maximum_absolute_discrepancy": (
                    verification.maximum_absolute_discrepancy
                ),
                "inventory_is_dense": verification.inventory_is_dense,
                "decisions": [
                    _decision(decision) for decision in verification.decisions
                ],
                "claim_boundary": (
                    "Passing verifies development reconstruction and first-passing "
                    "decisions only; it does not freeze a protocol, create provenance, "
                    "retain evidence, or establish material validity."
                ),
            }
        )


def _point(value: SmoothFourStateTruncationPointResult) -> dict[str, JsonValue]:
    """Encode one directly sampled amplitude."""
    return {
        "amplitude": value.amplitude,
        "conversion": {
            "reference_nyquist_power": value.reference_nyquist_power,
            "comparison_nyquist_power": value.comparison_nyquist_power,
            "reference_maximum_ordinary_hermiticity_residual": (
                value.reference_maximum_ordinary_hermiticity_defect
            ),
            "comparison_maximum_ordinary_hermiticity_residual": (
                value.comparison_maximum_ordinary_hermiticity_defect
            ),
        },
        "complete_model": {
            "maximum_direct_band_discrepancy": value.maximum_direct_band_defect,
            "comparison_maximum_interpolation_hamiltonian_error": (
                value.comparison_maximum_interpolation_hamiltonian_error
            ),
            "comparison_rms_interpolation_hamiltonian_error": (
                value.comparison_rms_interpolation_hamiltonian_error
            ),
            "comparison_maximum_interpolation_band_error": (
                value.comparison_maximum_interpolation_band_error
            ),
            "comparison_rms_interpolation_band_error": (
                value.comparison_rms_interpolation_band_error
            ),
        },
        "ranges": [_range(item) for item in value.ranges],
    }


def _range(value: SmoothFourStateTruncationRangeResult) -> dict[str, JsonValue]:
    """Encode one explicit ordinary-lattice cutoff."""
    return {
        "maximum_range": value.maximum_range,
        "reference_ordinary_omitted_power": value.reference_ordinary_omitted_power,
        "comparison_ordinary_omitted_power": value.comparison_ordinary_omitted_power,
        "reference_total_omitted_power": value.reference_total_omitted_power,
        "comparison_total_omitted_power": value.comparison_total_omitted_power,
        "reference_maximum_truncation_hamiltonian_error": (
            value.reference_maximum_truncation_hamiltonian_error
        ),
        "reference_rms_truncation_hamiltonian_error": (
            value.reference_rms_truncation_hamiltonian_error
        ),
        "reference_maximum_band_error": value.reference_maximum_band_error,
        "reference_rms_band_error": value.reference_rms_band_error,
        "comparison_maximum_truncation_hamiltonian_error": (
            value.comparison_maximum_truncation_hamiltonian_error
        ),
        "comparison_rms_truncation_hamiltonian_error": (
            value.comparison_rms_truncation_hamiltonian_error
        ),
        "comparison_maximum_truncation_band_error": (
            value.comparison_maximum_truncation_band_error
        ),
        "comparison_rms_truncation_band_error": (
            value.comparison_rms_truncation_band_error
        ),
        "comparison_maximum_total_hamiltonian_error": (
            value.comparison_maximum_total_hamiltonian_error
        ),
        "comparison_rms_total_hamiltonian_error": (
            value.comparison_rms_total_hamiltonian_error
        ),
        "comparison_maximum_total_band_error": (
            value.comparison_maximum_total_band_error
        ),
        "comparison_rms_total_band_error": value.comparison_rms_total_band_error,
    }


def _decision(value: SmoothFourStateTruncationRangeDecision) -> dict[str, JsonValue]:
    """Encode separate matrix and spectral first-passing decisions."""
    return {
        "amplitude": value.amplitude,
        "tolerance": value.tolerance,
        "reference_band_first_passing_range": (
            value.reference_band_first_passing_range
        ),
        "comparison_band_first_passing_range": (
            value.comparison_band_first_passing_range
        ),
        "reference_hamiltonian_first_passing_range": (
            value.reference_hamiltonian_first_passing_range
        ),
        "comparison_hamiltonian_first_passing_range": (
            value.comparison_hamiltonian_first_passing_range
        ),
        "band_range_inflation": value.band_range_inflation,
        "hamiltonian_range_inflation": value.hamiltonian_range_inflation,
    }


__all__ = [
    "SmoothFourStateTruncationInputSerializer",
    "SmoothFourStateTruncationResultSerializer",
    "SmoothFourStateTruncationVerificationSerializer",
    "truncation_identity_document",
]
