r"""Software verification for ``HermiticityNumericalError``.

System under test
-----------------
``HermiticityNumericalError`` is the structured public exception for an Analyzer-
owned numerical failure. Its public ``reason`` field is a closed
``HermiticityNumericalErrorCode``, not arbitrary explanatory prose. The exact
enum object supplied to the constructor is retained for machine-readable
inspection; the exception message is a secondary human-readable representation.
``HermiticityAnalyzer`` owns production emission, while these direct constructor
tests independently verify the exception's own public boundary.

Semantic boundary
-----------------
The currently approved reason ``NONFINITE_RESIDUAL`` means that the Analyzer
could not produce a finite binary64 value for

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

This is distinct from ``HermiticityUnitMismatchError`` for exact Analyzer/record
unit disagreement and ``HermiticityRequirementError`` for a finite residual
exceeding a finite tolerance. A numerical error means the requested finite
residual result could not be represented; it does not mean that a finite result
was calculated and found too large.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-HNE-001``
through ``SV-HNE-007``. The approved public exception and Sphinx contracts are
the oracle for ``ValueError`` hierarchy, complete closed-enum admission, exact
``reason`` identity retention, positional/keyword construction, semantic message
content, nominal type rejection, extra-detail exclusion, and absence of an
approved exception serialization API. The enum vocabulary itself remains owned
by ``SV-HNEC-001`` through ``SV-HNEC-006`` and is not retested here.

Interpretation and VVUQ boundaries
----------------------------------
Passing establishes direct exception construction and structured-reason
invariants only. Failure may indicate an exception regression, documentation
mismatch, or evidence defect requiring investigation. These tests invoke no
Analyzer, Result, record, NumPy operation, overflow matrix, warning filter,
private helper, or production emission. They establish no residual numerical
accuracy, overflow-handling correctness, physical Hermiticity, scientific
validation, uncertainty quantification, Rust implementation, or Rust conformance.
A future Rust mapping would use a closed error enum, but no Rust evidence or
serialized numerical-exception format is approved.
"""

from enum import Enum
from typing import Any, cast

import pytest

from ksdft2effmass.operators import (
    HermiticityNumericalError,
    HermiticityNumericalErrorCode,
)

pytestmark = pytest.mark.software_verification


class UnrelatedReason(Enum):
    """Test-local non-owner enum supporting ``SV-HNE-005``.

    Evidence ID
        Supporting fixture for ``SV-HNE-005``; it owns no separate identifier.
    Requirement
        An enum member from another nominal taxonomy is not a
        ``HermiticityNumericalErrorCode``, even when its value matches the
        approved machine-readable string.
    Method
        Define one synthetic local member with value ``nonfinite_residual`` and
        supply it only at the deliberate invalid constructor boundary.
    Oracle
        The approved constructor requires nominal membership in
        ``HermiticityNumericalErrorCode`` rather than enum-like shape or value.
    Acceptance
        The owning invalid-input test rejects this member with ``TypeError``.
    Interpretation
        Rejection establishes closed enum ownership without raw-value coercion.
    Limitations
        This fixture does not inspect enum members, aliases, lookups, Analyzer
        behavior, numerical verification, scientific validation, uncertainty
        quantification, or Rust conformance.
    """

    NONFINITE_RESIDUAL = "nonfinite_residual"


def test_public_construction_and_exception_taxonomy() -> None:
    """SV-HNE-001: construct the public structured ``ValueError`` subtype.

    Evidence ID
        ``SV-HNE-001``.
    Requirement
        One approved structured reason directly constructs
        ``HermiticityNumericalError``, which remains a ``ValueError`` and an
        ``Exception``.
    Method
        Construct through public imports without invoking the Analyzer and
        inspect only documented inheritance.
    Oracle
        The approved public exception contract specifies ``ValueError``
        inheritance and a one-reason constructor.
    Acceptance
        Construction succeeds and both hierarchy checks are true.
    Interpretation
        Passing establishes public direct construction and exception taxonomy.
    Limitations
        ``Exception.args``, traceback formatting, source location, hashability,
        pickling, private state, Analyzer emission, numerical verification,
        scientific validation, UQ, and Rust conformance are untested.
    """

    reason = HermiticityNumericalErrorCode.NONFINITE_RESIDUAL

    error = HermiticityNumericalError(reason)

    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


