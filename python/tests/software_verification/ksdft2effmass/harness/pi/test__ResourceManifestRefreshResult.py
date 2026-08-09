r"""Software verification of ``ResourceManifestRefreshResult``.

Facet and represented meaning

Software verification of the immutable resource-manifest refresh outcome.

Intrinsic and cross-object scope

The sole primary SUT is ``ResourceManifestRefreshResult``. Result field types,
status/value consistency, changed-ID membership, ordering, equality, and immutability
are in scope; filesystem observation is excluded.

VVUQ and scientific exclusions

Passing establishes exact result-record behavior only, not resource semantics,
scientific validity, uncertainty quantification, provenance truth, or acceptance.
"""

from __future__ import annotations

from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    ResourceManifest,
    ResourceManifestRefreshResult,
    ResourceReference,
    ValidationIssue,
    ValidationResult,
)

pytestmark = pytest.mark.software_verification
SUT = ResourceManifestRefreshResult


def make_refresh_result_manifest() -> ResourceManifest:
    """Evidence ID: Owns no identifier; supports refresh-result evidence.

    Requirement: Result tests require one independently valid manifest.

    Method: Construct one public manifest from fixed exact records.

    Oracle: Public DataObject constructors define valid support input.

    Acceptance: Return one valid ResourceManifest.

    Interpretation: Failure indicates invalid setup rather than result behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    identity = ArtifactIdentity(1, "sha256", "0" * 64)
    reference = ResourceReference(
        1, "example.resource", "reference", 1, "reference.txt", identity, ()
    )
    return ResourceManifest(1, "example.manifest", 1, "generic", None, (reference,))


def make_pass_validation_result() -> ValidationResult:
    """Evidence ID: Owns no identifier; supports successful result-state evidence.

    Requirement: Result tests require the exact issue-free validation state.

    Method: Construct ValidationResult with PASS and no issues.

    Oracle: The public validation contract fixes this exact state.

    Acceptance: Return a valid PASS ValidationResult.

    Interpretation: Failure indicates invalid setup rather than refresh-result behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    return ValidationResult(1, "PASS", ())


def make_fail_validation_result() -> ValidationResult:
    """Evidence ID: Owns no identifier; supports failed result-state evidence.

    Requirement: Result tests require one registered deterministic failure.

    Method: Construct a NOT_FOUND issue and matching FAIL result.

    Oracle: The public validation contract fixes issue and status consistency.

    Acceptance: Return one valid FAIL ValidationResult.

    Interpretation: Failure indicates invalid setup rather than refresh-result behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    issue = ValidationIssue(
        1,
        "PIH.RESOURCE.NOT_FOUND",
        "ERROR",
        "example.missing",
        None,
        (),
        "Resource ID was not found.",
    )
    return ValidationResult(1, "FAIL", (issue,))


def test_constructor__successful_fields__maps_exact_values() -> None:
    """Evidence ID: SV-HARNESS-084

    Requirement: A successful result contains an exact manifest, sorted changed IDs, and
    PASS.

    Method: Construct a successful result from independently valid public records.

    Oracle: The accepted result field and consistency contract fixes exact equality.

    Acceptance: Every field equals the supplied exact value.

    Interpretation: Failure indicates result mapping or successful-state drift.

    Limitations: The test does not establish that file bytes were observed correctly.
    """
    manifest = make_refresh_result_manifest()
    validation = make_pass_validation_result()
    result = SUT(manifest, ("example.resource",), validation)
    assert result.manifest is manifest
    assert result.changed_resource_ids == ("example.resource",)
    assert result.validation is validation


def test_constructor__failed_fields__maps_empty_result() -> None:
    """Evidence ID: SV-HARNESS-085

    Requirement: A failed result contains no refreshed manifest and no changed
    identifiers.

    Method: Construct the exact failed-state partition with one registered issue.

    Oracle: The accepted no-partial-result contract fixes both empty result fields.

    Acceptance: Construction succeeds with None, an empty tuple, and the exact FAIL
    result.

    Interpretation: Failure indicates failed-state representation drift.

    Limitations: Issue production and ordering across multiple findings are Action
    behavior.
    """
    validation = make_fail_validation_result()
    result = SUT(None, (), validation)
    assert result.manifest is None
    assert result.changed_resource_ids == ()
    assert result.validation is validation


@pytest.mark.parametrize(
    ("manifest", "changed", "validation", "exception"),
    [
        (object(), (), make_pass_validation_result(), TypeError),
        (
            make_refresh_result_manifest(),
            ["example.resource"],
            make_pass_validation_result(),
            TypeError,
        ),
        (
            make_refresh_result_manifest(),
            (1,),
            make_pass_validation_result(),
            TypeError,
        ),
        (
            make_refresh_result_manifest(),
            ("bad id",),
            make_pass_validation_result(),
            ValueError,
        ),
        (
            make_refresh_result_manifest(),
            ("example.resource", "example.resource"),
            make_pass_validation_result(),
            ValueError,
        ),
        (make_refresh_result_manifest(), (), object(), TypeError),
        (None, (), make_pass_validation_result(), ValueError),
        (
            make_refresh_result_manifest(),
            (),
            make_fail_validation_result(),
            ValueError,
        ),
        (
            None,
            ("example.resource",),
            make_fail_validation_result(),
            ValueError,
        ),
        (
            make_refresh_result_manifest(),
            ("example.missing",),
            make_pass_validation_result(),
            ValueError,
        ),
    ],
    ids=[
        "wrong_manifest_type",
        "wrong_changed_tuple_type",
        "wrong_changed_member_type",
        "malformed_changed_identifier",
        "duplicate_changed_identifier",
        "wrong_validation_type",
        "pass_without_manifest",
        "fail_with_manifest",
        "fail_with_changed_id",
        "changed_id_absent_from_manifest",
    ],
)
def test_constructor__invalid_result_state__raises_semantic_exception(
    manifest: Any,
    changed: Any,
    validation: Any,
    exception: type[Exception],
) -> None:
    """Evidence ID: SV-HARNESS-086

    Requirement: Result field types and success/failure/membership invariants fail
    closed.

    Method: Construct every required wrong-type and inconsistent-state partition.

    Oracle: The public result contract fixes TypeError versus ValueError behavior.

    Acceptance: Every case raises its declared semantic exception family.

    Interpretation: Failure indicates partial-result leakage or intrinsic-invariant
    drift.

    Limitations: This does not assess external file or manifest semantics.
    """
    with pytest.raises(exception):
        SUT(manifest, changed, validation)


def test_method__eq__and_frozen_assignment__follow_exact_value_semantics() -> None:
    """Evidence ID: SV-HARNESS-087

    Requirement: Equal field values produce equal immutable ResultObjects.

    Method: Construct two exact results, compare them, then attempt field assignment.

    Oracle: Frozen dataclass equality and assignment semantics are the exact oracle.

    Acceptance: Results compare equal and assignment raises AttributeError.

    Interpretation: Failure indicates value-semantic or immutability drift.

    Limitations: Equality does not establish scientific or semantic equivalence of
    resources.
    """
    first = SUT(
        make_refresh_result_manifest(),
        ("example.resource",),
        make_pass_validation_result(),
    )
    second = SUT(
        make_refresh_result_manifest(),
        ("example.resource",),
        make_pass_validation_result(),
    )
    assert first == second
    field = "manifest"
    with pytest.raises(AttributeError):
        setattr(first, field, None)
