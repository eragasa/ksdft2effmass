r"""Software verification for the residual-analysis numerical exception.

System under test
-----------------
``OperatorRecordComparisonNumericalError`` is a structured residual-analysis
numerical failure. Its sole authoritative category field is ``code``. The field
must contain an ``OperatorRecordComparisonNumericalErrorCode`` and accepts all
three closed members: ``NONFINITE_METRIC``, ``LINEAR_ALGEBRA_FAILURE``, and
``METRIC_ORDER_VIOLATION``. Raw strings are rejected rather than coerced. The
former ``reason`` alias is intentionally absent, and the human-readable message
is only a secondary diagnostic that callers must not parse.

Ownership and semantic separation
---------------------------------
Despite the retained ``Comparison`` name, ``OperatorRecordResidualAnalyzer``
owns production emission. ``OperatorRecordComparator`` may propagate the
exception, but it neither creates residual metrics nor owns their error taxonomy.
``NONFINITE_METRIC`` means a residual metric cannot be represented as a finite
binary64 scalar. ``LINEAR_ALGEBRA_FAILURE`` means spectral-norm SVD fails or
returns nonfinite singular values. ``METRIC_ORDER_VIOLATION`` means independently
computed raw metrics violate
``0 <= epsilon_max <= epsilon_2 <= epsilon_F`` by more than the Analyzer-owned
floating-point allowance.

This taxonomy is distinct from ``OperatorRecordDifferenceNumericalError`` for
nonfinite represented subtraction, ``HermiticityNumericalError`` for a
nonrepresentable Hermiticity residual, and ``IncompatibleOperatorRecordsError``
for exact representation-metadata incompatibility.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-ORCNE-001``
through ``SV-ORCNE-008``. Direct public construction verifies hierarchy,
complete enum acceptance and identity retention, supported call forms, semantic
message content, invalid-type rejection, exclusion of the removed ``reason``
alias and arbitrary detail, and absence of independent serialization APIs. The
approved public exception and Sphinx contracts are the oracle. These tests do
not execute numerical algorithms or actual production emission.

Interpretation and VVUQ boundaries
----------------------------------
Passing verifies the direct exception boundary; it does not decide whether a
physical residual is acceptable. Residual-metric accuracy and representable
floating-point behavior are owned by ``NV-ORA`` evidence. Production emission
belongs to ``SV-ORA`` evidence, and Workflow propagation belongs to ``SV-ORC``
evidence. Failure may indicate an exception regression, contract/documentation
mismatch, or evidence defect requiring investigation; it does not by itself
establish a numerical or physical-model error. No scientific-validation or
uncertainty-quantification claim is made. Rust mapping remains conceptual; no
Rust implementation or conformance is established.
"""

from enum import Enum
from typing import Any, cast

import pytest

from ksdft2effmass.operators import (
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonNumericalErrorCode,
)

pytestmark = pytest.mark.software_verification


class UnrelatedErrorCode(Enum):
    """Test-local non-owner enum supporting ``SV-ORCNE-005``.

    Evidence ID
        Supporting fixture for ``SV-ORCNE-005``; it owns no separate evidence
        identifier.
    Requirement
        An unrelated enum member is not an
        ``OperatorRecordComparisonNumericalErrorCode``, even when its value
        resembles an approved code value.
    Method
        Define one synthetic member and supply it only at the deliberate invalid
        constructor boundary.
    Oracle
        The approved constructor requires nominal membership in the owner enum.
    Acceptance
        The owning test rejects this member with exactly ``TypeError``.
    Interpretation
        Rejection establishes enum ownership rather than value-based coercion.
    Limitations
        This fixture does not inspect owner-enum membership, aliases, lookups,
        Analyzer or Workflow behavior, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance.
    """

    NONFINITE_METRIC = "nonfinite_metric"


def test_public_construction_and_exception_taxonomy() -> None:
    """SV-ORCNE-001: verify public construction and exception taxonomy.

    Evidence ID
        ``SV-ORCNE-001``.
    Requirement
        An approved structured code directly constructs a ``ValueError`` and
        ``Exception`` instance.
    Method
        Construct through public imports without invoking the residual Analyzer.
    Oracle
        The approved exception contract specifies ``ValueError`` inheritance and
        a one-code constructor.
    Acceptance
        Construction succeeds and both documented hierarchy checks are true.
    Interpretation
        Passing establishes direct public construction and exception hierarchy.
    Limitations
        ``Exception.args``, source location, traceback layout, hashability,
        pickling, private state, production emission, numerical verification,
        scientific validation, uncertainty quantification, and Rust conformance
        are unspecified or untested.
    """

    error = OperatorRecordComparisonNumericalError(
        OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    )

    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(code, id=f"SV-ORCNE-002-{code.value.replace('_', '-')}")
        for code in tuple(OperatorRecordComparisonNumericalErrorCode)
    ],
)
def test_complete_structured_code_acceptance_and_identity_retention(
    code: OperatorRecordComparisonNumericalErrorCode,
) -> None:
    """SV-ORCNE-002: accept every code and retain exact enum identity.

    Evidence ID
        ``SV-ORCNE-002``; parameter IDs derive from stable public values without
        creating additional evidence identifiers.
    Requirement
        Every approved category is accepted and retained without reconstruction
        or string conversion.
    Method
        Parameterize over the complete public enum, construct directly, and
        compare the public field with the supplied member by identity.
    Oracle
        The approved constructor accepts every owner-enum member and retains the
        exact supplied object through ``error.code``.
    Acceptance
        ``error.code is code`` for all three public members.
    Interpretation
        Passing establishes complete current admission and exact identity
        retention.
    Limitations
        Member count, aliases, ``StrEnum`` behavior, and lookups belong to
        ``SV-ORCNEC`` evidence. Analyzer emission, numerical verification,
        scientific validation, uncertainty quantification, and Rust conformance
        are not tested.
    """

    error = OperatorRecordComparisonNumericalError(code)

    assert error.code is code


