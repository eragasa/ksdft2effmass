r"""Software verification of ``ParticleInBoxGridEvaluator``.

Evidence profile: routine

Bounded artifact scope: one finite particle-in-a-box grid evaluation.

Facet and represented meaning

The ActionObject composes the public box, interval, sparse Hamiltonian, and complete
tridiagonal eigensolver contracts.

Intrinsic and cross-object scope

Dimension, sparse storage, and closed-form eigenvalue agreement are included.

VVUQ and scientific exclusions

This is software verification of the finite representation, not continuum convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxGridEvaluator,
    ParticleInBoxParameters,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import SparseMatrixQuantity

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxGridEvaluator


class TestParticleInBoxGridEvaluator:
    """Own software evidence for ``ParticleInBoxGridEvaluator``."""

    def test_method__execute__retains_sparse_complete_eigensystem(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PIB-004

        Requirement: One grid evaluation diagonalizes the sparse represented
        Hamiltonian without changing its finite closed-form spectrum.

        Acceptance: Eight points retain 22 CSR nonzeros and eigenvalues agree with the
        independently exposed discrete formula to binary64 tolerance.
        """
        parameters = ParticleInBoxParameters(
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
        )
        result = ParticleInBoxGridEvaluator().execute(parameters, 8)

        assert isinstance(result.eigenpairs.operator, SparseMatrixQuantity)
        assert result.eigenpairs.operator.nonzero_count == 22
        np.testing.assert_allclose(
            result.eigenpairs.eigenvalues.magnitude,
            result.finite_difference.discrete_energy_levels().magnitude,
            rtol=64.0 * np.finfo(np.float64).eps,
        )

    def test_method__execute__preserves_physical_units(self) -> None:
        r"""Evidence ID: SV-MODEL-SYSTEM-PIB-005

        Requirement: Physical particle-in-a-box evaluation distinguishes coordinate,
        wavefunction, and energy units while preserving the represented finite
        Dirichlet spectrum.

        Acceptance: A two-nanometer electron-mass box has a nanometer grid,
        inverse-square-root-meter boundary data, joule eigenvalues, and agrees with
        the independently evaluated centered-difference spectrum within binary64
        tolerance.
        """
        length = 2.0e-9
        mass = 9.109_383_713_9e-31
        hbar = 1.054_571_817e-34
        points = 8
        parameters = ParticleInBoxParameters(
            ScalarQuantity(2.0, PhysicalUnit("nanometer")),
            ScalarQuantity(mass, PhysicalUnit("kilogram")),
            ScalarQuantity(hbar, PhysicalUnit("joule * second")),
        )

        result = ParticleInBoxGridEvaluator().execute(parameters, points)

        spacing = length / (points + 1)
        modes = np.arange(1, points + 1, dtype=np.float64)
        expected = (
            2.0
            * hbar
            * hbar
            / (mass * spacing * spacing)
            * np.sin(modes * np.pi / (2.0 * (points + 1))) ** 2
        )
        assert result.finite_difference.interval.grid.coordinate_unit == PhysicalUnit(
            "nanometer"
        )
        assert result.finite_difference.interval.boundary_condition.value.unit == (
            PhysicalUnit("meter ** -0.5")
        )
        assert result.eigenpairs.eigenvalues.unit == PhysicalUnit("joule")
        np.testing.assert_allclose(
            result.eigenpairs.eigenvalues.magnitude,
            expected,
            rtol=64.0 * np.finfo(np.float64).eps,
            atol=0.0,
        )
