r"""Software verification for the represented-difference numerical exception.

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
"""

from enum import Enum
from typing import Any, cast

import pytest

from ksdft2effmass.operators import (
    OperatorRecordDifferenceNumericalError,
    OperatorRecordDifferenceNumericalErrorCode,
)

pytestmark = pytest.mark.software_verification


class UnrelatedErrorCode(Enum):
    """Test-local non-owner enum supporting ``SV-ORDNE-004``.

    Evidence ID
        Supporting fixture for ``SV-ORDNE-004``; it owns no separate evidence
        identifier.
    Requirement
        A member of another enum is not a difference numerical-error code, even
        when its value resembles the approved machine-readable string.
    Method
        Define one local enum member with value ``"nonfinite_difference"`` and
        supply that member at the deliberate invalid constructor boundary.
    Oracle
        The public constructor requires nominal membership in
        ``OperatorRecordDifferenceNumericalErrorCode``.
    Interpretation
        Rejection demonstrates exact enum ownership rather than value-based or
        string-based coercion.
    Limitations
        This fixture does not test the production enum's membership, aliases,
        lookup behavior, differencer execution, numerical verification,
        scientific validation, uncertainty quantification, or Rust conformance.
    """

    NONFINITE_DIFFERENCE = "nonfinite_difference"


