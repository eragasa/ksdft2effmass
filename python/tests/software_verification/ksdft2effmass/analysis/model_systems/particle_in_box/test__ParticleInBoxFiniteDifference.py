r"""Software verification of ``ParticleInBoxFiniteDifference``.

Evidence profile: routine

Bounded artifact scope: public one-dimensional zero-potential finite representation.

Facet and represented meaning

The model applies particle-in-a-box physics to a reusable homogeneous Dirichlet
interval and generic finite-difference operators.

Intrinsic and cross-object scope

Interval compatibility, matrix construction, and closed-form discrete energies are
included.

VVUQ and scientific exclusions

This verifies one finite representation, not continuum convergence, scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    ParticleInBoxAnalytical,
    ParticleInBoxFiniteDifference,
    ParticleInBoxParameters,
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = ParticleInBoxFiniteDifference


class TestParticleInBoxFiniteDifference:
    """Own software evidence for ``ParticleInBoxFiniteDifference``."""

    def test_method__hamiltonian__composes_zero_potential_dirichlet_box(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PIB-003

        Requirement: The model composes a homogeneous interval spanning ``[0,L]``
        with the generic kinetic and zero-potential operators.

        Acceptance: ``L=m=hbar=1`` with three interior points produces diagonal 16,
        adjacent ``-8``, and the exact centered-difference spectrum.
        """
        analytical = ParticleInBoxAnalytical(
            ParticleInBoxParameters(
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
            )
        )
        model = ParticleInBoxFiniteDifference(
            analytical,
            DirichletInterval(
                UniformCartesianGrid1D(
                    ScalarQuantity(0.0, Unitless()),
                    ScalarQuantity(1.0, Unitless()),
                    ScalarQuantity(0.25, Unitless()),
                ),
                DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
            ),
        )

        np.testing.assert_array_equal(
            model.hamiltonian().to_dense().magnitude,
            np.array([[16.0, -8.0, 0.0], [-8.0, 16.0, -8.0], [0.0, -8.0, 16.0]]),
        )
        indices = np.array([1.0, 2.0, 3.0])
        np.testing.assert_array_equal(
            model.discrete_energy_levels().magnitude,
            32.0 * np.sin(indices * np.pi / 8.0) ** 2,
        )
