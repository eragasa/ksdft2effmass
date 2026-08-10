r"""Software verification of ``OperatorRecordCompatibilityAnalyzer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the contract facet. System under test
-----------------
The Analyzer is an ActionObject that audits whether two independently valid
``OperatorRecord`` matrices already share the exact finite representation
metadata required for direct subtraction. Compatibility-critical metadata are
matrix dimension, state-space kind, operator kind, ordered basis labels, basis
kind, lattice vectors, boundary conditions, coordinate convention, geometry
length unit, energy unit, and energy-zero convention.

Identity and provenance boundary
--------------------------------
Record, state-space, and basis identifiers, ``Geometry.system``, and provenance
are ignored by the audit. Ignoring them means only that they do not prevent
direct subtraction under the current software contract; it does not establish
that two records describe the same physical system.

Evidence class, strategy, and oracle
------------------------------------
This module provides software-verification evidence ``SV-ORCA-001`` through
``SV-ORCA-003`` and ``SV-ORCA-016`` through ``SV-ORCA-019``. Public construction,
compatible execution, ignored metadata, enforcement, structured error
propagation, and both public input boundaries are exercised. The oracle is the
approved public Analyzer/ResultObject contract and public mismatch-code enum.
Acceptance uses exact types, tuples, role identifiers, enum sequences, values,
and documented diagnostics.

Behavior and exclusions
-----------------------
``execute()`` always returns a complete audit result; ``require()`` returns the
same value-equivalent compatible result or raises a structured
``IncompatibleOperatorRecordsError`` retaining the failed audit. Matching is
exact, not approximate, and issues use canonical deterministic enum order. The
Analyzer performs no matrix subtraction, basis or gauge alignment, energy-zero
alignment, unit conversion, geometry transformation, or provenance comparison.
Failure may indicate an Analyzer regression, a public-contract/documentation
mismatch, or an evidence defect requiring investigation.

VVUQ status
-----------
This is software verification because it checks public construction, control
flow, structured results, and type boundaries. It is not numerical verification
because no numerical approximation is assessed. Scientific validation and
uncertainty quantification have not been performed; synthetic records provide no
physical reference evidence, uncertainty model, or propagation procedure.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordCompatibilityAnalyzer``; collaborators only
construct inputs or expose public outcomes. Accepted public contracts, literal
expected values, Python language semantics, and assigned schema or fixture artifacts
provide the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from collections.abc import Mapping
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
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
    StateSpace,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordCompatibilityAnalyzer

type Cell = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]

VALID_CELL: Cell = (
    (1.0, 0.0, 0.0),
    (0.0, 2.0, 0.0),
    (0.0, 0.0, 3.0),
)


def make_record(
    *,
    identifier: str = "reference-record",
    operator_kind: str = "finite_test_hamiltonian",
    matrix: npt.NDArray[np.complex128] | None = None,
    state_space_identifier: str = "state-space-reference",
    state_space_kind: str = "finite synthetic",
    basis_identifier: str = "basis-reference",
    basis_kind: str = "site basis",
    basis_ordering: tuple[str, ...] = ("a", "b"),
    cell: Cell = VALID_CELL,
    geometry_system: str = "reference system",
    boundary_conditions: str = "periodic",
    coordinate_convention: str = "cartesian row lattice vectors",
    length_unit: str = "angstrom",
    energy_zero: str = "explicit zero",
    energy_unit: str = "eV",
    provenance: Mapping[str, str] | None = None,
) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Fixtures must satisfy every intrinsic record, state-space, basis, cell,
    finite-matrix, and dimension invariant before compatibility analysis.

    Method: Build explicit metadata and a finite ``np.complex128`` matrix. Matrix
    dimension,
    state-space dimension, and basis-ordering length are coupled through ``dimension =
    len(basis_ordering)``.

    Oracle: The public ``OperatorRecord`` construction contract defines those intrinsic
    invariants. Compatibility-critical parameters are matrix dimension, state-space
    kind, operator kind, basis ordering and kind, cell, boundary and coordinate
    conventions, length unit, energy unit, and energy-zero convention.

    Acceptance: Public construction succeeds and returns an intrinsically valid record
    without
    test-side invariant bypass or broad coercion.

    Interpretation: A returned object is an independently valid synthetic record
    suitable for testing
    the Analyzer's public boundary.

    Limitations: Identifiers, geometry-system text, and provenance are identity,
    descriptive, or
    provenance fields deliberately ignored by compatibility. Matrices are finite
    synthetic matrices; no record comes from DFT, Wannierization, experiment, or
    impurity extraction. Construction proves neither physical equivalence nor scientific
    validity. It performs no scientific validation or uncertainty quantification. Notes
    ----- No broad test-side coercion is performed. An explicitly supplied empty
    provenance mapping is preserved; only ``None`` selects the synthetic default.
    """

    if matrix is None:
        matrix = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=np.complex128)
    if provenance is None:
        provenance = {"source": "synthetic test", "physical_system": "reference"}
    # Coupling dimension to ordering ensures the state-space, basis, and matrix
    # can each satisfy their intrinsic dimensional invariants before analysis.
    dimension = len(basis_ordering)
    return OperatorRecord(
        identifier,
        operator_kind,
        matrix,
        StateSpace(state_space_identifier, state_space_kind, dimension),
        Basis(basis_identifier, basis_kind, basis_ordering, True),
        Geometry(
            geometry_system,
            cell,
            boundary_conditions,
            coordinate_convention,
            length_unit,
        ),
        EnergyReference(energy_zero, energy_unit),
        provenance,
    )


