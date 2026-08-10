r"""Software verification of ``ResourceManifestRefreshRequest``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of the immutable explicit-root refresh request.

Intrinsic and cross-object scope

The sole primary SUT is ``ResourceManifestRefreshRequest``. Intrinsic field types,
selection canonicalization, identifier validity, and immutability are in scope.
Filesystem observation and manifest refresh behavior are excluded.

VVUQ and scientific exclusions

Passing establishes only the stated software contract, not semantic correctness,
scientific validation, uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    ResourceManifest,
    ResourceManifestRefreshRequest,
    ResourceReference,
)

pytestmark = pytest.mark.software_verification
SUT = ResourceManifestRefreshRequest


def make_resource_manifest_request_fixture() -> ResourceManifest:
    """Evidence ID: Owns no identifier; supports request-constructor evidence.

    Requirement: Tests require one independently valid manifest input.

    Method: Construct one public manifest from fixed exact records.

    Oracle: Public DataObject constructors define valid support input.

    Acceptance: Return one valid ResourceManifest.

    Interpretation: Failure indicates invalid test setup rather than refresh behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    identity = ArtifactIdentity(1, "sha256", "0" * 64)
    reference = ResourceReference(
        1, "example.resource", "reference", 1, "reference.txt", identity, ()
    )
    return ResourceManifest(1, "example.manifest", 1, "generic", None, (reference,))


def test_constructor__valid_fields__maps_exact_values_and_canonical_selection(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-081

    Requirement: The request stores the explicit absolute root and exact manifest while
    canonicalizing a nonempty resource selection to sorted unique identifiers.

    Method: Construct the request with unsorted duplicate valid identifiers.

    Oracle: The accepted request contract and Python sorted-set semantics fix the
    fields.

    Acceptance: Root and manifest retain object identity and IDs equal the sorted unique
    tuple.

    Interpretation: Failure indicates field mapping or canonicalization drift.

    Limitations: No filesystem resource is observed and no manifest refresh is executed.
    """
    root = tmp_path.resolve()
    manifest = make_resource_manifest_request_fixture()
    request = SUT(root, manifest, ("example.z", "example.a", "example.z"))
    assert request.root is root
    assert request.manifest is manifest
    assert request.resource_ids == ("example.a", "example.z")


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    [
        ("root", "not-a-path", TypeError),
        ("root", Path("relative"), ValueError),
        ("manifest", object(), TypeError),
        ("resource_ids", ["example.resource"], TypeError),
        ("resource_ids", (), ValueError),
        ("resource_ids", (1,), TypeError),
        ("resource_ids", ("bad id",), ValueError),
    ],
    ids=[
        "wrong_root_type",
        "relative_root",
        "wrong_manifest_type",
        "wrong_selection_type",
        "empty_selection",
        "wrong_identifier_type",
        "malformed_identifier",
    ],
)
def test_constructor__invalid_field__raises_semantic_exception(
    tmp_path: Path, field: str, value: Any, exception: type[Exception]
) -> None:
    """Evidence ID: SV-HARNESS-082

    Requirement: Wrong semantic types raise TypeError and correctly typed invariant
    violations
    raise ValueError.

    Method: Replace one valid constructor field with each invalid semantic partition.

    Oracle: The public request invariant table fixes the exception class for every case.

    Acceptance: Construction raises exactly the declared TypeError or ValueError family.

    Interpretation: Failure indicates exception-taxonomy or intrinsic-validation drift.

    Limitations: Filesystem existence and selected-ID membership are ActionObject
    concerns.
    """
    values: dict[str, Any] = {
        "root": tmp_path.resolve(),
        "manifest": make_resource_manifest_request_fixture(),
        "resource_ids": ("example.resource",),
    }
    values[field] = value
    with pytest.raises(exception):
        SUT(**values)


def test_field__frozen_assignment__raises_attribute_error(tmp_path: Path) -> None:
    """Evidence ID: SV-HARNESS-083

    Requirement: Request state is immutable after construction.

    Method: Assign to a public field on a valid request.

    Oracle: Frozen dataclass semantics are the exact language-level oracle.

    Acceptance: Assignment raises AttributeError and stored state is unchanged.

    Interpretation: Failure indicates an unauthorized mutable request boundary.

    Limitations: Nested records are independently immutable under their own contracts.
    """
    request = SUT(
        tmp_path.resolve(),
        make_resource_manifest_request_fixture(),
        ("example.resource",),
    )
    field = "root"
    with pytest.raises(AttributeError):
        setattr(request, field, Path("/"))
