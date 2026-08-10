r"""Software verification of ``ResourceManifestRefresher``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of deterministic explicit-path manifest identity refresh.

Intrinsic and cross-object scope

The sole primary SUT is ``ResourceManifestRefresher``. Explicit selection, confined
file observation, SHA-256 replacement, preservation, deterministic findings,
nonmutation, and stateless execution are in scope. Intrinsic record invariants remain
owned by their DataObjects.

VVUQ and scientific exclusions

Passing establishes byte-identity maintenance behavior only. It does not establish
resource semantics, provenance truth, scientific validity, uncertainty quantification,
or human acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    JsonRecordSerializer,
    ResourceManifest,
    ResourceManifestRefresher,
    ResourceManifestRefreshRequest,
    ResourceReference,
)

pytestmark = pytest.mark.software_verification
SUT = ResourceManifestRefresher


def make_artifact_identity(data: bytes) -> ArtifactIdentity:
    """Evidence ID: Owns no identifier; supports exact-byte refresh evidence.

    Requirement: Tests require independently computed SHA-256 identities.

    Method: Hash caller-supplied controlled bytes with hashlib.

    Oracle: Python's maintained hashlib SHA-256 supplies the oracle.

    Acceptance: Return one valid ArtifactIdentity for the exact bytes.

    Interpretation: Failure indicates test setup or environment failure.

    Limitations: This helper owns no independent evidence claim.
    """
    return ArtifactIdentity(1, "sha256", hashlib.sha256(data).hexdigest())


def make_resource_reference(
    resource_id: str,
    path: str,
    data: bytes = b"recorded bytes",
    dependencies: tuple[str, ...] = (),
) -> ResourceReference:
    """Evidence ID: Owns no identifier; supports refresh-action evidence.

    Requirement: Tests require explicit valid manifest references.

    Method: Construct a ResourceReference from fixed fields and an independent identity.

    Oracle: Public DataObject constructors define valid support input.

    Acceptance: Return one valid ResourceReference.

    Interpretation: Failure indicates invalid setup rather than Action behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    return ResourceReference(
        1,
        resource_id,
        "reference",
        2,
        path,
        make_artifact_identity(data),
        dependencies,
    )


def make_resource_manifest(*resources: ResourceReference) -> ResourceManifest:
    """Evidence ID: Owns no identifier; supports refresh-action evidence.

    Requirement: Tests require one canonical manifest over explicit references.

    Method: Construct a local ResourceManifest from caller-supplied references.

    Oracle: Public ResourceManifest construction defines canonical ordering.

    Acceptance: Return one valid canonical ResourceManifest.

    Interpretation: Failure indicates invalid setup rather than Action behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    return ResourceManifest(
        1, "example.resources", 2, "local", "example.generic", tuple(resources)
    )


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID: SV-HARNESS-088

    Requirement: ResourceManifestRefresher is a concrete stateless ActionObject.

    Method: Construct two instances and inspect their storage boundary.

    Oracle: The accepted action contract requires empty slots and no instance
    dictionary.

    Acceptance: Both instances construct and expose no mutable instance storage.

    Interpretation: Failure indicates hidden state or public ActionObject drift.

    Limitations: Structural statelessness does not establish execution correctness.
    """
    assert SUT.__slots__ == ()
    assert not hasattr(SUT(), "__dict__")
    assert not hasattr(SUT(), "__dict__")


