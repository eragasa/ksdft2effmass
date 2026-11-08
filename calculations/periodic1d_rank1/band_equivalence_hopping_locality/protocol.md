# Periodic-1D rank-one Bloch-hopping research protocol

**Protocol identity:** `periodic1d-rank1-rk-bloch-hopping-v1`

**Status:** prospective operation-first aggregate protocol with one retained predecessor
execution

**Execution authority:** no external electronic-structure calculation is authorized or
required by this protocol

## 1. Purpose

This protocol studies the relation between a periodic rank-one Bloch Hamiltonian in
reciprocal space and its hopping representation on the ordinary one-dimensional lattice.
It separates five questions:

1. whether the retained scalar band is reconstructed by the declared finite Fourier
   representation;
2. how hopping magnitude is distributed over real-space displacements;
3. what support is deliberately removed by a finite-range model;
4. how interpolation, truncation, and total errors differ; and
5. which conclusions remain invariant under the rank-one `U(1)` gauge action.

The protocol is a finite numerical control. It does not establish continuum convergence,
a globally isolated band, material validity, or publication-qualified scientific
evidence.

## 2. Primary notation: the \(R\)-\(k\) pair

The direct lattice is

\[
\Lambda=\{R=na:n\in\mathbb Z\},
\]

where \(a>0\) is the lattice constant. The first Brillouin zone is represented by

\[
\mathcal B=[-\pi/a,\pi/a).
\]

The ordinary-lattice hopping coefficients and Bloch Hamiltonian form the Fourier pair

\[
H(k)=\sum_{R\in\Lambda}T(R)e^{ikR},
\qquad
T(R)=\frac{a}{2\pi}\int_{\mathcal B}H(k)e^{-ikR}\,dk.
\]

Here:

- \(R\) is a real-space lattice displacement;
- \(k\) is Bloch crystal momentum;
- \(T(R)\) has physical energy units; and
- rank one means that \(H(k)\) and each \(T(R)\) are scalar complex quantities.

Hermiticity requires

\[
T(-R)=T(R)^*,
\]

with a real onsite coefficient \(T(0)\). The symbol \(q\) is not used as the primary
Bloch coordinate. If a dimensionless reduced coordinate is needed for compatibility
with retained predecessor data, it is defined explicitly by

\[
q=\frac{ak}{2\pi}\in[-1/2,1/2),
\]

so that \(e^{ikR}=e^{2\pi iqn}\) for \(R=na\).

## 3. Physical scale and model role

The lattice kinetic-energy scale is

\[
E_a=\frac{\hbar^2}{m_ea^2},
\]

without the kinetic-operator factor \(1/2\). Normalized parameters are

\[
t_n=\frac{T(na)}{E_a}.
\]

Normalized values are dimensionless analysis inputs only. Before constructing a
Bloch-hopping model, they must be dimensionalized as \(T(na)=E_at_n\) in an explicit
physical energy unit. The model performs no implicit unit conversion.

A parameterized rank-one Bloch-hopping model has the fixed scientific role
`PeriodicModelRole.REDUCED_MODEL`. That role does not assert that fitting, independent
verification, scientific validation, or material qualification has completed.

## 4. Frozen retained field

The controlled ambient parent is

\[
K(k)=T_0+e^{ika}T_{+a}+e^{-ika}T_{+a}^{\dagger},
\]

acting on the standard four-state basis. The retained scalar field is the least ordered
eigenvalue

\[
H_{\mathrm{ret}}(k)=\lambda_0(K(k)).
\]

The exact rational parent coefficients, selected identity, and rejected alternatives are
owned by [`scientific-control-decision.md`](scientific-control-decision.md). The parent
has ambient matrix support \(\{-a,0,+a\}\). This does **not** imply finite ordinary-lattice
support for the nonlinear eigenvalue field \(H_{\mathrm{ret}}(k)\).

The predecessor execution used the exact positive reference `E_ref = 1` and stored its
parent entries as dimensionless ratios to that reference. This protocol does not rewrite
or reinterpret those retained bytes. A future operation-first execution must bind its
physical lattice geometry, \(E_a\), physical energy unit, basis identity, and energy
reference explicitly.

## 5. Scientific propositions under test

The finite study evaluates the following bounded propositions.

### P1. Rank-one gauge applicability

For every phase field \(U(k)\in U(1)\),

