r"""Software verification of ``Wannier90ProjectionFileWriter``.

Evidence profile: claim_bearing

Bounded artifact scope: deterministic writing of complete Wannier90 ``.amn`` tables.

Facet and represented meaning

The ActionObject writes ordered complex band-by-projection matrices at each reciprocal
point using native one-based indices.

Intrinsic and cross-object scope

Indexed text writing is included; projection generation and execution are excluded.

VVUQ and scientific exclusions

Round-trip agreement is software verification, not localization validation,
uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.integration.wannier90 import (
    Wannier90ProjectionData,
    Wannier90ProjectionFileWriter,
    Wannier90ProjectionParser,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = Wannier90ProjectionFileWriter


class TestWannier90ProjectionFileWriter:
    """Own deterministic ``.amn`` writer evidence."""

    def test_method__execute__round_trips_complete_complex_projections(self) -> None:
        """Evidence ID: SV-INTEGRATION-WANNIER90-018

        Requirement: Every band, projection, and reciprocal-point entry is retained.

        Method: Write one complex two-band matrix and parse the resulting bytes.

        Oracle: The existing parser independently reconstructs the indexed matrix.

        Acceptance: The comment and dimensions are exact and the matrix round trips.

        Interpretation: A pass verifies native ordering and complex-value writing.

        Limitations: The authored projection is not a localization result.
        """

        matrix = np.asarray([[1.0 + 0.5j, 2.0], [3.0j, 4.0 - 0.25j]])
        data = Wannier90ProjectionData((ComplexMatrixQuantity(matrix, Unitless()),))

        text = SUT().execute(data, "authored projection fixture")
        reconstructed = Wannier90ProjectionParser().execute(text.encode())

        assert text.splitlines()[:2] == [
            "authored projection fixture",
            "           2           1           2",
        ]
        np.testing.assert_array_equal(reconstructed.matrices[0].magnitude, matrix)
