# H0 harness inventory and ownership-classification report

## Result before human checkpoint

H0 technical inventory is complete and structurally valid. This is not human acceptance. H0 remains active and will block at `H0-HC01`; H1 is not activated.

## Environment and revision

- Repository: `ksdft2effmass`
- Branch: `dev`
- Commit-derived H0 baseline: `d0b253158eac2c57748923f6484a794721e5c97f`
- Python: 3.14.6
- PI model/provider: `gpt-5.6-sol` / `openai-codex`
- Initial worktree: clean

## Inventory totals

- Components: **316**, each naming one unique present file or one absent prospective root
- Capability-matrix rows: **12**
- Dependency edges: **76**
- Split/extraction candidates with consumer records: **38**
- Reviewed leakage occurrences: **527** across **38** candidate files

### Extraction classification

| Classification | Count |
| --- | ---: |
| `EXTRACTABLE` | 0 |
| `SPLIT_GENERIC_AND_LOCAL` | 38 |
| `KEEP_PROJECT_LOCAL` | 264 |
| `RETIRE_AS_DUPLICATE` | 0 |
| `DEFER` | 14 |

No component is safe for wholesale extraction or immediate retirement. Every reusable candidate currently contains a local/path/dispatch coupling or needs a protected H1 decision. This is a conservative result, not a claim that no generic behavior exists.

### Current authority

| Authority | Count |
| --- | ---: |
| `AUTHORITATIVE` | 150 |
| `DERIVED` | 1 |
| `ADVISORY` | 20 |
| `HISTORICAL_EVIDENCE` | 141 |
| `DUPLICATE` | 0 |
| `UNRESOLVED` | 4 |

The four unresolved components are the four documented but absent generic/local implementation/resource roots.

## Capability-matrix summary

The matrix accounts for each component exactly once. Its 12 capabilities cover policy and authority, maintained harness architecture, skill dispatch, agent roles, checkpoint control, instantiated task/chain/checkpoint state, ownership preflight, evidence/skill validation, VVUQ conventions, documentation collection, historical replay, and prospective interfaces.

The most mature generic nucleus is task-ownership v2: path confinement, nonoverlapping writers, independent reviewers, acyclic prerequisites, and completion-stage binding. It is still classified `SPLIT_GENERIC_AND_LOCAL` because the current schema/validator embeds `.pi` paths, agent frontmatter, default-chain routing and local profile semantics.

## Recommended ownership boundary

### Generic procedure

Future generic Python should own only immutable records/results and stateless actions for:

- artifact/resource identities and manifests;
- explicit project profiles;
- structured validation issues/results;
- ownership, checkpoint-set, chain-view, evidence-ID, checksum and skill-resource validation;
- explicit-root resource resolution and path confinement.

Future generic textual resources should own one versioned grammar/descriptor for each accepted generic skill or schema.

### Project-local policy

Project-local resources and adapters own:

- `.pi` layout and instantiated state;
- agent format and identities;
- Git branch/remote durability policy;
- evidence prefixes, pytest markers, filename rules and migration states;
- P1 version-1 compatibility;
- operator/CPN/SNAKES/QE/Wannier semantics;
- scientific acceptance, task identities and activation rules.

Generic code must not import local code, discover `.pi`, infer a Git/repository root, or depend on current-working-directory paths.

## Source-of-truth recommendation

- `.pi/`: task scope/status, chain dependency/activation, checkpoint decisions, evidence and runtime state.
- `docs/harness/`: maintained explanation only.
- `harness/pi/`: future generic resources, only after acceptance.
- `harness/local/`: future local profiles/extensions, only after acceptance.
- generic Python incubation path: structural records/actions/results.
- local Python incubation path: project adapters only.
- existing project-domain source: scientific/operator/CPN semantics and tests.
- historical evidence: immutable prior scripts, manifests, reports, reviews and mappings.

Every inventory component is assigned exactly once to one future authoritative capability owner in `source-of-truth-map.json`; the validator checks complete coverage and uniqueness.

## Six retained findings

