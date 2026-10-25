r"""Software verification of ``Qho1dComparisonResult``.

Evidence profile: routine

Bounded artifact scope: immutable array fields of Qho1dComparisonResult.

Facet and represented meaning

The class under test records one finite-grid injection, common-coordinate operators,
signed difference, and numerical diagnostics for a harmonic-oscillator comparison.

Intrinsic and cross-object scope

The exact public import, binary64 canonicalization, contract-derived array shapes, and
operational array immutability are included. The comparator is used only to construct
a coherent result; numerical correctness of its values is excluded.

VVUQ and scientific exclusions

This is software verification of immutable represented state. It establishes no
numerical verification, convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
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
    Qho1dComparisonResult,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
    Qho1dNondimensionalizer,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.software_verification
SUT = Qho1dComparisonResult


class TestQho1dComparisonResult:
    """Own software evidence for ``Qho1dComparisonResult``."""

    @staticmethod
    def result() -> Qho1dComparisonResult:
        """Return one coherent comparator-produced result fixture."""
        analytical = Qho1dAnalytical(
            Qho1dNondimensionalizer().execute(hbar=1.0, mass=1.0, omega=1.0)
        )
        request = Qho1dComparisonRequest(
            analytical=analytical,
            finite_difference=Qho1dFiniteDifference(
                analytical,
                DirichletInterval(
                    UniformCartesianGrid1D(
                        ScalarQuantity(-1.0, Unitless()),
                        ScalarQuantity(1.0, Unitless()),
                        ScalarQuantity(0.5, Unitless()),
                    ),
                    DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
                ),
            ),
            ladder_operators=Qho1dLadderOperators(analytical, LadderOperator1D(1)),
        )
        return Qho1dComparator().execute(request)

    def test_public_api__package__exports_supported_result_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-005

        Requirement: Qho1dComparisonResult is available through the
        supported public model-systems import surface.

        Acceptance: The package binding is the same class object as the documented
        harmonic-oscillator import.
        """
        assert model_systems.Qho1dComparisonResult is (Qho1dComparisonResult)

    def test_field__arrays__own_immutable_binary64_storage(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-006

        Requirement: Qho1dComparisonResult canonicalizes every numerical
        array to finite immutable binary64 storage with contract-derived shapes.

        Acceptance: A coherent result has float64 arrays with expected shapes, no
        array permits assignment, and a mutation attempt raises ValueError.
        """
        result = self.result()

        assert result.grid_coordinates.magnitude.dtype == np.dtype("float64")
        assert result.grid_coordinates.magnitude.shape == (3,)
        assert result.injection.magnitude.shape == (3, 1)
        assert result.gram_matrix.magnitude.shape == (1, 1)
        assert result.gram_inverse_square_root.magnitude.shape == (1, 1)
        assert result.pulled_back_hamiltonian.magnitude.shape == (1, 1)
        assert result.reference_hamiltonian.magnitude.shape == (1, 1)
        assert result.difference.magnitude.shape == (1, 1)
        assert not result.grid_coordinates.magnitude.flags.writeable
        assert not result.injection.magnitude.flags.writeable
        assert not result.difference.magnitude.flags.writeable
        with pytest.raises(ValueError, match="read-only"):
            result.injection.magnitude[0, 0] = 0.0
