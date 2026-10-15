# Si-VC Wannier-component-locality campaign

**Status:** proposed, unexecuted, and blocked. The bounded re-review of the
corrected CPN architecture found no remaining blocker in the three previously
identified topology defects; implementation and scientific readiness remain
incomplete. No Quantum ESPRESSO, `pw2wannier90.x`, Wannier90, scheduler, remote,
or production execution is authorized by this bundle.

This directory is the authoritative computational-planning surface for the
**Si-VC** PBE/PseudoDojo-ONCV QE--Wannier90 component-locality campaign.

- Campaign-family identity:
  `ksdft2effmass.campaign.bulk-silicon.si-vc.wannier-component-locality`
- Immutable campaign-version identity: not assigned
- Retained run or evidence-package identity: none

The family identity is independent of a publication and does not encode a provisional
version. The former single-file entry point is retained only as a compatibility pointer
at
[`bulk-silicon-wannier-component-locality-plan.md`](../../bulk-silicon-wannier-component-locality-plan.md).

## Purpose

The campaign asks whether, for one accepted silicon valence-plus-conduction
retained subspace and one declared Wannier construction, the represented total
Hamiltonian requires less pair-symmetric real-space support than both its
canonical kinetic component and represented non-kinetic remainder at frozen
operator-error levels.

The campaign does not presume that ordering. It must not infer it from a smooth
band plot, small spreads, one mesh, one gauge, one truncation radius, or a
successful calculator interface.

## Navigation

- [Scientific definition](scientific.md) — material branch, retained subspaces,
  bounded claim, gauge dependence, and allowed dispositions.
- [Numerical definition](numerics.md) — represented operators, truncation
  metrics, evaluation channels, guards, and staged numerical design.
- [CPN schematics](schematics.md) — authoritative-topology requirement,
  cross-repository ownership, human gates, authority boundary, and open topology
  findings.
- [Workflow binding profile](workflow-binding.md) — canonical CPN identity,
  content-addressed JSON tokens, hierarchical SCF-child binding, SCF→NSCF
  provenance, persistence, replay, cancellation, and conformance requirements.
- [SCF saved-state lineage](scf-saved-state-lineage.md) — provider-candidate
  response, exact Si-VC accepted-parent and staging-receipt schemas, derived NSCF
  lineage, companion-evidence amendment, and bounded cancellation declaration.
- [Implementation and readiness](implementation.md) — implemented foundations,
  provider preflight, missing contracts, evidence requirements, and execution
  blockers.

## Authoritative inputs

This plan composes, without revising:

- [`ksdft2Effmass.physical-specification.v1.md`](../../../../specification/ksdft2Effmass.physical-specification.v1.md);
- [`ksdft2Effmass.numerical-specification.v1.md`](../../../../specification/ksdft2Effmass.numerical-specification.v1.md);
- the [bulk-silicon production program](../../bulk-silicon-production-program.md);
- the [downstream sampling plan](../../bulk-silicon-downstream-sampling-plan.md);
- Tasks [`03.01.01`](../../ksdft2Effmass.computational.03.01.01.md),
  [`03.01.02`](../../ksdft2Effmass.computational.03.01.02.md), and
  [`03.01.03`](../../ksdft2Effmass.computational.03.01.03.md) for rank,
  projections, windows, and the uniform Wannier mesh; and
- Task [`02.01.04`](../../ksdft2Effmass.computational.02.01.04.md) for the
  zero-pressure PBE lattice.

Where this bundle and an authoritative specification differ, the specification
wins. Ambiguity that changes the physical or numerical problem blocks execution
rather than being resolved by preference.

## Current architecture disposition

The corrected provider-side draft proposes a net named
`si_vc_component_locality` and contains 56 unique places and 55 unique
transitions. Independent recounting matched those totals. The former 43-place,
47-transition inventory and report digest are superseded.

The corrected architecture now:

1. assigns the material scientific CPN to the `ksdft2effmass` campaign owner;
2. routes every external completion/evidence token through an explicit boundary
   place before an acceptance transition produces a retained record; and
3. uses one consumable `campaign_active` latch, a `finalization_action`, a
   Workflow quiescence event, and one `accept_campaign_finalization` transition
   so only one terminal outcome can be emitted.

The architecture decision fixes the authoritative source path as
`python/src/ksdft2effmass/campaigns/si_vc/cpn/net.py` and selects Generic
Workflow's runtime-neutral canonical CPN/binding contract. The Si-VC consumer
requirements for that contract are specified in the [workflow binding
profile](workflow-binding.md): CPN tokens carry typed content-addressed JSON
references, the authoritative simulations-owned SCF child is referenced without
copying its topology, and an exact SCF handoff plus verified staging receipt
binds the SCF saved-state outputs used as NSCF inputs. The proposed owner contract with exact SHA-256
`463e1021d19cae8c2f5d6ed9fb65015f8dc81f38c527f92e227838f1d82346b1` has
independent Workflow-owner and simulations-provider technical reviews with no
blocking findings. The operator selected that digest as the consumer-led
conformance target and removed any separate Workflow acceptance gate. It remains
unimplemented and must not be invented locally.

A corrected simulations provider proposal, exact SHA-256
`d33d584463c057783b955cd31cfdd801db75206e087bdef254ded99bd0065de5`
(superseding `616b713c…`), now defines the candidate-handoff and
deterministic-export design with exact candidate bounds and a truthful bounded
cancellation declaration. Its bounded review outcome remains `CHANGES_REQUIRED`:
terminal companion-evidence owner amendment, path-free artifact-set/success
projection, and future canonical exporter/golden bytes remain blockers. The
consumer response is recorded in
[SCF saved-state lineage](scf-saved-state-lineage.md).

No second campaign SNAKES implementation may be added under simulations. The
scientific freezes H1--H3 remain separate decisions. Protected execution
authorization is later, exact in scope, and does not follow from topology
acceptance.

## Evidence boundary

This bundle records a proposed calculation and software architecture. It reports
no Si-VC calculation, compatible production toolchain, converged setting,
validated effective mass, locality ordering, uncertainty quantification, or
material acceptance. Passing future software tests would establish software
behavior only.
