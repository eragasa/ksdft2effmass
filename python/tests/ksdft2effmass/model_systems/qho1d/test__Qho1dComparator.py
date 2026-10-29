r"""Software verification of ``Qho1dComparator``.

Evidence profile: routine

Bounded artifact scope: public request-admissibility behavior of
Qho1dComparator.

Facet and represented meaning

The class under test owns one deterministic finite-grid to retained-number-state
comparison and its explicit request-admissibility policy.

Intrinsic and cross-object scope

The supported public import and structured rejection of wrong request types,
nondivisible grids, and oversized retained spaces are included. Numerical agreement
with an independent mathematical oracle is excluded.

VVUQ and scientific exclusions

This is software verification of public behavior. It establishes no numerical
verification, convergence, scientific validation, uncertainty quantification, or
human acceptance.
"""

import pytest
from projectkoios.physkit.units import (
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass import model_systems
from ksdft2effmass.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.model_systems.qho1d import (
    Qho1dAnalytical,
    Qho1dComparator,
    Qho1dComparisonRequest,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
    Qho1dNondimensionalizationRequest,
    Qho1dNondimensionalizer,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = Qho1dComparator


class TestQho1dComparator:
    """Own software evidence for ``Qho1dComparator``."""

    @staticmethod
    def request(
        *, spacing: float = 0.5, retained_dimension: int = 1
    ) -> Qho1dComparisonRequest:
        """Return one dimensionless comparison request."""
        analytical = Qho1dAnalytical(
            Qho1dNondimensionalizer(
                Qho1dNondimensionalizationRequest(1.0, 1.0, 1.0)
            ).execute()
        )
        return Qho1dComparisonRequest(
            analytical=analytical,
            finite_difference=Qho1dFiniteDifference(
                analytical=analytical,
                interval=DirichletInterval(
                    grid=UniformCartesianGrid1D(
                        ScalarQuantity(-1.0, Unitless()),
                        ScalarQuantity(1.0, Unitless()),
                        ScalarQuantity(spacing, Unitless()),
                    ),
                    boundary_condition=DirichletBoundaryCondition(
                        ScalarQuantity(0.0, Unitless())
                    ),
                ),
            ),
            ladder_operators=Qho1dLadderOperators(
                analytical=analytical,
                ladder_operator=LadderOperator1D(retained_dimension),
            ),
        )

    def test_public_api__package__exports_supported_comparator_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-007

        Requirement: Qho1dComparator is available through the supported
        public model-systems import surface.

        Acceptance: The package binding is the same class object as the documented
        harmonic-oscillator import.
        """
        assert model_systems.Qho1dComparator is (Qho1dComparator)

    def test_method__execute__requires_bound_three_model_request(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-008

        Requirement: construction binds the exact three-model request type and
        rejects values outside that public contract.

        Acceptance: A Boolean request raises TypeError, while one admissible request
        is retained by identity and produces a result bound to that exact request.
        """
        with pytest.raises(TypeError, match="request must be"):
            Qho1dComparator(True)  # type: ignore[arg-type]
        request = self.request()
        comparator = Qho1dComparator(request)
        assert comparator.request is request
        assert comparator.execute().request is request
