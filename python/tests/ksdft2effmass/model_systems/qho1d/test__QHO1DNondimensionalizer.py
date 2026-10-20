r"""Software verification of ``QHO1DNondimensionalizer``.

Evidence profile: routine

Bounded artifact scope: public normalized-scalar adaptation contract.

Facet and represented meaning

The class under test owns explicit adaptation of already nondimensional harmonic-
oscillator scalars to first-class Unitless quantities.

Intrinsic and cross-object scope

Exact scalar preservation and Unitless attachment are included.

VVUQ and scientific exclusions

This verifies typed adaptation only. It does not derive nondimensional scales or
establish numerical convergence, scientific validation, uncertainty quantification,
or human acceptance.
"""

import pytest
from ksdft2effmass import model_systems
from ksdft2effmass.model_systems.qho1d import (
    QHO1DNondimensionalizer,
    ScalarQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = QHO1DNondimensionalizer


class TestQHO1DNondimensionalizer:
    """Own software evidence for ``QHO1DNondimensionalizer``."""

    def test_method__execute__attaches_unitless_without_rescaling(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-HO-018

        Requirement: The explicit nondimensionalization boundary preserves declared
        normalized magnitudes and attaches the Unitless type to every parameter.

        Acceptance: The public export is exact and inputs ``(2, 3, 4)`` become exact
        Unitless scalar quantities with those magnitudes.
        """
        assert model_systems.QHO1DNondimensionalizer is (QHO1DNondimensionalizer)

        parameters = QHO1DNondimensionalizer().execute(2.0, 3.0, 4.0)

        assert parameters.hbar == ScalarQuantity(2.0, Unitless())
        assert parameters.mass == ScalarQuantity(3.0, Unitless())
        assert parameters.omega == ScalarQuantity(4.0, Unitless())
