# Continuum-refinement numerical techniques and scientific reasoning

## Status and authority

This page explains the numerical design and scientific reasoning of the bounded
periodic-1D continuum-refinement campaign. It is an architecture explanation, not a
replacement for the authoritative retained calculation documents:

- `calculations/research-monograph/impurity-defect-1d-continuum-refinement/protocol.md`
  fixes the represented problem, refinement axes, diagnostics, thresholds, and decision
  rules;
- `calculations/research-monograph/impurity-defect-1d-continuum-refinement/input.json`
  is the exact version-one machine input;
- `calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json`
  is the exact retained machine result;
- `calculations/research-monograph/impurity-defect-1d-continuum-refinement/report.md`
  interprets that finite result; and
- `calculations/research-monograph/impurity-defect-1d-continuum-refinement/verify_result.py`
  independently reconstructs the retained numerical evidence.

The campaign produces synthetic test data and bounded numerical-verification evidence.
It does not establish an asymptotic theorem, a physical semiconductor model, material
validation, transferability, uncertainty quantification, or scientific acceptance.
Row 042 concerns exact encoded-document ownership; the scientific and numerical
interpretation described here belongs to the calculation, workflow, and verification
owners rather than to `ContinuumRefinementEncodedDocuments`.

## Scientific question

An earlier fixed-grid defect comparison observed improving agreement between a scalar
lattice parent and a parabolic band-edge comparator as a Gaussian profile broadened.
That observation alone cannot identify a continuum limit because several effects can
change together:

1. finite Fourier resolution;
2. finite physical domain;
3. periodic images of the defect;
4. represented lattice spacing;
5. defect width and normalization;
6. the difference between the full lattice dispersion and its quadratic band-edge
   approximation; and
7. spectral, state, and operator diagnostics.

The refinement campaign therefore asks a narrower question: after those controls are
varied independently, does the *declared finite sequence* satisfy a frozen,
multi-diagnostic comparison rule? This formulation deliberately avoids turning a
profile-broadening trend into an unsupported statement about changing lattice spaces or
an asymptotic limit.

## Represented parent and units

The accepted scalar hopping coefficients \(t_R\) define the dimensionless reduced-zone
dispersion

$$
E_{\mathrm{lat}}(k)=\sum_R t_R\exp(2\pi i kR).
$$

The lower band edge and quadratic coefficient are

$$
E_0=\sum_R t_R,
\qquad
\alpha=-\frac{1}{2}\sum_R(2\pi R)^2t_R.
$$

For the retained parent, the input records
\(\alpha=0.6519378386943853\,E_Ga_{\mathrm{ref}}^2\). Energies are expressed in
\(E_G\), lengths in the reference period \(a_{\mathrm{ref}}\), and all comparisons
use centered periodic Fourier modes ordered by increasing integer label. The energy
reference is the same declared lower edge in both routes.

This is a finite represented parent. The coefficients do not, by themselves, define a
material, a Kohn–Sham operator, a continuum operator, or an infinite-volume limit.

## Physical wave-number convention and changing lattice scale

On a periodic domain of length \(L\), Fourier mode \(m\) has physical reduced wave
number

$$
q_m=\frac{m}{L}.
$$

The parabolic comparator is

$$
E_{\mathrm{cont}}(q_m)=E_0+\alpha q_m^2.
$$

For represented lattice spacing \(a\), the lattice route uses

$$
E_a(q_m)=E_0+
\frac{E_{\mathrm{lat}}(a q_m)-E_0}{a^2}.
$$

The subtraction removes the common edge, and the factor \(a^{-2}\) preserves the
physical band-edge curvature while the represented lattice spacing changes. This is
the relevant scale sequence: \(a\) changes at fixed physical domain and fixed physical
profile. Merely widening a defect while holding \(a=a_{\mathrm{ref}}\) is a different
operation and is retained as a separate profile-family experiment.

The finite sequence \(a/a_{\mathrm{ref}}\in\{1,1/2,1/4,1/8\}\) can support a bounded
persistent-pass statement only. It does not prove convergence as \(a\to0\).

## Periodized defect profiles

For fixed integrated magnitude \(g=0.30E_Ga_{\mathrm{ref}}\), the analytical Fourier
coefficients of the periodized Gaussian are

$$
V_\ell=-\frac{g}{L}
\exp\!\left[-2\pi^2\sigma^2\left(\frac{\ell}{L}\right)^2\right].
$$

