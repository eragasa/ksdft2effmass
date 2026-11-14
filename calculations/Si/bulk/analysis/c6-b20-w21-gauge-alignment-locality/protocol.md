# C6-B20-W21 Hamiltonian gauge-alignment/locality protocol

## 1. Scientific question

For the authenticated finite rank-10 `C6-B20-W21` Wannier Hamiltonian, quantify which
properties remain invariant and which representation costs change under one frozen
momentum-dependent internal unitary.

The primary questions are:

1. Does the attack preserve Hermiticity and the complete represented spectrum at every
   declared construction and evaluation coordinate?
2. How much mismatch remains under identity and one-global-unitary alignment?
3. Do pointwise polar recovery and the known inverse restore the reference represented
   Hamiltonian within their declared numerical tolerances?
4. How does the attack redistribute finite Fourier-block power over physical-metric
   complete supports?
5. Across the complete support-error curves, how do the reference and attacked
   representations differ at equal attained Hamiltonian and sorted-band accuracy?
6. Can direct-parent representation error, conversion, interpolation, deliberate
   truncation, and total finite-model consequences remain separately attributable?

The experiment concerns representation efficiency of a DFT-derived finite operator. It
does not test physical inequivalence of the complete gauge-related fields.

## 2. Source and evidence roles

### 2.1 Fixed represented source

The source is the full untruncated provider-eligible rank-10 `C6-B20-W21` operator
qualified by S30. A frozen request must bind at least:

- the accepted direct lattice and reciprocal convention;
- the C6 ordered construction mesh;
- retained rank 10;
- the native energy unit and energy-reference identity;
- authenticated HR, `u`, `u_dis`, and required Wigner--Seitz-vector identities;
- S30 structural reconstruction and Hermiticity evidence; and
- the exact maintained implementation and dependency identities used to adapt the
  source.

The source operator remains scientifically limited by the S40 revealed-parent result.
Its use here does not reverse that disposition.

### 2.2 Construction coordinates

The construction inventory is the Gamma-origin `6 x 6 x 6` C6 mesh. The native
Wannier90 list uses coordinates `0, 1/6, ..., 5/6` on each axis. Before the centered
finite transform, the adapter must wrap and reindex that inventory to the exact axis
`(-1/2, -1/3, -1/6, 0, 1/6, 1/3)`, corresponding to centered-mesh offset
`(0.0, 0.0, 0.0)`. The frozen request must retain the native-to-centered permutation and
must not silently use the synthetic half-step offset `(0.5, 0.5, 0.5)`. The direct
represented Hamiltonian on this mesh is reconstructed through the authenticated native
HR/Wigner--Seitz route before adaptation to the generic field boundary.

### 2.3 Evaluation coordinates

The primary development evaluation inventory is the exact revealed 408-point geometry.
Its manifest assigns the same weight `1/408` to every point, so normalized weighted-RMS
channels coincide with equal-point RMS channels; the frozen request must authenticate
that weight inventory rather than infer it. The ordered point list is admitted directly
as the represented-field evaluation inventory; it is not padded into or replaced by a
tensor grid. The direct represented target is the full native-route `H_W(k)` evaluated
at those coordinates. The direct-parent eigenvalues form a separate labeled overlay and
are not an operator target in the retained Wannier coordinates.

The frozen 402-point confirmation geometry and all future parent values on it are
excluded from request construction, attack selection, thresholds, support selection,
analysis, and verification.

## 3. State-space and coordinate contract

All matrix subtraction in the generic analysis occurs in one declared retained
coordinate space `C^10` with:

- basis identity fixed to the authenticated `C6-B20-W21` Wannier coordinate order;
- one energy-reference identity and one physical energy unit;
- one right-handed direct lattice and associated physical metric;
- construction and evaluation coordinates expressed in the same reduced reciprocal
  convention; and
- identity reference frames in the retained coordinate space.

The identity frames do not claim that off-mesh raw DFT eigenvectors or Wannier90
`u_dis @ u` matrices have been reconstructed. The source subspace and native gauge are
qualified upstream; this experiment applies a controlled internal coordinate change to
the admitted represented Hamiltonian.

## 4. Frozen attack

The authorized prospective attack is one immutable
`Periodic3DRankNGivensGaugeTransformation` with:

