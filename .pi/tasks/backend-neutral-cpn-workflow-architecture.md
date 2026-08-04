# Backend-neutral Colored Petri Net workflow architecture correction

## Status

Architecture correction closed and human-accepted through `CPN-HC01` on 2026-08-03. The human PI accepted bounded preflight P0 as `CONDITIONAL_PASS` through `P0-HC01`, then accepted and closed P0A as `PASS`. P1 was separately activated after P0A closeout validation and is now blocked at unresolved `P1-HC01`; P2--P11 remain blocked and unauthorized. Production/scientific execution, pseudopotential selection, and QE, ABINIT, or Wannier90 calculations remain unauthorized.

## Authority and scope

This record prospectively corrects the workflow semantics in `.pi/tasks/backend-neutral-kohn-sham-qe-architecture.md` and `.pi/chains/backend-neutral-kohn-sham-qe.chain.json` without erasing their accepted scientific object, adapter, artifact, unit, gate-split, PAW, PhysKit, or execution-checkpoint decisions.

Authorized in this architecture pass:

- replace scientific-workflow DAG semantics with a project-owned stateful Colored Petri Net;
- retain acyclic static Python import direction where practical;
- record SNAKES as the selected candidate engine;
- define CPN mathematical, token, marking, guard, execution, persistence, fan-out, and provenance-join boundaries;
- record external-tool capability/request/result objects and token colors;
- add Markdown-first architecture, user-guide, dependency-catalog, computational, and research records;
- supersede A–H prospectively with bounded tasks P0–P11;
- request independent read-only architecture and integration reviews.

Excluded:

- production Python or test implementation;
- dependency or lock-file changes;
- SNAKES, MyST, cpnpy, SimPN, PhysKit, or external CPN code installation/copying;
- QE, Wannier90, MPI, scheduler, transfer, Graphviz, or container execution;
- convergence calculations;
- public implementation schemas or live marking persistence;
- launch of P0 or any later task;
- rewriting historical accepted evidence.

## Human decisions recorded

1. The scientific/computational workflow is a stateful CPN, while static Python imports retain acyclic dependency direction where practical.
2. The net is $\mathcal N=(P,T,A,\Sigma,C,G,E,I)$; a marking assigns a multiset of colored tokens to each place and is not a Boolean completion set.
3. SNAKES is the selected candidate engine. It may be rejected only by material technical, packaging, Python-version, or legal failure found by P0.
4. Scientific payloads, token schemas, marking validation, and persistence remain project-owned and do not inherit from or publicly expose SNAKES runtime classes.
5. External tools are represented by stable identity, specification, capability, installation, verification, immutable request/result, and structured failure objects. No plugin framework is approved.
6. Guards are pure. Every external operation uses a durable two-phase request/result protocol outside guard evaluation.
7. Durable tokens contain IDs and immutable payloads, never subprocess/scheduler/open-file handles, credentials, closures, mutable library instances, or SNAKES objects.
8. Logical project subnets cover preflight, provenance, DFT specification, QE I/O/execution, convergence, bulk validation, direct-TB, Wannier NSCF/bridge/execution, comparison, and scientific validation. No unverified SNAKES hierarchical-net API is assumed.
9. The accepted neutral `PeriodicElectronicStructureDataset` parent fans out to direct spectral/TB and Wannier paths. Their join requires common parent provenance and compatible specifications/representation metadata; two completion tokens are insufficient.
10. G01a, G01b, G02, and later gates are accepted marking predicates over typed evidence. G02 still depends on G01a. Stage 03's uniform-grid NSCF child retains the accepted G02 SCF parent manifest.
11. Durable marking persistence records schema/model IDs, multisets of typed token payloads, provenance, lineage, correlations, and retry/failure history. Live-net pickle, arbitrary-object pickle, lambda serialization, and Graphviz-as-authority are prohibited.
12. SNAKES Graphviz output is an optional derived view only.
13. New narrative documentation is Markdown-first. MyST is currently absent; its dependency/configuration compatibility is a bounded P0 documentation-tooling preflight and is not added now. Existing RST is not mass-converted.
14. `cpnpy` and SimPN are comparative references only. The supplied cpnpy example is retained unchanged and explicitly unverified. The exact UTF-8 fenced-block SHA-256 is `7e0b25a26bf648c5e1dc4cd96e1a4f2762195702312eac4ed489b3d825e90031`, with the human architecture-correction instruction dated 2026-08-03 as its source.
15. PhysKit remains ideas/contractual reimplementation only, with no runtime dependency, copied code, or shared package.

