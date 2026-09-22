r"""Software verification of ``ComplexMatrixQuantity``.

Evidence profile: routine

Bounded artifact scope: immutable dense complex128 matrix quantities with explicit
units.

Facet and represented meaning

The DataObject retains finite complex values and prevents mutation through caller-owned
arrays or maintained storage.

Intrinsic and cross-object scope

Complex preservation, defensive copying, immutability, and adverse scalar families are
included.

VVUQ and scientific exclusions

This verifies represented storage, not Hermiticity, an operator interpretation,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = ComplexMatrixQuantity


class TestComplexMatrixQuantity:
    """Own software evidence for ``ComplexMatrixQuantity``."""

    def test_constructor__complex_storage__is_exact_and_immutable(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-MATRIX-001

        Requirement: The quantity defensively owns finite complex128 matrix values.

        Acceptance: Complex entries are preserved exactly, source mutation has no
        effect, and maintained storage is not writeable.
        """
        source = np.array([[1.0 + 2.0j, -3.0j], [4.0, -2.0 + 0.5j]])
        expected = source.copy()

        quantity = ComplexMatrixQuantity(source, Unitless())
        source[0, 0] = 99.0

        np.testing.assert_array_equal(quantity.magnitude, expected)
        assert quantity.magnitude.dtype == np.dtype(np.complex128)
        assert not quantity.magnitude.flags.writeable
        with pytest.raises(ValueError, match="cannot set WRITEABLE"):
            quantity.magnitude.setflags(write=True)

    def test_constructor__numeric_boundary__rejects_boolean_and_nonfinite(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-MATRIX-002

        Requirement: Boolean and nonfinite values are rejected rather than coerced.

        Acceptance: Boolean storage raises ``TypeError`` and an infinite imaginary
        component raises ``ValueError``.
        """
        with pytest.raises(TypeError, match="excluding booleans"):
            ComplexMatrixQuantity(np.array([[True]], dtype=np.bool_), Unitless())
        with pytest.raises(ValueError, match="finite complex"):
            ComplexMatrixQuantity(np.array([[1.0 + np.inf * 1.0j]]), Unitless())
