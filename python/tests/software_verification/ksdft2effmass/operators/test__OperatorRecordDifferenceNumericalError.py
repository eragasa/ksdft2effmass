r"""Software verification of ``OperatorRecordDifferenceNumericalError``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the OperatorRecordDifferenceNumericalError facet.
System under test
-----------------
``OperatorRecordDifferenceNumericalError`` is the structured public exception
for numerical failures owned by represented differencing. Its authoritative
machine-readable state is ``code``, which must be an
``OperatorRecordDifferenceNumericalErrorCode``. The currently approved category
is ``NONFINITE_DIFFERENCE``. It means that compatible, individually finite input
matrices produced a nonfinite represented difference during
``Delta H = H_candidate - H_reference``.

Ownership and taxonomy
----------------------
The exception does not subtract matrices or detect nonfinite values. Actual
error production remains owned and tested by ``OperatorRecordDifferencer``. The
exception directly retains the enum member and provides a secondary human-
readable message containing its stable value. Callers should inspect
``error.code`` rather than parse that message.

This exception does not accept residual-analysis categories
``NONFINITE_METRIC``, ``LINEAR_ALGEBRA_FAILURE``, or
``METRIC_ORDER_VIOLATION``. Those belong to residual analysis and its separate
numerical-error type. This module performs no differencer execution and tests no
residual numerical behavior.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-ORDNE-001``
through ``SV-ORDNE-006``. Direct public construction verifies exception
hierarchy, complete structured-code acceptance, exact identity retention,
semantic diagnostic content, invalid-type rejection, free-form-reason exclusion,
and serialization exclusion. The accepted public constructor and source
documentation are the oracle. Passing establishes software structure and error
taxonomy; failure may indicate an exception regression, contract/documentation
mismatch, or evidence defect requiring investigation.

VVUQ and cross-language boundaries
----------------------------------
These tests do not verify floating-point subtraction accuracy, scientific
acceptability of a represented difference, physical compatibility or equivalence,
residual-metric correctness, scientific validation, or uncertainty
quantification. Future Rust mapping is conceptual through the enum category; no
Rust implementation, conformance, or serialized exception format is established.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordDifferenceNumericalError``; collaborators only
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

from enum import Enum
from typing import Any, cast

import pytest

from ksdft2effmass.operators import (
    OperatorRecordDifferenceNumericalError,
    OperatorRecordDifferenceNumericalErrorCode,
)

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordDifferenceNumericalError


class UnrelatedErrorCode(Enum):
    r"""Test-local non-owner enum supporting ``SV-ORDNE-004``.

    Evidence ID: Supporting fixture for ``SV-ORDNE-004``; it owns no separate evidence
    identifier.

    Requirement: A member of another enum is not a difference numerical-error code, even
    when its value resembles the approved machine-readable string.

    Method: Define one local enum member with value ``"nonfinite_difference"`` and
    supply that member at the deliberate invalid constructor boundary.

    Oracle: The public constructor requires nominal membership in
    ``OperatorRecordDifferenceNumericalErrorCode``.

    Interpretation: Rejection demonstrates exact enum ownership rather than value-based
    or
    string-based coercion.

    Limitations: This fixture does not test the production enum's membership, aliases,
    lookup behavior, differencer execution, numerical verification,
    scientific validation, uncertainty quantification, or Rust conformance.
    """

    NONFINITE_DIFFERENCE = "nonfinite_difference"


def test_constructor__public_construction_and_exception_taxonomy__is_enforced() -> None:
    r"""Evidence ID: SV-ORDNE-001

    Requirement: The supported public constructor accepts the approved structured code
    and produces a
    ``ValueError`` and ``Exception`` instance.

    Method: Construct the exception directly through public imports without invoking
    ``OperatorRecordDifferencer`` and inspect only documented inheritance.

    Oracle: The accepted exception contract declares ``ValueError`` inheritance and a
    one-code
    public constructor.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: Passing establishes direct public construction and documented
    hierarchy.

    Limitations: Internal module location, traceback layout, ``Exception.args``,
    differencer
    emission, numerical verification, scientific validation, uncertainty quantification,
    and Rust conformance are not tested.
    """

    error = OperatorRecordDifferenceNumericalError(
        OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    )

    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE,
            id="nonfinite_difference",
        ),
    ],
)
def test_field__accepted_codes_retain_identity__is_exact(
    code: OperatorRecordDifferenceNumericalErrorCode,
) -> None:
    r"""Evidence ID: SV-ORDNE-002

    Requirement: Every current public difference-error code is admitted without
    reconstruction,
    string conversion, or identity loss.

    Method: Parameterize over the complete public enum, construct the exception, and
    compare its
    public ``code`` attribute with the input by identity.

    Oracle: The approved constructor accepts exactly
    ``OperatorRecordDifferenceNumericalErrorCode`` members and retains the supplied
    member.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: Passing establishes complete current enum admission and exact
    structured- code
    identity retention.

    Limitations: Member count, aliases, ``StrEnum`` behavior, lookup taxonomy, exception
    equality/hashability, differencer execution, numerical verification, scientific
    validation, uncertainty quantification, and Rust conformance belong elsewhere or
    remain unperformed.
    """

    error = OperatorRecordDifferenceNumericalError(code)

    assert error.code is code


def test_protocol__str__human_readable_message_summarizes_authoritative_code() -> None:
    r"""Evidence ID: SV-ORDNE-003

    Requirement: The human-readable message identifies an operator-record difference
    numerical
    failure and contains the retained code's stable value, while ``error.code`` remains
    authoritative machine-readable state.

    Method: Construct the exception, inspect semantic substrings in ``str(error)``, and
    verify
    direct code identity.

    Oracle: Accepted source documentation promises a human-readable difference- failure
    message
    containing the enum value, but does not freeze incidental punctuation,
    capitalization, or separators.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: Passing establishes useful human diagnostics without promoting the
    message to a
    machine-parsing API.

    Limitations: Exact full message formatting, ``Exception.args``, differencer
    emission, subtraction
    accuracy, scientific validation, uncertainty quantification, and Rust conformance
    are not tested.
    """

    code = OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    error = OperatorRecordDifferenceNumericalError(code)
    message = str(error)

    assert "operator-record difference numerical failure" in message
    assert code.value in message
    assert error.code is code


@pytest.mark.parametrize(
    "invalid_code",
    [
        pytest.param("nonfinite_difference", id="sv_ordne_004_raw_string"),
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_ordne_004_boolean_true"),
        pytest.param(False, id="sv_ordne_004_boolean_false"),
        pytest.param(
            UnrelatedErrorCode.NONFINITE_DIFFERENCE, id="sv_ordne_004_unrelated_enum"
        ),
        pytest.param(object(), id="sv_ordne_004_arbitrary_object"),
    ],
)
def test_constructor__invalid_code_types_are_rejected__is_enforced(
    invalid_code: object,
) -> None:
    r"""Evidence ID: SV-ORDNE-004

    Requirement: Raw strings, ``None``, Booleans, unrelated enum members, and arbitrary
    objects are
    rejected rather than coerced to the owner enum.

    Method: Pass each representative invalid value directly to the public constructor,
    using
    ``Any`` and ``cast`` only at this deliberate invalid-type boundary.

    Oracle: The accepted constructor requires nominal
    ``OperatorRecordDifferenceNumericalErrorCode`` ownership and documents ``TypeError``
    with the precise owner-type fragment.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: Passing establishes wrong-type taxonomy and prevents
    string/value-based coercion or
    admission of another enum's member.

    Limitations: Valid-code acceptance belongs to ``the owning evidence``. No broad
    exception tuple,
    differencer execution, numerical verification, scientific validation, uncertainty
    quantification, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordDifferenceNumericalError(cast(Any, invalid_code))

    assert "OperatorRecordDifferenceNumericalErrorCode" in str(exc_info.value)


