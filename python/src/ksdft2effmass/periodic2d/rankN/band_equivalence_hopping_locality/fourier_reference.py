"""Independent periodic-2D rank-N Fourier, shell, and support references.

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
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array, Int64Array
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .reference import _IndependentPeriodic2DRankNCase
from .request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequest,
)
from .result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels,
    Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis,
    Periodic2DRankNSupportSelected,
    Periodic2DRankNSupportSelection,
    Periodic2DRankNSupportUnresolved,
)

_REFERENCE_ABSOLUTE_TOLERANCE = 2.0e-10


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest
):
    """Bind one analyzed case to the typed study geometry and mesh controls."""

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
            or case.attack_coefficient not in self.study_request.attack_coefficients
        ):
            raise ValueError("case_analysis must identify one exact request expansion")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNBandEquivalenceHoppingLocalityFourierReference(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue
):
    """Retain immutable direct-sum Fourier and support comparisons."""

    request: Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest
    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest
        ):
            raise TypeError("request must be the exact periodic-2D Fourier reference")
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


@dataclass(frozen=True, slots=True)
class _ErrorValues:
    maximum_matrix_frobenius: float
    root_mean_square_matrix_frobenius: float
    maximum_ordered_spectrum: float
    root_mean_square_ordered_spectrum: float


@dataclass(frozen=True, slots=True)
class _FourierChannel:
    coefficients: Complex128Array
    full_construction: Complex128Array
    full_evaluation: Complex128Array
    normalized_powers: Float64Array


@dataclass(frozen=True, slots=True)
class _ExpectedSupport:
    selected_index: int | None
    satisfying_error: float | None
    preceding_error: float | None
    minimum_observed_error: float
    largest_support_error: float


@final
class _DirectFiniteFourierGrid:
    """Own explicit construction/evaluation phases and independent metric shells."""

    __slots__ = (
        "_construction_phase",
        "_construction_shape",
        "_evaluation_phase",
        "_evaluation_shape",
        "_metric_indices",
        "_modes",
        "_ordinary",
        "_rank",
        "_transform_phase",
    )

    def __init__(
        self,
        *,
        construction_coordinates: Float64Array,
        evaluation_coordinates: Float64Array,
        construction_size: int,
        retained_rank: int,
        geometry: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
    ) -> None:
        dimension = 2
        axis = np.arange(
            -construction_size // 2, construction_size // 2, dtype=np.int64
        )
        all_modes = np.asarray(
            np.stack(np.meshgrid(axis, axis, indexing="ij"), axis=-1).reshape(
                -1, dimension
            ),
            dtype=np.int64,
        )
        ordinary = ~np.any(all_modes == -construction_size // 2, axis=1)
        modes = np.asarray(all_modes[ordinary], dtype=np.int64)
        construction_flat = construction_coordinates.reshape(-1, dimension)
        evaluation_flat = evaluation_coordinates.reshape(-1, dimension)
        self._transform_phase = np.asarray(
            np.exp(-2.0j * np.pi * (construction_flat @ all_modes.T)),
            dtype=np.complex128,
        )
        self._construction_phase = np.asarray(
            np.exp(2.0j * np.pi * (construction_flat @ modes.T)),
            dtype=np.complex128,
        )
        self._evaluation_phase = np.asarray(
            np.exp(2.0j * np.pi * (evaluation_flat @ modes.T)),
            dtype=np.complex128,
        )
        metric = geometry.direct_metric.metric_tensor
        metric_values = geometry.shell_metric_scale * np.einsum(
            "ri,ij,rj->r",
            modes,
            metric,
            modes,
        )
        rounded = np.rint(metric_values)
        if float(np.max(np.abs(metric_values - rounded))) > 1.0e-12:
            raise ValueError("independent scaled metric values are not integral")
        self._metric_indices = np.asarray(rounded, dtype=np.int64)
        self._modes = modes
        self._ordinary = np.asarray(ordinary, dtype=np.bool_)
        self._construction_shape = construction_coordinates.shape[:-1]
        self._evaluation_shape = evaluation_coordinates.shape[:-1]
        self._rank = retained_rank

    @property
    def metric_indices(self) -> Int64Array:
        """Return the independently classified ordinary-mode metric values."""
        return self._metric_indices

    @property
    def modes(self) -> Int64Array:
        """Return the independently enumerated ordinary Fourier modes."""
        return self._modes

    def channel(self, construction_field: Complex128Array) -> _FourierChannel:
        """Transform and evaluate one field through explicit dense finite sums."""
        point_count = math.prod(self._construction_shape)
        flattened = construction_field.reshape(point_count, self._rank * self._rank)
        all_coefficients = (self._transform_phase.T @ flattened) / float(point_count)
        coefficients = np.asarray(
            all_coefficients[self._ordinary].reshape(-1, self._rank, self._rank),
            dtype=np.complex128,
        )
        full_construction = np.asarray(
            (
                self._construction_phase @ coefficients.reshape(-1, self._rank**2)
            ).reshape(
                *self._construction_shape,
                self._rank,
                self._rank,
            ),
            dtype=np.complex128,
        )
        full_evaluation = np.asarray(
            (self._evaluation_phase @ coefficients.reshape(-1, self._rank**2)).reshape(
                *self._evaluation_shape,
                self._rank,
                self._rank,
            ),
            dtype=np.complex128,
        )
        normalized_powers = np.asarray(
            np.sum(np.abs(coefficients) ** 2, axis=(-2, -1)) / float(self._rank),
            dtype=np.float64,
        )
        return _FourierChannel(
            coefficients=coefficients,
            full_construction=full_construction,
            full_evaluation=full_evaluation,
            normalized_powers=normalized_powers,
        )

    def shell_evaluation(
        self,
        channel: _FourierChannel,
        metric_shell_value: int,
    ) -> Complex128Array:
        """Evaluate one complete cumulative physical-metric shell."""
        selected = self._metric_indices <= metric_shell_value
        return np.asarray(
            (
                self._evaluation_phase[:, selected]
                @ channel.coefficients[selected].reshape(-1, self._rank**2)
            ).reshape(*self._evaluation_shape, self._rank, self._rank),
            dtype=np.complex128,
        )


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction
):
    """Compare aggregate Fourier/locality evidence with explicit finite sums."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest,
    ) -> None:
        if (
            type(request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest
        ):
            raise TypeError("request must be the exact periodic-2D Fourier reference")
        self._request = request

    @property
    def request(
        self,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest:
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

    @staticmethod
    def _errors(
        approximation: Complex128Array, direct: Complex128Array
    ) -> _ErrorValues:
        rank = int(approximation.shape[-1])
        difference = approximation - direct
        frobenius = np.linalg.norm(difference, axis=(-2, -1))
        band_difference = np.abs(
            np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(direct)
        )
        band_l2 = np.linalg.norm(band_difference, axis=-1)
        rank_scale = math.sqrt(rank)
        return _ErrorValues(
            maximum_matrix_frobenius=float(np.max(frobenius)) / rank_scale,
            root_mean_square_matrix_frobenius=(
                float(np.sqrt(np.mean(frobenius**2))) / rank_scale
            ),
            maximum_ordered_spectrum=float(np.max(band_difference)),
            root_mean_square_ordered_spectrum=(
                float(np.sqrt(np.mean(band_l2**2))) / rank_scale
            ),
        )

    def _add_errors(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        prefix: str,
        observed: Periodic2DRankNBandEquivalenceHoppingLocalityErrorChannels,
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

    @staticmethod
    def _selection(errors: tuple[float, ...], tolerance: float) -> _ExpectedSupport:
        selected = next(
            (index for index, error in enumerate(errors) if error <= tolerance),
            None,
        )
        if selected is None:
            return _ExpectedSupport(
                selected_index=None,
                satisfying_error=None,
                preceding_error=None,
                minimum_observed_error=min(errors),
                largest_support_error=errors[-1],
            )
        return _ExpectedSupport(
            selected_index=selected,
            satisfying_error=errors[selected],
            preceding_error=None if selected == 0 else errors[selected - 1],
            minimum_observed_error=min(errors),
            largest_support_error=errors[-1],
        )

    def _add_support(
        self,
        comparisons: dict[str, MaximumAbsoluteErrorComparison],
        prefix: str,
        observed: Periodic2DRankNSupportSelection,
        expected: _ExpectedSupport,
        metric_shell_values: tuple[int, ...],
    ) -> None:
        if expected.selected_index is None:
            if type(observed) is not Periodic2DRankNSupportUnresolved:
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
        if type(observed) is not Periodic2DRankNSupportSelected:
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

    def execute(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityFourierReference:
        """Return direct finite-sum comparisons without retained side effects."""
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
        exact_construction = independent.exact_operators(construction)
        exact_evaluation = independent.exact_operators(evaluation)
        construction_gauge = independent.gauges(construction)
        evaluation_gauge = independent.gauges(evaluation)
        attacked_construction = np.asarray(
            np.swapaxes(construction_gauge.conjugate(), -1, -2)
            @ exact_construction
            @ construction_gauge,
            dtype=np.complex128,
        )
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
        global_right = independent._right_polar_factor(global_cross)
        global_construction = np.asarray(
            global_right.conjugate().T @ attacked_construction @ global_right,
            dtype=np.complex128,
        )
        global_evaluation = np.asarray(
            global_right.conjugate().T @ attacked_evaluation @ global_right,
            dtype=np.complex128,
        )
        fields = MappingProxyType(
            {
                Periodic2DRankNGaugeAlignment.IDENTITY: (
                    attacked_construction,
                    attacked_evaluation,
                ),
                Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY: (
                    global_construction,
                    global_evaluation,
                ),
                Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY: (
                    exact_construction,
                    exact_evaluation,
                ),
                Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                    exact_construction,
                    exact_evaluation,
                ),
            }
        )
        grid = _DirectFiniteFourierGrid(
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
                is not Periodic2DRankNBandEquivalenceHoppingLocalityQualifiedAlignmentAnalysis  # noqa: E501
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
        return Periodic2DRankNBandEquivalenceHoppingLocalityFourierReference(
            request=request,
            comparisons=comparisons,
        )


__all__ = [
    "Periodic2DRankNBandEquivalenceHoppingLocalityFourierReference",
    "Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer",
    "Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest",
]
