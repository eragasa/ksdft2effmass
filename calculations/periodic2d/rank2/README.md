# Periodic 2-D rank-two calculations

This directory is the calculation-side owner boundary for the controlled periodic
2-D studies whose retained operator representation has rank two. It is an inventory
and composition boundary, not a shared execution, result, or evidence package.

The child calculations answer different questions and retain separate identities:

| Calculation owner | Lifecycle status | Scope |
|---|---|---|
| [`orthogonal/band-equivalence-locality/`](orthogonal/band-equivalence-locality/README.md) | Direct typed lifecycle; one retained **CALCULATED RESULT — UNSEALED** execution | Square direct lattice, directed-axis parent, and axis-maximum gauge control. |
| [`periodic2d_rank2_hexagonal/`](../../periodic2d_rank2_hexagonal/README.md) | Replaceable nominal/refinement actions; no retained execution | Matched square, triangular-Bravais, and two-basis-metric synthetic controls with bond-RMS gauge normalization. This is not graphene. |
| [`periodic2d_rank2_rhombic_path/`](../../periodic2d_rank2_rhombic_path/README.md) | Development composition only; no retained execution | Unit-area rhombic geometry, M0/M1/M2 response controls, witnesses, and sampled transition scans. This is not an elastic or material model. |

The maintained periodic-1D rank-two calculation at
[`calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/`](../../periodic1d/rank2/band-equivalence-versus-hopping-locality/README.md)
is the lifecycle and evidence-architecture donor for this boundary. The periodic-2D
children preserve its separation of calculation, independent verification,
authenticated rendering, immutable execution identity, and explicit claim boundaries.
One-dimensional coefficients, meshes, Nyquist rules, support endpoints, and conclusions
are not transferred as periodic-2D scientific controls.

The band-equivalence calculations expose their public rank-two capabilities under
`ksdft2effmass.periodic2d.rank2` while retaining reusable arithmetic under
`ksdft2effmass.band_equivalence_hopping_locality`. They do not share a
scientific family identity, a metric, a bond inventory, a shell cap, or a conclusion.
The strain calculation is a separate family and must not be inferred from or merged into
either nominal band-equivalence execution.

## Shared rank-two conventions

For the nominal band-equivalence calculations, the donor's ordered scientific
responsibilities are retained as qualification, transport, equivalence, Fourier,
truncation/interpolation, support-selection, refinement, retention, independent
verification, and authenticated-rendering channels. In particular:

- a four-state synthetic parent is reduced to a declared rank-two retained space;
- comparisons occur only after the retained space, basis, gauge, energy reference,
  units, reciprocal coordinates, and direct-lattice geometry are identified;
- primitive direct-lattice vectors are serialized as columns;
- construction and withheld evaluation meshes have distinct declared origins;
- real-space truncation uses complete physical-metric shells and never splits an
  equal-radius shell;
- interpolation, truncation, and total errors remain separate channels; and
- sampled first-passing support is the minimum stored complete shell satisfying every
  declared finite criterion. An unresolved row remains unresolved at the frozen cap.

The Ragasa2026a rank-two quadratic loss specialization is

\[
L_H=\frac{1}{2E_{\mathrm{ref}}^2}\sum_q w_q
\lVert H_q-\widetilde H_q\rVert_F^2,
\qquad
L_\epsilon=\frac{1}{2E_{\mathrm{ref}}^2}\sum_q w_q
\sum_{n=1}^{2}(\epsilon_{qn}-\widetilde\epsilon_{qn})^2.
\]

`E_ref` is a declared normalization, not a band gap. Weights are normalized,
nonnegative, and index the leading tensor-mesh axes in NumPy C order. The reusable
finite-rank implementation is generic, but the historical square execution predates
that record and its result bytes are immutable. A future execution that retains these
losses must use a new execution identity and bind the exact matrix fields, basis,
retained-space, gauge, and geometry identifiers, energy-unit identity, normalization,
weights, production loss, and independent scalar reconstruction. It must not rewrite or reinterpret the
retained square `v1` bytes.

See [`scientific-controls.md`](scientific-controls.md) for the calculation-family
crosswalk and explicit admission boundaries. The exhaustive
[`diagnostic-parity.md`](diagnostic-parity.md) catalog maps every periodic-1D donor
diagnostic family to its periodic-2D typed realization or explicit dimension-specific
inapplicability disposition.

## Artifact and evidence rules

A direct lifecycle is

`typed configuration -> typed calculated result -> byte-owning independent verification -> authenticated rendering`.

Each stage owns exact canonical typed bytes and SHA-256 identities. A hash establishes
byte identity only. Verification establishes agreement with the declared finite checks
only. Neither establishes material validity, convergence, human acceptance, sealing,
or publication acceptance.

Scientific execution and retained-result creation require separate authorization. This
owner boundary does not authorize running any nominal, refinement, response, or scan
producer. Rendering must consume admitted stored bytes and must not rerun a scientific
calculation.

## Current limitations

- The retained square execution is unsealed and does not include the newer generic
  loss record.
- The nonorthogonal direct lifecycle is software-tested only in temporary roots; no
  retained direct execution exists.
- The strain family has typed development records but no byte-owning independent
  verifier, authenticated projection, direct execution package, or retained result.
- Mesh refinement is bounded diagnostic work, not convergence or uncertainty evidence.
- No child calculation is a first-principles, graphene, silicon, elastic, or
  experimentally validated material calculation.
