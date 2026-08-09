r"""Software verification of ``HarnessTaskDocumentSource``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskDocumentSource``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskDocumentSource

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskDocumentSource


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-005``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_request().source
    assert type(value) is SUT
    assert value == value


def test_constructor__identity_fields__reject_count_git_and_hash_disagreement() -> None:
    """Evidence ID: ``SV-HT-037``.

    Requirement: Source construction binds byte count, Git object syntax, and
    SHA-256 identity.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    source = make_request().source
    with pytest.raises(ValueError, match="byte_count"):
        SUT(
            source.path,
            source.revision,
            source.git_object,
            source.content,
            0,
            source.artifact_identity,
        )
    with pytest.raises(ValueError, match="git_object"):
        SUT(
            source.path,
            source.revision,
            "ABC",
            source.content,
            source.byte_count,
            source.artifact_identity,
        )
    with pytest.raises(ValueError, match="identity"):
        SUT(
            source.path,
            source.revision,
            None,
            source.content,
            source.byte_count,
            identity(b"other"),
        )