@pytest.mark.parametrize(
    "reason_form",
    [
        pytest.param("positional", id="sv_ordne_005_positional_reason"),
        pytest.param("keyword", id="sv_ordne_005_keyword_reason"),
    ],
)
def test_constructor__input_boundary__free_form_reason_and_extra_argument_are(
    reason_form: str,
) -> None:
    r"""Evidence ID: SV-ORDNE-005

    Requirement: The constructor accepts only one structured code; positional and
    keyword free-form
    reasons raise ``TypeError``, and successful instances expose no public ``reason``
    attribute.

    Method: Invoke the constructor through a deliberate ``Any``-typed invalid- signature
    boundary for each reason form, then inspect an ordinary valid instance for absence
    of ``reason``.

    Oracle: The approved signature has exactly one ``code`` parameter and defines no
    free-form
    reason attribute.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: Passing protects the closed enum-backed taxonomy from contradictory
    or arbitrary
    structured diagnostic state.

    Limitations: Signature-generated ``TypeError`` wording is not frozen. Message text,
    differencer
    execution, numerical verification, scientific validation, uncertainty
    quantification, and Rust conformance are not tested.
    """

    code = OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    invalid_constructor = cast(Any, OperatorRecordDifferenceNumericalError)

    if reason_form == "positional":
        with pytest.raises(TypeError):
            invalid_constructor(code, "synthetic reason")
    else:
        with pytest.raises(TypeError):
            invalid_constructor(code, reason="synthetic reason")

    error = OperatorRecordDifferenceNumericalError(code)
    assert not hasattr(error, "reason")


def test_method__serialize__exception_has_no_serialization_api() -> None:
    r"""Evidence ID: SV-ORDNE-006

    Requirement: The in-memory structured exception exposes none of the six unapproved
    JSON,
    dictionary, serializer, or deserializer method names.

    Method: Inspect both the valid instance and public class for each excluded name.

    Oracle: Schema version 1 serializes ``OperatorRecord`` only; no numerical- exception
    schema
    or independent exception serializer is approved.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: Passing establishes absence of object-owned serialization APIs while
    preserving
    ``error.code`` as in-memory machine-readable state.

    Limitations: Pickling, traceback serialization, future schema design, differencer
    execution,
    numerical verification, scientific validation, uncertainty quantification, and Rust
    conformance are outside this evidence. Future Rust mapping remains conceptual
    through the enum category only.
    """

    error = OperatorRecordDifferenceNumericalError(
        OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    )

    assert all(
        (not hasattr(error, method_name))
        and (not hasattr(OperatorRecordDifferenceNumericalError, method_name))
        for method_name in (
            "to_json",
            "to_dict",
            "serialize",
            "from_json",
            "from_dict",
            "deserialize",
        )
    )
