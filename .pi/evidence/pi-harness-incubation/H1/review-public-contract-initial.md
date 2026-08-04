## Review

**Verdict: FAIL**

- **Correct:** The proposal consistently remains non-production and defers implementation, schemas, fixtures, execution, and successor activation (`contract-surface.md:5-14`; `docs/harness/ksdft2effmass.harness.02.md:5-14`).
- **Correct:** Identifier grammar, file-resource confinement, symlink rejection, and extension-only overlay behavior are substantially bounded (`field-and-wire-contract.md:8-22`; `path-and-resource-resolution-contract.md:9-27,54-75,103-118`).
- **Correct:** Issue ordering and result claim boundaries are explicit (`issue-code-and-ordering-contract.md:62-117`).

- **Blocker:** `OwnershipManifestView.owned_paths` uses `ResourcePath` (`field-and-wire-contract.md:179-187`), but `ResourcePath` rejects trailing slashes and represents regular files rather than directories (`path-and-resource-resolution-contract.md:15-27`). Current accepted ownership data demonstrably uses directory scopes such as `.pi/skills/` and `python/tests/.../cpn/` (`.pi/evidence/class-owned-evidence-convention/task-ownership.json:11-14,30-32`). The proposed view therefore cannot represent a demonstrated v2 consumer or perform prefix-overlap checks exactly. A separate repository ownership-scope path type and invariants are required.

- **Blocker:** Several actions lack the policy data needed to produce their promised deterministic results. `ProjectProfile` contains policy IDs but not resource-format compatibility, skill-behavior compatibility, evidence-prefix/range grammar, protected scopes, or local issue-code registrations (`field-and-wire-contract.md:120-136`). Nevertheless:
  - `ValidateResourceManifest` must reject unsupported format versions;
  - `AuditEvidenceIdentifiers` claims the profile supplies prefixes, filename policy, and protected/warning state;
  - `ValidateSkillResources` must decide behavior/policy compatibility
  (`contract-surface.md:74,78,80`).

  These actions receive neither resolved policy-resource bytes nor a typed policy record. Their exact validity, failure, and Rust behavior is consequently unimplementable from the proposed inputs.

- **High:** Strict JSON behavior is not an exact public API. The contract says malformed serialized records return `ValidationResult` (`field-and-wire-contract.md:33-48`), but only `LoadProjectProfile` accepts serialized bytes; all other actions accept already-constructed records (`contract-surface.md:72-80`). No public encode/decode method or ActionObject is specified for the other twelve public JSON records. Canonical output also combines “declared field order,” “recursively sorted map keys,” and “without ASCII escaping where allowed” without defining how nested record objects or optional escaping are handled (`field-and-wire-contract.md:39-42`). Independent Python and Rust implementations can therefore produce different canonical bytes.

- **High:** Issue codes are registered but exact failure-code and severity decisions are incomplete. For example, checksum missing/hash failures could use either the generic path/artifact codes or the checksum-specific codes (`issue-code-and-ordering-contract.md:24-25,33`), while `ValidateChecksumManifest` does not select between them (`contract-surface.md:79`). The registry has no per-code severity column, despite stating severity is otherwise fixed (`issue-code-and-ordering-contract.md:40-52`). `LoadProjectProfile` similarly leaves “bad identity” ambiguous between artifact and profile identity codes (`contract-surface.md:72`; `issue-code-and-ordering-contract.md:25,27`).

- **High:** Version negotiation is internally incomplete. New issue codes and enum values refer to negotiated “minor” versions (`version-boundaries.md:42-49`; `issue-code-and-ordering-contract.md:12-14`), but the only public-contract field represents a single major integer (`field-and-wire-contract.md:122`). The claim that every action receives supported versions or obtains them from a profile (`version-boundaries.md:60-67`) is also false for `ValidateChecksumManifest`, which receives neither (`contract-surface.md:79`).

- **High:** Exact Rust portability is not specified despite the maintained page claiming every interface has a Rust representation (`docs/harness/ksdft2effmass.harness.02.md:55-59`). Examples include:
  - `ResourcePath`: “String/newtype,” not one exact representation (`field-and-wire-contract.md:11`);
  - `ValidationIssue.code`: “String/enum wrapper” (`field-and-wire-contract.md:270`);
  - no Rust signatures, error types, filesystem-path representation, or serialization decision for any ActionObject;
  - no explicit Rust object mappings for `ChecksumEntry`, `ChecksumManifest`, or `ValidationResult` (`field-and-wire-contract.md:248-284`).

- **High:** The no-speculative-API claim is not attested at field/signature level. `interface-decision-matrix.json` names candidate-level consumers but does not trace each mandatory field or action argument to evidence. In particular, mandatory `SkillDescriptor.result_contract_id` and `failure_contract_id` (`field-and-wire-contract.md:160-164`) freeze resources whose current inventory describes generic result schemas and runtime enforcement as prospective (`.pi/skills/skill-capability-inventory.json:16,23,137,180-183`).

- **Note:** Repository-root `plan.md` and `progress.md` were absent, so the durable H1 task, chain, evidence, and maintained documentation were reviewed directly.
- **Note:** No files were edited or staged.
