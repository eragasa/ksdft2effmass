# HarnessTask migration review: `example.task`

## Review target

- Review ID: `harness-task-migration.example.task`
- Subject: HarnessTask migration candidate example.task from records/example-source.md to docs/example.md
- Evidence class: `software_verification`
- Source revision: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- Contract references:
  - `.pi/evidence/docs-json/task-model-contract/harness-task-contract.md`
  - `.pi/tasks/harness.simplification.docs-json.task-document-migration.json`
  - `.pi/evidence/task-control/task-document-human-mediation-decision.md`

## Source provenance and rollback identity

- Path: `records/example-source.md`
- Revision: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- Git object: `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`
- Byte count: `24`
- SHA-256: `3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`
- Rollback identity: `sha256:3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`

## Original Markdown

```markdown
Synthetic introduction.
```

## Candidate canonical HarnessTask JSON

Identity: `sha256:8f32622c2700ede897290ec4a461e4572df59d7a963d256ba5e724ffebdd3242`

```json
{
  "schema_version": 2,
  "task_id": "example.task",
  "title": "Example Task",
  "status": "proposed",
  "status_detail": null,
  "parent_task_id": null,
  "task_prerequisite_ids": [],
  "external_prerequisite_ids": [],
  "explicit_activation_required": true,
  "objective": "Verify the accepted software contract.",
  "authority_reference_paths": [
    "records/decision.md"
  ],
  "authorized_scope": [
    "Use synthetic test data."
  ],
  "completion_criteria": [
    "Exact checks pass."
  ],
  "exclusions": [
    "No migration is authorized."
  ],
  "intake_path": "records/example.intake.md",
  "documentation_path": "docs/example.md"
}
```

## Candidate maintained Markdown

Identity: `sha256:3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`

```markdown
Synthetic introduction.
```

## Source mappings

| Mapping ID | Source bytes | Disposition | Target references | Transformation | Rationale |
|---|---:|---|---|---|---|
| "intro" | `0:24` | `DOCUMENTATION_OWNED_CONTENT` | ["docs/example.md"] | "preserve exact bytes" | "synthetic documentation content" |

## Exact comparison

- Status: `EXACT`
- Source identity: `sha256:3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`
- Rendered identity: `sha256:3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`

### Byte differences

- None

### Unmapped spans

- None

### Human-readable unified diff

```diff

```

## Opaque documentation-block preservation

- `intro`: preserved exactly; SHA-256 `3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`

## Limitations and claim boundary

- Mapped differences are mechanical coverage only and do not establish semantic correctness or human acceptance.
- Byte-structural software verification does not establish semantic migration correctness.
- The rendered review document is not operational authority or a human decision.
- No packet or document authenticates human identity or authorizes migration or activation.

## Human choices

Choose exactly one:

1. Accept this file migration.
2. Revise the contract or mappings.
3. Retain Markdown ownership.
4. Defer the file.
