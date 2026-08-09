"""Shared synthetic constructors for HarnessTask software-verification tests.

This helper module owns no evidence identifier or independent acceptance claim.
"""

from __future__ import annotations

import hashlib
import json

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


def _represented_identity(value: ArtifactIdentity) -> dict[str, object]:
    """Represent an identity with explicit independently readable fields."""
    return {
        "algorithm": value.algorithm,
        "digest": value.digest,
        "schema_version": value.schema_version,
    }


def _detail(value: object) -> str:
    """Return the exact canonical observation detail used by the public contract."""
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def make_request(
    *,
    source_bytes: bytes = b"Synthetic introduction.\n",
    git_object: str | None = "b" * 40,
) -> HarnessTaskMigrationReviewPacketRequest:
    """Construct one compatible explicit packet-preparation request."""
    task = make_task()
    source = HarnessTaskDocumentSource(
        "records/example-source.md",
        "a" * 40,
        git_object,
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
        f"harness-task-migration.{task.task_id}",
        source.revision,
        f"HarnessTask migration candidate {task.task_id} from {source.path} to "
        f"{rendered.path}",
        (source.path, rendered.path),
        "software_verification",
        (
            ".pi/evidence/docs-json/task-model-contract/harness-task-contract.md",
            ".pi/tasks/harness.simplification.docs-json.task-document-migration.json",
            ".pi/evidence/task-control/task-document-human-mediation-decision.md",
        ),
    )
    canonical_json = HarnessTaskSerializer().execute(task)
    observations = (
        HumanReviewObservation(
            "harness-task-migration.candidate-json",
            "candidate canonical HarnessTask JSON identity",
            "passed",
            "The candidate canonical JSON is bound to the reviewed packet.",
            task.documentation_path,
            _detail(
                {
                    "byte_count": len(canonical_json),
                    "candidate_task_id": task.task_id,
                    "identity": _represented_identity(identity(canonical_json)),
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.comparison",
            "exact source and rendered byte comparison",
            "passed",
            "The exact comparison result is bound to the reviewed packet.",
            rendered.path,
            _detail(
                {
                    "differences": [],
                    "rendered_identity": _represented_identity(
                        rendered.artifact_identity
                    ),
                    "source_identity": _represented_identity(source.artifact_identity),
                    "status": "EXACT",
                    "unmapped_spans": [],
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.limitations",
            "applicable comparison limitations",
            "passed",
            "Every applicable comparison limitation is bound to the packet.",
            rendered.path,
            _detail({"limitations": list(comparison.limitations)}),
        ),
        HumanReviewObservation(
            "harness-task-migration.mappings",
            "source mappings and unmapped-span account",
            "passed",
            "All source mappings and unmapped spans are bound to the packet.",
            source.path,
            _detail(
                {
                    "mappings": [
                        {
                            "disposition": mapping.disposition.value,
                            "end_byte": mapping.end_byte,
                            "mapping_id": mapping.mapping_id,
                            "rationale": mapping.rationale,
                            "source_identity": _represented_identity(
                                mapping.source_identity
                            ),
                            "span_identity": _represented_identity(
                                mapping.span_identity
                            ),
                            "start_byte": mapping.start_byte,
                            "target_references": list(mapping.target_references),
                            "transformation": mapping.transformation,
                        }
                    ],
                    "unmapped_spans": [],
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.opaque-blocks",
            "opaque documentation-block preservation",
            "passed",
            "Every documentation-owned source block is preserved exactly.",
            rendered.path,
            _detail(
                {
                    "documentation_blocks": [
                        {
                            "mapping_id": mapping.mapping_id,
                            "preserved": True,
                            "span_identity": _represented_identity(
                                mapping.span_identity
                            ),
                        }
                    ]
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.rendered",
            "rendered-document identity",
            "passed",
            "The rendered document bytes are bound to the reviewed packet.",
            rendered.path,
            _detail(
                {
                    "byte_count": len(rendered.content),
                    "identity": _represented_identity(rendered.artifact_identity),
                }
            ),
        ),
        HumanReviewObservation(
            "harness-task-migration.source",
            "source identity and byte count",
            "passed",
            "The exact source bytes are bound to the reviewed packet.",
            source.path,
            _detail(
                {
                    "artifact_identity": _represented_identity(
                        source.artifact_identity
                    ),
                    "byte_count": source.byte_count,
                    "git_object": source.git_object,
                    "path": source.path,
                    "revision": source.revision,
                }
            ),
        ),
    )
    review = HumanReviewPreparer().execute(
        target, observations, comparison.findings, comparison.limitations
    )
    return HarnessTaskMigrationReviewPacketRequest(
        source,
        (mapping,),
        task,
        canonical_json,
        content,
        profile,
        rendered,
        comparison,
        review,
    )
