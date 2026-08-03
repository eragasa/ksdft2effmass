r"""Software-verification evidence for ``OperatorRecordComparator`` Workflow.

System under test and evidence class
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
    """Construct one synthetic finite operator record without test-side coercion.

    Parameters
    ----------
    matrix
        Exact caller-prepared ``numpy.ndarray`` with ``complex128`` dtype. The
        helper does not coerce lists, array subclasses, dtype, rank, or shape.
    identifier
        Identity-specific label used deliberately in record, state-space, basis,
        geometry, and provenance metadata that compatibility ignores.
    energy_unit
        Deterministic matrix-energy metadata, ``eV`` by default. Override is used
        only to create the focused incompatibility case.

    Returns
    -------
    OperatorRecord
        Synthetic record whose state-space dimension and ordered basis labels are
        derived directly from ``matrix.shape[0]``. Records made with equal matrix
        dimensions and default arguments are representation-compatible despite
        their identity-specific metadata.

    Notes
    -----
    ``VALID_CELL`` supplies fixed nonsingular synthetic geometry. The record is
    not DFT, Wannier, impurity, or experimental data and establishes no physical
    or scientific validity.
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


def test_construct_default_workflow_dependencies() -> None:
    """SV-ORC-001: construct the two documented default dependencies.

    Requirement and method
        Construct the Workflow without arguments and inspect its public fields.
    Acceptance
        ``differencer`` and ``residual_analyzer`` are instances of their exact
        documented concrete public dependency types.
    Interpretation and limitations
        Passing verifies default dependency construction only and does not retest
        either dependency's internal behavior.
    """

    comparator = OperatorRecordComparator()

    assert isinstance(comparator.differencer, OperatorRecordDifferencer)
    assert isinstance(comparator.residual_analyzer, OperatorRecordResidualAnalyzer)


def test_retain_explicitly_injected_dependencies() -> None:
    """SV-ORC-002: retain explicitly injected dependency identities.

    Requirement and method
        Inject concrete public differencer and residual-analyzer instances.
    Acceptance
        Workflow fields are identical to the supplied objects, demonstrating no
        hidden replacement.
    Interpretation and limitations
        Passing verifies explicit composition, not abstract substitution or
        lower-layer algorithms.
    """

    differencer = OperatorRecordDifferencer()
    residual_analyzer = OperatorRecordResidualAnalyzer()

    comparator = OperatorRecordComparator(differencer, residual_analyzer)

    assert comparator.differencer is differencer
    assert comparator.residual_analyzer is residual_analyzer


def test_reproduce_explicit_public_composition() -> None:
    """SV-ORC-003: reproduce differencer-then-analyzer composition exactly.

    Requirement
        Workflow execution is equivalent to explicit execution of its approved
        lower-layer public ActionObjects in sequence.
    Method
        Compute a difference, analyze it explicitly, then execute the Workflow
        with the same dependency instances and records.
    Acceptance
        Results compare exactly equal and preserve reference/candidate roles.
    Interpretation and limitations
        This is a composition oracle, not an independent numerical oracle. Norm
        accuracy remains owned by ``NV-ORA-001`` through ``NV-ORA-017``.
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
            id="SV-ORC-004-invalid-differencer",
        ),
        pytest.param(
            "residual_analyzer",
            "residual_analyzer must be an OperatorRecordResidualAnalyzer",
            id="SV-ORC-004-invalid-residual-analyzer",
        ),
    ],
)
def test_reject_invalid_workflow_dependencies(
    field_name: str, expected_message: str
) -> None:
    """SV-ORC-004: reject each invalid concrete dependency independently.

    Requirement and method
        Supply a plain object to one public dependency field per collected case.
    Acceptance
        The exact field-specific ``TypeError`` diagnostic is raised.
    Interpretation and limitations
        Passing verifies concrete dependency validation only; mocks, private
        fields, and abstract interfaces are outside this Workflow contract.
    """

    kwargs = {field_name: cast(Any, object())}
    with pytest.raises(TypeError) as exc_info:
        OperatorRecordComparator(**cast(Any, kwargs))

    assert str(exc_info.value) == expected_message


def test_propagate_structured_incompatibility() -> None:
    """SV-ORC-005: propagate exact energy-unit incompatibility evidence.

    Requirement
        The Workflow neither replaces nor reinterprets the differencer's public
        compatibility result.
    Method
        Execute records differing only in energy unit.
    Acceptance
        The propagated error retains both identifiers, false compatibility, and
        exactly ``ENERGY_UNIT_MISMATCH``.
    Interpretation and limitations
        Passing verifies one representative propagation path. Complete rule
        coverage belongs to ``OperatorRecordCompatibilityAnalyzer`` tests.
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


def test_propagate_represented_difference_numerical_failure() -> None:
    """SV-ORC-006: propagate structured nonfinite-difference failure.

    Requirement
        Subtraction overflow propagates unchanged as
        ``OperatorRecordDifferenceNumericalError`` with ``NONFINITE_DIFFERENCE``.
    Method
        Execute ``candidate - reference`` for ``+1e308 - (-1e308)`` while
        promoting raw ``RuntimeWarning`` to an error at the Workflow boundary.
    Acceptance
        Only the exact public exception and enum code are observed; no warning
        escapes.
    Interpretation and limitations
        Passing verifies Workflow propagation. Subtraction behavior is owned and
        independently tested by ``OperatorRecordDifferencer``.
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


def test_propagate_residual_analysis_numerical_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SV-ORC-007: propagate structured residual backend failure unchanged.

    Requirement
        A lower-layer residual failure reaches the caller with
        ``LINEAR_ALGEBRA_FAILURE``.
    Method
        Replace ``numpy.linalg.svd`` because deterministic ``LinAlgError`` cannot
        be induced reliably from the small valid public matrix.
    Acceptance
        The propagated public comparison numerical error carries the exact enum.
    Interpretation and limitations
        This verifies Workflow propagation only and does not verify SVD accuracy
        or duplicate the residual analyzer's complete fault-translation suite.
    """

    reference = make_record(
        np.zeros((1, 1), dtype=np.complex128), identifier="reference"
    )
    candidate = make_record(
        np.ones((1, 1), dtype=np.complex128), identifier="candidate"
    )

    def fail_svd(*_args: object, **_kwargs: object) -> npt.NDArray[np.float64]:
        """Make controlled ``numpy.linalg.svd`` raise synthetic ``LinAlgError``.

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