1. **Artifact versus boundary:** retain generic primary kinds `class_owned` and `artifact_owned`; model agreement/direction as artifact relation metadata. Preserve local P1 `boundary_owned` compatibility and existing `artifact` test surfaces.
2. **Evidence-skill overlap:** extract/update the existing `document-research-python` grammar capability; do not create an independent duplicate skill.
3. **Validator decomposition:** extract stateless structural primitives and structured results; keep paths, prefixes, markers, agent format, inventories and historical compatibility local.
4. **H2/H3 scheduling:** run **H3 then H2 sequentially**, because H3 owns resource/profile identities consumed by H2 and root policy requires shared-worktree writers to be sequential.
5. **Agent/path ownership:** create harness-specific future roles and version-2 manifests; do not widen operator/CPN roles or assume `harness/pi` is an automatic discovery path.
6. **Leakage:** use explicit data-only profiles and caller-supplied roots. The audit approved zero generic-to-local edges.

All six are protected H1-scope/ownership recommendations requiring human acceptance at `H0-HC01`.

## Proposed H1 contract

The proposed minimum surface is limited to demonstrated records and validators:

- `ArtifactIdentity`, `ResourceReference`, `ResourceManifest`, `ProjectProfile`, and `SkillDescriptor`;
- `ValidationIssue` and `ValidationResult`;
- narrow ownership, checkpoint, task/chain-view, checksum, command-result and decision-boundary records;
- stateless loaders/resolvers/validators with explicit roots and profiles.

It explicitly excludes orchestration, dispatch, subprocess/Git/package operations, scientific CPNs, domain adapters, package publication, Graphify, universal filename rules, a new evidence grammar, and any scientific-validation/UQ interface.

## Deferred items and migration risks

- Public API names, serialized fields and compatibility policy remain H1 human decisions.
- Package/distribution/import/CLI identity remains H5.
- Graphify remains an optional externally managed integration outside minimum H1.
- The checkpoint skill requires durability/replay fields absent from the current schema.
- Tasks/chains lack common schemas and a reusable consistency validator.
- Complete skill resource identity is not validated beyond each `SKILL.md` hash.
- Strict evidence-ID validation remains blocked by 22 known protected operator tests; H0 does not change them.
- P1 version-1 ownership metadata intentionally retains obsolete artifact names and must be treated as local compatibility input.
- Live status prose is already stale in maintained documentation; task/chain/checkpoint state remains authoritative.
- Historical evidence and legacy validators must remain until H4 shadow parity and explicit cutover.

## Review results

Four independent final reviews passed after two retained deterministic correction rounds. They inspected the structured inventory, matrix, dependency/source maps, leakage audit, finding resolutions, H1 proposal and validation results. Their retained records are:

- `review-inventory-completeness.md`;
- `review-architecture-classification.md`;
- `review-evidence-vvuq.md`;
- `review-integration-control-plane.md`.

Initial and correction findings remain in corresponding `*-initial.md` and
`*-correction-1.md` records; they were not overwritten or concealed.

## Validation summary

Passed structural inventory schema, classification cardinality, component accounting, capability completeness, source-owner uniqueness, dependency consistency, leakage reproduction, chain/task/P2 assertions, checkpoint dry runs, skill capability validation, ownership-validator tests, P1 ownership/evidence replay, Sphinx warnings-as-errors, the 341-entry H0 checksum catalog, Ruff lint, protected-path nonmutation and `git diff --check`. Four closed task checksum catalogs still pass. The closed initialization catalog is preserved unchanged and reports exactly two expected current-tree drifts for the authorized H0 task/chain status transition; `historical-checksum-replay.json` records that boundary.

The non-strict evidence-ID audit passed with 22 known warnings. Strict mode returned 1 as expected and is not reported as a pass. This retained limitation is not an H0 defect and is not silently waived.

## Scope confirmation

H0 created only bounded evidence and control-plane records. It created no harness Python/resource implementation, moved or retired no skill/validator, changed no test semantics/node IDs/dependencies/lockfiles/source/specification/fixtures/docs, began no H1/P2 work, and executed no scientific software. Concurrent unrelated meeting/paper/conference paths that appeared after the clean H0 start are preserved and explicitly inventoried in `concurrent-unrelated-worktree.json`. Their hashes are provenance snapshots rather than a freeze on active user edits. H0 rejects any unlisted path and rejects staging any listed concurrent path. Numerical verification was not applicable because no harness numerical algorithm was discovered. Scientific validation and uncertainty quantification were not applicable.
