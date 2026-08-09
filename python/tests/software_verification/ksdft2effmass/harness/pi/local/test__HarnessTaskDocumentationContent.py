r"""Software verification of ``HarnessTaskDocumentationContent``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskDocumentationContent``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskDocumentationContent

from .task_model_examples import make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskDocumentationContent


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-008``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_request().documentation_content
    assert type(value) is SUT
    assert value == value


def test_constructor__mapping_alignment__rejects_misaligned_and_nonbyte_blocks() -> (
    None
):
    """Evidence ID: ``SV-HT-039``.

    Requirement: Documentation content requires aligned mapping IDs and exact
    nonempty bytes.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    request = make_request()
    content = request.documentation_content
    with pytest.raises(ValueError, match="align"):
        SUT(content.source_identity, content.documentation_path, ("a", "b"), (b"one",))
    with pytest.raises(TypeError, match="bytes"):
        SUT(content.source_identity, content.documentation_path, ("a",), ("text",))  # type: ignore[arg-type]
