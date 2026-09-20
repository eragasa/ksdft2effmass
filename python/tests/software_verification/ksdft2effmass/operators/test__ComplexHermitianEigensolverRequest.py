r"""Software verification of ``ComplexHermitianEigensolverRequest``.

Evidence profile: routine

Bounded artifact scope: immutable sparse complex-Hermitian solver controls.

Facet and represented meaning

The DataObject declares selected count, iterative tolerance and limit, deterministic
initial-vector seed, and the independent algebraic-residual acceptance tolerance.

Intrinsic and cross-object scope

Strict scalar types and positive or nonnegative domains are included.

VVUQ and scientific exclusions

This does not execute or validate an eigensolver, scientific model, UQ analysis,
campaign, or protected calculation and does not provide human acceptance.
"""

import pytest

from ksdft2effmass.operators import ComplexHermitianEigensolverRequest

pytestmark = pytest.mark.software_verification
SUT = ComplexHermitianEigensolverRequest


class TestComplexHermitianEigensolverRequest:
    """Own software evidence for sparse eigensolver request validation."""

    def test_constructor__controls__require_explicit_valid_domains(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-EIGENSOLVER-001

        Requirement: Solver and acceptance controls use strict built-in scalar types
        and valid numerical domains.

        Acceptance: A valid request is retained; boolean count and negative residual
        tolerance are rejected.
        """
        request = ComplexHermitianEigensolverRequest(2, 0.0, 500, 0, 1.0e-10)
        assert request.selected_count == 2
        assert request.maximum_iterations == 500
        assert request.initial_vector_seed == 0
        with pytest.raises(TypeError, match="selected_count"):
            ComplexHermitianEigensolverRequest(True, 0.0, None, 0, 1.0e-10)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="residual_tolerance"):
            ComplexHermitianEigensolverRequest(2, 0.0, None, 0, -1.0)
