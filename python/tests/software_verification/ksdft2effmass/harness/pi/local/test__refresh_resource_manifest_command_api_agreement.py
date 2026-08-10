r"""Software verification of refresh resource manifest command api agreement.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of the thin read-only CLI projection of the public resource
manifest refresh API.

Intrinsic and cross-object scope

The primary owner is the command/API agreement artifact. Explicit argument parsing,
deserialization, ActionObject invocation, canonical proposed text, exit status, and
nonwriting behavior are in scope.

VVUQ and scientific exclusions

Passing establishes command/API software agreement only, not resource semantics,
scientific validity, uncertainty quantification, provenance truth, or acceptance.
"""

from __future__ import annotations

import hashlib
import json
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
from ksdft2effmass.harness.pi.local.refresh_resource_manifest import main

pytestmark = pytest.mark.software_verification


def make_cli_resource_manifest() -> ResourceManifest:
    """Evidence ID: Owns no identifier; supports command/API agreement evidence.

    Requirement: Agreement tests require one independently valid manifest input.

    Method: Construct one public manifest from fixed exact records.

    Oracle: Public DataObject constructors define valid support input.

    Acceptance: Return one valid ResourceManifest.

    Interpretation: Failure indicates invalid setup rather than CLI behavior.

    Limitations: This helper owns no independent evidence claim.
    """
    identity = ArtifactIdentity(1, "sha256", hashlib.sha256(b"old").hexdigest())
    reference = ResourceReference(
        1, "example.resource", "reference", 1, "resource.txt", identity, ()
    )
    return ResourceManifest(1, "example.manifest", 1, "generic", None, (reference,))


def test_artifact__command_api__emits_equal_canonical_read_only_proposal(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: SV-HARNESS-096

    Requirement: The stable CLI emits the same canonical manifest proposed by the public
    API and
    does not modify the explicit manifest file.

    Method: Serialize a controlled manifest, invoke CLI main with explicit absolute
    paths,
    and compare its JSON projection with direct ActionObject and serializer output.

    Oracle: The public ActionObject plus maintained serializer provide the independent
    command-projection oracle.

    Acceptance: Exit is 0, status and changed IDs agree, proposed text is byte-for-byte
    canonical,
    and manifest input bytes remain unchanged.

    Interpretation: Failure indicates wrapper parsing, projection, or write-boundary
    drift.

    Limitations: Direct ``main`` invocation does not test shell or interpreter
    installation.
    """
    root = tmp_path / "root"
    root.mkdir()
    (root / "resource.txt").write_bytes(b"new bytes")
    manifest = make_cli_resource_manifest()
    serialized = JsonRecordSerializer().execute(manifest).payload
    assert serialized is not None
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_bytes(serialized)

    request = ResourceManifestRefreshRequest(
        root.resolve(), manifest, ("example.resource",)
    )
    api_result = ResourceManifestRefresher().execute(request)
    assert api_result.manifest is not None
    expected = JsonRecordSerializer().execute(api_result.manifest).payload
    assert expected is not None

    exit_status = main(
        (
            "--root",
            str(root.resolve()),
            "--manifest",
            str(manifest_path.resolve()),
            "--resource-id",
            "example.resource",
        )
    )
    output = json.loads(capsys.readouterr().out)

    assert exit_status == 0
    assert output["status"] == api_result.validation.status
    assert output["changed_resource_ids"] == list(api_result.changed_resource_ids)
    assert output["proposed_manifest"] == expected.decode("utf-8")
    assert manifest_path.read_bytes() == serialized


def test_artifact__command_api__returns_structured_failure_without_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: SV-HARNESS-097

    Requirement: Action validation failure produces exit 1, deterministic findings, no
    proposal,
    and no manifest-file mutation.

    Method: Invoke the CLI for one manifest-declared file absent from the explicit root.

    Oracle: Public ActionObject failure semantics fix the PATH.MISSING projection.

    Acceptance: Exit is 1, proposal is null, exact finding is present, and input bytes
    are equal.

    Interpretation: Failure indicates partial output, wrong exit mapping, or hidden
    write.

    Limitations: Invalid JSON and command-construction errors are neighboring
    serializer/CLI
    partitions rather than this agreement case.
    """
    root = tmp_path / "root"
    root.mkdir()
    serialized = JsonRecordSerializer().execute(make_cli_resource_manifest()).payload
    assert serialized is not None
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_bytes(serialized)

    exit_status = main(
        (
            "--root",
            str(root.resolve()),
            "--manifest",
            str(manifest_path.resolve()),
            "--resource-id",
            "example.resource",
        )
    )
    output = json.loads(capsys.readouterr().out)

    assert exit_status == 1
    assert output["proposed_manifest"] is None
    assert [finding["code"] for finding in output["findings"]] == ["PIH.PATH.MISSING"]
    assert manifest_path.read_bytes() == serialized
