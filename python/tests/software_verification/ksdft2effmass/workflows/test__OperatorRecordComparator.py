r"""Software verification of ``OperatorRecordComparator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the OperatorRecordComparator facet. System under test
and evidence class
------------------------------------
The system under test is the genuine concrete production Workflow
``OperatorRecordComparator``. This cohesive module provides software-verification
evidence ``SV-ORC-001`` through ``SV-ORC-007``. It applies no numerical-
verification, scientific-validation, or uncertainty-quantification marker.

Workflow definition and dependencies
------------------------------------
The public composition is

``OperatorRecord + OperatorRecord -> OperatorRecordDifferencer ->``
``OperatorRecordDifferenceResult -> OperatorRecordResidualAnalyzer ->``
``OperatorRecordComparisonResult``.

The Workflow owns sequencing and explicit dependency composition only. The
``OperatorRecordDifferencer`` owns compatibility enforcement, signed subtraction,
and finite-difference failure. The ``OperatorRecordResidualAnalyzer`` owns norm
calculation, floating-point scaling, roundoff allowance, and metric
canonicalization.

Requirements, strategy, and acceptance
--------------------------------------
Tests inspect default and explicitly injected concrete dependencies, compare
Workflow output with explicit lower-layer public composition, validate dependency
types, and require unchanged propagation of representative structured errors.
Controlled replacement of ``numpy.linalg.svd`` reaches a deterministic backend
failure that small valid input cannot induce reliably. It verifies Workflow
propagation of the public error and does not verify SVD accuracy.

Ownership boundaries, interpretation, and limitations
-----------------------------------------------------
The Workflow does not own compatibility rules, subtraction, matrix storage,
finite-difference checks, norms, scaling, roundoff policy, physical thresholds,
scientific validation, or uncertainty quantification. Passing means the concrete
Workflow composes and propagates its public dependencies as documented. Failure
may indicate a Workflow sequencing/dependency regression, lower-layer contract
change, or evidence defect requiring investigation; it does not by itself prove
numerical inaccuracy, physical-model error, or scientific invalidity.

Independent norm accuracy belongs to ``NV-ORA-001`` through ``NV-ORA-017``.
Passing this module does not establish independent norm accuracy, basis or gauge
alignment, common physical-system identity, scientific residual acceptability,
reduced-Hamiltonian validity, or quantified uncertainty. Scientific validation
and uncertainty quantification have not been performed.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordComparator``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import warnings
from typing import Any, cast

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    IncompatibleOperatorRecordsError,
    OperatorRecord,
    OperatorRecordComparator,
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonNumericalErrorCode,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordDifferenceNumericalError,
    OperatorRecordDifferenceNumericalErrorCode,
    OperatorRecordDifferencer,
    OperatorRecordResidualAnalyzer,
    StateSpace,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordComparator

# Fixed linearly independent row lattice vectors provide a nonsingular synthetic
# geometry without introducing geometry transformation or comparison policy.
VALID_CELL: tuple[tuple[float, float, float], ...] = (
    (1.0, 0.0, 0.0),
    (0.0, 2.0, 0.0),
    (0.0, 0.0, 3.0),
)


def make_record(
    matrix: npt.NDArray[np.complex128],
    *,
    identifier: str,
    energy_unit: str = "eV",
) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Differencer and comparator cases require independently valid synthetic
    records with
    controlled identifiers, matrices, and energy units.

    Method: Construct or inspect only the named synthetic fixture operation (make
    record); the
    helper owns no assertion result and introduces no hidden oracle.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    dimension = matrix.shape[0]
    ordering = tuple(f"state-{index}" for index in range(dimension))
    return OperatorRecord(
        identifier,
        "finite_test_hamiltonian",
        matrix,
        StateSpace(f"space-{identifier}", "finite synthetic", dimension),
        Basis(f"basis-{identifier}", "site basis", ordering, True),
        Geometry(
            identifier,
            VALID_CELL,
            "periodic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        EnergyReference("explicit zero", energy_unit),
        {"source": f"synthetic Workflow test {identifier}"},
    )


def test_workflow__construct_default_workflow_dependencies__composes_exactly() -> None:
    r"""Evidence ID: SV-ORC-001

    Requirement: OperatorRecordComparator has this explicit differencer-then-analyzer
    Workflow
    property: construct default workflow dependencies: composes exactly.

    Method: Construct the declared public dependencies and records for construct default
    workflow dependencies: composes exactly, execute the Workflow, and compare it with
    explicit differencer-then-analyzer composition.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    comparator = OperatorRecordComparator()

    assert isinstance(comparator.differencer, OperatorRecordDifferencer)
    assert isinstance(comparator.residual_analyzer, OperatorRecordResidualAnalyzer)


