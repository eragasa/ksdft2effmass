"""Canonical JSON serialization for the smooth continuum convergence study."""

from __future__ import annotations

import hashlib
import json

from .definition import (
    CONTINUOUS_ALIGNMENT_METHOD_ID,
    EXPERIMENT_FAMILY_ID,
    FOURIER_CONVENTION_ID,
    FOURIER_NORMALIZATION_ID,
    SMOOTH_CONTINUUM_INPUT_SCHEMA_ID,
    SMOOTH_CONTINUUM_METHOD_ID,
    SMOOTH_CONTINUUM_RESULT_SCHEMA_ID,
    SMOOTH_CONTINUUM_VERIFICATION_SCHEMA_ID,
    SmoothBlochContinuumConvergenceDefinition,
)
from .results import (
    SmoothBlochContinuumConvergenceResult,
    SmoothBlochContinuumPointResult,
    SmoothBlochContinuumRefinementResult,
    SmoothBlochContinuumResult,
)
from .verify import SmoothBlochContinuumConvergenceVerificationResult

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def canonical_json_bytes(document: dict[str, JsonValue]) -> bytes:
    """Return sorted finite UTF-8 JSON terminated by one line feed."""
    if type(document) is not dict:
        raise TypeError("document must be a built-in dict")
    return (
        json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def smooth_continuum_identity_document() -> dict[str, JsonValue]:
    """Return publication-independent method identities without a version claim."""
    return {
        "family_id": EXPERIMENT_FAMILY_ID,
        "method_id": SMOOTH_CONTINUUM_METHOD_ID,
        "alignment_method_id": CONTINUOUS_ALIGNMENT_METHOD_ID,
        "parent_model_id": "normalized-flat-rank-two-traceless-parent.v1",
        "reduced_coordinate_id": "q-equals-k-over-reciprocal-period.v1",
        "fourier_convention_id": FOURIER_CONVENTION_ID,
        "fourier_normalization_id": FOURIER_NORMALIZATION_ID,
    }


class SmoothBlochContinuumInputSerializer:
    """Encode explicit nested meshes, amplitudes, and caller-selected tolerances."""

    __slots__ = ()

    def serialize(self, definition: SmoothBlochContinuumConvergenceDefinition) -> bytes:
        """Return one canonical continuum-study input document."""
        if type(definition) is not SmoothBlochContinuumConvergenceDefinition:
            raise TypeError(
                "definition must be SmoothBlochContinuumConvergenceDefinition"
            )
        thresholds = definition.thresholds
        return canonical_json_bytes(
            {
                "schema": SMOOTH_CONTINUUM_INPUT_SCHEMA_ID,
                "identity": smooth_continuum_identity_document(),
                "reciprocal_mesh_sizes": list(definition.reciprocal_mesh_sizes),
                "mesh_rule": "nested-uniform-half-open-doubling.v1",
                "amplitudes": list(definition.amplitudes),
                "amplitude_unit": "radian",
                "harmonic_absolute_degeneracy_tolerance": (
                    definition.harmonic_absolute_degeneracy_tolerance
                ),
                "harmonic_relative_degeneracy_tolerance": (
                    definition.harmonic_relative_degeneracy_tolerance
                ),
                "verification_absolute_tolerance": (
                    definition.verification_absolute_tolerance
                ),
                "required_stable_refinements": (definition.required_stable_refinements),
                "convergence_thresholds": {
                    "maximum_correlation_change": (
                        thresholds.maximum_correlation_change
                    ),
                    "maximum_threshold_change": (thresholds.maximum_threshold_change),
                    "maximum_hopping_weight_change": (
                        thresholds.maximum_hopping_weight_change
                    ),
                    "maximum_hopping_block_power_change": (
                        thresholds.maximum_hopping_block_power_change
                    ),
                    "maximum_angle_change": thresholds.maximum_angle_change,
                    "maximum_fine_quadrature_defect": (
                        thresholds.maximum_fine_quadrature_defect
                    ),
                    "maximum_band_defect": thresholds.maximum_band_defect,
                    "maximum_identity_defect": thresholds.maximum_identity_defect,
                    "maximum_parseval_defect": thresholds.maximum_parseval_defect,
                },
                "scope": {
                    "continuous_global_alignment": True,
                    "external_calculator_execution": False,
                    "material_validation": False,
                    "scientific_acceptance": False,
                    "retained_run": False,
                },
            }
        )


class SmoothBlochContinuumResultSerializer:
    """Encode finite-mesh evidence separately from analytic comparators."""

    __slots__ = ()

    def serialize(self, result: SmoothBlochContinuumConvergenceResult) -> bytes:
        """Return one canonical continuum convergence result document."""
        if type(result) is not SmoothBlochContinuumConvergenceResult:
            raise TypeError("result must be SmoothBlochContinuumConvergenceResult")
        input_wire = SmoothBlochContinuumInputSerializer().serialize(result.definition)
        return canonical_json_bytes(
            {
                "schema": SMOOTH_CONTINUUM_RESULT_SCHEMA_ID,
                "identity": smooth_continuum_identity_document(),
                "input_binding": {
                    "schema": SMOOTH_CONTINUUM_INPUT_SCHEMA_ID,
                    "sha256": hashlib.sha256(input_wire).hexdigest(),
                },
                "mesh_results": [_mesh_result(item) for item in result.mesh_results],
                "refinements": [_refinement(item) for item in result.refinements],
                "disposition": result.disposition.value,
                "interpretation": {
                    "band_equivalence_is_locality_equivalence": False,
                    "finite_mesh_and_analytic_correlations_are_distinct": True,
                    "fourier_blocks_are_finite_mesh_aliased_coefficients": True,
                    "convergence_is_scientific_validation": False,
                },
            }
        )


class SmoothBlochContinuumVerificationSerializer:
    """Encode independent mesh and refinement reconstruction evidence."""

    __slots__ = ()

    def serialize(
        self, verification: SmoothBlochContinuumConvergenceVerificationResult
    ) -> bytes:
        """Return one canonical verification document bound to result bytes."""
        if type(verification) is not SmoothBlochContinuumConvergenceVerificationResult:
            raise TypeError(
                "verification must be SmoothBlochContinuumConvergenceVerificationResult"
            )
        result_wire = SmoothBlochContinuumResultSerializer().serialize(
            verification.experiment_result
        )
        return canonical_json_bytes(
            {
                "schema": SMOOTH_CONTINUUM_VERIFICATION_SCHEMA_ID,
                "identity": smooth_continuum_identity_document(),
                "result_binding": {
                    "schema": SMOOTH_CONTINUUM_RESULT_SCHEMA_ID,
                    "sha256": hashlib.sha256(result_wire).hexdigest(),
                },
                "mesh_maximum_absolute_defects": [
                    item.maximum_absolute_defect
                    for item in verification.mesh_verifications
                ],
                "mesh_passes": [
                    item.passes for item in verification.mesh_verifications
                ],
                "maximum_refinement_absolute_defect": (
                    verification.maximum_refinement_absolute_defect
                ),
                "disposition_matches": verification.disposition_matches,
                "passes": verification.passes,
                "claim_boundary": (
                    "Passing establishes bounded analytic-family software and mesh-"
                    "convergence consistency only; it does not establish material "
                    "validity, scientific acceptance, or uncertainty quantification."
                ),
            }
        )


def _mesh_result(value: SmoothBlochContinuumResult) -> dict[str, JsonValue]:
    """Encode one finite reciprocal mesh without replacing it by analytic values."""
    return {
        "reciprocal_mesh_size": value.definition.reciprocal_mesh_size,
        "points": [_point(point) for point in value.points],
    }


def _point(value: SmoothBlochContinuumPointResult) -> dict[str, JsonValue]:
    """Encode all side-by-side channels at one amplitude."""
    maximum = value.harmonic_maximum
    return {
        "amplitude": value.amplitude,
        "maximum_band_defect": value.maximum_band_defect,
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
            "irreducible_operator_squared_loss": (
                value.irreducible_operator_squared_loss
            ),
            "nonzero_hopping_weight": value.nonzero_hopping_weight,
            "onsite_mismatch_squared": value.onsite_mismatch_squared,
            "hopping_blocks": [
                {
                    "displacement": item.displacement,
                    "normalized_squared_frobenius_norm": (
                        item.normalized_squared_frobenius_norm
                    ),
                }
                for item in value.hopping_blocks
            ],
        },
        "analytic_comparator": {
            "bessel_j0_of_twice_amplitude": value.analytic_maximum_correlation,
            "minimum_operator_threshold": (value.analytic_minimum_operator_threshold),
            "exact_spectrum_joint_operator_threshold": (
                value.analytic_exact_spectrum_joint_operator_threshold
            ),
        },
        "defects": {
            "correlation_quadrature": value.correlation_quadrature_defect,
            "three_way_identity": value.three_way_identity_defect,
            "parseval": value.parseval_defect,
        },
    }


