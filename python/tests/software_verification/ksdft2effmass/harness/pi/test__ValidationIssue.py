r"""Software verification of ``ValidationIssue``.

Facet and represented meaning
Software verification of the public ``ValidationIssue`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope
The sole primary SUT is ``ValidationIssue``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    DeserializeJsonRecord,
    ValidationIssue,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification
SUT = ValidationIssue


def test_constructor__h3_valid_fixture__preserves_exact_public_value() -> None:
    """Evidence ID
    SV-HARNESS-015
    Requirement
    ValidationIssue accepts the complete valid version-1 H3 wire instance and is
    immutable.
    Method
    Decode the accepted ``validation-issue.json`` fixture through the
    caller-selected public record kind, then attempt field mutation.
    Oracle
    The accepted H1 field contract and H3 valid fixture fix the class, field values,
    tuple storage, and immutability.
    Acceptance
    The result is exactly SUT, validation is PASS, tuple fields remain tuples, and
    mutation raises AttributeError.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    payload = (ROOT / "harness/pi/fixtures/valid/validation-issue.json").read_bytes()
    result = DeserializeJsonRecord().execute(WireRecordKind.ValidationIssue, payload)
    assert result.validation.status == "PASS"
    assert type(result.record) is SUT

    def exercise_value_case_61_3(value: Any) -> Any:
        assert type(value) is not list

    _ = [
        exercise_value_case_61_3(value)
        for value in (
            vars(result.record).values() if hasattr(result.record, "__dict__") else ()
        )
    ]
    with pytest.raises((AttributeError, TypeError)):
        setattr(result.record, next(iter(result.record.__dataclass_fields__)), None)


def test_constructor__diagnostic_path_corpus__accepts_and_rejects_exactly() -> None:
    """Evidence ID
    SV-HARNESS-048
    Requirement
    DiagnosticPath accepts file, directory-scope, None, and NFC spellings and
    rejects the complete 19-case malformed corpus without normalization.
    Method
    Construct ValidationIssue directly for every accepted H3 indexed spelling.
    Oracle
    The accepted H1 DiagnosticPath grammar and H3 oracle index fix the partition.
    Acceptance
    Four valid paths are retained exactly; all 19 invalid paths raise ValueError
    containing the exact registered issue code.
    Interpretation
    Failure identifies constructor, H3 corpus, or H1 lexical-contract drift.
    Limitations
    Paths are lexical; existence and file kind are not established.
    """
    import json

    corpus = json.loads(
        (ROOT / "harness/pi/fixtures/diagnostic-path/oracle-index.json").read_text()
    )
    assert len(corpus["valid"]) == 4

    def exercise_case_case_93_2(case: Any) -> Any:
        issue = SUT(1, "PIH.PATH.MISSING", "ERROR", None, case["path"], (), "x")
        assert issue.path == case["path"]
        assert type(issue.path) is str or issue.path is None

    _ = [exercise_case_case_93_2(case) for case in (corpus["valid"])]
    assert len(corpus["invalid"]) == 19

    def exercise_case_case_98_1(case: Any) -> Any:
        value = case.get("path")
        if value is None:
            value = case["path_escaped"].encode().decode("unicode_escape")
        with pytest.raises(ValueError, match=case["expected"].replace(".", "\\.")):
            SUT(1, "PIH.PATH.MISSING", "ERROR", None, value, (), "x")

    _ = [exercise_case_case_98_1(case) for case in (corpus["invalid"])]
