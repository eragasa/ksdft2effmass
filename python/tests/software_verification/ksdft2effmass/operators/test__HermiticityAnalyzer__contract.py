r"""Software verification of ``HermiticityAnalyzer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the contract facet. Evidence IDs
------------
``SV-HA-011`` through ``SV-HA-019``.

Requirement: The ActionObject accepts only ``OperatorRecord`` inputs, constructs public
unit-bearing Results, checks exact units before arithmetic, enforces results
through ``require()``, owns tolerance policy, and translates nonfinite residuals
to a structured public failure.

Method: ``SV-HA-011`` through ``SV-HA-019`` exercise only public Analyzer methods with
finite synthetic records and deliberate invalid inputs.

Oracle: The approved operator-record architecture and Hermiticity Sphinx contract define
public behavior, ordering, and structured errors. Exact-zero cases avoid
approximate numerical metric oracles in this software module.

Acceptance: Exact result values where mathematically exact, exact public exception
classes,
retained structured fields, enum identity, and warning containment must match.

Interpretation: Passing establishes public ActionObject execution, enforcement, policy
ownership,
and failure taxonomy. Failure indicates an implementation, contract, or evidence
defect requiring investigation.

Limitations: Nonzero residual accuracy is excluded and belongs to ``NV-HA``. Synthetic
data
make no DFT, Wannier, impurity, or scientific-validity claim. Scientific
validation, uncertainty quantification, and Rust conformance are not established.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``HermiticityAnalyzer``; collaborators only construct inputs or
expose public outcomes. Accepted public contracts, literal expected values, Python
language semantics, and assigned schema or fixture artifacts provide the oracles. No
runtime warning is accepted unless a test explicitly states otherwise.

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
    HermiticityAnalyzer,
    HermiticityNumericalError,
    HermiticityNumericalErrorCode,
    HermiticityRequirementError,
    HermiticityResult,
    HermiticityUnitMismatchError,
    OperatorRecord,
    StateSpace,
)

pytestmark = pytest.mark.software_verification

SUT = HermiticityAnalyzer

VALID_CELL = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def make_record(
    matrix: npt.NDArray[np.complex128],
    *,
    energy_unit: str = "eV",
) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: ----------- The test factory accepts an explicitly prepared
    ``np.complex128`` matrix
    and matching unit metadata without broad coercion.

    Method: ------ Derive dimension from the already valid square shape and construct
    matching
    finite state-space and ordered-basis metadata.

    Oracle: ------ The supplied matrix and unit are passed unchanged to public
    constructors;
    deterministic identity geometry and provenance complete the fixture.

    Acceptance: ---------- Public ``OperatorRecord`` construction validates the fixture.

    Interpretation: -------------- The helper supplies auditable public inputs to
    Analyzer contract
    evidence.

    Limitations: ----------- It performs no ``np.asarray`` coercion and makes no DFT,
    Wannier,
    impurity, scientific-validation, UQ, or Rust-conformance claim.
    """

    dimension = matrix.shape[0]
    ordering = tuple(f"basis-{index}" for index in range(dimension))
    return OperatorRecord(
        identifier="synthetic-hermiticity-contract",
        operator_kind="finite_test_hamiltonian",
        matrix=matrix,
        state_space=StateSpace("synthetic-state-space", "finite synthetic", dimension),
        basis=Basis("ordered-test-basis", "finite synthetic", ordering, True),
        geometry=Geometry(
            "synthetic",
            VALID_CELL,
            "finite synthetic",
            "cartesian row lattice vectors",
            "angstrom",
        ),
        energy_reference=EnergyReference("explicit synthetic zero", energy_unit),
        provenance={"source": "synthetic HermiticityAnalyzer contract evidence"},
    )


@pytest.mark.parametrize(
    "invalid_record",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_ha_011_boolean"),
        pytest.param(object(), id="sv_ha_011_arbitrary_object"),
    ],
)
def test_method__execute__execute_rejects_non_operator_record_inputs(
    invalid_record: Any,
) -> None:
    r"""Evidence ID: SV-HA-011

    Requirement: ----------- ``execute()`` accepts only a public ``OperatorRecord``.

    Method: ------ Pass representative invalid semantic inputs without conversion.

    Oracle: ------ The approved method signature and stable ``OperatorRecord``
    diagnostic apply.

    Acceptance: ---------- Exact exception category is ``TypeError`` and diagnostic
    names the type.

    Interpretation: -------------- Passing establishes the independent ``execute()``
    input boundary.

    Limitations: ----------- ``Any``/``cast`` is confined to invalid input. Numerical
    accuracy,
    scientific validation, UQ, and Rust conformance are excluded.
    """

    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with pytest.raises(TypeError, match="OperatorRecord"):
        analyzer.execute(cast(Any, invalid_record))


