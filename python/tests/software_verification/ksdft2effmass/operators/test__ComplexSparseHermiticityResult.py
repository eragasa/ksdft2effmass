r"""Software verification of ``ComplexSparseHermiticityResult``.

Evidence profile: routine

Bounded artifact scope: immutable sparse complex Hermiticity outcomes.

Facet and represented meaning

The ResultObject retains the exact matrix, residual, tolerance, unit, and inclusive
acceptance status.

Intrinsic and cross-object scope

Unit retention, inclusive acceptance, and scalar invariant rejection are included.

VVUQ and scientific exclusions

This verifies result-state consistency, not correctness of an analyzer invocation,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexSparseHermiticityResult,
    ComplexSparseMatrixQuantity,
    PhysicalUnit,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexSparseHermiticityResult


class TestComplexSparseHermiticityResult:
    """Own software evidence for ``ComplexSparseHermiticityResult``."""

    def test_constructor__scalars__retains_unit_and_inclusive_status(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-SPARSE-HERMITICITY-003

        Requirement: Residual and tolerance share the matrix unit and use inclusive
        acceptance.

        Acceptance: Equal residual and tolerance are accepted in electron volts.
        """
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0 + 0.0j]])),
            PhysicalUnit("electron_volt"),
        )

        result = ComplexSparseHermiticityResult(matrix, 1.0e-12, 1.0e-12)

        assert result.is_hermitian
        assert result.unit == PhysicalUnit("electron_volt")

    def test_constructor__scalars__rejects_negative_or_nonfinite_values(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-SPARSE-HERMITICITY-004

        Requirement: Result scalars are finite nonnegative built-in floats.

        Acceptance: Negative residual and infinite tolerance each raise ``ValueError``.
        """
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0 + 0.0j]])),
            PhysicalUnit("electron_volt"),
        )

        with pytest.raises(ValueError, match="finite and nonnegative"):
            ComplexSparseHermiticityResult(matrix, -1.0, 0.0)
        with pytest.raises(ValueError, match="finite and nonnegative"):
            ComplexSparseHermiticityResult(matrix, 0.0, float("inf"))
