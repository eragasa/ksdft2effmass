"""Bounded independent periodic-2D rank-N parent, alignment, and transport references.

The reference reconstructs the selected analytic formulas directly from the typed study
request. It does not call the maintained analytic model, aggregate analyzer, Procrustes
solver, gauge-alignment actions, or transport owner. Independent direct-sum Fourier,
shell-power, and support-selection comparisons live in ``fourier_reference``.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import final

import numpy as np
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.periodic2d.base import Periodic2DCapability
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .model import Periodic2DRankNGaugeNormalizationEnum
from .request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from .result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    Periodic2DRankNFittedAlignmentEvidence,
)

_REFERENCE_ABSOLUTE_TOLERANCE = 1.0e-10


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest:
    """Bind one exact analyzed case to its complete typed study definition."""

    study_request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest
    case_analysis: Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis

    def __post_init__(self) -> None:
        if (
            type(self.study_request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError("study_request must be the exact periodic-2D request")
        if (
            type(self.case_analysis)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis
        ):
            raise TypeError("case_analysis must be the exact periodic-2D case analysis")
        case = self.case_analysis
        if (
            case.case_identifier
            not in tuple(item.identifier for item in self.study_request.cases)
            or case.retained_rank not in self.study_request.retained_ranks
            or case.circuit_depth not in self.study_request.circuit_depths
            or case.parent_scale not in self.study_request.parent_scales
            or case.attack_coefficient not in self.study_request.attack_coefficients
        ):
            raise ValueError("case_analysis must identify one exact request expansion")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNBandEquivalenceHoppingLocalityReference:
    """Retain immutable producer-independent scalar comparisons."""

    request: Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest
    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest
        ):
            raise TypeError("request must be the exact periodic-2D reference request")
        if not isinstance(self.comparisons, Mapping) or not self.comparisons:
            raise TypeError("comparisons must be a nonempty mapping")
        if any(
            type(key) is not str
            or not key
            or type(value) is not MaximumAbsoluteErrorComparison
            for key, value in self.comparisons.items()
        ):
            raise TypeError("comparisons contain an invalid entry")
        object.__setattr__(
            self, "comparisons", MappingProxyType(dict(self.comparisons))
        )

    @property
    def passed(self) -> bool:
        """Return whether every bounded independent comparison passed."""
        return all(
            comparison.result().passed for comparison in self.comparisons.values()
        )


@dataclass(frozen=True, slots=True)
class _ExpectedFittedEvidence:
    sample_count: int
    minimum_numerical_rank: int
    minimum_cross_singular_value: float
    maximum_optimal_residual_frobenius_norm: float
    maximum_applied_rank_cutoff: float


@dataclass(frozen=True, slots=True)
class _ExpectedAlignment:
    maximum_aligned_frame_defect: float
    maximum_direct_matrix_difference: float
    fitted_evidence: _ExpectedFittedEvidence | None


@final
class _IndependentPeriodic2DRankNCase:
    """Evaluate the selected formulas without invoking the maintained model owner."""

    __slots__ = (
        "_attack_coefficient",
        "_circuit_depth",
        "_geometry",
        "_parent_scale",
        "_rank",
    )

    def __init__(
        self,
        *,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        retained_rank: int,
        circuit_depth: int,
        parent_scale: float,
        attack_coefficient: float,
    ) -> None:
        self._geometry = geometry
        self._rank = retained_rank
        self._circuit_depth = circuit_depth
        self._parent_scale = parent_scale
        self._attack_coefficient = attack_coefficient

    @staticmethod
    def coordinates(size: int, offset: float) -> np.ndarray:
        axis = -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    def _orbital_coordinates(self) -> np.ndarray:
        orbital = np.arange(self._rank, dtype=np.float64)
        return np.asarray(
            (2.0 * orbital - self._rank + 1.0) / (self._rank - 1.0),
            dtype=np.float64,
        )

    def _arguments(self, coordinates: np.ndarray) -> np.ndarray:
        bonds = np.asarray(self._geometry.positive_bonds, dtype=np.float64)
        return np.asarray(
            2.0 * np.pi * np.einsum("...d,bd->...b", coordinates, bonds),
            dtype=np.float64,
        )

    def structure_factor(self, coordinates: np.ndarray) -> np.ndarray:
        arguments = self._arguments(coordinates)
        return np.asarray(
            np.mean(
                0.75 * np.cos(arguments) + 0.25 * np.cos(2.0 * arguments),
                axis=-1,
            ),
            dtype=np.float64,
        )

    def retained_energies(self, coordinates: np.ndarray) -> np.ndarray:
        orbital = self._orbital_coordinates()
        structure = self.structure_factor(coordinates)
        return np.asarray(
            0.4 * orbital
            + 0.25 * self._parent_scale * (1.0 + 0.2 * orbital) * structure[..., None],
            dtype=np.float64,
        )

    def exterior_energies(self, coordinates: np.ndarray) -> np.ndarray:
        orbital = self._orbital_coordinates()
        structure = self.structure_factor(coordinates)
        return np.asarray(
            3.0 + 0.3 * orbital + 0.1 * self._parent_scale * structure[..., None],
            dtype=np.float64,
        )

    def exact_operators(self, coordinates: np.ndarray) -> np.ndarray:
        energies = self.retained_energies(coordinates)
        return np.asarray(
            energies[..., :, None] * np.eye(self._rank, dtype=np.complex128),
            dtype=np.complex128,
        )

    def gauges(self, coordinates: np.ndarray) -> np.ndarray:
        arguments = self._arguments(coordinates)
        identity = np.eye(self._rank, dtype=np.complex128)
        gauges = np.broadcast_to(
            identity,
            (*coordinates.shape[:-1], self._rank, self._rank),
        ).copy()
        normalization = (
            0.5
            if self._geometry.gauge_normalization
            is Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            else math.sqrt(2.0 / float(len(self._geometry.positive_bonds)))
        )
        for layer_index in range(1, self._circuit_depth + 1):
            harmonic = 0.75 * np.sin(arguments) + 0.25 * (
                (-1.0) ** layer_index
            ) * np.sin(2.0 * arguments)
            scalar = normalization * np.sum(harmonic, axis=-1)
            layer = np.broadcast_to(
                identity,
                (*coordinates.shape[:-1], self._rank, self._rank),
            ).copy()
            first_left = 0 if layer_index % 2 == 1 else 1
            for left in range(first_left, self._rank - 1, 2):
                pair_index = left + 1
                pair_coordinate = (2.0 * pair_index - self._rank) / (self._rank - 1.0)
                weight = (1.0 + 0.15 * pair_coordinate) / 1.15
                angle = (
                    self._attack_coefficient
                    * (-1.0) ** (layer_index + pair_index)
                    * weight
                    * scalar
                )
                cosine = np.cos(angle)
                sine = np.sin(angle)
                layer[..., left, left] = cosine
                layer[..., left, left + 1] = -sine
                layer[..., left + 1, left] = sine
                layer[..., left + 1, left + 1] = cosine
            gauges = gauges @ layer
        return np.asarray(gauges, dtype=np.complex128)

    def minimum_gap(self, construction_coordinates: np.ndarray) -> float:
        retained = self.retained_energies(construction_coordinates)
        exterior = self.exterior_energies(construction_coordinates)
        return float(np.min(exterior[..., 0] - retained[..., -1]))

    @staticmethod
    def _right_polar_factor(cross: np.ndarray) -> np.ndarray:
        gram = cross.conjugate().T @ cross
        eigenvalues, eigenvectors = np.linalg.eigh(gram)
        if bool((eigenvalues <= 0.0).any()):
            raise ValueError("bounded reference requires a positive cross Gram matrix")
        inverse_square_root = (
            eigenvectors * (1.0 / np.sqrt(eigenvalues))[None, :]
        ) @ eigenvectors.conjugate().T
        return np.asarray(cross @ inverse_square_root, dtype=np.complex128)

    @staticmethod
    def _maximum_frobenius(left: np.ndarray, right: np.ndarray) -> float:
        return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))

    def _cutoff(self, largest_singular_value: float) -> float:
        return max(1.0e-12, 1.0e-10 * largest_singular_value)

    def alignments(
        self,
        construction_coordinates: np.ndarray,
        evaluation_coordinates: np.ndarray,
    ) -> Mapping[Periodic2DRankNGaugeAlignment, _ExpectedAlignment]:
        rank = self._rank
        identity = np.eye(rank, dtype=np.complex128)
        construction_gauge = self.gauges(construction_coordinates)
        evaluation_gauge = self.gauges(evaluation_coordinates)
        exact_evaluation = self.exact_operators(evaluation_coordinates)
        attacked_evaluation = np.asarray(
            np.swapaxes(evaluation_gauge.conjugate(), -1, -2)
            @ exact_evaluation
            @ evaluation_gauge,
            dtype=np.complex128,
        )

        global_cross = np.sum(
            np.swapaxes(construction_gauge.conjugate(), -1, -2),
            axis=tuple(range(construction_gauge.ndim - 2)),
        )
        global_right = self._right_polar_factor(global_cross)
        global_singular_values = np.sqrt(
            np.maximum(
                np.linalg.eigvalsh(global_cross.conjugate().T @ global_cross), 0.0
            )
        )[::-1]
        global_difference = construction_gauge @ global_right - identity
        global_residual = float(np.linalg.norm(global_difference.reshape(-1, rank)))
        global_cutoff = self._cutoff(float(global_singular_values[0]))
        global_evidence = _ExpectedFittedEvidence(
            sample_count=1,
            minimum_numerical_rank=int(
                np.count_nonzero(global_singular_values > global_cutoff)
            ),
            minimum_cross_singular_value=float(global_singular_values[-1]),
            maximum_optimal_residual_frobenius_norm=global_residual,
            maximum_applied_rank_cutoff=global_cutoff,
        )
        pointwise_cutoff = self._cutoff(1.0)
        pointwise_evidence = _ExpectedFittedEvidence(
            sample_count=(
                math.prod(construction_coordinates.shape[:-1])
                + math.prod(evaluation_coordinates.shape[:-1])
            ),
            minimum_numerical_rank=rank,
            minimum_cross_singular_value=1.0,
            maximum_optimal_residual_frobenius_norm=0.0,
            maximum_applied_rank_cutoff=pointwise_cutoff,
        )
        global_evaluation = np.asarray(
            global_right.conjugate().T @ attacked_evaluation @ global_right,
            dtype=np.complex128,
        )
        return MappingProxyType(
            {
                Periodic2DRankNGaugeAlignment.IDENTITY: _ExpectedAlignment(
                    maximum_aligned_frame_defect=self._maximum_frobenius(
                        construction_gauge,
                        identity,
                    ),
                    maximum_direct_matrix_difference=self._maximum_frobenius(
                        attacked_evaluation,
                        exact_evaluation,
                    ),
                    fitted_evidence=None,
                ),
                Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY: _ExpectedAlignment(
                    maximum_aligned_frame_defect=self._maximum_frobenius(
                        construction_gauge @ global_right,
                        identity,
                    ),
                    maximum_direct_matrix_difference=self._maximum_frobenius(
                        global_evaluation,
                        exact_evaluation,
                    ),
                    fitted_evidence=global_evidence,
                ),
                Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY: _ExpectedAlignment(
                    maximum_aligned_frame_defect=0.0,
                    maximum_direct_matrix_difference=0.0,
                    fitted_evidence=pointwise_evidence,
                ),
                Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: _ExpectedAlignment(
                    maximum_aligned_frame_defect=0.0,
                    maximum_direct_matrix_difference=0.0,
                    fitted_evidence=None,
                ),
            }
        )


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer(
    Periodic2DCapability
):
    """Compare one analyzed case with independent parent and alignment formulas."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest,
    ) -> None:
        if (
            type(request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest
        ):
            raise TypeError("request must be the exact periodic-2D reference request")
        self._request = request

    @property
    def request(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest:
        """Return the immutable reference request bound to this action."""
        return self._request

    @staticmethod
    def _comparison(
        observed: float,
        reference: float,
        tolerance: float = _REFERENCE_ABSOLUTE_TOLERANCE,
    ) -> MaximumAbsoluteErrorComparison:
        unit = Unitless()
        return MaximumAbsoluteErrorComparison(
            observed=ScalarQuantity(observed, unit),
            reference=ScalarQuantity(reference, unit),
            tolerance=ScalarQuantity(tolerance, unit),
        )

    def execute(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityReference:
        """Return bounded independent comparisons without retained side effects."""
        request = self._request
        study = request.study_request
        observed_case = request.case_analysis
        geometry = next(
            case
            for case in study.cases
            if case.identifier == observed_case.case_identifier
        )
        independent = _IndependentPeriodic2DRankNCase(
            geometry=geometry,
            retained_rank=observed_case.retained_rank,
            circuit_depth=observed_case.circuit_depth,
            parent_scale=observed_case.parent_scale,
            attack_coefficient=observed_case.attack_coefficient,
        )
        construction = independent.coordinates(study.construction_size, 0.5)
        evaluation = independent.coordinates(
            study.evaluation_size,
            0.5 + study.evaluation_shift,
        )
        expected_alignments = independent.alignments(construction, evaluation)
        observed_alignments = {
            item.alignment: item for item in observed_case.alignments
        }
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {
            "parent.minimum_sampled_external_gap": self._comparison(
                observed_case.minimum_sampled_external_gap,
                independent.minimum_gap(construction),
            )
        }
        for alignment in study.gauge_alignments:
            observed = observed_alignments[alignment]
            if (
                type(observed)
                is not Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis  # noqa: E501
            ):
                raise ValueError(
                    "bounded parent/alignment reference requires qualified routes"
                )
            expected = expected_alignments[alignment]
            prefix = f"alignment[{alignment.to_wire()}]"
            comparisons[f"{prefix}.maximum_aligned_frame_defect"] = self._comparison(
                observed.maximum_aligned_frame_defect,
                expected.maximum_aligned_frame_defect,
            )
            comparisons[f"{prefix}.maximum_direct_matrix_difference"] = (
                self._comparison(
                    observed.maximum_direct_matrix_difference,
                    expected.maximum_direct_matrix_difference,
                )
            )
            comparisons[f"{prefix}.maximum_direct_ordered_spectrum_difference"] = (
                self._comparison(
                    observed.maximum_direct_ordered_spectrum_difference,
                    0.0,
                )
            )
            transport_cutoff = max(
                study.transport_rank_absolute,
                study.transport_rank_relative,
            )
            for name, observed_value, reference_value in (
                (
                    "minimum_transport_singular_value",
                    observed.minimum_transport_singular_value,
                    1.0,
                ),
                (
                    "maximum_transport_procrustes_residual",
                    observed.maximum_transport_procrustes_residual,
                    0.0,
                ),
                (
                    "maximum_transport_unitarity_defect",
                    observed.maximum_transport_unitarity_defect,
                    0.0,
                ),
                (
                    "maximum_transport_rank_cutoff",
                    observed.maximum_transport_rank_cutoff,
                    transport_cutoff,
                ),
                (
                    "maximum_plaquette_phase",
                    observed.maximum_plaquette_phase,
                    0.0,
                ),
            ):
                comparisons[f"{prefix}.{name}"] = self._comparison(
                    observed_value,
                    reference_value,
                )
            for index, phase in enumerate(observed.maximum_absolute_closure_phases):
                comparisons[f"{prefix}.maximum_absolute_closure_phase[{index}]"] = (
                    self._comparison(phase, 0.0)
                )
            expected_evidence = expected.fitted_evidence
            if expected_evidence is None:
                continue
            observed_evidence = observed.alignment_evidence
            if type(observed_evidence) is not Periodic2DRankNFittedAlignmentEvidence:
                raise TypeError("fitted route must retain fitted alignment evidence")
            for name, observed_value, reference_value, tolerance in (
                (
                    "sample_count",
                    float(observed_evidence.sample_count),
                    float(expected_evidence.sample_count),
                    0.0,
                ),
                (
                    "minimum_numerical_rank",
                    float(observed_evidence.minimum_numerical_rank),
                    float(expected_evidence.minimum_numerical_rank),
                    0.0,
                ),
                (
                    "minimum_cross_singular_value",
                    observed_evidence.minimum_cross_singular_value,
                    expected_evidence.minimum_cross_singular_value,
                    _REFERENCE_ABSOLUTE_TOLERANCE,
                ),
                (
                    "maximum_optimal_residual_frobenius_norm",
                    observed_evidence.maximum_optimal_residual_frobenius_norm,
                    expected_evidence.maximum_optimal_residual_frobenius_norm,
                    _REFERENCE_ABSOLUTE_TOLERANCE,
                ),
                (
                    "maximum_applied_rank_cutoff",
                    observed_evidence.maximum_applied_rank_cutoff,
                    expected_evidence.maximum_applied_rank_cutoff,
                    _REFERENCE_ABSOLUTE_TOLERANCE,
                ),
            ):
                comparisons[f"{prefix}.{name}"] = self._comparison(
                    observed_value,
                    reference_value,
                    tolerance,
                )
        return Periodic2DRankNBandEquivalenceHoppingLocalityReference(
            request=request,
            comparisons=comparisons,
        )


__all__ = [
    "Periodic2DRankNBandEquivalenceHoppingLocalityReference",
    "Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer",
    "Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest",
]
