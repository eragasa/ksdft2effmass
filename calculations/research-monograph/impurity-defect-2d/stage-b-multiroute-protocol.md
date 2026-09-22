# Adopted multi-route Stage B execution-free protocol

## Status and authority

This document defines the adopted adversarial replacement for the blocked
single-route twist convention. The human response ``recommendation authorized``
resolved `RM-IMPURITY-DEFECT-2D-STAGE-B-TWIST-GAUGE-HC04` to the multi-route
data-complete execution-free option. The implementation does not read or execute
the accepted parent. A Stage B calculation still requires a separate exact
execution checkpoint and authorization record.

The design uses two independently constructed finite-matrix routes and one
explicit gauge bridge. The bridge is not a third estimate and routes are never
averaged, ranked, or voted. A disagreement is retained as a failed criterion.

## Shared represented problem

Both routes use the frozen spinless scalar $8\times8$ supercell, retained
hoppings with $R_x^2+R_y^2\leq18$, the Gamma and $(0.37,-0.23)$-turn twist
lifts, the central and off-axis $-0.25E_G$ point-onsite plants, the exact eight
$D_4$ operations, and the existing known-map attack. Matrix rows are source
sites and columns are target sites. Coordinates are reduced only after applying
an integer site map.

For a source $x=(x_1,x_2)$, retained hopping $R=(R_1,R_2)$, canonical target
$y$, and integer seam-crossing vector $q$, write

$$
x+R=y+Nq,
\qquad N=(8,8).
$$

This equation fixes the signs used by both finite-matrix constructors and the
gauge bridge.

## Route A: centred uniform-link representation

Route A retains the twist lift $\widetilde\phi$ in the centred componentwise
domain $[-1/2,1/2)$. Every $D_4$ image of the frozen generic twist remains in
that domain, so Stage B needs no integer reduction in this route.

The represented hopping is

$$
H_A(\widetilde\phi)_{x,y}
 =\sum_{R,q:\,x+R=y+Nq}
 h_R\exp\!\left[
 2\pi i\left(
 \frac{\widetilde\phi_1R_1}{N_1}
 +\frac{\widetilde\phi_2R_2}{N_2}
 \right)\right].
$$

For an isotropic $D_4$-covariant hopping inventory and the bare site
permutation $U_M|x\rangle=|Mx\bmod N\rangle$,

$$
H_A(M\widetilde\phi,Mp)
 =U_MH_A(\widetilde\phi,p)U_M^\dagger.
$$

The runner must build Route A directly from retained hops. It may not obtain
Route A by transforming Route B.

## Route B: reduced seam representation

Route B retains

$$
\bar\phi=\widetilde\phi\bmod1\in[0,1)^2
$$

and constructs seam phases directly:

$$
H_B(\bar\phi)_{x,y}
 =\sum_{R,q:\,x+R=y+Nq}
 h_R\exp(2\pi i\,q\cdot\bar\phi).
$$

This representation is periodic under integer changes of the twist metadata,
but bare site permutations move its seams. Define

$$
D(\widetilde\phi)|x\rangle
 =\exp\!\left[
 2\pi i\left(
 \frac{x_1\widetilde\phi_1}{N_1}
 +\frac{x_2\widetilde\phi_2}{N_2}
 \right)\right]|x\rangle
$$

and

$$
W_M(\widetilde\phi)
 =D(M\widetilde\phi)U_MD(\widetilde\phi)^\dagger.
$$

Then Route B tests

$$
H_B(M\widetilde\phi\bmod1,Mp)
 =W_M(\widetilde\phi)
  H_B(\widetilde\phi\bmod1,p)
  W_M(\widetilde\phi)^\dagger.
$$

Route B must be assembled from seam-crossing quotients. Constructing it by a
similarity transform of a retained Route A matrix is forbidden because that
would make the route comparison tautological.

## Gauge bridge

The two independently constructed matrices must satisfy

$$
H_B(\widetilde\phi\bmod1,p)
 =D(\widetilde\phi)
  H_A(\widetilde\phi,p)
  D(\widetilde\phi)^\dagger.
$$

The record retains the lift $\widetilde\phi$, reduced metadata $\bar\phi$, and
exact integer pair $n=\widetilde\phi-\bar\phi$. It never infers the lift from a
favorable matrix match.

For the known-map attack

$$
C_r=G H_rG^\dagger+cI,
$$

the attacked bridge is

$$
C_B-cI
 =B_G(C_A-cI)B_G^\dagger,
\qquad
B_G=G D(\widetilde\phi)G^\dagger.
$$