## Prospective token colors

```text
ToolDeclaredToken
ToolVerifiedToken
ToolCapabilityToken
ExecutionAuthorizationToken
ExecutionRequestToken
ExecutionAcceptedToken
ExecutionResultToken
ExecutionFailureToken
ArtifactAvailableToken
ManifestVerifiedToken
ScientificValidationToken
RetryAuthorizationToken
```

Scientific result and specification tokens use project-owned payloads such as `PeriodicElectronicStructureDataset`, `SCFConvergenceResult`, `RunManifest`, and artifact identities.

Prospective future-backend concepts are `BackendIdentityToken`, `BackendCapabilityToken`, `BackendQualificationToken`, `BackendExecutionRequestToken`, `BackendExecutionResultToken`, `NeutralPeriodicDatasetToken`, `UnsupportedCapabilityToken`, and `BackendDisagreementToken`. They are not implemented by this correction and do not insert ABINIT into the concrete QE production subnet. Future qualification is scoped by schema versions, backend/executable and adapter versions, method profile, pseudopotential lineage, and numerical-verification protocol; it is never only a Boolean.

## Supersession map from A–H

The A–H records remain historical prospective decomposition and are marked superseded for workflow sequencing:

| Previous | Preserved content | Prospective successor |
|---|---|---|
| A | language-neutral scientific and wire contract | P1, P4 |
| B | provenance and artifact identity/location | P2, P3 |
| C | neutral periodic electronic-structure DataObjects/ResultObjects | P4 |
| D | QE mechanical input/output | P5 |
| E | separate input mapper/result adapter | P6 |
| F | immutable execution and SCF result boundary | P2, P5, P6 |
| G | direct spectral TB fan-out | P7 |
| H | Wannier specification and QE bridge | P8, P9 |

No accepted scientific decision in A–H is removed. Their linear/DAG-like supervisory sequence is superseded by the CPN-oriented P0–P11 task program.

## Bounded task program

| ID | Objective | Prerequisites | State |
|---|---|---|---|
| P0 | SNAKES Python/packaging/license/capability and MyST documentation-tooling preflight | human acceptance and explicit launch | Closed; human-accepted `CONDITIONAL_PASS` |
| P0A | bounded SNAKES/MyST packaging, license notice, and documentation configuration | accepted P0 and explicit human authorization | Closed; human-accepted `PASS` |
| P1 | project-owned CPN token/place/transition/marking contract | accepted P0A | Active; blocked at unresolved `P1-HC01` |
| P2 | provenance and external-tool capability records | accepted P1 | Blocked |
| P3 | SNAKES net construction and project-owned marking persistence | accepted P1, P2 | Blocked |
| P4 | neutral periodic electronic-structure structures, specifications, and datasets | accepted P1, P2 | Blocked |
| P5 | QE mechanical I/O and immutable execution boundary | accepted P2, P4 | Blocked |
| P6 | QE semantic adapter and SCF-validation subnet | accepted P3, P4, P5 | Blocked |
| P7 | direct spectral/TB fan-out subnet | accepted P3, P4, P6 | Blocked |
| P8 | Wannier specification and QE-to-Wannier90 bridge | accepted P3, P4, P5, P6 | Blocked |
| P9 | Wannier90 execution and result-adaptation subnet | accepted P2, P3, P8 | Blocked |
| P10 | synthetic composed workflow verification | accepted P6, P7, P8, P9 and required metrics | Blocked |
| P11 | human-authorized bulk-Si computational campaign | accepted G01a marking, human-accepted P10, and accepted production checkpoint | Blocked |

Each task independently requires implementation, tests, documentation, read-only review, parent verification, and human acceptance. P11 additionally requires the existing production-environment and pseudopotential authorization checkpoint. Acceptance never automatically launches a successor.

## Bounded post-review domain correction

The approved integration domain is periodic KS/GKS electronic structure for crystalline solids producing Bloch-band representations suitable for band analysis, TB reduction, and Wannierization. Its operator structure is

$$
\hat H\cong\int_{\mathrm{BZ}}^\oplus\hat H(\mathbf k)\,\mathrm d\mathbf k.
$$

Molecular-orbital and finite-system calculations are outside scope. This is not universal DFT integration, coverage of all Kohn–Sham or PAW implementations, or authorization for ORCA or another molecular package.

