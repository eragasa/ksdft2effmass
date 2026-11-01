"""Producer-independent Fourier reference analysis for all gauge controls.

This module deliberately reconstructs every represented field and recomputes direct
finite Fourier sums with NumPy.  It does not invoke the maintained model, Procrustes,
Fourier, interpolation, locality, or diagnostic actions.  This bounded slice is not
complete protocol verification.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import final

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.gauge_case_result import (
    Periodic1DRankNGaugeAlignmentMeshResult,
)
from ksdft2effmass.periodic1d.rankN.diagnostics.matrix import (
    Periodic1DRankNMatrixErrorResult,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentStatus,
)
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ..calculation_result import Periodic1DRankNAlignmentCalculationResult
from .analytic_reference import (
    _Periodic1DRankNAnalyticReferenceModel,
    _reduced_coordinates,
)

_REFERENCE_SCALAR_ABSOLUTE_TOLERANCE = 1.0e-11
_REFERENCE_ARRAY_ABSOLUTE_TOLERANCE = 1.0e-10
_REFERENCE_DIRECT_SUM_CHUNK_SIZE = 256
_EXACT_ORACLE_SUPPORT = 2
_ERROR_FIELDS = (
    "matrix_frobenius_maximum",
    "matrix_frobenius_rms",
    "normalized_matrix_frobenius_maximum",
    "normalized_matrix_frobenius_rms",
    "ordered_spectrum_maximum",
    "ordered_spectrum_l2_rms",
    "normalized_ordered_spectrum_maximum",
    "normalized_ordered_spectrum_l2_rms",
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNFourierReferenceRequest:
    """Bind one exact producer result to the bounded Fourier reference action."""

    calculation_result: Periodic1DRankNAlignmentCalculationResult

    def __post_init__(self) -> None:
        if (
            type(self.calculation_result)
            is not Periodic1DRankNAlignmentCalculationResult
        ):
            raise TypeError("calculation_result must be the exact calculation result")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNFourierReference:
    """Store immutable direct-sum comparisons for all four gauge controls."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not isinstance(self.comparisons, Mapping) or not self.comparisons:
            raise TypeError("comparisons must be a nonempty mapping")
        if any(
            type(key) is not str
            or not key
            or type(value) is not MaximumAbsoluteErrorComparison
            for key, value in self.comparisons.items()
        ):
            raise TypeError("comparison inventory contains an invalid entry")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@final
