# Colored-Petri-net schematics

## One eventual authoritative scientific topology

Si-VC requires one authoritative flat parent colored Petri net (CPN) with typed
runtime bindings to separately authoritative child CPN instances. No current Si-VC
net is authoritative: the earlier 56-place/55-transition draft is superseded by the
cutoff/k-point→structure→final-confirmation ordering decision. A stage list,
imperative sequencer, provider runner, workflow-name inventory, or copied child
topology must not become a competing topology. The eventual reviewed parent CPN will
own the campaign's scientific places, transitions, arcs, guards, and token expressions.

Cross-repository ownership is:

```text
ksdft2effmass
  owns Si-VC scientific campaign topology and policy
       |
       | typed child-workflow requirements and retained outcomes
       v
projectkoios-simulations
  owns reusable calculator-neutral SCF/NSCF/relaxation capability composition
  and outward QE/Wannier90 provider adapters
       |
       | transition requests, effect intents, evidence references
       v
projectkoios-workflow
  owns run, transition occurrence, attempt, authority, dispatch,
  retry, reconciliation, persistence, replay, and runtime identities
```

The former corrected provider draft called the net `si_vc_component_locality` and
contained 56 unique places and 55 unique transitions. Independent recounting matched
those totals, but the draft put zero-pressure relaxation before numerical setting
qualification and cannot represent the required re-relax/reconfirm feedback. The
former 43-place/47-transition inventory and this later 56/55 draft are both
superseded. Neither may be implemented.

### Superseded 56-place inventory

The names are retained only so the historical design and digest remain inspectable:

| Group | Places | Count |
|---|---|---:|
| Campaign/control | `workflow_start`, `campaign_active`, `campaign_request`, `preflight_action`, `preflight_observed`, `scientific_decision_required`, `scientific_decision_received`, `campaign_frozen`, `confirmatory_policy_required`, `confirmatory_policy_received`, `finalization_action`, `finalization_observed`, `terminal_outcome` | 13 |
| Protected-child boundary | `protected_child_required`, `execution_authority_admitted`, `protected_child_action`, `protected_child_succeeded`, `protected_child_failed` | 5 |
| Zero pressure | `zero_pressure_action`, `zero_pressure_observed`, `zero_pressure_assessed` | 3 |
| SCF and convergence | `scf_child_required`, `scf_child_outcome`, `scf_observations`, `scf_convergence_action`, `scf_convergence_observed`, `scf_convergence_assessed`, `production_scf_parent` | 7 |
| Subspace decision | `subspace_decision_required`, `subspace_decision_received` | 2 |
| NSCF semantics | `nscf_qualification_action`, `nscf_qualification_observed`, `nscf_qualified` | 3 |
| Wannier interface/localization | `wannier_interface_ready`, `wannier_localization_ready` | 2 |
| Provider frame | `frame_qualification_action`, `frame_qualification_observed`, `frame_qualified` | 3 |
| Operator reconstruction | `operator_reconstruction_action`, `operator_reconstruction_observed`, `operator_reconstructed` | 3 |
| Operator verification | `operator_verification_action`, `operator_verification_observed`, `operator_verified` | 3 |
| Candidate assessment | `candidate_assessment_action`, `candidate_assessment_observed`, `candidate_assessed` | 3 |
| Guard assessment | `guard_assessment_action`, `guard_assessment_observed`, `guards_assessed` | 3 |
| Direct-QE qualification | `direct_qe_qualification_action`, `direct_qe_qualification_observed`, `direct_qe_qualified` | 3 |
| Locality assessment | `locality_assessment_action`, `locality_assessment_observed`, `locality_assessed` | 3 |
| **Total** |  | **56** |

### Prospective transition inventory

The 55 transition names are:

```text
start_preflight
accept_preflight
accept_scientific_decisions
block_unready_campaign
require_zero_pressure_relaxation
admit_protected_child
route_relaxation_success
accept_protected_child_failure
assess_zero_pressure
accept_zero_pressure
reject_zero_pressure
execute_scf_child
accept_convergence_scf_child
reject_scf_child
request_scf_convergence_assessment
accept_scf_convergence_assessment
extend_scf_convergence
finalize_scf_convergence_exhaustion
accept_scf_convergence
accept_production_scf_child
request_subspace_decision
accept_subspace_decision
route_nscf_success
qualify_nscf_semantics
reject_nscf_semantics
require_wannier_preprocess
route_wannier_preprocess_success
route_pw2wannier90_success
route_wannier_localization_success
qualify_provider_frame
reject_provider_frame
request_operator_reconstruction
accept_operator_reconstruction
reject_operator_reconstruction
request_operator_verification
accept_operator_verification
reject_operator_verification
request_subspace_candidate_assessment
accept_subspace_candidate_assessment
extend_subspace_candidates
finalize_candidate_exhaustion
request_numerical_and_gauge_guards
request_guard_assessment
accept_guard_assessment
extend_guards
finalize_guard_inconclusive
route_direct_qe_success
qualify_direct_qe_validation
reject_direct_qe_validation
request_confirmatory_policy
accept_confirmatory_policy
start_confirmatory_locality_analysis
accept_locality_assessment
reject_locality_assessment
accept_campaign_finalization
```

