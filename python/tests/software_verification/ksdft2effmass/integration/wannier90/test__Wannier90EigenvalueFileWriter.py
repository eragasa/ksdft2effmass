r"""Software verification of ``Wannier90EigenvalueFileWriter``.

Evidence profile: claim_bearing

Bounded artifact scope: deterministic writing of complete Wannier90 ``.eig`` tables.

Facet and represented meaning

The ActionObject writes one-based native indices for an ordered k-point-by-band energy
table while the typed record retains its explicit energy unit.

Intrinsic and cross-object scope

Indexed text writing is included; energy conversion and execution are excluded.

VVUQ and scientific exclusions

Round-trip agreement is software verification, not numerical or scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.integration.wannier90 import (
    Wannier90EigenvalueData,
    Wannier90EigenvalueFileWriter,
    Wannier90EigenvalueParser,
)
from ksdft2effmass.operators import MatrixQuantity, PhysicalUnit

pytestmark = pytest.mark.software_verification
SUT = Wannier90EigenvalueFileWriter


class TestWannier90EigenvalueFileWriter:
    """Own deterministic ``.eig`` writer evidence."""

    def test_method__execute__round_trips_complete_indexed_table(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-017

        Requirement: Every energy is written once in k-point-major, band-minor order.

        Method: Write a two-by-two table and parse the resulting bytes independently.

        Oracle: The existing parser reconstructs native one-based indices directly.

        Acceptance: Parsed magnitudes and the exact deterministic text agree.

        Interpretation: A pass verifies indexed writing and parser compatibility.

        Limitations: No energy-unit conversion or Wannier90 execution is performed.
        """

        unit = PhysicalUnit("eV")
        data = Wannier90EigenvalueData(
            MatrixQuantity(np.asarray([[1.0, 2.0], [3.0, 4.0]]), unit)
        )

        text = SUT().execute(data)
        reconstructed = Wannier90EigenvalueParser().execute(text.encode(), unit)

        assert text == (
            "    1     1 1.0000000000000000e+00\n"
            "    2     1 2.0000000000000000e+00\n"
            "    1     2 3.0000000000000000e+00\n"
            "    2     2 4.0000000000000000e+00\n"
        )
        np.testing.assert_array_equal(
            reconstructed.eigenvalues.magnitude, data.eigenvalues.magnitude
        )
