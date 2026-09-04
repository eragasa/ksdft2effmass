r"""Software verification of private normalized-band comparison contract.

Evidence profile: routine

Bounded artifact scope: private normalized-band comparison contract.

Facet and represented meaning

Fail-closed compatibility and pointwise comparison of complete aligned band
representations.

Intrinsic and cross-object scope

Constructed immutable observations and an explicit specification are the oracle.
Cross-object settings and alignment identities remain comparator-owned.

VVUQ and scientific exclusions

The values are synthetic test data. These tests establish no parent-model
agreement, numerical verification, scientific validation, or acceptance.
"""

from dataclasses import replace

import pytest

import ksdft2effmass.analysis as analysis_package
from ksdft2effmass.analysis._band_comparison import (
    BandComparisonSpecification,
    BandStructureComparator,
    BandStructureComparisonIssueCode,
    BandStructureComparisonOutcome,
    BandStructureComparisonResult,
)
from ksdft2effmass.periodic._bands import (
    BandEnergyUnit,
    BandStructureObservation,
    BandStructureObservationIdentity,
    DftBackend,
)

pytestmark = pytest.mark.software_verification
_PSEUDO_SHA256 = "a" * 64


def make_observation(
    identity: str,
    backend: DftBackend,
    eigenvalues: tuple[tuple[float, ...], ...] | None,
) -> BandStructureObservation:
    """Evidence ID: Owns no identifier; supports SV-BAND-COMPARISON-001
    through SV-BAND-COMPARISON-004.

    Requirement: Test setup supplies one normalized observation shape.

    Method: Construct an immutable observation from explicit synthetic values.

    Oracle: The function arguments and fixed alignment identities define setup.

    Acceptance: The returned observation preserves those values exactly.

    Interpretation: Failure identifies synthetic observation setup drift.

    Limitations: The helper owns no independent comparison or scientific claim.
    """
    return BandStructureObservation(
        BandStructureObservationIdentity(identity),
        f"{identity}:source",
        backend,
        "synthetic-system",
        True,
        ("L", "Gamma", "X"),
        2,
        2,
        "normalized reduced coordinates",
        "synthetic-grid-v1",
        10.0,
        9.0,
        _PSEUDO_SHA256,
        "synthetic-pseudopotential-alignment-v1",
        BandEnergyUnit.HARTREE,
        "synthetic aligned zero",
        "synthetic-energy-alignment-v1",
        f"{identity}:spectrum",
        eigenvalues,
    )


def make_specification() -> BandComparisonSpecification:
    """Evidence ID: Owns no identifier; supports SV-BAND-COMPARISON-001
    through SV-BAND-COMPARISON-004.

    Requirement: Test setup supplies one explicit synthetic comparison policy.

    Method: Construct the immutable specification from literal expected values.

    Oracle: The accepted synthetic test contract defines every policy field.

    Acceptance: The returned specification preserves the exact policy values.

    Interpretation: Failure identifies synthetic specification setup drift.

    Limitations: The helper owns no independent comparison or scientific claim.
    """
    return BandComparisonSpecification(
        "synthetic-system",
        ("L", "Gamma", "X"),
        2,
        BandEnergyUnit.HARTREE,
        "synthetic-grid-v1",
        "synthetic-pseudopotential-alignment-v1",
        "synthetic-energy-alignment-v1",
        0.0,
        0.0,
        0.01,
    )


def test_artifact__comparison__compares_complete_aligned_synthetic_spectra() -> None:
    """Evidence ID: SV-BAND-COMPARISON-001

    Requirement: Complete observations satisfying every explicit alignment field
    are compared pointwise in hartree under the supplied absolute tolerance.

    Method: Compare two explicit complete two-point, two-band arrays.

    Oracle: Direct subtraction gives an exact maximum difference of 0.005 hartree.

    Acceptance: The result is compared, the maximum is 0.005 hartree, and the
    0.01-hartree tolerance is satisfied without findings.

    Interpretation: Failure identifies aligned pointwise-comparison drift.

    Limitations: Synthetic values do not verify a scientific numerical method.
    """
    left = make_observation(
        "left", DftBackend.QUANTUM_ESPRESSO, ((0.0, 1.0), (2.0, 3.0))
    )
    right = make_observation("right", DftBackend.ABINIT, ((0.005, 1.0), (2.0, 3.0)))

    result = BandStructureComparator().execute(left, right, make_specification())

    assert result.outcome is BandStructureComparisonOutcome.COMPARED
    assert result.workflow_structure_compatible is True
    assert result.maximum_absolute_difference_hartree == 0.005
    assert result.within_eigenvalue_tolerance is True
    assert result.issues == ()


