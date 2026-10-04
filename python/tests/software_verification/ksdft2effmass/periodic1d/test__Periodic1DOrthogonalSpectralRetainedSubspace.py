"""Software verification of ``Periodic1DOrthogonalSpectralRetainedSubspace``.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The class binds one numerical orthonormal eigenspace representation to an identified
one-dimensional scientific retained space.

Intrinsic and cross-object scope
--------------------------------
Exact type, parent dimension, retained rank, and ambient-dimension agreement are
covered.

VVUQ and scientific exclusions
------------------------------
Synthetic matrices establish software compatibility only, not numerical verification,
parent alignment, scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import (
    MatrixQuantity,
    OrthogonalSpectralSubspace,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.periodic import (
    PeriodicOperatorReference,
    PeriodicRetainedSubspace,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)
from ksdft2effmass.periodic1d import Periodic1DOrthogonalSpectralRetainedSubspace

pytestmark = pytest.mark.software_verification


class TestPeriodic1DOrthogonalSpectralRetainedSubspace:
    """Own compatibility evidence for represented spectral retained spaces."""

    @staticmethod
    def make_retained_subspace(ambient_dimension: int = 3) -> PeriodicRetainedSubspace:
        """Return one synthetic rank-two retained-space identity."""
        definition = PeriodicRetentionDefinition(
            "retention",
            PeriodicOperatorReference("parent", "operator", "ambient", 1),
            "retained",
            PeriodicRetentionKind.SPECTRAL_RESTRICTION,
            2,
            ("state-0", "state-1"),
            "domain",
            "construction",
            (),
            "provenance",
        )
        return PeriodicRetainedSubspace(
            definition,
            "ambient",
            ambient_dimension,
            "spinless",
            "scalar",
            "periodic-sewing",
            "subspace-provenance",
        )

    @staticmethod
    def make_representation() -> OrthogonalSpectralSubspace:
        """Return one synthetic three-by-two orthonormal eigenspace."""
        return OrthogonalSpectralSubspace(
            VectorQuantity(np.asarray([1.0, 2.0]), Unitless()),
            MatrixQuantity(
                np.asarray(((1.0, 0.0), (0.0, 1.0), (0.0, 0.0))), Unitless()
            ),
        )

    def test_construction__dimensions__binds_matching_scientific_and_numerical_spaces(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-SPECTRAL-SUBSPACE-001

        Requirement: Scientific rank and ambient dimension agree exactly with the
        numerical orthonormal eigenspace representation.

        Acceptance: Construction preserves both exact input objects.
        """
        retained = self.make_retained_subspace()
        represented = self.make_representation()
        result = Periodic1DOrthogonalSpectralRetainedSubspace(retained, represented)
        assert result.retained_subspace is retained
        assert result.represented_subspace is represented

    def test_construction__ambient_dimension__rejects_mismatch(self) -> None:
        """Evidence ID: SV-PERIODIC1D-SPECTRAL-SUBSPACE-002

        Requirement: The represented embedding acts in the declared ambient dimension.

        Acceptance: Dimension disagreement raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="ambient dimensions must agree"):
            Periodic1DOrthogonalSpectralRetainedSubspace(
                self.make_retained_subspace(4), self.make_representation()
            )
