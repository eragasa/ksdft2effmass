"""Deterministic schema-v1 encoding for prospective isolated-band results."""

from __future__ import annotations

import json

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.operators import ScalarQuantity
from ksdft2effmass.serialization import JsonSerializer

from .results import (
    Periodic1DIsolatedBandCalculationResult,
    Periodic1DIsolatedBandRangeResult,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

SCHEMA_ID = "ksdft2effmass.periodic1d.isolated-band-calculation-result.v1"


class Periodic1DIsolatedBandResultJsonSerializer(
    JsonSerializer[Periodic1DIsolatedBandCalculationResult, bytes]
):
    """Encode the new M1 result without reusing historical Appendix G identity.

    The schema records defining model data, all sampling roles, convergence channels,
    complete and finite-range hopping data, direct-fit results, and diagnostics needed
    by a separately maintained retained-evidence verifier. It intentionally contains no
    Wannier localization fields and no scientific acceptance disposition.
    """

    __slots__ = ()

    def serialize(self, record: Periodic1DIsolatedBandCalculationResult) -> bytes:
        """Return the complete M1 result as canonical schema-v1 UTF-8 JSON.

        Parameters
        ----------
        record
            Exact correlated M1 result; serialization never recomputes diagnostics.

        Returns
        -------
        bytes
            Sorted compact JSON with finite values and exactly one terminal newline.

        Raises
        ------
        TypeError
            If ``record`` is not the exact M1 result type.
        ValueError
            If JSON encoding encounters a nonfinite value.
        """
        if type(record) is not Periodic1DIsolatedBandCalculationResult:
            raise TypeError("record must be Periodic1DIsolatedBandCalculationResult")
        document = self._document(record)
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

    def _document(
        self, record: Periodic1DIsolatedBandCalculationResult
    ) -> dict[str, JsonValue]:
        """Build the complete schema-v1 JSON value tree for one M1 result."""
        definition = record.definition
        model = definition.parent_model
        potential = model.potential
        complete = record.complete_transform
        return {
            "schema": SCHEMA_ID,
            "definition": {
                "calculation_id": definition.calculation_id,
                "parent_model": {
                    "model_id": model.model_id,
                    "model_role": model.model_role.value,
                    "period": self._scalar(
                        potential.period.magnitude, potential.period.unit.expression
                    ),
                    "constant_coefficient": self._scalar(
                        potential.constant_coefficient.magnitude,
                        potential.constant_coefficient.unit.expression,
                    ),
                    "cosine_coefficients": self._vector(
                        potential.cosine_coefficients.magnitude.tolist(),
                        potential.cosine_coefficients.unit.expression,
                    ),
                    "sine_coefficients": self._vector(
                        potential.sine_coefficients.magnitude.tolist(),
                        potential.sine_coefficients.unit.expression,
                    ),
                    "reciprocal_vector": self._scalar(
                        model.reciprocal_vector.magnitude,
                        model.reciprocal_vector.unit.expression,
                    ),
                    "recoil_energy": self._scalar(
                        model.recoil_energy.magnitude,
                        model.recoil_energy.unit.expression,
                    ),
                    "duality_absolute_tolerance": model.duality_absolute_tolerance,
                },
                "plane_wave_cutoffs": list(definition.plane_wave_cutoffs),
                "plane_wave_reference_cutoff": (definition.plane_wave_reference_cutoff),
                "production_plane_wave_cutoff": (
                    definition.production_plane_wave_cutoff
                ),
                "finite_difference_points": list(definition.finite_difference_points),
                "parent_sample_reduced_momenta": list(
                    definition.parent_sample_reduced_momenta
                ),
                "compared_band_count": definition.compared_band_count,
                "reciprocal_mesh_size": definition.reciprocal_mesh_size,
                "hopping_ranges": list(definition.hopping_ranges),
                "withheld_mesh_size": definition.withheld_mesh_size,
                "withheld_mesh_rule": "staggered-uniform-disjoint-v1",
                "withheld_reduced_momenta": list(definition.withheld_reduced_momenta),
                "coordinate_absolute_tolerance": (
                    definition.coordinate_absolute_tolerance
                ),
                "reconstruction_absolute_tolerance": (
                    definition.reconstruction_absolute_tolerance
                ),
                "hermiticity_absolute_tolerance": self._quantity(
                    definition.hermiticity_absolute_tolerance
                ),
                "parseval_absolute_tolerance": self._quantity(
                    definition.parseval_absolute_tolerance
                ),
                "imaginary_absolute_tolerance": self._quantity(
                    definition.imaginary_absolute_tolerance
                ),
            },
            "parent_reference": self._spectrum(record.parent_reference),
            "plane_wave_convergence": [
                {
                    "cutoff": item.cutoff,
                    "maximum_absolute_error": self._quantity(
                        item.maximum_absolute_error
                    ),
                }
                for item in record.plane_wave_convergence
            ],
            "finite_difference_convergence": [
                {
                    "point_count": item.point_count,
                    "maximum_absolute_error": self._quantity(
                        item.maximum_absolute_error
                    ),
                }
                for item in record.finite_difference_convergence
            ],
            "training_target": self._spectrum(record.training_target),
            "withheld_target": self._spectrum(record.withheld_target),
            "complete_transform": {
                "representatives": list(complete.hopping_model.representatives),
                "hopping_blocks": [
                    self._complex_matrix(
                        block.magnitude.tolist(), block.unit.expression
                    )
                    for block in complete.hopping_model.hopping_blocks
                ],
                "reconstruction_maximum_frobenius_error": self._scalar(
                    complete.reconstruction_maximum_frobenius_error,
                    complete.hopping_model.hopping_blocks[0].unit.expression,
                ),
                "reconstruction_absolute_tolerance": self._scalar(
                    complete.reconstruction_absolute_tolerance,
                    complete.hopping_model.hopping_blocks[0].unit.expression,
                ),
                "reconstruction_passes": complete.reconstruction_passes,
            },
            "hopping_hermiticity": {
                "representative_modulus": (
                    record.hopping_hermiticity.representative_modulus
                ),
                "paired_representatives": list(
                    record.hopping_hermiticity.paired_representatives
                ),
                "missing_opposite_representatives": list(
                    record.hopping_hermiticity.missing_opposite_representatives
                ),
                "maximum_frobenius_defect": self._quantity(
                    record.hopping_hermiticity.maximum_frobenius_defect
                ),
                "absolute_tolerance": self._quantity(
                    record.hopping_hermiticity.absolute_tolerance
                ),
                "passes": record.hopping_hermiticity.passes,
            },
            "range_study": [self._range(item) for item in record.range_study],
            "scope": {
                "localization_included": False,
                "external_calculator_execution_included": False,
                "scientific_acceptance_included": False,
            },
        }

    def _range(self, result: Periodic1DIsolatedBandRangeResult) -> dict[str, JsonValue]:
        """Encode one correlated mediated/direct finite-range result."""
        truncated = result.truncation.truncated
        fitted = result.direct_fit.fitted_model
        route = result.direct_mediated_comparison
        band_shape = result.band_shape
        return {
            "maximum_range": result.maximum_range,
            "retained_representatives": list(truncated.representatives),
            "retained_hopping_blocks": [
                self._complex_matrix(block.magnitude.tolist(), block.unit.expression)
                for block in truncated.hopping_blocks
            ],
            "omitted_block_l2_norm": self._scalar(
                result.truncation.omitted_block_l2_norm,
                truncated.hopping_blocks[0].unit.expression,
            ),
            "training_maximum_absolute_error": self._quantity(
                result.training_error.maximum_absolute_error
            ),
            "withheld_maximum_absolute_error": self._quantity(
                result.withheld_error.maximum_absolute_error
            ),
            "parseval": {
                "training_squared_frobenius_residual": self._quantity(
                    result.parseval.training_squared_frobenius_residual
                ),
                "expected_squared_frobenius_residual": self._quantity(
                    result.parseval.expected_squared_frobenius_residual
                ),
                "parseval_absolute_residual": self._quantity(
                    result.parseval.parseval_absolute_residual
                ),
                "absolute_tolerance": self._quantity(
                    result.parseval.absolute_tolerance
                ),
                "passes": result.parseval.passes,
            },
            "direct_fit": {
                "representatives": list(fitted.representatives),
                "hopping_blocks": [
                    self._complex_matrix(
                        block.magnitude.tolist(), block.unit.expression
                    )
                    for block in fitted.hopping_blocks
                ],
                "design_rank": result.direct_fit.design_rank,
                "design_condition_number": (result.direct_fit.design_condition_number),
                "is_identified": result.direct_fit.is_identified,
                "training_l2_frobenius_residual": self._scalar(
                    result.direct_fit.training_l2_frobenius_residual,
                    fitted.hopping_blocks[0].unit.expression,
                ),
                "training_maximum_frobenius_residual": self._scalar(
                    result.direct_fit.training_maximum_frobenius_residual,
                    fitted.hopping_blocks[0].unit.expression,
                ),
            },
            "direct_mediated_comparison": {
                "coefficient_l2_frobenius_defect": self._quantity(
                    route.coefficient_l2_frobenius_defect
                ),
                "sampled_l2_frobenius_defect": self._quantity(
                    route.sampled_l2_frobenius_defect
                ),
                "sampled_maximum_frobenius_defect": self._quantity(
                    route.sampled_maximum_frobenius_defect
                ),
            },
            "band_shape": {
                "bandwidth": self._quantity(band_shape.bandwidth),
                "zone_center_curvature": self._quantity(
                    band_shape.zone_center_curvature
                ),
                "maximum_imaginary_residual": self._quantity(
                    band_shape.maximum_imaginary_residual
                ),
                "imaginary_absolute_tolerance": self._quantity(
                    band_shape.imaginary_absolute_tolerance
                ),
                "passes": band_shape.passes,
            },
        }

    @staticmethod
    def _spectrum(
        spectrum: BandSpectrumSamples1D,
    ) -> dict[str, JsonValue]:
        """Encode coordinates, reciprocal period, eigenvalues, and their units."""
        if type(spectrum) is not BandSpectrumSamples1D:
            raise TypeError("spectrum must be BandSpectrumSamples1D")
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
        """Encode one validated scalar quantity with its unit expression."""
        if type(quantity) is not ScalarQuantity:
            raise TypeError("quantity must be ScalarQuantity")
        return {
            "magnitude": quantity.magnitude,
            "unit": quantity.unit.expression,
        }

    @staticmethod
    def _scalar(magnitude: float, unit: str) -> dict[str, JsonValue]:
        """Encode a scalar and explicit wire-unit expression."""
        return {"magnitude": magnitude, "unit": unit}

    @staticmethod
    def _vector(magnitude: list[float], unit: str) -> dict[str, JsonValue]:
        """Encode a real vector and explicit wire-unit expression."""
        json_magnitude: list[JsonValue] = list(magnitude)
        return {"magnitude": json_magnitude, "unit": unit}

    @staticmethod
    def _complex_matrix(
        magnitude: list[list[complex]], unit: str
    ) -> dict[str, JsonValue]:
        """Encode a complex matrix as ordered ``[real, imaginary]`` pairs."""
        return {
            "magnitude": [
                [[float(value.real), float(value.imag)] for value in row]
                for row in magnitude
            ],
            "unit": unit,
        }


__all__ = ["Periodic1DIsolatedBandResultJsonSerializer", "SCHEMA_ID"]
