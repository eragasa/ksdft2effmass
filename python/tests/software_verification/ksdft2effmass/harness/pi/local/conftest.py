"""Shared construction support for project-local software verification."""

from __future__ import annotations

from pathlib import Path

from ksdft2effmass.harness.pi.local import (
    LoadLocalHarnessContext,
    LocalHarnessContext,
    RepositoryRoots,
)


def repository_root() -> Path:
    """Evidence ID
    Owns no identifier; supports SV-HL-001 through SV-HL-037.
    Requirement
    Local harness evidence requires one explicit repository root independent of the
    process current directory.
    Method
    Resolve the fixed parent depth of this test-owned support module.
    Oracle
    The mirrored test hierarchy fixes the repository root at parent seven.
    Acceptance
    Return one absolute ``Path`` naming the current repository checkout.
    Interpretation
    Failure indicates test-layout drift rather than a production harness defect.
    Limitations
    This helper owns no evidence result and does not validate repository contents.
    """
    return Path(__file__).resolve().parents[7]


def local_context() -> LocalHarnessContext:
    """Evidence ID
    Owns no identifier; supports SV-HL-003 through SV-HL-013 and SV-HL-036 through
    SV-HL-037.
    Requirement
    Local composition evidence consumes explicit current profile and manifest bytes.
    Method
    Construct public roots and call ``LoadLocalHarnessContext`` with the three
    maintained resource files.
    Oracle
    The public loader contract requires a complete ``LocalHarnessContext`` for
    mutually consistent current resources.
    Acceptance
    The action returns an exact ``LocalHarnessContext`` value without fallback
    discovery.
    Interpretation
    Failure identifies stale resource identities, composition drift, or bad setup.
    Limitations
    This helper does not independently validate the resources or own an evidence ID.
    """
    root = repository_root()
    roots = RepositoryRoots(root, root / "harness/pi", root / "harness/local")
    result = LoadLocalHarnessContext().execute(
        roots,
        (root / "harness/local/profiles/ksdft2effmass-v2.json").read_bytes(),
        (root / "harness/pi/resource-manifest.json").read_bytes(),
        (root / "harness/local/resource-manifest.json").read_bytes(),
    )
    assert isinstance(result.value, LocalHarnessContext)
    return result.value
