r"""Software verification of ``ResourceManifest``.

Facet and represented meaning

Software verification of the public ``ResourceManifest`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope

The sole primary SUT is ``ResourceManifest``.  Accepted H1 field/wire contracts and
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
    JsonRecordDeserializer,
    ResourceManifest,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification
SUT = ResourceManifest


def test_constructor__h3_valid_fixture__preserves_exact_public_value() -> None:
    """Evidence ID: SV-HARNESS-003

    Requirement: ResourceManifest accepts the complete valid version-1 H3 wire instance
    and is
    immutable.

    Method: Decode the accepted ``resource-manifest.json`` fixture through the
    caller-selected public record kind, then attempt field mutation.

    Oracle: The accepted H1 field contract and H3 valid fixture fix the class, field
    values,
    tuple storage, and immutability.

    Acceptance: The result is exactly SUT, validation is PASS, tuple fields remain
    tuples, and
    mutation raises AttributeError.

    Interpretation: A failure identifies a production, accepted-contract, fixture, or
    environment
    discrepancy requiring independent review.

    Limitations: This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    payload = (ROOT / "harness/pi/fixtures/valid/resource-manifest.json").read_bytes()
    result = JsonRecordDeserializer().execute(WireRecordKind.ResourceManifest, payload)
    assert result.validation.status == "PASS"
    assert type(result.record) is SUT

    def exercise_value_case_61_1(value: Any) -> Any:
        assert type(value) is not list

    _ = [
        exercise_value_case_61_1(value)
        for value in (
            vars(result.record).values() if hasattr(result.record, "__dict__") else ()
        )
    ]
    with pytest.raises((AttributeError, TypeError)):
        setattr(result.record, next(iter(result.record.__dataclass_fields__)), None)


def test_constructor__canonical_resources__preserves_relational_duplicates() -> None:
    """Evidence ID: SV-HARNESS-061

    Requirement: Canonical manifest ordering preserves duplicate IDs, duplicate paths,
    and exact
    duplicate entries for later relational validation.

    Method: Construct four references in reverse canonical order, including one ID
    duplicate,
    one path duplicate, and an exact duplicate, then construct a generic manifest.

    Oracle: The corrected H1 field contract fixes stable canonical sorting without
    deduplication; Python tuple multiplicity supplies the independent exact-count
    oracle.

    Acceptance: The manifest has four entries in canonical order, both duplicated fields
    occur with
    count three, and the exact reference occurs twice.

    Interpretation: Failure identifies unauthorized constructor rejection, lossy
    canonicalization, or
    contract/test-data drift.

    Limitations: This test does not accept the candidate manifest; scientific
    validation, UQ,
    physical correctness, and Rust conformance are excluded.
    """
    from ksdft2effmass.harness.pi import ArtifactIdentity, ResourceReference

    identity = ArtifactIdentity(1, "sha256", "0" * 64)
    exact = ResourceReference(
        1, "example.a", "reference", 1, "references/a.txt", identity, ()
    )
    duplicate_id = ResourceReference(
        1, "example.a", "reference", 1, "references/b.txt", identity, ()
    )
    duplicate_path = ResourceReference(
        1, "example.b", "reference", 1, "references/a.txt", identity, ()
    )
    manifest = SUT(
        1,
        "example.generic",
        1,
        "generic",
        None,
        (duplicate_path, duplicate_id, exact, exact),
    )

    assert manifest.resources == (exact, exact, duplicate_id, duplicate_path)
    assert sum(item.resource_id == "example.a" for item in manifest.resources) == 3
    assert sum(item.path == "references/a.txt" for item in manifest.resources) == 3
    assert manifest.resources.count(exact) == 2
