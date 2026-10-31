"""Software contracts for dimension-independent support-tolerance selection."""

from __future__ import annotations

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from ksdft2effmass.real_space_support_truncation import (
    ConjugateClosedSupport,
    MinimumToleranceSatisfyingSupport,
    OrderedEigenvalueErrors,
    RankNormalizedMatrixFrobeniusErrors,
    RealSpaceSupportTruncationComparison,
    RealSpaceSupportTruncationErrors,
    RealSpaceSupportTruncationToleranceSelection,
    RealSpaceSupportTruncationToleranceSelectionRequest,
    RealSpaceSupportTruncationToleranceSelector,
    SupportToleranceUnresolved,
    SymmetricRangeSupport1D,
)

pytestmark = pytest.mark.software_verification


def _errors(matrix: float, spectrum: float) -> RealSpaceSupportTruncationErrors:
    return RealSpaceSupportTruncationErrors(
        matrix_frobenius=RankNormalizedMatrixFrobeniusErrors(
            maximum_error=matrix,
            root_mean_square_error=matrix / 2.0,
        ),
        ordered_eigenvalues=OrderedEigenvalueErrors(
            maximum_absolute_error=spectrum,
            root_mean_square_error=spectrum / 2.0,
        ),
    )


def _support(
    dimension: LatticeDimension,
    components: tuple[tuple[int, ...], ...],
) -> ConjugateClosedSupport:
    return ConjugateClosedSupport(
        tuple(LatticeDisplacement(dimension, value) for value in components)  # type: ignore[arg-type]
    )


def _comparisons_for_dimension(
    dimension: LatticeDimension,
) -> tuple[RealSpaceSupportTruncationComparison, ...]:
    if dimension is LatticeDimension.ONE:
        supports = tuple(
            SymmetricRangeSupport1D(maximum_range).support for maximum_range in range(3)
        )
    elif dimension is LatticeDimension.TWO:
        supports = (
            _support(dimension, ((0, 0),)),
            _support(dimension, ((-1, 0), (0, 0), (1, 0))),
            _support(
                dimension,
                ((-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)),
            ),
        )
    else:
        supports = (
            _support(dimension, ((0, 0, 0),)),
            _support(dimension, ((-1, 0, 0), (0, 0, 0), (1, 0, 0))),
            _support(
                dimension,
                (
                    (-1, 0, 0),
                    (0, -1, 0),
                    (0, 0, 0),
                    (0, 1, 0),
                    (1, 0, 0),
                ),
            ),
        )
    return tuple(
        RealSpaceSupportTruncationComparison(
            support=support,
            reference_model_errors=_errors(
                matrix=(0.8, 0.2, 0.05)[index],
                spectrum=(0.4, 0.08, 0.03)[index],
            ),
            comparison_model_errors=_errors(
                matrix=(0.9, 0.3, 0.2)[index],
                spectrum=(0.7, 0.1, 0.04)[index],
            ),
        )
        for index, support in enumerate(supports)
    )


class TestRealSpaceSupportTruncationToleranceSelector:
    """Select the minimum satisfying support in one, two, and three dimensions."""

    @pytest.mark.parametrize(
        "dimension",
        [LatticeDimension.ONE, LatticeDimension.TWO, LatticeDimension.THREE],
    )
    def test_execute__nested_supports__selects_exact_error_functionals(
        self, dimension: LatticeDimension
    ) -> None:
        """One shared selector preserves model and error-functional identity."""
        request = RealSpaceSupportTruncationToleranceSelectionRequest(
            comparisons=_comparisons_for_dimension(dimension),
            tolerance=0.1,
        )

        selection = RealSpaceSupportTruncationToleranceSelector().execute(request)

        reference_spectrum = (
            selection.reference_model.ordered_eigenvalue_maximum_absolute_error
        )
        reference_matrix = selection.reference_model.matrix_frobenius_maximum_error
        comparison_spectrum = (
            selection.comparison_model.ordered_eigenvalue_maximum_absolute_error
        )
        comparison_matrix = selection.comparison_model.matrix_frobenius_maximum_error
        assert type(reference_spectrum) is MinimumToleranceSatisfyingSupport
        assert reference_spectrum.comparison_index == 1
        assert reference_spectrum.satisfying_error == 0.08
        assert reference_spectrum.preceding_error == 0.4
        assert type(reference_matrix) is MinimumToleranceSatisfyingSupport
        assert reference_matrix.comparison_index == 2
        assert type(comparison_spectrum) is MinimumToleranceSatisfyingSupport
        assert comparison_spectrum.comparison_index == 1
        assert comparison_spectrum.satisfying_error == request.tolerance
        assert type(comparison_matrix) is SupportToleranceUnresolved
        assert comparison_matrix.comparison_count == 3
        assert comparison_matrix.minimum_observed_error == 0.2
        assert comparison_matrix.largest_support_error == 0.2

    def test_selection__request_constructor__derives_the_selector_outcome(self) -> None:
        """The public constructor accepts no independently supplied outcomes."""
        request = RealSpaceSupportTruncationToleranceSelectionRequest(
            comparisons=_comparisons_for_dimension(LatticeDimension.ONE),
            tolerance=0.1,
        )

        selection = RealSpaceSupportTruncationToleranceSelection(request)

        assert selection == RealSpaceSupportTruncationToleranceSelector().execute(
            request
        )

    def test_request__nonnested_supports__is_rejected(self) -> None:
        """A minimum support is defined only over the declared strict nesting order."""
        comparisons = _comparisons_for_dimension(LatticeDimension.ONE)
        with pytest.raises(ValueError, match="strictly nested"):
            RealSpaceSupportTruncationToleranceSelectionRequest(
                comparisons=(comparisons[1], comparisons[0]),
                tolerance=0.1,
            )

    def test_request__mixed_lattice_dimensions__is_rejected(self) -> None:
        """One ordered support inventory cannot mix lattice dimensions."""
        one_dimensional = _comparisons_for_dimension(LatticeDimension.ONE)[0]
        two_dimensional = _comparisons_for_dimension(LatticeDimension.TWO)[1]
        with pytest.raises(ValueError, match="one lattice dimension"):
            RealSpaceSupportTruncationToleranceSelectionRequest(
                comparisons=(one_dimensional, two_dimensional),
                tolerance=0.1,
            )

    @pytest.mark.parametrize("value", [True, 1, "0.1"])
    def test_errors__nonfloat_scalar__is_rejected(
        self, value: bool | int | str
    ) -> None:
        """Error scalars reject booleans, integers, and numeric strings."""
        with pytest.raises(TypeError, match="built-in float"):
            RankNormalizedMatrixFrobeniusErrors(
                maximum_error=value,  # type: ignore[arg-type]
                root_mean_square_error=0.0,
            )
        with pytest.raises(TypeError, match="built-in float"):
            OrderedEigenvalueErrors(
                maximum_absolute_error=value,  # type: ignore[arg-type]
                root_mean_square_error=0.0,
            )

    @pytest.mark.parametrize("tolerance", [True, 1, "0.1"])
    def test_request__nonfloat_tolerance__is_rejected(
        self, tolerance: bool | int | str
    ) -> None:
        """Booleans, integers, and strings do not enter the tolerance contract."""
        with pytest.raises(TypeError, match="built-in float"):
            RealSpaceSupportTruncationToleranceSelectionRequest(
                comparisons=_comparisons_for_dimension(LatticeDimension.ONE),
                tolerance=tolerance,  # type: ignore[arg-type]
            )
