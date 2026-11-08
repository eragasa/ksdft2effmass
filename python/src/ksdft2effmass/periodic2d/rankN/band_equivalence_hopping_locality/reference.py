"""Bounded independent periodic-2D rank-N parent, alignment, and transport references.

The reference reconstructs the selected analytic formulas directly from the typed study
request. It does not call the maintained analytic model, aggregate analyzer, Procrustes
solver, gauge-alignment actions, or transport owner. Independent direct-sum Fourier,
shell-power, and support-selection comparisons live in ``fourier_reference``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import final

from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.band_equivalence_hopping_locality.rankN.reference import (
    _ExpectedAlignment,
    _IndependentPeriodicRankNCase,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGaugeNormalizationEnum,
)
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

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
class Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest
):
    """Bind one exact analyzed case to its complete typed study definition."""

    study_request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest
    case_analysis: Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis

    @property
    def band_subspace_rank(self) -> int:
        """Return the bound case's represented band-subspace rank."""
        return self.case_analysis.retained_rank

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
            or case.transformation_coefficient
            not in self.study_request.transformation_coefficients
        ):
            raise ValueError("case_analysis must identify one exact request expansion")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNBandEquivalenceHoppingLocalityReference(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue
):
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
    def band_subspace_rank(self) -> int:
        """Return the independently assessed band-subspace rank."""
        return self.request.band_subspace_rank

    @property
    def passed(self) -> bool:
        """Return whether every bounded independent comparison passed."""
        return all(
            comparison.result().passed for comparison in self.comparisons.values()
        )


@final
class _IndependentPeriodic2DRankNCase(_IndependentPeriodicRankNCase):
    """Bind the independent common formulas to periodic-2D identities."""

    __slots__ = ()

    def __init__(
        self,
        *,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
        retained_rank: int,
        circuit_depth: int,
        parent_scale: float,
        transformation_coefficient: float,
    ) -> None:
        super().__init__(
            spatial_dimension=2,
            positive_bonds=geometry.positive_bonds,
            axis_maximum_normalization=(
                geometry.gauge_normalization
                is Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            ),
            retained_rank=retained_rank,
            circuit_depth=circuit_depth,
            parent_scale=parent_scale,
            transformation_coefficient=transformation_coefficient,
        )

    def dimension_alignments(
        self,
        construction_coordinates: Float64Array,
        evaluation_coordinates: Float64Array,
    ) -> Mapping[Periodic2DRankNGaugeAlignment, _ExpectedAlignment]:
        expected = super().alignments(
            construction_coordinates,
            evaluation_coordinates,
        )
        return MappingProxyType(
            {
                Periodic2DRankNGaugeAlignment.IDENTITY: expected.identity,
                Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY: expected.global_unitary,
                Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY: (
                    expected.pointwise_unitary
                ),
                Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                    expected.known_inverse_oracle
                ),
            }
        )


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction
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

    @property
    def band_subspace_rank(self) -> int:
        """Return the independently assessed band-subspace rank."""
        return self.request.band_subspace_rank

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
            transformation_coefficient=observed_case.transformation_coefficient,
        )
        construction = independent.coordinates(study.construction_size, 0.5)
        evaluation = independent.coordinates(
            study.evaluation_size,
            0.5 + study.evaluation_shift,
        )
        expected_alignments = independent.dimension_alignments(
            construction,
            evaluation,
        )
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
