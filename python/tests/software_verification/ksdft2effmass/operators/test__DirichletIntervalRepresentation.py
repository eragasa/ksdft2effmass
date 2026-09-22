r"""Software verification of ``DirichletIntervalRepresentation``.

Evidence profile: routine

Bounded artifact scope: public structural interval input contract for represented
Dirichlet operators.

Facet and represented meaning

The protocol identifies grid and boundary components required by operator construction
while concrete interval ownership remains with model-system analysis.

Intrinsic and cross-object scope

Runtime structural recognition of the public Dirichlet interval is included.

VVUQ and scientific exclusions

This verifies software conformance only, not operator convergence, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)
from ksdft2effmass.operators import DirichletIntervalRepresentation

pytestmark = pytest.mark.software_verification
SUT = DirichletIntervalRepresentation


class TestDirichletIntervalRepresentation:
    """Own software evidence for the operator interval-input protocol."""

    def test_protocol__runtime_contract__accepts_public_dirichlet_interval(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-007

        Requirement: Operator construction consumes a structural interval contract
        without importing the analysis implementation.

        Acceptance: The public DirichletInterval satisfies the runtime protocol and
        exposes conforming grid and boundary components.
        """
        interval = DirichletInterval(
            UniformCartesianGrid1D(
                ScalarQuantity(-1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(0.5, Unitless()),
            ),
            DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
        )

        assert isinstance(interval, DirichletIntervalRepresentation)
        assert interval.grid.interior_point_count == 3
        assert interval.boundary_condition.condition_kind == "dirichlet"