def test_artifact__comparison__rejects_missing_alignment_and_spectrum() -> None:
    """Evidence ID: SV-BAND-COMPARISON-002

    Requirement: Structural workflow agreement cannot replace comparison-grid,
    pseudopotential, energy-reference, or complete-spectrum prerequisites.

    Method: Remove the three alignment identities and both complete spectra.

    Oracle: The explicit specification requires each removed prerequisite.

    Acceptance: The result remains structurally compatible but is rejected with
    exactly the four missing-prerequisite codes and no numerical difference.

    Interpretation: Failure identifies fail-closed comparison-admission drift.

    Limitations: This does not establish which scientific alignment should be used.
    """
    left = make_observation("left", DftBackend.QUANTUM_ESPRESSO, None)
    right = make_observation("right", DftBackend.ABINIT, None)
    left = replace(
        left,
        comparison_grid_identity=None,
        pseudopotential_alignment_identity=None,
        energy_alignment_identity=None,
    )
    right = replace(
        right,
        comparison_grid_identity=None,
        pseudopotential_alignment_identity=None,
        energy_alignment_identity=None,
    )

    result = BandStructureComparator().execute(left, right, make_specification())

    assert result.outcome is BandStructureComparisonOutcome.REJECTED
    assert result.workflow_structure_compatible is True
    assert {item.code for item in result.issues} == {
        BandStructureComparisonIssueCode.COMPARISON_GRID_MISMATCH,
        BandStructureComparisonIssueCode.PSEUDOPOTENTIAL_ALIGNMENT_MISSING,
        BandStructureComparisonIssueCode.ENERGY_ALIGNMENT_MISSING,
        BandStructureComparisonIssueCode.COMPLETE_SPECTRUM_UNAVAILABLE,
    }
    assert result.maximum_absolute_difference_hartree is None
    assert result.within_eigenvalue_tolerance is None


def test_artifact__comparison__reports_every_incompatibility_in_stable_order() -> None:
    """Evidence ID: SV-BAND-COMPARISON-003

    Requirement: A rejected comparison reports every represented incompatibility
    in the comparator's documented deterministic order without computing a value.

    Method: Make every independently represented compatibility prerequisite fail
    across two intrinsically valid observations.

    Oracle: The private contract declares thirteen issue codes in comparison-check
    order, from system mismatch through unavailable complete spectra.

    Acceptance: The result is rejected with exactly those thirteen ordered codes,
    false workflow compatibility, and absent numerical fields.

    Interpretation: Failure identifies a missing, reordered, or bypassed fail-closed
    admission check.

    Limitations: Synthetic mismatches do not identify a scientifically correct
    alignment or establish that two physical calculations are comparable.
    """
    left = replace(
        make_observation("left", DftBackend.QUANTUM_ESPRESSO, None),
        system_identity="left-system",
        scf_to_fixed_density_bands=False,
        path_topology=("L",),
        point_count=1,
        band_count=1,
        coordinate_convention="left coordinates",
        comparison_grid_identity="left-grid",
        lattice_parameter_bohr=9.0,
        wavefunction_cutoff_hartree=8.0,
        pseudopotential_alignment_identity=None,
        energy_unit=BandEnergyUnit.ELECTRON_VOLT,
        energy_alignment_identity=None,
    )
    right = replace(
        make_observation("right", DftBackend.ABINIT, None),
        system_identity="right-system",
        scf_to_fixed_density_bands=False,
        path_topology=("X",),
        point_count=2,
        band_count=3,
        coordinate_convention="right coordinates",
        comparison_grid_identity="right-grid",
        lattice_parameter_bohr=11.0,
        wavefunction_cutoff_hartree=10.0,
        pseudopotential_alignment_identity=None,
        energy_unit=BandEnergyUnit.ELECTRON_VOLT,
        energy_alignment_identity=None,
    )

    result = BandStructureComparator().execute(left, right, make_specification())

    assert result.outcome is BandStructureComparisonOutcome.REJECTED
    assert result.workflow_structure_compatible is False
    assert tuple(issue.code for issue in result.issues) == (
        BandStructureComparisonIssueCode.SYSTEM_MISMATCH,
        BandStructureComparisonIssueCode.WORKFLOW_TOPOLOGY_MISMATCH,
        BandStructureComparisonIssueCode.PATH_TOPOLOGY_MISMATCH,
        BandStructureComparisonIssueCode.BAND_COUNT_MISMATCH,
        BandStructureComparisonIssueCode.POINT_COUNT_MISMATCH,
        BandStructureComparisonIssueCode.COORDINATE_CONVENTION_MISMATCH,
        BandStructureComparisonIssueCode.COMPARISON_GRID_MISMATCH,
        BandStructureComparisonIssueCode.LATTICE_PARAMETER_MISMATCH,
        BandStructureComparisonIssueCode.WAVEFUNCTION_CUTOFF_MISMATCH,
        BandStructureComparisonIssueCode.PSEUDOPOTENTIAL_ALIGNMENT_MISSING,
        BandStructureComparisonIssueCode.ENERGY_UNIT_MISMATCH,
        BandStructureComparisonIssueCode.ENERGY_ALIGNMENT_MISSING,
        BandStructureComparisonIssueCode.COMPLETE_SPECTRUM_UNAVAILABLE,
    )
    assert result.maximum_absolute_difference_hartree is None
    assert result.within_eigenvalue_tolerance is None