def test_method__execute__refreshes_one_identity_and_preserves_manifest(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-089

    Requirement: Refreshing one selected resource replaces only its content identity
    using
    SHA-256 of exact observed bytes and performs no mutation or write.

    Method: Execute against one controlled file whose bytes differ from the manifest.

    Oracle: hashlib SHA-256, immutable input equality, and exact field values are
    independent
    oracles for the proposed manifest.

    Acceptance: Only the selected identity changes, all other fields and input objects
    are
    preserved, the output is new, and root bytes and entries remain unchanged.

    Interpretation: Failure indicates hashing, preservation, mutation, or write-boundary
    drift.

    Limitations: Byte equality does not establish semantic correctness or provenance.
    """
    observed = b"observed\x00bytes\n"
    path = tmp_path / "resource.bin"
    path.write_bytes(observed)
    reference = make_resource_reference("example.resource", "resource.bin")
    manifest = make_resource_manifest(reference)
    original_payload = JsonRecordSerializer().execute(manifest).payload
    before_entries = tuple(sorted(item.name for item in tmp_path.iterdir()))

    result = SUT().execute(
        ResourceManifestRefreshRequest(
            tmp_path.resolve(), manifest, ("example.resource",)
        )
    )

    assert result.validation.status == "PASS"
    assert result.changed_resource_ids == ("example.resource",)
    assert result.manifest is not None and result.manifest is not manifest
    refreshed = result.manifest.resources[0]
    assert refreshed is not reference
    assert refreshed.content_identity == make_artifact_identity(observed)
    assert replace(refreshed, content_identity=reference.content_identity) == reference
    assert JsonRecordSerializer().execute(manifest).payload == original_payload
    assert path.read_bytes() == observed
    assert tuple(sorted(item.name for item in tmp_path.iterdir())) == before_entries


def test_method__execute__refreshes_multiple_with_mixed_changed_selection(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-090

    Requirement: Explicit multiple selection distinguishes selected IDs from actually
    changed IDs
    and returns canonical manifest ordering.

    Method: Select three resources supplied in reverse order; two files differ and one
    already matches.

    Oracle: Exact bytes and ResourceManifest's accepted canonical ordering fix the
    result.

    Acceptance: Changed IDs contain only the two differing resources in sorted order and
    output
    resources are canonically ordered with every nonidentity field preserved.

    Interpretation: Failure indicates selection, change reporting, preservation, or
    ordering drift.

    Limitations: The test does not validate generic/local profile relationships.
    """
    reference_c = make_resource_reference(
        "example.c", "c.txt", b"old-c", ("example.a",)
    )
    reference_a = make_resource_reference("example.a", "a.txt", b"old-a")
    reference_b = make_resource_reference("example.b", "b.txt", b"same-b")
    (tmp_path / "c.txt").write_bytes(b"new-c")
    (tmp_path / "a.txt").write_bytes(b"new-a")
    (tmp_path / "b.txt").write_bytes(b"same-b")
    manifest = make_resource_manifest(reference_c, reference_a, reference_b)

    result = SUT().execute(
        ResourceManifestRefreshRequest(
            tmp_path.resolve(),
            manifest,
            ("example.c", "example.b", "example.a"),
        )
    )

    assert result.validation.status == "PASS"
    assert result.changed_resource_ids == ("example.a", "example.c")
    assert result.manifest is not None
    assert tuple(r.resource_id for r in result.manifest.resources) == (
        "example.a",
        "example.b",
        "example.c",
    )
    refreshed_a, refreshed_b, refreshed_c = result.manifest.resources
    assert (
        replace(refreshed_a, content_identity=reference_a.content_identity)
        == reference_a
    )
    assert refreshed_b is reference_b
    assert (
        replace(refreshed_c, content_identity=reference_c.content_identity)
        == reference_c
    )


def test_method__execute__matching_selection_returns_equal_new_manifest(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-091

    Requirement: Selected bytes that already match return successful unchanged manifest
    state.

    Method: Execute with a file whose exact SHA-256 is already recorded.

    Oracle: Exact dataclass equality and known bytes fix the unchanged result.

    Acceptance: Changed IDs are empty and the returned newly constructed manifest equals
    input.

    Interpretation: Failure indicates false change reporting or missing successful no-op
    behavior.

    Limitations: Equality is represented-state equality only.
    """
    data = b"already current"
    (tmp_path / "current.txt").write_bytes(data)
    manifest = make_resource_manifest(
        make_resource_reference("example.current", "current.txt", data)
    )
    result = SUT().execute(
        ResourceManifestRefreshRequest(
            tmp_path.resolve(), manifest, ("example.current",)
        )
    )
    assert result.validation.status == "PASS"
    assert result.changed_resource_ids == ()
    assert result.manifest == manifest
    assert result.manifest is not manifest


def test_method__execute__unknown_and_missing_resources_return_ordered_findings(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HARNESS-092

    Requirement: Unknown IDs and missing selected files produce deterministic structured
    failure
    with no partial manifest.

    Method: Select one absent manifest ID and one declared path absent from an existing
    root.

    Oracle: The registered issue ordering sorts PIH.PATH before PIH.RESOURCE codes.

    Acceptance: Codes have the exact deterministic order and result values are empty.

    Interpretation: Failure indicates discovery, partial refresh, or issue-ordering
    drift.

    Limitations: Only two independent failure partitions are aggregated.
    """
    manifest = make_resource_manifest(
        make_resource_reference("example.missing", "missing.txt")
    )
    result = SUT().execute(
        ResourceManifestRefreshRequest(
            tmp_path.resolve(), manifest, ("example.unknown", "example.missing")
        )
    )
    assert [issue.code for issue in result.validation.issues] == [
        "PIH.PATH.MISSING",
        "PIH.RESOURCE.NOT_FOUND",
    ]
    assert result.manifest is None
    assert result.changed_resource_ids == ()


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("case_mismatch", "PIH.PATH.CASE_MISMATCH"),
        ("symlink", "PIH.PATH.SYMLINK"),
        ("nonregular", "PIH.PATH.NOT_FILE"),
    ],
    ids=["case_mismatch", "symlink", "nonregular_file"],
)
def test_method__execute__unsafe_or_nonregular_path_is_rejected(
    tmp_path: Path, case: str, expected_code: str
) -> None:
    """Evidence ID: SV-HARNESS-093

    Requirement: Refresh reuses exact-case, nonsymlink, regular-file resource
    confinement.

    Method: Execute controlled case-mismatch, symlink, and directory partitions.

    Oracle: The existing explicit-root resource-resolution contract fixes each issue
    code.

    Acceptance: The exact expected singleton code is returned with no manifest.

    Interpretation: Failure indicates divergence from maintained resource path
    observation.

    Limitations: Platform-independent lexical traversal rejection is covered separately.
    """
    if case == "case_mismatch":
        (tmp_path / "Actual.txt").write_bytes(b"data")
        path = "actual.txt"
    elif case == "symlink":
        (tmp_path / "target.txt").write_bytes(b"data")
        (tmp_path / "link.txt").symlink_to("target.txt")
        path = "link.txt"
    else:
        (tmp_path / "directory").mkdir()
        path = "directory"
    manifest = make_resource_manifest(make_resource_reference("example.resource", path))
    result = SUT().execute(
        ResourceManifestRefreshRequest(
            tmp_path.resolve(), manifest, ("example.resource",)
        )
    )
    assert [issue.code for issue in result.validation.issues] == [expected_code]
    assert result.manifest is None


