r"""Software verification of ``HumanReviewFinding``.

Facet and represented meaning
Software verification of one immutable candidate issue for human judgment.

Intrinsic and cross-object scope
The sole primary SUT is ``HumanReviewFinding``. Intrinsic issue representation is
covered; supporting-observation existence and target membership belong to preparation.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. A harness-generated finding is
not accepted, scientifically valid, or a human disposition.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.harness.pi import HumanReviewFinding

pytestmark = pytest.mark.software_verification
SUT = HumanReviewFinding


def make_finding() -> HumanReviewFinding:
    """Evidence ID
    Owns no identifier; supports finding evidence.
    Requirement
    Finding tests require one intrinsically valid value.
    Method
    Construct one finding from fixed public inputs.
    Oracle
    The accepted constructor contract defines valid support input.
    Acceptance
    Return one HumanReviewFinding.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    return SUT(
        "human-review.finding.scope",
        "advisory",
        "The observation covers software verification only.",
        "python/tests/test_example.py",
        ("human-review.observation.tests",),
        "A human must decide whether the stated evidence boundary is adequate.",
    )


def test_constructor__exact_value__owns_supporting_identifiers_and_text() -> None:
    """Evidence ID
    ``SV-HARNESS-133``.
    Requirement
    A finding retains exact issue text and defensively owns supporting identifiers.
    Method
    Construct one complete finding and inspect every stored value and collection type.
    Oracle
    The accepted field contract and exact tuple/string semantics are exact.
    Acceptance
    Text is unchanged, identifiers preserve order, and storage uses built-in tuple.
    Interpretation
    Failure identifies field, text, or canonical-ownership drift.
    Limitations
    Supporting-observation existence is not intrinsic to this record.
    """
    supplied = ("human-review.observation.tests",)
    finding = SUT(
        "human-review.finding.scope",
        "advisory",
        "The observation covers software verification only.",
        "python/tests/test_example.py",
        supplied,
        "A human must decide whether the stated evidence boundary is adequate.",
    )
    assert finding == make_finding()
    assert type(finding.supporting_observation_ids) is tuple
    assert finding.supporting_observation_ids == supplied
    assert finding.supporting_observation_ids is not supplied


def test_field__immutability__has_exact_value_semantics() -> None:
    """Evidence ID
    ``SV-HARNESS-134``.
    Requirement
    Finding state is frozen with exact dataclass equality.
    Method
    Compare separate equal instances and attempt severity mutation.
    Oracle
    Frozen dataclass semantics are exact.
    Acceptance
    Instances compare equal and mutation raises FrozenInstanceError.
    Interpretation
    Failure identifies mutability or equality drift.
    Limitations
    No packet relationship is exercised.
    """
    first = make_finding()
    assert first == make_finding()
    with pytest.raises(FrozenInstanceError):
        first.severity = "low"  # type: ignore[misc]


@pytest.mark.parametrize(
    "severity",
    (
        pytest.param("blocker", id="blocker"),
        pytest.param("high", id="high"),
        pytest.param("medium", id="medium"),
        pytest.param("low", id="low"),
        pytest.param("advisory", id="advisory"),
    ),
)
def test_constructor__severity__accepts_closed_vocabulary(severity: str) -> None:
    """Evidence ID
    ``SV-HARNESS-135``.
    Requirement
    Finding severity accepts the complete closed five-value vocabulary.
    Method
    Replace one valid severity with each declared member.
    Oracle
    The public severity vocabulary supplies exact expected strings.
    Acceptance
    Every declared severity is retained exactly.
    Interpretation
    Failure identifies vocabulary drift.
    Limitations
    Severity does not determine human disposition.
    """
    assert replace(make_finding(), severity=severity).severity == severity


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    (
        pytest.param("finding_id", "", ValueError, id="empty_identifier"),
        pytest.param("finding_id", "invalid id", ValueError, id="malformed_identifier"),
        pytest.param(
            "severity", "critical", ValueError, id="closed_vocabulary_violation"
        ),
        pytest.param("statement", " ", ValueError, id="blank_statement"),
        pytest.param("path", "../outside.py", ValueError, id="traversal_path"),
        pytest.param(
            "supporting_observation_ids",
            ("human-review.observation.tests", "human-review.observation.tests"),
            ValueError,
            id="duplicate_support",
        ),
        pytest.param("unresolved_limitation", "", ValueError, id="empty_limitation"),
        pytest.param("severity", 2, TypeError, id="non_string_severity"),
    ),
)
def test_constructor__fields__rejects_malformed_semantic_partitions(
    field: str, value: object, exception: type[Exception]
) -> None:
    """Evidence ID
    ``SV-HARNESS-136``.
    Requirement
    Finding identity, severity, text, path, support, and limitation fail closed.
    Method
    Replace one valid field with each malformed semantic partition.
    Oracle
    Public identifier, vocabulary, path, uniqueness, and exact-type contracts are
    exact.
    Acceptance
    Every partition raises the specified exception.
    Interpretation
    Failure identifies intrinsic-validation or exception-taxonomy drift.
    Limitations
    Unknown but well-formed supporting identifiers are checked by preparation.
    """
    with pytest.raises(exception):
        replace(make_finding(), **{field: value})  # type: ignore[arg-type]


def test_constructor__optional_path__accepts_explicit_none_without_disposition() -> (
    None
):
    """Evidence ID
    ``SV-HARNESS-137``.
    Requirement
    A finding may concern the whole target and stores no human disposition field.
    Method
    Construct with path None and inspect the public dataclass field set.
    Oracle
    The accepted optional-path contract and declared public fields are exact.
    Acceptance
    Path is None and neither disposition nor human_decision is a field.
    Interpretation
    Failure identifies optional-state or authority-boundary drift.
    Limitations
    Attribute absence does not itself prove runtime noninteraction.
    """
    finding = replace(make_finding(), path=None)
    assert finding.path is None
    assert "disposition" not in finding.__dataclass_fields__
    assert "human_decision" not in finding.__dataclass_fields__
