r"""Software verification of ``HumanReviewObservation``.

Facet and represented meaning
Software verification of one immutable deterministic review observation.

Intrinsic and cross-object scope
The sole primary SUT is ``HumanReviewObservation``. Intrinsic lexical state is covered;
target-path membership and packet composition belong to packet preparation.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. Observation status does not
establish human acceptance, numerical verification, scientific validation, or UQ.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.harness.pi import HumanReviewObservation

pytestmark = pytest.mark.software_verification
SUT = HumanReviewObservation


def make_observation() -> HumanReviewObservation:
    """Evidence ID
    Owns no identifier; supports observation evidence.
    Requirement
    Observation tests require one intrinsically valid value.
    Method
    Construct one observation from fixed public inputs.
    Oracle
    The accepted constructor contract defines valid support input.
    Acceptance
    Return one HumanReviewObservation.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    return SUT(
        "human-review.observation.tests",
        "pytest focused",
        "passed",
        "Focused tests completed with zero failures.",
        "python/tests/test_example.py",
        "3 tests collected and passed.",
    )


def test_constructor__exact_value__preserves_substantive_text_and_optional_fields() -> (
    None
):
    """Evidence ID
    ``SV-HARNESS-128``.
    Requirement
    An observation retains exact built-in field values without rewriting substantive
    text.
    Method
    Construct one complete observation and compare every field with explicit inputs.
    Oracle
    The accepted field contract and exact string equality are independent oracles.
    Acceptance
    Every value and built-in stored type is retained exactly.
    Interpretation
    Failure identifies field mapping, type, or text-preservation drift.
    Limitations
    The observed check is represented data and is not executed by construction.
    """
    observation = make_observation()
    assert observation.observation_id == "human-review.observation.tests"
    assert observation.check_name == "pytest focused"
    assert observation.status == "passed"
    assert observation.summary == "Focused tests completed with zero failures."
    assert observation.path == "python/tests/test_example.py"
    assert observation.detail == "3 tests collected and passed."
    assert all(
        type(value) is str
        for value in (
            observation.observation_id,
            observation.check_name,
            observation.status,
            observation.summary,
            observation.path,
            observation.detail,
        )
    )


def test_field__immutability__has_exact_value_semantics() -> None:
    """Evidence ID
    ``SV-HARNESS-129``.
    Requirement
    Observation state is frozen with exact dataclass equality.
    Method
    Compare separate equal instances and attempt summary mutation.
    Oracle
    Frozen dataclass semantics are exact.
    Acceptance
    Instances compare equal and mutation raises FrozenInstanceError.
    Interpretation
    Failure identifies mutability or equality drift.
    Limitations
    No packet relationship is exercised.
    """
    first = make_observation()
    assert first == make_observation()
    with pytest.raises(FrozenInstanceError):
        first.summary = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    "status",
    (
        pytest.param("passed", id="passed"),
        pytest.param("failed", id="failed"),
        pytest.param("indeterminate", id="indeterminate"),
        pytest.param("not_run", id="not_run"),
    ),
)
def test_constructor__status__accepts_closed_vocabulary(status: str) -> None:
    """Evidence ID
    ``SV-HARNESS-130``.
    Requirement
    Observation status accepts the complete closed four-value vocabulary.
    Method
    Replace one valid observation status with each declared member.
    Oracle
    The public status vocabulary supplies exact expected strings.
    Acceptance
    Every declared status is retained exactly.
    Interpretation
    Failure identifies vocabulary drift.
    Limitations
    Status records occurrence only and is not an acceptance decision.
    """
    assert replace(make_observation(), status=status).status == status


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    (
        pytest.param("observation_id", "", ValueError, id="empty_identifier"),
        pytest.param(
            "observation_id", "not valid", ValueError, id="malformed_identifier"
        ),
        pytest.param("check_name", " ", ValueError, id="blank_check_name"),
        pytest.param("status", "PASS", ValueError, id="acceptance_like_status"),
        pytest.param("summary", "", ValueError, id="empty_summary"),
        pytest.param("path", "/tmp/result", ValueError, id="absolute_path"),
        pytest.param("detail", " ", ValueError, id="blank_detail"),
        pytest.param("summary", 4, TypeError, id="non_string_summary"),
    ),
)
def test_constructor__fields__rejects_malformed_semantic_partitions(
    field: str, value: object, exception: type[Exception]
) -> None:
    """Evidence ID
    ``SV-HARNESS-131``.
    Requirement
    Observation identifiers, text, status, path, and optional detail fail closed.
    Method
    Replace one valid field with each malformed semantic partition.
    Oracle
    Identifier, text, root-relative path, exact-type, and closed-vocabulary contracts
    supply the expected exception taxonomy.
    Acceptance
    Every partition raises the specified exception.
    Interpretation
    Failure identifies intrinsic-validation or exception-taxonomy drift.
    Limitations
    Target path membership is checked by HumanReviewPreparer instead.
    """
    with pytest.raises(exception):
        replace(make_observation(), **{field: value})  # type: ignore[arg-type]


def test_constructor__optional_fields__accepts_explicit_none() -> None:
    """Evidence ID
    ``SV-HARNESS-132``.
    Requirement
    Path and supporting detail are independently optional.
    Method
    Construct an observation with both optional fields set to None.
    Oracle
    The public optional-field contract fixes exact None storage.
    Acceptance
    Both fields are None and all substantive fields remain unchanged.
    Interpretation
    Failure identifies optional-state drift.
    Limitations
    Absence of detail does not imply absence of limitations.
    """
    observation = replace(make_observation(), path=None, detail=None)
    assert observation.path is None
    assert observation.detail is None