\[
U(k)^*H_{\mathrm{ret}}(k)U(k)=H_{\mathrm{ret}}(k).
\]

Therefore the scalar represented operator has one operator-trivial gauge-applicability
result. Global, pointwise, inverse-oracle, and restricted-circuit alignment cases are not
emitted as duplicate numerical channels.

### P2. Complete finite Fourier reconstruction

On each declared construction mesh, the complete finite cyclic transform must reconstruct
its source samples within the declared software tolerance. Agreement on a finite mesh is
not continuum equality.

### P3. Descriptive hopping locality

Before deleting support, the complete coefficient inventory is measured through
coefficient magnitudes and omitted-tail norms. These are descriptive properties of the
selected representation and do not themselves define a truncated model.

### P4. Support-truncation tradeoff

For each declared range \(R_c\), deliberate removal of coefficients outside
\(|R|\le R_c\) produces a distinct reduced candidate. Smaller error at one sampled mesh
does not establish global optimality or material adequacy.

## 6. Finite cyclic and ordinary-lattice representations

The finite discrete Fourier transform produces coefficients on a cyclic group. Those
coefficient classes are not automatically ordinary integer-lattice hoppings.

Every execution must retain separately:

1. the centered cyclic representative inventory;
2. the exact transform convention and normalization;
3. any negative-Nyquist-boundary class;
4. the declared conversion from cyclic classes to ordinary displacements; and
5. the resulting ordinary-lattice coefficient inventory.

No native cyclic coefficient may be silently substituted for an ordinary-lattice hopping.
If conversion removes, combines, or reassigns a representative, its contribution must be
recorded as a separate conversion channel before interpolation or truncation is evaluated.

The construction meshes, disjoint evaluation meshes, support inventory, gap gate,
thresholds, refinement rule, and finite error-complexity diagnostic are frozen in
[`numerical-control-decision.md`](numerical-control-decision.md).

## 7. Error-channel decomposition

Let \(I_N(k)\) be the complete interpolant constructed from an \(N\)-point mesh, and let
\(H_{N,R_c}(k)\) be the ordinary-lattice candidate after deliberate support restriction
to \(|R|\le R_c\). On the disjoint evaluation mesh \(E_M\), define

\[
e_{\mathrm{int}}(N,M)
 =\max_{k\in E_M}|H_{\mathrm{ret}}(k)-I_N(k)|,
\]

\[
e_{\mathrm{trunc}}(N,R_c,M)
 =\max_{k\in E_M}|I_N(k)-H_{N,R_c}(k)|,
\]

and

\[
e_{\mathrm{tot}}(N,R_c,M)
 =\max_{k\in E_M}|H_{\mathrm{ret}}(k)-H_{N,R_c}(k)|.
\]

These channels have different meanings:

- interpolation error compares the direct retained field with the complete interpolant;
- truncation error isolates deliberate support removal relative to that interpolant; and
- total error compares the truncated candidate directly with the retained field.

The pointwise residuals telescope, but the three maxima are not added as if they were
independent uncertainties. Verification checks

\[
e_{\mathrm{tot}}\le e_{\mathrm{int}}+e_{\mathrm{trunc}}
\]

without replacing any channel by the bound. Threshold and first-passage decisions use
\(e_{\mathrm{tot}}\), not \(e_{\mathrm{trunc}}\).

Any direct coefficient-fitting route remains a separate construction. Its residual must
not be relabelled as interpolation error or transform-mediated truncation error.

## 8. Operation ownership and execution order

The calculation is composed in the following order.

1. **Model definition** — bind \(a\), length unit, \(E_a\), energy unit, energy reference,
   basis identity, and ordinary-lattice Hermiticity.
2. **Gauge applicability** — serialize the one rank-one `operator-trivial` result.
3. **Band equivalence** — calculate the retained scalar field and complete finite cyclic
   reconstruction.
4. **Cyclic-to-ordinary conversion** — retain the conversion ledger without changing the
   source transform record.
5. **Hopping locality** — measure the complete ordinary coefficient inventory and omitted
   tails without removing support.
6. **Support truncation** — construct each declared finite-range candidate.
7. **Error evaluation** — retain interpolation, truncation-only, and total channels
   separately on construction and disjoint evaluation meshes as declared.
8. **Aggregate decisions** — apply adjacent-mesh stability, the final `128 -> 256` gate,
   threshold passage, first joint passage, and sustained-passage rules.
