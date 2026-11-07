# Periodic-1D rank-one band equivalence and hopping locality

**Status:** typed calculate → independently verify → authenticated render lifecycle
implemented and exercised through one local unsealed execution; no sealed evidence
package, evidence promotion, publication artifact, or release exists.

This aggregate calculation root sequences the model-family-compatible rank-one null
control in the periodic multiband program. It composes scalar band equivalence, Fourier
interpolation, descriptive hopping locality, deliberate support truncation, and their
separate numerical consequences using conventions compatible with the rank-two and
higher-rank controlled calculations.

For a scalar represented Hamiltonian, phase conjugation is operator-trivial:

\[
U(k)^\dagger H(k)U(k)=H(k), \qquad U(k)\in U(1).
\]

The calculation therefore cannot exhibit gauge-induced represented-operator locality. Its scientific role is to establish the scalar Fourier/locality baseline and the boundary at which nontrivial internal gauge effects first become possible.

## Surfaces

- [`calculator.py`](calculator.py) defines `Periodic1dRank1Calculator`, a read-only,
  request-bound composition over one exact typed Fourier-locality result and one
  caller-selected physical lattice geometry. It exposes the unchanged source result as
  rank-one band equivalence and constructs separate alignment-applicability,
  hopping-locality, and support-truncation views over the exact production mesh. It
  introduces no wire and does not rewrite retained execution bytes.
- [`calculator.md`](calculator.md) records the calculator's ownership, correlation,
  numerical, and scientific boundaries.
- [`tests/test__Periodic1dRank1Calculator__result.py`](tests/test__Periodic1dRank1Calculator__result.py)
  replays the retained typed producer result read-only and verifies exact source-object
  correlation across all rank-one capability views.
- [`protocol.md`](protocol.md) defines the canonical rank-one \(R\)-\(k\)
  Bloch-hopping pair, physical lattice kinetic-energy scale, cyclic-to-ordinary
  conversion boundary, three-channel error decomposition, operation-first lifecycle,
  independent-verification requirements, and evidence boundary.
- [`donor-crosswalk.md`](donor-crosswalk.md) classifies every Mathieu1D, historical M1,
  former installed M1, rank-two, and shared-operation donor channel.
- [`legacy-retirement.md`](legacy-retirement.md) binds the exact removed source, test, and
  API-documentation bytes to their Git recovery authority and records package-aligned
  successor test ownership.
- [`scientific-control-decision.md`](scientific-control-decision.md) records the selected
  lowest ordered eigenvalue field of the exact controlled four-state parent, rejected
  alternatives, and the exact-versus-sampled claim boundary.
- [`numerical-control-decision.md`](numerical-control-decision.md) freezes the exact
  construction and Mathieu-scaled evaluation point sets, support inventory, three error
  channels, donor-compatible range analysis, finite error--complexity diagnostic, gates,
  thresholds, passage rules, and figure inventory.
- [`simulations/`](simulations/README.md) records the in-process calculation boundary;
  direct calculate, independently verify, and authenticated-render adapters live at this
  calculation root.
- [`analysis/`](analysis/README.md) records the implemented channels; reusable analysis
  belongs to installed source owners and rendering consumes verifier-authenticated data.
- [`technical-report/`](technical-report/README.md) is the comprehensive upstream
  scientific record: theory, literature position, exact parent, five benchmarks,
  complete finite results, diagnostics, verification, publication relationship,
  provenance, and nonclaims.
- [`docs/architecture/v3/ksdft2effmass/periodic1d/fourier_locality/`](../../../docs/architecture/v3/ksdft2effmass/periodic1d/fourier_locality/index.md) records the implemented package, module, and public-class contracts.

The three direct stage scripts produced the local unsealed
`executions/direct-controlled-four-state-n256/` scalar producer calculation, independent
verification, and authenticated two-figure rendering. The execution remains an
illustrative finite numerical control and has not been sealed or promoted. The existing
result wire predates the operation-first calculation layout: it contains the authoritative
Fourier, locality, and truncation channels, but it does not serialize the newer
rank-owned gauge-applicability, hopping-locality, and support-truncation wrapper values as
separate aggregate fields. `Periodic1dRank1Calculator` now composes those views in memory
without changing or reclassifying the retained wire.

## Analysis order

This family occupies the structural/scalar-control stage of the shared
[periodic analysis order](../../periodic/multiband/analysis-order.md). Interpret its
channels in this order:

1. exact parent, scalar retained field, units, sample roles, and support inventory;
2. complete Fourier reconstruction, Hermitian/Parseval checks, and withheld interpolation;
3. descriptive hopping locality before support removal;
4. complete-support truncation;
5. separate interpolation, truncation-only, and total consequences;
6. byte-owning independent verification; and
7. authenticated rendering from admitted verification data.

The scalar phase identity is the null control; it must be established before using
matrix-valued gauge-locality results. The operational scripts remain calculate, verify,
then render. Completion of those stages does not authorize sealing or evidence promotion.

## Relationship to Mathieu1D

The retained [`calculations/mathieu1d/`](../../mathieu1d/) package remains a separate periodic-potential and single-band Fourier-reduction benchmark. It is not renamed, replaced, or treated as the rank-one specialization of this controlled model family.

## Program context

The cross-rank plan and current evidence map are maintained under [`calculations/periodic/multiband/`](../../periodic/multiband/).

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Scalar null-control protocol | Implemented; phase alignment is operator-trivial and is not emitted as duplicate alignment results. |
| Simulation, analysis, and technical-report surfaces | Typed configuration/result wires, producer, independent verifier, authenticated projection, closed renderer, direct scripts, tests, and comprehensive upstream report exist; one local unsealed execution has completed all three stages without evidence promotion. |
| [`calculations/mathieu1d/`](../../mathieu1d/) | Retained scalar periodic-potential benchmark and method donor, not this compatible specialization. |
| Historical ICMSEP M1 isolated-band package | Refinement, reconstruction, truncation, fitting-route, and withheld-evaluation donor at Git tree `418999a90efa3001d2e50a2e7912f126bc30903f` from commit `c5d34a93b4710a4a430738c404c775865d418d42`; not this family identity. |
| Former installed M1 surface | Completely retired after direct replacement; exact source, test, and Sphinx bytes remain recoverable through `legacy-retirement.md`, with no compatibility facade or live schema-v1 decoder. |
| Shared single-band reduction operations | Audited in `donor-crosswalk.md`; canonical `solidstate`, `analysis`, and model-analysis infrastructure retain reusable behavior, while this calculation retains its own model, conventions, controls, tolerances, and interpretation. |
| Scalar parent | Bound in the typed configuration as the lowest ordered eigenvalue field of exact parent `ksdft2effmass.periodic1d.controlled-four-state-parent.v1`; sampled gap qualification does not establish a globally isolated band. |
| Finite numerical controls | Frozen in `numerical-control-decision.md`; all results remain finite and numerical, and no Formal certificate is introduced. |