After each route applies its own known inverse and reference correction, the
recovered scalar onsite defects agree directly: the diagonal site gauge
commutes with a point-onsite projector. Raw matrices from different gauges are
never directly subtracted.

## Frozen inventories

Each matrix route retains the original 18 known-map cases: two central cases
and sixteen off-axis cases from two base twists and eight $D_4$ operations. The
proposal therefore contains 36 route-local known-map evaluations and 18 matched
cross-route comparison records.

Each route separately evaluates 512 Gamma candidates and 64 generic-twist
candidates. One schedule therefore has 1,152 blind candidate evaluations. Route
A uses direct comparison of centred lifts; Route B uses torus distance for
reduced twist metadata. Cross-route blind evidence requires equality of the
complete ordered ambiguity map identities, not merely the counts.

## Route order as an adversarial factor

The proposal does not assume that a correct finite operator physically depends
on software schedule. It instead treats order as a falsification factor capable
of exposing hidden mutable state. Two schedules run in separate fresh spawned
processes with identical immutable inputs:

1. Route A, then Route B, then the bridge; and
2. Route B, then Route A, then the bridge.

Neither schedule receives outputs, caches, matrices, inferred phases, ambiguity
sets, or diagnostics from the other. Within a schedule, the bridge runs only
after both route-local outputs exist. Retained serialization is always Route A,
Route B, bridge, so changing execution order cannot change record ordering.

Across both schedules the proposal contains 72 known-map route evaluations, 36
cross-route case records, and 2,304 blind candidate evaluations. The two
schedules yield 54 known-case order comparisons: 18 for Route A, 18 for Route B,
and 18 for the bridge. Six blind-summary comparisons cover both route-local
summaries and the bridge at the two twists.

A clean authored nearest-neighbour toy produced zero Route A and Route B
schedule differences and a $4.01\times10^{-16}$ bridge residual. An intentionally
invalid mutation let the first route write its twist representative into a
shared cache and forced the second route to consume it. That mutation produced
a Route A schedule difference of $0.7654$ and a bridge mismatch of $0.7654$ for
unit toy hopping, while the periodic seam route differed only at rounding level.
These values are synthetic software-test observations, not accepted-parent
Stage B evidence. They demonstrate that the order control is discriminating;
they do not establish that the correct calculation has an order effect.

Any clean schedule difference is retained as a software or protocol failure. It
is not interpreted as physical gauge dependence, and no schedule may be chosen
post hoc.

## Route-local and cross-route criteria

Both routes independently own:

- known-map recovery, support, amplitude, Hermiticity, and model residuals;
- defect and full-Hamiltonian covariance;
- the 512- and 64-map blind structured stops;
- median energy-shift diagnostics;
- pre-alignment, omitted-shift, fixed-twist, and information-boundary controls.

The bridge separately owns canonical, attacked, recovered-defect, spectral,
ambiguity-identity, and shift comparisons. The overall disposition is a pass
only if Route A, Route B, and bridge criteria all pass. A reproduced route-local
failure remains negative numerical evidence even when independent
reconstruction agrees.

## Independent verification

A future runner would enumerate Route A hops with uniform-link phases and Route
B hops with seam quotients. A verifier must not import that runner and would
instead:

1. reconstruct Route A from the shifted sampled dispersion and an independently
   assembled discrete Fourier transform;
2. reconstruct Route B from independently assembled seam-shift factors for each
   retained two-dimensional hopping;
3. construct $D$, $W_M$, integer lifts, and attack bridges from formulas;
4. reconstruct exact case and blind-map inventories; and
5. recompute criteria without using retained route-local matrices as oracles.

Spectral agreement cannot replace operator agreement, route agreement cannot
replace comparison with the compact plant, and a common digest can be asserted
only after the declared gauge conversion.

## Adverse controls and stops

Execution-free toy evidence must distinguish $D$ from $D^\dagger$, source from
target phase evaluation, raw lifts from reduced metadata, $U_M$ from $W_M$ in
Route B, direct seam construction from a transformed Route A matrix, and exact
ambiguity-map identity from count equality. It must also exercise a disconnected
hopping graph, which stops as `DEFECT_2D.PHASE_GRAPH_DISCONNECTED` before blind
candidate ranking.

A route disagreement, failed bridge, missing lift, disconnected phase graph,
changed inventory, nondiscriminating mutation, favorable route selection, or
attempted execution without later exact authority is a stop. No route is chosen
post hoc to rescue another.

## Scope limitation

The proposal verifies finite synthetic representations only. It does not make a
claim about twist-boundary continuity, directional or nonlocal defects,
finite-size convergence, composite spaces, spin, DFT, Wannier90, materials,
scientific validation, uncertainty quantification, or a general theorem of
gauge invariance.