def test_method__execute__execute_constructs_public_result_for_exact_hermitian() -> (
    None
):
    r"""Evidence ID: SV-HA-012

    Requirement: ----------- Execution returns residual, Analyzer tolerance, and common
    energy unit.

    Method: ------ Analyze an exactly diagonal Hermitian binary64 matrix.

    Oracle: ------ Each off-diagonal and diagonal conjugate difference is exactly zero.

    Acceptance: ---------- Result type, exact zero, tolerance, unit roles, and true
    predicate all
    match.

    Interpretation: -------------- Passing establishes execution-path Result
    construction, not nonzero
    accuracy.

    Limitations: ----------- Nonzero numerical oracles, scientific validation, UQ, and
    Rust
    conformance are excluded.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 2.0 + 0.0j]],
        dtype=np.complex128,
    )
    record = make_record(matrix)
    analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")

    result = analyzer.execute(record)

    assert isinstance(result, HermiticityResult)
    assert result.residual == 0.0
    assert result.tolerance == analyzer.tolerance
    assert result.energy_unit == analyzer.energy_unit
    assert result.energy_unit == record.energy_reference.unit
    assert result.is_hermitian


def test_method__execute__execute_propagates_exact_energy_unit_mismatch_roles() -> None:
    r"""Evidence ID: SV-HA-013

    Requirement: ----------- Analyzer ``eV`` and record ``hartree`` are an exact
    software mismatch.

    Method: ------ Execute an exact-zero matrix carrying a distinct record unit.

    Oracle: ------ Approved exact string equality requires no conversion or
    normalization.

    Acceptance: ---------- ``HermiticityUnitMismatchError`` retains both exact ordered
    role strings.

    Interpretation: -------------- Passing establishes public mismatch detection and
    structured
    propagation.

    Limitations: ----------- Direct exception invariants, unit conversion, physical
    equivalence,
    scientific validation, UQ, and Rust conformance are not duplicated.
    """

    matrix = np.array([[1.0 + 0.0j]], dtype=np.complex128)
    record = make_record(matrix, energy_unit="hartree")
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with pytest.raises(HermiticityUnitMismatchError) as exc_info:
        analyzer.execute(record)

    assert exc_info.value.analyzer_energy_unit == "eV"
    assert exc_info.value.record_energy_unit == "hartree"


def test_constructor__unit_validation_precedes_overflow_prone__is_enforced() -> None:
    r"""Evidence ID: SV-HA-014

    Requirement: ----------- A mismatched unit must fail before forming overflow-prone
    ``H-H^dagger``.

    Method: ------ Execute a finite extreme matrix with mismatched units while
    RuntimeWarning is
    promoted to an exception.

    Oracle: ------ The approved operation ordering makes unit mismatch the first public
    failure.

    Acceptance: ---------- Only ``HermiticityUnitMismatchError`` is observed; neither a
    warning nor
    ``HermiticityNumericalError`` occurs first.

    Interpretation: -------------- Passing establishes protected error ordering at the
    public method
    boundary.

    Limitations: ----------- It does not verify overflow residual accuracy, scientific
    validation,
    UQ, or Rust conformance.
    """

    matrix = np.array(
        [[0.0 + 0.0j, 1.0e308 + 0.0j], [-1.0e308 + 0.0j, 0.0 + 0.0j]],
        dtype=np.complex128,
    )
    record = make_record(matrix, energy_unit="hartree")
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(HermiticityUnitMismatchError):
            analyzer.execute(record)


def test_method__require__require_returns_value_equivalent_successful_result() -> None:
    r"""Evidence ID: SV-HA-015

    Requirement: ----------- ``require()`` returns the accepted execution result by
    exact value
    semantics.

    Method: ------ Compare public ``execute()`` and ``require()`` on one exact Hermitian
    record.

    Oracle: ------ The approved method contract promises value equivalence and success
    state.

    Acceptance: ---------- Results compare exactly equal and the required result is
    Hermitian.

    Interpretation: -------------- Passing establishes enforcement success without
    requiring object
    identity.

    Limitations: ----------- Scientific suitability, scientific validation, UQ, and Rust
    conformance
    are not established.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 0.0 + 1.0j], [0.0 - 1.0j, 2.0 + 0.0j]],
        dtype=np.complex128,
    )
    record = make_record(matrix)
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    execute_result = analyzer.execute(record)
    require_result = analyzer.require(record)

    assert require_result == execute_result
    assert require_result.is_hermitian


