r"""Software verification of ``ValidateChecksumManifest``.

Facet and represented meaning
Software verification of the public ``ValidateChecksumManifest`` surface; no physical
model, mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope
The sole primary SUT is ``ValidateChecksumManifest``.  Accepted H1 field/wire contracts
and read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import ValidateChecksumManifest

pytestmark = pytest.mark.software_verification
SUT = ValidateChecksumManifest


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-034
    Requirement
    ValidateChecksumManifest is a concrete stateless ActionObject.
    Method
    Construct two instances and inspect their public storage boundary.
    Oracle
    The accepted H1 action contract requires no retained root, profile, cache,
    client, or mutable state.
    Acceptance
    Construction succeeds and instances expose no instance dictionary or slots
    containing fields.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    action = SUT()
    assert not hasattr(action, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_valid_and_invalid__returns_exact_partition(
    tmp_path: Path,
) -> None:
    """Evidence ID
    SV-HARNESS-058
    Requirement
    The public action executes one valid and one major invalid partition.
    Method
    Invoke execute directly with accepted records and a controlled invalid input.
    Oracle
    Accepted H1 action semantics and H3 fixtures fix the exact result partition.
    Acceptance
    Valid output is exact; invalid output has the expected code and no partial value.
    Interpretation
    Failure identifies action-contract drift requiring independent review.
    Limitations
    This is deterministic software verification, not scientific validation or UQ.
    """

    import hashlib

    from ksdft2effmass.harness.pi import (
        ArtifactIdentity,
        ChecksumEntry,
        ChecksumManifest,
    )

    payload = b"checked bytes\n"
    (tmp_path / "entry.txt").write_bytes(payload)
    identity = ArtifactIdentity(1, "sha256", hashlib.sha256(payload).hexdigest())
    manifest = ChecksumManifest(1, (ChecksumEntry(1, "entry.txt", identity),))
    assert SUT().execute(tmp_path, manifest).status == "PASS"
    (tmp_path / "entry.txt").write_bytes(b"changed")
    invalid = SUT().execute(tmp_path, manifest)
    assert [issue.code for issue in invalid.issues] == ["PIH.CHECKSUM.HASH_MISMATCH"]
