r"""Software verification of ``HarnessTaskMigrationDisposition``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationDisposition``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskMigrationDisposition

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationDisposition


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-017``.

    Requirement: The public enum exposes exactly its accepted closed vocabulary.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    assert tuple(item.value for item in SUT) == (
        "ACCEPT_FILE_MIGRATION",
        "REVISE_CONTRACT_OR_MAPPING",
        "RETAIN_DOCUMENTATION_OWNERSHIP",
        "DEFER_FILE",
    )