class Periodic1DRankNFourierReferenceAnalyzer:
    """Recompute direct Fourier controls without producer analysis actions."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRankNFourierReferenceRequest) -> None:
        if type(request) is not Periodic1DRankNFourierReferenceRequest:
            raise TypeError("request must be the exact Fourier reference request")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNFourierReferenceRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNFourierReference:
        """Return bounded direct-sum Fourier comparisons."""
        request = self._request
        calculation = request.calculation_result
        calculation_request = calculation.request
        controls = calculation_request.controls
        rank = calculation_request.retained_rank
        depth = calculation_request.circuit_depth
        reference_model = _Periodic1DRankNAnalyticReferenceModel(rank, depth)
        energy_reference = controls.energy_reference
        matrix_scale = math.sqrt(rank) * energy_reference
        exact_offsets, exact_first, exact_second = reference_model.energy_parameters()
        selection_size = (
            calculation_request.configuration.global_unitary_selection_mesh_size
        )
        selection_coordinates = _reduced_coordinates(selection_size)
        selection_gauge = reference_model.gauge_unitaries(selection_coordinates)
        selection_cross = np.mean(
            np.swapaxes(selection_gauge.conjugate(), -1, -2),
            axis=0,
        )
        global_right = _right_polar_factor(selection_cross)
        global_right_adjoint = global_right.conjugate().T
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}

        for mesh in calculation.meshes:
            size = mesh.construction_mesh_size
            coordinates = _reduced_coordinates(size)
            exact_field = reference_model.exact_field(coordinates)
            gauge = reference_model.gauge_unitaries(coordinates)
            gauge_adjoint = np.swapaxes(gauge.conjugate(), -1, -2)
            identity_field = np.asarray(
                gauge_adjoint @ exact_field @ gauge,
                dtype=np.complex128,
            )
            global_field = np.asarray(
                global_right_adjoint @ identity_field @ global_right,
                dtype=np.complex128,
            )
            observed_by_gauge = {
                result.status.gauge_alignment: result
                for result in mesh.gauge_alignment_results
            }
            for gauge_alignment, field in (
                (Periodic1DRankNGaugeAlignment.IDENTITY, identity_field),
                (Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY, global_field),
                (Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY, exact_field),
                (
                    Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
                    exact_field,
                ),
            ):
                observed = observed_by_gauge[gauge_alignment]
                if (
                    observed.status.status
                    is not Periodic1DRankNAlignmentStatus.QUALIFIED
                ):
                    raise ValueError(
                        "bounded Fourier reference requires qualified control results"
                    )
                gauge_wire = gauge_alignment.to_wire()
                prefix = f"mesh[{size}].{gauge_wire}"
                modes, coefficients = _direct_fourier_transform(coordinates, field)
                reconstruction = _direct_fourier_evaluation(
                    modes,
                    coefficients,
                    coordinates,
                )
                _add_block_inventory_comparisons(
                    comparisons,
                    prefix,
                    modes,
                    coefficients,
                    observed.coefficient_translations,
                    observed.block_raw_frobenius_norms,
                    observed.block_normalized_frobenius_norms,
                    matrix_scale,
                    _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
                )
                _add_error_comparisons(
                    comparisons,
                    f"{prefix}.reconstruction",
                    _matrix_error_values(
                        reconstruction,
                        field,
                        energy_reference,
                    ),
                    observed.reconstruction,
                    _REFERENCE_SCALAR_ABSOLUTE_TOLERANCE,
                )
                sample_energy = float(
                    np.mean(np.linalg.norm(field, axis=(-2, -1)) ** 2)
                )
                coefficient_energy = float(
                    np.sum(np.linalg.norm(coefficients, axis=(-2, -1)) ** 2)
                )
                parseval_defect = abs(sample_energy - coefficient_energy) / max(
                    sample_energy,
                    controls.saturation_denominator_floor,
                )
                hermiticity_defect = float(
                    np.max(
                        np.linalg.norm(
                            coefficients[::-1]
                            - np.swapaxes(coefficients.conjugate(), -1, -2),
                            axis=(-2, -1),
                        )
                    )
                    / matrix_scale
                )
                for name, calculated, observed_value in (
                    (
                        "parseval_relative_defect",
                        parseval_defect,
                        observed.parseval_relative_defect,
                    ),
                    (
                        "ordinary_hermiticity_defect",
                        hermiticity_defect,
                        observed.ordinary_hermiticity_defect,
                    ),
                    (
                        "twisted_cyclic_hermiticity_defect",
                        hermiticity_defect,
                        observed.twisted_cyclic_hermiticity_defect,
                    ),
                ):
                    if observed_value is None:
                        raise ValueError(f"qualified result is missing {name}")
                    comparisons[f"{prefix}.{name}"] = _comparison(
                        ScalarQuantity(calculated, Unitless()),
                        ScalarQuantity(observed_value, Unitless()),
                        absolute_tolerance=_REFERENCE_SCALAR_ABSOLUTE_TOLERANCE,
                    )

                _add_interpolation_and_tail_comparisons(
                    comparisons,
                    prefix,
                    modes,
                    coefficients,
                    observed,
                    gauge_alignment,
                    depth,
                    calculation_request.configuration.evaluation_mesh_size,
                    calculation_request.configuration.evaluation_shift_numerator,
                    calculation_request.configuration.evaluation_shift_denominator,
                    energy_reference,
                    global_right,
                    _REFERENCE_SCALAR_ABSOLUTE_TOLERANCE,
                )
                if (
                    gauge_alignment
                    is Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE
                ):
                    _add_oracle_exact_support_comparisons(
                        comparisons,
                        prefix,
                        modes,
                        coefficients,
                        exact_offsets,
                        exact_first,
                        exact_second,
                        _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
                    )

        return Periodic1DRankNFourierReference(MappingProxyType(comparisons))


def _right_polar_factor(cross: np.ndarray) -> np.ndarray:
    gram = cross.conjugate().T @ cross
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    if bool((eigenvalues <= 0.0).any()):
        raise ValueError(
            "bounded Fourier reference requires positive global cross Gram"
        )
    inverse_square_root = (
        eigenvectors * (1.0 / np.sqrt(eigenvalues))[None, :]
    ) @ eigenvectors.conjugate().T
    return np.asarray(cross @ inverse_square_root, dtype=np.complex128)


def _comparison(
    observed: ScalarQuantity | VectorQuantity | ComplexMatrixQuantity,
    reference: ScalarQuantity | VectorQuantity | ComplexMatrixQuantity,
    *,
    absolute_tolerance: float,
) -> MaximumAbsoluteErrorComparison:
    return MaximumAbsoluteErrorComparison(
        observed=observed,
        reference=reference,
        tolerance=ScalarQuantity(absolute_tolerance, observed.unit),
    )


def _direct_fourier_transform(
    coordinates: np.ndarray,
    field: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    size = coordinates.size
    modes = np.arange(-(size // 2), size // 2 + 1, dtype=np.int64)
    flattened = field.reshape((size, -1))
    coefficient_chunks: list[np.ndarray] = []
    for start in range(0, size, _REFERENCE_DIRECT_SUM_CHUNK_SIZE):
        selected = modes[start : start + _REFERENCE_DIRECT_SUM_CHUNK_SIZE]
        phase = np.exp(-2.0j * np.pi * coordinates[:, None] * selected[None, :])
        coefficient_chunks.append((phase.T @ flattened) / size)
    coefficients = np.concatenate(coefficient_chunks, axis=0).reshape(field.shape)
    return modes, np.asarray(coefficients, dtype=np.complex128)


def _direct_fourier_evaluation(
    modes: np.ndarray,
    coefficients: np.ndarray,
    coordinates: np.ndarray,
) -> np.ndarray:
    flattened = coefficients.reshape((modes.size, -1))
    value_chunks: list[np.ndarray] = []
    for start in range(0, coordinates.size, _REFERENCE_DIRECT_SUM_CHUNK_SIZE):
        selected = coordinates[start : start + _REFERENCE_DIRECT_SUM_CHUNK_SIZE]
        phase = np.exp(2.0j * np.pi * selected[:, None] * modes[None, :])
        value_chunks.append(phase @ flattened)
    return np.asarray(
        np.concatenate(value_chunks, axis=0).reshape(
            (coordinates.size, coefficients.shape[-2], coefficients.shape[-1])
        ),
        dtype=np.complex128,
    )


def _matrix_error_values(
    approximation: np.ndarray,
    reference: np.ndarray,
    energy_reference: float,
) -> dict[str, float]:
    rank = int(approximation.shape[-1])
    difference = approximation - reference
    frobenius = np.linalg.norm(difference, axis=(-2, -1))
    band_difference = np.abs(
        np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(reference)
    )
    band_l2 = np.linalg.norm(band_difference, axis=-1)
    matrix_scale = math.sqrt(rank) * energy_reference
    matrix_maximum = float(np.max(frobenius))
    matrix_rms = float(np.sqrt(np.mean(frobenius**2)))
    spectrum_maximum = float(np.max(band_difference))
    spectrum_l2_rms = float(np.sqrt(np.mean(band_l2**2)))
    return {
        "matrix_frobenius_maximum": matrix_maximum,
        "matrix_frobenius_rms": matrix_rms,
        "normalized_matrix_frobenius_maximum": matrix_maximum / matrix_scale,
        "normalized_matrix_frobenius_rms": matrix_rms / matrix_scale,
        "ordered_spectrum_maximum": spectrum_maximum,
        "ordered_spectrum_l2_rms": spectrum_l2_rms,
        "normalized_ordered_spectrum_maximum": spectrum_maximum / energy_reference,
        "normalized_ordered_spectrum_l2_rms": spectrum_l2_rms / matrix_scale,
    }


def _add_block_inventory_comparisons(
    comparisons: dict[str, MaximumAbsoluteErrorComparison],
    prefix: str,
    modes: np.ndarray,
    coefficients: np.ndarray,
    observed_translations: np.ndarray,
    observed_raw: np.ndarray,
    observed_normalized: np.ndarray,
    matrix_scale: float,
    tolerance: float,
) -> None:
    mask = np.abs(modes) <= int(np.max(np.abs(observed_translations)))
    translations = modes[mask]
    raw = np.asarray(
        np.linalg.norm(coefficients[mask], axis=(-2, -1)),
        dtype=np.float64,
    )
    comparisons[f"{prefix}.coefficient_translations"] = _comparison(
        VectorQuantity(np.asarray(translations, dtype=np.float64), Unitless()),
        VectorQuantity(np.asarray(observed_translations, dtype=np.float64), Unitless()),
        absolute_tolerance=0.0,
    )
    comparisons[f"{prefix}.block_raw_frobenius_norms"] = _comparison(
        VectorQuantity(raw, Unitless()),
        VectorQuantity(observed_raw, Unitless()),
        absolute_tolerance=tolerance,
    )
    comparisons[f"{prefix}.block_normalized_frobenius_norms"] = _comparison(
        VectorQuantity(raw / matrix_scale, Unitless()),
        VectorQuantity(observed_normalized, Unitless()),
        absolute_tolerance=tolerance,
    )


def _add_error_comparisons(
    comparisons: dict[str, MaximumAbsoluteErrorComparison],
    prefix: str,
    calculated: Mapping[str, float],
    observed: Periodic1DRankNMatrixErrorResult | None,
    tolerance: float,
) -> None:
    if observed is None:
        raise ValueError(f"qualified result is missing {prefix}")
    observed_values = {
        "matrix_frobenius_maximum": observed.matrix_frobenius_maximum,
        "matrix_frobenius_rms": observed.matrix_frobenius_rms,
        "normalized_matrix_frobenius_maximum": (
            observed.normalized_matrix_frobenius_maximum
        ),
        "normalized_matrix_frobenius_rms": (observed.normalized_matrix_frobenius_rms),
        "ordered_spectrum_maximum": observed.ordered_spectrum_maximum,
        "ordered_spectrum_l2_rms": observed.ordered_spectrum_l2_rms,
        "normalized_ordered_spectrum_maximum": (
            observed.normalized_ordered_spectrum_maximum
        ),
        "normalized_ordered_spectrum_l2_rms": (
            observed.normalized_ordered_spectrum_l2_rms
        ),
    }
    for field_name in _ERROR_FIELDS:
        comparisons[f"{prefix}.{field_name}"] = _comparison(
            ScalarQuantity(calculated[field_name], Unitless()),
            ScalarQuantity(observed_values[field_name], Unitless()),
            absolute_tolerance=tolerance,
        )


def _add_interpolation_and_tail_comparisons(
    comparisons: dict[str, MaximumAbsoluteErrorComparison],
    prefix: str,
    modes: np.ndarray,
    coefficients: np.ndarray,
    observed: Periodic1DRankNGaugeAlignmentMeshResult,
    gauge_alignment: Periodic1DRankNGaugeAlignment,
    depth: int,
    evaluation_size: int,
    shift_numerator: int,
    shift_denominator: int,
    energy_reference: float,
    global_right: np.ndarray,
    scalar_tolerance: float,
) -> None:
    rank = observed.status.retained_rank
    reference_model = _Periodic1DRankNAnalyticReferenceModel(rank, depth)
    evaluation_coordinates = np.asarray(
        -0.5
        + (
            np.arange(evaluation_size, dtype=np.float64)
            + shift_numerator / shift_denominator
        )
        / evaluation_size,
        dtype=np.float64,
    )
    interpolated = _direct_fourier_evaluation(
        modes,
        coefficients,
        evaluation_coordinates,
    )
    exact = reference_model.exact_field(evaluation_coordinates)
    if gauge_alignment in (
        Periodic1DRankNGaugeAlignment.IDENTITY,
        Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
    ):
        gauge = reference_model.gauge_unitaries(evaluation_coordinates)
        attacked = np.asarray(
            np.swapaxes(gauge.conjugate(), -1, -2) @ exact @ gauge,
            dtype=np.complex128,
        )
        if gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY:
            direct = np.asarray(
                global_right.conjugate().T @ attacked @ global_right,
                dtype=np.complex128,
            )
        else:
            direct = attacked
    else:
        direct = exact
    interpolation = observed.interpolation
    if interpolation is None:
        raise ValueError("qualified control result is missing interpolation evidence")
    _add_error_comparisons(
        comparisons,
        f"{prefix}.interpolation",
        _matrix_error_values(interpolated, direct, energy_reference),
        interpolation.errors,
        scalar_tolerance,
    )

    matrix_scale = math.sqrt(rank) * energy_reference
    squared_scale = rank * energy_reference**2
    for support in observed.supports:
        omitted = coefficients[np.abs(modes) > support.maximum_range]
        block_norms = np.linalg.norm(omitted, axis=(-2, -1))
        weight = float(np.sum(block_norms**2))
        l2_norm = math.sqrt(weight)
        l1_norm = float(np.sum(block_norms))
        values = (
            (
                "omitted_squared_frobenius_weight",
                weight,
                support.omitted_squared_frobenius_weight,
            ),
            (
                "normalized_omitted_squared_frobenius_weight",
                weight / squared_scale,
                support.normalized_omitted_squared_frobenius_weight,
            ),
            (
                "omitted_frobenius_l2_norm",
                l2_norm,
                support.omitted_frobenius_l2_norm,
            ),
            (
                "normalized_omitted_frobenius_l2_norm",
                l2_norm / matrix_scale,
                support.normalized_omitted_frobenius_l2_norm,
            ),
            ("omitted_block_l1_norm", l1_norm, support.omitted_block_l1_norm),
            (
                "normalized_omitted_block_l1_norm",
                l1_norm / matrix_scale,
                support.normalized_omitted_block_l1_norm,
            ),
        )
        for field_name, calculated, observed_value in values:
            comparisons[f"{prefix}.support[{support.maximum_range}].{field_name}"] = (
                _comparison(
                    ScalarQuantity(calculated, Unitless()),
                    ScalarQuantity(observed_value, Unitless()),
                    absolute_tolerance=scalar_tolerance,
                )
            )


def _add_oracle_exact_support_comparisons(
    comparisons: dict[str, MaximumAbsoluteErrorComparison],
    prefix: str,
    modes: np.ndarray,
    coefficients: np.ndarray,
    offsets: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    array_tolerance: float,
) -> None:
    expected_by_mode = {
        -2: np.diag(second / 2.0).astype(np.complex128),
        -1: np.diag(first / 2.0).astype(np.complex128),
        0: np.diag(offsets).astype(np.complex128),
        1: np.diag(first / 2.0).astype(np.complex128),
        2: np.diag(second / 2.0).astype(np.complex128),
    }
    lookup = {
        int(mode): coefficient
        for mode, coefficient in zip(modes, coefficients, strict=True)
    }
    for mode, expected in expected_by_mode.items():
        comparisons[f"{prefix}.exact_coefficient[{mode}]"] = _comparison(
            ComplexMatrixQuantity(lookup[mode], Unitless()),
            ComplexMatrixQuantity(expected, Unitless()),
            absolute_tolerance=array_tolerance,
        )
    outside = np.abs(modes) > _EXACT_ORACLE_SUPPORT
    outside_maximum = float(
        np.max(np.linalg.norm(coefficients[outside], axis=(-2, -1)))
    )
    comparisons[f"{prefix}.maximum_outside_exact_support_norm"] = _comparison(
        ScalarQuantity(outside_maximum, Unitless()),
        ScalarQuantity(0.0, Unitless()),
        absolute_tolerance=array_tolerance,
    )


__all__ = [
    "Periodic1DRankNFourierReference",
    "Periodic1DRankNFourierReferenceAnalyzer",
    "Periodic1DRankNFourierReferenceRequest",
]
