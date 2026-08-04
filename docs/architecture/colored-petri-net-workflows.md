# Colored Petri Net workflow architecture

## Status

The human PI granted final acceptance to the corrected project-owned Colored Petri Net (CPN) architecture through `CPN-HC01` on 2026-08-03. SNAKES is the selected candidate Python execution engine, subject to bounded compatibility, packaging, and license preflight. This document records architecture only. It does not add SNAKES, implement workflow code, execute an external tool, or authorize a calculation.

Static Python imports and scientific workflow semantics are different structures:

```text
Static Python import structure:
    acyclic dependency direction where practical

Scientific and computational workflow:
    stateful Colored Petri Net
```

A static dependency projection may help plan tasks or inspect imports, but it is not the authoritative scientific workflow state.

## Mathematical model

The project workflow net is

$$
\mathcal N
=
(P,T,A,\Sigma,C,G,E,I),
$$

where:

- $P$ is the set of places;
- $T$ is the set of transitions;
- $A$ is the set of directed arcs;
- $\Sigma$ is the collection of token color sets;
- $C$ assigns an admissible color set to each place;
- $G$ assigns guards to transitions;
- $E$ assigns arc expressions;
- $I$ defines the initial marking.

A marking $M$ assigns a **multiset** of colored tokens to every place. Multiple independently identified tokens may occupy one place. The marking is not reduced to Boolean task-completion flags.

A transition is enabled only when:

1. its input places contain tokens satisfying the input arc expressions;
2. the resulting token bindings satisfy the transition guard;
3. every required authorization, provenance, capability, or validation token is present.

Firing consumes and produces the multisets prescribed by the arc expressions. Project policy may additionally require durable request/result correlation, parent-manifest compatibility, and immutable token payloads.

## Required workflow semantics

The project CPN contract must represent:

- colored typed tokens;
- multiple tokens at a place;
- pure guarded transitions;
- independent branch execution;
- synchronization joins;
- retries with explicit authorization;
- failure and recovery paths;
- repeated convergence iterations;
- durable markings;
- explicit provenance and parent-child run relationships;
- explicit accepted, rejected, failed, and blocked outcome states with defined scope.

Outcome scope is explicit. A failed **attempt** is terminal and retained durably, while an authorized retry creates a new attempt identity in the same broader workflow. A blocked branch or request is normally recoverable when missing prerequisite/authorization tokens arrive; it becomes a terminal blocked outcome only through an explicit finalization/cancellation transition. Accepted or rejected outcomes are terminal only for the declared attempt, branch, gate, or workflow scope. No terminal token is erased by retry or recovery.

An execution result token is not automatically an accepted scientific token. Process completion, parser acceptance, SCF convergence, numerical-protocol acceptance, scientific validation, and uncertainty quantification remain distinct token colors or explicitly represented states.

## Project-owned scientific payloads

SNAKES does not own the scientific domain model. Project-owned immutable payloads include:

```text
CrystalStructure
KPointSet
PeriodicElectronicStructureSpecification
PeriodicBandStructure
PeriodicElectronicStructureArtifactSet
PeriodicElectronicStructureDataset
SCFConvergenceResult
PseudopotentialSpecification
PseudopotentialArtifact
ArtifactReference
ArtifactLocation
RunManifest
```

These objects do not inherit from SNAKES classes. Neutral periodic electronic-structure and provenance APIs do not expose SNAKES `Place`, `Transition`, `PetriNet`, marking, expression, or token implementation classes. Accepted P0 established bounded engine feasibility; a future SNAKES adapter may carry immutable project DataObjects only after the separate P1 project contract is implemented and human-accepted.

## Prospective package ownership

```text
workflows/
└── cpn/
    ├── tokens.py
    ├── markings.py
    ├── validation.py
    ├── persistence.py
    ├── model.py
    └── engines/
        └── snakes.py
```

The spelling may be refined during P1, but ownership direction is fixed:

```text
neutral periodic electronic-structure/provenance objects
    do not import workflows.cpn or SNAKES

project CPN contract
    imports neutral token payload types only where justified

SNAKES adapter
    imports SNAKES and the project CPN contract

QE/Wannier adapters
    consume immutable execution requests
    produce immutable execution results
```

No multi-engine framework is authorized. The project contract exists so scientific tokens and durable markings are not inseparable from SNAKES runtime objects, not to support arbitrary engines.

## External-tool lifecycle model

Narrow project-owned objects will represent common external-tool lifecycle properties:

```text
ExternalToolIdentity
ExternalToolSpecification
ExternalToolCapability
ExternalToolInstallationRecord
ExternalToolVerificationResult
ExternalExecutionRequest
ExternalExecutionResult
ExternalExecutionFailure
```

Exact names may be refined, but responsibilities remain:

- stable tool identity and implementation family;
- requested and verified capability;
- observed version and executable/package identity;
- executable hash when available;
- installation/environment record;
- verification evidence;
- immutable request and correlated result;
- structured failure.