- retained rank `10`;
- circuit depth `2`;
- layer 1 pairs `(0,1)`, `(2,3)`, `(4,5)`, `(6,7)`, `(8,9)`;
- layer 2 pairs `(1,2)`, `(3,4)`, `(5,6)`, `(7,8)`;
- harmonic bonds `(1,0,0)`, `(0,1,0)`, `(0,0,1)` in that order;
- normalization `axis-maximum`;
- coefficient `pi/8`, whose binary64 value is `0x1.921fb54442d18p-2`;
- conservative angle upper bound `pi/8`; and
- attack identity
  `ksdft2effmass.periodic3d-rankN-alternating-givens-attack.v1:r10:L02:axis-maximum:bonds-1,0,0;0,1,0;0,0,1:coefficient-0x1.921fb54442d18p-2`.

This is the established middle nonzero synthetic control, selected before inspecting
any silicon locality, truncation, or support outcome. Its maximum sampled angle,
unitarity defect, periodicity, and reciprocal-boundary consistency are verification
channels.

Changing any attack coordinate defines a new request identity rather than a retry.

## 5. Alignment channels

For reference field `H(k)` and attacked field

```math
A(k) = G(k)^\dagger H(k) G(k),
```

retain these distinct channels:

1. **identity** — compare `A(k)` and `H(k)` without recovery;
2. **global unitary** — fit one momentum-independent complete unitary over the declared
   construction inventory;
3. **pointwise polar** — reconstruct one complete-unitary polar action independently at
   every coordinate from the declared frames; and
4. **known inverse** — apply the exact generating inverse supplied by the attack.

The pointwise and known-inverse channels are oracle controls. Agreement between them
checks conventions and implementation; it is not evidence that the generating inverse
could be discovered from an unknown material target.

Freeze the established software-control tolerances:

- Procrustes rank-cutoff rule: `maximum`;
- Procrustes absolute rank cutoff: `1e-12`;
- Procrustes relative rank cutoff: `1e-10`;
- Procrustes absolute validation tolerance: `1e-12`;
- Procrustes relative validation tolerance: `1e-10`;
- transport absolute rank cutoff: `1e-10`; and
- transport relative rank cutoff: `1e-12`.

A deficient pointwise or global overlap fails closed; no implicit null-space completion
is admitted. Changing any cutoff or validation tolerance defines a new request identity.

## 6. Fourier and support routes

### 6.1 Centered finite-cyclic transform

Apply the declared normalized three-dimensional finite transform to the complete
construction field. Retain the centered cyclic displacement inventory and verify:

- field reconstruction on every construction coordinate;
- cyclic block Hermiticity;
- Parseval consistency; and
- independent transform reconstruction.

### 6.2 Ordinary-lattice conversion

Before physical-support truncation, remove or otherwise explicitly disposition every
centered representative lacking an ordinary integer-lattice conjugate partner. The
multidimensional even-mesh Nyquist boundary must be encoded explicitly. Conversion
power remains separate from deliberate truncation power and from spectral error.

### 6.3 Complete physical-metric block supports

After ordinary conversion, each displacement component belongs to
`{-2, -1, 0, 1, 2}`, giving the full 125-block ordinary inventory. For the accepted FCC
primitive direct basis and lattice parameter `a = 5.469182093640207 angstrom`, freeze

```text
shell_metric_scale = 4 / a^2
                   = 0x1.11ded5e27f418p-3
```

so the integer metric label of displacement `(n1,n2,n3)` is

```text
q = 2 * (n1^2 + n2^2 + n3^2 + n1*n2 + n1*n3 + n2*n3).
```

The full ordinary inventory has maximum label `q = 48`; therefore freeze the reusable
shell cap at `48`. The ordered support inventory is the ascending sequence of distinct
attained labels, with each support containing every represented displacement whose
label is no larger than its boundary. Every support is inversion complete. Support
identity includes the exact displacement inventory, physical radius
`sqrt(q / shell_metric_scale)`, and retained block count, not merely the integer label.

These are lattice-block supports for the complete rank-10 matrices `T_R`. They are not
orbital-center-resolved individual matrix-element distances and make no atomic-orbital
locality claim.

The attacked representation receives its own transformed block coefficients on this
same frozen displacement inventory. The native S90/S100 Wigner--Seitz shells are a
separate fixed-gauge comparator and do not define the finite-cyclic attacked supports
automatically.