def test_public_construction_and_exception_taxonomy() -> None:
    """SV-ORDNE-001: verify public construction and ``ValueError`` taxonomy.

    Evidence ID
        ``SV-ORDNE-001``.
    Requirement
        The supported public constructor accepts the approved structured code
        and produces a ``ValueError`` and ``Exception`` instance.
    Method
        Construct the exception directly through public imports without invoking
        ``OperatorRecordDifferencer`` and inspect only documented inheritance.
    Oracle
        The accepted exception contract declares ``ValueError`` inheritance and
        a one-code public constructor.
    Interpretation
        Passing establishes direct public construction and documented hierarchy.
    Limitations
        Internal module location, traceback layout, ``Exception.args``,
        differencer emission, numerical verification, scientific validation,
        uncertainty quantification, and Rust conformance are not tested.
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
            code,
            id=f"SV-ORDNE-002-{code.value.replace('_', '-')}",
        )
        for code in tuple(OperatorRecordDifferenceNumericalErrorCode)
    ],
)
def test_complete_structured_code_acceptance_and_identity_retention(
    code: OperatorRecordDifferenceNumericalErrorCode,
) -> None:
    """SV-ORDNE-002: accept every public code and retain exact identity.

    Evidence ID
        ``SV-ORDNE-002``; parameter IDs derive from stable public code values
        without creating additional evidence identifiers.
    Requirement
        Every current public difference-error code is admitted without
        reconstruction, string conversion, or identity loss.
    Method
        Parameterize over the complete public enum, construct the exception, and
        compare its public ``code`` attribute with the input by identity.
    Oracle
        The approved constructor accepts exactly
        ``OperatorRecordDifferenceNumericalErrorCode`` members and retains the
        supplied member.
    Interpretation
        Passing establishes complete current enum admission and exact structured-
        code identity retention.
    Limitations
        Member count, aliases, ``StrEnum`` behavior, lookup taxonomy, exception
        equality/hashability, differencer execution, numerical verification,
        scientific validation, uncertainty quantification, and Rust conformance
        belong elsewhere or remain unperformed.
    """

    error = OperatorRecordDifferenceNumericalError(code)

    assert error.code is code


def test_human_readable_message_summarizes_authoritative_code() -> None:
    """SV-ORDNE-003: verify stable semantic diagnostic content.

    Evidence ID
        ``SV-ORDNE-003``.
    Requirement
        The human-readable message identifies an operator-record difference
        numerical failure and contains the retained code's stable value, while
        ``error.code`` remains authoritative machine-readable state.
    Method
        Construct the exception, inspect semantic substrings in ``str(error)``,
        and verify direct code identity.
    Oracle
        Accepted source documentation promises a human-readable difference-
        failure message containing the enum value, but does not freeze incidental
        punctuation, capitalization, or separators.
    Interpretation
        Passing establishes useful human diagnostics without promoting the
        message to a machine-parsing API.
    Limitations
        Exact full message formatting, ``Exception.args``, differencer emission,
        subtraction accuracy, scientific validation, uncertainty quantification,
        and Rust conformance are not tested.
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
        pytest.param("nonfinite_difference", id="SV-ORDNE-004-raw-string"),
        pytest.param(None, id="SV-ORDNE-004-none"),
        pytest.param(True, id="SV-ORDNE-004-boolean-true"),
        pytest.param(False, id="SV-ORDNE-004-boolean-false"),
        pytest.param(
            UnrelatedErrorCode.NONFINITE_DIFFERENCE,
            id="SV-ORDNE-004-unrelated-enum",
        ),
        pytest.param(object(), id="SV-ORDNE-004-arbitrary-object"),
    ],
)
def test_invalid_code_types_are_rejected(invalid_code: object) -> None:
    """SV-ORDNE-004: reject non-owner code values with ``TypeError``.

    Evidence ID
        ``SV-ORDNE-004``; readable parameter IDs distinguish each invalid family.
    Requirement
        Raw strings, ``None``, Booleans, unrelated enum members, and arbitrary
        objects are rejected rather than coerced to the owner enum.
    Method
        Pass each representative invalid value directly to the public constructor,
        using ``Any`` and ``cast`` only at this deliberate invalid-type boundary.
    Oracle
        The accepted constructor requires nominal
        ``OperatorRecordDifferenceNumericalErrorCode`` ownership and documents
        ``TypeError`` with the precise owner-type fragment.
    Interpretation
        Passing establishes wrong-type taxonomy and prevents string/value-based
        coercion or admission of another enum's member.
    Limitations
        Valid-code acceptance belongs to ``SV-ORDNE-002``. No broad exception
        tuple, differencer execution, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordDifferenceNumericalError(cast(Any, invalid_code))

    assert "OperatorRecordDifferenceNumericalErrorCode" in str(exc_info.value)


@pytest.mark.parametrize(
    "reason_form",
    [
        pytest.param("positional", id="SV-ORDNE-005-positional-reason"),
        pytest.param("keyword", id="SV-ORDNE-005-keyword-reason"),
    ],
)
def test_free_form_reason_and_extra_argument_are_excluded(reason_form: str) -> None:
    """SV-ORDNE-005: reject free-form reasons and expose no ``reason`` state.

    Evidence ID
        ``SV-ORDNE-005``; parameter IDs distinguish positional and keyword
        attempts without assigning new evidence identifiers.
    Requirement
        The constructor accepts only one structured code; positional and keyword
        free-form reasons raise ``TypeError``, and successful instances expose no
        public ``reason`` attribute.
    Method
        Invoke the constructor through a deliberate ``Any``-typed invalid-
        signature boundary for each reason form, then inspect an ordinary valid
        instance for absence of ``reason``.
    Oracle
        The approved signature has exactly one ``code`` parameter and defines no
        free-form reason attribute.
    Interpretation
        Passing protects the closed enum-backed taxonomy from contradictory or
        arbitrary structured diagnostic state.
    Limitations
        Signature-generated ``TypeError`` wording is not frozen. Message text,
        differencer execution, numerical verification, scientific validation,
        uncertainty quantification, and Rust conformance are not tested.
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


def test_exception_has_no_independent_serialization_api() -> None:
    """SV-ORDNE-006: verify exclusion of exception serialization methods.

    Evidence ID
        ``SV-ORDNE-006``.
    Requirement
        The in-memory structured exception exposes none of the six unapproved
        JSON, dictionary, serializer, or deserializer method names.
    Method
        Inspect both the valid instance and public class for each excluded name.
    Oracle
        Schema version 1 serializes ``OperatorRecord`` only; no numerical-
        exception schema or independent exception serializer is approved.
    Interpretation
        Passing establishes absence of object-owned serialization APIs while
        preserving ``error.code`` as in-memory machine-readable state.
    Limitations
        Pickling, traceback serialization, future schema design, differencer
        execution, numerical verification, scientific validation, uncertainty
        quantification, and Rust conformance are outside this evidence. Future
        Rust mapping remains conceptual through the enum category only.
    """

    error = OperatorRecordDifferenceNumericalError(
        OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE
    )

    for method_name in (
        "to_json",
        "to_dict",
        "serialize",
        "from_json",
        "from_dict",
        "deserialize",
    ):
        assert not hasattr(error, method_name)
        assert not hasattr(OperatorRecordDifferenceNumericalError, method_name)
