r"""Software verification for ``OperatorRecordCompatibilityIssue``.

System under test
-----------------
The system under test is the immutable slotted compatibility Issue value object.

Evidence class
--------------
This cohesive module provides software-verification evidence ``SV-OCI-001``
through ``SV-OCI-007``. It applies no numerical-verification,
scientific-validation, or uncertainty-quantification marker.

Stored state
------------
An Issue stores exactly one authoritative public field,
``code: OperatorRecordCompatibilityMismatchCode``. Enum-member identity is the
machine-readable state; raw strings are not silently converted.

Derived state
-------------
``description`` is a canonical property derived as
``issue.description == issue.code.description``. It is not stored or independently
editable, preventing contradictory code/text combinations.

Canonical-description ownership
-------------------------------
The mismatch-code enum owns exact description text under ``SV-OCMC-005``. This
module verifies only that every Issue derives and exposes its code's description;
it does not duplicate the enum's complete expected-description table or
uniqueness evidence.

Test strategy, oracle, and acceptance criteria
-----------------------------------------------
Tests construct valid Issues, cover every public code, reject representative
non-code and free-form-description inputs, exercise frozen slotted state, compare
exact value state, and audit absent serialization APIs. The oracle is the
approved public source and Sphinx contract: one dataclass field with the exact
public enum annotation, public enum-member identity and description derivation,
documented constructor validation, frozen slotted DataObject architecture, exact
value semantics, and explicit serialization exclusion. Passing means the Python
Issue preserves one authoritative mismatch code and consistently derives its
canonical description. Failure may indicate an Issue regression, contract or
Sphinx synchronization defect, or evidence defect requiring investigation.

Equality semantics
------------------
Equality is exact structural equality by authoritative code. It is not text
comparison, approximate numerical equality, or evidence that records are
compatible. Hash behavior was audited but is not asserted because no explicit
public hashability or unhashability contract is established.

Serialization exclusion
-----------------------
The Issue has no independent wire-format contract. Future compatibility-result
serialization requires an explicitly approved serializer and versioned schema.

Python/Rust representation boundary
-----------------------------------
The Python shape is conceptually portable to a Rust value object containing one
enum field and a derived description method. This module does not implement or
verify a Rust representation or conformance.

Scientific-validation status
----------------------------
Scientific validation has not been performed. Passing does not establish mismatch
reachability, analyzer correctness, actual operator compatibility, or physical
model validity.

UQ status
---------
Uncertainty quantification has not been performed. This structural value-object
contract contains no uncertainty model or propagation procedure.
"""

from dataclasses import FrozenInstanceError, fields
from enum import StrEnum
from typing import Any, get_type_hints

import pytest

from ksdft2effmass.operators import (
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
)

pytestmark = pytest.mark.software_verification


class UnrelatedCode(StrEnum):
    """Local unrelated enum used only to verify exact public code typing."""

    VALUE = "unrelated_code"


def test_construct_issue_from_public_mismatch_code() -> None:
    """SV-OCI-001: construct an Issue from one public mismatch code.

    Requirement
        Construction requires only one authoritative public mismatch-code member.
    Method
        Construct with ``ENERGY_UNIT_MISMATCH``; inspect public state and the
        documented dataclass field names and resolved public annotation.
    Oracle
        The approved public contract declares exactly one stored field, ``code``,
        typed as ``OperatorRecordCompatibilityMismatchCode``; the enum property
        owns the approved description text.
    Acceptance
        Field metadata and annotation match exactly, ``code`` retains enum
        identity, and ``description`` derives from the code without a text
        argument.
    Interpretation
        Passing verifies enum-member identity as authoritative machine state.
    Limitations
        One representative construction does not establish all-code derivation,
        analyzer reachability, or actual operator compatibility.
    """

    code = OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH

    issue = OperatorRecordCompatibilityIssue(code)

    assert tuple(field.name for field in fields(OperatorRecordCompatibilityIssue)) == (
        "code",
    )
    assert get_type_hints(OperatorRecordCompatibilityIssue) == {
        "code": OperatorRecordCompatibilityMismatchCode
    }
    assert issue.code is code
    assert issue.description == issue.code.description


@pytest.mark.parametrize(
    "code",
    tuple(OperatorRecordCompatibilityMismatchCode),
    ids=lambda code: code.value,
)
def test_derive_canonical_description_for_every_mismatch_code(
    code: OperatorRecordCompatibilityMismatchCode,
) -> None:
    """SV-OCI-002: derive the canonical description for every public code.

    Requirement
        Every public mismatch code must construct an Issue whose description is
        derived directly from the authoritative enum member.
    Method
        Parameterize over public enum iteration and inspect Issue code identity
        and description properties.
    Oracle
        Public enum iteration supplies the complete member set, and each enum
        member's public ``description`` is the canonical derivation source.
    Acceptance
        Every Issue retains the code singleton and exposes its nonempty,
        whitespace-trimmed built-in string description exactly.
    Interpretation
        Passing establishes complete Issue-to-code description derivation.
    Limitations
        Exact wording and description uniqueness belong to ``SV-OCMC-005`` and
        are deliberately not re-specified here; reachability is not tested.
    """

    issue = OperatorRecordCompatibilityIssue(code)

    assert issue.code is code
    assert issue.description == code.description
    assert type(issue.description) is str
    assert issue.description != ""
    assert issue.description == issue.description.strip()


