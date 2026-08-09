r"""Software verification of ``OperatorRecordCompatibilityMismatchCode``.

Facet and represented meaning

-----------------------------
This class-owned module owns the OperatorRecordCompatibilityMismatchCode facet.
System under test
-----------------
The system under test is ``OperatorRecordCompatibilityMismatchCode``.

Evidence class
--------------
This cohesive module provides software-verification evidence ``SV-OCMC-001``
through ``SV-OCMC-006``. It applies no numerical-verification,
scientific-validation, or uncertainty-quantification marker.

Public contract
---------------
The enum contract comprises exact public member names, stable machine values,
canonical ordering, absence of aliases, Python ``StrEnum`` behavior, lookup
round trips, canonical descriptions, and invalid-lookup exception taxonomy.
``EXPECTED_CONTRACT`` is an independently written executable public contract;
it is not generated dynamically from the enum implementation.

Canonical ordering
------------------
``tuple(OperatorRecordCompatibilityMismatchCode)`` defines the canonical
compatibility-rule order used by compatibility results and analyzers. No extra,
missing, aliased, or reordered public member is accepted.

Machine-readable representation
-------------------------------
Stable ASCII snake-case values are the machine-readable codes. Python string
behavior supports deterministic mapping to other language representations.

Human-readable description ownership
------------------------------------
Each enum member owns one approved canonical public ``description`` for findings
shown to humans. Descriptions do not replace enum values in serialized or
cross-language logic.

Test strategy and acceptance criteria
-------------------------------------
Literal expected names, values, and descriptions are compared with public enum
iteration, ``Enum.__members__``, string behavior, public lookups, and description
access. Passing means the Python enum exactly matches its approved public
enumeration contract. Failure may indicate an enum regression, contract or
Sphinx synchronization defect, or evidence defect requiring investigation.

Reachability exclusion
----------------------
This module does not establish that every code is reachable from independently
valid ``OperatorRecord`` pairs. Reachability and analyzer correctness belong to
``OperatorRecordCompatibilityAnalyzer`` software-verification tests.

Rust-conformance boundary
-------------------------
The Python representation is tested for deterministic cross-language mapping,
but no Rust implementation is proved to exist or conform.

Scientific-validation status
----------------------------
Scientific validation has not been performed. Passing does not establish the
physical compatibility of actual Hamiltonians or validity of a scientific model.

UQ status
---------
Uncertainty quantification has not been performed. The enum contract contains no
uncertainty model or propagation procedure.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordCompatibilityMismatchCode``; collaborators only
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

import enum
import re
from typing import NamedTuple

import pytest

from ksdft2effmass.operators import OperatorRecordCompatibilityMismatchCode

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordCompatibilityMismatchCode


class ExpectedMismatchCodeContract(NamedTuple):
    r"""One immutable row of the independently specified public enum contract.

    Attributes
    ----------
    name
    Exact public Python enum member name.
    value
    Stable machine-readable compatibility mismatch code.
    description
    Approved canonical human-readable compatibility finding description.
    """

    name: str
    value: str
    description: str


# This literal immutable table is the executable expected public contract. It is
# deliberately independent of enum iteration, values, and descriptions so an
# implementation change cannot regenerate its own oracle.
EXPECTED_CONTRACT: tuple[ExpectedMismatchCodeContract, ...] = (
    ExpectedMismatchCodeContract(
        "MATRIX_DIMENSION_MISMATCH",
        "matrix_dimension_mismatch",
        "matrix dimensions must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "STATE_SPACE_KIND_MISMATCH",
        "state_space_kind_mismatch",
        "state-space kind must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "OPERATOR_KIND_MISMATCH",
        "operator_kind_mismatch",
        "operator_kind must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "ORDERED_BASIS_LABELS_MISMATCH",
        "ordered_basis_labels_mismatch",
        "ordered basis labels must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "BASIS_KIND_MISMATCH",
        "basis_kind_mismatch",
        "basis kind must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "LATTICE_VECTORS_MISMATCH",
        "lattice_vectors_mismatch",
        "lattice vectors must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "BOUNDARY_CONDITIONS_MISMATCH",
        "boundary_conditions_mismatch",
        "boundary conditions must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "COORDINATE_CONVENTION_MISMATCH",
        "coordinate_convention_mismatch",
        "coordinate convention must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "GEOMETRY_LENGTH_UNIT_MISMATCH",
        "geometry_length_unit_mismatch",
        "geometry length unit must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "ENERGY_UNIT_MISMATCH",
        "energy_unit_mismatch",
        "energy unit must match exactly",
    ),
    ExpectedMismatchCodeContract(
        "ENERGY_ZERO_CONVENTION_MISMATCH",
        "energy_zero_convention_mismatch",
        "energy-zero convention must match exactly",
    ),
)


def test_field__exact_public_names_values_and_canonical_ordering__is_exact() -> None:
    r"""Evidence ID: SV-OCMC-001

    Requirement: Enum iteration must equal the approved ordered name/value sequence
    without extra,
    missing, or reordered members.

    Method: Compare public iteration pairs with the independent literal contract.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: The two tuples are exactly equal.

    Interpretation: Passing establishes the Python enum's exact iterable public rule
    set.

    Limitations: This does not establish rule reachability or analyzer behavior. Order
    is public
    because compatibility results and analyzers use
    ``tuple(OperatorRecordCompatibilityMismatchCode)`` as canonical order.
    """

    actual = tuple(
        (code.name, code.value) for code in OperatorRecordCompatibilityMismatchCode
    )
    expected = tuple((row.name, row.value) for row in EXPECTED_CONTRACT)

    assert actual == expected


@pytest.mark.parametrize(
    "expected",
    [
        pytest.param(EXPECTED_CONTRACT[0], id="matrix_dimension_mismatch"),
        pytest.param(EXPECTED_CONTRACT[1], id="state_space_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[2], id="operator_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[3], id="ordered_basis_labels_mismatch"),
        pytest.param(EXPECTED_CONTRACT[4], id="basis_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[5], id="lattice_vectors_mismatch"),
        pytest.param(EXPECTED_CONTRACT[6], id="boundary_conditions_mismatch"),
        pytest.param(EXPECTED_CONTRACT[7], id="coordinate_convention_mismatch"),
        pytest.param(EXPECTED_CONTRACT[8], id="geometry_length_unit_mismatch"),
        pytest.param(EXPECTED_CONTRACT[9], id="energy_unit_mismatch"),
        pytest.param(EXPECTED_CONTRACT[10], id="energy_zero_convention_mismatch"),
    ],
)
def test_protocol__str__python_strenum_and_machine_string_behavior(
    expected: ExpectedMismatchCodeContract,
) -> None:
    r"""Evidence ID: SV-OCMC-002

    Requirement: The enum must subclass ``enum.StrEnum`` and every value must be a
    nonempty ASCII
    string satisfying ``^[a-z][a-z0-9_]*$``.

    Method: Resolve each approved name and inspect inheritance, string compatibility,
    exact
    value type, ``str()`` behavior, ASCII encoding, and ``re.fullmatch``.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Every property holds for every expected member.

    Interpretation: Passing verifies the Python representation needed for deterministic
    cross-language
    mapping.

    Limitations: It does not prove that a Rust implementation exists or is conformant.
    """

    code = OperatorRecordCompatibilityMismatchCode[expected.name]

    assert issubclass(OperatorRecordCompatibilityMismatchCode, enum.StrEnum)
    assert isinstance(code, str)
    assert type(code.value) is str
    assert str(code) == code.value
    assert code.value != ""
    code.value.encode("ascii")
    assert re.fullmatch(r"[a-z][a-z0-9_]*", code.value) is not None


@pytest.mark.parametrize(
    "expected",
    [
        pytest.param(EXPECTED_CONTRACT[0], id="matrix_dimension_mismatch"),
        pytest.param(EXPECTED_CONTRACT[1], id="state_space_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[2], id="operator_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[3], id="ordered_basis_labels_mismatch"),
        pytest.param(EXPECTED_CONTRACT[4], id="basis_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[5], id="lattice_vectors_mismatch"),
        pytest.param(EXPECTED_CONTRACT[6], id="boundary_conditions_mismatch"),
        pytest.param(EXPECTED_CONTRACT[7], id="coordinate_convention_mismatch"),
        pytest.param(EXPECTED_CONTRACT[8], id="geometry_length_unit_mismatch"),
        pytest.param(EXPECTED_CONTRACT[9], id="energy_unit_mismatch"),
        pytest.param(EXPECTED_CONTRACT[10], id="energy_zero_convention_mismatch"),
    ],
)
def test_method__getitem__name_and_value_lookup_round_trips(
    expected: ExpectedMismatchCodeContract,
) -> None:
    r"""Evidence ID: SV-OCMC-003

    Requirement: Public construction by stable value and subscription by public name
    must return the
    same canonical enum singleton.

    Method: Resolve the expected member by name, then perform both documented public
    lookup
    forms.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Both lookup results are identical to the resolved member.

    Interpretation: Passing establishes deterministic value-based and name-based lookup.

    Limitations: No private enum internals or compatibility analysis are exercised.
    """

    code = OperatorRecordCompatibilityMismatchCode[expected.name]

    assert OperatorRecordCompatibilityMismatchCode(code.value) is code
    assert OperatorRecordCompatibilityMismatchCode[code.name] is code


def test_field__unique_values_and_absence_of_enum_aliases__is_exact() -> None:
    r"""Evidence ID: SV-OCMC-004

    Requirement: The complete documented ``Enum.__members__`` mapping must contain only
    the expected
    ordered public names, with no aliases, and values are unique.

    Method: Compare member-map and iteration counts, compare ordered member-map names
    with the
    independent contract, and compare value count with set size.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Counts match, names match exactly, and every stable value is unique.

    Interpretation: Passing closes the alias gap left by normal enum iteration, which
    omits aliases.

    Limitations: ``Enum.__members__`` is the documented public Enum API; no
    project-private
    implementation state or rule reachability is tested.
    """

    iterated_codes = tuple(OperatorRecordCompatibilityMismatchCode)
    expected_names = tuple(row.name for row in EXPECTED_CONTRACT)
    stable_values = tuple(code.value for code in iterated_codes)

    assert len(OperatorRecordCompatibilityMismatchCode.__members__) == len(
        iterated_codes
    )
    assert tuple(OperatorRecordCompatibilityMismatchCode.__members__) == expected_names
    assert len(stable_values) == len(set(stable_values))


@pytest.mark.parametrize(
    "expected",
    [
        pytest.param(EXPECTED_CONTRACT[0], id="matrix_dimension_mismatch"),
        pytest.param(EXPECTED_CONTRACT[1], id="state_space_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[2], id="operator_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[3], id="ordered_basis_labels_mismatch"),
        pytest.param(EXPECTED_CONTRACT[4], id="basis_kind_mismatch"),
        pytest.param(EXPECTED_CONTRACT[5], id="lattice_vectors_mismatch"),
        pytest.param(EXPECTED_CONTRACT[6], id="boundary_conditions_mismatch"),
        pytest.param(EXPECTED_CONTRACT[7], id="coordinate_convention_mismatch"),
        pytest.param(EXPECTED_CONTRACT[8], id="geometry_length_unit_mismatch"),
        pytest.param(EXPECTED_CONTRACT[9], id="energy_unit_mismatch"),
        pytest.param(EXPECTED_CONTRACT[10], id="energy_zero_convention_mismatch"),
    ],
)
def test_field__canonical_public_descriptions__is_exact(
    expected: ExpectedMismatchCodeContract,
) -> None:
    r"""Evidence ID: SV-OCMC-005

    Requirement: Every member exposes its approved exact human-readable description as a
    deterministic, nonempty, whitespace-trimmed built-in string.

    Method: Compare two public property reads with the independent description row and
    inspect
    exact type and boundary whitespace.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Both reads equal the approved text and all string invariants hold.

    Interpretation: Passing establishes synchronized human-facing compatibility
    findings; the enum value
    remains the stable machine-readable code.

    Limitations: Descriptions are not replacements for values in serialization or
    cross-language
    logic and do not prove analyzer reachability.
    """

    code = OperatorRecordCompatibilityMismatchCode[expected.name]
    first_description = code.description
    second_description = code.description

    assert type(first_description) is str
    assert first_description != ""
    assert first_description == first_description.strip()
    assert first_description == expected.description
    assert second_description == first_description


def test_method__getitem__invalid_name_and_value_lookup_failures() -> None:
    r"""Evidence ID: SV-OCMC-006

    Requirement: An unknown stable value raises ``ValueError`` and an unknown public
    name raises
    ``KeyError`` through standard enum lookup APIs.

    Method: Perform one invalid value construction and one invalid name subscription.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Each operation raises exactly its intended exception category; no broad
    exception
    tuple or complete message match is used.

    Interpretation: Passing establishes predictable lookup failure categories for
    callers.

    Limitations: Exception-message text and analyzer diagnostics are outside this
    evidence.
    """

    with pytest.raises(ValueError):
        OperatorRecordCompatibilityMismatchCode("not_a_compatibility_code")

    with pytest.raises(KeyError):
        OperatorRecordCompatibilityMismatchCode["NOT_A_COMPATIBILITY_CODE"]
