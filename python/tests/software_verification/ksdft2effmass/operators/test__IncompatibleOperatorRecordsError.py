r"""Software-verification evidence for ``IncompatibleOperatorRecordsError``.

System under test
-----------------
``IncompatibleOperatorRecordsError`` is the structured public failure emitted
when a compatibility audit contains one or more mismatches under the current
exact direct-representation compatibility contract. The authoritative
machine-readable evidence is its retained
``OperatorRecordCompatibilityResult``, which preserves reference and candidate
roles and the canonical ordered ``OperatorRecordCompatibilityIssue`` tuple. The
exception message is a human-readable mismatch-code summary, not a replacement
for that structured result.

Evidence class, strategy, and oracle
------------------------------------
This module provides software-verification evidence ``SV-IORE-001`` through
``SV-IORE-006``. Direct public construction tests the exception independently of
``OperatorRecordCompatibilityAnalyzer.require()``. Analyzer-to-exception
propagation is already owned by ``SV-ORCA-017`` and is not duplicated here. The
oracle is the accepted public exception source and Sphinx contract: ``ValueError``
inheritance, exact audit-object retention, semantic message content, exact
``TypeError`` versus ``ValueError`` taxonomy, and absence of an approved
exception serialization API.

Interpretation and exclusions
-----------------------------
Passing establishes exception construction, error taxonomy, exact audit-object
retention, documented diagnostic summarization, invalid/compatible input
rejection, and serialization exclusion. Incompatibility means only that records
fail the current exact direct-representation contract. It does not determine
whether basis alignment, gauge alignment, energy-zero alignment, unit conversion,
geometry transformation, or another scientifically justified identification map
could make them comparable.

These tests compute no numerical norm and establish no numerical accuracy,
physical Hamiltonian incompatibility, scientific validity of compatibility
rules, scientific validation, uncertainty bounds, uncertainty quantification,
or Rust conformance. Synthetic Issues and Results carry no DFT, Wannier,
impurity, experimental, or physical-system provenance. Failure may indicate an
exception-contract regression, documentation mismatch, or evidence defect that
requires investigation; it does not itself establish scientific invalidity.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import (
    IncompatibleOperatorRecordsError,
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)

pytestmark = pytest.mark.software_verification


def make_incompatible_result(
    codes: tuple[OperatorRecordCompatibilityMismatchCode, ...] = (
        OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
    ),
    *,
    reference_identifier: str = "reference",
    candidate_identifier: str = "candidate",
) -> OperatorRecordCompatibilityResult:
    """Construct a deterministic incompatible synthetic audit result.

    Evidence ID
        Supporting fixture for ``SV-IORE-001`` through ``SV-IORE-003`` and
        ``SV-IORE-006``; it owns no separate evidence identifier.
    Requirement
        Valid exception fixtures contain a nonempty exact built-in Issue tuple in
        the caller-supplied canonical mismatch-code order.
    Method
        Construct every Issue through its public constructor, then pass the
        resulting tuple and role identifiers to the public Result constructor.
        No sorting, deduplication, string conversion, set, dictionary, private
        validation, ``Any``, or ``cast`` is used.
    Oracle
        Public Issue and Result contracts require enum-backed Issues and an exact
        canonically ordered tuple.
    Acceptance
        Construction returns an incompatible Result whose Issue tuple preserves
        the supplied enum sequence exactly.
    Interpretation
        A returned object is deterministic in-memory software evidence suitable
        for direct exception construction.
    Limitations
        The helper does not execute the Analyzer or prove physical
        incompatibility. Its synthetic state has no DFT, Wannier, impurity,
        experimental, or physical-system provenance and establishes no numerical
        verification, scientific validation, uncertainty quantification, or Rust
        conformance.
    """

    issues = tuple(OperatorRecordCompatibilityIssue(code) for code in codes)
    return OperatorRecordCompatibilityResult(
        reference_identifier,
        candidate_identifier,
        issues,
    )


def test_public_construction_and_exception_taxonomy() -> None:
    """SV-IORE-001: construct the public structured ``ValueError`` subtype.

    Evidence ID
        ``SV-IORE-001``.
    Requirement
        An incompatible public Result constructs the public exception, whose
        accepted hierarchy is ``IncompatibleOperatorRecordsError -> ValueError``.
    Method
        Construct one synthetic incompatible Result and pass it directly to the
        exception imported from ``ksdft2effmass.operators``.
    Oracle
        The accepted public source declares ``ValueError`` inheritance and the
        constructor accepts an incompatible compatibility Result.
    Acceptance
        Construction succeeds and the object is an instance of the public class,
        ``ValueError``, and ``Exception``.
    Interpretation
        Passing establishes public construction and documented exception
        taxonomy independently of Analyzer execution.
    Limitations
        ``Exception.args`` formatting, internal module location, mutability,
        pickling, traceback state, numerical accuracy, scientific validation,
        uncertainty quantification, and Rust conformance are not tested.
    """

    result = make_incompatible_result()

    error = IncompatibleOperatorRecordsError(result)

    assert isinstance(error, IncompatibleOperatorRecordsError)
    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


def test_exact_incompatible_audit_result_identity_is_retained() -> None:
    """SV-IORE-002: retain the exact supplied audit object and ordered state.

    Evidence ID
        ``SV-IORE-002``.
    Requirement
        Callers can inspect the same audit object that caused failure without
        reconstruction or loss of input roles or Issue ordering.
    Method
        Supply one direct incompatible Result and inspect only the public
        ``compatibility_result`` attribute and its public state.
    Oracle
        The exception contract requires identity retention of the authoritative
        ``OperatorRecordCompatibilityResult``.
    Acceptance
        The retained object is identical to the input and exposes the exact
        identifiers, Issue tuple, and incompatible state.
    Interpretation
        Passing establishes exact in-memory audit retention, role fidelity,
        Issue-tuple fidelity, and incompatible state.
    Limitations
        Result constructor invariants remain owned by ``SV-ORCAR-001`` through
        ``SV-ORCAR-013``. No Analyzer, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance is tested.
    """

    result = make_incompatible_result(
        reference_identifier="reference-role",
        candidate_identifier="candidate-role",
    )
    expected_issues = result.issues

    error = IncompatibleOperatorRecordsError(result)
    retained = error.compatibility_result

    assert retained is result
    assert retained.reference_identifier == "reference-role"
    assert retained.candidate_identifier == "candidate-role"
    assert retained.issues is expected_issues
    assert retained.issues == expected_issues
    assert retained.is_compatible is False


@pytest.mark.parametrize(
    "codes",
    [
        pytest.param(
            (OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,),
            id="SV-IORE-003-single-energy-unit",
        ),
        pytest.param(
            (
                OperatorRecordCompatibilityMismatchCode.OPERATOR_KIND_MISMATCH,
                OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH,
            ),
            id="SV-IORE-003-multiple-canonical-codes",
        ),
    ],
)
def test_human_readable_message_summarizes_structured_codes(
    codes: tuple[OperatorRecordCompatibilityMismatchCode, ...],
) -> None:
    """SV-IORE-003: summarize retained codes in their canonical Issue order.

    Evidence ID
        ``SV-IORE-003``.
    Requirement
        The human-readable message states incompatibility and includes every
        retained machine code in the same order as the authoritative Issue tuple.
    Method
        Construct single- and multi-Issue Results, then inspect stable semantic
        message content without freezing punctuation or separators.
    Oracle
        Source documentation promises a readable mismatch-code summary while
        designating ``compatibility_result`` as authoritative machine state.
    Acceptance
        The base incompatibility statement and every retained code occur, with
        multi-Issue codes in retained canonical order.
    Interpretation
        Passing establishes semantic diagnostic coverage and ordering, not a
        wire format or independently parseable protocol.
    Limitations
        Exact punctuation, capitalization beyond the documented base phrase,
        canonical description wording, Analyzer propagation, numerical accuracy,
        scientific validation, uncertainty quantification, and Rust conformance
        are outside this evidence.
    """

    result = make_incompatible_result(codes)

    error = IncompatibleOperatorRecordsError(result)
    message = str(error)

    assert "operator records are not compatible" in message
    positions = tuple(message.index(code.value) for code in codes)
    assert positions == tuple(sorted(positions))
    assert tuple(issue.code for issue in error.compatibility_result.issues) == codes


@pytest.mark.parametrize(
    "invalid_result",
    [
        pytest.param(None, id="SV-IORE-004-none"),
        pytest.param("energy_unit_mismatch", id="SV-IORE-004-string"),
        pytest.param(True, id="SV-IORE-004-boolean"),
        pytest.param(object(), id="SV-IORE-004-arbitrary-object"),
        pytest.param(
            OperatorRecordCompatibilityIssue(
                OperatorRecordCompatibilityMismatchCode.ENERGY_UNIT_MISMATCH
            ),
            id="SV-IORE-004-issue-object",
        ),
    ],
)
def test_invalid_compatibility_result_types_are_rejected(
    invalid_result: object,
) -> None:
    """SV-IORE-004: reject representative wrong semantic input types.

    Evidence ID
        ``SV-IORE-004``.
    Requirement
        Values that are not ``OperatorRecordCompatibilityResult`` instances
        raise ``TypeError`` at the public constructor boundary.
    Method
        Parameterize ``None``, string, Boolean, arbitrary object, and Issue, using
        ``Any`` and ``cast`` only at this deliberate invalid-type call.
    Oracle
        The public exception contract specifies ``TypeError`` and identifies the
        ``compatibility_result`` field in its diagnostic.
    Acceptance
        Every parameter raises only ``TypeError`` and the diagnostic names
        ``compatibility_result``.
    Interpretation
        Passing establishes exact wrong-type taxonomy and field-specific
        diagnostic scope.
    Limitations
        A correctly typed compatible Result belongs to ``SV-IORE-005``. This
        evidence performs no Analyzer execution, numerical verification,
        scientific validation, uncertainty quantification, or Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        IncompatibleOperatorRecordsError(cast(Any, invalid_result))

    assert "compatibility_result" in str(exc_info.value)


