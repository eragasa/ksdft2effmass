# Implementation and readiness

## Present implementation state

The Si-VC scientific CPN is **not implemented**. No supported constructor,
initial marking, domain-token codec, hierarchy binding, runtime adapter, retained
run, or execution evidence exists for the campaign.

Three foundations exist but must not be conflated with Si-VC completion:

1. `ksdft2effmass.petrinet.colored` provides immutable generic definitions,
   markings, validation, enablement, selection, and pure firing.
2. The execution-free bulk-silicon Option-A descriptor compiles ten logical
   candidates into nine reused SCF-to-diagnostic-NSCF branches followed by
   collection and analysis. Its synthetic CPN has 38 places and 20 transitions.
   It performs no calculator execution and is not the Si-VC topology.
3. `projectkoios-simulations` owns the authoritative single-SCF SNAKES net at
   `projectkoios.simulations.workflows.pw_dft_scf.cpn.net`. It has twelve typed
   places and eight transitions and is consumed through its existing facade.

Generic Workflow also contains an engine-neutral colored-Petri-net package, but
its current definition is flat, its values are closed generic scalars, and it
has no hierarchical substitution or domain-payload binding. Its current runtime
Slice A retains effect-free local history and pure transition processing; it
does not implement protected dispatch, attempts, leases, or reconciliation.
The selected Si-VC consumer requirements are explicit in the [runtime-neutral
CPN and hierarchical binding profile](workflow-binding.md) and are aligned to
merged owner contract `projectkoios.workflow.cpn-bindings@0.1.0`, exact SHA-256
`e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`.
The retained [cross-repository exact-digest review](reviews/SI-VC-WORKFLOW-BINDING-001.md)
reported `NO_BLOCKING_FINDINGS` for its former bounded design-consistency scope. The
later decision to qualify cutoff/k-point settings before structural convergence changes
the scientific dependency graph and invalidates the reviewed 56/55 topology as an
implementation candidate. The contract and replacement topology remain unimplemented,
and neither the historical review nor operator selection grants implementation,
dependency, migration, or execution authority.

## Selected ownership boundary

The architecture decision fixes this boundary:

- `ksdft2effmass` owns the material campaign topology, scientific tokens,
  thresholds, schemas, dispositions, retained results, and claim-to-evidence
  projection;
- `projectkoios-simulations` owns reusable calculator-neutral child workflow
  contracts and outward QE/Wannier90 providers; and
- `projectkoios-workflow` owns generic net/runtime identities, transition
  occurrences, attempts, authority verification, dispatch, retries,
  reconciliation, persistence, and replay.

The superseded provider draft's proposed
`projectkoios.simulations.workflows.si_vc` semantic owner was rejected because
it would have transferred material-campaign policy into the simulation-provider
repository. The ownership decision assigns scientific ownership to
`ksdft2effmass`; the operator reserved the eventual authoritative path
`python/src/ksdft2effmass/campaigns/si_vc/cpn/net.py`. No current topology at that path
is implemented or authoritative.

Current simulations policy permits `snakes` imports only under
`pw_dft_scf.cpn`. Si-VC must not be hidden beneath that subtree or create a
second simulations-side SNAKES owner merely to bypass the rule. The selected
architecture uses Generic Workflow's runtime-neutral canonical CPN/binding
contract, keeps the scientific definition in `ksdft2effmass`, and retains SNAKES
behind reviewed child/runtime adapters. The concrete Generic Workflow API is not
yet available and must not be invented in the campaign package.

## Behavior-preserving migration order

This integration is not a greenfield workflow rewrite. It migrates execution
ownership to Generic Workflow without moving domain workflow definitions into
that repository. In the long-term model, domain repositories author and own flat
CPN definitions, payload-color bindings and codecs, child exports/bindings,
mappings, initial-marking constructors, and runtime requests. Generic Workflow
provides the consumer-facing authoring/compilation boundary, validates and links
immutable execution plans, and executes their instances without importing a
domain package or copying its topology.

