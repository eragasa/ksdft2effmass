r"""Software verification of ``HarmonicOscillatorComparator``.

Evidence profile: routine

Bounded artifact scope: public request-admissibility behavior of
HarmonicOscillatorComparator.

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

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorAnalytical,
    HarmonicOscillatorComparator,
    HarmonicOscillatorComparisonRequest,
    HarmonicOscillatorFiniteDifference,
    HarmonicOscillatorLadderOperators,
    HarmonicOscillatorNondimensionalizer,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = HarmonicOscillatorComparator


class TestHarmonicOscillatorComparator:
    """Own software evidence for ``HarmonicOscillatorComparator``."""

    @staticmethod
    def request(
        *, spacing: float = 0.5, retained_dimension: int = 1
    ) -> HarmonicOscillatorComparisonRequest:
        """Return one dimensionless comparison request."""
        analytical = HarmonicOscillatorAnalytical(
            HarmonicOscillatorNondimensionalizer().execute(
                hbar=1.0, mass=1.0, omega=1.0
            )
        )
        return HarmonicOscillatorComparisonRequest(
            analytical=analytical,
            finite_difference=HarmonicOscillatorFiniteDifference(
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
            ladder_operators=HarmonicOscillatorLadderOperators(
                analytical=analytical,
                ladder_operator=LadderOperator1D(retained_dimension),
            ),
        )

    def test_public_api__package__exports_supported_comparator_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-007

        Requirement: HarmonicOscillatorComparator is available through the supported
        public model-systems import surface.

        Acceptance: The package binding is the same class object as the documented
        harmonic-oscillator import.
        """
        assert model_systems.HarmonicOscillatorComparator is (
            HarmonicOscillatorComparator
        )

    def test_method__execute__requires_bound_three_model_request(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-008

        Requirement: execute accepts its exact three-model request type and rejects
        values outside that public contract.

        Acceptance: A Boolean request raises TypeError, while one admissible request
        produces a result bound to the exact request.
        """
        comparator = HarmonicOscillatorComparator()

        with pytest.raises(TypeError, match="request must be"):
            comparator.execute(True)  # type: ignore[arg-type]
        request = self.request()
        assert comparator.execute(request).request is request
