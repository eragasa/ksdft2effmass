r"""Software verification of ``LocalHarnessContextLoader``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies explicit-root composition of the local harness context.

Intrinsic and cross-object scope

``LocalHarnessContextLoader`` is the sole system under test; input records remain caller
owned.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    LocalHarnessContext,
    LocalHarnessContextLoader,
    RepositoryRoots,
)

from .conftest import local_context, repository_root

pytestmark = pytest.mark.software_verification
SUT = LocalHarnessContextLoader


def test_method__execute__rejects_invalid_profile_and_unconfined_roots(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-006

    Requirement: Context composition uses only explicit valid roots and supplied
    resource bytes.

    Method: Load current explicit inputs, then supply invalid profile bytes and invalid
    roots.

    Oracle: The public contract requires an absolute confined root set and a valid
    explicit profile.

    Acceptance: Valid inputs produce ``LocalHarnessContext``; invalid profile reports
    ``PIHL.CONTEXT.PROFILE_INVALID``; relative or outside roots raise ``ValueError``;
    and a symlinked resource root reports ``PIHL.CONTEXT.ROOT_INVALID``.

    Interpretation: Failure indicates ambient discovery or weakened confinement.

    Limitations: Concurrent filesystem replacement, installation relocation,
    scientific validity, and UQ are excluded.
    """
    context = local_context()
    assert isinstance(context, LocalHarnessContext)
    root = repository_root()
    roots = RepositoryRoots(root, root / "harness/pi", root / "harness/local")
    result = LocalHarnessContextLoader().execute(
        roots,
        b"{}",
        (root / "harness/pi/resource-manifest.json").read_bytes(),
        (root / "harness/local/resource-manifest.json").read_bytes(),
    )
    assert result.validation.issues[0].code == "PIHL.CONTEXT.PROFILE_INVALID"
    with pytest.raises(ValueError):
        RepositoryRoots(Path("."), root / "harness/pi", root / "harness/local")
    outside = tmp_path.resolve()
    outside.mkdir(exist_ok=True)
    with pytest.raises(ValueError):
        RepositoryRoots(root, outside, root / "harness/local")
    temporary_root = tmp_path / "explicit-repository"
    generic = temporary_root / "generic"
    local = temporary_root / "local"
    generic.mkdir(parents=True)
    local.mkdir()
    linked_generic = temporary_root / "linked-generic"
    linked_generic.symlink_to(generic, target_is_directory=True)
    linked_roots = RepositoryRoots(temporary_root, linked_generic, local)
    linked = LocalHarnessContextLoader().execute(linked_roots, b"{}", b"{}", b"{}")
    assert linked.validation.issues[0].code == "PIHL.CONTEXT.ROOT_INVALID"
