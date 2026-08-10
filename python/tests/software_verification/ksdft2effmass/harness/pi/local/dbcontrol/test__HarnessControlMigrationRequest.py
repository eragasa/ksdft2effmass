r"""Software verification of ``HarnessControlMigrationRequest``.

Facet and represented meaning

The module owns the intrinsic behavior of
``HarnessControlMigrationRequest``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import HarnessControlMigrationRequest

SUT = HarnessControlMigrationRequest

pytestmark = pytest.mark.software_verification


def test_constructor__optional_ownership_input__is_immutable_and_root_confined() -> (
    None
):
    """Evidence ID: software-verification.harness.sqlite-control.migration-request.optional-ownership-input-is-immutable-and-root-confined

    Requirement: The optional evidence-module ownership input is an immutable, strictly typed, repository-relative request field whose default is ``None``.

    Method: Construct default and explicit requests, inspect the public field, attempt assignment, and construct wrong-type, absolute, and parent-traversing variants.

    Oracle: Frozen dataclass semantics and repository-relative ``Path`` semantics define the accepted states.

    Acceptance: The default is exactly ``None``, the relative path is preserved, assignment raises ``FrozenInstanceError``, wrong type raises ``TypeError``, and escaping paths raise ``ValueError``.

    Interpretation: Failure indicates a mutable, ambient, or insufficiently root-confined migration input boundary.

    Limitations: Filesystem symlink confinement and document conformance are exercised by the migration Action.
    """  # noqa: E501
    from dataclasses import FrozenInstanceError

    root = Path("/repository")
    default = HarnessControlMigrationRequest(root)
    assert default.evidence_module_ownership_path is None
    assert default.evidence_profile_matrix_path is None
    request = HarnessControlMigrationRequest(
        root,
        evidence_module_ownership_path=Path("updates/ownership.json"),
        evidence_profile_matrix_path=Path("harness/pi/evidence/profile.json"),
    )
    assert request.evidence_module_ownership_path == Path("updates/ownership.json")
    assert request.evidence_profile_matrix_path == Path(
        "harness/pi/evidence/profile.json"
    )
    with pytest.raises(FrozenInstanceError):
        request.evidence_module_ownership_path = None  # type: ignore[misc]
    with pytest.raises(TypeError):
        HarnessControlMigrationRequest(
            root,
            evidence_module_ownership_path="updates/ownership.json",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        HarnessControlMigrationRequest(
            root, evidence_module_ownership_path=Path("/updates/ownership.json")
        )
    with pytest.raises(ValueError):
        HarnessControlMigrationRequest(
            root, evidence_module_ownership_path=Path("../ownership.json")
        )
    with pytest.raises(ValueError):
        HarnessControlMigrationRequest(
            root, evidence_profile_matrix_path=Path("harness/pi/evidence/profile.json")
        )


def test_constructor__relative_root__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-request.relative-root-raises-value-error

    Requirement: The migration request accepts only an explicit absolute repository root.

    Method: Construct the public request with a relative ``Path``.

    Oracle: ``Path("repository")`` is relative by Python path semantics.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Failure indicates an ambient-root persistence boundary regression.

    Limitations: Filesystem existence and migration behavior are not exercised.
    """  # noqa: E501
    with pytest.raises(ValueError):
        HarnessControlMigrationRequest(Path("repository"))
