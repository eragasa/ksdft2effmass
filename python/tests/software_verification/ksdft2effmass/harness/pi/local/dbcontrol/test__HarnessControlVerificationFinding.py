r"""Software verification of ``HarnessControlVerificationFinding``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns one immutable structured control disagreement.

Intrinsic and cross-object scope

Closed code, optional path, nonempty message, equality, and immutability are intrinsic;
aggregation belongs to the verification result.

VVUQ and scientific exclusions

This is structural software verification only; scientific validation and UQ are
excluded.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.harness.pi.local import HarnessControlVerificationFinding

SUT = HarnessControlVerificationFinding
pytestmark = pytest.mark.software_verification


def test_constructor__fields__preserve_value_semantics_and_immutability() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-finding.structured-fields

    Requirement: A finding preserves exact closed code, optional path, and message with
    immutable value semantics.

    Method: Construct two equal literal findings and attempt field assignment.

    Oracle: Literal values and frozen dataclass semantics define expected behavior.

    Acceptance: Values and equality are exact and mutation raises
    ``FrozenInstanceError``.

    Interpretation: Failure identifies lost or mutable disagreement information.

    Limitations: Finding aggregation belongs to verification-result evidence.
    """  # noqa: E501
    expected = SUT("changed_artifact", "harness/task-graph.json", "candidate differs")
    assert expected == SUT(
        "changed_artifact", "harness/task-graph.json", "candidate differs"
    )
    assert (expected.code, expected.path, expected.message) == (
        "changed_artifact",
        "harness/task-graph.json",
        "candidate differs",
    )
    with pytest.raises(FrozenInstanceError):
        expected.message = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("code", "path", "message", "error"),
    (
        pytest.param(1, None, "message", TypeError, id="wrong_code_type"),
        pytest.param("", None, "message", ValueError, id="empty_code"),
        pytest.param("unknown", None, "message", ValueError, id="unsupported_code"),
        pytest.param("changed_artifact", 1, "message", TypeError, id="wrong_path_type"),
        pytest.param("changed_artifact", "", "message", ValueError, id="empty_path"),
        pytest.param("changed_artifact", None, 1, TypeError, id="wrong_message_type"),
        pytest.param("changed_artifact", None, "", ValueError, id="empty_message"),
    ),
)
def test_constructor__fields__reject_invalid_type_and_value_partitions(
    code: object, path: object, message: object, error: type[Exception]
) -> None:
    """Evidence ID: software-verification.harness.sqlite-control.verification-finding.invalid-fields

    Requirement: Wrong semantic types raise ``TypeError`` and correctly typed invalid
    values raise ``ValueError`` for every finding field.

    Method: Construct one finding for each independent invalid partition.

    Oracle: The closed finding vocabulary and nonempty field contract define exact
    exception categories.

    Acceptance: Every partition raises its expected error type.

    Interpretation: Failure weakens finding structure or exception taxonomy.

    Limitations: Supported-code meanings are exercised by verifier evidence.
    """  # noqa: E501
    with pytest.raises(error):
        SUT(code, path, message)  # type: ignore[arg-type]
