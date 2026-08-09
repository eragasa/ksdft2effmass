r"""Software verification of ``HarnessTaskMigrationReviewDocument``.

Facet and represented meaning

Software verification of the runtime-only human-readable migration-review document.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationReviewDocument``. Rendering and packet
agreement belong to ``HarnessTaskMigrationReviewPacketRenderer``.

VVUQ and scientific exclusions

Passing establishes exact DataObject invariants only. It does not establish migration
correctness, provenance truth, human authority, scientific validity, or acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskMigrationReviewDocument

from .task_model_examples import identity

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationReviewDocument


def test_constructor__fields__retain_exact_runtime_document() -> None:
    """Evidence ID: ``SV-HT-052``.

    Requirement: The runtime result retains path, exact UTF-8 bytes with one final LF,
    and their matching SHA-256 identity.

    Method: Construct one explicit synthetic document and inspect fields and value.

    Oracle: The accepted narrow interface defines the three fields in exact order and
    ``hashlib``-derived support supplies the byte identity.

    Acceptance: Field order and retained values equal the explicit inputs exactly.

    Interpretation: Failure identifies public field or exact-value drift.

    Limitations: Construction does not establish that content came from a packet.
    """
    content = b"# Synthetic review\n"
    value = SUT("docs/example.review.md", content, identity(content))
    assert tuple(field.name for field in fields(SUT)) == (
        "path",
        "content",
        "artifact_identity",
    )
    assert value.path == "docs/example.review.md"
    assert value.content == content
    assert value.artifact_identity == identity(content)


@pytest.mark.parametrize(
    "content",
    (
        pytest.param(b"missing final LF", id="missing_final_lf"),
        pytest.param(b"two final LFs\n\n", id="two_final_lfs"),
        pytest.param(b"invalid UTF-8: \xff\n", id="invalid_utf8"),
    ),
)
def test_constructor__content__rejects_noncanonical_document_bytes(
    content: bytes,
) -> None:
    """Evidence ID: ``SV-HT-053``.

    Requirement: Review-document bytes are UTF-8 with exactly one final LF.

    Method: Construct independently invalid final-LF and UTF-8 partitions.

    Oracle: Literal byte endings and strict UTF-8 decoding define exact acceptance.

    Acceptance: Every invalid partition raises ``ValueError``.

    Interpretation: Failure permits ambiguous or unreadable review-document bytes.

    Limitations: Other Markdown semantics are renderer-owned.
    """
    with pytest.raises(ValueError):
        SUT("docs/example.review.md", content, identity(content))
