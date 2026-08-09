"""Shared synthetic constructors for HarnessTask software-verification tests.

This helper module owns no evidence identifier or independent acceptance claim.
"""

from __future__ import annotations

import hashlib

from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    HumanReviewObservation,
    HumanReviewPreparer,
    HumanReviewTarget,
)
from ksdft2effmass.harness.pi.local import (
    HarnessTask,
    HarnessTaskDocumentationComparator,
    HarnessTaskDocumentationContent,
    HarnessTaskDocumentationRenderer,
    HarnessTaskDocumentSource,
    HarnessTaskMigrationReviewPacketRequest,
    HarnessTaskProjectionProfile,
    HarnessTaskSerializer,
    HarnessTaskSourceDisposition,
    HarnessTaskSourceMapping,
)


def identity(content: bytes) -> ArtifactIdentity:
    """Return the independently calculated SHA-256 identity."""
    return ArtifactIdentity(1, "sha256", hashlib.sha256(content).hexdigest())


def make_task(**changes: object) -> HarnessTask:
    """Construct one valid synthetic Task with explicit overrides."""
    values: dict[str, object] = {
        "schema_version": 2,
        "task_id": "example.task",
        "title": "Example Task",
        "status": "proposed",
        "status_detail": None,
        "parent_task_id": None,
        "task_prerequisite_ids": (),
        "external_prerequisite_ids": (),
        "explicit_activation_required": True,
        "objective": "Verify the accepted software contract.",
        "authority_reference_paths": ("records/decision.md",),
        "authorized_scope": ("Use synthetic test data.",),
        "completion_criteria": ("Exact checks pass.",),
        "exclusions": ("No migration is authorized.",),
        "intake_path": "records/example.intake.md",
        "documentation_path": "docs/example.md",
    }
    values.update(changes)
    return HarnessTask(**values)  # type: ignore[arg-type]


def make_request() -> HarnessTaskMigrationReviewPacketRequest:
    """Construct one compatible explicit packet-preparation request."""
    task = make_task()
    source_bytes = b"Synthetic introduction.\n"
    source = HarnessTaskDocumentSource(
        "records/example-source.md",
        "a" * 40,
        "b" * 40,
        source_bytes,
        len(source_bytes),
        identity(source_bytes),
    )
    mapping = HarnessTaskSourceMapping(
        "intro",
        source.artifact_identity,
        0,
        len(source_bytes),
        identity(source_bytes),
        HarnessTaskSourceDisposition.DOCUMENTATION_OWNED_CONTENT,
        ("docs/example.md",),
        "preserve exact bytes",
        "synthetic documentation content",
    )
    content = HarnessTaskDocumentationContent(
        source.artifact_identity,
        task.documentation_path,
        (mapping.mapping_id,),
        (source_bytes,),
    )
    template = b"{{content.intro}}"
    profile = HarnessTaskProjectionProfile(
        1, "synthetic-profile", template, identity(template), True
    )
    rendered = HarnessTaskDocumentationRenderer().execute(task, content, profile)
    comparison = HarnessTaskDocumentationComparator().execute(
        source, rendered, (mapping,)
    )
    target = HumanReviewTarget(
        "synthetic-migration-review",
        source.revision,
        "Synthetic non-migration example",
        (source.path, rendered.path),
        "software_verification",
        ("records/contract.md",),
    )
    observation = HumanReviewObservation(
        "synthetic-rendering-observation",
        "exact representative rendering",
        "passed",
        "Synthetic source and rendering agree exactly.",
        rendered.path,
    )
    review = HumanReviewPreparer().execute(target, (observation,), (), ())
    return HarnessTaskMigrationReviewPacketRequest(
        source,
        (mapping,),
        task,
        HarnessTaskSerializer().execute(task),
        content,
        profile,
        rendered,
        comparison,
        review,
    )
