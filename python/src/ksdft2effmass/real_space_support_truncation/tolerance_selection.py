"""Dimension-independent tolerance selection for real-space support truncation."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeIntegerComponents,
)

from .base import RealSpaceSupportTruncation
from .support import ConjugateClosedSupport


@dataclass(frozen=True, slots=True)
class RankNormalizedMatrixFrobeniusErrors(RealSpaceSupportTruncation):
    """Retain maximum and RMS rank-normalized matrix Frobenius errors."""

    maximum_error: float
    root_mean_square_error: float

    def __post_init__(self) -> None:
        for name in ("maximum_error", "root_mean_square_error"):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class OrderedEigenvalueErrors(RealSpaceSupportTruncation):
    """Retain maximum-absolute and RMS ordered-eigenvalue errors."""

    maximum_absolute_error: float
    root_mean_square_error: float

    def __post_init__(self) -> None:
        for name in ("maximum_absolute_error", "root_mean_square_error"):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationErrors(RealSpaceSupportTruncation):
    """Retain typed errors on one common reciprocal-space sample grid.

    Matrix errors use the Frobenius norm divided by the square root of the retained
    matrix rank before maximum or root-mean-square aggregation. Eigenvalue errors pair
    equal-rank eigenvalues in ascending order before maximum-absolute or
    root-mean-square aggregation. The family adapter owns state-space alignment,
    energy reference, units, and reciprocal-space sampling.
    """

    matrix_frobenius: RankNormalizedMatrixFrobeniusErrors
    ordered_eigenvalues: OrderedEigenvalueErrors

    def __post_init__(self) -> None:
        if type(self.matrix_frobenius) is not RankNormalizedMatrixFrobeniusErrors:
            raise TypeError(
                "matrix_frobenius must be exact RankNormalizedMatrixFrobeniusErrors"
            )
        if type(self.ordered_eigenvalues) is not OrderedEigenvalueErrors:
            raise TypeError("ordered_eigenvalues must be exact OrderedEigenvalueErrors")


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationComparison(RealSpaceSupportTruncation):
    """Compare two model routes at one admitted real-space support."""

    support: ConjugateClosedSupport
    reference_model_errors: RealSpaceSupportTruncationErrors
    comparison_model_errors: RealSpaceSupportTruncationErrors

    def __post_init__(self) -> None:
        if type(self.support) is not ConjugateClosedSupport:
            raise TypeError("support must be an exact ConjugateClosedSupport")
        if type(self.reference_model_errors) is not RealSpaceSupportTruncationErrors:
            raise TypeError(
                "reference_model_errors must be exact RealSpaceSupportTruncationErrors"
            )
        if type(self.comparison_model_errors) is not RealSpaceSupportTruncationErrors:
            raise TypeError(
                "comparison_model_errors must be exact RealSpaceSupportTruncationErrors"
            )


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationToleranceSelectionRequest(RealSpaceSupportTruncation):
    """Own an ordered comparison inventory and its selection tolerance."""

    comparisons: tuple[RealSpaceSupportTruncationComparison, ...]
    tolerance: float

    def __post_init__(self) -> None:
        if type(self.comparisons) is not tuple or not self.comparisons:
            raise TypeError("comparisons must be a nonempty tuple")
        if any(
            type(comparison) is not RealSpaceSupportTruncationComparison
            for comparison in self.comparisons
        ):
            raise TypeError("comparisons must contain exact truncation comparisons")
        if type(self.tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(self.tolerance) or self.tolerance < 0.0:
            raise ValueError("tolerance must be finite and nonnegative")
        dimension = self.comparisons[0].support.dimension
        previous_components: set[LatticeIntegerComponents] | None = None
        for comparison in self.comparisons:
            if comparison.support.dimension is not dimension:
                raise ValueError("all supports must have one lattice dimension")
            components = {
                displacement.components
                for displacement in comparison.support.displacements
            }
            if previous_components is not None and not previous_components < components:
                raise ValueError("supports must form a strictly nested sequence")
            previous_components = components

    @property
    def supports(self) -> tuple[ConjugateClosedSupport, ...]:
        """Return supports in declared comparison order."""
        return tuple(comparison.support for comparison in self.comparisons)

    @property
    def reference_matrix_frobenius_maximum_errors(self) -> tuple[float, ...]:
        """Return reference-route matrix errors in comparison order."""
        return tuple(
            comparison.reference_model_errors.matrix_frobenius.maximum_error
            for comparison in self.comparisons
        )

    @property
    def reference_ordered_eigenvalue_maximum_absolute_errors(
        self,
    ) -> tuple[float, ...]:
        """Return reference-route eigenvalue errors in comparison order."""
        return tuple(
            comparison.reference_model_errors.ordered_eigenvalues.maximum_absolute_error
            for comparison in self.comparisons
        )

    @property
    def comparison_matrix_frobenius_maximum_errors(self) -> tuple[float, ...]:
        """Return comparison-route matrix errors in comparison order."""
        return tuple(
            comparison.comparison_model_errors.matrix_frobenius.maximum_error
            for comparison in self.comparisons
        )

    @property
    def comparison_ordered_eigenvalue_maximum_absolute_errors(
        self,
    ) -> tuple[float, ...]:
        """Return comparison-route eigenvalue errors in comparison order."""
        return tuple(
            comparison.comparison_model_errors.ordered_eigenvalues.maximum_absolute_error
            for comparison in self.comparisons
        )


class SupportToleranceSelectionOutcome(RealSpaceSupportTruncation):
    """Closed outcome base for one support-tolerance selection."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class MinimumToleranceSatisfyingSupport(SupportToleranceSelectionOutcome):
    """Retain the minimum admitted support satisfying one error inequality."""

    comparison_index: int
    support: ConjugateClosedSupport
    satisfying_error: float
    preceding_error: float | None

    def __post_init__(self) -> None:
        if type(self.comparison_index) is not int:
            raise TypeError("comparison_index must be a built-in int")
        if self.comparison_index < 0:
            raise ValueError("comparison_index must be nonnegative")
        if type(self.support) is not ConjugateClosedSupport:
            raise TypeError("support must be an exact ConjugateClosedSupport")
        if type(self.satisfying_error) is not float:
            raise TypeError("satisfying_error must be a built-in float")
        if not math.isfinite(self.satisfying_error) or self.satisfying_error < 0.0:
            raise ValueError("satisfying_error must be finite and nonnegative")
        if self.preceding_error is not None:
            if type(self.preceding_error) is not float:
                raise TypeError("preceding_error must be a built-in float or None")
            if not math.isfinite(self.preceding_error) or self.preceding_error < 0.0:
                raise ValueError("preceding_error must be finite and nonnegative")
        if (self.comparison_index == 0) is not (self.preceding_error is None):
            raise ValueError(
                "preceding_error must be absent exactly for the first comparison"
            )