This common lifecycle seam is not a plugin framework. QE- and Wannier-specific scientific semantics, file formats, and adapters remain concrete.

### External-tool token colors

Prospective colors include:

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

A durable tool token may contain tool identity, implementation family, observed version, executable/package identifier, executable hash, supported capability, installation/environment record ID, verification-result ID, and provenance ID.

Durable tokens must not contain subprocess handles, scheduler clients, open files, arbitrary mutable library instances, unserializable closures, credentials, or SNAKES implementation objects.

## Pure guards and two-phase external execution

Transition guards inspect immutable token fields only. A guard must not invoke an executable, dynamically import or probe a package, contact a scheduler, access an uncontrolled deployment path, read or write files, transfer artifacts, mutate manifests or environments, or perform DFT, Wannierization, or tight-binding calculations.

Every external operation uses a durable request/result protocol. QE SCF is representative:

```text
qe_input_ready
    -> request_qe_execution
    -> qe_execution_requested

external QE adapter outside guard evaluation:
    consumes an authorized immutable request
    returns a correlated immutable result or failure

qe_execution_requested + qe_execution_result_received
    -> record_qe_success
    -> qe_execution_completed

qe_execution_requested + qe_execution_failure_received
    -> record_qe_failure
    -> qe_execution_failed

qe_execution_failed + retry_authorized
    -> request_qe_retry
```

The same boundary applies to Quantum ESPRESSO, Wannier90, MPI/scheduler submission, artifact transfer, and optional Graphviz rendering. `ExecutionAcceptedToken` means a request was durably accepted by the execution boundary; it does not mean the scientific output passed.

## Logical subnet ownership

The first project net may be one CPN assembled from project-level compositional boundaries:

- dependency and environment preflight;
- provenance and artifact verification;
- periodic KS/GKS electronic-structure specification;
- Quantum ESPRESSO input preparation;
- Quantum ESPRESSO execution;
- SCF convergence;
- bulk-silicon validation;
- direct spectral/tight-binding fan-out;
- Wannier-compatible NSCF preparation;
- QE-to-Wannier90 bridge;
- Wannier90 execution;
- Wannier-derived tight-binding construction;
- operator and spectral comparison;
- scientific validation.

These are logical subnets, not a claim that SNAKES supplies a verified hierarchical-net API. P0 verified only the bounded features in its retained capability matrix. Any additional engine feature requires separately authorized evidence before the design depends on it.

## Periodic electronic-structure fan-out and provenance join

Representative places include:

```text
periodic_electronic_structure_specification_ready
qe_scf_requested
qe_scf_completed
scf_result_parsed
scf_result_verified
periodic_electronic_structure_dataset_accepted
direct_tb_request_ready
wannier_nscf_request_ready
wannier_bridge_ready
wannier90_request_ready
wannier_dataset_accepted
tb_result_accepted
comparison_ready
```

Representative transitions include:

```text
verify_qe_capability
authorize_scf
construct_qe_input
request_qe_scf
record_qe_scf_result
parse_qe_scf_result
adapt_qe_result_to_periodic_dataset
validate_scf_parent
fan_out_accepted_periodic_dataset
construct_direct_tb_request
construct_wannier_nscf_request
request_wannier_nscf
construct_qe_wannier_bridge
verify_wannier90_capability
request_wannier90
record_wannier90_result
construct_wannier_tb_result
join_common_parent_results
```

The accepted neutral parent feeds both branches:

```text
accepted PeriodicElectronicStructureDataset
├── direct spectral/TB reconstruction
└── Wannier specification and Wannier90 reconstruction
```

The fan-out consumes or references the same accepted parent token according to explicit arc expressions; it does not fabricate two unrelated parents.

`join_common_parent_results` is enabled only when bindings establish:

- the same accepted periodic electronic-structure parent identity and parent manifest;
- compatible physical, numerical, pseudopotential, and workflow schema versions;
- required representation metadata and energy conventions;
- verified artifact and manifest lineage;
- the validation state required by the comparison being requested.

Two completed result tokens alone never enable comparison.

## Deferred future-backend token semantics

The concrete QE production subnet is preserved. The following token concepts are prospective extension seams only:

```text
BackendIdentityToken
BackendCapabilityToken
BackendQualificationToken
BackendExecutionRequestToken
BackendExecutionResultToken
NeutralPeriodicDatasetToken
UnsupportedCapabilityToken
BackendDisagreementToken
```

A future backend-qualification token must be scoped by neutral specification- and dataset-schema versions, backend identity and executable version, adapter version, method profile, pseudopotential lineage, and numerical-verification protocol. A Boolean such as `qualified=True` is insufficient.