def test_workflow__retain_explicitly_injected_dependencies__composes_exactly() -> None:
    r"""Evidence ID: SV-ORC-002

    Requirement: OperatorRecordComparator has this explicit differencer-then-analyzer
    Workflow
    property: retain explicitly injected dependencies: composes exactly.

    Method: Construct the declared public dependencies and records for retain explicitly
    injected dependencies: composes exactly, execute the Workflow, and compare it with
    explicit differencer-then-analyzer composition.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    differencer = OperatorRecordDifferencer()
    residual_analyzer = OperatorRecordResidualAnalyzer()

    comparator = OperatorRecordComparator(differencer, residual_analyzer)

    assert comparator.differencer is differencer
    assert comparator.residual_analyzer is residual_analyzer


def test_workflow__reproduce_explicit_public_composition__composes_exactly() -> None:
    r"""Evidence ID: SV-ORC-003

    Requirement: Workflow execution is equivalent to explicit execution of its approved
    lower-layer
    public ActionObjects in sequence.

    Method: Compute a difference, analyze it explicitly, then execute the Workflow with
    the same
    dependency instances and records.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Results compare exactly equal and preserve reference/candidate roles.
    interpretation
    and limitations This is a composition oracle, not an independent numerical oracle.
    Norm accuracy remains owned by ``the owning evidence`` through ``the owning
    evidence``.

    Interpretation: A pass supports only this requirement; a failure may identify an
    implementation,
    fixture, oracle, environment, or accepted-contract defect and requires diagnosis
    rather than weakened expectations.

    Limitations: This synthetic software evidence does not establish numerical
    verification, physical
    correctness, scientific validation, UQ, portability, or cross-language agreement.
    """

    reference = make_record(
        np.zeros((2, 2), dtype=np.complex128), identifier="reference"
    )
    candidate = make_record(
        np.array([[3.0, 0.0], [0.0, 4.0]], dtype=np.complex128),
        identifier="candidate",
    )
    differencer = OperatorRecordDifferencer()
    residual_analyzer = OperatorRecordResidualAnalyzer()
    comparator = OperatorRecordComparator(differencer, residual_analyzer)

    difference = differencer.execute(reference, candidate)
    expected = residual_analyzer.execute(difference)
    actual = comparator.execute(reference, candidate)

    assert actual == expected
    assert actual.reference_identifier == "reference"
    assert actual.candidate_identifier == "candidate"


@pytest.mark.parametrize(
    ("field_name", "expected_message"),
    [
        pytest.param(
            "differencer",
            "differencer must be an OperatorRecordDifferencer",
            id="invalid_differencer",
        ),
        pytest.param(
            "residual_analyzer",
            "residual_analyzer must be an OperatorRecordResidualAnalyzer",
            id="invalid_residual_analyzer",
        ),
    ],
)
def test_workflow__reject_invalid_workflow_dependencies__composes_exactly(
    field_name: str, expected_message: str
) -> None:
    r"""Evidence ID: SV-ORC-004

    Requirement: OperatorRecordComparator has this explicit differencer-then-analyzer
    Workflow
    property: reject invalid workflow dependencies: composes exactly.

    Method: Construct the declared public dependencies and records for reject invalid
    workflow
    dependencies: composes exactly, execute the Workflow, and compare it with explicit
    differencer-then-analyzer composition.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    kwargs = {field_name: cast(Any, object())}
    with pytest.raises(TypeError) as exc_info:
        OperatorRecordComparator(**cast(Any, kwargs))

    assert str(exc_info.value) == expected_message