def test_compatible_audit_result_is_rejected_as_invalid_exception_state() -> None:
    """SV-IORE-005: reject a compatible Result with ``ValueError``.

    Evidence ID
        ``SV-IORE-005``.
    Requirement
        The correct Result type violates the exception-state invariant when it
        has no Issues, so rejection is ``ValueError`` rather than ``TypeError``.
    Method
        Construct an ordinary valid compatible Result with an empty exact tuple
        and pass it directly to the exception constructor.
    Oracle
        The public contract distinguishes wrong semantic type from a correctly
        typed but compatible result and requires an incompatible audit.
    Acceptance
        Construction raises only ``ValueError`` with the documented incompatible-
        result diagnostic.
    Interpretation
        Passing establishes the documented TypeError/ValueError taxonomy split.
    Limitations
        No object mutation, invariant bypass, Analyzer execution, physical
        incompatibility determination, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance occurs.
    """

    compatible = OperatorRecordCompatibilityResult("reference", "candidate", ())

    with pytest.raises(ValueError) as exc_info:
        IncompatibleOperatorRecordsError(compatible)

    assert "compatibility_result must be incompatible" in str(exc_info.value)


def test_exception_has_no_independent_serialization_api() -> None:
    """SV-IORE-006: exclude unsupported exception serialization methods.

    Evidence ID
        ``SV-IORE-006``.
    Requirement
        The exception retains an in-memory audit but exposes no independent JSON,
        dictionary, serializer, or deserializer API.
    Method
        Inspect the public instance/class boundary for the six explicitly
        unapproved method names.
    Oracle
        Schema version 1 serializes ``OperatorRecord`` only; no exception,
        comparison-result, or compatibility-result wire format is approved.
    Acceptance
        All six unapproved API names are absent from both instance and class.
    Interpretation
        Passing establishes absence of object-owned serialization APIs without
        adding or implying a wire contract.
    Limitations
        Pickling, hashability, memory layout, Rust representation, Analyzer
        propagation, numerical verification, scientific validation, and
        uncertainty quantification are outside this evidence.
    """

    error = IncompatibleOperatorRecordsError(make_incompatible_result())

    for method_name in (
        "to_json",
        "to_dict",
        "serialize",
        "from_json",
        "from_dict",
        "deserialize",
    ):
        assert not hasattr(error, method_name)
        assert not hasattr(IncompatibleOperatorRecordsError, method_name)
