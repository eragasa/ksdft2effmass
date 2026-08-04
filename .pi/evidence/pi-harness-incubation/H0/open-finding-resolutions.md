# H0 retained-finding resolutions

These are recommendations for `H0-HC01`, not implemented decisions. “Human judgment required” means the recommendation affects H1's protected contract, ownership, or schedule and therefore requires checkpoint acceptance.

## 1. Artifact versus boundary ownership

**Current evidence.** The accepted grammar uses class-owned and artifact-owned integration. P1's Python-runtime/JSON-wire module is locally recorded as `boundary_owned`, but its filename names both sides and all four tests use `test_artifact__...`. The prospective harness page introduces boundary-owned as a peer type and a new `boundary` function surface.

**Alternatives.** (a) make boundary a third primary kind and test surface; (b) collapse every boundary into undifferentiated artifact ownership; (c) retain two generic primary kinds while representing a boundary as artifact relation metadata.

**Recommendation.** Select (c). Use generic `class_owned` and `artifact_owned`; require artifact relation metadata to distinguish intrinsic artifacts, symmetric agreements, and directional mappings. A public Workflow class remains class-owned; a technical workflow/subnet boundary is artifact-owned. Preserve P1's `boundary_owned` value through a local compatibility mapping and do not rename its tests.

**Consequences.** H1 needs relation-side identities and directionality but no new test-function surface. Exact filenames and allowed surfaces remain task/profile policy.

**Human judgment required:** yes.

## 2. Evidence-skill overlap

**Current evidence.** `document-research-python` already owns the accepted reusable grammar; `develop-operator-records` adds domain constraints by reference; the AST auditor and P1 validators enforce bounded structure; the accepted skill audit found no new AI-skill gap.

**Alternatives.** New independent `write-research-evidence-tests`; extraction of `document-research-python`; composition of several full skills; one authoritative grammar plus routing and local/domain extensions; defer all resource work.

**Recommendation.** One authoritative grammar plus composition. H1 should identify the existing `document-research-python` evidence grammar as the source capability. H3 may package a generic resource derived from it, with a local profile and operator/CPN extensions, but must not create a competing grammar or silently retire the current skill.

**Consequences.** Deterministic validators consume the same profile; semantic review remains separate; H4 proves routing parity before cutover.

**Human judgment required:** yes.

## 3. Generic versus local validator decomposition

**Current evidence.** Ownership v2 contains reusable role/path/acyclicity logic but binds `.pi` paths and agent frontmatter. Checkpoint validation contains reusable schema/set checks but fixed discovery and a synthetic resolver. Evidence auditing contains reusable AST/range logic but hard-coded roots, prefixes and markers. P1/evidence-migration validators contain historical inventories and node maps.

**Alternatives.** Extract scripts wholesale; leave every validator local; extract stateless primitives and provide explicit local profiles/adapters.

**Recommendation.** Extract only stateless primitives and structured results. Generic actions accept records, schemas, explicit roots and immutable profiles. Local configuration owns roots, marker/prefix vocabularies, filename policies, agent format, task/checkpoint identities, migration states and v1 compatibility. Historical validators remain intact for shadow replay.

**Consequences.** H1 must specify stable issue codes/order, malformed-input versus internal-failure behavior, path confinement, explicit roots, and version boundaries. Passing remains software-structural evidence only.

**Human judgment required:** yes.

## 4. H2 and H3 scheduling

**Current evidence.** The chain models H2 and H3 as siblings after H1 and conditionally permits concurrency. The architecture index renders H2 before H3. Root policy requires writers to run sequentially in a shared worktree. H2 will consume profile/resource schemas and identities that H3 is planned to own; H2's optional local adapters overlap H4.

**Alternatives.** Concurrent siblings after disjoint manifests; H2 then H3; H3 then H2.

**Recommendation.** H3 then H2 sequentially. H3 first creates the accepted textual schemas, resource manifest and local profile identities; H2 then implements against those identities. Defer project-local Python adapters to H4 unless H1 assigns exact nonoverlapping H2 files. Do not use concurrency without a later explicit exception to root policy.

**Consequences.** H1 must revise the authoritative schedule/ownership plan after acceptance; current blocked chain remains unchanged while the checkpoint is pending.

**Human judgment required:** yes.

## 5. Harness agent and path ownership

**Current evidence.** `.agents/skills` is shared repository discovery; `.pi/skills` is pi-specific and explicitly loaded by current agents; global pi skills are fallbacks and may be shadowed; prospective `harness/pi` has no current dispatch semantics. Existing writer/reviewer roles are operator/CPN-centered and own no future harness paths. H0 is non-production and explicitly parent-operated, so production ownership preflight is not applicable to its evidence-only writes.

**Alternatives.** Widen existing agents; rely on ambient/global skill discovery; create harness-specific roles and version-2 manifests; treat `harness/pi` as automatically dispatchable.

**Recommendation.** Create harness-specific H2/H3 writer and reviewer records only after H1 acceptance. Version-2 manifests own exact paths. `harness/pi` and `harness/local` are manifest-addressed resource roots, not assumed discovery roots. Global resources are considered only through explicit fallback policy. Keep `.pi/agents` and instantiated state local.

**Consequences.** H1 must specify resource descriptor, overlay, precedence and selected-content identity. H2/H3 cannot launch until their manifests and completion validators pass.

**Human judgment required:** yes.

## 6. Project-specific leakage

**Current evidence.** The complete readable-candidate leakage audit reports 527 reviewed lexical occurrences across all 38 generic/split candidate files: 95 `ksdft2effmass`, 237 `.pi/`, 12 `python/src/`, 43 `docs/`, 16 `P0`, 55 `P1`, 3 `P2`, 61 `backend-neutral-cpn`, 2 `QuantumEspresso`, and one each `Wannier90`, `SNAKES`, and repository-root discovery. Exact `SV-CPN` content is concentrated in components already classified local rather than generic candidates.

**Alternatives.** Copy and later clean; parameterize every string; identify semantic generic invariants and keep all project values in local records/profiles.

**Recommendation.** Use semantic split, not blind replacement. Keep universal integrity invariants in generic code. Supply project roots, IDs, markers, evidence namespaces, domain extensions, Git policy, and compatibility data through explicit local profiles or runtime records. Prohibit generic-to-local imports, implicit `.pi`, current-working-directory discovery and repository-relative defaults.

**Consequences.** H1 needs a versioned, data-only project profile and negative leakage/path tests. Lexical scans remain screening evidence and require semantic review.

**Human judgment required:** yes.

## Additional H0 findings

- Current task and chain records lack common schemas and a reusable consistency validator.
- Checkpoint identity uniqueness is not fully enforced when duplicate files choose different normalized decisions.
- Checkpoint skill/result requirements exceed the current checkpoint schema.
- Complete skill identity is not validated because references/scripts/assets are not hashed as one resource closure.
- Repository-wide strict evidence-ID validation is intentionally blocked by 22 known protected operator-test gaps; H1 must support profile-scoped migrated/protected/warning states rather than weaken the audit.
- Maintained status prose is already stale relative to the authoritative H0 chain.
- The P1 version-1 ownership manifest intentionally preserves obsolete artifact-module names and is compatibility input, not current path authority.