@pytest.mark.parametrize(
    "reason",
    [
        pytest.param(
            reason,
            id=f"SV-HNE-002-{reason.value.replace('_', '-')}",
        )
        for reason in tuple(HermiticityNumericalErrorCode)
    ],
)
def test_complete_structured_reason_acceptance_and_identity_retention(
    reason: HermiticityNumericalErrorCode,
) -> None:
    """SV-HNE-002: accept every current reason and retain exact identity.

    Evidence ID
        ``SV-HNE-002``; parameter IDs derive from stable reason values without
        creating additional evidence identifiers.
    Requirement
        Every current closed-enum member is accepted and retained through the
        public ``reason`` field without reconstruction or string conversion.
    Method
        Parameterize over the complete public enum, construct directly, and
        compare the retained field with the supplied member by identity.
    Oracle
        The approved exception contract accepts exactly
        ``HermiticityNumericalErrorCode`` members and retains the supplied object.
    Acceptance
        ``error.reason is reason`` for every current member.
    Interpretation
        Passing establishes complete current reason admission and exact identity
        retention; the current enum contains only ``NONFINITE_RESIDUAL``.
    Limitations
        Member count, aliases, ``StrEnum`` behavior, and lookup semantics belong
        to ``SV-HNEC`` evidence. Analyzer emission, numerical verification,
        scientific validation, UQ, and Rust conformance are not tested.
    """

    error = HermiticityNumericalError(reason)

    assert error.reason is reason


def test_positional_and_keyword_construction_retain_the_same_reason() -> None:
    """SV-HNE-003: verify equivalent supported constructor argument forms.

    Evidence ID
        ``SV-HNE-003``.
    Requirement
        Positional and ``reason=`` keyword construction both retain the canonical
        public enum member.
    Method
        Construct two distinct exception objects with the two supported call
        forms and inspect each public ``reason`` field by identity.
    Oracle
        The approved public signature names one parameter ``reason`` and Python
        supports positional or matching keyword binding.
    Acceptance
        Both fields are the canonical ``NONFINITE_RESIDUAL`` singleton.
    Interpretation
        Passing establishes constructor-form equivalence for retained structured
        state, not exception-object equality.
    Limitations
        No exception value-equality contract, Analyzer emission, numerical
        verification, scientific validation, uncertainty quantification, or
        Rust conformance is tested.
    """

    reason = HermiticityNumericalErrorCode.NONFINITE_RESIDUAL

    positional = HermiticityNumericalError(reason)
    keyword = HermiticityNumericalError(reason=reason)

    assert positional.reason is HermiticityNumericalErrorCode.NONFINITE_RESIDUAL
    assert keyword.reason is HermiticityNumericalErrorCode.NONFINITE_RESIDUAL


def test_human_readable_structured_reason_summary() -> None:
    """SV-HNE-004: verify only documented stable message semantics.

    Evidence ID
        ``SV-HNE-004``.
    Requirement
        The human-readable message identifies a Hermiticity numerical failure and
        contains the stable retained reason value ``nonfinite_residual``.
    Method
        Construct directly, case-fold only the failure phrase, and inspect the
        literal stable reason value without asserting full message equality.
    Oracle
        Approved public documentation promises a concise failure summary
        containing the enum value, not fixed punctuation or separators.
    Acceptance
        Both semantic failure content and the stable reason value occur, while
        ``error.reason`` remains the canonical structured category.
    Interpretation
        Passing establishes a useful secondary diagnostic without requiring
        callers to parse it for machine-readable state.
    Limitations
        Full formatting, capitalization, punctuation, Analyzer emission,
        numerical accuracy, scientific validation, UQ, and Rust conformance are
        not compatibility guarantees or tested evidence.
    """

    reason = HermiticityNumericalErrorCode.NONFINITE_RESIDUAL
    error = HermiticityNumericalError(reason)
    message = str(error)

    assert "hermiticity numerical failure" in message.casefold()
    assert "nonfinite_residual" in message
    assert error.reason is reason