The fixed-peak family instead uses a peak depth \(V_0=0.12E_G\), corresponding to an
integrated magnitude \(V_0\sqrt{2\pi}\sigma\). These families must not be merged:

- fixed-integrated broadening redistributes a constant integrated strength; while
- fixed-peak broadening increases integrated strength and can increase the number of
  shallow bound states.

The continuum route uses analytical Fourier coefficients. The lattice route samples
the periodized real-space profile on lattice sites and transforms the diagonal site
potential into the same centered Fourier ordering. The two constructions therefore
exercise different numerical routes while meeting in an explicitly declared common
finite representation.

## Finite Hamiltonian construction

For each finite mode set, the continuum Hamiltonian is the diagonal parabolic parent
plus the convolution matrix generated by the analytical profile coefficients. The
lattice Hamiltonian is the scaled lattice dispersion plus the Fourier transform of the
sampled site-diagonal profile.

Both matrices are checked to be finite and Hermitian before diagonalization. The
workflow uses dense Hermitian eigensolves. If \(M\) is the represented dimension, this
requires \(O(M^2)\) storage and conventionally \(O(M^3)\) dense eigensolver work. The
campaign dimensions are frozen finite test inputs; the implementation does not infer
scientific adequacy from the fact that an eigensolve completes.

No matrix subtraction occurs until both represented Hamiltonians use the same finite
mode ordering, physical domain, energy unit, and energy reference. The signed operator
difference is

$$
D=H_a-H_{\mathrm{cont}}.
$$

Changing the order would change the sign of matrix elements, although the norm
criteria used here would remain nonnegative. The retained contract nevertheless fixes
the order so downstream interpretation is unambiguous.

## Why five refinement operations remain separate

### Continuum mesh

The mode counts \(64,96,128,192,256\) are varied at fixed
\(L=64a_{\mathrm{ref}}\), \(\sigma=2a_{\mathrm{ref}}\), and fixed-integrated
normalization. This isolates truncation of the Fourier representation for that fixed
finite-domain continuum problem.

### Continuum domain

The domain lengths \(L/a_{\mathrm{ref}}=32,48,64,96,128\) are varied at fixed spectral
spacing \(L/M=0.25a_{\mathrm{ref}}\) and fixed profile. Increasing both \(L\) and
\(M\) this way targets finite-domain and boundary-localization effects without
simultaneously coarsening the represented spectral spacing.

### Lattice supercell

The site counts \(N=32,48,64,96,128\) are varied at fixed
\(a=a_{\mathrm{ref}}\) and fixed profile. This targets periodic-image and finite
supercell effects in the represented lattice problem. It is not lattice-spacing
refinement.

### Lattice scale

The represented spacings \(a/a_{\mathrm{ref}}=1,1/2,1/4,1/8\) are varied at fixed
\(L=64a_{\mathrm{ref}}\), \(\sigma=2a_{\mathrm{ref}}\), and fixed-integrated
normalization. The site or mode count changes so the physical domain remains fixed.
This is the axis that tests the finite changing-scale comparison.

### Profile width

The widths \(\sigma/a_{\mathrm{ref}}=0.5,1,2,4,8,12\) are varied at fixed
\(a=a_{\mathrm{ref}}\) and \(L=128a_{\mathrm{ref}}\). Fixed-integrated and fixed-peak
normalizations are evaluated as separate families. This axis asks whether broadening a
profile on the original lattice makes every frozen comparison criterion pass; it is not
a substitute for the lattice-scale sequence.

## Spectral and localization diagnostics

A dense Hermitian eigensolve supplies ordered eigenvalues and eigenvectors. The campaign
retains the lowest-state energy, binding relative to \(E_0\), and the number of
eigenvalues below the edge by more than the declared margin. Count agreement matters
because a small lowest-state error can coexist with a different finite bound-state
spectrum.

For a normalized lowest state \(\psi\), a discrete inverse Fourier transform constructs
the corresponding periodic coordinate-space state. Boundary probability is the weight
at coordinate distances at least \(L/4\) from the profile center. It is a finite-domain
localization diagnostic, not an infinite-volume decay theorem.

## Gauge-invariant lowest-state comparison

Direct eigenvector subtraction is phase dependent. The campaign instead compares the
rank-one projectors of the two lowest states. If \(\psi_a\) and \(\psi_c\) are aligned
on compatible Fourier labels, their normalized fidelity is