@pytest.mark.parametrize(
    ("difference_hartree", "expected_within_tolerance"),
    (
        pytest.param(0.005, True, id="below_absolute_tolerance"),
        pytest.param(0.01, True, id="equal_to_absolute_tolerance"),
        pytest.param(0.02, False, id="above_absolute_tolerance"),
    ),
)
def test_artifact__comparison__applies_inclusive_absolute_tolerance(
    difference_hartree: float,
    expected_within_tolerance: bool,
) -> None:
    """Evidence ID: SV-BAND-COMPARISON-004

    Requirement: Comparison classifies a finite maximum difference as within the
    supplied absolute tolerance exactly when the difference is less than or equal
    to that tolerance.

    Method: Place one explicit difference below, at, or above the fixed 0.01-hartree
    synthetic tolerance while holding every admission prerequisite constant.

    Oracle: Direct ordering against 0.01 hartree gives true, true, and false for the
    three semantic partitions.

    Acceptance: Each compared result preserves the explicit maximum and returns the
    corresponding inclusive-boundary classification without issues.

    Interpretation: Failure identifies absolute-tolerance boundary drift.

    Limitations: The synthetic tolerance is not production policy or physical
    acceptance evidence.
    """
    left = make_observation(
        "left", DftBackend.QUANTUM_ESPRESSO, ((0.0, 1.0), (2.0, 3.0))
    )
    right = make_observation(
        "right",
        DftBackend.ABINIT,
        ((difference_hartree, 1.0), (2.0, 3.0)),
    )

    result = BandStructureComparator().execute(left, right, make_specification())

    assert result.outcome is BandStructureComparisonOutcome.COMPARED
    assert result.maximum_absolute_difference_hartree == difference_hartree
    assert result.within_eigenvalue_tolerance is expected_within_tolerance
    assert result.issues == ()


def test_artifact__result__rejects_false_workflow_compatibility() -> None:
    """Evidence ID: SV-BAND-COMPARISON-005

    Requirement: A manually constructed compared result must represent compatible
    workflow structure in addition to present numerical fields and absent issues.

    Method: Construct the otherwise complete compared variant with workflow
    compatibility set to false.

    Oracle: Comparator admission rejects every workflow-structure mismatch, so no
    compared result can consistently carry false workflow compatibility.

    Acceptance: Construction raises ``ValueError`` for the inconsistent variant.

    Interpretation: Failure permits a result state that the owning ActionObject can
    never produce under its fail-closed contract.

    Limitations: This intrinsic check does not establish scientific comparability.
    """
    with pytest.raises(ValueError, match="fields do not match the outcome"):
        BandStructureComparisonResult(
            BandStructureComparisonOutcome.COMPARED,
            False,
            (),
            0.0,
            True,
        )


def test_artifact__public_api__keeps_private_comparison_names_unexported() -> None:
    """Evidence ID: SV-BAND-COMPARISON-006

    Requirement: The revisable comparison slice is absent from the supported
    ``ksdft2effmass.analysis`` package surface.

    Method: Inspect the package namespace for every private comparison contract name.

    Oracle: The accepted initial-slice architecture explicitly defers public exports.

    Acceptance: None of the six comparison names is present on the package root.

    Interpretation: Failure identifies accidental public-contract expansion.

    Limitations: Namespace absence does not prevent direct private-module imports.
    """
    prohibited_names = {
        "BandComparisonSpecification",
        "BandStructureComparator",
        "BandStructureComparisonIssue",
        "BandStructureComparisonIssueCode",
        "BandStructureComparisonOutcome",
        "BandStructureComparisonResult",
    }

    assert prohibited_names.isdisjoint(vars(analysis_package))