def issue_codes(
    result: OperatorRecordCompatibilityResult,
) -> tuple[OperatorRecordCompatibilityMismatchCode, ...]:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Assertions must preserve Analyzer-owned deterministic issue ordering.

    Method: Read each public Issue ``code`` in the ResultObject tuple's existing order;
    no set,
    dictionary, sort, or private method is used.

    Oracle: The public ResultObject exposes ``issues`` as its canonical audit tuple.

    Acceptance: The output contains exactly the public codes in their existing order.

    Interpretation: The returned tuple is a direct projection of public audit state.

    Limitations: This helper performs no compatibility analysis and does not establish
    the enum's
    canonical order independently, scientific validation, or uncertainty quantification.
    """

    return tuple(issue.code for issue in result.issues)


def make_ignored_metadata_candidate(variation: str) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Every ignored identity, descriptive, and provenance field must be
    independently
    reachable while compatibility-critical fields stay equal.

    Method: Select one explicit public-constructor variation by readable case name.

    Oracle: The approved Analyzer contract identifies exactly five ignored fields.

    Acceptance: Construction returns a valid candidate with the requested isolated or
    explicitly
    combined ignored-field variation.

    Interpretation: Each returned candidate isolates one ignored-field boundary, except
    the explicitly
    named combined case.

    Limitations: Compatibility of these synthetic records establishes subtractability
    only, not
    common physical-system identity, scientific validation, or uncertainty
    quantification.
    """

    match variation:
        case "operator-record-identifier":
            return make_record(identifier="candidate-record")
        case "state-space-identifier":
            return make_record(state_space_identifier="state-space-candidate")
        case "basis-identifier":
            return make_record(basis_identifier="basis-candidate")
        case "geometry-system":
            return make_record(geometry_system="candidate descriptive system")
        case "provenance":
            return make_record(provenance={})
        case "combined-ignored-metadata":
            return make_record(
                identifier="candidate-record",
                state_space_identifier="state-space-candidate",
                basis_identifier="basis-candidate",
                geometry_system="candidate descriptive system",
                provenance={"source": "independent synthetic source"},
            )
        case _:
            raise ValueError(f"unknown ignored-metadata variation: {variation}")


def test_constructor__default_public_analyzer_construction__is_enforced() -> None:
    r"""Evidence ID: SV-ORCA-001

    Requirement: The public ActionObject is default-constructible.

    Method: Invoke its public constructor without arguments.

    Oracle: The approved public API exposes a stateless default Analyzer.

    Acceptance: Construction returns ``OperatorRecordCompatibilityAnalyzer``.

    Interpretation: Passing establishes public construction, not rule correctness.

    Limitations: No record pair is analyzed; no scientific validation or uncertainty
    quantification
    is performed.
    """

    analyzer = OperatorRecordCompatibilityAnalyzer()

    assert isinstance(analyzer, OperatorRecordCompatibilityAnalyzer)