def _refinement(value: SmoothBlochContinuumRefinementResult) -> dict[str, JsonValue]:
    """Encode one adjacent nested-mesh comparison."""
    return {
        "coarse_mesh_size": value.coarse_mesh_size,
        "fine_mesh_size": value.fine_mesh_size,
        "maximum_correlation_change": value.maximum_correlation_change,
        "maximum_threshold_change": value.maximum_threshold_change,
        "maximum_hopping_weight_change": value.maximum_hopping_weight_change,
        "maximum_hopping_block_power_change": (
            value.maximum_hopping_block_power_change
        ),
        "maximum_angle_change": value.maximum_angle_change,
        "maximizing_angle_dispositions_stable": (
            value.maximizing_angle_dispositions_stable
        ),
        "maximum_fine_quadrature_defect": value.maximum_fine_quadrature_defect,
        "maximum_band_defect": value.maximum_band_defect,
        "maximum_identity_defect": value.maximum_identity_defect,
        "maximum_parseval_defect": value.maximum_parseval_defect,
        "within_tolerances": value.within_tolerances,
    }


__all__ = [
    "SmoothBlochContinuumInputSerializer",
    "SmoothBlochContinuumResultSerializer",
    "SmoothBlochContinuumVerificationSerializer",
    "canonical_json_bytes",
    "smooth_continuum_identity_document",
]
