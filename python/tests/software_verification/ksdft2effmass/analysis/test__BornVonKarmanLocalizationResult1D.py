r"""Software verification of ``BornVonKarmanLocalizationResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated finite Born--von Karman localization results.

Facet and represented meaning

The ResultObject retains sampled density, normalization, center, spread, and units.

Intrinsic and cross-object scope

Density normalization and derived-scalar correlation are included.

VVUQ and scientific exclusions

Result consistency is not physical localization validation or uncertainty evidence.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.wannier_localization import (
    BornVonKarmanLocalizationAnalyzer1D,
    BornVonKarmanLocalizationResult1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    ReciprocalBandFramePath1D,
)

pytestmark = pytest.mark.software_verification
SUT = BornVonKarmanLocalizationResult1D


class TestBornVonKarmanLocalizationResult1D:
    """Own software evidence for ``BornVonKarmanLocalizationResult1D``."""

    def test_constructor__normalization__rejects_unnormalized_density(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-012

        Requirement: Retained density integrates to one under the declared quadrature.

        Acceptance: Doubling a valid density raises ``ValueError``.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 2)
        frame = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        path = ReciprocalBandFramePath1D(
            mesh,
            (frame, frame),
            ComplexMatrixQuantity(np.zeros((1, 1)), Unitless()),
            1.0e-14,
        )
        valid = BornVonKarmanLocalizationAnalyzer1D().execute(
            path,
            PlaneWaveBasis1D(ScalarQuantity(1.0, Unitless()), 0),
            ScalarQuantity(2.0 * np.pi, Unitless()),
            4,
            1.0e-14,
            1.0e-14,
        )

        with pytest.raises(ValueError, match="normalization tolerance"):
            BornVonKarmanLocalizationResult1D(
                valid.source,
                valid.basis,
                valid.period,
                valid.samples_per_cell,
                valid.coordinates,
                VectorQuantity(
                    2.0 * valid.normalized_density.magnitude,
                    valid.normalized_density.unit,
                ),
                valid.quadrature_norm,
                valid.center,
                valid.spread,
                valid.normalization_absolute_tolerance,
            )