def test_method__execute__execute_constructs_complete_compatible_audit_result() -> None:
    r"""Evidence ID: SV-ORCA-002

    Requirement: ``execute()`` returns the public compatible audit with input roles and
    the complete
    canonical applied-rule sequence.

    Method: Analyze two independently constructed records with equal critical metadata
    and
    distinct role identifiers.

    Oracle: The public ResultObject contract and enum iteration define exact output.

    Acceptance: Type, compatibility, empty issues, identifiers, and rules all match.

    Interpretation: Passing establishes Analyzer-owned ResultObject construction without
    duplicating
    direct-constructor invariants owned by SV-ORCAR evidence.

    Limitations: Synthetic compatibility is not physical equivalence, scientific
    validation, or
    uncertainty quantification.
    """

    reference = make_record(identifier="reference-role")
    candidate = make_record(identifier="candidate-role")

    result = OperatorRecordCompatibilityAnalyzer().execute(reference, candidate)

    assert isinstance(result, OperatorRecordCompatibilityResult)
    assert result.is_compatible is True
    assert result.issues == ()
    assert result.reference_identifier == reference.identifier
    assert result.candidate_identifier == candidate.identifier
    assert result.rules_applied == tuple(OperatorRecordCompatibilityMismatchCode)


@pytest.mark.parametrize(
    "variation",
    [
        pytest.param("operator-record-identifier", id="identifier"),
        pytest.param("state-space-identifier", id="identifier"),
        pytest.param("basis-identifier", id="identifier"),
        pytest.param("geometry-system", id="system"),
        pytest.param("provenance", id="provenance_empty_mapping"),
        pytest.param(
            "combined-ignored-metadata", id="sv_orca_003_combined_ignored_metadata"
        ),
    ],
)
def test_field__ignored_identity_descriptive_and_provenance_metadata__is_exact(
    variation: str,
) -> None:
    r"""Evidence ID: SV-ORCA-003

    Requirement: Record, state-space, and basis identifiers, geometry-system text, and
    provenance do
    not prevent direct subtraction when critical fields match.

    Method: Independently vary each ignored field, plus one combined case, while
    constructing
    both records through valid public constructors.

    Oracle: The approved exact-compatibility field inventory excludes these fields.

    Acceptance: Every case is compatible and has no issues.

    Interpretation: Passing distinguishes representation compatibility from identity and
    provenance
    equality.

    Limitations: Ignoring a field does not prove a common physical system, equivalent
    DFT or Wannier
    provenance, scientific acceptability of subtraction, or scientific validation; no
    uncertainty quantification is performed.
    """

    reference = make_record()
    candidate = make_ignored_metadata_candidate(variation)

    result = OperatorRecordCompatibilityAnalyzer().execute(reference, candidate)

    assert result.is_compatible is True
    assert result.issues == ()


def test_method__require__require_returns_value_equivalent_compatible_audit() -> None:
    r"""Evidence ID: SV-ORCA-016

    Requirement: ``require()`` returns a compatible audit equal to ``execute()`` output.

    Method: Invoke both public methods on the same independently valid pair.

    Oracle: The documented ``require()`` success contract is the complete audit.

    Acceptance: Results compare equal and the required result is compatible.

    Interpretation: Passing establishes value-equivalent public behavior without
    imposing an
    undocumented object-identity requirement.

    Limitations: No incompatible branch, physical equivalence, scientific validation, or
    uncertainty
    quantification is established.
    """

    analyzer = OperatorRecordCompatibilityAnalyzer()
    reference = make_record(identifier="reference-role")
    candidate = make_record(identifier="candidate-role")

    execute_result = analyzer.execute(reference, candidate)
    require_result = analyzer.require(reference, candidate)

    assert require_result == execute_result
    assert require_result.is_compatible is True


