# Bulk-silicon simulation plan

## Status

**Documentation-first design only; no runnable production stage and no production
result.** This directory owns future pristine bulk-silicon simulation declarations,
authorized execution records, compact outputs, and experiment verification. The
current documents define the intended software, calculation, execution, and
verification boundaries before implementation or protected execution.

Nothing in this directory establishes an accepted silicon parent, converged numerical
settings, a qualified Wannier representation, effective masses, scientific validation,
or calculator-execution authority.

## Objective

Prepare a separately authorized route that:

1. qualifies a scalar-relativistic, non-spin-polarized, non-SOC PBE bulk-silicon
   parent;
2. retains an identity-bound SCF state and constructs a full-grid NSCF state;
3. passes the verified NSCF state through `wannier90.x -pp`,
   `pw2wannier90.x`, and Wannier90 localization;
4. compares direct-parent and Wannier representations on declared construction and
   withheld sets; and
5. preserves exact evidence for later valley, effective-mass, and reduced-model
   analysis without treating software or process success as scientific acceptance.

## Ownership

This calculation root owns scientific selection, exact campaign declarations,
execution evidence, numerical acceptance, and experiment verification. Reusable
calculator-neutral records, workflow-domain composition, provider integrations,
native parsers, exact artifact handoffs, and single-calculator execution mechanics
belong to
[`projectkoios-simulations`](https://github.com/eragasa/projectkoios-simulations).
Project Koios must not select this calculation's scientific values or own its retained
results.

The local scientific authority remains:

- [`../development-plan.md`](../development-plan.md) — gated calculation sequence;
- [`../provisional-use-disposition.md`](../provisional-use-disposition.md) — limits on
  historical C48/K8 evidence;
- [`../evidence-crosswalk.md`](../evidence-crosswalk.md) — predecessor evidence status
  and non-transfer rules; and
- [`../../../../specification/dft-pseudopotential-library/v1/index.md`](../../../../specification/dft-pseudopotential-library/v1/index.md)
  — accepted pseudopotential-family decision; and
- [`../../../../docs/computational/Si-bulk/wannier-component-locality/index.md`](../../../../docs/computational/Si-bulk/wannier-component-locality/index.md)
  — authoritative Si-VC component-operator campaign planning.

These simulation documents bind future Project Koios consumption and execution
readiness across those authorities. They do not supersede the physical or numerical
specifications or create a competing Si-VC campaign definition.

## Upstream software authority

| Field | Binding |
| --- | --- |
| Repository | [`eragasa/projectkoios-simulations`](https://github.com/eragasa/projectkoios-simulations) |
| Inspected implementation baseline | `bbb9f1d8110ed9fe3ea1873c2366073c98f48c71` |
| Reviewed documentation-only architecture | `7ad5cad6576338945959a683f3cd407759e7c37c` |
| Existing authorities | `projectkoios.simulations.execution`, `calculator_input`, `evidence`; QE SCF/NSCF/saved-state and `pw2wannier90` integrations; Wannier90 native parsers |
| Planned bulk-qualification route | `projectkoios.simulations.workflows.pw_dft_bulk_qualification` |
| Planned Wannier route | `projectkoios.simulations.workflows.pw_dft_wannierization` |
| Planned neutral architecture | `docs/architecture/projectkoios/simulations/workflows/pw_dft_bulk_qualification/` and `pw_dft_wannierization/` |
| Planned provider architecture | `integrations/wannier90/preprocessing/`, `integrations/wannier90/localization/`, and `integrations/quantumespresso/pw2wannier90/artifacts/` under the upstream architecture tree |
| Planned first-party composition | Outward `projectkoios.adapters` mappings plus `tools/pw_dft_bulk_qualification` and `tools/pw_dft_wannierization` for provider selection, operational configuration, and route invocation |
| Current status | Implementation baseline plus reviewed architecture pin only; all listed end-to-end, provider, adapter, and tool additions remain unimplemented and are not an accepted dependency |

The architecture pin is a local documentation commit and has not been pushed. It adds
no `src/` implementation and grants no acquisition or execution authority. Normative
baseline links and the future dependency/conformance procedure are recorded
in [`architecture-plan.md`](architecture-plan.md). When an implemented upstream
capability is reviewed and actually imported, this project must pin its exact revision
through the declared dependency files. Adding or replacing that dependency requires
explicit human authorization. No copied description in this directory supersedes the
upstream software contract.

## Existing predecessor

The completed direct bootstrap remains at
[`calculations/bulk-silicon/production-convergence-preflight/`](../../../bulk-silicon/production-convergence-preflight/).
It contains nine SCF and nine linked diagnostic NSCF executions. Its inputs, compact
records, checksums, external-run identities, and embedded repository paths remain under
that immutable historical owner.

## Documentation set

| Document | Purpose |
| --- | --- |
| [`scientific-contract.md`](scientific-contract.md) | Physical branches, state spaces, unresolved decisions, and non-transfer rules |
| [`seed-structure-decision.md`](seed-structure-decision.md) | Exact selected provisional \(S_0\), identity, role, rationale, and non-transfer boundary |
| [`architecture-plan.md`](architecture-plan.md) | Existing Project Koios capability, missing capability, package ownership, and documentation-first work packages |
| [`execution-contract.md`](execution-contract.md) | Fail-closed preflight, stage boundaries, artifact policy, authorization packets, and failure behavior |
| [`verification-plan.md`](verification-plan.md) | Software, numerical, scientific, and independent-verification evidence and gates |
| [`readiness.md`](readiness.md) | Inspected repository and local-resource inventory, exact known identities, and current blockers |

## Scientific campaign order

The predecessor campaign is not part of the later five-occurrence Wannier route. Its
fixed order is:

1. joint coupled-cutoff and k-point qualification on the exact, explicitly provisional
   [`Si.PrimitiveUnitCell` seed \(S_0\)](seed-structure-decision.md), yielding only
   \(Q_0@S_0\);
2. zero-pressure structural convergence under \(Q_0\), yielding a mechanically
   qualified structure \(S_1\);
3. fresh joint setting confirmation on \(S_1\); and
4. re-relaxation and reconfirmation whenever the selected setting changes, until an
   exact stable pair \((S_*,Q_*)\) is accepted or the frozen budget ends
   inconclusively.

Only the accepted pair may emit a new, separately authorized parent-SCF requirement
for the separate SCF→NSCF→preprocessing→converter→localization route. A confirmation
SCF is not reused as that parent under this architecture.

## Admission rule for a successor

A numerical-qualification version may use an exact seed structure only when its
provisional status and non-transfer boundary are explicit. A production-parent version
requires the accepted pair \((S_*,Q_*)\). Every simulation version additionally
requires:

1. an accepted physical branch for its declared purpose;
2. exact executable and pseudopotential identities;
3. frozen inputs, numerical settings, warning policy, and stop policy;
4. a declared external workspace and compact-artifact policy;
5. expected runtime and resource bounds;
6. explicit authorization for the bounded QE or Wannier90 execution; and
7. an independent experiment-verification contract.

No empty stage scripts are provided. A stage is created only when its input, output,
failure, provenance, and verification contracts exist.

## Required order of work

1. Review and correct this documentation set.
2. Resolve every scientific decision assigned to this calculation owner.
3. Implement only accepted reusable capability in Project Koios.
4. Add deterministic tests and render-only demonstrations; do not execute a
   calculator.
5. Materialize exact declarations here and verify all identities.
6. Prepare one bounded execution authorization packet.
7. Execute only after explicit authorization, then retain evidence without automatic
   promotion.

The expected simulation families are historical-parent comparison, production-parent
setting qualification, conduction-valley characterization, Wannier
construction/qualification, and prospectively declared sensitivity controls. They
remain distinct versions. A later stage may consume only a verified predecessor and
must not overwrite it.

## Nonclaims

This plan does not:

- accept the 5.43 Å Project Koios example structure as a production PBE lattice;
- relabel the historical PseudoDojo v0.4.1 Si UPF as v0.5/stringent;
- accept the retained SSSP/QE 7.5 grid as this calculation's convergence evidence;
- declare locally available QE or Wannier90 executables scientifically accepted;
- authorize pseudopotential acquisition or calculator execution;
- define publication-grade numerical tolerances; or
- create, move, or overwrite calculation evidence.