Prospective active names are `PeriodicElectronicStructureSpecification`, `PeriodicElectronicStructureDataset`, `PeriodicBandStructure`, and `PeriodicElectronicStructureArtifactSet`. Independent axes cover system domain, boundary conditions, Bloch-fiber organization, KS/GKS method, norm-conserving/ultrasoft/PAW core treatment, numerical representation, and available products. PAW is a formalism/capability; no generic `PAWCalculator` is authorized.

The directional neutral-specification -> capability -> concrete mapper/serializer -> immutable request and concrete parser -> semantic adapter -> neutral-dataset boundaries remain consistent with the pure-guard, two-phase execution contract. QE remains the initial production backend. Hybrid GKS profiles and a narrow ABINIT conformance adapter are deferred until after the first accepted end-to-end dopant result and do not enter P0–P11. The exact domain, hybrid plan, PAW representations, paired tutorial corpus, pseudopotential matching levels, future-backend tokens, and staging are authoritative in `docs/architecture/periodic-electronic-structure-integration.md`.

## Documentation ownership

- `docs/user-guide/`: installation, operation, dependencies, and troubleshooting;
- `docs/architecture/`: CPN, static import direction, scientific object, adapter, persistence, and ownership decisions;
- `docs/computational/`: places/markings, calculation protocols, stages, and acceptance evidence;
- `docs/research/`: scientific relationships, claims, limitations, and epistemic boundaries;
- `docs/papers/`: static claim prerequisites, not workflow runtime state.

## Validation gates for this correction

- chain JSON and P0–P11 prerequisite validation;
- static prospective import-direction cycle audit, explicitly separate from workflow semantics;
- CPN place/transition/token/guard/request-result contract scan;
- SNAKES selected-but-not-added scan;
- no implementation/test/dependency/lock changes;
- no external execution or generated Sphinx output;
- checkpoint validation;
- Markdown link/navigation and supplied cpnpy block integrity checks;
- Sphinx warnings-as-errors for currently supported sources;
- stale DAG-as-workflow terminology scan;
- computational/research/paper synchronization review;
- `git diff --check`;
- five independent read-only review lanes and final parent verification.

## Deterministic review corrections

- CPN-001: Initial wording called accepted, rejected, failed, and blocked states globally terminal, conflicting with retries and prerequisite recovery. Correction: outcome scope is explicit; failed attempts remain terminal history, retries create new attempt identities, blocked branches are recoverable unless explicitly finalized, and accepted/rejected terminality applies to the declared attempt/branch/gate/workflow scope.
- CPN-002: P11 eligibility used ambiguous “as applicable” wording. Correction: accepted G01a marking, human-accepted P10, and the accepted production checkpoint are all mandatory.
- CPN-003: Research note `ksdft2Effmass.05.md` incorrectly made the Wannier Hamiltonian the common parent of both TB routes. Correction: the accepted neutral Kohn–Sham dataset/manifest is the common parent; direct spectral TB begins from G02, while the operator-mediated route consumes its validated G03 Wannier child.
- CPN-004: G04 comparison did not encode the provenance-compatible join. Correction: join eligibility now requires the same accepted Kohn–Sham parent/manifest, compatible specification/workflow versions, representation/energy metadata, verified artifact lineage, and accepted branch states.
- CPN-005: The supplied cpnpy block lacked durable source attestation. Correction: record the human instruction date and exact UTF-8 block SHA-256 while preserving the explicitly unverified status.
- CPN-006: Sphinx source navigation copied only the Markdown user-guide index. Correction: register all nine then-current Markdown user-guide sources as Sphinx download/navigation entries while MyST remains unapproved.
- CPN-007: The duplicated historical research-plan body lacked the workflow disclaimer, and directly touched research indexes contained stale links/limited mojibake. Correction: add the disclaimer to the preserved duplicate and repair only the directly reviewed index/hierarchy strings and targets; no broad historical rewrite was performed.
- CPN-008: Seven computational leaf records already modified by the backend-neutral control-plane correction retained “downstream dependency graph” wording. Correction: identify their outputs as required by the downstream static prerequisite projection and CPN transition contracts. Untouched historical leaf wording remains interpreted by the Stage-00 static-projection disclaimer and is not rewritten mechanically.
- CPN-009: Final integration review found one remaining research paragraph naming the validated Wannier Hamiltonian as both routes' common parent and one abbreviated P11 prerequisite row. Correction: synchronize `ksdft2Effmass.03.md` to the accepted neutral Kohn–Sham dataset/source manifest common-parent rule and state all three mandatory P11 prerequisites explicitly in the Stage-00 registry.
- CPN-010: Human-requested post-review correction bounded the neutral domain to periodic KS/GKS Bloch-band electronic structure, corrected active prospective object/place/transition names, separated method/core-treatment/representation/backend/product axes, recorded PAW representation semantics, deferred hybrid GKS and ABINIT conformance plans, defined paired tutorial VVUQ and pseudopotential-matching policies, preserved the QE production subnet and P0–P11 sequence, and returned to unresolved `CPN-HC01` without launching implementation.
- CPN-011: Focused post-correction reviews found deterministic synchronization issues only. Correction: distinguish wavefunction representation from product role/availability, synchronize remaining active `PeriodicElectronicStructureDataset` names and Wannier artifact criteria, classify tutorial Layer 2 as software verification with integration evidence, make pending acceptance and prospective staging explicit, complete the declared runtime/development/notebook/documentation/build toolchain catalog, and refresh the current 13-page Markdown attestation. The pre-existing untracked conference fan-out note remains preserved and explicitly nonauthoritative under the original architecture record; it is outside the corrected active-contract terminology sweep.

