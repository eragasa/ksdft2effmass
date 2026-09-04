r"""Numerical verification of the private aligned band-comparison probe.

Evidence profile: claim_bearing

Bounded artifact scope: the private aligned synthetic band-comparison probe.

Facet and represented meaning

The probe compares two complete synthetic two-point, two-band spectra represented in
hartree on one common synthetic grid. For left spectrum :math:`L` and right spectrum
:math:`R`, the implemented scalar is

.. math::

   d_{\max}=\max_{k,n}|L_{kn}-R_{kn}|.

The literal arrays differ entrywise by ``0.125``, ``0.125``, ``0.25``, and ``0.25``
hartree, so the independently derived maximum is exactly ``0.25`` hartree. These
values are binary fractions and require no approximate decimal oracle.

Intrinsic and cross-object scope

Both immutable observations carry the same synthetic system, path, point count, band
count, coordinate convention, comparison-grid identity, lattice parameter, cutoff,
pseudopotential-alignment identity, energy unit, and energy-alignment identity. Their
calculator labels and synthetic pseudopotential digests remain distinct. The explicit
comparison specification owns the alignment requirements and a ``0.25``-hartree
boundary tolerance.

VVUQ and scientific exclusions

Passing establishes only the maximum-absolute-difference calculation and inclusive
tolerance boundary for this small exact synthetic representation. The alignment
identities are synthetic test declarations, not evidence that any physical
pseudopotentials or energy references are aligned. This test invokes no calculator and
establishes no DFT convergence, backend agreement, physical accuracy, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis._band_comparison import (
    BandComparisonSpecification,
    BandStructureComparator,
    BandStructureComparisonOutcome,
)
from ksdft2effmass.periodic._bands import (
    BandEnergyUnit,
    BandStructureObservation,
    BandStructureObservationIdentity,
    DftBackend,
)

pytestmark = pytest.mark.numerical_verification


def make_observation(
    identity: str,
    backend: DftBackend,
    pseudopotential_sha256: str,
    eigenvalues: tuple[tuple[float, ...], ...],
) -> BandStructureObservation:
    r"""Construct one aligned synthetic observation without comparing values.

    Evidence ID: Helper owns no identifier; supports ``NV-BAND-COMPARISON-001``.

    Requirement: The numerical case requires complete immutable spectra with common
    synthetic comparison metadata and distinct calculator provenance labels.

    Method: Supply literal metadata and the caller's explicit point-by-band array to
    the private observation constructor.

    Oracle: The consuming test owns the arrays and hand-derived difference; this
    helper performs no subtraction, reduction, or tolerance decision.

    Acceptance: Return a valid observation preserving the supplied spectrum exactly.

    Interpretation: Failure identifies fixture construction drift and blocks the
    consuming numerical evidence.

    Limitations: Synthetic alignment metadata establishes no physical alignment.
    """
    return BandStructureObservation(
        BandStructureObservationIdentity(identity),
        f"{identity}:source-result",
        backend,
        "synthetic-diamond-silicon",
        True,
        ("L", "Gamma", "X", "Gamma"),
        2,
        2,
        "synthetic common reduced coordinates",
        "synthetic-common-grid-v1",
        10.0,
        12.0,
        pseudopotential_sha256,
        "synthetic-pseudopotential-alignment-v1",
        BandEnergyUnit.HARTREE,
        "synthetic aligned energy zero",
        "synthetic-energy-alignment-v1",
        f"{identity}:spectrum",
        eigenvalues,
    )


def make_specification() -> BandComparisonSpecification:
    r"""Construct the explicit aligned synthetic comparison policy.

    Evidence ID: Helper owns no identifier; supports ``NV-BAND-COMPARISON-001``.

    Requirement: The comparison requires exact common metadata and an inclusive
    ``0.25``-hartree eigenvalue tolerance.

    Method: Construct the private specification from fixed literal policy values.

    Oracle: The consuming test independently derives ``0.25`` hartree from the input
    arrays; this helper performs no numerical comparison.

    Acceptance: Return a valid immutable specification with the exact boundary.

    Interpretation: Failure identifies fixture-policy construction drift.

    Limitations: The large synthetic tolerance is test policy, not scientific policy.
    """
    return BandComparisonSpecification(
        "synthetic-diamond-silicon",
        ("L", "Gamma", "X", "Gamma"),
        2,
        BandEnergyUnit.HARTREE,
        "synthetic-common-grid-v1",
        "synthetic-pseudopotential-alignment-v1",
        "synthetic-energy-alignment-v1",
        0.0,
        0.0,
        0.25,
    )


def test_artifact__maximum_difference__agrees_with_exact_synthetic_oracle() -> None:
    r"""Evidence ID: NV-BAND-COMPARISON-001

    Requirement: For complete admitted spectra, ``BandStructureComparator`` computes
    :math:`d_{\max}=\max_{k,n}|L_{kn}-R_{kn}|` in hartree and treats equality with
    the explicit absolute tolerance as within tolerance.

    Method: Compare literal ``2 x 2`` spectra whose four absolute differences are
    hand-derived binary fractions, with the maximum occurring away from the first
    element and repeated in the second point.

    Oracle: For ``L=((0,1),(2,3))`` and
    ``R=((0.125,0.875),(2.25,2.75))`` hartree, the absolute differences are
    ``(0.125,0.125,0.25,0.25)`` and therefore ``d_max=0.25`` hartree exactly.

    Acceptance: The outcome is ``compared``, the represented maximum equals exactly
    ``0.25`` hartree, the inclusive ``0.25``-hartree tolerance is satisfied, and no
    incompatibility issue is returned.

    Interpretation: Failure indicates comparison admission, traversal, absolute
    difference, maximum reduction, or inclusive-boundary drift for this exact case.

    Limitations: One small binary-exact synthetic case is not an arbitrary-size
    floating-point error analysis or a physical cross-backend comparison.
    """
    left = make_observation(
        "synthetic-left",
        DftBackend.QUANTUM_ESPRESSO,
        "a" * 64,
        ((0.0, 1.0), (2.0, 3.0)),
    )
    right = make_observation(
        "synthetic-right",
        DftBackend.ABINIT,
        "b" * 64,
        ((0.125, 0.875), (2.25, 2.75)),
    )

    result = BandStructureComparator().execute(left, right, make_specification())

    assert result.outcome is BandStructureComparisonOutcome.COMPARED
    assert result.workflow_structure_compatible is True
    assert result.issues == ()
    assert result.maximum_absolute_difference_hartree == 0.25
    assert result.within_eigenvalue_tolerance is True