9. **Independent verification** — reconstruct admitted values without invoking the
   production analyzer.
10. **Authenticated rendering** — render only the closed figure inventory from passing,
    digest-bound verification data.

The operation owners are documented at the context root:

- [`../gauge_alignment/`](../gauge_alignment/README.md);
- [`../band_equivalence/`](../band_equivalence/README.md);
- [`../hopping_locality/`](../hopping_locality/README.md); and
- [`../support_truncation/`](../support_truncation/README.md).

## 9. Required retained records

A new aggregate execution must retain immutable, canonically serialized records for:

- protocol and configuration identity;
- lattice constant, length unit, and reciprocal convention;
- energy-scale convention, energy unit, and energy-reference identity;
- parent and retained-field identity;
- basis identity and retained dimension;
- construction and evaluation meshes with sample roles;
- complete cyclic coefficients;
- cyclic-to-ordinary conversion ledger;
- complete ordinary-lattice coefficients;
- per-range omitted-tail quantities;
- per-range retained coefficients and candidate identity;
- interpolation, truncation-only, and total errors;
- finite qualification, refinement, threshold, and passage decisions;
- child-result identities and SHA-256 digests;
- independent-verification results; and
- authenticated visualization-data and figure digests.

An aggregate must correlate child records by exact identity and digest rather than copying
uncorrelated values into a new wire.

## 10. Independent-verification requirements

The verifier owns the admitted result bytes. It must not call the production analyzer or
trust stored derived decisions as an oracle. It independently reconstructs:

- the retained parent samples;
- the finite transform and inverse reconstruction;
- Hermiticity and conjugate displacement pairing;
- the cyclic-to-ordinary conversion;
- omitted-tail quantities;
- every truncated candidate;
- all three error channels;
- mesh-refinement and passage decisions; and
- the visualization projection.

Passing software verification establishes agreement with the declared finite protocol
only. It is not a proof of scientific correctness, continuum convergence, or material
validity.

## 11. Lifecycle and overwrite policy

The direct lifecycle remains:

1. `run_01_calculation.py` — calculate and write immutable result bytes;
2. `run_02_verification.py` — independently verify exact admitted bytes; and
3. `run_03_render.py` — render only passing authenticated data.

Each stage must refuse overwrite. A new operation-first aggregate uses a new execution
identity and must not mutate
`executions/direct-controlled-four-state-n256/`.

That predecessor execution remains a local unsealed illustrative finite control. Its
existing Fourier-locality wire predates the operation-first wrappers and is preserved as
retained historical evidence; this protocol does not silently add fields to or relabel
that wire.

## 12. Certification boundary

The reusable exact certification contract is owned by
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support`, not by this
calculation directory or the Fourier-locality analyzer. It may bind a future exact
execution and its independent numerical verification to the finite proposition that one
selected support is the first support jointly passing the mediated and direct
maximum-total-error threshold.

The implemented certification wire classifies supplied exact rational intervals only.
It does not currently produce or independently verify outward enclosures, does not alter
the retained predecessor bytes, and does not admit a runtime certificate as evidence.
Any interval engine, producer trace, independent containment verifier, or retained
certification execution requires separate review. A dependency addition also requires
explicit human authorization.

## 13. Acceptance and disposition

A finite execution may be reported as **software-pass** only when:

- all required records are present and type-valid;
- complete transform reconstruction satisfies the frozen tolerances;
- Hermiticity and route-agreement checks pass;
- the independent verifier reconstructs every admitted value and decision;
- result, verification, visualization-data, and figure digests are correlated; and
- no-overwrite behavior is confirmed.

The following remain separate human dispositions:

- whether the control is scientifically adequate for a stated comparison;
- whether an execution may be sealed or promoted as evidence;
- whether a result may support a publication claim; and
- whether a fitted reduced model is adequate for a material application.

## 14. Claim boundary

This protocol does not establish:

- a global band-isolation theorem;
- continuum or infinite-mesh convergence;
- non-Abelian gauge behavior;
- physical material validation;
- a fitted-model optimum;
- uncertainty quantification;
- equivalence to a DFT or Wannier parent;
- sealing, publication qualification, or software release status; or
- authority to run Quantum ESPRESSO, Wannier90, remote, cluster, or cloud computation.

Its intended result is a reproducible, operation-separated rank-one \(R\)-\(k\)
Bloch-hopping control whose representation, conversion, locality, truncation, and error
channels can be compared without conflation.
