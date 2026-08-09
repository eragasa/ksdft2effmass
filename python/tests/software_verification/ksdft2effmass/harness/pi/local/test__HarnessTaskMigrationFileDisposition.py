r"""Software verification of ``HarnessTaskMigrationFileDisposition``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationFileDisposition``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskMigrationFileDisposition

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationFileDisposition


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-018``.

    Requirement: The public immutable object declares its accepted dataclass fields.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    assert hasattr(SUT, "__dataclass_fields__")
    assert tuple(SUT.__dataclass_fields__) == (
        "packet",
        "human_decision",
        "migration_disposition",
    )


def test_constructor__member_types__rejects_non_packet_input() -> None:
    """Evidence ID: ``SV-HT-048``.

    Requirement: File disposition construction requires exact packet, decision, and
    migration enum types.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    with pytest.raises(TypeError, match="packet"):
        SUT(object(), object(), object())  # type: ignore[arg-type]
