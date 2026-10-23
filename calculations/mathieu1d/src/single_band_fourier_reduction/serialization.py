"""Canonical strict-schema documents for retained experiment evidence."""

from __future__ import annotations

import json

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingRangeReductionResult1D,
)
from ksdft2effmass.linalg import (
    ComplexMatrixQuantity,
    ScalarQuantity,
)

from .definition import (
    EXPERIMENT_IDENTITY,
    INPUT_SCHEMA_ID,
    RESULT_SCHEMA_ID,
    VERIFICATION_SCHEMA_ID,
    SingleBandFourierReductionExperimentDefinition,
)
from .results import SingleBandFourierReductionExperimentResult
from .verify import SingleBandFourierReductionVerificationResult

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def canonical_json_bytes(document: dict[str, JsonValue]) -> bytes:
    """Return sorted compact finite UTF-8 JSON with one terminal newline."""
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


def identity_document() -> dict[str, JsonValue]:
    """Return the immutable version and convention identity mapping."""
    identity = EXPERIMENT_IDENTITY
    return {
        "family_id": identity.family_id,
        "version_id": identity.version_id,
        "energy_reference_id": identity.energy_reference_id,
        "fourier_convention_id": identity.fourier_convention_id,
        "fourier_normalization_id": identity.fourier_normalization_id,
        "objective_construction_role_id": identity.objective_construction_role_id,
        "objective_evaluation_role_id": identity.objective_evaluation_role_id,
    }


class SingleBandFourierReductionInputSerializer:
    """Encode the complete immutable version-one protocol controls."""

    __slots__ = ()

    def serialize(
        self, definition: SingleBandFourierReductionExperimentDefinition
    ) -> bytes:
        """Return canonical input bytes for one exact definition."""
        if type(definition) is not SingleBandFourierReductionExperimentDefinition:
            raise TypeError(
                "definition must be SingleBandFourierReductionExperimentDefinition"
            )
        model = definition.parent_model
        potential = model.potential
        document: dict[str, JsonValue] = {
            "schema": INPUT_SCHEMA_ID,
            "identity": identity_document(),
            "model": {
                "identity": model.identity,
                "model_role": "toy",
                "period": _quantity(potential.period),
                "constant_coefficient": _quantity(potential.constant_coefficient),
                "cosine_coefficients": {
                    "magnitude": potential.cosine_coefficients.magnitude.tolist(),
                    "unit": potential.cosine_coefficients.unit.expression,
                },
                "sine_coefficients": {
                    "magnitude": potential.sine_coefficients.magnitude.tolist(),
                    "unit": potential.sine_coefficients.unit.expression,
                },
                "reciprocal_vector": _quantity(model.reciprocal_vector),
                "recoil_energy": _quantity(model.recoil_energy),
                "duality_absolute_tolerance": model.duality_absolute_tolerance,
            },
            "parent_representation": {
                "plane_wave_cutoffs": list(definition.plane_wave_cutoffs),
                "plane_wave_reference_cutoff": definition.plane_wave_reference_cutoff,
                "production_plane_wave_cutoff": (
                    definition.production_plane_wave_cutoff
                ),
                "finite_difference_points": list(definition.finite_difference_points),
                "sample_reduced_momenta": list(
                    definition.parent_sample_reduced_momenta
                ),
                "compared_band_count": definition.compared_band_count,
            },
            "reduction": {
                "selected_band_index": definition.selected_band_index,
                "training_reduced_momenta": list(definition.training_reduced_momenta),
                "evaluation_reduced_momenta": list(
                    definition.evaluation_reduced_momenta
                ),
                "hopping_ranges": list(definition.hopping_ranges),
                "fitting_weights": list(definition.fitting_weights),
            },
            "tolerances": {
                "coordinate_absolute": _quantity(
                    definition.tolerances.coordinate_absolute
                ),
                "reconstruction_absolute": _quantity(
                    definition.tolerances.reconstruction_absolute
                ),
                "hermiticity_absolute": _quantity(
                    definition.tolerances.hermiticity_absolute
                ),
                "parseval_absolute": _quantity(definition.tolerances.parseval_absolute),
                "imaginary_absolute": _quantity(
                    definition.tolerances.imaginary_absolute
                ),
            },
            "scope": {
                "evidence_class": "controlled-synthetic-numerical-verification",
                "external_calculator_execution": False,
                "scientific_acceptance": False,
                "material_validation": False,
                "uncertainty_quantification": False,
            },
        }
        return canonical_json_bytes(document)


