# HarnessTask final contract clarification

Decision checkpoint: `.pi/checkpoints/harness.simplification.docs-json.task-model-contract.revised-final-acceptance.json`

Normalized decision: Option B

Correction class: Contract text only

Mappings changed: no

HarnessTask fields changed: no; 16 retained

Proposed interfaces changed: no; 19 retained

Independent review repeated: no

## Clarified decisions

Graph result: `HarnessTaskGraphValidator` returns existing project-local `LocalValidationResult` and `LocalIssue` values rather than generic `ValidationResult`. Exact `PIHL.TASK.*` codes and precedence are deferred to Stage 2 implementation hardening.

Projection profile: `template_bytes` is the one authoritative template representation. `HarnessTaskProjectionProfile` owns only schema version, profile identifier, exact nonempty template bytes, matching template identity, and final-LF policy. Documentation-mapping coverage and Task/content/profile compatibility belong to `HarnessTaskDocumentationRenderer` and `HarnessTaskMigrationReviewPacketPreparer`. Exact parsing and validation cases are deferred to Stage 2.

Comparator claim: `HarnessTaskDocumentationComparator` reports exact byte differences, mapping coverage, and documentation-block preservation. Mechanically mapped differences do not establish semantic correctness or human acceptance. Exact comparison algorithms and hardening tests are deferred to Stage 2.

Path contract: `ResourcePath` uses the already accepted harness path contract unchanged. This proposal adds no duplicate path grammar. Exhaustive schema fixtures and rejection tests are deferred to Stage 2.

Legacy limitation: The version-1 generated-page drift is accepted as a separate legacy limitation and does not block Stage 1. The generated page and expected fixture remain unchanged in this correction.

## Preserved boundaries

The six source identities, 20,074 bytes, 118 mappings, six `002.002.000` through `002.002.005` documentation destinations, 16 `HarnessTask` fields, schema version 2, 19-interface count, 20 diagrams, packet and decision ownership, retained failed independent review, seven prior corrected review findings, source authority, Stage-2 block, and automatic-successor prohibition remain unchanged.

No interface, schema, fixture, source, test, migrated Task JSON, destination documentation file, dependency, or lockfile is implemented or modified.