These names and counts are not fixed requirements for the replacement topology.
Generic Workflow owns the selected runtime-neutral CPN/binding contract and runtime
mechanics; `ksdft2effmass` owns the eventual scientific definition at the reserved
source path `python/src/ksdft2effmass/campaigns/si_vc/cpn/net.py`. Only a newly
reviewed source definition implementing the revised order can become topology
authority.

## Scientific flow

The intended scientific dependency structure is:

```text
start
  -> execution-free preflight
  -> H1 prerequisite decisions
  -> frozen campaign
  -> joint coupled-cutoff/k-point qualification on exact seed S0
  -> provisional setting Q0@S0
  -> zero-pressure structural convergence under Q0
  -> mechanically qualified structure S1
  -> fresh joint setting confirmation Q1@S1
  -> bounded re-relax/reconfirm feedback if the selected setting changes
  -> accepted exact pair (S*,Q*)
  -> new separately authorized production SCF parent
  -> H2 subspace/construction decisions
  -> semantically qualified uniform NSCF branches
  -> Wannier preprocessing
  -> pw2wannier90 conversion
  -> Wannier localization
  -> exact provider-frame qualification
  -> represented H/T/R reconstruction
  -> independent represented-operator verification
  -> candidate assessment without locality inputs
  -> numerical and gauge guards
  -> independent direct-QE validation
  -> H3 confirmatory-analysis policy
  -> component-locality assessment
  -> exactly one terminal outcome
```

This diagram states dependency meaning only. The reviewed CPN definition, not
this rendering, is the topology authority.

## Hierarchical SCF child

Every SCF occurrence must reuse the simulations-owned authoritative constructor

`projectkoios.simulations.workflows.pw_dft_scf.cpn.net::build_dft_pw_scf_net`.

The intended substitution boundary is:

```text
parent scf_child_required
  -> reserve execute_scf_child occurrence
       -> fresh dft_pw_scf child instance
            child workflow_start/request <- exact parent requirement
            child terminal_outcome
              + separately retained QE saved-state candidate companion
              -> verified terminal delivery
              -> one execute_scf_child firing
              -> correlated parent scf_child_outcome
```

The parent must not copy the child's twelve places or these eight transitions:

- `start_workflow`;
- `accept_registration`;
- `accept_submission`;
- `accept_completion`;
- `accept_analysis`;
- `reject_analysis`;
- `accept_analysis_failure`; and
- `accept_failure`.

A `SiVcScfChildRequirement` identifies scientific role, exact request and parent
references, and campaign coordinate. A `SiVcScfChildOutcome` wraps the
Workflow-owned child occurrence and exact terminal SCF outcome. The selected
neutral hierarchical/substitution design contract exists, but its APIs,
canonical exporter, runtime segments, and conformance fixtures do not. The
selected Si-VC consumer requirements are specified in the [workflow binding
profile](workflow-binding.md). In particular, the parent token
carries a content-addressed typed JSON reference rather than a raw mapping or
machine path, and the child terminal mapping must bind the exact Workflow child
instance, occurrence, attempt, terminal outcome, and saved-state handoff. The
candidate is required companion evidence for success, not a second child CPN
token. The provider response and exact accepted-parent/staging lineage are in
[SCF saved-state lineage](scf-saved-state-lineage.md). The unchanged child has no
universal in-net cancellation transition; unresolved cancellation cannot map the
parent or satisfy quiescence.

## Action, event, and retained-result separation

Effectful and analytical work follows the same shape:

```text
scientific prerequisites
  -> request transition
  -> typed action place
  -> external actionizer or protected child
  -> typed event/evidence place
  -> acceptance or qualification transition
  -> retained record place
```

No transition manufactures both an action and evidence that the action
succeeded. External observations enter as tokens in explicit places; they are
not extra-procedural arguments injected directly into a transition.

The superseded draft demonstrated this rule for zero-pressure, SCF-convergence,
NSCF-semantic, provider-frame, reconstruction, verification, candidate, guard,
direct-QE, and locality results. The replacement topology must preserve that
separation while adding the ordered bulk-qualification child and feedback outcomes. It
must also route human scientific, subspace-construction, and confirmatory-policy
decisions through declared boundary places. A complete
token-color-to-boundary-place table must forbid direct runtime injection into
transitions.

## Human gates

