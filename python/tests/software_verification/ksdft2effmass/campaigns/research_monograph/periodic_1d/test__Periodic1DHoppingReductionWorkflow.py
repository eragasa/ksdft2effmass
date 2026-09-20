r"""Software verification of ``Periodic1DHoppingReductionWorkflow``.

Evidence profile: routine

Bounded artifact scope: execution-independent periodic-1D reduction orchestration.

Facet and represented meaning

The Workflow composes complete transform, truncation, fit, Parseval, and comparisons.

Intrinsic and cross-object scope

Distinct lower-layer ResultObjects are retained without filesystem or external tools.

VVUQ and scientific exclusions

This synthetic check is not a rerun or scientific validation of Appendix G.
"""

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DHoppingReductionRequest,
    Periodic1DHoppingReductionWorkflow,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorSamples1D,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DHoppingReductionWorkflow


class TestPeriodic1DHoppingReductionWorkflow:
    """Own software evidence for the versioned reduction Workflow."""

    def test_method__execute__retains_distinct_reduction_routes(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-001

        Requirement: One request produces separate complete, truncated, fitted,
        Parseval, and comparison outcomes.

        Acceptance: An exact nearest-neighbor series reconstructs and fits within
        binary64 tolerance while all outcomes remain separately addressable.
        """
        mesh = CenteredUniformReciprocalMesh1D(ScalarQuantity(1.0, Unitless()), 4)
        values = 2.0 + np.cos(2.0 * np.pi * mesh.coordinates.magnitude)
        source = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            mesh.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(np.asarray([[value]]), Unitless())
                for value in values
            ),
        )
        request = Periodic1DHoppingReductionRequest(
            source,
            mesh,
            1,
            (-2, -1, 0, 1),
            VectorQuantity(np.ones(4), Unitless()),
            VectorQuantity(np.linspace(-0.5, 0.5, 9), Unitless()),
            0.0,
            1.0e-14,
            ScalarQuantity(1.0e-14, Unitless()),
        )

        result = SUT().execute(request)

        assert result.transform.reconstruction_maximum_frobenius_error <= 1.0e-14
        assert result.fit.is_identified
        assert result.parseval.passes
        assert result.complete_vs_fit.sampled_l2_frobenius_defect.magnitude < 1.0e-13
