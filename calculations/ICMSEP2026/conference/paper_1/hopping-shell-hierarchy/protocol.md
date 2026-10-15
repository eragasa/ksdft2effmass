# Draft protocol: certified two-dimensional hopping-shell hierarchy

## 1. Status and evidence boundary

This is a **draft prospective protocol**. It is not frozen and has not been
executed. It reports no numerical result and does not establish a critical
hopping shell, compatibility, separation, material adequacy, scientific
validation, or uncertainty quantification.

The proposed calculation is local synthetic software and numerical
verification. It reuses a content-bound projection of the retained
square-lattice two-dimensional parent in
`calculations/research-monograph/periodic-2d/`. It executes no external
scientific calculator and makes no claim about silicon or another material.

Working identity:

`icmsep2026.paper1.periodic2d.hopping-shell-hierarchy.v1`.

Working planning label: **HSH-1** (hopping-shell hierarchy 1). It is not an
extension or amendment of sealed M3 evidence and does not renumber the separate
draft M4 common-space calculation.

## 2. Scientific question

For one fixed scalar periodic parent, one fixed spectral objective, one fixed
real-space operator objective, and one fixed pair of thresholds, define nested
model classes by increasing the allowed hopping support. The calculation asks:

> What is the smallest tested shell class for which one represented
> Hamiltonian satisfies both the spectral and operator criteria, and which
> smaller classes can be excluded by certified positive admissible-set
> separation?

The answer is meaningful only within the frozen hierarchy, parent, parameter
metric, sampling, weights, thresholds, and energy reference. It does not
identify a universal minimum interaction range.

## 3. Retained source parent

The intended source is the strongest-coupling member
\(\lambda_{xy}=0.30\) of the retained scalar square-lattice family

\[
H=-\nabla^2+0.5\cos x+0.5\cos y+0.30\cos x\cos y,
\]

with \(a=2\pi\), reciprocal scale \(G=1\), and energy scale \(E_G=1\).
The retained calculation uses a \(15\times15\) reciprocal transform mesh and a
separate \(31\times31\) withheld mesh.

The current source identities are:

| Source | Current SHA-256 | Intended role |
|---|---|---|
| `calculations/research-monograph/periodic-2d/input.json` | `82e9915101e755f7cc77cb8901478f88d878ffaa808732036631b7ae5cfd78ec` | source controls |
| `calculations/research-monograph/periodic-2d/result.json` | `4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6` | retained energies and hopping blocks |
| `calculations/research-monograph/periodic-2d/SHA256SUMS` | `4f18c5f8d548374bdb74c865ba3aaa37ecdd44862ee5bc49e3747db9f28d1205` | retained package boundary |

These hashes describe the current bytes; they are not a freeze record for the
new calculation. Before freezing HSH-1, the builder must verify the exact source
manifest entry for every consumed file and copy the required compact source
values into a self-contained generated input.

### 3.1 Exact symmetry projection

The source lowest-band hopping family is expected to obey Hermiticity, time
reversal, and square-lattice \(D_4\) symmetry up to binary64-scale defects. The
new input builder must:

1. reconstruct the complete \(15\times15\) finite hopping family;
2. measure raw Hermiticity, imaginary-part, and \(D_4\)-orbit defects;
3. fail if any defect exceeds a prospectively frozen source tolerance;
4. average each accepted orbit to produce one exact real \(D_4\)-symmetric
   scalar target; and
5. retain the projection defect separately.

All spectral targets used by HSH-1 are reconstructed from this exact symmetric
finite target. This prevents binary64 symmetry noise from deciding whether the
complete class has an exact common witness. The original direct-parent values
remain a separate withheld interpolation comparator.

The energy zero is fixed by subtracting the source-mesh average from the target
band. The same scalar shift is applied to every comparison and recorded; it is
not refitted separately by the spectral and operator channels.

## 4. One common maximal parameter space

Let the centered canonical representatives be

\[
\mathcal R_{\max}=\{(R_x,R_y):R_x,R_y\in\{-7,\ldots,7\}\}.
\]

Partition these representatives into \(D_4\) orbits. Associate one real hopping
coefficient \(\theta_o\) with each orbit \(o\), including the onsite orbit.
With orbit function

\[
\phi_o(\mathbf k)=\sum_{\mathbf R\in o}
 e^{2\pi i\mathbf k\cdot\mathbf R},
\]

the candidate scalar band is

\[
E_\theta(\mathbf k)=\sum_o\theta_o\phi_o(\mathbf k).
\]