@pytest.mark.parametrize(
    "invalid_code",
    [
        pytest.param("energy_unit_mismatch", id="raw-machine-string"),
        pytest.param(None, id="none"),
        pytest.param(True, id="python-boolean"),
        pytest.param(object(), id="arbitrary-object"),
        pytest.param(UnrelatedCode.VALUE, id="unrelated-enum-member"),
    ],
)
def test_reject_values_that_are_not_public_mismatch_codes(
    invalid_code: Any,
) -> None:
    """SV-OCI-003: reject values outside the public mismatch-code enum.

    Requirement
        ``code`` must be an ``OperatorRecordCompatibilityMismatchCode``; raw
        values and unrelated types are not coerced.
    Method
        Construct with representative string, null, Boolean, object, and
        unrelated-enum inputs.
    Oracle
        The public constructor contract accepts only the mismatch-code enum and
        documents ``TypeError`` without raw-value coercion.
    Acceptance
        Each input raises ``TypeError`` with a field-specific diagnostic naming
        ``OperatorRecordCompatibilityMismatchCode``.
    Interpretation
        Passing requires callers to explicitly select or construct the public
        enum member before constructing an Issue.
    Limitations
        This is representative type-boundary coverage, not exhaustive Python
        object enumeration or analyzer behavior.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordCompatibilityIssue(invalid_code)

    diagnostic = str(exc_info.value)
    assert "compatibility issue code" in diagnostic
    assert "OperatorRecordCompatibilityMismatchCode" in diagnostic


def test_reject_independently_supplied_free_form_descriptions() -> None:
    """SV-OCI-004: reject positional and keyword free-form descriptions.

    Requirement
        The constructor accepts only ``code`` and cannot store independently
        supplied description text.
    Method
        Attempt both a second positional argument and an undeclared description
        keyword through the public constructor.
    Oracle
        The approved constructor contract contains only ``code`` and explicitly
        excludes independently supplied description state.
    Acceptance
        Each unsupported call raises ``TypeError`` without depending on complete
        interpreter-generated message wording.
    Interpretation
        Structural rejection prevents contradictory code/description states.
    Limitations
        The test does not make interpreter-generated diagnostic text public API.
    """

    code = OperatorRecordCompatibilityMismatchCode.MATRIX_DIMENSION_MISMATCH

    with pytest.raises(TypeError):
        OperatorRecordCompatibilityIssue(code, "free-form text")  # type: ignore[call-arg]

    with pytest.raises(TypeError):
        OperatorRecordCompatibilityIssue(  # type: ignore[call-arg]
            code=code,
            description="free-form text",
        )


def test_enforce_immutable_slotted_state() -> None:
    """SV-OCI-005: enforce immutable declared state without dynamic fields.

    Requirement
        Authoritative code, derived description, and object shape remain
        unchanged after construction; no per-instance dictionary is exposed.
    Method
        Attempt assignment to ``code``, ``description``, and one undeclared
        attribute, then inspect the documented slotted-object boundary.
    Oracle
        The approved frozen, slotted DataObject architecture requires assignment
        rejection and no per-instance dynamic-attribute dictionary.
    Acceptance
        Every assignment raises exactly ``FrozenInstanceError`` and the instance
        has no ``__dict__``.
    Interpretation
        Passing protects compatibility-audit evidence from ordinary mutation.
    Limitations
        No private attributes or invariant-bypass techniques are inspected.
    """

    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH
    )

    with pytest.raises(FrozenInstanceError):
        issue.code = OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        issue.description = "free-form text"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        issue.unexpected = "dynamic state"  # type: ignore[attr-defined]

    assert not hasattr(issue, "__dict__")


def test_exact_structural_equality_by_mismatch_code() -> None:
    """SV-OCI-006: provide exact structural equality by authoritative code.

    Requirement
        Independently constructed Issues compare by their sole stored code field.
    Method
        Compare two Issues with one code, an Issue with a different code, and an
        unrelated object.
    Oracle
        The public exact DataObject equality contract uses the sole authoritative
        ``code`` field and defines no text or approximate comparison policy.
    Acceptance
        Same-code Issues are equal; different-code and unrelated values are not.
    Interpretation
        Passing establishes exact code-based value equality, not free-form text
        comparison or approximate numerical equality.
    Limitations
        Equality does not prove that actual records are compatible. Hash behavior
        is intentionally not asserted because it is not an explicit contract.
    """

    same_code_left = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    )
    same_code_right = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
    )
    different_code = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.BASIS_KIND_MISMATCH
    )

    assert same_code_left == same_code_right
    assert same_code_left != different_code
    assert same_code_left != object()


@pytest.mark.parametrize(
    "api_name",
    ["to_json", "from_json", "to_dict", "from_dict", "serialize", "deserialize"],
)
def test_exclude_unsupported_serialization_apis(api_name: str) -> None:
    """SV-OCI-007: exclude unsupported independent serialization APIs.

    Requirement
        The Issue exposes none of the listed object-owned serialization methods.
    Method
        Inspect both the public class and a valid instance for each API name.
    Oracle
        The approved architecture assigns future wire formats to an explicit
        serializer and versioned schema, not to this Issue value object.
    Acceptance
        Every named API is absent from both surfaces.
    Interpretation
        Passing preserves serializer ownership and the absence of an Issue wire
        format.
    Limitations
        Future compatibility-result serialization requires separate approval, an
        explicit serializer ActionObject, and a versioned schema.
    """

    issue = OperatorRecordCompatibilityIssue(
        OperatorRecordCompatibilityMismatchCode.STATE_SPACE_KIND_MISMATCH
    )

    assert not hasattr(OperatorRecordCompatibilityIssue, api_name)
    assert not hasattr(issue, api_name)
