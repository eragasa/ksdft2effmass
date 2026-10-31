# Bulk-silicon verification plan

## Scope

This document owns calculation-specific numerical verification, independent-toolchain
comparison, scientific validation, and evidence-promotion gates. Reusable Project Koios
software tests and generic validation algorithms remain authoritative upstream and are
not duplicated here.

## Evidence classes

| Evidence class | Authority | Question answered | Does not establish |
| --- | --- | --- | --- |
| Software verification | Project Koios | Does reusable software satisfy its declared deterministic contract? | Numerical convergence or physical correctness |
| Calculation composition verification | This calculation | Do exact local declarations conform to the pinned upstream contracts and agree internally? | Numerical or scientific acceptance |
| Numerical verification | This calculation | Are finite settings stable for named observables under prospective comparisons? | Parent-model adequacy or experimental agreement |
| Scientific validation | This calculation | Does the qualified parent/representation support the intended physical claims within stated scope? | Universal transferability |
| Independent verification | This calculation's independent verifier | Can compact evidence and named observables be reproduced independently? | Automatic acceptance or publication authority |

Human acceptance and calculator authorization are separate from all five.

## Upstream software gate

Before this calculation composes a route, the exact Project Koios dependency revision
must provide and verify the required public contracts. The current inspected baseline
is cataloged in [`architecture-plan.md`](architecture-plan.md); it is not a complete
route conformance pin.

The upstream review must establish, without a production silicon run:

- deterministic neutral and provider projections;
- exact artifact identity and lineage verification;
- rejection of unsafe paths, tampering, mismatched dimensions, and unrelated parent
  states;
- fail-closed authorization and one-process occurrence behavior;
- timeout, failure, and output recording with fake executables;
- provider-native artifact closure for the spectral profile and any declared
  component-operator coefficient or sampled-wavefunction extension; and
- repository boundary, typing, packaging, and documentation checks.

This calculation records the exact upstream revision and test evidence it consumes. It
does not restate upstream field inventories, validation algorithms, or complete test
matrices.

## Calculation composition gate

Before authorization, an independent preflight check must authenticate and correlate:

- local scientific and execution declarations;
- exact structure and pseudopotential identities;
- exact Project Koios revision, consumed public symbols, and schema versions;
- exact executable identities and toolchain records;
- stage input and predecessor manifests;
- k-point, band, spin, Wannier-rank, and artifact dimensions;
- workspace and invocation-count bounds; and
- warning, retry, timeout, stop, and retention policies.

The result is pass, fail, or inconclusive with exact reasons. A pass permits an
authorization request only.

## Historical Stage-0 comparator

The comparator assesses the provisional historical C48/K8 branch and warning behavior.
Before execution, freeze:

- exact historical structure, pseudopotential, inputs, and reference-output identities;
- independently identified QE executable and toolchain;
- named observables and residual definitions;
- prospective tolerances;
- handling of invalid, divide-by-zero, overflow, and underflow warnings; and
- an inconclusive outcome when evidence cannot support harmlessness or disagreement.

Retain native totals and residuals, parsed completion and convergence facts, warning
classes, exact output identities, and an independently generated compact comparison.
Matching total energy alone is insufficient. A rerun with the same executable and
linked libraries is repeatability evidence, not an independent toolchain comparison.

## Bulk-parent qualification gates

The setting-qualification branch begins only after exact v0.5/stringent Si UPF2
identity, the exact provisional
[`Si.PrimitiveUnitCell.RightHanded` \(S_0\)](seed-structure-decision.md), and frozen
coordinates, observables, tolerances, and budgets. The gates then execute in this
order:

1. **Joint cutoff/k-point gate on \(S_0\).** Separately assess wavefunction and
   charge-density cutoff behavior, reciprocal-sampling behavior, their selected-corner
   interaction, SCF residual/solver stability, total energy, stress, and any declared
   fixed-point band/gap controls. Retain only \(Q_0@S_0\).
2. **Structural gate under \(Q_0\).** Verify process and optimizer facts separately
   from final-cell validity, force tolerance, pressure residual relative to the declared
   target, allowed cell-mode changes, and exact artifact correlation. A qualified result
   yields \(S_1\), not yet a production pair.
3. **Final-setting gate on \(S_1\).** Repeat a joint confirmation stencil with the
   candidate and prospectively required stricter context. Produce \(Q_1@S_1\); do not
   transfer \(Q_0@S_0\) by matching labels or integer mesh tuples.
4. **Stable-pair gate.** If the selected setting changes, re-relax and reconfirm. Accept
   only \((S_*,Q_*)\) within the frozen feedback budget; otherwise retain a failed,
   inconclusive, or budget-exhausted record.