def test_positional_and_keyword_construction_retain_the_same_code() -> None:
    """SV-ORCNE-003: verify positional and keyword constructor forms.

    Evidence ID
        ``SV-ORCNE-003``.
    Requirement
        Positional and ``code=`` keyword construction both retain the canonical
        public enum member.
    Method
        Construct distinct exceptions using both supported forms and inspect
        each authoritative field by identity.
    Oracle
        The approved signature names one parameter ``code`` and supports normal
        Python positional or matching-keyword binding.
    Acceptance
        Both fields are the canonical ``NONFINITE_METRIC`` singleton.
    Interpretation
        Passing establishes constructor-form equivalence for structured state.
    Limitations
        Exception-object equality, Analyzer emission, numerical verification,
        scientific validation, uncertainty quantification, and Rust conformance
        are not tested.
    """

    positional = OperatorRecordComparisonNumericalError(
        OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    )
    keyword = OperatorRecordComparisonNumericalError(
        code=OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    )

    assert (
        positional.code is OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    )
    assert keyword.code is OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(code, id=f"SV-ORCNE-004-{code.value.replace('_', '-')}")
        for code in tuple(OperatorRecordComparisonNumericalErrorCode)
    ],
)
def test_human_readable_structured_code_summary(
    code: OperatorRecordComparisonNumericalErrorCode,
) -> None:
    """SV-ORCNE-004: verify documented semantic diagnostic content.

    Evidence ID
        ``SV-ORCNE-004``; parameter IDs cover every public code.
    Requirement
        The secondary message identifies an operator-record residual numerical
        failure and includes the authoritative code's stable value.
    Method
        Construct directly, case-fold the documented semantic phrase, and check
        the literal public code value without asserting full message equality.
    Oracle
        The approved architecture and Sphinx contracts promise semantic
        residual-failure wording and the code value, not exact incidental
        formatting.
    Acceptance
        The semantic phrase and ``code.value`` occur, while identity remains on
        ``error.code``.
    Interpretation
        Passing establishes a useful human diagnostic without making it a
        machine-parsing interface.
    Limitations
        Exact punctuation, capitalization, quoting, separators,
        ``Exception.args``, Analyzer emission, numerical verification,
        scientific validation, uncertainty quantification, and Rust conformance
        are not compatibility guarantees or tested evidence.
    """

    error = OperatorRecordComparisonNumericalError(code)
    message = str(error)

    assert "operator-record residual numerical failure" in message.casefold()
    assert code.value in message
    assert error.code is code


