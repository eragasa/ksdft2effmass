"""Deterministic schema-v1 encoding for constrained admissible-set results."""

from __future__ import annotations

import json

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity
from ksdft2effmass.serialization import JsonSerializer

from .definition import Periodic1DAdmissibleSetThresholds
from .results import (
    Periodic1DAdmissibleSetCaseResult,
    Periodic1DAdmissibleSetParameterEvaluation,
    Periodic1DConstrainedAdmissibleSetCalculationResult,
    Periodic1DQuadraticLoss,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

SCHEMA_ID = "ksdft2effmass.periodic1d.constrained-admissible-set-result.v1"


class Periodic1DConstrainedAdmissibleSetResultJsonSerializer(
    JsonSerializer[Periodic1DConstrainedAdmissibleSetCalculationResult, bytes]
):
    """Encode the complete M3 proof result under its distinct schema identity.

    The document preserves the composed M2 controls, continuous parameter rectangle,
    finite angle family, normalized loss convention, analytic quadratics, witness and
    certificate evaluations, locality, and explicit scope exclusions. Serialization
    owns wire mechanics only.
    """

    __slots__ = ()

    def serialize(
        self, record: Periodic1DConstrainedAdmissibleSetCalculationResult
    ) -> bytes:
        """Return one exact M3 result as canonical finite UTF-8 JSON.

        Parameters
        ----------
        record
            Exact correlated M3 result; proof objects are encoded, not recomputed.

        Returns
        -------
        bytes
            Sorted compact schema-v1 JSON with one terminal newline.
        """
        if type(record) is not Periodic1DConstrainedAdmissibleSetCalculationResult:
            raise TypeError(
                "record must be Periodic1DConstrainedAdmissibleSetCalculationResult"
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
        self, record: Periodic1DConstrainedAdmissibleSetCalculationResult
    ) -> dict[str, JsonValue]:
        """Build the complete M3 schema-v1 JSON value tree."""
        definition = record.definition
        baseline_definition = definition.multiband_baseline
        model = baseline_definition.parent_model
        parent = model.hopping_model
        baseline_diagnostics = record.multiband_baseline.diagnostics
        return {
            "schema": SCHEMA_ID,
            "definition": {
                "calculation_id": definition.calculation_id,
                "multiband_baseline": {
                    "calculation_id": baseline_definition.calculation_id,
                    "parent_model": {
                        "model_id": model.model_id,
                        "model_role": model.model_role.value,
                        "reciprocal_period": self._quantity(parent.reciprocal_period),
                        "representatives": list(parent.representatives),
                        "hopping_blocks": [
                            self._complex_matrix(block)
                            for block in parent.hopping_blocks
                        ],
                        "hermiticity_absolute_tolerance": self._quantity(
                            model.hermiticity_absolute_tolerance
                        ),
                    },
                    "retained_rank": baseline_definition.retained_rank,
                    "reciprocal_mesh_size": baseline_definition.reciprocal_mesh_size,
                    "withheld_mesh_size": baseline_definition.withheld_mesh_size,
                    "withheld_mesh_rule": "staggered-uniform-disjoint-v1",
                    "hopping_ranges": list(baseline_definition.hopping_ranges),
                    "attack": {
                        "family": "rank-two-real-rotation-sine-series-v1",
                        "constant_angle": baseline_definition.attack_constant_angle,
                        "sine_coefficients": list(
                            baseline_definition.attack_sine_coefficients
                        ),
                    },
                    "external_gap_lower_bound": self._quantity(
                        baseline_definition.external_gap_lower_bound
                    ),
                    "overlap_singular_value_threshold": (
                        baseline_definition.overlap_singular_value_threshold
                    ),
                    "orthonormality_absolute_tolerance": (
                        baseline_definition.orthonormality_absolute_tolerance
                    ),
                    "coordinate_absolute_tolerance": (
                        baseline_definition.coordinate_absolute_tolerance
                    ),
                    "reconstruction_absolute_tolerance": (
                        baseline_definition.reconstruction_absolute_tolerance
                    ),
                    "hermiticity_absolute_tolerance": self._quantity(
                        baseline_definition.hermiticity_absolute_tolerance
                    ),
                    "verification_absolute_tolerance": (
                        baseline_definition.verification_absolute_tolerance
                    ),
                },
                "candidate_family": (
                    "trace-plus-energy-shift-and-positive-traceless-splitting-v1"
                ),
                "parameter_order": ["energy_shift_ratio", "splitting_scale"],
                "energy_shift_ratio_bounds": list(definition.energy_shift_ratio_bounds),
                "splitting_scale_bounds": list(definition.splitting_scale_bounds),
                "alignment_family": "finite-one-global-real-rotation-v1",
                "alignment_angles": list(definition.alignment_angles),
                "loss_energy_scale": self._quantity(definition.loss_energy_scale),
                "loss_normalization": "sqrt(sum-frobenius-squared/(N*rank))/scale",
                "compatible_thresholds": self._thresholds(
                    definition.compatible_thresholds
                ),
                "separated_thresholds": self._thresholds(
                    definition.separated_thresholds
                ),
                "compatible_witness": list(definition.compatible_witness),
                "locality_ranges": list(definition.locality_ranges),
                "separation_metric": "euclidean-parameter-distance",
                "separation_resolution": definition.separation_resolution,
                "quadratic_absolute_tolerance": (
                    definition.quadratic_absolute_tolerance
                ),
                "verification_absolute_tolerance": (
                    definition.verification_absolute_tolerance
                ),
            },
            "baseline_summary": {
                "external_gap_minimum": self._quantity(
                    baseline_diagnostics.external_gap_minimum
                ),
                "minimum_neighbor_or_closure_overlap_singular_value": (
                    baseline_diagnostics.transport.minimum_overlap_singular_value
                ),
                "projector_maximum_frobenius_defect": (
                    baseline_diagnostics.pointwise_alignment.projector_maximum_frobenius_defect
                ),
            },
            "training_quadratic_losses": {
                "spectral": self._loss(record.spectral_loss),
                "operator_components": [
                    self._loss(item) for item in record.operator_losses
                ],
            },
            "cases": [self._case(item) for item in record.cases],
            "scope": {
                "training_defines_admissible_sets": True,
                "withheld_data_changes_models_or_certificates": False,
                "finite_global_alignment_family_only": True,
                "general_nonconvex_alignment_solution_included": False,
                "material_validation_included": False,
                "uncertainty_quantification_included": False,
                "external_calculator_execution_included": False,
                "scientific_acceptance_included": False,
            },
        }

    @staticmethod
    def _thresholds(
        value: Periodic1DAdmissibleSetThresholds,
    ) -> dict[str, JsonValue]:
        """Encode one named spectral/operator threshold pair."""
        return {
            "case_id": value.case_id,
            "spectral_rms_threshold": value.spectral_rms_threshold,
            "operator_rms_threshold": value.operator_rms_threshold,
        }

    @staticmethod
    def _loss(value: Periodic1DQuadraticLoss) -> dict[str, JsonValue]:
        """Encode one centered quadratic proof object and optional angle."""
        return {
            "channel_id": value.channel_id,
            "alignment_angle": value.alignment_angle,
            "center": list(value.center),
            "quadratic_matrix": [list(row) for row in value.quadratic_matrix],
            "minimum_squared_loss": value.minimum_squared_loss,
        }

    def _case(self, value: Periodic1DAdmissibleSetCaseResult) -> dict[str, JsonValue]:
        """Encode one bounded disposition with its witness or certificate."""
        return {
            "thresholds": self._thresholds(value.thresholds),
            "disposition": value.disposition.value,
            "feasible_operator_component_angles": list(
                value.feasible_operator_component_angles
            ),
            "common_witness": (
                None
                if value.common_witness is None
                else self._evaluation(value.common_witness)
            ),
            "spectral_certificate_point": self._evaluation(
                value.spectral_certificate_point
            ),
            "operator_certificate_point": self._evaluation(
                value.operator_certificate_point
            ),
            "separation_lower_bound": value.separation_lower_bound,
            "separation_upper_bound": value.separation_upper_bound,
            "separation_resolution": value.separation_resolution,
        }

    @staticmethod
    def _evaluation(
        value: Periodic1DAdmissibleSetParameterEvaluation,
    ) -> dict[str, JsonValue]:
        """Encode one role-identified training/evaluation proof point."""
        return {
            "role": value.role,
            "parameter": list(value.parameter),
            "selected_alignment_angle": value.selected_alignment_angle,
            "training_spectral_rms_loss": value.training_spectral_rms_loss,
            "training_operator_rms_loss": value.training_operator_rms_loss,
            "withheld_spectral_rms_loss": value.withheld_spectral_rms_loss,
            "withheld_operator_rms_loss": value.withheld_operator_rms_loss,
            "locality": [
                {
                    "maximum_range": item.maximum_range,
                    "reference_omitted_block_l2_norm": (
                        item.reference_omitted_block_l2_norm
                    ),
                    "attacked_omitted_block_l2_norm": (
                        item.attacked_omitted_block_l2_norm
                    ),
                    "candidate_omitted_block_l2_norm": (
                        item.candidate_omitted_block_l2_norm
                    ),
                }
                for item in value.locality
            ],
        }

    @staticmethod
    def _wire_unit(expression: str) -> str:
        """Use the frozen wire symbol for dimensionless model-energy units."""
        return "1" if expression == "dimensionless" else expression

    @classmethod
    def _quantity(cls, value: ScalarQuantity) -> dict[str, JsonValue]:
        """Encode a scalar quantity using the frozen wire-unit spelling."""
        return {
            "magnitude": value.magnitude,
            "unit": cls._wire_unit(value.unit.expression),
        }

    @classmethod
    def _complex_matrix(cls, value: ComplexMatrixQuantity) -> dict[str, JsonValue]:
        """Encode a complex matrix as ordered real/imaginary pairs with units."""
        return {
            "magnitude": [
                [[float(item.real), float(item.imag)] for item in row]
                for row in value.magnitude
            ],
            "unit": cls._wire_unit(value.unit.expression),
        }


__all__ = [
    "Periodic1DConstrainedAdmissibleSetResultJsonSerializer",
    "SCHEMA_ID",
]
