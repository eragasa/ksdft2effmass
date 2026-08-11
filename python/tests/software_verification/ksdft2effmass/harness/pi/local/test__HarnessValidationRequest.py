r"""Software verification of ``HarnessValidationRequest``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns intrinsic repository-boundary request state.

Intrinsic and cross-object scope

Only construction, exact value semantics, and immutability are exercised.

VVUQ and scientific exclusions

This is structural software verification only; scientific validation and UQ are
excluded.
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import HarnessValidationRequest

SUT = HarnessValidationRequest
pytestmark = pytest.mark.software_verification


def test_constructor__repository_root__preserves_absolute_value_and_equality() -> None:
    """Evidence ID: software-verification.harness.repository-validation.request.absolute-value

    Requirement: An absolute lexical repository path is preserved with exact value
    semantics.

    Method: Construct two requests from the same independent literal path.

    Oracle: ``Path('/repository')`` is absolute and dataclass equality compares fields.

    Acceptance: Both values equal each other and preserve the exact path.

    Interpretation: Failure identifies request canonicalization or value loss.

    Limitations: Filesystem existence belongs to ``HarnessValidator``.
    """  # noqa: E501
    expected = Path("/repository")
    assert SUT(expected) == SUT(expected)
    assert SUT(expected).repository_root == expected


@pytest.mark.parametrize(
    ("value", "error"),
    (
        pytest.param("/repository", TypeError, id="wrong_path_type"),
        pytest.param(Path("repository"), ValueError, id="relative_path"),
        pytest.param(Path("."), ValueError, id="empty_path_value"),
        pytest.param(Path("/repository/../escape"), ValueError, id="lexical_traversal"),
    ),
)
def test_constructor__repository_root__rejects_invalid_partitions(
    value: object, error: type[Exception]
) -> None:
    """Evidence ID: software-verification.harness.repository-validation.request.invalid-root

    Requirement: Repository roots are exact ``Path`` values, absolute, nonempty, and
    free of lexical parent traversal.

    Method: Construct one request for each independently invalid partition.

    Oracle: Python ``Path`` type and lexical path parts define acceptance.

    Acceptance: Every partition raises its exact exception category.

    Interpretation: Failure permits ambiguous or ambient repository selection.

    Limitations: Symlink and existence checks occur during Action execution.
    """  # noqa: E501
    with pytest.raises(error):
        SUT(value)  # type: ignore[arg-type]


def test_constructor__immutability__rejects_field_assignment() -> None:
    """Evidence ID: software-verification.harness.repository-validation.request.immutable

    Requirement: Repository-validation requests are immutable after construction.

    Method: Assign a new root to a valid frozen record.

    Oracle: Frozen dataclass semantics reject public field mutation.

    Acceptance: Assignment raises ``FrozenInstanceError``.

    Interpretation: Failure permits request identity to change during validation.

    Limitations: Nested state is absent.
    """  # noqa: E501
    request = SUT(Path("/repository"))
    with pytest.raises(FrozenInstanceError):
        request.repository_root = Path("/other")  # type: ignore[misc]