def test_workflow__propagate_structured_incompatibility__composes_exactly() -> None:
    r"""Evidence ID: SV-ORC-005

    Requirement: OperatorRecordComparator has this explicit differencer-then-analyzer
    Workflow
    property: propagate structured incompatibility: composes exactly.

    Method: Construct the declared public dependencies and records for propagate
    structured
    incompatibility: composes exactly, execute the Workflow, and compare it with
    explicit differencer-then-analyzer composition.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: The named partition raises exactly IncompatibleOperatorRecordsError with
    the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    reference = make_record(
        np.zeros((1, 1), dtype=np.complex128),
        identifier="reference",
        energy_unit="eV",
    )
    candidate = make_record(
        np.zeros((1, 1), dtype=np.complex128),
        identifier="candidate",
        energy_unit="hartree",
    )

    with pytest.raises(IncompatibleOperatorRecordsError) as exc_info:
        OperatorRecordComparator().execute(reference, candidate)

    result = exc_info.value.compatibility_result
    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.is_compatible is False
    assert tuple(issue.code for issue in result.issues) == (
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
    )


def test_workflow__propagate_represented_difference__composes_exactly() -> None:
    r"""Evidence ID: SV-ORC-006

    Requirement: OperatorRecordComparator has this explicit differencer-then-analyzer
    Workflow
    property: propagate represented difference: composes exactly.

    Method: Construct the declared public dependencies and records for propagate
    represented
    difference: composes exactly, execute the Workflow, and compare it with explicit
    differencer-then-analyzer composition.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: The named partition raises exactly
    OperatorRecordDifferenceNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    reference = make_record(
        np.array([[-1.0e308 + 0.0j]], dtype=np.complex128), identifier="reference"
    )
    candidate = make_record(
        np.array([[1.0e308 + 0.0j]], dtype=np.complex128), identifier="candidate"
    )

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(OperatorRecordDifferenceNumericalError) as exc_info:
            OperatorRecordComparator().execute(reference, candidate)

    assert (
        exc_info.value.code
        is OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    )


def test_workflow__propagate_residual_analysis_numerical__composes_exactly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    r"""Evidence ID: SV-ORC-007

    Requirement: OperatorRecordComparator has this explicit differencer-then-analyzer
    Workflow
    property: propagate residual analysis numerical: composes exactly.

    Method: Construct the declared public dependencies and records for propagate
    residual
    analysis numerical: composes exactly, execute the Workflow, and compare it with
    explicit differencer-then-analyzer composition.

    Oracle: Explicit public composition of a separately constructed
    OperatorRecordDifferencer
    and OperatorRecordResidualAnalyzer fixes the expected Workflow result and propagated
    errors.

    Acceptance: The named partition raises exactly
    OperatorRecordComparisonNumericalError with the
    asserted public message, code, or attached result; no alternate exception is
    accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    reference = make_record(
        np.zeros((1, 1), dtype=np.complex128), identifier="reference"
    )
    candidate = make_record(
        np.ones((1, 1), dtype=np.complex128), identifier="candidate"
    )

    def fail_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        r"""Make controlled ``numpy.linalg.svd`` raise synthetic ``LinAlgError``.

        The controlled dependency cannot be failed reliably by the small valid
        input. This injection verifies propagation of the structured public
        error and does not verify NumPy SVD accuracy.
        """

        raise np.linalg.LinAlgError("synthetic SVD backend failure")

    monkeypatch.setattr(np.linalg, "svd", fail_svd)
    with pytest.raises(OperatorRecordComparisonNumericalError) as exc_info:
        OperatorRecordComparator().execute(reference, candidate)

    assert (
        exc_info.value.code
        is OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
    )