$$
F=\frac{|\langle\psi_a,\psi_c\rangle|^2}
{\langle\psi_a,\psi_a\rangle\langle\psi_c,\psi_c\rangle},
$$

and the Frobenius distance between rank-one projectors is

$$
\lVert |\psi_a\rangle\langle\psi_a|
      -|\psi_c\rangle\langle\psi_c|\rVert_F
=\sqrt{2(1-F)}.
$$

The implementation clips roundoff-level excursions of \(F\) into \([0,1]\) before the
square root. This metric removes a global phase ambiguity but does not solve a
degenerate-subspace matching problem. The retained claim is therefore limited to the
lowest nondegenerate state.

## Operator and high-momentum diagnostics

Let \(P\) select the declared physical low-momentum sector
\(|q|\le0.25/a_{\mathrm{ref}}\). The campaign retains

$$
\lVert PDP\rVert_2
$$

as the compressed low-momentum discrepancy and

$$
\lVert PD(I-P)\rVert_2
$$

as a cross-sector coupling between the low sector and its represented complement. As
written, \(PD(I-P)\) maps complement inputs into low-sector outputs. Because \(D\) is
Hermitian, its adjoint \((I-P)DP\) maps in the opposite direction and has the same
spectral norm. The compressed norm is computed from the largest absolute Hermitian
eigenvalue of the compressed block; the cross norm from the largest singular value of
the rectangular cross block.

The lattice state's outer-Brillouin weight is

$$
\sum_{|aq_m|\ge0.25}|\psi_a(m)|^2.
$$

These diagnostics answer different questions:

- binding error tests one spectral quantity;
- bound-state count tests finite spectral multiplicity below the edge;
- projector defect tests the lowest-state subspace;
- compressed residual tests the operator discrepancy inside the intended low-momentum
  sector;
- cross residual tests cross-sector coupling between that sector and its complement;
  and
- Brillouin-edge weight tests whether the compared state occupies momenta where the
  quadratic approximation is least credible.

No one channel is accepted as a proxy for the others.

## Frozen numerical decisions

The support axes pass only when the final mesh, domain, or supercell steps meet the
thresholds fixed before evaluation. The exact protocol controls the normative values.
In summary:

- continuum mesh requires final binding change at most \(10^{-10}E_G\) and final
  projector defect at most \(10^{-6}\);
- continuum domain requires final binding change at most \(10^{-8}E_G\) and boundary
  probability at most \(10^{-8}\); and
- lattice supercell requires final binding change at most \(10^{-8}E_G\) and boundary
  probability at most \(10^{-8}\).

A lattice/continuum comparison point passes only if all six conditions hold:

| Channel | Frozen bound |
|---|---:|
| Relative binding error | \(10^{-3}\) |
| Lowest-state projector defect | \(10^{-2}\) |
| Compressed residual | \(10^{-3}E_G\) |
| Cross residual | \(10^{-3}E_G\) |
| Outer-Brillouin weight | \(10^{-4}\) |
| Below-edge count | Exact equality |

A lattice-scale boundary is the largest tested spacing for which that point and every
finer tested point pass. A profile-width crossover is the smallest tested width for
which that point and every broader tested point pass. This persistent-tail rule avoids
calling an isolated pass a boundary or crossover. Thresholds are not relaxed after
examining the result.

These thresholds are frozen campaign decisions, not universal physical constants or
validated material-acceptance tolerances.

## Retained bounded observations

The retained report states that the continuum-mesh, continuum-domain, and
lattice-supercell support axes pass their frozen criteria. For the fixed physical
profile, every criterion passes from \(a=0.5a_{\mathrm{ref}}\) through the finest tested
spacing \(a=0.125a_{\mathrm{ref}}\). The campaign therefore records a persistent bounded
lattice-scale pass beginning at the tested spacing \(0.5a_{\mathrm{ref}}\).

At \(a=a_{\mathrm{ref}}\), neither profile family establishes a crossover over the
tested width sequence. For sufficiently broad profiles, spectral and projector errors
can become small while the compressed parent-dispersion residual remains
\(3.78\times10^{-3}E_G\), above the frozen \(10^{-3}E_G\) criterion. The fixed-peak
family can additionally change the number of shallow bound states because its
integrated strength grows with width.

