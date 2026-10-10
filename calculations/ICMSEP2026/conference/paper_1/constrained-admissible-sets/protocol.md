# Prospective M3 constrained-admissible-set protocol

## Status and scope

Status: **prospectively frozen before confirmatory execution**.

Calculation identity:
`icmsep2026.paper1.periodic1d.constrained-admissible-sets.v1`.

This protocol defines a local synthetic calculation. It evaluates bounded
numerical and software behavior for one finite rank-two model, one compact
parameter rectangle, two fixed threshold pairs, and a finite family of global
real rotations. It does not establish material validation, uncertainty
quantification, continuum convergence, arbitrary nonconvex alignment results,
or scientific acceptance. No external electronic-structure or localization
calculator is executed.

## Configuration and M2 composition

The human-readable source of scientific controls is `configuration.toml`.
`build_input.py` verifies the byte-level SHA-256 identity of
`../multiband-alignment/input.json`, embeds its decoded document as the exact M2
baseline, and emits canonical self-contained `input.json`. `input.json` is a
derived wire artifact and must equal `build_input.py --check` byte for byte.

M3 composes M2; it does not subclass or reinterpret it. The inherited M2
baseline fixes the parent hopping model, rank two, the 64-point training mesh,
the staggered 257-point withheld mesh, the transported frame construction, the
basis attack, and all baseline tolerances. The historical M1 name
“isolated-band” is not used as evidence of physical isolation here.

## Frozen candidate family

For each training point, let the M2 represented reference Hamiltonian be
\(H(k)\), let \(\bar E(k)=\operatorname{tr}H(k)/2\), and let the configured
model-energy scale be \(E_G=1\) in parent unit `1`. For
\(p=(s,\lambda)\), define

\[
H_p(k)=\bar E(k)I+sE_GI+\lambda\bigl(H(k)-\bar E(k)I\bigr).
\]

The parameter order is `(energy_shift_ratio, splitting_scale)` and the compact
domain is

\[
-0.25\le s\le0.25,\qquad 0.4\le\lambda\le1.2.
\]

The splitting scale is positive throughout the domain, so eigenvalue ordering
is preserved. The configured compatibility witness is exactly \((0,1)\).

## Comparison channels and alignment family

The spectral channel compares ordered eigenvalues and is invariant under frame
changes. The represented-operator channel compares matrices only after an
explicit one-global rotation. Its frozen family consists of the nine real
rotation angles

`[-1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2]` radians.

This finite family is not pointwise Procrustes recovery and is not an optimizer
over all continuous or nonconvex alignment maps.

For either channel, normalized RMS loss is

\[
L=\frac{\left(\sum_k\lVert\Delta H(k)\rVert_F^2\right)^{1/2}}
        {E_G\sqrt{N r}},\qquad r=2.
\]

The training losses are represented as analytic positive-definite quadratics
in \(p\). Centers, quadratic matrices, and minimum squared losses are retained.
The absolute quadratic-reconstruction tolerance is `1e-12`; the final
verification tolerance is `1e-11`.

## Admissible sets and cases

For a threshold pair \((\tau_S,\tau_O)\), the spectral admissible set is the
intersection of the spectral quadratic sublevel set with the compact parameter
domain. The operator admissible set is the union, over the finite global-angle
family, of each operator quadratic sublevel set intersected with the same
domain.

Two cases are frozen:

1. `compatible`: \(\tau_S=0.03\), \(\tau_O=0.33\). The confirmatory prediction
   is that the exact witness \((0,1)\), with a selected nonidentity global
   rotation, belongs to both sets.
2. `separated`: \(\tau_S=0.03\), \(\tau_O=0.31\). The confirmatory prediction
   is that finite-component certification establishes separation greater than
   the frozen resolution `0.05` in Euclidean parameter distance.

The compatibility claim is constructive: only a retained common witness proves
compatibility. Failed search alone would not prove incompatibility.

## Finite-component separation certificate

For the separated case, the certificate applies only to the frozen finite
global-angle family and its positive-definite, unclipped quadratic ellipsoids.
The producer and verifier:

1. determine which operator components are feasible on the compact domain by
   exact box-constrained quadratic minimization;
2. select a feasible spectral boundary point minimizing the splitting-scale
   coordinate;
3. for every feasible operator component, compute the boundary point maximizing
   that coordinate;
4. retain the largest operator extreme and use the coordinate gap as a certified
   lower bound; and
5. use the Euclidean distance between the two retained feasible boundary points
   as an upper bound.

Every retained certificate point must lie in the frozen domain and satisfy its
own channel threshold. A `certified-separated` disposition requires the lower
bound to exceed `0.05`; otherwise the disposition is `unresolved`. No claim is
made beyond these finite components or if clipping by the domain boundary would
invalidate the declared ellipsoid extreme.

## Training, withheld evaluation, and locality

Only the 64 training points define quadratics, admissible sets, feasible
components, witnesses, certificate points, bounds, and dispositions. The 257
staggered withheld points are reconstructed only after those objects are fixed.
They report evaluation losses and cannot alter any fitted or certified object.

For each retained evaluation point, complete discrete Fourier transforms of the
reference, attacked, and aligned-candidate represented Hamiltonians are formed.
Omitted-block \(\ell^2\) norms are retained for maximum ranges
`[0, 1, 2, 3, 4, 6, 8]`. These are diagnostics for this finite mesh and frame;
they are not general locality or compressibility guarantees. Spectral and
projector agreement alone does not protect finite-range tight-binding locality.

## Independent verification

`verify_result.py` imports no `ksdft2effmass` producer module. It strictly
decodes input and result fields and units; reconstructs the M2 fibers, frame
transport, attack, spectra, projectors, complete Fourier transforms, training
quadratics, withheld evaluations, locality diagnostics, feasible components,
compatibility witness, and separation certificate; and fails closed when the
maximum defect exceeds `1e-11`.

The independent verifier shares NumPy/SciPy, eigensolver behavior,
floating-point arithmetic, and mathematical conventions with the producer.
Passing it is therefore not an independent physical validation.

## Retained outputs and integrity

Confirmatory execution may create only:

- `result.json`;
- `verification.json`;
- `standalone-verification.json`;
- `figure-data.csv`;
- `constrained-admissible-sets-summary.png`;
- `report.md`; and
- `software.json`.

`protocol-freeze.json` binds the pre-execution protocol and implementation
inputs. `source.sha256` will bind exact source files used by execution, and
`SHA256SUMS` will bind retained package bytes. SHA-256 identifies bytes; it does
not by itself establish when they existed.