A deferred paired QE–ABINIT qualification subnet may derive both backend requests independently from one neutral parent, adapt both results to neutral periodic datasets, and record unsupported capabilities or disagreements. It is not inserted into the prospective QE production path, and a production QE run does not require an ABINIT duplicate. ABINIT remains deferred until after the first accepted end-to-end dopant result. See [`periodic-electronic-structure-integration.md`](periodic-electronic-structure-integration.md).

## Skill-capability testing boundary

Repository skills are instruction/capability bundles applied by an external agent or harness; they are never guards or transitions. Prospective skill invocation uses immutable capability and request tokens, external execution outside guard evaluation, correlated result/failure tokens, and a later validation/recording transition. Deterministic tools retain authoritative command pass/fail, agent reviews produce findings, parent verification checks evidence completeness, and human acceptance remains separate.

The audited inventory, block mapping, capability-token responsibilities, deterministic tool owners, and prospective testing subnet are recorded in [`cpn-skill-capability-audit.md`](cpn-skill-capability-audit.md) and `.pi/skills/skill-capability-inventory.json`. No skill invocation runtime or SNAKES subnet is implemented.

## Gates as accepted markings

Computational gates are predicates over typed evidence in durable markings, not graph-node completion:

```text
G01a:
    computational foundation and reproducibility capabilities accepted

G01b:
    composed synthetic scientific workflows accepted

G02:
    accepted bulk-Si SCF parent and bulk-validation evidence
```

G02 requires the accepted G01a marking. Meeting notes or unmanifested historical calculations cannot supply the required tokens. The Wannier-compatible uniform-grid NSCF remains a Stage 03 child carrying the accepted G02 SCF parent manifest identity.

Later gates likewise require their declared accepted evidence tokens. A failed or blocked branch may coexist in the marking with successful independent branches without being mistaken for gate acceptance.

## Durable marking persistence

Durable workflow state is project-owned. The future persistence contract must record:

- workflow schema version;
- net/model identifier;
- marking;
- token type identifier and payload;
- provenance identifiers;
- parent-child relationships;
- request/result correlation;
- retry and failure history where required.

The following are not approved:

- pickling a live SNAKES net;
- pickling arbitrary Python objects;
- serializing guards as lambdas;
- storing credentials or deployment clients;
- treating Graphviz output as authoritative state.

Persistence implementation is deferred to P3 after P0 and P1 acceptance.

## Visualization

P0 loaded the SNAKES 0.9.33 `gv` plugin and constructed DOT, but system `dot` was unavailable and Python 3.14 exposed deprecated `codecs.open` use in the render path. Graphviz therefore remains optional and conditionally usable only after a bounded compatibility correction and environment-specific executable preflight. Any future diagrams should distinguish places, transitions, guarded transitions, external execution boundaries, retry/failure paths, QE flow, direct-TB flow, Wannier90 flow, provenance joins, and accepted scientific markings.

A rendered diagram is never the authoritative net, marking, manifest, or acceptance record.

## Engine and comparative references

SNAKES remains the selected candidate engine. P0 exercised version 0.9.33 on CPython 3.14.6 and found the required construction, colored-token, multiset, pure-guard, binding, inscription, firing, retry/history, provenance-join, neutral-extraction, and bounded-reachability semantics feasible. The human PI accepted the result as `CONDITIONAL_PASS` through `P0-HC01` and authorized only bounded P0A packaging/configuration. For project governance the explicit upstream grant is recorded as `LGPL-2.1-or-later`, while the observed distributed license file contains LGPLv3 text; this is not a general legal conclusion. Graphviz remains optional, derived, and nonauthoritative. No engine-selection reopening is recommended from the runtime evidence.

`cpnpy` and SimPN are comparative references only. Their APIs and licenses are not accepted dependencies. Accepted P0 evidence found no material failure requiring engine reconsideration; any future comparison or engine-selection reopening requires separate authorization and new evidence.

## P1 implementation status

The authorized P1 implementation now provides the executable backend-neutral
contract under `python/src/ksdft2effmass/workflows/cpn/`, version-1 schemas and
synthetic fixtures under `specification/workflow-cpn/v1/`, and focused
software-verification evidence. It implements immutable routing tokens,
complete multiset markings, closed declarative guards and inscriptions,
deterministic enablement and read/consume/output firing, explicit scoped
outcomes, retry/recovery/iteration representation, and structured errors.

This implementation and its deterministic correction pass are complete. The
retained initial independent reviews recorded FAIL findings; corrected evidence
is pending independent re-review, parent verification, and human final
acceptance. This status does not close or accept P1. SNAKES adaptation,
authoritative persistence, concrete workflows, provenance/tool objects,
scientific payloads, external execution, and P2--P11 remain blocked.

## VVUQ boundary

Architecture review and synthetic CPN tests are software-verification evidence. They do not establish correctness of a QE calculation, numerical convergence, scientific validation, uncertainty quantification, or Rust conformance. The accepted operator-record foundation remains completed and independent of this workflow implementation.
