#!/usr/bin/env python3
"""Verify retained package bytes, strict schemas, and bound predecessor identities."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

RUN_ID = (
    "ksdft2effmass.campaign.periodic-reduction.periodic1d."
    "single-band-fourier-reduction.v1.run-20261014T184707Z"
)
EXPECTED_OPTIMIZATION_REVISION = "d9a82252faa1b41d82cce11149329aa91b84dff0"
EXPECTED_PHYSKIT_REVISION = "62ee89870db74b7b8b374c42add72701fd95d3a4"


def sha256(path: Path) -> str:
    """Return one lowercase SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(document: dict[str, JsonValue]) -> bytes:
    """Return the evidence contract's canonical JSON bytes."""
    return (
        json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def json_object(wire: str | bytes, name: str) -> dict[str, JsonValue]:
    """Decode one JSON mapping under the recursive finite evidence boundary."""
    value: JsonValue = json.loads(wire)
    if not isinstance(value, dict):
        raise TypeError(f"{name} root must be a dict")
    return value


def main() -> int:
    """Verify the selected immutable evidence package without running its producer."""
    experiment = Path(__file__).resolve().parent
    repository = experiment.parents[3]
    package = experiment / "runs" / RUN_ID
    expected_manifest_identity = (
        (package / "evidence-package-identity.txt").read_text(encoding="utf-8").strip()
    )
    if expected_manifest_identity != f"sha256:{sha256(package / 'SHA256SUMS')}":
        raise ValueError("evidence-package identity does not match SHA256SUMS")

    entries: dict[str, str] = {}
    for line in (package / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, filename = line.split("  ", maxsplit=1)
        if filename in entries:
            raise ValueError("duplicate SHA256SUMS entry")
        entries[filename] = digest
    for filename, digest in entries.items():
        if sha256(package / filename) != digest:
            raise ValueError(f"digest mismatch: {filename}")

    documents: dict[str, dict[str, JsonValue]] = {}
    for name in ("input", "result", "verification"):
        wire = (package / f"{name}.json").read_bytes()
        document = json_object(wire, name)
        if canonical(document) != wire:
            raise ValueError(f"{name} is not canonical JSON")
        schema = json_object(
            (experiment / "schemas" / f"{name}.schema.json").read_text(
                encoding="utf-8"
            ),
            f"{name} schema",
        )
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(document)
        documents[name] = document

    verification = documents["verification"]
    parity = json_object(
        (package / "parity.json").read_text(encoding="utf-8"), "parity"
    )
    provenance = json_object(
        (package / "provenance.json").read_text(encoding="utf-8"), "provenance"
    )
    if verification.get("passes") is not True:
        raise ValueError("retained independent numerical verification did not pass")
    if parity.get("passes") is not True:
        raise ValueError("historical parity did not pass")
    dependencies = provenance.get("dependencies")
    if not isinstance(dependencies, dict):
        raise TypeError("provenance dependencies must be a dict")
    if (
        dependencies.get("projectkoios_optimization_git_revision")
        != EXPECTED_OPTIMIZATION_REVISION
        or dependencies.get("projectkoios_physkit_git_revision")
        != EXPECTED_PHYSKIT_REVISION
    ):
        raise ValueError("provenance dependency revisions do not match version v1")
    # Version-one execution dependencies remain frozen in this checksummed provenance
    # document and its retained source manifest. Live development declarations may
    # advance independently and are intentionally not treated as retained-run bytes.

    repository_provenance = provenance.get("repository")
    if not isinstance(repository_provenance, dict):
        raise TypeError("provenance repository record must be a dict")
    source_manifest_name = repository_provenance.get("source_manifest")
    source_manifest_digest = repository_provenance.get("source_manifest_sha256")
    if not isinstance(source_manifest_name, str) or not isinstance(
        source_manifest_digest, str
    ):
        raise TypeError("source-manifest name and digest are required")
    if sha256(package / source_manifest_name) != source_manifest_digest:
        raise ValueError("source manifest does not match retained provenance")

    predecessor = provenance.get("historical_predecessor")
    if not isinstance(predecessor, dict):
        raise TypeError("historical_predecessor must be a dict")
    predecessor_path = predecessor.get("repository_relative_path")
    predecessor_digests = predecessor.get("sha256")
    if not isinstance(predecessor_path, str) or not isinstance(
        predecessor_digests, dict
    ):
        raise TypeError("historical predecessor path and digests are required")
    for predecessor_filename, predecessor_digest in predecessor_digests.items():
        if not isinstance(predecessor_digest, str):
            raise TypeError("historical predecessor digest entries must be strings")
        if (
            sha256(repository / predecessor_path / predecessor_filename)
            != predecessor_digest
        ):
            raise ValueError(f"historical predecessor changed: {predecessor_filename}")

    print(RUN_ID)
    print(expected_manifest_identity)
    print("package-verification: pass")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"package-verification: fail: {error}", file=sys.stderr)
        raise
