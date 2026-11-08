"""Independent periodic-3D rank-N Fourier, shell, and support references.

This bounded reference uses explicit dense finite sums and direct metric arithmetic. It
does not call the production Fourier transformer, evaluator, shell classifier,
hopping-locality analyzer, support selector, or aggregate analyzer.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import final

import numpy as np
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.band_equivalence_hopping_locality.rankN.fourier_reference import (
    _DirectFiniteFourierGrid,
    _ErrorValues,
    _ExpectedSupport,
    _PeriodicRankNBandEquivalenceHoppingLocalityFourierReferenceArithmetic,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseRequest,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.definition import (
    Periodic3DRankNGaugeAlignment,
)
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .reference import _IndependentPeriodic3DRankNCase
from .request import Periodic3DRankNBandEquivalenceHoppingLocalityRequest
from .result import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
    Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    Periodic3DRankNSupportSelected,
    Periodic3DRankNSupportSelection,
    Periodic3DRankNSupportUnresolved,
)

_REFERENCE_ABSOLUTE_TOLERANCE = 2.0e-10


@dataclass(frozen=True, slots=True)
class Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest(
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseRequest
):
    """Bind one analyzed case to the typed study geometry and mesh controls."""

    study_request: Periodic3DRankNBandEquivalenceHoppingLocalityRequest
    case_analysis: Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis

    @property
    def band_subspace_rank(self) -> int:
        """Return the bound case's represented band-subspace rank."""
        return self.case_analysis.retained_rank

    def __post_init__(self) -> None:
        if (
            type(self.study_request)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError("study_request must be the exact periodic-3D request")
        if (
            type(self.case_analysis)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalysis
        ):
            raise TypeError("case_analysis must be the exact periodic-3D case analysis")
        case = self.case_analysis
        if (
            case.case_identifier
            not in tuple(
                item.lattice_control.to_wire() for item in self.study_request.cases
            )
            or case.retained_rank not in self.study_request.retained_ranks
            or case.circuit_depth not in self.study_request.circuit_depths
            or case.parent_scale not in self.study_request.parent_scales
            or case.transformation_coefficient
            not in self.study_request.transformation_coefficients
        ):
            raise ValueError("case_analysis must identify one exact request expansion")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNBandEquivalenceHoppingLocalityFourierReference(
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue
):
    """Retain immutable direct-sum Fourier and support comparisons."""

    request: Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest
    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest
        ):
            raise TypeError("request must be the exact periodic-3D Fourier reference")
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
        """Return whether every independent finite-sum comparison passed."""
        return all(
            comparison.result().passed for comparison in self.comparisons.values()
        )


