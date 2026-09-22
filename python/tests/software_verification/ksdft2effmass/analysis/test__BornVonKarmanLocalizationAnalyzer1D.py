r"""Software verification of ``BornVonKarmanLocalizationAnalyzer1D``.

Evidence profile: routine

Bounded artifact scope: isolated-band finite Born--von Karman localization.

Facet and represented meaning

The ActionObject samples a declared plane-wave frame path on a centered supercell.

Intrinsic and cross-object scope

Inverse Bloch transformation, normalization, center, spread, and identity are included.

VVUQ and scientific exclusions

This finite-supercell diagnostic is not scientific validation or a modern-polarization
observable.
"""

import hashlib

import numpy as np
import pytest

from ksdft2effmass.analysis.wannier_localization import (
    BornVonKarmanLocalizationAnalyzer1D,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = BornVonKarmanLocalizationAnalyzer1D


class TestBornVonKarmanLocalizationAnalyzer1D:
    """Own software evidence for ``BornVonKarmanLocalizationAnalyzer1D``."""

    def test_method__execute__matches_closed_form_constant_periodic_parts(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-011

        Requirement: A two-point isolated path with constant periodic parts produces
        the analytical interference density ``(1 + cos(x/2)) / (4 pi)``.

        Acceptance: Density, norm, and center match independent values; SHA-256
        authenticates the retained little-endian density bytes.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        frame = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        path = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.zeros((1, 1)), Unitless()),
            1.0e-14,
        )

        result = BornVonKarmanLocalizationAnalyzer1D().execute(
            path,
            PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 0),
            ScalarQuantity(2.0 * np.pi, Unitless()),
            4,
            1.0e-14,
            1.0e-14,
        )

        expected_density = (1.0 + np.cos(0.5 * result.coordinates.magnitude)) / (
            4.0 * np.pi
        )
        np.testing.assert_allclose(
            result.normalized_density.magnitude, expected_density, atol=1.0e-16
        )
        np.testing.assert_allclose(result.quadrature_norm, 1.0, atol=1.0e-15)
        np.testing.assert_allclose(result.center.magnitude, 0.0, atol=1.0e-15)
        retained_bytes = np.asarray(
            result.normalized_density.magnitude, dtype="<f8"
        ).tobytes(order="C")
        assert (
            result.density_content_sha256 == hashlib.sha256(retained_bytes).hexdigest()
        )
