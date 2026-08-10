r"""Software verification of ``OperatorRecordCompatibilityAnalyzer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the rules facet. System under test
-----------------
The Analyzer is an ActionObject that performs a complete exact audit of the
representation metadata required before direct subtraction of two independently
valid finite ``OperatorRecord`` matrices. Critical fields are matrix dimension,
state-space kind, operator kind, ordered basis labels, basis kind, lattice
vectors, boundary conditions, coordinate convention, geometry length unit,
energy unit, and energy-zero convention. Record, state-space, and basis
identifiers, geometry-system text, and provenance are deliberately ignored.

Evidence class, strategy, and oracle
------------------------------------
This module provides software-verification evidence ``SV-ORCA-004`` through
``SV-ORCA-015``. Each public mismatch code is reached through ordinary valid
public objects, and one valid pair reaches the complete sequence. The oracle is
the approved public compatibility rule inventory and the enum-owned canonical
sequence ``tuple(OperatorRecordCompatibilityMismatchCode)``. Acceptance requires
exact ordered tuples; sets are used only for the separate membership-coverage
assertion and never to determine public issue order.

Exactness, ordering, and exclusions
-----------------------------------
Compatibility matching is exact, not approximate. Issue ordering is public,
deterministic audit ordering from enum declaration order, not discovery order
from a set or dictionary. ``execute()`` returns audit evidence; ``require()``
would enforce that evidence but is contract-tested separately. The Analyzer does
not align bases or gauges, align energy zeros, convert units, transform geometry,
compare provenance, perform matrix subtraction, or establish physical
equivalence. Ignored fields permit direct subtraction only under this software
contract and do not show that records describe the same physical system.

VVUQ status
-----------
This is software verification of public rule execution and deterministic audit
state. It is not numerical verification because no approximation or convergence
is assessed. Scientific validation and uncertainty quantification have not been
performed; the synthetic records supply neither independent physical evidence
nor an uncertainty model and propagation procedure. Failure may indicate an
Analyzer regression, contract/documentation mismatch, or evidence defect that
requires investigation, not scientific invalidity by itself.

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

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
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

    Requirement: Every analyzed fixture must satisfy intrinsic state-space, basis,
    matrix-dimension,
    finite-value, and geometry invariants before analysis.

    Method: Build explicit public metadata and a finite ``np.complex128`` matrix.
    ``dimension =
    len(basis_ordering)`` couples state-space dimension to the valid ordering; supplied
    matrices explicitly match that dimension.

    Oracle: Public record construction defines intrinsic validity. Analyzer-critical
    fields are
    dimension, state-space and operator kinds, ordered labels and basis kind, cell and
    geometry conventions/units, and energy zero/unit.

    Acceptance: Public construction returns an intrinsically valid record without broad
    coercion,
    mutation, or invariant bypass.

    Interpretation: A returned record can reach Analyzer findings without frozen-object
    mutation or
    invariant bypass.

    Limitations: Record/state-space/basis identifiers, geometry-system text, and
    provenance are
    deliberately ignored fields. All matrices and metadata are synthetic: they come from
    no DFT, Wannierization, experiment, or impurity extraction and establish no physical
    equivalence, scientific validation, or uncertainty quantification. Notes ----- The
    helper performs no broad test-side coercion. Explicitly supplied empty provenance is
    preserved; only ``None`` selects the synthetic default.
    """

    if matrix is None:
        matrix = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=np.complex128)
    if provenance is None:
        provenance = {"source": "synthetic test", "physical_system": "reference"}
    # This equality is required so each record is intrinsically valid before
    # the compatibility ActionObject compares it with another valid record.
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

    Requirement: Ordered assertions must observe the ResultObject's existing issue
    order.

    Method: Read public Issue codes sequentially without a set, dictionary, sort, or
    private
    Analyzer method.

    Oracle: ``result.issues`` is the public deterministic audit tuple.

    Acceptance: Output codes exactly preserve the public Issue tuple's existing order.

    Interpretation: The tuple exposes exactly the order returned by ``execute()``.

    Limitations: This projection neither executes rules nor independently defines their
    canonical
    order, scientific validation, or uncertainty quantification.
    """

    return tuple(issue.code for issue in result.issues)


def make_rule_candidate(
    code: OperatorRecordCompatibilityMismatchCode,
) -> OperatorRecord:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Every public mismatch code must be reachable from independently valid
    records, with
    coupled findings retained where validity requires them.

    Method: Select an explicit public-constructor variation for the requested code; no
    mutation,
    invariant bypass, broad coercion, set, or dictionary drives rule execution or
    ordering.

    Oracle: The approved Analyzer rule inventory specifies each isolated variation and
    the
    dimension/ordered-label coupling.

    Acceptance: Construction succeeds with only the documented isolated variation or
    unavoidable
    coupled dimension/ordering variation.

    Interpretation: The returned record differs only in the targeted critical field,
    except that a
    dimension change also requires a valid different label count.

    Limitations: Reachability demonstrates software behavior, not physical
    compatibility, scientific
    acceptability of subtraction, scientific validation, or uncertainty quantification.
    """

    code_type = OperatorRecordCompatibilityMismatchCode
    match code:
        case code_type.MATRIX_DIMENSION_MISMATCH:
            return make_record(
                identifier="candidate",
                matrix=np.eye(3, dtype=np.complex128),
                basis_ordering=("a", "b", "c"),
            )
        case code_type.STATE_SPACE_KIND_MISMATCH:
            return make_record(
                identifier="candidate", state_space_kind="different state space"
            )
        case code_type.OPERATOR_KIND_MISMATCH:
            return make_record(identifier="candidate", operator_kind="different")
        case code_type.ORDERED_BASIS_LABELS_MISMATCH:
            return make_record(identifier="candidate", basis_ordering=("b", "a"))
        case code_type.BASIS_KIND_MISMATCH:
            return make_record(identifier="candidate", basis_kind="different basis")
        case code_type.LATTICE_VECTORS_MISMATCH:
            return make_record(
                identifier="candidate",
                cell=((1.0, 0.0, 0.0), (0.0, 4.0, 0.0), (0.0, 0.0, 3.0)),
            )
        case code_type.BOUNDARY_CONDITIONS_MISMATCH:
            return make_record(identifier="candidate", boundary_conditions="open")
        case code_type.COORDINATE_CONVENTION_MISMATCH:
            return make_record(
                identifier="candidate", coordinate_convention="different convention"
            )
        case code_type.GEOMETRY_LENGTH_UNIT_MISMATCH:
            return make_record(identifier="candidate", length_unit="bohr")
        case code_type.ENERGY_UNIT_MISMATCH:
            return make_record(identifier="candidate", energy_unit="hartree")
        case code_type.ENERGY_ZERO_CONVENTION_MISMATCH:
            return make_record(
                identifier="candidate", energy_zero="valence band maximum"
            )
    raise AssertionError(f"unhandled public mismatch code: {code}")