def test_method__require__require_raises_error_retaining_complete_incompatible() -> (
    None
):
    r"""Evidence ID: SV-ORCA-017

    Requirement: ``require()`` raises the public structured error retaining the same
    complete audit
    that ``execute()`` returns for the incompatible pair.

    Method: Differ only in energy unit, execute first, then require the same pair.

    Oracle: Exact energy-unit mismatch and structured-error retention are public.

    Acceptance: Error type, retained value, exact code, and role identifiers all match.

    Interpretation: Passing establishes Analyzer-to-error structured propagation.

    Limitations: It does not retest the exception constructor's complete invariant set
    or perform
    scientific validation or uncertainty quantification.
    """

    analyzer = OperatorRecordCompatibilityAnalyzer()
    reference = make_record(identifier="reference-role")
    candidate = make_record(identifier="candidate-role", energy_unit="hartree")
    execute_result = analyzer.execute(reference, candidate)

    with pytest.raises(IncompatibleOperatorRecordsError) as exc_info:
        analyzer.require(reference, candidate)

    retained = exc_info.value.compatibility_result
    assert retained == execute_result
    assert issue_codes(retained) == (
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
    )
    assert retained.reference_identifier == reference.identifier
    assert retained.candidate_identifier == candidate.identifier


@pytest.mark.parametrize(
    ("invalid_role", "expected_message"),
    [
        pytest.param(
            "reference", "reference must be an OperatorRecord", id="invalid_reference"
        ),
        pytest.param(
            "candidate", "candidate must be an OperatorRecord", id="invalid_candidate"
        ),
    ],
)
def test_method__execute__execute_rejects_each_invalid_public_input(
    invalid_role: str, expected_message: str
) -> None:
    r"""Evidence ID: SV-ORCA-018

    Requirement: Reference and candidate must each be ``OperatorRecord`` instances.

    Method: Create valid records inside each case and use ``Any``/``cast`` only to cross
    the
    deliberate invalid public boundary for the selected role.

    Oracle: The public method documentation specifies ``TypeError`` and the stable
    role-specific
    diagnostic.

    Acceptance: Exact ``TypeError`` text identifies the invalid input role.

    Interpretation: Passing establishes independent public boundary diagnostics.

    Limitations: It does not exercise malformed records, which public constructors
    reject before
    Analyzer execution, or perform scientific validation or uncertainty quantification.
    """

    analyzer = OperatorRecordCompatibilityAnalyzer()
    reference = make_record()
    candidate = make_record(identifier="candidate")

    with pytest.raises(TypeError) as exc_info:
        if invalid_role == "reference":
            analyzer.execute(cast(Any, object()), candidate)
        else:
            analyzer.execute(reference, cast(Any, object()))

    assert str(exc_info.value) == expected_message


@pytest.mark.parametrize(
    ("invalid_role", "expected_message"),
    [
        pytest.param(
            "reference", "reference must be an OperatorRecord", id="invalid_reference"
        ),
        pytest.param(
            "candidate", "candidate must be an OperatorRecord", id="invalid_candidate"
        ),
    ],
)
def test_method__require__require_rejects_each_invalid_public_input(
    invalid_role: str, expected_message: str
) -> None:
    r"""Evidence ID: SV-ORCA-019

    Requirement: ``require()`` independently documents and enforces both record inputs.

    Method: Create valid records inside each case and cross only the selected public
    type
    boundary with deliberate ``Any``/``cast`` usage.

    Oracle: The public ``require()`` documentation specifies the same role-specific
    ``TypeError`` diagnostics, regardless of current delegation internals.

    Acceptance: Exact ``TypeError`` text identifies the invalid role for each case.

    Interpretation: Passing establishes ``require()`` as an independently tested public
    API.

    Limitations: The test makes no assertion about internal delegation to ``execute()``
    and performs
    no scientific validation or uncertainty quantification.
    """

    analyzer = OperatorRecordCompatibilityAnalyzer()
    reference = make_record()
    candidate = make_record(identifier="candidate")

    with pytest.raises(TypeError) as exc_info:
        if invalid_role == "reference":
            analyzer.require(cast(Any, object()), candidate)
        else:
            analyzer.require(reference, cast(Any, object()))

    assert str(exc_info.value) == expected_message
