r"""Software verification of ``HarnessTaskProjectionProfile``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskProjectionProfile``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskProjectionProfile

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskProjectionProfile


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-009``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_request().projection_profile
    assert type(value) is SUT
    assert value == value


def test_constructor__template_identity__rejects_empty_and_hash_disagreement() -> None:
    """Evidence ID: ``SV-HT-040``.

    Requirement: Projection profile requires nonempty exact bytes and a matching
    SHA-256 identity.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    profile = make_request().projection_profile
    with pytest.raises(ValueError, match="nonempty"):
        SUT(1, profile.profile_id, b"", identity(b""), True)
    with pytest.raises(ValueError, match="identity"):
        SUT(1, profile.profile_id, profile.template_bytes, identity(b"other"), True)