@final
class Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer(
    _PeriodicRankNBandEquivalenceHoppingLocalityFourierReferenceArithmetic,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseAction,
):
    """Compare aggregate Fourier/locality evidence with explicit finite sums.

    The non-onsite locality scalar currently repeats the producer's subtraction and
    zero-clipping policy.  It therefore does not independently detect the
    roundoff-scale false-zero mechanism recorded as ``TD-BEL-003``.  Other shell and
    support comparisons retain their direct finite-sum routes.
    """

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest,
    ) -> None:
        if (
            type(request)
            is not Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest
        ):
            raise TypeError("request must be the exact periodic-3D Fourier reference")
        self._request = request

    @property
    def request(
        self,
    ) -> Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest:
        """Return the immutable Fourier-reference request."""
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

    def _add_errors(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        prefix: str,
        observed: Periodic3DRankNBandEquivalenceHoppingLocalityErrorChannels,
        reference: _ErrorValues,
    ) -> None:
        for name in (
            "maximum_matrix_frobenius",
            "root_mean_square_matrix_frobenius",
            "maximum_ordered_spectrum",
            "root_mean_square_ordered_spectrum",
        ):
            comparisons[f"{prefix}.{name}"] = self._comparison(
                getattr(observed, name),
                getattr(reference, name),
            )

    def _add_support(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        prefix: str,
        observed: Periodic3DRankNSupportSelection,
        expected: _ExpectedSupport,
        metric_shell_values: tuple[int, ...],
    ) -> None:
        if expected.selected_index is None:
            if type(observed) is not Periodic3DRankNSupportUnresolved:
                raise ValueError("independent unresolved support disposition differs")
            comparisons[f"{prefix}.comparison_count"] = self._comparison(
                float(observed.comparison_count),
                float(len(metric_shell_values)),
                0.0,
            )
            comparisons[f"{prefix}.minimum_observed_error"] = self._comparison(
                observed.minimum_observed_error,
                expected.minimum_observed_error,
            )
            comparisons[f"{prefix}.largest_support_error"] = self._comparison(
                observed.largest_support_error,
                expected.largest_support_error,
            )
            return
        if type(observed) is not Periodic3DRankNSupportSelected:
            raise ValueError("independent selected support disposition differs")
        index = expected.selected_index
        comparisons[f"{prefix}.ordinal_shell_index"] = self._comparison(
            float(observed.ordinal_shell_index),
            float(index),
            0.0,
        )
        comparisons[f"{prefix}.metric_shell_value"] = self._comparison(
            float(observed.metric_shell_value),
            float(metric_shell_values[index]),
            0.0,
        )
        if expected.satisfying_error is None:
            raise RuntimeError("selected support must retain a satisfying error")
        comparisons[f"{prefix}.satisfying_error"] = self._comparison(
            observed.satisfying_error,
            expected.satisfying_error,
        )
        if expected.preceding_error is None:
            if observed.preceding_error is not None:
                raise ValueError("shell-zero support must not retain a preceding error")
        else:
            if observed.preceding_error is None:
                raise ValueError("nonzero selected support requires a preceding error")
            comparisons[f"{prefix}.preceding_error"] = self._comparison(
                observed.preceding_error,
                expected.preceding_error,
            )

    def execute(self) -> Periodic3DRankNBandEquivalenceHoppingLocalityFourierReference:
        """Return direct finite-sum comparisons without retained side effects."""
        request = self._request
        study = request.study_request
        observed_case = request.case_analysis
        geometry = next(
            case
            for case in study.cases
            if case.lattice_control.to_wire() == observed_case.case_identifier
        )
        independent = _IndependentPeriodic3DRankNCase(
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
        exact_construction = independent.exact_operators(construction)
        exact_evaluation = independent.exact_operators(evaluation)
        construction_gauge = independent.gauges(construction)
        evaluation_gauge = independent.gauges(evaluation)
        gauge_transformed_construction = np.asarray(
            np.swapaxes(construction_gauge.conjugate(), -1, -2)
            @ exact_construction
            @ construction_gauge,
            dtype=np.complex128,
        )
        gauge_transformed_evaluation = np.asarray(
            np.swapaxes(evaluation_gauge.conjugate(), -1, -2)
            @ exact_evaluation
            @ evaluation_gauge,
            dtype=np.complex128,
        )
        global_cross = np.sum(
            np.swapaxes(construction_gauge.conjugate(), -1, -2),
            axis=tuple(range(construction_gauge.ndim - 2)),
        )
        global_right = independent._right_polar_factor(global_cross)
        global_construction = np.asarray(
            global_right.conjugate().T @ gauge_transformed_construction @ global_right,
            dtype=np.complex128,
        )
        global_evaluation = np.asarray(
            global_right.conjugate().T @ gauge_transformed_evaluation @ global_right,
            dtype=np.complex128,
        )
        fields = MappingProxyType(
            {
                Periodic3DRankNGaugeAlignment.IDENTITY: (
                    gauge_transformed_construction,
                    gauge_transformed_evaluation,
                ),
                Periodic3DRankNGaugeAlignment.GLOBAL_UNITARY: (
                    global_construction,
                    global_evaluation,
                ),
                Periodic3DRankNGaugeAlignment.POINTWISE_UNITARY: (
                    exact_construction,
                    exact_evaluation,
                ),
                Periodic3DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                    exact_construction,
                    exact_evaluation,
                ),
            }
        )
        grid = _DirectFiniteFourierGrid(
            spatial_dimension=3,
            construction_coordinates=construction,
            evaluation_coordinates=evaluation,
            construction_size=study.construction_size,
            retained_rank=observed_case.retained_rank,
            geometry=geometry,
        )
        reference_channel = grid.channel(exact_construction)
        metric_shell_values = tuple(
            value
            for value in sorted(set(int(item) for item in grid.metric_indices))
            if value <= study.shell_cap
        )
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}
        observed_by_alignment = {
            item.alignment: item for item in observed_case.alignments
        }
        for alignment in study.gauge_alignments:
            observed = observed_by_alignment[alignment]
            if (
                type(observed)
                is not Periodic3DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis  # noqa: E501
            ):
                raise ValueError(
                    "Fourier reference requires qualified alignment routes"
                )
            comparison_construction, comparison_evaluation = fields[alignment]
            comparison_channel = grid.channel(comparison_construction)
            prefix = f"alignment[{alignment.to_wire()}]"
            self._add_errors(
                comparisons,
                f"{prefix}.reference_reconstruction",
                observed.reference_reconstruction_errors,
                self._errors(reference_channel.full_construction, exact_construction),
            )
            self._add_errors(
                comparisons,
                f"{prefix}.comparison_reconstruction",
                observed.comparison_reconstruction_errors,
                self._errors(
                    comparison_channel.full_construction,
                    comparison_construction,
                ),
            )
            self._add_errors(
                comparisons,
                f"{prefix}.reference_interpolation",
                observed.reference_interpolation_errors,
                self._errors(reference_channel.full_evaluation, exact_evaluation),
            )
            self._add_errors(
                comparisons,
                f"{prefix}.comparison_interpolation",
                observed.comparison_interpolation_errors,
                self._errors(
                    comparison_channel.full_evaluation,
                    comparison_evaluation,
                ),
            )
            zero_modes = np.all(grid.modes == 0, axis=1)
            for channel_name, observed_locality, channel in (
                ("reference", observed.reference_locality, reference_channel),
                ("comparison", observed.comparison_locality, comparison_channel),
            ):
                total_power = float(
                    math.fsum(float(value) for value in channel.normalized_powers)
                )
                onsite_power = float(
                    math.fsum(
                        float(value) for value in channel.normalized_powers[zero_modes]
                    )
                )
                nononsite_power = max(0.0, total_power - onsite_power)
                for name, observed_value, reference_value in (
                    ("total_power", observed_locality.total_power, total_power),
                    ("onsite_power", observed_locality.onsite_power, onsite_power),
                    (
                        "nononsite_power",
                        observed_locality.nononsite_power,
                        nononsite_power,
                    ),
                ):
                    comparisons[f"{prefix}.{channel_name}_locality.{name}"] = (
                        self._comparison(
                            observed_value,
                            reference_value,
                        )
                    )
            reference_total_errors: list[_ErrorValues] = []
            comparison_total_errors: list[_ErrorValues] = []
            for ordinal, (metric_value, observed_shell) in enumerate(
                zip(metric_shell_values, observed.shells, strict=True)
            ):
                selected = grid.metric_indices <= metric_value
                reference_shell = grid.shell_evaluation(reference_channel, metric_value)
                comparison_shell = grid.shell_evaluation(
                    comparison_channel, metric_value
                )
                reference_total = self._errors(reference_shell, exact_evaluation)
                comparison_total = self._errors(comparison_shell, comparison_evaluation)
                reference_truncation = self._errors(
                    reference_shell,
                    reference_channel.full_evaluation,
                )
                comparison_truncation = self._errors(
                    comparison_shell,
                    comparison_channel.full_evaluation,
                )
                reference_total_errors.append(reference_total)
                comparison_total_errors.append(comparison_total)
                shell_prefix = f"{prefix}.shell[{metric_value}]"
                for name, observed_value, reference_value, tolerance in (
                    (
                        "ordinal_shell_index",
                        float(observed_shell.ordinal_shell_index),
                        float(ordinal),
                        0.0,
                    ),
                    (
                        "metric_shell_value",
                        float(observed_shell.metric_shell_value),
                        float(metric_value),
                        0.0,
                    ),
                    (
                        "retained_block_count",
                        float(observed_shell.retained_block_count),
                        float(np.count_nonzero(selected)),
                        0.0,
                    ),
                    (
                        "reference_shell_power",
                        observed_shell.reference_shell_power,
                        float(
                            math.fsum(
                                float(value)
                                for value in reference_channel.normalized_powers[
                                    grid.metric_indices == metric_value
                                ]
                            )
                        ),
                        _REFERENCE_ABSOLUTE_TOLERANCE,
                    ),
                    (
                        "comparison_shell_power",
                        observed_shell.comparison_shell_power,
                        float(
                            math.fsum(
                                float(value)
                                for value in comparison_channel.normalized_powers[
                                    grid.metric_indices == metric_value
                                ]
                            )
                        ),
                        _REFERENCE_ABSOLUTE_TOLERANCE,
                    ),
                    (
                        "reference_omitted_power",
                        observed_shell.reference_omitted_power,
                        float(
                            math.fsum(
                                float(value)
                                for value in reference_channel.normalized_powers[
                                    grid.metric_indices > metric_value
                                ]
                            )
                        ),
                        _REFERENCE_ABSOLUTE_TOLERANCE,
                    ),
                    (
                        "comparison_omitted_power",
                        observed_shell.comparison_omitted_power,
                        float(
                            math.fsum(
                                float(value)
                                for value in comparison_channel.normalized_powers[
                                    grid.metric_indices > metric_value
                                ]
                            )
                        ),
                        _REFERENCE_ABSOLUTE_TOLERANCE,
                    ),
                ):
                    comparisons[f"{shell_prefix}.{name}"] = self._comparison(
                        observed_value,
                        reference_value,
                        tolerance,
                    )
                self._add_errors(
                    comparisons,
                    f"{shell_prefix}.reference_total",
                    observed_shell.reference_total_errors,
                    reference_total,
                )
                self._add_errors(
                    comparisons,
                    f"{shell_prefix}.comparison_total",
                    observed_shell.comparison_total_errors,
                    comparison_total,
                )
                self._add_errors(
                    comparisons,
                    f"{shell_prefix}.reference_truncation",
                    observed_shell.reference_truncation_errors,
                    reference_truncation,
                )
                self._add_errors(
                    comparisons,
                    f"{shell_prefix}.comparison_truncation",
                    observed_shell.comparison_truncation_errors,
                    comparison_truncation,
                )
            for observed_decision in observed.tolerance_decisions:
                tolerance = observed_decision.tolerance
                decision_prefix = f"{prefix}.tolerance[{tolerance.hex()}]"
                reference_matrix_errors = tuple(
                    value.maximum_matrix_frobenius for value in reference_total_errors
                )
                reference_band_errors = tuple(
                    value.maximum_ordered_spectrum for value in reference_total_errors
                )
                comparison_matrix_errors = tuple(
                    value.maximum_matrix_frobenius for value in comparison_total_errors
                )
                comparison_band_errors = tuple(
                    value.maximum_ordered_spectrum for value in comparison_total_errors
                )
                for name, observed_selection, errors in (
                    (
                        "reference_matrix",
                        observed_decision.reference_matrix,
                        reference_matrix_errors,
                    ),
                    (
                        "reference_ordered_spectrum",
                        observed_decision.reference_ordered_spectrum,
                        reference_band_errors,
                    ),
                    (
                        "comparison_matrix",
                        observed_decision.comparison_matrix,
                        comparison_matrix_errors,
                    ),
                    (
                        "comparison_ordered_spectrum",
                        observed_decision.comparison_ordered_spectrum,
                        comparison_band_errors,
                    ),
                ):
                    self._add_support(
                        comparisons,
                        f"{decision_prefix}.{name}",
                        observed_selection,
                        self._selection(errors, tolerance),
                        metric_shell_values,
                    )
        return Periodic3DRankNBandEquivalenceHoppingLocalityFourierReference(
            request=request,
            comparisons=comparisons,
        )


__all__ = [
    "Periodic3DRankNBandEquivalenceHoppingLocalityFourierReference",
    "Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer",
    "Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest",
]
