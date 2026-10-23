r"""Software verification of ``RealMatrixQuantity``.

Evidence profile: routine

Bounded artifact scope: public RealMatrixQuantity represented software contract.

Facet and represented meaning

The class under test owns the declared public RealMatrixQuantity contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This is software verification of unit representation or conversion behavior. It
establishes no numerical convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass import linalg
from ksdft2effmass.linalg import PhysicalUnit, RealMatrixQuantity

pytestmark = pytest.mark.software_verification
SUT = RealMatrixQuantity


class TestRealMatrixQuantity:
    """Own software evidence for ``RealMatrixQuantity``."""

    def test_constructor__matrix__copies_to_immutable_binary64_storage(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-005

        Requirement: RealMatrixQuantity owns finite immutable binary64 matrix storage
        and an explicit unit.

        Acceptance: The public export is exact, source mutation cannot alter the
        record, and the physical unit remains attached.
        """
        assert linalg.RealMatrixQuantity is RealMatrixQuantity
        source = np.eye(2)
        quantity = RealMatrixQuantity(source, PhysicalUnit("joule"))
        source[0, 0] = 2.0
        np.testing.assert_array_equal(quantity.magnitude, np.eye(2))
        assert quantity.unit == PhysicalUnit("joule")
        assert not quantity.magnitude.flags.writeable