Existing `ksdft2effmass` runtime/control code is compatibility evidence and a
behavior-preserving bridge during the transfer of execution responsibility; it
is not the permanent generic executor and does not cease to be the source of
its domain definitions. The migration must fit existing workflow and CPN
behavior through explicit bridges and parity evidence:

1. preserve `ksdft2effmass.petrinet.colored` definition, marking, enablement,
   ordering, selection, and firing semantics while binding them into the exact
   Generic Workflow execution profile;
2. compile the existing flat definitions in `workflows/_dft_scf_bands.py` and
   `workflows/_dft_scf_nscf_dos.py` into execution plans rather than rewriting
   their topology;
3. bridge existing `workflows.model` and `workflows.cpn_adapter` domain APIs at
   the owner boundary;
4. translate the existing `workflows.runs` aggregate identities and records for
   attempts, nested membership/intents, terminal observations, authority, and
   replay, and the existing `workflows.control` preparation, claim, dispatch,
   result-ingress, and reconciliation records;
5. adapt existing persistence through translation and dual verification before
   any replacement or retirement;
6. replace raw or string result payloads only at the boundary with exact
   six-field references and payload-color bindings;
7. add the Si-VC 56-place/55-transition flat parent through its authoritative
   campaign constructor while referencing, never copying, the simulations-owned
   12-place/eight-transition SCF child export; and
8. retire duplicate project-owned runtime behavior only after golden parity
   fixtures, replay equivalence, independent review, and separate authorization.

The implementation sequence is therefore bridge plus golden parity first,
then payload binding, the nested child route, and runtime-segment integration;
retirement is last. A migration must fail closed rather than silently change an
existing workflow's topology, selected binding, marking, authority, persistence,
or replay behavior. The detailed source-to-target mapping, semantic-witness
fixtures, dual-verification protocol, gates, and stop conditions are specified in
the [Generic Workflow migration crosswalk](../../../architecture/v2/ksdft2effmass/workflows/generic-workflow-migration-crosswalk.md).

## Read-only provider preflight

The simulations-side preflight was performed against
`projectkoios-simulations` commit
`33b7170fffb289f4e7205c63b7789a4f9468a74b`. The latest synchronized
architecture report was observed at SHA-256
`728862e4a68fb0cac85109c1e1abe84a54e45ca1a923b0c08fe6a7a88a152fb3`.
That digest binds the observed report bytes only; the report is not a retained
repository artifact and does not establish acceptance or chronology. Its 56
place rows and 55 transition rows were independently counted, were unique, and
matched the inventories in [CPN schematics](schematics.md). The later scientific
ordering decision supersedes that topology, so this digest now authenticates only a
historical design candidate. The earlier digests
`c3429ee81b21b0bbeeef0e8edd3c34f031d0c749e903c5420954c32935437c54`,
`2b472588a459f283eb9659094e036b33cfa83ffd68fca10501295d78d9226523`,
`f049415a408197e538c23ff7a4e417ec09644be702581b94923878eb2fc56078`,
and `4f92d3b0a9331580bb8ef1287f99e2dc17df0ea732f651a2ee1d23018867de1`
are superseded; the last bound the obsolete 43-place/47-transition inventory.

The earlier standard-table PseudoDojo comparator was found at
`/Users/eugene/opt/pseudodojo/1.0/pbe/nc-sr-04-standard/Si/Si.upf`, 225602 bytes,
SHA-256
`39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`.
This observation does not satisfy the later accepted v0.5 PBE
scalar-relativistic stringent UPF2 requirement; that exact artifact remains
unacquired and unverified. The observed executable candidates were:

| Role | Candidate SHA-256 | Bytes | Observed linkage |
|---|---|---:|---|
| `pw.x` | `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` | 9673048 | Apple Accelerate |
| `pw2wannier90.x` | `61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c` | 8379632 | Apple Accelerate |
| QE-bundled `wannier90.x` | `91d0f7e522b0c36dbf72d6c3ae82d20f551316ce9d624cbc4618d0d1551928f1` | 988680 | Apple Accelerate |
| standalone `wannier90.x` | `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd` | 891048 | OpenBLAS |

