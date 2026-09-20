r"""Software verification of ``DirichletBoundaryConditionRepresentation``.

Evidence profile: routine

Bounded artifact scope: public structural homogeneous-Dirichlet input contract.

Facet and represented meaning

The protocol identifies boundary kind and homogeneity required by the represented
finite-difference Laplacian without transferring boundary ownership to operators.

Intrinsic and cross-object scope

Runtime structural recognition of the public Dirichlet boundary DataObject is
included.

VVUQ and scientific exclusions

This verifies software conformance only, not boundary-model adequacy, convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import DirichletBoundaryConditionRepresentation

pytestmark = pytest.mark.software_verification
SUT = DirichletBoundaryConditionRepresentation


class TestDirichletBoundaryConditionRepresentation:
    """Own software evidence for the operator boundary-input protocol."""

    def test_protocol__runtime_contract__accepts_public_dirichlet_condition(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-006

        Requirement: Laplacian construction depends on structural Dirichlet metadata
        while the concrete boundary DataObject remains analysis-owned.

        Acceptance: The public homogeneous Dirichlet condition satisfies the runtime
        protocol and reports exact kind ``dirichlet`` and homogeneous state.
        """
        condition = DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless()))

        assert isinstance(condition, DirichletBoundaryConditionRepresentation)
        assert condition.condition_kind == "dirichlet"
        assert condition.is_homogeneous
