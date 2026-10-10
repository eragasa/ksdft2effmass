"""Deterministic schema-v1 encoding for multiband alignment results."""

from __future__ import annotations

import json

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityResult1D,
)
from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity
from ksdft2effmass.serialization import JsonSerializer
from ksdft2effmass.solid_state import ReciprocalOperatorFourierTransformResult1D

from .results import (
    Periodic1DMultibandAlignmentCalculationResult,
    Periodic1DMultibandAlignmentRangeResult,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

SCHEMA_ID = "ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1"


class Periodic1DMultibandAlignmentResultJsonSerializer(
    JsonSerializer[Periodic1DMultibandAlignmentCalculationResult, bytes]
):
    """Encode M2 without reusing historical periodic-campaign identities."""

    __slots__ = ()

    def serialize(self, record: Periodic1DMultibandAlignmentCalculationResult) -> bytes:
        """Return canonical UTF-8 JSON bytes terminated by one newline."""
        if type(record) is not Periodic1DMultibandAlignmentCalculationResult:
            raise TypeError(
                "record must be Periodic1DMultibandAlignmentCalculationResult"
            )
        return (
            json.dumps(
                self._document(record),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")

    def _document(
        self, record: Periodic1DMultibandAlignmentCalculationResult
    ) -> dict[str, JsonValue]:
        definition = record.definition
        model = definition.parent_model
        parent = model.hopping_model
        diagnostics = record.diagnostics
        return {
            "schema": SCHEMA_ID,
            "definition": {
                "calculation_id": definition.calculation_id,
                "parent_model": {
                    "model_id": model.model_id,
                    "model_role": model.model_role.value,
                    "reciprocal_period": self._quantity(parent.reciprocal_period),
                    "representatives": list(parent.representatives),
                    "hopping_blocks": [
                        self._complex_matrix(block) for block in parent.hopping_blocks
                    ],
                    "hermiticity_absolute_tolerance": self._quantity(
                        model.hermiticity_absolute_tolerance
                    ),
                },
                "retained_rank": definition.retained_rank,
                "reciprocal_mesh_size": definition.reciprocal_mesh_size,
                "withheld_mesh_size": definition.withheld_mesh_size,
                "withheld_mesh_rule": "staggered-uniform-disjoint-v1",
                "withheld_reduced_momenta": list(definition.withheld_reduced_momenta),
                "hopping_ranges": list(definition.hopping_ranges),
                "attack": {
                    "family": "rank-two-real-rotation-sine-series-v1",
                    "constant_angle": definition.attack_constant_angle,
                    "sine_coefficients": list(definition.attack_sine_coefficients),
                },
                "external_gap_lower_bound": self._quantity(
                    definition.external_gap_lower_bound
                ),
                "overlap_singular_value_threshold": (
                    definition.overlap_singular_value_threshold
                ),
                "orthonormality_absolute_tolerance": (
                    definition.orthonormality_absolute_tolerance
                ),
                "coordinate_absolute_tolerance": (
                    definition.coordinate_absolute_tolerance
                ),
                "reconstruction_absolute_tolerance": (
                    definition.reconstruction_absolute_tolerance
                ),
                "hermiticity_absolute_tolerance": self._quantity(
                    definition.hermiticity_absolute_tolerance
                ),
                "verification_absolute_tolerance": (
                    definition.verification_absolute_tolerance
                ),
            },
            "training_target": self._spectrum(record.training_target),
            "withheld_target": self._spectrum(record.withheld_target),
            "alignment_diagnostics": {
                "external_gap_minimum": self._quantity(
                    diagnostics.external_gap_minimum
                ),
                "minimum_neighbor_or_closure_overlap_singular_value": (
                    diagnostics.transport.minimum_overlap_singular_value
                ),
                "closure_eigenphases": list(diagnostics.transport.closure_eigenphases),
                "projector_maximum_frobenius_defect": (
                    diagnostics.pointwise_alignment.projector_maximum_frobenius_defect
                ),
                "attack_frame_maximum_frobenius_defect": (
                    diagnostics.attack_frame_maximum_frobenius_defect
                ),
                "pointwise_frame_maximum_frobenius_defect": (
                    diagnostics.pointwise_alignment.frame_maximum_frobenius_defect
                ),
                "pointwise_rotation_recovery_maximum_frobenius_defect": (
                    diagnostics.pointwise_rotation_recovery_maximum_frobenius_defect
                ),
                "constrained_global_rotation": self._complex_matrix(
                    diagnostics.constrained_rotation
                ),
                "constrained_frame_maximum_frobenius_defect": (
                    diagnostics.constrained_frame_maximum_frobenius_defect
                ),
                "attacked_operator_maximum_frobenius_defect": self._quantity(
                    diagnostics.attacked_operator_maximum_frobenius_defect
                ),
                "pointwise_operator_maximum_frobenius_defect": self._quantity(
                    diagnostics.pointwise_operator_maximum_frobenius_defect
                ),
                "constrained_operator_maximum_frobenius_defect": self._quantity(
                    diagnostics.constrained_operator_maximum_frobenius_defect
                ),
            },
            "complete_transforms": {
                "reference": self._transform(
                    record.reference_transform, record.reference_hermiticity
                ),
                "attacked": self._transform(
                    record.attacked_transform, record.attacked_hermiticity
                ),
                "pointwise_aligned": self._transform(
                    record.aligned_transform, record.aligned_hermiticity
                ),
            },
            "range_study": [self._range(item) for item in record.range_study],
            "scope": {
                "pointwise_procrustes_included": True,
                "global_unitary_constraint_included": True,
                "general_nonconvex_alignment_solution_included": False,
                "material_validation_included": False,
                "uncertainty_quantification_included": False,
                "external_calculator_execution_included": False,
                "scientific_acceptance_included": False,
            },
        }

    def _transform(
        self,
        transform: ReciprocalOperatorFourierTransformResult1D,
        hermiticity: BlockHoppingHermiticityResult1D,
    ) -> dict[str, JsonValue]:
        model = transform.hopping_model
        return {
            "representatives": list(model.representatives),
            "hopping_blocks": [
                self._complex_matrix(block) for block in model.hopping_blocks
            ],
            "reconstruction_maximum_frobenius_error": self._scalar(
                transform.reconstruction_maximum_frobenius_error,
                model.hopping_blocks[0].unit.expression,
            ),
            "reconstruction_absolute_tolerance": self._scalar(
                transform.reconstruction_absolute_tolerance,
                model.hopping_blocks[0].unit.expression,
            ),
            "reconstruction_passes": transform.reconstruction_passes,
            "hermiticity": {
                "maximum_frobenius_defect": self._quantity(
                    hermiticity.maximum_frobenius_defect
                ),
                "absolute_tolerance": self._quantity(hermiticity.absolute_tolerance),
                "passes": hermiticity.passes,
            },
        }

    def _range(
        self, result: Periodic1DMultibandAlignmentRangeResult
    ) -> dict[str, JsonValue]:
        return {
            "maximum_range": result.maximum_range,
            "reference": self._range_channel(
                result.reference_truncation.omitted_block_l2_norm,
                result.reference_training_error.maximum_absolute_error,
                result.reference_withheld_error.maximum_absolute_error,
            ),
            "attacked": self._range_channel(
                result.attacked_truncation.omitted_block_l2_norm,
                result.attacked_training_error.maximum_absolute_error,
                result.attacked_withheld_error.maximum_absolute_error,
            ),
            "pointwise_aligned": self._range_channel(
                result.aligned_truncation.omitted_block_l2_norm,
                result.aligned_training_error.maximum_absolute_error,
                result.aligned_withheld_error.maximum_absolute_error,
            ),
        }

    @staticmethod
    def _range_channel(
        omitted_norm: float,
        training_error: ScalarQuantity,
        withheld_error: ScalarQuantity,
    ) -> dict[str, JsonValue]:
        return {
            "omitted_block_l2_norm": {
                "magnitude": omitted_norm,
                "unit": training_error.unit.expression,
            },
            "training_maximum_absolute_spectral_error": {
                "magnitude": training_error.magnitude,
                "unit": training_error.unit.expression,
            },
            "withheld_maximum_absolute_spectral_error": {
                "magnitude": withheld_error.magnitude,
                "unit": withheld_error.unit.expression,
            },
        }

    @staticmethod
    def _spectrum(spectrum: BandSpectrumSamples1D) -> dict[str, JsonValue]:
        return {
            "coordinates": {
                "magnitude": spectrum.coordinates.magnitude.tolist(),
                "unit": spectrum.coordinates.unit.expression,
            },
            "reciprocal_period": {
                "magnitude": spectrum.reciprocal_period.magnitude,
                "unit": spectrum.reciprocal_period.unit.expression,
            },
            "eigenvalues": {
                "magnitude": spectrum.eigenvalues.magnitude.tolist(),
                "unit": spectrum.eigenvalues.unit.expression,
            },
        }

    @staticmethod
    def _quantity(quantity: ScalarQuantity) -> dict[str, JsonValue]:
        return {
            "magnitude": quantity.magnitude,
            "unit": quantity.unit.expression,
        }

    @staticmethod
    def _scalar(magnitude: float, unit: str) -> dict[str, JsonValue]:
        return {"magnitude": magnitude, "unit": unit}

    @staticmethod
    def _complex_matrix(matrix: ComplexMatrixQuantity) -> dict[str, JsonValue]:
        return {
            "magnitude": [
                [[float(value.real), float(value.imag)] for value in row]
                for row in matrix.magnitude
            ],
            "unit": matrix.unit.expression,
        }


__all__ = ["Periodic1DMultibandAlignmentResultJsonSerializer", "SCHEMA_ID"]