These are byte and linkage observations, not a frozen compatible toolchain. The
QE-bundled Wannier90 is the first compatibility-test candidate because it shares
the QE build tree and observed Accelerate linkage. This recommendation is not
scientific acceptance. The earlier OpenBLAS divide-by-zero warning remains
classified but observably unresolved.

## Provider candidate/export proposal status

The merged simulations provider design has exact SHA-256
`adfa47ba9007e3b08b02d219bf5d7b29de28a48531876c79559a510fc5484858`.
It preserves the authoritative 12-place/eight-transition topology, separates
stable topology from the two-token initial marking, defines exact candidate
bounds and child-export correlation, selects a version-pinned closed-AST export
route, and defines post-terminal QE saved-state companion evidence with truthful
bounded cancellation. The exact owner/consumer/provider design review found no
blocking compatibility inconsistency within its former scope. The provider child design
remains reusable, but the changed Si-VC child order requires a replacement consumer
binding and renewed review.

Nested implementation remains blocked by the immutable path-free artifact-set
and success-projection contracts, actual canonical control-record and exporter
implementations, generated profile/plan/export/golden bytes, runtime segments,
and independently verified fixtures. The consumer response and Si-VC-owned
schemas are in [SCF saved-state lineage](scf-saved-state-lineage.md).

## Missing CPN/runtime contracts

The superseded 56/55 inventory demonstrated explicit external-event places and a
unique-finalization structure, but it is not an implementation target. Implementation
review now needs:

- a complete replacement topology with reviewed places, transitions, typed boundary
  routes, active-latch arcs, guards, and token expressions;
- hierarchical composition of the ProjectKoios bulk-qualification child, including
  structure-scoped setting evidence, stable-pair feedback outcomes, and the accepted
  \((S_*,Q_*)\) handoff before the five-occurrence Wannier child;
- Workflow cancellation, delivery reconciliation, and quiescence evidence for
  the declared finalization invariant;
- separately authorized implementation conforming to the selected and
  technically reviewed [canonical CPN, content-addressed JSON, and hierarchical
  binding profile](workflow-binding.md);
- neutral hierarchical substitution for the authoritative SCF child without
  copied child topology;
- domain-record-to-generic-token binding, canonical JSON references, strict
  codecs, and artifact resolution without machine paths in canonical state;
- an SCF saved-state handoff and pre-dispatch staging receipt proving that the
  accepted SCF outputs are the exact inputs copied for the correlated NSCF
  attempt;
- occurrence-correlated action/event/result adapters;
- attempt-bound authority verification and single-use dispatch admission;
- bounded retry and indeterminate-effect reconciliation semantics; and
- replay/conformance tests covering directed and concurrent branch behavior.

The stable campaign-family identifier is
`projectkoios.campaigns.si-vc.pbe-pseudodojo-oncv.qe-wannier90.v1`. It is a
domain identity, not a substitute runtime occurrence scheme. Si-VC must not
invent `si-vc-occurrence-<digest>` identities.

## Missing provider capabilities

Production readiness additionally requires:

- general-mesh, multi-observable cutoff/mesh convergence and bounded interaction
  records;
- zero-pressure qualification and complete executable/build/environment
  provenance;
- authenticated transitive SCF→NSCF→converter→Wannier parent/restart lineage,
  beginning with a Workflow-correlated SCF saved-state handoff and verified
  SCF→NSCF staging receipt;
- maintained `wannier90.x -pp` and main/localization actionizers;
- branch-aware closed manifests for `.win`, `.nnkp`, `.amn`, `.mmn`, `.eig`,
  profile-declared UNKs when required, `U`, conditionally required `U_dis`, HR,
  `.wout`, logs, executions, checkpoints, any explicitly requested native
  center output, and external artifacts, plus authenticated center/spread
  observations parsed from `.wout`;