class SingleBandFourierReductionResultSerializer:
    """Encode complete retained outputs without paper-specific identity."""

    __slots__ = ()

    def serialize(self, result: SingleBandFourierReductionExperimentResult) -> bytes:
        """Return canonical result bytes without recomputing any value."""
        if type(result) is not SingleBandFourierReductionExperimentResult:
            raise TypeError("result must be SingleBandFourierReductionExperimentResult")
        reduction = result.reduction
        complete = reduction.complete_transform
        document: dict[str, JsonValue] = {
            "schema": RESULT_SCHEMA_ID,
            "identity": identity_document(),
            "input": json.loads(
                SingleBandFourierReductionInputSerializer()
                .serialize(result.definition)
                .decode("utf-8")
            ),
            "parent_reference": _spectrum(result.parent_reference),
            "plane_wave_refinement": [
                {
                    "cutoff": item.cutoff,
                    "maximum_absolute_error": _quantity(item.maximum_absolute_error),
                }
                for item in result.plane_wave_refinement
            ],
            "finite_difference_refinement": [
                {
                    "point_count": item.point_count,
                    "maximum_absolute_error": _quantity(item.maximum_absolute_error),
                }
                for item in result.finite_difference_refinement
            ],
            "training_gap": {
                "external_minimum_gap": _quantity(
                    _required_gap(result.training_gap.external_minimum_gap)
                ),
                "spectrum": _spectrum(result.training_gap.spectrum),
            },
            "evaluation_gap": {
                "external_minimum_gap": _quantity(
                    _required_gap(result.evaluation_gap.external_minimum_gap)
                ),
                "spectrum": _spectrum(result.evaluation_gap.spectrum),
            },
            "reduction": {
                "training_target": _spectrum(reduction.request.training_target),
                "evaluation_target": _spectrum(reduction.request.evaluation_target),
                "complete_transform": {
                    "representatives": list(complete.hopping_model.representatives),
                    "hopping_blocks": [
                        _complex_matrix(block)
                        for block in complete.hopping_model.hopping_blocks
                    ],
                    "reconstruction_maximum_frobenius_error": _scalar(
                        complete.reconstruction_maximum_frobenius_error,
                        complete.hopping_model.hopping_blocks[0].unit.expression,
                    ),
                    "reconstruction_absolute_tolerance": _scalar(
                        complete.reconstruction_absolute_tolerance,
                        complete.hopping_model.hopping_blocks[0].unit.expression,
                    ),
                    "reconstruction_passes": complete.reconstruction_passes,
                },
                "hopping_hermiticity": {
                    "representative_modulus": (
                        reduction.hopping_hermiticity.representative_modulus
                    ),
                    "paired_representatives": list(
                        reduction.hopping_hermiticity.paired_representatives
                    ),
                    "missing_opposite_representatives": list(
                        reduction.hopping_hermiticity.missing_opposite_representatives
                    ),
                    "maximum_frobenius_defect": _quantity(
                        reduction.hopping_hermiticity.maximum_frobenius_defect
                    ),
                    "absolute_tolerance": _quantity(
                        reduction.hopping_hermiticity.absolute_tolerance
                    ),
                    "passes": reduction.hopping_hermiticity.passes,
                },
                "range_study": [self._range(item) for item in reduction.range_study],
            },
            "interpretation": {
                "sampled_gap_is_not_continuum_isolation_certificate": True,
                "range_selected_as_scientifically_adequate": False,
                "passing_is_bounded_software_numerical_evidence_only": True,
            },
        }
        return canonical_json_bytes(document)

    @staticmethod
    def _range(
        result: SingleBandHoppingRangeReductionResult1D,
    ) -> dict[str, JsonValue]:
        """Encode one already validated range result."""
        if type(result) is not SingleBandHoppingRangeReductionResult1D:
            raise TypeError("result must be SingleBandHoppingRangeReductionResult1D")
        model = result.truncation.truncated
        fit = result.direct_fit
        route = result.route_comparison
        shape = result.band_shape
        return {
            "maximum_range": result.maximum_range,
            "retained_representatives": list(model.representatives),
            "retained_hopping_blocks": [
                _complex_matrix(block) for block in model.hopping_blocks
            ],
            "omitted_block_l2_norm": _scalar(
                result.truncation.omitted_block_l2_norm,
                model.hopping_blocks[0].unit.expression,
            ),
            "training_maximum_absolute_error": _quantity(
                result.training_error.maximum_absolute_error
            ),
            "evaluation_maximum_absolute_error": _quantity(
                result.evaluation_error.maximum_absolute_error
            ),
            "parseval": {
                "training_squared_frobenius_residual": _quantity(
                    result.parseval.training_squared_frobenius_residual
                ),
                "expected_squared_frobenius_residual": _quantity(
                    result.parseval.expected_squared_frobenius_residual
                ),
                "parseval_absolute_residual": _quantity(
                    result.parseval.parseval_absolute_residual
                ),
                "absolute_tolerance": _quantity(result.parseval.absolute_tolerance),
                "passes": result.parseval.passes,
            },
            "direct_fit": {
                "representatives": list(fit.representatives),
                "hopping_blocks": [
                    _complex_matrix(block) for block in fit.fitted_model.hopping_blocks
                ],
                "design_rank": fit.design_rank,
                "design_condition_number": fit.design_condition_number,
                "is_identified": fit.is_identified,
                "training_l2_frobenius_residual": _scalar(
                    fit.training_l2_frobenius_residual,
                    fit.fitted_model.hopping_blocks[0].unit.expression,
                ),
                "training_maximum_frobenius_residual": _scalar(
                    fit.training_maximum_frobenius_residual,
                    fit.fitted_model.hopping_blocks[0].unit.expression,
                ),
            },
            "route_comparison": {
                "coefficient_l2_frobenius_defect": _quantity(
                    route.coefficient_l2_frobenius_defect
                ),
                "sampled_l2_frobenius_defect": _quantity(
                    route.sampled_l2_frobenius_defect
                ),
                "sampled_maximum_frobenius_defect": _quantity(
                    route.sampled_maximum_frobenius_defect
                ),
            },
            "band_shape": {
                "bandwidth": _quantity(shape.bandwidth),
                "zone_center_curvature": _quantity(shape.zone_center_curvature),
                "maximum_imaginary_residual": _quantity(
                    shape.maximum_imaginary_residual
                ),
                "imaginary_absolute_tolerance": _quantity(
                    shape.imaginary_absolute_tolerance
                ),
                "passes": shape.passes,
            },
        }


