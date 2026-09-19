r"""Software verification of ``PintUnitConverter``.

Evidence profile: routine

Bounded artifact scope: public PintUnitConverter represented software contract.

Facet and represented meaning

The class under test owns the declared public PintUnitConverter contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This is software verification of unit representation or conversion behavior. It
establishes no numerical convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    PhysicalUnit,
    PintUnitConverter,
    ScalarQuantity,
    SparseMatrixQuantity,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = PintUnitConverter


class TestPintUnitConverter:
    """Own software evidence for ``PintUnitConverter``."""

    def test_method__convert_scalar__uses_pint_dimensions_and_scale(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-006

        Requirement: Unit conversion and dimensional compatibility are delegated to
        Pint rather than a project-owned unit algebra.

        Acceptance: The public export is exact, 100 centimeters converts to one meter,
        and length-to-energy conversion is rejected.
        """
        assert model_systems.PintUnitConverter is PintUnitConverter
        converter = PintUnitConverter()
        converted = converter.convert_scalar(
            ScalarQuantity(100.0, PhysicalUnit("centimeter")),
            PhysicalUnit("meter"),
        )
        assert converted == ScalarQuantity(1.0, PhysicalUnit("meter"))
        with pytest.raises(ValueError, match="incompatible"):
            converter.convert_scalar(
                ScalarQuantity(1.0, PhysicalUnit("meter")),
                PhysicalUnit("joule"),
            )

    def test_method__convert_sparse_matrix__preserves_csr_structure(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-007

        Requirement: Unit conversion scales sparse matrix values without changing
        shape, stored positions, or sparse ownership.

        Acceptance: A centimeter diagonal converts to meters with the same two stored
        entries and no dense intermediate in the returned quantity.
        """
        source = SparseMatrixQuantity.from_csr(
            sparse.diags([100.0, 200.0], offsets=0, format="csr"),
            PhysicalUnit("centimeter"),
        )

        converted = PintUnitConverter().convert_sparse_matrix(
            source, PhysicalUnit("meter")
        )

        assert converted.shape == (2, 2)
        assert converted.nonzero_count == 2
        np.testing.assert_array_equal(converted.data, [1.0, 2.0])

    def test_method__convert_complex_matrix__preserves_complex_values(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-008

        Requirement: Pint-backed dense conversion scales complex matrix values without
        erasing imaginary components.

        Acceptance: One complex centimeter value converts to meters with both
        components scaled by ``0.01``.
        """
        source = ComplexMatrixQuantity(
            np.array([[100.0 + 200.0j]]), PhysicalUnit("centimeter")
        )

        converted = PintUnitConverter().convert_complex_matrix(
            source, PhysicalUnit("meter")
        )

        np.testing.assert_array_equal(converted.magnitude, [[1.0 + 2.0j]])

    def test_method__convert_complex_sparse_matrix__preserves_complex_values(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-009

        Requirement: Pint-backed sparse conversion scales complex values without
        erasing imaginary components or changing sparse ownership.

        Acceptance: One stored complex centimeter value converts to meters with both
        components scaled by ``0.01`` and one stored position retained.
        """
        source = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array([[100.0 + 200.0j]]), PhysicalUnit("centimeter")
        )

        converted = PintUnitConverter().convert_complex_sparse_matrix(
            source, PhysicalUnit("meter")
        )

        np.testing.assert_array_equal(converted.data, [1.0 + 2.0j])
        assert converted.nonzero_count == 1