@dataclass(frozen=True, slots=True)
class SupportToleranceUnresolved(SupportToleranceSelectionOutcome):
    """Retain observed errors when no admitted support satisfies the tolerance."""

    comparison_count: int
    minimum_observed_error: float
    largest_support_error: float

    def __post_init__(self) -> None:
        if type(self.comparison_count) is not int:
            raise TypeError("comparison_count must be a built-in int")
        if self.comparison_count <= 0:
            raise ValueError("comparison_count must be positive")
        for name in ("minimum_observed_error", "largest_support_error"):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if self.minimum_observed_error > self.largest_support_error:
            raise ValueError(
                "minimum_observed_error cannot exceed largest_support_error"
            )


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationErrorToleranceSelectionRequest(
    RealSpaceSupportTruncation
):
    """Bind one nested support inventory and one scalar error channel."""

    supports: tuple[ConjugateClosedSupport, ...]
    errors: tuple[float, ...]
    tolerance: float

    def __post_init__(self) -> None:
        if type(self.supports) is not tuple or not self.supports:
            raise TypeError("supports must be a nonempty tuple")
        if any(
            type(support) is not ConjugateClosedSupport for support in self.supports
        ):
            raise TypeError("supports must contain exact ConjugateClosedSupport values")
        if type(self.errors) is not tuple or len(self.errors) != len(self.supports):
            raise TypeError("errors must be a tuple aligned with supports")
        if any(type(error) is not float for error in self.errors):
            raise TypeError("errors must contain built-in floats")
        if any(not math.isfinite(error) or error < 0.0 for error in self.errors):
            raise ValueError("errors must be finite and nonnegative")
        if type(self.tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(self.tolerance) or self.tolerance < 0.0:
            raise ValueError("tolerance must be finite and nonnegative")
        dimension = self.supports[0].dimension
        previous_components: set[LatticeIntegerComponents] | None = None
        for support in self.supports:
            if support.dimension is not dimension:
                raise ValueError("supports must have one lattice dimension")
            components = {
                displacement.components for displacement in support.displacements
            }
            if previous_components is not None and not previous_components < components:
                raise ValueError("supports must form a strictly nested sequence")
            previous_components = components


class RealSpaceSupportTruncationErrorToleranceSelector(RealSpaceSupportTruncation):
    """Select one minimum tolerance-satisfying support for one error channel."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: RealSpaceSupportTruncationErrorToleranceSelectionRequest,
    ) -> None:
        if (
            type(request)
            is not RealSpaceSupportTruncationErrorToleranceSelectionRequest
        ):
            raise TypeError("request must be the exact single-error request")
        self._request = request

    @property
    def request(self) -> RealSpaceSupportTruncationErrorToleranceSelectionRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def execute(self) -> SupportToleranceSelectionOutcome:
        """Return the first passing support or an explicit unresolved outcome."""
        for index, error in enumerate(self._request.errors):
            if error <= self._request.tolerance:
                return MinimumToleranceSatisfyingSupport(
                    comparison_index=index,
                    support=self._request.supports[index],
                    satisfying_error=error,
                    preceding_error=(
                        None if index == 0 else self._request.errors[index - 1]
                    ),
                )
        return SupportToleranceUnresolved(
            comparison_count=len(self._request.errors),
            minimum_observed_error=min(self._request.errors),
            largest_support_error=self._request.errors[-1],
        )


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationModelToleranceSelection(RealSpaceSupportTruncation):
    """Retain support selections for two explicitly named error functionals."""

    matrix_frobenius_maximum_error: SupportToleranceSelectionOutcome
    ordered_eigenvalue_maximum_absolute_error: SupportToleranceSelectionOutcome

    def __post_init__(self) -> None:
        for name in (
            "matrix_frobenius_maximum_error",
            "ordered_eigenvalue_maximum_absolute_error",
        ):
            outcome = getattr(self, name)
            if type(outcome) not in (
                MinimumToleranceSatisfyingSupport,
                SupportToleranceUnresolved,
            ):
                raise TypeError(f"{name} must be one closed outcome variant")


@dataclass(frozen=True, slots=True, init=False)
class RealSpaceSupportTruncationToleranceSelection(RealSpaceSupportTruncation):
    """Derive model-specific support outcomes from one exact request.

    The constructor accepts only the canonical request. Model outcomes cannot be
    supplied independently, so this value has no duplicated-state consistency check.
    """

    request: RealSpaceSupportTruncationToleranceSelectionRequest
    reference_model: RealSpaceSupportTruncationModelToleranceSelection
    comparison_model: RealSpaceSupportTruncationModelToleranceSelection

    def __init__(
        self,
        request: RealSpaceSupportTruncationToleranceSelectionRequest,
    ) -> None:
        if type(request) is not RealSpaceSupportTruncationToleranceSelectionRequest:
            raise TypeError("request must be an exact tolerance-selection request")
        supports = request.supports
        outcomes = tuple(
            RealSpaceSupportTruncationErrorToleranceSelector(
                request=RealSpaceSupportTruncationErrorToleranceSelectionRequest(
                    supports=supports,
                    errors=errors,
                    tolerance=request.tolerance,
                )
            ).execute()
            for errors in (
                request.reference_matrix_frobenius_maximum_errors,
                request.reference_ordered_eigenvalue_maximum_absolute_errors,
                request.comparison_matrix_frobenius_maximum_errors,
                request.comparison_ordered_eigenvalue_maximum_absolute_errors,
            )
        )
        object.__setattr__(self, "request", request)
        object.__setattr__(
            self,
            "reference_model",
            RealSpaceSupportTruncationModelToleranceSelection(
                matrix_frobenius_maximum_error=outcomes[0],
                ordered_eigenvalue_maximum_absolute_error=outcomes[1],
            ),
        )
        object.__setattr__(
            self,
            "comparison_model",
            RealSpaceSupportTruncationModelToleranceSelection(
                matrix_frobenius_maximum_error=outcomes[2],
                ordered_eigenvalue_maximum_absolute_error=outcomes[3],
            ),
        )


class RealSpaceSupportTruncationToleranceSelector(RealSpaceSupportTruncation):
    """Select minimum tolerance-satisfying supports without family labels."""

    __slots__ = ()

    def execute(
        self, request: RealSpaceSupportTruncationToleranceSelectionRequest
    ) -> RealSpaceSupportTruncationToleranceSelection:
        """Return model-specific selections for the exact admitted request."""
        return RealSpaceSupportTruncationToleranceSelection(request)


__all__ = [
    "MinimumToleranceSatisfyingSupport",
    "OrderedEigenvalueErrors",
    "RankNormalizedMatrixFrobeniusErrors",
    "RealSpaceSupportTruncationErrorToleranceSelectionRequest",
    "RealSpaceSupportTruncationErrorToleranceSelector",
    "RealSpaceSupportTruncationErrors",
    "RealSpaceSupportTruncationModelToleranceSelection",
    "RealSpaceSupportTruncationComparison",
    "RealSpaceSupportTruncationToleranceSelection",
    "RealSpaceSupportTruncationToleranceSelectionRequest",
    "RealSpaceSupportTruncationToleranceSelector",
    "SupportToleranceSelectionOutcome",
    "SupportToleranceUnresolved",
]
