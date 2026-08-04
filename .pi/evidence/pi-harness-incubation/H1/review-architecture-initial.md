# H1 architecture review 1 of 4

**Verdict: FAIL**

The proposal has sound exclusions, explicit-root resolution, extension-only overlays, and mechanically unique capability-matrix markings. However, several contract inconsistencies block acceptance.

## Findings

1. **BLOCKER — Ownership paths cannot represent the proposed consumers.**
   `OwnershipManifestView.writers[].owned_paths` uses `ResourcePath` (`.pi/evidence/pi-harness-incubation/H1/field-and-wire-contract.md:179-186`), but `ResourcePath` represents regular files and rejects trailing slashes/directories (`path-and-resource-resolution-contract.md:5-27`). The successor plan assigns directory scopes such as `harness/pi/schemas/`, `harness/local/profiles/`, and fixture/test roots (`h3-h2-ownership-plan.json:54-82,160-181`).
   **Correction:** Define a distinct immutable ownership-scope type with explicit file-versus-directory-prefix semantics, confinement, canonicalization, and overlap rules, or require manifests to enumerate exact files. This is a protected public-contract choice for `H1-HC01`.

2. **BLOCKER — Policy identifiers leave actions unable to operate without hidden lookup.**
   `ProjectProfile` stores only `policy_reference_ids`, `filename_policy_id`, and `local_extension_ids` (`field-and-wire-contract.md:126-136`). Nevertheless, `AuditEvidenceIdentifiers` must apply filename and protected/migration policy, while accepting only source bytes and the profile (`contract-surface.md:78`). `ValidateResourceManifest` and `ValidateSkillResources` similarly claim policy/version compatibility checks without receiving resolved policy contents (`contract-surface.md:74,80`). The profile does not contain the demonstrated protected-scope/range/filename rules, and the actions prohibit discovery.
   **Correction:** Pass validated policy DataObjects or explicit policy bytes to each action, or place the complete required immutable policy data in `ProjectProfile`. Define who loads and validates policy resources. Identifiers alone are insufficient.

3. **HIGH — Serialization and operation-result ownership violate the DataObject/ActionObject model.**
   All records declare public JSON behavior (`field-and-wire-contract.md:24-50`), and H2 must prove Python/wire agreement (`migration-and-compatibility-plan.md:89-98`), but the exact public API contains no serializer/deserializer ActionObject except profile loading (`contract-surface.md:40-52,72`). Implementing codecs privately or on DataObjects would conflict with the authoritative rule that serialization belongs to a named ActionObject (`.pi/skills/design-data-action-objects/references/data-action-architecture.md:25-31`).
   In addition, loading, resolution, chain evaluation, and evidence audit return unnamed nested tuples (`contract-surface.md:72-78`), despite the architecture requiring explicit DataObject or ResultObject operation outputs (`data-action-architecture.md:13-21`).
   **Correction:** Establish explicit serializer/deserializer ownership and concrete immutable results such as profile-load, resource-resolution, chain-evaluation, and evidence-audit results. Human approval is required because this changes the exact public surface.

4. **HIGH — Generic ownership validation consumes undefined project-local agent bytes.**
   `ValidateOwnershipManifest` accepts raw `agent_records` bytes and reports malformed agent declarations, while the same row says agent format is selected by a local adapter and the generic view excludes agent frontmatter (`contract-surface.md:75`; `field-and-wire-contract.md:186-189`). This makes generic Python responsible for parsing an unspecified local format or requires hidden adapter behavior.
   **Correction:** Have the local adapter produce a narrowly defined immutable normalized agent view before generic validation, or move agent-format validation entirely local. Do not pass raw project-format bytes to the generic action.

5. **HIGH — Minor-version compatibility is specified but not representable.**
   `Version` is a single positive integer and `public_contract_version` is described as a major (`field-and-wire-contract.md:12,122`). Yet compatibility rules rely on “supported newer minor,” open/closed code sets, and schema minors (`version-boundaries.md:44,48`), while negotiation performs exact-major matching (`version-boundaries.md:60-66`). No minor value or supported-minor declaration exists.
   **Correction:** Either define a concrete major/minor representation and negotiation rules or make version 1 closed and require a new integer schema/contract version for registry or enum expansion.

6. **MEDIUM — The capability matrix mislabels existing scientific ownership as local harness Python.**
   The row for all scientific/CPN/QE/Wannier/operator semantics places its sole PRIMARY in the “Local Python” column while describing the owner as “existing domain source” (`contract-surface.md:101,117`). Those semantics span existing domain source, specifications, tests, and documentation and must not appear owned by future H4 local harness Python.
   **Correction:** Add an “existing project-domain source” column or mark the capability explicitly outside the harness ownership matrix.

## Confirmed strengths

- Every included interface has a named demonstrated consumer in `interface-decision-matrix.json`.
- The table has exactly one textual `PRIMARY` marking per accepted capability row.
- Explicit roots and the prohibition on CWD, Git-root, `.pi`, package-resource, and ambient fallback discovery are clear.
- Extension-only overlays prevent generic/local shadow replacement.
- Generic-to-local dependency prohibition is explicit.
- Workflow engines, dispatch frameworks, Git/subprocess mutation, Graphify, scientific interfaces, and a third evidence ownership kind are correctly excluded.
- H3 → H2 → H4 remains proposed, sequential, separately activated, and non-production.

## Files inspected

- `AGENTS.md`
- `README.md`
- `.pi/skills/design-data-action-objects/SKILL.md`
- `.pi/skills/design-data-action-objects/references/data-action-architecture.md`
- `.pi/tasks/operator-record-refactor.md`
- `docs/harness/ksdft2effmass.harness.02.md`
- All ten current files under `.pi/evidence/pi-harness-incubation/H1/`
- H0 accepted proposal/context:
  - `.pi/evidence/pi-harness-incubation/H0/proposed-H1-contract.md`
  - `.pi/evidence/pi-harness-incubation/H0/open-finding-resolutions.md`
  - `.pi/evidence/pi-harness-incubation/H0/source-of-truth-map.json`
  - the four final H0 specialty review files

## Residual risks

- H1 remains proposal evidence only; no schemas, fixtures, serializers, package, or tests exist.
- Exact corrections alter public API, wire semantics, architecture boundaries, or compatibility and therefore require human decision at `H1-HC01`.
- Current validators and skills must remain authoritative until accepted H4 parity and cutover.
- This review did not assess the future evidence/VVUQ, integration, or checksum review artifacts.