```text
preflight -> [H1] -> frozen campaign
production SCF -> [H2] -> candidate executions
sealed construction and validation -> [H3] -> locality analysis
```

- **H1** freezes warning disposition, toolchain family, convergence coordinates,
  and zero-pressure acceptance policy.
- **H2** freezes rank, bands, projections, windows, meshes, gauge initialization,
  random seeds, optimizer-basin rule, and selection thresholds.
- **H3** freezes physical radii, pair masks, operator tolerances, grids,
  normalization, comparison rules, evidence roles, and dispositions.

The candidate-selection subnet has no incoming arc from locality-assessment
places. This structurally prevents selecting a candidate because its component
tails look favorable.

## Protected authority boundary

A scientifically enabled transition is not authorized execution. Each protected
occurrence requires a Workflow-issued, exact-scope admission bound to campaign,
transition occurrence, action kind, specification and parent digests, executable
scope, authority evidence, and execution tranche.

```text
protected requirement + Workflow authority admission
  -> admitted action
  -> one attempt under runtime policy
  -> reconciled terminal evidence
  -> scientific qualification transition
```

Changed cutoff, mesh, candidate, gauge initialization, validation sample, or
parent digest creates a new occurrence. A retry of unchanged work is a new
attempt of the same occurrence. Ambiguous effects enter reconciliation; they are
never automatically redispatched merely because a lease expired or a process
report was lost.

The current Generic Workflow implementation is effect-free Slice A. Protected
dispatch, attempt-bound admission, and reconciliation remain prospective runtime
contracts rather than available production services.

## SCF→NSCF provenance and semantic NSCF gate

```text
accepted SCF child outcome
  + Workflow-correlated SCF saved-state handoff
  -> verify source manifest and files
  -> copy into fresh attempt-scoped NSCF workspace
  -> verify copied destination against the same manifest
  -> retain staging receipt before NSCF dispatch
  -> zero-return NSCF + exact post-NSCF saved-tree inventory
  -> nscf_qualification_action
  -> normalized QEXSD and source-frame evidence
  -> qualify_nscf_semantics
       accepted -> nscf_qualified -> Wannier preprocessing eligible
       rejected -> candidate rejection or terminal block
```

The hard requirement is provenance that the accepted SCF outputs are the exact
inputs staged for the correlated NSCF attempt. Copying is the selected
stage-isolation mechanism, not the provenance claim by itself. The handoff,
parent manifest, destination verification, staging receipt, NSCF occurrence,
and attempt must remain correlated as specified in the [workflow binding
profile](workflow-binding.md).

A zero return and byte-authenticated save tree are necessary but not sufficient.
Qualification must check completion, requested k-point and band inventories,
structure, pseudopotential, spin/SOC branch, units, and source ordering.

## Unique terminal-state invariant

The superseded draft provided the following finalization structure, which remains a
required invariant for the replacement topology:

```text
one active/finalization token
  -> exactly one terminal transition consumes it
  -> one terminal outcome token
  -> no subsequent scientific transition enabled
  -> outstanding child occurrences cancelled or reconciled to quiescence
```

All nonfinal scientific transitions test `campaign_active`. Every transition
requesting termination consumes that sole token and emits one
`finalization_action`. Workflow must reject new admissions, cancel or finish
admitted children under policy, reconcile late and duplicate deliveries, and
emit `finalization_observed` only after quiescence. Only
`accept_campaign_finalization` can then emit `terminal_outcome`; late evidence
remains retainable but cannot enable post-terminal scientific work.

Required conformance cases include simultaneous protected-child failures,
SCF-child failure racing a scientific rejection, late success after terminal
selection, duplicate external events, and replay from every intermediate
marking.

## Topology review status

- Finding disposition — revised scientific ordering: `MUST_FIX`
- Problem — the retained 56/55 topology puts structural convergence before numerical
  setting qualification and has no stable-pair feedback loop.
- Next action — produce a complete replacement topology that composes the
  ProjectKoios bulk-qualification child before the five-occurrence Wannier child.
- Current bounded review outcome: `CHANGES_REQUIRED`
- Immediate operator request: `NONE`; the scientific ordering is now explicit.

The operator selected Generic Workflow's runtime-neutral canonical CPN/binding
contract and reserved the `ksdft2effmass` owner path. The merged owner contract
has SHA-256
`e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`.
The retained [owner/consumer/provider exact-digest review](reviews/SI-VC-WORKFLOW-BINDING-001.md)
reported `NO_BLOCKING_FINDINGS` for the former bounded design-consistency scope. The
scientific-order change invalidates that outcome for implementation. The contract,
replacement topology, and concrete APIs remain unimplemented and require separately
authorized work. This
architecture decision does not freeze H1--H3 or grant calculator, dependency,
migration, publication, or release authority.