The maximal parameter vector contains every orbit in
\(\mathcal R_{\max}\), in deterministic order by squared radius, then a frozen
integer representative. All shell classes are embedded into this same vector
space. An inactive orbit is fixed to zero; it is not deleted and the remaining
coordinates are not renormalized.

A compact coefficient box must be frozen before execution and must contain the
complete symmetric target with margin. The bound-selection rule may depend on
\(E_G\) and declared target coefficient scales but not on the eventual
admissible-set distances or desired figure shape. Booleans, strings, nonfinite
values, and nonpositive scales are rejected by strict decoding.

## 5. Nested shell classes

Use the already retained squared-radius sequence

\[
S=(0,1,2,4,8,18,50,98).
\]

Define

\[
\mathcal M_k=
\{\theta:\theta_o=0\text{ whenever }
\lVert\mathbf R_o\rVert^2>S_k\}.
\]

Thus \(\mathcal M_0\subset\cdots\subset\mathcal M_7\). Each class retains
complete \(D_4\) orbits and therefore preserves Hermiticity, time reversal, and
square symmetry by construction. This is an interaction-range hierarchy, not
an expansion of the orbital basis.

The complete class \(\mathcal M_7\) contains the exact symmetric finite target
and therefore supplies a predicted common witness. Whether an earlier class is
compatible is a confirmatory result, not a design assumption.

## 6. Frozen comparison channels

### 6.1 Spectral channel

The scalar spectral residual is linear in \(\theta\), so its squared loss is a
convex quadratic:

\[
L_E(\theta)^2=
\frac{1}{E_G^2\sum_{\mathbf k\in K_E}w_{\mathbf k}}
\sum_{\mathbf k\in K_E}w_{\mathbf k}
\left|E_\theta(\mathbf k)-E_{\rm ref}(\mathbf k)\right|^2.
\]

The spectral point set and every positive weight are part of the fixed problem
definition. They must be common to all shell classes. The intended design uses
the complete \(15\times15\) source mesh with a prospectively defined,
coordinate-based emphasis on the band-edge and symmetry-line region. All
weights remain positive so that the design matrix can be checked for full rank;
no weight may be fitted from hierarchy outcomes. Equal full-mesh weights are
not suitable for the primary experiment because Parseval equivalence would
make the spectral and operator reductions identical under matched objectives.

Before freeze, the exact weight formula and its physical interpretation must be
selected. The builder must retain both raw weights and normalized effective
weights. Common positive rescaling of all weights and \(\tau_E\) leaves the
admissible set unchanged; relative reweighting changes the scientific problem.

### 6.2 Operator channel

The operator target is the complete exact symmetric finite hopping family. Use
one global normalization and fixed positive per-block weights:

\[
L_H(\theta)^2=
\frac{1}{E_G^2\sum_{\mathbf R\in\mathcal R_{\max}}v_{\mathbf R}}
\sum_{\mathbf R\in\mathcal R_{\max}}v_{\mathbf R}
\left|t_\theta(\mathbf R)-t_{\rm ref}(\mathbf R)\right|^2.
\]

The primary proposal is equal weight per represented block. Orbit
multiplicities are therefore included explicitly rather than giving one equal
weight per free orbit. The operator comparison domain and normalization remain
identical for every class; they are not truncated to the class's active shell.
Otherwise omitted target content would disappear from the criterion as the
model class changed.

This rank-one real target has no internal gauge optimization. The state space,
energy zero, Fourier convention, and lattice representatives are fixed before
subtraction.

### 6.3 Admissible sets

For prospectively frozen positive thresholds \((\tau_E,\tau_H)\), define

\[
\mathcal A_{E,k}=\{\theta\in\mathcal M_k:L_E(\theta)\le\tau_E\},
\qquad
\mathcal A_{H,k}=\{\theta\in\mathcal M_k:L_H(\theta)\le\tau_H\}.
\]

Each set is the intersection of a convex quadratic sublevel set, the common
coefficient box, and the affine zero constraints defining \(\mathcal M_k\).
Producer and verifier must establish positive-semidefinite quadratic matrices,
active-coordinate rank, finite minima, and threshold feasibility independently.

If either channel set is empty, the class fails that criterion directly and no
finite inter-set distance is reported. The plot must show an explicit
`spectral-set-empty` or `operator-set-empty` disposition rather than treating
emptiness as positive separation. Certified positive distance is used only
when both sets are nonempty.

## 7. One metric across the hierarchy

