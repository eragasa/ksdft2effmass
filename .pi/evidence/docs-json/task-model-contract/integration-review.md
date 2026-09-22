# HarnessTask model-contract independent integration review

Review status: failed

Reviewed base revision: `dd50c74513f6c51e2a1c823a60b3111738082b3c`

Reviewer role: `ksdft2effmass.ksdft2effmass-harness-integration-reviewer`

Review scope: Read-only review of the six-source inventory, complete source mappings, frozen 19-interface contract, maintained review pages, active Task, six source Tasks, and existing identity, human-review, wire, and Task-pilot contracts.

## Material findings

1. Blocker: Generic/project-local ownership was reversed. The draft placed Task vocabulary, schema, and all interfaces in generic `harness/pi` and `ksdft2effmass.harness.pi`, contrary to the accepted project-local Task/control ownership boundary.
2. High: `HTM-03-014`, `HTM-04-012`, and `HTM-06-015` used `CANONICAL_TASK_INFORMATION` while promising exact documentation-byte preservation, leaving no defined `HarnessTaskDocumentationContent` route.
3. High: `HarnessTaskMigrationReviewPacket.packet_id` had no deterministic value or derivation from explicit inputs.
4. High: Generic human-decision dispositions had no exact compatibility table with `HarnessTaskMigrationDisposition`, and the exact packet/decision relationship was underspecified.
5. High: Proposed schema, fixtures, manifest ownership, resource identities, and relationship to `WireRecordKind` and `HarnessWireRecord` were incomplete.
6. High: `HarnessTaskGraphValidator` required completed prerequisites for active or completed Tasks despite the absence of a closed lifecycle vocabulary or explicit lifecycle-policy input.
7. Medium: Compatibility incorrectly referred to five remaining Markdown records before migration; the selected population is six Markdown records plus the existing JSON pilot.

## Confirmed observations

- Six Git blobs, SHA-256 identities, and byte counts agree at the source revision.
- All 118 span hashes recompute successfully.
- Coverage is ordered, contiguous, nonoverlapping, and complete for 20,074 bytes.
- Six proposed documentation destinations agree across the draft records.
- The maintained proposal contains 19 proposed interfaces and 20 Mermaid diagrams.
- Runtime request/preparer separation and explicit renderer inputs are present.
- No implementation, migration, selection state, source-authority replacement, human acceptance, or scientific claim was introduced.

## Review boundary

This failed result is retained unchanged. One bounded correction pass may disposition the findings and deterministically verify corrections. No repeated independent review is required or authorized by the active Task. Human acceptance remains pending.
