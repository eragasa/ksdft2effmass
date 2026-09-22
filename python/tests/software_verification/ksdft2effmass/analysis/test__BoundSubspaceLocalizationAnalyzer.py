r"""Software verification of ``BoundSubspaceLocalizationAnalyzer``.

Evidence profile: routine

Bounded artifact scope: gauge-invariant averaged subspace density, core probability,
IPR, and minimum-image axis RMS radii.

Facet and represented meaning

The ActionObject uses the complete bound-subspace column span; unitary mixing within
that span cannot change the reported density-derived metrics.

Intrinsic and cross-object scope

Two occupied basis sites on a three-site periodic ring provide hand-derived values.

VVUQ and scientific exclusions

Spectra are synthetic test data. Metrics do not establish physical localization,
material validation, UQ, campaign execution, or human acceptance.
"""

import math

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.analysis.bound_subspaces import (
    BoundStateProjectorConstructor,
    BoundSubspaceLocalizationAnalyzer,
)
from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartitioner,
)
from ksdft2effmass.analysis.finite_domain_spectra import (
    HostEdgeBoundStateAnalyzer,
    HostEdgeReference,
)
from ksdft2effmass.operators import (
    ComplexHermitianEigenpairResidualAnalyzer,
    ComplexHermitianEigenpairResult,
    ComplexMatrixQuantity,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    HermitianEigenpairSelection,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = BoundSubspaceLocalizationAnalyzer


class TestBoundSubspaceLocalizationAnalyzer:
    """Own software evidence for gauge-invariant localization analysis."""

    def test_method__execute__matches_two_site_subspace_density(self) -> None:
        """Evidence ID: SV-ANALYSIS-BOUND-LOCALIZATION-001

        Requirement: Metrics derive from the normalized projector diagonal rather than
        an arbitrary eigenvector gauge.

        Acceptance: Occupied sites zero and one yield probabilities (1/2,1/2,0), core
        probability 1/2, IPR 1/2, and RMS radius ``1/sqrt(2)``.
        """
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), Unitless()
        )
        eigenpairs = ComplexHermitianEigenpairResult(
            operator,
            ComplexSparseHermiticityAnalyzer().execute(
                operator, absolute_tolerance=0.0
            ),
            VectorQuantity(np.array([-2.0, -1.0, 1.0]), Unitless()),
            ComplexMatrixQuantity(np.eye(3, dtype=np.complex128), Unitless()),
            HermitianEigenpairSelection.LOWEST,
        )
        bound = HostEdgeBoundStateAnalyzer().execute(
            ComplexHermitianEigenpairResidualAnalyzer().execute(
                eigenpairs, absolute_tolerance=0.0
            ),
            HostEdgeReference("edge", ScalarQuantity(0.0, Unitless())),
            ScalarQuantity(0.0, Unitless()),
        )
        projector = BoundStateProjectorConstructor().execute(bound)
        shape = FiniteLatticeShape(LatticeDimension.ONE, (3,))
        partition = MinimumImageChebyshevPartitioner().execute(
            shape,
            LatticeCoordinate(LatticeDimension.ONE, (0,)),
            core_radius=0,
        )

        result = BoundSubspaceLocalizationAnalyzer().execute(projector, partition)

        assert result.site_probabilities is not None
        np.testing.assert_array_equal(
            result.site_probabilities.magnitude, [0.5, 0.5, 0.0]
        )
        assert result.core_probability == 0.5
        assert result.inverse_participation_ratio == 0.5
        assert result.rms_radii == pytest.approx((1.0 / math.sqrt(2.0),))