- explicit provider-frame qualification for QEXSD, UPF, k/G ordering, bands,
  spin/SOC branch, units, and indices;
- represented \(H^W\), \(T^W\), and \(R^W\) reconstruction and independent
  verification records; and
- direct-QE path, extrema, valley, and effective-mass execution and
  qualification records.

The corrected NSCF boundary is narrow: failed, timed-out, start, output, and
termination failures cannot reach handoff creation because the calculator action
raises. After zero-return success, however, an exact save-tree inventory does
not prove that QEXSD matches the requested NSCF semantics. Wannier preprocessing
must remain disabled until an authenticated semantic qualification record is
accepted.

## Retained evidence requirements

Compact repository evidence must include:

- frozen scientific, numerical, and evaluation specifications;
- exact pseudopotential, source, dependency, executable, and environment
  identities;
- closed input/output manifests and parent/child correlations;
- compact logs, centers, spreads, convergence summaries, and operator/tail
  tables;
- exact CPN definition and initial-marking identities;
- ordered firings, bindings, guards, successor markings, terminal marking, and
  replay/conformance evidence;
- Workflow run, occurrence, request, plan, effect-intent, authority, attempt,
  execution-evidence, and reconciliation identities as applicable;
- independent verification and regeneration records;
- rejected candidates and bounded reason codes; and
- a generated claim-to-evidence projection.

Large wavefunction, density, restart, UNK, and dense-matrix payloads remain
outside Git under complete checksummed manifests. Hashes establish byte identity,
not provenance authentication, semantic validity, or scientific acceptance.

## Blocking prerequisites

Protected Si-VC execution remains blocked until all of the following exist:

1. a complete replacement Si-VC topology that composes the ProjectKoios
   bulk-qualification child in the required cutoff/k-point→structure→confirmation
   order, preserves bounded re-relax/reconfirm feedback, and passes renewed review;
2. an implemented and tested Generic Workflow canonical CPN/binding contract and
   replacement Si-VC CPN conforming to the selected ownership, event-place, and
   terminal invariant;
3. implemented and tested bulk-qualification and SCF/Wannier child substitution,
   authority, cancellation, quiescence, and reconciliation contracts;
4. human disposition of the unresolved QE/OpenBLAS warning;
5. an accepted exact stable pair \((S_*,Q_*)\) with structure-scoped cutoff/k-point,
   structural, final-confirmation, and feedback evidence;
6. an authenticated production SCF parent and restart lineage;
7. accepted validation-domain path, valley, and effective-mass records;
8. frozen rank, bands, projections, windows, mesh sequence,
   gauge/initialization policy, optimizer-basin rule, thresholds, and validation
   sampling;
9. a frozen compatible executable/build/environment set;
10. semantic NSCF qualification before every downstream handoff; and
11. explicit authorization for each protected occurrence or precisely bounded
    execution tranche.

An architecture decision, enabled CPN binding, passing software test, file
manifest, prior result, smoke marker, or local executable does not grant
calculator authority.

## Verification plan

Implementation verification must include at least:

- definition and initial-marking validation;
- exact place, transition, color, arc, guard, and expression conformance;
- SCF-child binding without copied child topology;
- strict canonical JSON payload-reference decoding and rejection of duplicate,
  unknown, missing, oversized, noncanonical, or digest-mismatched documents;
- action/event/result correlation and rejection of stale or wrong-occurrence
  events;
- exact source-manifest verification, fresh-workspace copy, destination
  verification, and durable staging-receipt retention before NSCF dispatch;
- no candidate-selection input from locality results;
- no Wannier eligibility without accepted NSCF semantic qualification;
- exactly one terminal token and no enabled post-terminal scientific transition;
- bounded extension versus retry distinction;
- ambiguous-effect reconciliation before any redispatch;
- authority rejection before effect dispatch;
- complete replay from retained firings and evidence references; and
- tamper tests for parent, manifest, executable, policy, and event identities.

These are software checks. They do not establish convergence, material validity,
or uncertainty quantification.