@pytest.mark.parametrize(
    "invalid_code",
    [
        pytest.param(None, id="SV-ORCNE-005-none"),
        pytest.param(True, id="SV-ORCNE-005-boolean-true"),
        pytest.param(False, id="SV-ORCNE-005-boolean-false"),
        pytest.param(1, id="SV-ORCNE-005-integer"),
        pytest.param(
            "nonfinite_metric",
            id="SV-ORCNE-005-raw-nonfinite-metric",
        ),
        pytest.param(
            "linear_algebra_failure",
            id="SV-ORCNE-005-raw-linear-algebra-failure",
        ),
        pytest.param(
            "metric_order_violation",
            id="SV-ORCNE-005-raw-metric-order-violation",
        ),
        pytest.param(
            UnrelatedErrorCode.NONFINITE_METRIC,
            id="SV-ORCNE-005-unrelated-enum",
        ),
        pytest.param(object(), id="SV-ORCNE-005-arbitrary-object"),
    ],
)
def test_invalid_code_types_are_rejected(invalid_code: object) -> None:
    """SV-ORCNE-005: reject every specified non-owner code type.

    Evidence ID
        ``SV-ORCNE-005``; stable parameter IDs identify each invalid family.
    Requirement
        ``None``, Booleans, integer, all three raw code strings, an unrelated
        enum member, and an arbitrary object are rejected without coercion.
    Method
        Supply each independently collected value using ``Any`` and ``cast``
        only at this deliberate invalid constructor boundary.
    Oracle
        The approved constructor requires nominal
        ``OperatorRecordComparisonNumericalErrorCode`` membership and documents
        ``TypeError`` with the owner-type fragment.
    Acceptance
        Every invalid value raises exactly ``TypeError`` naming the owner enum.
    Interpretation
        Passing establishes wrong-type taxonomy and excludes raw-string and
        enum-like coercion.
    Limitations
        Valid-code admission belongs to ``SV-ORCNE-002``. No Analyzer, Workflow,
        numerical verification, scientific validation, uncertainty
        quantification, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        OperatorRecordComparisonNumericalError(cast(Any, invalid_code))

    assert "OperatorRecordComparisonNumericalErrorCode" in str(exc_info.value)


@pytest.mark.parametrize(
    "reason_form",
    [
        pytest.param("attribute", id="SV-ORCNE-006-reason-keyword"),
    ],
)
def test_removed_reason_alias_remains_absent(reason_form: str) -> None:
    """SV-ORCNE-006: protect exclusion of the former ``reason`` alias.

    Evidence ID
        ``SV-ORCNE-006``; the parameter ID records the rejected keyword form.
    Requirement
        ``code`` is the sole public structured category field; valid instances
        expose no ``reason`` and ``reason=`` construction is unsupported.
    Method
        Inspect a valid exception, then invoke an ``Any``-typed constructor at
        the deliberate invalid-signature boundary with ``reason=``.
    Oracle
        The approved correction removed the alias and retains only the one-
        parameter ``code`` signature.
    Acceptance
        The attribute is absent and keyword construction raises exactly
        ``TypeError``.
    Interpretation
        Passing protects the prior correction from accidental compatibility-
        alias restoration.
    Limitations
        Incidental signature-generated diagnostic wording is not frozen.
        Analyzer emission, numerical verification, scientific validation,
        uncertainty quantification, and Rust conformance are not tested.
    """

    code = OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    error = OperatorRecordComparisonNumericalError(code)
    invalid_constructor = cast(Any, OperatorRecordComparisonNumericalError)

    assert reason_form == "attribute"
    assert not hasattr(error, "reason")
    with pytest.raises(TypeError):
        invalid_constructor(reason=code)


@pytest.mark.parametrize(
    "detail_form",
    [
        pytest.param("positional", id="SV-ORCNE-007-positional-detail"),
        pytest.param("keyword", id="SV-ORCNE-007-keyword-detail"),
    ],
)
def test_additional_free_form_detail_is_excluded(detail_form: str) -> None:
    """SV-ORCNE-007: reject arbitrary detail and expose no detail state.

    Evidence ID
        ``SV-ORCNE-007``; parameter IDs distinguish positional and keyword
        attempts.
    Requirement
        The closed enum code is sufficient structured state; no positional or
        keyword free-form detail is accepted or exposed.
    Method
        Call an ``Any``-typed constructor only at each deliberate invalid-
        signature boundary, then inspect a valid exception for ``detail``.
    Oracle
        The approved one-code constructor defines no arbitrary detail parameter
        or attribute.
    Acceptance
        Both invalid forms raise exactly ``TypeError`` and a valid instance has
        no ``detail`` attribute.
    Interpretation
        Passing prevents arbitrary prose from competing with the structured code.
    Limitations
        Signature-generated diagnostic wording is not frozen. Analyzer emission,
        numerical verification, scientific validation, uncertainty
        quantification, and Rust conformance are not tested.
    """

    code = OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
    invalid_constructor = cast(Any, OperatorRecordComparisonNumericalError)

    if detail_form == "positional":
        with pytest.raises(TypeError):
            invalid_constructor(code, "synthetic detail")
    else:
        with pytest.raises(TypeError):
            invalid_constructor(code, detail="synthetic detail")

    error = OperatorRecordComparisonNumericalError(code)
    assert not hasattr(error, "detail")


def test_exception_has_no_independent_serialization_api() -> None:
    """SV-ORCNE-008: verify exclusion of exception serialization methods.

    Evidence ID
        ``SV-ORCNE-008``.
    Requirement
        Neither instance nor class exposes the six unapproved JSON, dictionary,
        serializer, or deserializer method names.
    Method
        Inspect a valid instance and the public class for each excluded name.
    Oracle
        ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; no
        numerical-exception wire format or schema is approved.
    Acceptance
        Every excluded method is absent from both instance and class.
    Interpretation
        Passing establishes absence of object-owned serialization while
        preserving ``error.code`` as in-memory structured state.
    Limitations
        ``StrEnum`` values do not independently create an exception schema.
        Pickling and future schemas are unspecified; Rust mapping remains
        conceptual, and no Analyzer emission, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance is tested.
    """

    error = OperatorRecordComparisonNumericalError(
        OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
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
        assert not hasattr(OperatorRecordComparisonNumericalError, method_name)