Define a fixed orbit-multiplicity metric in the maximal coefficient space:

\[
d_{\rm red}(\theta,\theta')=
\left[
\frac{1}{E_G^2\,|\mathcal R_{\max}|}
\sum_o |o|\,|\theta_o-\theta'_o|^2
\right]^{1/2}.
\]

This is the normalized Frobenius distance between the two complete scalar
hopping families. The metric is independent of active parameter count and shell
radius. All classes use the restriction of this one metric; distances from
separately normalized parameter spaces must not be compared.

For nonempty channel sets,

\[
\delta_k^*=\inf_{\theta_E\in\mathcal A_{E,k},\,
                       \theta_H\in\mathcal A_{H,k}}
 d_{\rm red}(\theta_E,\theta_H).
\]

Because both admissible sets expand under the exact nested embedding,
\(\delta_{k+1}^*\le\delta_k^*\). This monotonicity is a semantic consequence of
the design, not an oracle for accepting computed values. Loose certified
intervals may overlap even when the exact distances are monotone.

## 8. Threshold design and freeze boundary

Threshold selection is a pre-execution human-owned design decision. Two honest
routes are allowed:

1. choose fixed dimensionless tolerances from the intended benchmark scale and
   accept empty, separated, unresolved, or compatible outcomes; or
2. inspect channel minima only in an explicitly exploratory design stage, then
   choose pedagogical thresholds intended to expose nonempty separated and
   compatible regimes, disclose that construction, reseal the final problem,
   and perform a distinct confirmatory evaluation.

The recommended route is the second, matching M3's transparent pedagogical
threshold design. Exploratory records must not be described as blind or
confirmatory. No distance bound, witness, withheld error, or plot styling may
be used to revise the sealed thresholds.

Before confirmatory execution, freeze:

- source identities and symmetry-projection tolerance;
- orbit ordering, coefficient box, and shell sequence;
- spectral weights and operator weights;
- \(\tau_E\), \(\tau_H\), and distance-resolution target;
- certificate method and numerical tolerances;
- training and withheld roles;
- figure axes and disposition vocabulary; and
- producer, verifier, test, and dependency identities.

## 9. Certified distance bounds

A multistart optimizer is not an incompatibility certificate. For each class
with two nonempty sets, retain both constructive and lower-bounding evidence.

### 9.1 Constructive upper bound

Any verified feasible pair gives

\[
\delta_k^*\le
\overline\delta_k=d_{\rm red}(\theta_{E,k},\theta_{H,k}).
\]

A verified common witness \(\theta_k\in\mathcal A_{E,k}\cap\mathcal A_{H,k}\)
establishes \(\delta_k^*=0\) exactly at the mathematical level. The verifier
must check both inequalities from reconstructed quadratics with outward
numerical tolerance; a small optimizer objective alone is insufficient.

### 9.2 Certified lower bound

The primary lower certificate uses a separating direction in the fixed metric.
For a declared covector \(u\), independently bound

\[
\alpha_{E,k}(u)=\min_{\theta\in\mathcal A_{E,k}}u^T\theta,
\qquad
\beta_{H,k}(u)=\max_{\theta\in\mathcal A_{H,k}}u^T\theta.
\]

If \(\alpha_{E,k}(u)>\beta_{H,k}(u)\), dual-norm geometry gives a positive
lower bound on \(\delta_k^*\). The producer may obtain a candidate direction
from a convex quadratically constrained optimization, but the standalone
verifier must reconstruct conservative support bounds with directed/outward
rounding. Replacing a box-clipped ellipsoid by an enclosing full ellipsoid is
allowed because it weakens rather than invalidates the lower bound.

A center-and-enclosing-radius triangle bound may be retained as an independent,
usually weaker certificate. A `certified-separated` disposition requires at
least one reconstructed lower bound to exceed the frozen resolution. Solver
termination, agreement of repeated starts, or failure to locate an intersection
is not enough.

The result reports intervals

\[
\underline\delta_k\le\delta_k^*\le\overline\delta_k,
\]

not point estimates unless the bounds coincide under the declared exact or
interval argument.

## 10. Training and withheld evaluation

Only the \(15\times15\) source-mesh objective defines quadratics, admissible
sets, thresholds, witnesses, bounds, the critical class, and dispositions.
After all such objects are fixed, evaluate retained witnesses and certificate
points on the disjoint \(31\times31\) direct-parent mesh.

Withheld outputs include:

- maximum and RMS spectral error;
- shell-resolved coefficient and omitted-tail diagnostics;
- exact source-mesh reconstruction defect;
- complete-class withheld interpolation floor; and
- whether withheld performance changes the interpretation without changing the
  training disposition.

The withheld mesh cannot alter weights, thresholds, class order, witnesses,
certificates, or the claimed minimum class. In particular, the known nonzero
full-shell withheld error remains reciprocal-mesh interpolation error rather
than hopping-shell inadequacy.

## 11. Critical-class decision

Let

\[
k_{\rm crit}=\min\{k:\mathcal A_{E,k}\cap\mathcal A_{H,k}\neq\varnothing\}.
\]

The disposition `minimum-tested-compatible-class-certified` requires:

1. an explicit verified common witness in \(\mathcal M_{k_{\rm crit}}\);
2. either certified positive separation or direct channel emptiness for every
   smaller class;
3. the exact nested embedding and common metric checks;
4. no unresolved smaller class; and
5. unchanged frozen controls throughout the hierarchy.

If a smaller class is unresolved, the result may state only that a compatible
witness was found at a particular shell. It may not call that shell minimal.
Once compatibility is established, larger nested classes are compatible by
embedding the same witness, but their independently computed diagnostics may
still be reported.

Allowed per-class dispositions are:

- `spectral-set-empty`;
- `operator-set-empty`;
- `certified-separated`;
- `compatible-common-witness`;
- `unresolved-nonempty`; and
- `invalid-premise`.

## 12. Independent verification

The standalone verifier must not import producer modules. It must strictly
decode source and result records and independently reconstruct:

- source correlation and exact symmetric target projection;
- \(D_4\) orbits, ordering, multiplicities, and shell masks;
- spectral and operator design matrices and analytic quadratics;
- channel minima and nonemptiness;
- the fixed maximal-space metric;
- every feasible point and common witness;
- every lower-bound support calculation;
- nested-class and monotonicity premises;
- source- and withheld-mesh evaluations; and
- figure data from result values.

Adversarial tests must alter source hashes, shell ordering, orbit
multiplicities, weights, thresholds, inactive coordinates, feasible points,
certificate directions, bounds, and withheld roles and must demonstrate
fail-closed behavior.

The producer and verifier may share NumPy/SciPy, floating-point behavior, and
mathematical conventions. Passing both establishes bounded software/numerical
agreement only.

## 13. Planned figure and manuscript integration

If accepted, the result replaces V2 Figure `fig:2d` rather than adding another
main-text figure.

The proposed figure has two panels:

1. certified \([\underline\delta_k,\overline\delta_k]\) intervals versus
   squared-radius shell, with distinct markers for empty, separated,
   unresolved, and common-witness cases; and
2. channel minima plus withheld spectral error for the same hierarchy, showing
   why admissible-set disposition and ordinary fit error are not interchangeable.

The existing parent-refinement, coupling-continuation, hopping-map, and shell
interpolation panels move to supplementary evidence. The M3 admissible-set
figure, composite gauge-locality figure, and silicon figures remain.

Main-text language must say "smallest tested compatible class under the frozen
problem definition," not "the physically minimal Hamiltonian" or "the required
shell range for two-dimensional materials."

## 14. Planned retained package

Before execution:

- `README.md`;
- `protocol.md`;
- editable configuration;
- deterministic input builder and canonical generated input;
- producer, typed records, and strict codecs;
- standalone verifier;
- software, numerical, adversarial, and artifact-correlation tests;
- source manifest; and
- prospective protocol-freeze record.

After one authorized local synthetic execution:

- `result.json`;
- `verification.json`;
- `standalone-verification.json`;
- `figure-data.csv`;
- `hopping-shell-hierarchy-summary.png` or vector equivalent;
- `report.md`;
- `software.json`;
- `source.sha256`; and
- `SHA256SUMS`.

No large scientific-calculator artifacts are needed. SHA-256 identifies bytes;
it does not establish semantic validity, chronology, or scientific acceptance.

## 15. Pre-freeze decisions still required

This plan deliberately leaves the following unresolved until their owning
review:

1. the exact positive spectral-weight formula;
2. coefficient-box construction and margin;
3. \(\tau_E\), \(\tau_H\), and the separation-resolution target;
4. the directed-rounding or interval implementation used by the standalone
   support-bound verifier;
5. whether classes with an empty channel remain in the primary figure or appear
   only in the supplement; and
6. final manuscript label and placement after the result is known.

These are design decisions, not calculated outcomes. Resolving them and
freezing the package does not itself authorize or establish the result.
