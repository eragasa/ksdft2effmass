r"""Software verification of harness pi path confinement contract.

Facet and represented meaning

Software verification of lexical path roles, issue ordering, and explicit-root
confinement; no physical, mathematical, or numerical object is represented.

Intrinsic and cross-object scope

The primary owner is the H1 path-confinement artifact contract. Literal lexical examples
and disposable filesystem topology provide independent oracles.

VVUQ and scientific exclusions

Passing establishes only software path safety and deterministic diagnostics; numerical
verification, scientific validation, UQ, and physical correctness are excluded.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    ChecksumEntry,
    ChecksumManifest,
    ChecksumManifestValidator,
    OwnershipScope,
    ValidationIssue,
    ValidationResult,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification


def test_artifact__semantic_path_roles__remain_specialized_and_neutral() -> None:
    """Evidence ID: SV-HARNESS-043

    Requirement: ResourcePath remains a file spelling, OwnershipScopePath carries
    explicit
    containment, and DiagnosticPath remains neutral lexical text or None.

    Method: Construct a file checksum entry, directory-tree scope, and issues from the
    two
    exact spellings plus no location.

    Oracle: H1 defines three distinct semantic roles while requiring the same accepted
    lexical grammar.

    Acceptance: Exact spellings are retained, tree containment uses the slash boundary,
    and the
    no-location issue retains None.

    Interpretation: Failure identifies accidental path-role conflation or lexical
    mutation.

    Limitations: Built-in ``str`` aliases cannot provide runtime nominal distinction;
    meaning is
    verified through owning public fields only.
    """
    identity = ArtifactIdentity(1, "sha256", "0" * 64)
    entry = ChecksumEntry(1, "records/item.json", identity)
    scope = OwnershipScope(1, "tests/verification", "directory_tree")
    file_issue = ValidationIssue(
        1, "PIH.PATH.MISSING", "ERROR", None, entry.path, (), "x"
    )
    scope_issue = ValidationIssue(
        1, "PIH.OWNERSHIP.PATH_OVERLAP", "ERROR", None, scope.path, (), "x"
    )
    none_issue = ValidationIssue(
        1, "PIH.PATH.ROOT_INVALID", "ERROR", None, None, (), "x"
    )
    assert (file_issue.path, scope_issue.path, none_issue.path) == (
        "records/item.json",
        "tests/verification",
        None,
    )
    assert scope.contains("tests/verification/test_x.py")
    assert not scope.contains("tests/verification-other/test_x.py")


def test_artifact__diagnostic_order_and_duplicates__use_exact_machine_key() -> None:
    """Evidence ID: SV-HARNESS-044

    Requirement: Issue construction rejects duplicate machine findings and orders None
    paths
    before NFC UTF-8 spellings.

    Method: Construct literal registered issues in the accepted total order, then
    attempt
    reversed and duplicate aggregates.

    Oracle: H1 issue-code-and-ordering-contract.md defines the exact machine duplicate
    key
    and path ordering.

    Acceptance: The ordered aggregate constructs exactly; reversed and duplicate
    sequences raise
    ValueError.

    Interpretation: Failure identifies deterministic-ordering or duplicate-coalescing
    contract drift.

    Limitations: This constructor check does not observe private coalescing routes
    inside every
    action.
    """
    first = ValidationIssue(1, "PIH.PATH.MISSING", "ERROR", None, None, (), "a")
    second = ValidationIssue(
        1, "PIH.PATH.MISSING", "ERROR", None, "résultats/a", (), "b"
    )
    assert ValidationResult(1, "FAIL", (first, second)).issues == (first, second)
    with pytest.raises(ValueError):
        ValidationResult(1, "FAIL", (second, first))
    with pytest.raises(ValueError):
        ValidationResult(1, "FAIL", (first, first))


def test_artifact__explicit_root__rejects_symlink_components(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-045

    Requirement: Files selected below an explicit root reject every symlink component
    even when
    the target remains inside the root.

    Method: Create a disposable regular file and a symlink to it, then validate a
    checksum
    manifest through the public action.

    Oracle: The accepted H1 path contract independently requires lexical plus resolved
    confinement and unconditional below-root symlink rejection.

    Acceptance: Validation returns FAIL with exactly ``PIH.PATH.SYMLINK`` and performs
    no repair.

    Interpretation: Failure exposes a confinement defect or a platform lacking
    symlink-test support.

    Limitations: The test uses a disposable local filesystem and does not cover every
    host race
    or case-insensitive filesystem behavior.
    """
    target = tmp_path / "target.txt"
    target.write_bytes(b"safe")
    link = tmp_path / "link.txt"
    try:
        link.symlink_to(target.name)
    except OSError, NotImplementedError:
        pytest.skip("symlinks unavailable on this platform")
    identity = ArtifactIdentity(1, "sha256", hashlib.sha256(b"safe").hexdigest())
    result = ChecksumManifestValidator().execute(
        tmp_path.resolve(),
        ChecksumManifest(1, (ChecksumEntry(1, "link.txt", identity),)),
    )
    assert result.status == "FAIL"
    assert tuple(issue.code for issue in result.issues) == ("PIH.PATH.SYMLINK",)