class SingleBandFourierReductionVerificationSerializer:
    """Encode independent reconstruction defects and bounded disposition."""

    __slots__ = ()

    def serialize(
        self, verification: SingleBandFourierReductionVerificationResult
    ) -> bytes:
        """Return canonical verification bytes."""
        if type(verification) is not SingleBandFourierReductionVerificationResult:
            raise TypeError(
                "verification must be SingleBandFourierReductionVerificationResult"
            )
        return canonical_json_bytes(
            {
                "schema": VERIFICATION_SCHEMA_ID,
                "identity": identity_document(),
                "energy_maximum_absolute_defect": _quantity(
                    verification.energy_maximum_absolute_defect
                ),
                "squared_energy_maximum_absolute_defect": _quantity(
                    verification.squared_energy_maximum_absolute_defect
                ),
                "energy_absolute_tolerance": _quantity(
                    verification.energy_absolute_tolerance
                ),
                "squared_energy_absolute_tolerance": _quantity(
                    verification.squared_energy_absolute_tolerance
                ),
                "structural_checks_pass": verification.structural_checks_pass,
                "passes": verification.passes,
                "claim_boundary": (
                    "Passing establishes bounded finite-protocol numerical and "
                    "software consistency only; it does not establish continuum "
                    "isolation, material validity, scientific acceptance, or "
                    "uncertainty quantification."
                ),
            }
        )


def _required_gap(value: ScalarQuantity | None) -> ScalarQuantity:
    """Narrow an experiment-guaranteed sampled external gap."""
    if value is None:
        raise ValueError("retained experiment requires an external gap")
    return value


def _spectrum(spectrum: BandSpectrumSamples1D) -> dict[str, JsonValue]:
    """Encode one ordered spectrum with explicit coordinate and energy units."""
    if type(spectrum) is not BandSpectrumSamples1D:
        raise TypeError("spectrum must be BandSpectrumSamples1D")
    return {
        "coordinates": {
            "magnitude": spectrum.coordinates.magnitude.tolist(),
            "unit": spectrum.coordinates.unit.expression,
        },
        "reciprocal_period": _quantity(spectrum.reciprocal_period),
        "eigenvalues": {
            "magnitude": spectrum.eigenvalues.magnitude.tolist(),
            "unit": spectrum.eigenvalues.unit.expression,
        },
    }


def _quantity(value: ScalarQuantity) -> dict[str, JsonValue]:
    """Encode a validated scalar quantity."""
    if type(value) is not ScalarQuantity:
        raise TypeError("value must be ScalarQuantity")
    return {"magnitude": value.magnitude, "unit": value.unit.expression}


def _scalar(magnitude: float, unit: str) -> dict[str, JsonValue]:
    """Encode an owner scalar paired with its explicit unit."""
    return {"magnitude": magnitude, "unit": unit}


def _complex_matrix(value: ComplexMatrixQuantity) -> dict[str, JsonValue]:
    """Encode complex values as exact ordered real/imaginary pairs."""
    if type(value) is not ComplexMatrixQuantity:
        raise TypeError("value must be ComplexMatrixQuantity")
    return {
        "magnitude": [
            [[float(item.real), float(item.imag)] for item in row]
            for row in value.magnitude
        ],
        "unit": value.unit.expression,
    }


__all__ = [
    "SingleBandFourierReductionInputSerializer",
    "SingleBandFourierReductionResultSerializer",
    "SingleBandFourierReductionVerificationSerializer",
    "canonical_json_bytes",
    "identity_document",
]