@pytest.mark.parametrize(
    ("code", "expected_codes"),
    [
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.MATRIX_DIMENSION_MISMATCH,
            (
                OperatorRecordCompatibilityMismatchCode.MATRIX_DIMENSION_MISMATCH,
                OperatorRecordCompatibilityMismatchCode.ORDERED_BASIS_LABELS_MISMATCH,
            ),
            id="matrix_dimension_and_ordered_labels",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH,),
            id="kind",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,),
            id="kind",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.ORDERED_BASIS_LABELS_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.ORDERED_BASIS_LABELS_MISMATCH,),
            id="sv_orca_007_ordered_basis_labels",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH,),
            id="kind",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.LATTICE_VECTORS_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.LATTICE_VECTORS_MISMATCH,),
            id="sv_orca_009_lattice_vectors",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.BOUNDARY_CONDITIONS_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.BOUNDARY_CONDITIONS_MISMATCH,),
            id="boundary_conditions",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.COORDINATE_CONVENTION_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.COORDINATE_CONVENTION_MISMATCH,),
            id="coordinate_convention",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.GEOMETRY_LENGTH_UNIT_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.GEOMETRY_LENGTH_UNIT_MISMATCH,),
            id="length_unit",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,),
            id="unit",
        ),
        pytest.param(
            OperatorRecordCompatibilityMismatchCode.ENERGY_ZERO_CONVENTION_MISMATCH,
            (OperatorRecordCompatibilityMismatchCode.ENERGY_ZERO_CONVENTION_MISMATCH,),
            id="zero_convention",
        ),
    ],
)
def test_method__execute__every_public_mismatch_rule_is_reachable_from_valid(
    code: OperatorRecordCompatibilityMismatchCode,
    expected_codes: tuple[OperatorRecordCompatibilityMismatchCode, ...],
) -> None:
    r"""Evidence ID: SV-ORCA-004

    Requirement: Each public code is observable. Dimension mismatch must produce the
    coupled
    ordered-label finding because valid records require matrix dimension = state-space
    dimension = basis-ordering length; remaining cases change only one critical field
    and produce one code.

    Method: Construct reference and candidate independently through public objects,
    execute the
    Analyzer, and compare the exact ordered code tuple.

    Oracle: The parameter table is the approved rule-to-finding contract, including the
    explicitly non-isolatable dimension finding.

    Acceptance: Every parameter returns exactly its documented ordered tuple.

    Interpretation: Passing establishes rule reachability without malformed-state
    fixtures.

    Limitations: Exact synthetic metadata mismatches are software evidence only; they do
    not assess
    physical equivalence, alignment, scientific validation, or uncertainty
    quantification.
    """

    reference = make_record()
    candidate = make_rule_candidate(code)

    result = OperatorRecordCompatibilityAnalyzer().execute(reference, candidate)

    assert issue_codes(result) == expected_codes