def test_method__execute__validated_resource_path_prevents_traversal_input() -> None:
    """Evidence ID: SV-HARNESS-094

    Requirement: Public refresh input cannot contain a traversal path because
    ResourcePath owns
    lexical traversal rejection before Action execution.

    Method: Attempt to construct a selected ResourceReference with a parent segment.

    Oracle: The existing ResourcePath intrinsic contract requires INVALID_SEGMENT
    rejection.

    Acceptance: Public input construction raises ValueError containing the registered
    code.

    Interpretation: Failure would expose a traversal route before confined observation.

    Limitations: This checks the accepted DataObject gate rather than bypassing it with
    private
    object mutation.
    """
    with pytest.raises(ValueError, match="PIH.PATH.INVALID_SEGMENT"):
        make_resource_reference("example.escape", "../escape.txt")


def test_method__execute__is_cwd_independent_read_only_and_repeatable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID: SV-HARNESS-095

    Requirement: Execution uses only explicit inputs, performs no implicit write, and
    repeated
    identical invocation returns an equal result from a nonrepository CWD.

    Method: Change CWD to an unrelated directory, snapshot explicit-root state, and
    execute
    the same request twice.

    Oracle: Exact result equality and unchanged directory bytes/names are independent
    oracles.

    Acceptance: Results compare equal and no explicit-root file or directory entry
    changes.

    Interpretation: Failure indicates ambient discovery, nondeterminism, mutation, or
    hidden write.

    Limitations: The test does not trace operating-system reads outside Python's public
    APIs.
    """
    root = tmp_path / "explicit-root"
    root.mkdir()
    data = b"deterministic"
    resource = root / "resource.txt"
    resource.write_bytes(data)
    elsewhere = tmp_path / "unrelated-cwd"
    elsewhere.mkdir()
    manifest = make_resource_manifest(
        make_resource_reference("example.resource", "resource.txt", b"old")
    )
    request = ResourceManifestRefreshRequest(
        root.resolve(), manifest, ("example.resource",)
    )
    before = (tuple(sorted(p.name for p in root.iterdir())), resource.read_bytes())
    monkeypatch.chdir(elsewhere)

    first = SUT().execute(request)
    second = SUT().execute(request)

    assert first == second
    assert (
        tuple(sorted(p.name for p in root.iterdir())),
        resource.read_bytes(),
    ) == before