def test_method__require__retains_failed_result() -> None:
    r"""Evidence ID: SV-HA-016

    Requirement: ----------- A finite residual above tolerance raises an error retaining
    the Result.

    Method: ------ Obtain expected state from ``execute()`` then call ``require()`` on
    the same
    finite real nonsymmetric record.

    Oracle: ------ Public execution supplies authoritative structured state; the
    independently
    obvious off-diagonal difference is exactly one.

    Acceptance: ---------- Error Result equals execution Result, is failed, and retains
    exact roles.

    Interpretation: -------------- Passing establishes Analyzer production of structured
    requirement
    failure.

    Limitations: ----------- Direct exception-constructor invariants and broad nonzero
    numerical
    accuracy are not duplicated; scientific validation, UQ, and Rust are excluded.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 2.0 + 0.0j], [3.0 + 0.0j, 4.0 + 0.0j]],
        dtype=np.complex128,
    )
    record = make_record(matrix)
    analyzer = HermiticityAnalyzer(tolerance=0.5, energy_unit="eV")
    execute_result = analyzer.execute(record)

    with pytest.raises(HermiticityRequirementError) as exc_info:
        analyzer.require(record)

    assert exc_info.value.result == execute_result
    assert not exc_info.value.result.is_hermitian
    assert exc_info.value.result.residual == execute_result.residual
    assert exc_info.value.result.tolerance == analyzer.tolerance
    assert exc_info.value.result.energy_unit == analyzer.energy_unit


@pytest.mark.parametrize(
    "invalid_record",
    [
        pytest.param(None, id="none"),
        pytest.param(False, id="sv_ha_017_boolean"),
        pytest.param(object(), id="sv_ha_017_arbitrary_object"),
    ],
)
def test_method__require__rejects_wrong_input_type(
    invalid_record: Any,
) -> None:
    r"""Evidence ID: SV-HA-017

    Requirement: ----------- ``require()`` accepts only a public ``OperatorRecord``.

    Method: ------ Call ``require()`` itself with representative invalid semantic
    inputs.

    Oracle: ------ Its public signature and stable ``OperatorRecord`` diagnostic are
    approved.

    Acceptance: ---------- Exact ``TypeError`` category names ``OperatorRecord``.

    Interpretation: -------------- Passing shows ``execute()`` evidence is not assumed
    to cover another
    method.

    Limitations: ----------- ``Any``/``cast`` is confined to invalid inputs. Numerical
    accuracy,
    scientific validation, UQ, and Rust conformance are excluded.
    """

    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with pytest.raises(TypeError, match="OperatorRecord"):
        analyzer.require(cast(Any, invalid_record))


def test_method__execute__distinct_analyzers_own_distinct_tolerance_policies() -> None:
    r"""Evidence ID: SV-HA-018

    Requirement: ----------- Tolerance belongs to the ActionObject rather than
    ``OperatorRecord``.

    Method: ------ Analyze one exact-unit record with strict and loose tolerances
    bracketing its
    exactly represented residual.

    Oracle: ------ For the matrix, the nonzero off-diagonal residual is exactly
    ``1e-8``.

    Acceptance: ---------- Strict policy rejects and loose policy accepts while units
    remain
    identical.

    Interpretation: -------------- Passing establishes policy ownership, not which
    policy is
    scientifically apt.

    Limitations: ----------- No scientific tolerance selection, scientific validation,
    UQ, or Rust
    conformance is established.
    """

    matrix = np.array(
        [[1.0 + 0.0j, 0.0 + 0.0j], [1.0e-8 + 0.0j, 2.0 + 0.0j]],
        dtype=np.complex128,
    )
    record = make_record(matrix, energy_unit="eV")
    strict = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")
    loose = HermiticityAnalyzer(tolerance=1.0e-6, energy_unit="eV")

    assert strict.execute(record).is_hermitian is False
    assert loose.execute(record).is_hermitian is True


def test_constructor__nonfinite_residual_is_a_warning_free__is_enforced() -> None:
    r"""Evidence ID: SV-HA-019

    Requirement: ----------- Finite entries whose conjugate subtraction overflows
    produce the closed
    ``NONFINITE_RESIDUAL`` category without leaking ``RuntimeWarning``.

    Method: ------ Execute an overflow-triggering same-unit record with warnings treated
    as
    errors and inspect the public exception enum by identity.

    Oracle: ------ ``1e308 - (-1e308)`` exceeds binary64 range; approved translation
    owns this
    public structured failure.

    Acceptance: ---------- ``HermiticityNumericalError`` is raised and ``error.reason
    is`` the exact
    ``NONFINITE_RESIDUAL`` member, with no warning escaping first.

    Interpretation: -------------- Passing establishes Analyzer warning containment and
    structured
    translation.

    Limitations: ----------- Direct exception invariants are not duplicated. This is
    software failure
    evidence, not scientific validation, UQ, or Rust conformance.
    """

    matrix = np.array(
        [[0.0 + 0.0j, 1.0e308 + 0.0j], [-1.0e308 + 0.0j, 0.0 + 0.0j]],
        dtype=np.complex128,
    )
    record = make_record(matrix)
    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(HermiticityNumericalError) as exc_info:
            analyzer.execute(record)

    assert exc_info.value.reason is HermiticityNumericalErrorCode.NONFINITE_RESIDUAL