The scientific lesson is negative but informative: profile broadening can improve a
selected state-level comparison without eliminating the low-momentum operator mismatch
of the fixed-spacing parents. Conversely, a successful finite lattice-scale sequence
does not prove an asymptotic theorem.

## Independent verification strategy

The maintained runner and verifier intentionally use different construction routes.
The runner constructs the lattice matrix directly in Fourier coordinates. The verifier
instead:

1. authenticates the input payload, any retained implementation identity, and the
   three explicitly declared source-result identities without recursively following
   their provenance links;
2. assembles the scaled hopping operator in site coordinates;
3. adds the sampled site-diagonal defect;
4. transforms the complete lattice matrix into centered Fourier coordinates;
5. reconstructs the continuum matrix entry by entry;
6. repeats every eigensolve, projector comparison, operator partition, criterion, and
   boundary decision; and
7. recomputes canonical matrix content identities.

Canonical matrix digests round real and imaginary coordinates to
\(10^{-9}E_G\) only for stable content identity across independently ordered
floating-point operations. Numerical comparisons use unrounded matrices. Digest
agreement establishes quantized content identity, not exact real-number equality,
execution provenance, scientific validity, or acceptance.

Independence here is implementation independence within one declared synthetic model.
It is not independent experimental evidence or validation against a physical system.

## Error accounting

The result preserves the following categories rather than reporting one undifferentiated
"continuum error":

| Error or modeling channel | Controlling operation | What remains outside the claim |
|---|---|---|
| Fourier discretization | Continuum mode-count refinement | An arbitrary continuum function space or analytic discretization theorem |
| Finite domain | Continuum-domain refinement | An infinite-volume theorem |
| Periodic images | Lattice-supercell refinement | A universal image law |
| Represented lattice scale | Fixed-profile scale sequence | Proof of \(a\to0\) convergence |
| Profile model | Separate fixed-integrated and fixed-peak families | Equivalence of normalization families |
| Parent-operator approximation | Compressed and cross residuals | Unique attribution to one physical mechanism |
| Spectral behavior | Binding and below-edge count | Full spectral convergence |
| State behavior | Rank-one projector and edge weight | Degenerate or multiband subspace convergence |
| Floating-point reproducibility | Independent construction and quantized digests | Exact arithmetic or formal verification |
| Scientific adequacy | Not tested | Material validation, transferability, or UQ |

A small value in one row cannot discharge the others.

## Relationship to prior literature

The literature is used to motivate distinctions, not to transfer theorem conclusions to
this finite represented campaign:

- Koster and Slater (1954) provide historical finite-rank impurity context; available
  review access supports only a bounded methodological precedent.
- Hoefer and Weinstein (2011) and Duchêne, Vukićević, and Weinstein (2015) motivate
  explicit weak, slowly varying, near-band-edge scaling. Their hypotheses are not
  claimed for this synthetic finite parent.
- Nakamura and Tadano (2021) motivate explicit state-space identification and a declared
  lattice-spacing parameter in discrete-to-continuum reasoning. Their square-lattice
  norm-resolvent result is not reproduced here.
- König, Lee, and Hammer (2011) motivate treating finite-volume bound-state effects as
  a separate channel; the campaign measures its own one-dimensional periodic boundary
  diagnostic rather than importing their law.
- Kohn and Luttinger (1955) and Gamble *et al.* (2015) mark the multivalley and
  central-cell boundary relevant to semiconductor donor modeling. This campaign is
  scalar, synthetic, and not a silicon donor calculation.

Exact bibliographic identities, access levels, and claim limits are retained in
`docs/research/literature-reviews/impurity-defect-1d/source-register.md` and
`claim-to-source-matrix.md`.

## Reproducibility and protected-execution boundary

The authoritative protocol records commands for reproducing the synthetic calculation,
independent verification, plot, and checksum validation. Row-042 reconciliation does
not execute those commands or rewrite the retained files. No Quantum ESPRESSO or
Wannier90 execution is involved in this campaign or authorized by this documentation.

The exact row-042 encoded-document identities remain:

| Artifact | SHA-256 content identity |
|---|---|
| `input.json` | `55d647a8c259d3a1f1e5c756b496a9d1a16fee0a691c7b53d2f877da5f287fdd` |
| `result.json` | `1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc` |

These digests identify bytes only. See the [encoded-document module
dossier](encoded_documents/index.md) for ownership, import, evidence, and repository-root
boundaries.