## Read-only reviews and parent verification

After deterministic correction loops:

1. CPN semantics, markings, guards, retries, recovery, and external execution: **PASS** (`e7778064`).
2. Neutral DFT, QE, direct-TB, Wannier90 ownership and fan-out: **PASS** (`ee8c4cab`, child 1).
3. SNAKES packaging assumptions and cpnpy/SimPN comparative treatment: **PASS** (`ee8c4cab`, child 2).
4. Markdown-first documentation, user guide, task inventory, and research/computational synchronization: **PASS** (`ee8c4cab`, child 3).
5. Final integration and control-plane consistency after CPN-009: **PASS** (`1fe47192`).

Focused post-review correction reviews:

1. Periodic KS/GKS domain, PAW semantics, and molecular exclusion: **PASS** after CPN-011 (`7696cb48`, child 1).
2. QE–ABINIT tutorial conformance, pseudopotential matching, and VVUQ classification: **PASS** (`3f20087f`, child 2).
3. Staging, deferred status, documentation synchronization, and active-chain preservation: **PASS** after CPN-011 (`7696cb48`, child 2).
4. Final CPN integration consistency: **PASS** (`3f20087f`, child 4).

Parent verification after CPN-011 passed chain JSON parsing, P0–P11 cycle/prerequisite assertions, static import-direction feasibility, checkpoint validation, supplied-block hashing, 13-page Markdown user-guide inventory/navigation checks, dependency-catalog/source/test/generated-output scans, Sphinx warnings-as-errors to a temporary output directory, stale terminology and common-parent scans, and `git diff --check`.

These reviews establish architecture/control-plane consistency only. They do not establish SNAKES compatibility, production software behavior, numerical convergence, scientific validation, uncertainty quantification, or Rust conformance.

## Final human acceptance and closeout

The human PI selected Option A at `CPN-HC01` on 2026-08-03 and accepted:

- the stateful CPN workflow semantics;
- the periodic KS/GKS electronic-structure domain;
- PAW and pseudopotential formalisms as independent capabilities;
- QE as the initial production backend;
- deferred ABINIT VVUQ conformance infrastructure;
- deferred hybrid GKS and broader backend integration;
- Markdown-first documentation;
- the post-dopant launch condition for deferred generalization.

This architecture task is closed and human-accepted. The accepted public result is the prospective architecture and control-plane contract documented by the authoritative files listed in `CPN-HC01`. No production software, calculation, convergence result, scientific-validation result, or UQ result was produced.

## Remaining future decisions

- P0 was human-accepted as `CONDITIONAL_PASS` through resolved `P0-HC01` on 2026-08-03 and is closed.
- Bounded P0A packaging/configuration is human-accepted as `PASS` and closed.
- P1 was separately activated after P0A closeout validation and is blocked at unresolved `P1-HC01`; P2--P11 and production/scientific execution remain blocked and unauthorized.
- Pseudopotential selection remains a later human scientific decision.
- A later production checkpoint remains mandatory before any real QE, ABINIT, or Wannier90 execution.

No checkpoint remains unresolved for this architecture task. Closed P0 owns its retained technical and bounded license/packaging evidence without reopening the accepted architecture absent material failure. Scientific validation, uncertainty quantification, and Rust conformance remain not performed.
