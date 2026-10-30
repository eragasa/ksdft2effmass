# Si-VC Wannier-component-locality campaign

**Status:** proposed, unexecuted, and blocked. A later scientific sequencing decision
requires cutoff/k-point qualification before structural convergence and invalidates the
previous 56-place/55-transition Si-VC topology as an implementation candidate. The
retained exact-digest review remains evidence about its former bounded scope only; a
revised topology and review are required. No Quantum ESPRESSO,
`pw2wannier90.x`, Wannier90, scheduler, remote, or production execution is
authorized by this bundle.

This directory is the authoritative computational-planning surface for the
**Si-VC** PBE/PseudoDojo-ONCV QE--Wannier90 component-locality campaign. The
former single-file entry point is retained only as a compatibility pointer at
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
  lineage, selected terminal-companion contract, and bounded cancellation
  declaration.
- [Exact-digest design review](reviews/SI-VC-WORKFLOW-BINDING-001.md) — immutable
  owner/consumer/provider candidate, resolved findings, retained implementation
  blockers, and change-invalidation rule.
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

## Historical topology and replacement requirement

The previously corrected provider-side draft proposed a net named
`si_vc_component_locality` with 56 unique places and 55 unique transitions.
Independent recounting matched those totals, but the draft orders zero-pressure
relaxation before cutoff/SCF-mesh qualification. It is therefore superseded by the
new seed-setting→structure→final-confirmation decision and must not be implemented.
Its counts and digest remain historical design-correlation evidence only.

A replacement architecture must:

1. assign the material scientific CPN to the `ksdft2effmass` campaign owner;
2. consume the ProjectKoios bulk-qualification child as
   \(S_0\to Q_0@S_0\to S_1\to Q_1@S_1\), including bounded re-relax/reconfirm
   feedback, before admitting a production parent;
3. route every external completion/evidence token through an explicit boundary
   place before an acceptance transition produces a retained record; and
4. preserve the consumable active latch, quiescent finalization, and exactly-one
   terminal-outcome invariant.

The ownership decision reserves the eventual authoritative source path as
`python/src/ksdft2effmass/campaigns/si_vc/cpn/net.py` and selects Generic
Workflow's runtime-neutral canonical CPN/binding contract, but no current topology is
authoritative or ready to implement. The Si-VC consumer
requirements for that contract are specified in the [workflow binding
profile](workflow-binding.md): CPN tokens carry typed content-addressed JSON
references, the authoritative simulations-owned SCF child is referenced without
copying its topology, and an exact SCF handoff plus verified staging receipt
binds the SCF saved-state outputs used as NSCF inputs. The merged Generic Workflow owner contract has exact SHA-256
`e6428a8b0d8a47d4f9a6596300fe5ccc65bb16c12e1cc8ffe64884720bd513c2`
(owner source commit `9ec0944dad3af1706edf01101e443e244da22ef5`, merge
commit `3861f22db3b182743bd1e7ba6fe5721d7895948b`). It defines the
bounded control-record/expression, payload-reference, terminal-companion,
staging, replay, cancellation, and quiescence design contracts. It remains
unimplemented and must not be invented locally.

The merged simulations provider design has exact SHA-256
`adfa47ba9007e3b08b02d219bf5d7b29de28a48531876c79559a510fc5484858`
(provider source commit `b6995de15dd44067c55d9055735d26b11b80e712`,
merge commit `8e70e02cc0f723477bcac42b0f163097f628c88a`). It closes
candidate bounds, exact child-export correlation, terminal-companion mapping,
the version-pinned closed-AST export route, and truthful bounded cancellation at
design level. The retained [exact-digest review](reviews/SI-VC-WORKFLOW-BINDING-001.md)
reported `NO_BLOCKING_FINDINGS` for the now-superseded bounded design. Under its own
change-invalidation rule, that outcome does not review the new campaign order. A
replacement topology, renewed cross-repository review, path-free immutable
artifact-set/success projection, actual canonical exporter, profile, golden bytes,
runtime segments, and fixtures remain implementation-readiness blockers.

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
