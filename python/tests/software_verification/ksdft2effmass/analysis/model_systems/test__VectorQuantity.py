r"""Software verification of ``VectorQuantity``.

Evidence profile: routine

Bounded artifact scope: public VectorQuantity represented software contract.

Facet and represented meaning

The class under test owns the declared public VectorQuantity contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This is software verification of unit representation or conversion behavior. It
establishes no numerical convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import Unitless, VectorQuantity

pytestmark = pytest.mark.software_verification
SUT = VectorQuantity


class TestVectorQuantity:
    """Own software evidence for ``VectorQuantity``."""

    def test_constructor__vector__copies_to_immutable_binary64_storage(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-004

        Requirement: VectorQuantity owns finite immutable binary64 vector storage and
        an explicit unit.

        Acceptance: The public export is exact, source mutation cannot alter the
        record, and direct record-array mutation is rejected.
        """
        assert model_systems.VectorQuantity is VectorQuantity
        source = np.array([1.0, 2.0])
        quantity = VectorQuantity(source, Unitless())
        source[0] = 3.0
        np.testing.assert_array_equal(quantity.magnitude, [1.0, 2.0])
        with pytest.raises(ValueError, match="read-only"):
            quantity.magnitude[0] = 4.0