@pytest.mark.parametrize(
    "invalid_reason",
    [
        pytest.param(None, id="SV-HNE-005-none"),
        pytest.param(True, id="SV-HNE-005-boolean-true"),
        pytest.param(False, id="SV-HNE-005-boolean-false"),
        pytest.param(1, id="SV-HNE-005-integer"),
        pytest.param("nonfinite_residual", id="SV-HNE-005-raw-string"),
        pytest.param(
            UnrelatedReason.NONFINITE_RESIDUAL,
            id="SV-HNE-005-unrelated-enum",
        ),
        pytest.param(object(), id="SV-HNE-005-arbitrary-object"),
    ],
)
def test_invalid_reason_types_are_rejected(invalid_reason: object) -> None:
    """SV-HNE-005: reject non-owner reason values with ``TypeError``.

    Evidence ID
        ``SV-HNE-005``; parameter IDs identify each distinct semantic type.
    Requirement
        ``None``, Booleans, integer, one raw string, unrelated enum member, and
        arbitrary object are rejected rather than coerced to the owner enum.
    Method
        Pass each independently collected value using ``Any`` and ``cast`` only
        at this deliberate invalid constructor boundary.
    Oracle
        The approved constructor requires nominal
        ``HermiticityNumericalErrorCode`` ownership and documents ``TypeError``
        with the stable owner-type fragment.
    Acceptance
        Every input raises exactly ``TypeError`` naming
        ``HermiticityNumericalErrorCode``.
    Interpretation
        Passing establishes closed structured-reason typing and no raw-string or
        enum-like coercion.
    Limitations
        The raw string appears once; its equivalence to the enum's string value
        is not duplicated. No Analyzer, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        HermiticityNumericalError(cast(Any, invalid_reason))

    assert "HermiticityNumericalErrorCode" in str(exc_info.value)


@pytest.mark.parametrize(
    "detail_form",
    [
        pytest.param(
            "positional",
            id="SV-HNE-006-extra-positional-detail",
        ),
        pytest.param("keyword", id="SV-HNE-006-keyword-detail"),
    ],
)
def test_additional_free_form_detail_is_excluded(detail_form: str) -> None:
    """SV-HNE-006: reject arbitrary extra detail and expose no detail state.

    Evidence ID
        ``SV-HNE-006``; parameter IDs distinguish positional and keyword forms.
    Requirement
        The approved structured ``reason`` is the sole constructor state;
        additional arbitrary detail raises ``TypeError`` and is not exposed.
    Method
        Invoke an ``Any``-typed constructor only at each deliberate invalid-
        signature boundary, then inspect a valid exception for ``detail``.
    Oracle
        The approved one-parameter signature and enum-backed reason model define
        no additional free-form detail parameter or attribute.
    Acceptance
        Both invalid forms raise exactly ``TypeError`` and a valid instance has
        no public ``detail`` attribute.
    Interpretation
        Passing prevents arbitrary prose from competing with the structured
        ``reason`` category.
    Limitations
        Signature-generated ``TypeError`` wording is not frozen. The approved
        ``reason`` field remains present. Analyzer emission, numerical
        verification, scientific validation, UQ, and Rust conformance are not
        tested.
    """

    reason = HermiticityNumericalErrorCode.NONFINITE_RESIDUAL
    invalid_constructor = cast(Any, HermiticityNumericalError)

    if detail_form == "positional":
        with pytest.raises(TypeError):
            invalid_constructor(reason, "synthetic detail")
    else:
        with pytest.raises(TypeError):
            invalid_constructor(reason, detail="synthetic detail")

    error = HermiticityNumericalError(reason)
    assert not hasattr(error, "detail")


def test_exception_has_no_independent_serialization_api() -> None:
    """SV-HNE-007: verify exclusion of exception serialization methods.

    Evidence ID
        ``SV-HNE-007``.
    Requirement
        The in-memory structured exception exposes none of the six unapproved
        JSON, dictionary, serializer, or deserializer method names.
    Method
        Inspect both a valid instance and the public class for each excluded
        method.
    Oracle
        ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; no
        numerical-exception JSON schema or independent serializer is approved.
    Acceptance
        Every excluded method name is absent from both instance and class.
    Interpretation
        Passing establishes serialization exclusion while preserving ``reason``
        as the in-memory machine-readable category.
    Limitations
        ``StrEnum`` compatibility does not create a wire format. Pickling and
        future schemas are unspecified; no Analyzer emission, numerical
        verification, scientific validation, UQ, Rust serialization, or Rust
        conformance is established.
    """

    error = HermiticityNumericalError(HermiticityNumericalErrorCode.NONFINITE_RESIDUAL)

    for method_name in (
        "to_json",
        "to_dict",
        "serialize",
        "from_json",
        "from_dict",
        "deserialize",
    ):
        assert not hasattr(error, method_name)
        assert not hasattr(HermiticityNumericalError, method_name)
