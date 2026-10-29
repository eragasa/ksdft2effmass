r"""Software verification of centered even-mesh cyclic conversion.

Evidence profile: routine

The tests establish the reusable represented-hopping conversion contract only. They do
not establish scientific validity, retained evidence, or material applicability.
"""

import numpy as np
import pytest
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.solidstate import (
    BlockHoppingModel1D,
    CenteredEvenMeshCyclicToOrdinaryConverter1D,
    CenteredEvenMeshCyclicToOrdinaryRequest1D,
)

pytestmark = pytest.mark.software_verification
SUT = CenteredEvenMeshCyclicToOrdinaryConverter1D


class TestCenteredEvenMeshCyclicToOrdinaryConverter1D:
    """Verify explicit negative-Nyquist removal and conversion accounting."""

    def test_method__execute__separates_negative_nyquist_from_ordinary_support(
        self,
    ) -> None:
        """The converter removes only ``-N/2`` and reports its normalized power."""
        period = ScalarQuantity(1.0, Unitless())
        blocks = tuple(
            ComplexMatrixQuantity(
                np.asarray(
                    [[value, 0.0], [0.0, -value]],
                    dtype=np.complex128,
                ),
                Unitless(),
            )
            for value in (2.0, 0.5, 1.0, 0.5)
        )
        source = BlockHoppingModel1D(period, (-2, -1, 0, 1), blocks)
        request = CenteredEvenMeshCyclicToOrdinaryRequest1D(source)
        converter = SUT(request)

        result = converter.execute()

        assert converter.request is request
        assert result.source is source
        assert result.conversion_representative == -2
        assert result.ordinary.reciprocal_period is period
        assert result.ordinary.representatives == (-1, 0, 1)
        assert all(
            retained is original
            for retained, original in zip(
                result.ordinary.hopping_blocks,
                blocks[1:],
                strict=True,
            )
        )
        np.testing.assert_allclose(
            result.conversion_power_per_matrix_dimension,
            4.0,
            rtol=0.0,
            atol=np.finfo(np.float64).eps * 4.0,
        )

    def test_class__init__rejects_odd_representative_inventory(self) -> None:
        """An odd mesh has no unique negative-Nyquist conversion class."""
        unit = Unitless()
        block = ComplexMatrixQuantity(np.asarray([[1.0]], dtype=np.complex128), unit)
        source = BlockHoppingModel1D(
            ScalarQuantity(1.0, unit),
            (-1, 0, 1),
            (block, block, block),
        )

        with pytest.raises(ValueError, match="even representative count"):
            CenteredEvenMeshCyclicToOrdinaryRequest1D(source)

    def test_class__init__rejects_incomplete_centered_inventory(self) -> None:
        """Conversion does not guess a missing or shifted cyclic representative."""
        unit = Unitless()
        block = ComplexMatrixQuantity(np.asarray([[1.0]], dtype=np.complex128), unit)
        source = BlockHoppingModel1D(
            ScalarQuantity(1.0, unit),
            (0, 1),
            (block, block),
        )

        with pytest.raises(ValueError, match="complete centered"):
            CenteredEvenMeshCyclicToOrdinaryRequest1D(source)