def test_method__execute__orders_all_mismatches() -> None:
    r"""Evidence ID: SV-ORCA-015

    Requirement: A complete multi-finding audit follows public enum order, and every
    public enum
    member is reachable through valid records.

    Method: Compare valid dimension-two and dimension-three records differing in all
    critical
    fields; assert tuple order first, then set membership coverage.

    Oracle: The public enum itself owns canonical ordering, so no second hard-coded
    competing
    sequence is created.

    Acceptance: Ordered issue codes equal the enum tuple and observed membership equals
    the set of
    all public enum members.

    Interpretation: Passing establishes deterministic public audit order and complete
    code reachability;
    set equality is coverage only and does not drive ordering.

    Limitations: The candidate remains intrinsically valid but synthetic. This does not
    establish
    physical equivalence, alignment, scientific validation, or uncertainty
    quantification.
    """

    reference = make_record()
    candidate = make_record(
        identifier="candidate",
        operator_kind="different operator",
        matrix=np.eye(3, dtype=np.complex128),
        state_space_kind="different state space",
        basis_ordering=("c", "b", "a"),
        basis_kind="different basis",
        cell=((2.0, 0.0, 0.0), (0.0, 4.0, 0.0), (0.0, 0.0, 5.0)),
        boundary_conditions="open",
        coordinate_convention="different convention",
        length_unit="bohr",
        energy_zero="different zero",
        energy_unit="hartree",
    )

    result = OperatorRecordCompatibilityAnalyzer().execute(reference, candidate)
    ordered_codes = issue_codes(result)

    assert ordered_codes == tuple(OperatorRecordCompatibilityMismatchCode)
    observed_codes = set(ordered_codes)
    assert observed_codes == set(OperatorRecordCompatibilityMismatchCode)