5. **Downstream parent gates.** Stable-pair acceptance emits a new separately
   authorized parent-SCF requirement; confirmation SCFs are not reused as the parent.
   Only from that parent assess valley identity and location and
   curvature/effective-mass sensitivity under their separate policies.

The retained FCC-native relaxation completed structural gate execution under the
provisional \(Q_0\): QEXSD exit status, stdout completion, electronic convergence,
optimizer convergence, atom count, pressure, force, right-handed basis restoration,
and exact artifact identities were checked separately. The result is provisional
\(S_1\), not by itself a stable pair. Gate 3 has now completed on the exact
`Si.PrimitiveUnitCell.RightHanded.RelaxedS1` bytes: the calculation-owned sampled
rules again select Gamma-centered K10 and 42/336 Ry. The operator accepted this exact
pair at gate 4 under those rules. Gate 5 remains unexecuted and requires a new parent
SCF with separate bounded authorization.

Adjacent finite-setting stability is evidence about those finite points, not an
infinite-basis error bound. Changing pseudopotential resets the campaign. Changing
geometry invalidates transfer and requires the declared fresh confirmation step.

## Valley and effective-mass gates

Before execution, declare:

- search domain and reciprocal-coordinate convention;
- band or cluster identity tracking and degeneracy handling;
- construction and withheld k-points;
- finite-difference stencil or fit model;
- fit window and conditioning criteria;
- energy and momentum units;
- tensor convention and principal-axis extraction; and
- convergence and sensitivity criteria.

Acceptance requires evidence that the located minimum is not merely an assumed nominal
probe. Fixed-point band agreement cannot substitute for curvature convergence.

## Wannier construction gates

### Construction evidence

Retain:

- exact projections, outer/frozen windows, rank, seedname, mesh, and neighbor graph;
- direct-parent band inventory and selected subspace;
- exact upstream and native route identities;
- preprocessing and converter evidence;
- for the component-operator profile, authenticated parent plane-wave coefficient
  evidence and its exact correlation with the gauge/disentanglement frame, plus exact
  transform evidence if sampled real-space wavefunctions are used;
- localization convergence, centers, spreads, and warnings;
- gauge and disentanglement matrices as applicable; and
- real-space Hamiltonian with lattice-vector and degeneracy conventions.

### Construction and withheld comparisons

On prospectively separated sets, compare as applicable:

- direct and interpolated eigenvalues after declared scalar energy alignment;
- isolated states or degenerate-cluster projectors after declared state-space
  alignment;
- band ordering and valley identity;
- group velocities or curvature/effective masses;
- represented operators after basis/gauge alignment; and
- sensitivity to windows, projections, mesh, and real-space truncation.

Training-set interpolation agreement alone is insufficient. Separate channel optima do
not establish a common admissible witness.

### Failure and inconclusive outcomes

The calculation must retain without promotion:

- localization failure or nonconvergence;
- dimension or lineage inconsistency;
- direct/Wannier disagreement beyond prospective tolerance;
- withheld failure despite construction-set agreement;
- numerical floors too large for the target decision; and
- inconclusive evidence.

Process failure, numerical failure, and scientific inadequacy remain distinct outcomes.

## Independent compact-result verifier

The independent verifier consumes retained compact evidence rather than the producer's
in-memory result. It must:

1. authenticate every compact input and output;
2. independently parse or recompute named observables where practical;
3. check dimensions, units, basis, energy reference, and parent identity;
4. reproduce comparison arithmetic and prospective tolerances;
5. report pass, fail, or inconclusive with exact reasons; and
6. remain unable to authorize successors or promote evidence automatically.

Its implementation and retained identity belong to this calculation's verification
contract. It may consume generic Project Koios records but must not trust process status
as scientific acceptance.

## Gate matrix

| Gate | Producer | Verifier | Success permits |
| --- | --- | --- | --- |
| Upstream architecture accepted | Project Koios | Upstream architecture review | Upstream implementation only |
| Upstream software verified | Project Koios | Exact upstream test/review evidence | Dependency review only |
| Dependency accepted | This project | Dependency and boundary review | Local composition only |
| Exact campaign preflight | This calculation | Independent identity/preflight check | Authorization request only |
| Authorized occurrence completed | Provider integration | Process/artifact verifier | Stage analysis only |
| Numerical setting accepted | This calculation | Independent compact-result verifier | Named successor declaration |
| Wannier representation accepted | This calculation | Withheld-set and lineage verifier | Declared downstream use only |
| Publication claim accepted | Publication owner | Applicable scientific review | Exact bounded claim only |

No gate grants calculator execution except a separate explicit execution
authorization.