## 7. Error channels

For reference and attacked representations, retain maximum and weighted-RMS raw errors
in electron-volts together with normalized channels using the frozen reporting scale
`1.0 eV`. The matrix normalization is `sqrt(10) * 1.0 eV`; the sorted-band maximum is
normalized by `1.0 eV`, and the sorted-band L2 RMS by `sqrt(10) * 1.0 eV`. This reporting
scale is not an acceptance threshold. Retain matrix Frobenius and sorted-band channels
separately. For each finite support report:

1. **conversion** — cyclic-to-ordinary block power removed by representation change;
2. **interpolation** — full ordinary finite interpolant relative to the direct native
   represented target on the 408-point inventory;
3. **deliberate truncation** — truncated ordinary model relative to its full ordinary
   finite interpolant;
4. **represented total** — truncated ordinary model relative to the direct native
   represented target; and
5. **direct-parent overlay** — sorted candidate bands relative to the revealed direct
   parent, reported only after the internal represented-field results are fixed.

Separately maximized or RMS channels are not added. Cancellation or reinforcement is
retained as observed behavior rather than hidden in an additive budget.

## 8. Support curves without acceptance thresholds

The first retained development request freezes the complete ordered ordinary-support
inventory and sets the reusable policy's `band_tolerances` inventory to empty. It does
not invent Hamiltonian or sorted-band acceptance thresholds after the earlier silicon
truncation study explicitly declined to establish them.

For every complete support and both representations, report:

- exact displacement inventory and physical-radius identity;
- retained block count;
- matrix maximum and RMS errors;
- sorted-band maximum and L2-RMS errors;
- omitted block power; and
- predecessor and successor support identities when present.

Compare the two complete support-error curves using Pareto dominance and
**equal-attained-error** statements: for an error value actually attained by one frozen
support, identify the minimum support of the other representation that attains no larger
error. Such comparisons are descriptive curve projections, not post-hoc acceptance or
reduction decisions. Matrix and sorted-band projections remain separately named.

A future study may add first-passing decisions only after an externally justified target
inventory is frozen prospectively. No direct-parent target may choose supports or
thresholds in this development experiment.

## 9. Producer checks and assurance status

This development version does not require an independent reconstruction path. The
producing analysis must retain and check:

- authenticated source identities and declared metadata;
- direct native-route represented fields on both coordinate inventories;
- attack matrices, inverse actions, and unitarity;
- complete-field spectral equivalence;
- identity, global, pointwise, and known-inverse alignment results;
- centered cyclic blocks and construction reconstruction;
- ordinary conversion and physical support inventories;
- interpolation, truncation, represented-total, and direct-parent-overlay channels;
- complete support-error curves, Pareto comparisons, and every equal-attained-error
  projection; and
- every value admitted into a table or figure.

Plot generation may consume the authenticated producer result directly. Every result,
table, and figure must be labeled
`producer-checked-development-analysis-not-independently-verified`. This reduced
assurance is an explicit scope decision, not evidence of independent numerical
verification. A later publication-qualified result may add independent reconstruction
without changing the identity of this development result.

## 10. Result status and allowed claims

A successful development result may support statements of the form:

> Within the authenticated finite `C6-B20-W21` represented Hamiltonian and declared
> rank-10 internal gauge transformation, complete spectra agree while restricted alignment,
> finite Fourier-block distributions, and equal-accuracy support requirements differ.

It may not support:

- acceptance of the source as an adequate silicon Hamiltonian;
- validated silicon gap, valley, or effective masses;
- a universal gauge-locality law;
- continuum or infinite-mesh convergence;
- atomic-orbital or Slater--Koster semantics;
- physical inequivalence of complete gauge-related fields; or
- transfer of development status to publication-qualified evidence.

## 11. Execution and authorization boundary

The 2026-11-02 retained no-calculator analysis and nine-figure rendering were explicitly
authorized after reporting their executable scope, authenticated inputs, outputs, and
expected resources. The retained execution invoked no calculator. Any additional
retained analysis requires a new bounded authorization. Quantum ESPRESSO,
`pw2wannier90.x`, and Wannier90 execution remain outside this protocol and require their
own explicit protected-action authorization.
