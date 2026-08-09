r"""Software verification of ``HarnessTaskMigrationReviewPacketRenderer``.

Facet and represented meaning

Software verification of deterministic complete human-readable migration review.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskMigrationReviewPacketRenderer``. It revalidates a
prepared packet and owns presentation, strict UTF-8 handling, fence safety, and exact
review-document bytes.

VVUQ and scientific exclusions

Passing establishes rendering behavior only. The document is not operational authority,
a migration decision, scientific validation, or human acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import (
    HarnessTaskMigrationReviewPacketPreparer,
    HarnessTaskMigrationReviewPacketRenderer,
)

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskMigrationReviewPacketRenderer


def expected_document_bytes() -> bytes:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Exact expected Markdown bytes remain separate from production code.

    Method: Read the retained test-owned fixture adjacent to this module.

    Oracle: The reviewed literal fixture is the independent exact-byte oracle.

    Acceptance: Return fixture bytes without decoding or normalization.

    Interpretation: Failure identifies missing or unreadable test evidence.

    Limitations: This helper owns no independent evidence result.
    """
    return (
        Path(__file__).with_name("fixtures") / "harness-task-migration-review.md"
    ).read_bytes()


def test_method__execute__renders_exact_complete_review_document() -> None:
    """Evidence ID: ``SV-HT-054``.

    Requirement: Rendering exposes the complete before/after material, mappings,
    comparison, rollback identity, limitations, and exactly four human choices.

    Method: Render one prepared synthetic packet and compare every byte with a retained
    literal fixture.

    Oracle: The test-owned fixture independently fixes stable ordering, complete blocks,
    labels, table, diff, claim boundary, choices, and final LF.

    Acceptance: Content equals the fixture byte-for-byte; path and SHA-256 agree
    exactly; each choice occurs once.

    Interpretation: Failure identifies missing review material or presentation drift.

    Limitations: Synthetic material does not authorize or validate a real migration.
    """
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(make_request())
    result = SUT().execute(packet)
    expected = expected_document_bytes()
    assert result.path == "docs/example.md.migration-review.md"
    assert result.content == expected
    assert result.artifact_identity == identity(expected)
    assert result.content.count(b"Accept this file migration.") == 1
    assert result.content.count(b"Revise the contract or mappings.") == 1
    assert result.content.count(b"Retain Markdown ownership.") == 1
    assert result.content.count(b"Defer the file.") == 1


def test_method__execute__is_deterministic_and_fence_safe() -> None:
    """Evidence ID: ``SV-HT-055``.

    Requirement: Equal packets render byte-identically and embedded backtick or tilde
    fence runs cannot terminate enclosed source or candidate documentation.

    Method: Render one equal packet twice using source bytes containing both fence
    characters and inspect the selected source fence and exact included bytes.

    Oracle: A fence longer than every enclosed backtick run cannot be closed by the
    content; tilde runs cannot close a backtick fence.

    Acceptance: Results are equal, the selected fence is longer than the five-backtick
    source run, and the complete source text occurs unchanged.

    Interpretation: Failure identifies nondeterminism or unsafe fenced presentation.

    Limitations: Markdown implementations outside CommonMark-compatible fence behavior
    are not evaluated.
    """
    source = b"# Embedded fences\n`````\n~~~~~~\nopaque content\n"
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(
        make_request(source_bytes=source)
    )
    first = SUT().execute(packet)
    second = SUT().execute(packet)
    assert first == second
    assert b"``````markdown\n" in first.content
    assert source in first.content


def test_method__execute__rejects_invalid_utf8_source() -> None:
    """Evidence ID: ``SV-HT-056``.

    Requirement: Human-readable rendering fails closed when arbitrary source bytes are
    not valid UTF-8.

    Method: Prepare a structurally valid packet containing one invalid UTF-8 byte and
    invoke the public renderer.

    Oracle: Strict UTF-8 decoding rejects byte ``0xff``.

    Acceptance: Rendering raises ``ValueError`` naming source content and UTF-8.

    Interpretation: Failure permits silent replacement or an unreadable human packet.

    Limitations: Internal packet preparation remains byte-oriented and may validly
    represent non-UTF-8 bytes before presentation is requested.
    """
    packet = HarnessTaskMigrationReviewPacketPreparer().execute(
        make_request(source_bytes=b"opaque \xff bytes\n")
    )
    with pytest.raises(ValueError, match="source content must be UTF-8"):
        SUT().execute(packet)
