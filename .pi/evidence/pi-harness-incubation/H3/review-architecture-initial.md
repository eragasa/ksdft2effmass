# H3 architecture / Rust / resource-contract review

## Findings

### HIGH — Public-record schemas accept wire values that violate exact H1 DataObject invariants

The schemas often state cross-field invariants only in `description` text rather than encoding them. An independent Draft 2020-12 check showed that all of the following H1-invalid mutations are schema-valid:

- a `generic` `ResourceManifest` with non-null `extends_manifest_id` (`harness/pi/schemas/records/resource-manifest.schema.json:6,24-41`), contrary to the exact layer invariant in `.pi/evidence/pi-harness-incubation/H1/field-and-wire-contract.md` under `ResourceManifest`;
- a `ProjectProfile` with non-null `local_manifest_id` and null `local_manifest_version` (`harness/pi/schemas/records/project-profile.schema.json:6,24-42`), contrary to the required paired presence invariant;
- a `ResourceReference` whose `dependency_ids` contains its own `resource_id` (`harness/pi/schemas/records/resource-reference.schema.json:35-41`);
- a `TaskReference` whose `task_prerequisite_ids` contains its own `task_id` (`harness/pi/schemas/records/task-reference.schema.json:20-31`);
- a `ChainView` whose `explicitly_activated_task_ids` contains an ID absent from `tasks` (`harness/pi/schemas/records/chain-view.schema.json:25-39`).

These are not merely action-level filesystem or profile-policy checks: H1 declares them as exact record invariants and says malformed serialized field/invariant input is rejected. The schemas are H3's public serialized-contract artifacts, and the H3 fixture set supplies only one coarse invalid case per record, so the passing validator does not detect this underconstraint. At minimum, JSON-Schema-expressible conditions (manifest layer/base pairing and profile local-ID/version pairing) must be encoded and covered by boundary fixtures; invariants that cannot be expressed portably in Draft 2020-12 need an explicit schema/semantic-validation boundary and retained negative oracle coverage rather than description-only apparent acceptance.

### MEDIUM — The generic evidence grammar imposes a filename policy that H1 explicitly keeps local

`harness/pi/skills/document-research-python/references/test-evidence-documentation.md:122-143` declares exact class-owned and artifact-owned evidence-module filename conventions. H1 rejects “universal filename rules” (`.pi/evidence/pi-harness-incubation/H1/contract-surface.md:190`) and assigns filename interpretation to the local `ProjectProfile.filename_policy_id`/adapter. The local extension then declares the project filename policy at `harness/local/extensions/evidence-documentation.md:23-35`. Thus policy ownership is split/repeated across generic and local layers rather than the generic resource owning only reusable evidence grammar and the local extension owning filename policy. This is a generic/local dependency-boundary mismatch even though manifest dependency edges themselves point only local-to-generic.

### LOW — A generic DiagnosticPath fixture embeds the current repository's test-tree spelling

`harness/pi/fixtures/diagnostic-path/valid/directory-tree-scope.json:6` and `harness/pi/fixtures/diagnostic-path/oracle-index.json:10-12` use `python/tests/software_verification`, which is the active repository's local test-root convention. H1 requires a directory-tree spelling but does not require this project path, and H3 prohibits repository paths in the generic layer. A neutral spelling (as already used elsewhere in the canonical vectors) would test identical `DiagnosticPath` semantics without local topology leakage. The validator's leakage scan excludes generic fixtures, so its PASS cannot detect this.

## Conforming areas checked

- Exact closed set of 16 public-JSON record schemas, required field names, `schema_version = 1`, unknown-field rejection, enum closures, safe-integer bounds, and SHA-256 digest spelling align with H1.
- `ValidationIssue.path` references `DiagnosticPath | null`, while resource and ownership fields retain `ResourcePath` and `OwnershipScopePath`; valid/null/NFC and required invalid path families are present.
- Generic/local manifests have stable IDs, byte hashes, acyclic closure, extension-only identity/path behavior, and no generic-to-local manifest dependency.
- Skill entry and required-resource closure resolve; the authoritative grammar is referenced rather than copied wholesale into the skill entry.
- Canonical vectors contain all 16 public record kinds, RFC-8785-style canonical JSON plus one LF, hashes, NFC diagnostic spelling, and declared future Python/intended-Rust targets. They are suitable textual inputs for later validated Rust newtypes, but do not establish Rust implementation conformance.
- No H2 production package, Rust implementation, H4 integration, dependency/lockfile change, live-skill retirement, scientific execution, or successor activation was found in H3 scope.

## Commands

- `python .pi/task-ownership/validate_task_ownership.py --task H3 --chain .pi/chains/pi-harness-incubation.chain.json` — PASS.
- `python harness/pi/validation/validate_h3_resources.py` — PASS, 46 gates, 0 defects.
- Independent `jsonschema.Draft202012Validator` mutation probe with the repository schema store — accepted the five invalid record mutations listed above (and correctly rejected an ERROR-bearing `ValidationResult` changed to `PASS`).
- `rg` leakage scan over `harness/pi`, manifest/schema/skill/docs inspection, symlink/executable scan, and `git diff --stat`/scoped diff inspection.

## Limitations

This was read-only review of the uncommitted H3 candidate and retained H1/H3 records. No future Python or Rust codec exists to execute cross-language round trips. RFC 8785 hashes were replayed by the H3 validator, not by an independent Rust implementation. Unrelated pre-existing worktree files were not reviewed.

Review status: FAIL
