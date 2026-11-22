"""Synthetic conditional-error bounds, not silicon convergence or verification."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from itertools import product
from math import ulp

import numpy as np
import pytest
from common_space.verification.native_precision import (
    CommonSpaceMatrixUncertainty,
    CommonSpaceNativeRoundingModel,
    CommonSpaceOverlapUncertainty,
)
from projectkoios.physkit.units.quantities import (
    ComplexMatrixQuantity,
    PhysicalUnit,
    Unitless,
)

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestCommonSpaceNativePrecisionBounds:
    """Keep native rounding, binary conversion, and mixed product terms explicit."""

    def test_nearest_decimal_model__uses_exact_absolute_component_errors(self) -> None:
        model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
            amn=12, gauge=10, disentanglement=0
        )

        assert model.amn_component_error == Fraction(1, 2 * 10**12)
        assert model.gauge_component_error == Fraction(1, 2 * 10**10)
        assert model.disentanglement_component_error == Fraction(1, 2)

    def test_large_declared_precision__does_not_underflow_to_zero(self) -> None:
        model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
            amn=4096, gauge=4096, disentanglement=4096
        )

        assert model.amn_component_error == Fraction(1, 2 * 10**4096)
        assert model.amn_component_error > 0

    @pytest.mark.parametrize("places", (True, "12", -1, 1.0))
    def test_decimal_count__rejects_booleans_strings_and_noninteger_values(
        self, places: int | str | float
    ) -> None:
        with pytest.raises(ValueError, match="nonnegative built-in integers"):
            CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
                amn=places,  # type: ignore[arg-type]
                gauge=10,
                disentanglement=10,
            )

    @pytest.mark.parametrize("value", (True, "0", 0.0, Fraction(-1)))
    def test_component_bound__requires_nonnegative_exact_fraction(
        self, value: Fraction | str | float
    ) -> None:
        with pytest.raises(ValueError, match="nonnegative built-in Fractions"):
            CommonSpaceNativeRoundingModel(
                amn_component_error=value,  # type: ignore[arg-type]
                gauge_component_error=Fraction(0),
                disentanglement_component_error=Fraction(0),
            )

    @pytest.mark.parametrize("value", (0j, 3 + 4j, complex(2.0**-1074), 1e308 + 0j))
    def test_matrix_profile__bounds_scalar_norm_and_binary64_rounding(
        self, value: complex
    ) -> None:
        matrix = ComplexMatrixQuantity(
            np.asarray(((value,),), dtype=np.complex128), Unitless()
        )
        bound = CommonSpaceMatrixUncertainty.from_parsed_matrix(
            matrix=matrix, native_component_error=Fraction(1, 1000)
        )
        exact_squared = (
            Fraction.from_float(value.real) ** 2 + Fraction.from_float(value.imag) ** 2
        )
        parsing_squared = (Fraction.from_float(ulp(value.real)) / 2) ** 2 + (
            Fraction.from_float(ulp(value.imag)) / 2
        ) ** 2

        assert (bound.row_count, bound.column_count) == (1, 1)
        assert bound.nominal_norm_bound**2 >= exact_squared
        assert bound.parsing_error_bound**2 >= parsing_squared
        assert bound.parsing_error_bound > 0
        assert bound.native_error_bound**2 >= Fraction(2, 1000**2)
        if value == 3 + 4j:
            assert bound.nominal_norm_bound == 5

    @pytest.mark.parametrize("value", (True, "0", 0.0, Fraction(-1)))
    def test_matrix_component_bound__does_not_coerce_invalid_scalars(
        self, value: Fraction | str | float
    ) -> None:
        matrix = ComplexMatrixQuantity(np.ones((1, 1), dtype=np.complex128), Unitless())
        with pytest.raises(ValueError, match="nonnegative built-in Fraction"):
            CommonSpaceMatrixUncertainty.from_parsed_matrix(
                matrix=matrix,
                native_component_error=value,  # type: ignore[arg-type]
            )

    def test_zero_matrix__retains_subnormal_conversion_error_bound(self) -> None:
        matrix = ComplexMatrixQuantity(
            np.zeros((1, 1), dtype=np.complex128), Unitless()
        )
        bound = CommonSpaceMatrixUncertainty.from_parsed_matrix(
            matrix=matrix, native_component_error=Fraction(0)
        )

        assert bound.nominal_norm_bound == 0
        assert bound.native_error_bound == 0
        assert bound.parsing_error_bound**2 >= 2 * Fraction(1, 2**1075) ** 2
        assert bound.parsing_error_bound > 0

    def test_rectangular_profile__does_not_assume_disentanglement_isometry(
        self,
    ) -> None:
        matrix = ComplexMatrixQuantity(
            np.asarray(((1, 0), (0, 1), (1j, 0)), dtype=np.complex128), Unitless()
        )
        bound = CommonSpaceMatrixUncertainty.from_parsed_matrix(
            matrix=matrix, native_component_error=Fraction(0)
        )

        assert (bound.row_count, bound.column_count) == (3, 2)
        assert bound.nominal_norm_bound == 2  # Conservative ceil(sqrt(2)), not 1.
        assert bound.native_error_bound == 0

    def test_nonunitless_matrix__cannot_enter_overlap_error_propagation(self) -> None:
        matrix = ComplexMatrixQuantity(
            np.ones((1, 1), dtype=np.complex128), PhysicalUnit("electron_volt")
        )
        with pytest.raises(TypeError, match="unitless ComplexMatrixQuantity"):
            CommonSpaceMatrixUncertainty.from_parsed_matrix(
                matrix=matrix, native_component_error=Fraction(0)
            )

    def test_product_partition__retains_native_parse_mixed_terms(self) -> None:
        matrix = CommonSpaceMatrixUncertainty(
            row_count=1,
            column_count=1,
            nominal_norm_bound=Fraction(1),
            parsing_error_bound=Fraction(1, 100),
            native_error_bound=Fraction(1, 10),
        )
        bounds = CommonSpaceOverlapUncertainty(
            amn=matrix, gauge=matrix, disentanglement=matrix
        )

        assert bounds.parsing_error_bound == Fraction(30301, 10**6)
        assert bounds.native_error_bound == Fraction(33733, 10**5)
        assert bounds.combined_error_bound == Fraction(367631, 10**6)
        assert (
            bounds.combined_error_bound
            == bounds.parsing_error_bound + bounds.native_error_bound
        )
        native_only = Fraction(11, 10) ** 3 - 1
        assert bounds.combined_error_bound > native_only + bounds.parsing_error_bound

    def test_scalar_corner_perturbations__stay_within_separate_and_total_bounds(
        self,
    ) -> None:
        profile = CommonSpaceMatrixUncertainty(
            row_count=1,
            column_count=1,
            nominal_norm_bound=Fraction(1),
            parsing_error_bound=Fraction(1, 100),
            native_error_bound=Fraction(1, 10),
        )
        bounds = CommonSpaceOverlapUncertainty(
            amn=profile, gauge=profile, disentanglement=profile
        )
        for signs in product((-1, 1), repeat=6):
            decimal = tuple(Fraction(1) + Fraction(sign, 100) for sign in signs[:3])
            native = tuple(
                value + Fraction(sign, 10)
                for value, sign in zip(decimal, signs[3:], strict=True)
            )
            decimal_product = decimal[0] * decimal[1] * decimal[2]
            native_product = native[0] * native[1] * native[2]
            assert abs(decimal_product - 1) <= bounds.parsing_error_bound
            assert abs(native_product - decimal_product) <= bounds.native_error_bound
            assert abs(native_product - 1) <= bounds.combined_error_bound

    def test_profile_shapes__must_support_the_declared_overlap_product(self) -> None:
        profile = CommonSpaceMatrixUncertainty(
            row_count=1,
            column_count=1,
            nominal_norm_bound=Fraction(1),
            parsing_error_bound=Fraction(0),
            native_error_bound=Fraction(0),
        )
        with pytest.raises(ValueError, match="dimensions do not correlate"):
            CommonSpaceOverlapUncertainty(
                amn=profile,
                gauge=replace(profile, column_count=2),
                disentanglement=profile,
            )
        with pytest.raises(ValueError, match="positive built-in integers"):
            replace(profile, row_count=True)
        with pytest.raises(ValueError, match="nonnegative built-in Fractions"):
            replace(profile, nominal_norm_bound=1.0)  # type: ignore[arg-type]

    def test_error_records__are_operationally_immutable(self) -> None:
        model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
            amn=12, gauge=10, disentanglement=10
        )
        with pytest.raises(FrozenInstanceError):
            model.amn_component_error = Fraction(0)  # type: ignore[misc]
