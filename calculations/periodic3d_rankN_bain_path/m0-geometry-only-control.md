# Selected M0 geometry-only/frozen-response control

**Status: SELECTED SCIENTIFIC SUBPROTOCOL — NO CASE INVENTORY, CALCULATION, OR EXECUTION AUTHORITY**

This calculation-owned subprotocol closes the exact periodic-3D rank-N M0 parent,
representation, frozen-gauge, and zero-response semantics. It uses the selected
[`geometry-common-state-space.md`](geometry-common-state-space.md) path and the reviewed
fixed-geometry rank-N analytic family. It does not select ranks, circuit depths, attack
coefficients, reciprocal samples, fitted alignments, Fourier discretization, support,
tolerances, resources, visualization, lifecycle, or execution identity.

The control is a synthetic geometry test. It is not material strain, elasticity, phase
stability, martensitic physics, silicon, or material validation. Rank-two M0 supplies
vocabulary and composition only; its parent, parameters, outcomes, thresholds, and
evidence do not transfer.

## Human-selected parent boundary

The selected M0 parent is the shared `2r` flat specialization, not a distinct
retained-only parent. For any later admitted finite band-subspace rank \(r>1\), define

\[
 \xi_j=\frac{2j-r+1}{r-1},\qquad j=0,\ldots,r-1,
\]

and

\[
 D^-_{r,0}=\operatorname{diag}(0.4\xi_0,\ldots,0.4\xi_{r-1}),
 \qquad
 D^+_{r,0}=\operatorname{diag}(3.0+0.3\xi_0,\ldots,3.0+0.3\xi_{r-1}).
\]

The full parent and retained seed are

\[
 H^{\mathrm{M0}}_r
 =\operatorname{diag}(D^-_{r,0},D^+_{r,0})
 \quad\text{on}\quad
 \mathbb C^{2r}=\mathbb C^r_{\mathrm{ret}}\oplus\mathbb C^r_{\mathrm{ext}},
 \qquad
 F_0=\begin{bmatrix}I_r\\0\end{bmatrix}.
\]

This is exactly the fixed analytic parent's parameter-free `lambda=0` specialization.
It has no residual `lambda` input or inventory in M0. It is independent of reduced
coordinate \(q\), path coordinate \(s\), and the direct metric. Selecting this
specialization does not adopt the fixed-geometry study's rank, depth, attack-coefficient,
mesh, or tolerance inventories.

The ambient parent dimension is `2r`; the represented band-subspace rank is `r`. The
retained sector is an exact invariant eigenspace, not a numerical or approximate
model-reduction output. Numerical rank, circuit depth, and any future genuine
model-reduction retained rank remain separate quantities.

## Spectrum, energy, and isolation certificate

The energy unit is the same dimensionless unit as M1N, the energy zero is fixed, and
`norm_energy_scale=1`. The retained energies are the strictly ordered simple values

\[
 -0.4=0.4\xi_0<\cdots<0.4\xi_{r-1}=0.4,
\]

and the exterior energies are the strictly ordered simple values

\[
 2.7=3.0+0.3\xi_0<\cdots<3.0+0.3\xi_{r-1}=3.3.
\]

Thus every displayed eigenvalue has multiplicity one for finite \(r>1\), and the exact
retained-to-exterior isolation certificate is

\[
 \min_j(D^+_{r,0})_{jj}-\max_k(D^-_{r,0})_{kk}=2.7-0.4=2.3.
\]

The lower bound `2.3` is an analytic consequence of the selected formulas, not a
calculated result, convergence statement, material gap, or transferable M1N outcome.

## Frozen reduced-coordinate gauge action

Let \(\mathcal B_B\) be the exact oriented six-bond inventory selected in
[`geometry-common-state-space.md`](geometry-common-state-space.md). Its bond-RMS
normalization is

\[
 N_{\mathcal B_B}=\sqrt{\frac{2}{|\mathcal B_B|}}=\frac{1}{\sqrt3}.
\]

For each later admitted circuit depth \(L\) and attack coefficient \(A\), retain the
fixed-geometry right-acting alternating real Givens circuit. For layer
\(\ell=1,\ldots,L\),

\[
 s_{\mathcal B_B,\ell}(q)
 =N_{\mathcal B_B}\sum_{b\in\mathcal B_B}
 \left[\frac34\sin(2\pi q\cdot b)
 +\frac14(-1)^\ell\sin(4\pi q\cdot b)\right].
\]

For adjacent-pair index \(p=1,\ldots,r-1\),

\[
 w_{r,p}=\frac{1+0.15(2p-r)/(r-1)}{1.15},
 \qquad
 \theta_{\ell,p}(q)
 =A(-1)^{\ell+p}w_{r,p}s_{\mathcal B_B,\ell}(q).
\]

Odd layers act on zero-based pairs `(0,1), (2,3), ...`; even layers act on
`(1,2), (3,4), ...`. On an active pair, the Givens block is

\[
 \begin{pmatrix}
 \cos\theta&-\sin\theta\\
 \sin\theta&\cos\theta
 \end{pmatrix}.
\]

The ordered layer product \(G_{r,L,\mathcal B_B}(q;A)\in SO(r)\) acts from the right.
It is smooth, periodic on the reduced reciprocal torus, and has the exact known inverse
\(G^\dagger\). The full ambient basis action is

\[
 W_{r,L}(q;A)=G_{r,L,\mathcal B_B}(q;A)\oplus I_r.
\]

The subprotocol selects this action formula and bond-RMS normalization but no values or
inventories for \(r\), \(L\), or \(A\). Once a case is admitted, its \(r\), \(L\), and
\(A\) are held fixed for every \(s\in[0,1]\); no path-dependent refit,
renormalization, depth change, or bond-sign canonicalization is permitted.

## Represented operator family

The attacked retained frame and retained operator are

\[
 F^{\mathrm{M0}}_{r,L}(q,s;A)
 =F_0G_{r,L,\mathcal B_B}(q;A),
\]

\[
 \widetilde D^{\mathrm{M0}}_{r,L}(q,s;A)
 =G_{r,L,\mathcal B_B}(q;A)^\dagger
 D^-_{r,0}
 G_{r,L,\mathcal B_B}(q;A).
\]

The full represented parent is

\[
 \widetilde H^{\mathrm{M0}}_{r,L}(q,s;A)
 =W_{r,L}(q;A)^\dagger H^{\mathrm{M0}}_r W_{r,L}(q;A).
\]

None of these right-hand sides depends on \(s\). M0 and M1N share the ordered
\(\mathbb C^r_{\mathrm{ret}}\oplus\mathbb C^r_{\mathrm{ext}}\) state space, energy unit,
energy zero, normalization, common Bain cell labels, basis offsets, and oriented bond
inventory. They remain scientifically distinct: M0 uses the flat `lambda=0` parent as a
geometry-only control, while M1N retains the subsequently admitted fixed analytic parent
case, which need not be flat.

## Same-strain and cross-strain operands

At one path point, the exact representation-equivalence operands are
\(D^-_{r,0}\) in the reference retained basis and
\(\widetilde D^{\mathrm{M0}}_{r,L}(q;A)\) in the attacked retained basis, with the declared
frame map \(G\). Expressed in the reference basis,

\[
 G\widetilde D^{\mathrm{M0}}G^\dagger=D^-_{r,0},
\]

and the ordered spectra agree exactly. This analytic identity does not select a fitted
alignment inventory or tolerance. Any future identity, global, pointwise, or
known-inverse diagnostic must remain separately labelled and use its selected operands.

For any \(s_0,s_1\in[0,1]\), pull both operators into the common Bain cell/state space
selected by the geometry subprotocol. At fixed reduced \(q_B\),

\[
 H^{\mathrm{M0}}_r(s_1)-H^{\mathrm{M0}}_r(s_0)=0,
\]

\[
 \Delta\widetilde D^{\mathrm{M0}}_s(q_B;s_1,s_0)
 =\widetilde D^{\mathrm{M0}}(q_B,s_1)
 -\widetilde D^{\mathrm{M0}}(q_B,s_0)=0,
\]

and likewise \(\Delta\widetilde H^{\mathrm{M0}}_s=0\). These are exact analytic
common-coordinate identities. A nonzero aligned M0 path response is a
numerical/state-identification failure, not physical response. The statement compares a
fixed point of the abstract reduced reciprocal torus; it does not claim that the
corresponding Cartesian wave vector is fixed as the metric changes.

## Frozen and metric-varying quantities

The following are frozen for an admitted M0 case:

- the full `2r` parent, ordered retained/exterior basis, retained seed, energy zero,
  dimensionless unit, `norm_energy_scale=1`, multiplicities, and analytic gap;
- the oriented bond inventory, reduced basis offsets, admitted \(r\), \(L\), and \(A\);
- the right-acting gauge circuit, layer order, bond-RMS normalization, known inverse, and
  common reduced-coordinate represented operator; and
- every exact reduced-coordinate Fourier coefficient and translation label of the
  attacked represented field.

Only geometry-derived quantities may vary with \(s\):

- the direct metric, reciprocal basis, and Cartesian wave vector associated with fixed
  reduced \(q_B\);
- physical bond vectors and lengths;
- basis-aware displacement vectors and lengths;
- equality, ordering, and multiplicity of complete physical-metric shells; and
- physical radii and block counts after a future support/reporting policy is selected.

A changed shell or physical-radius description is a metric effect. It is not operator,
parent-model, numerical, or material response. A shell index may not be transferred
between path points as if it were a fixed physical radius.

## Independent analytic reference obligations

A future producer-independent M0 reference must reconstruct the formulas in this file
without calling the eventual M0 producer and must establish:

1. the `2r` direct-sum state space, seed, simple retained/exterior spectra, fixed energy
   conventions, and exact `2.3` isolation certificate;
2. absence of \(q\), \(s\), and metric dependence in the unrepresented parent;
3. the exact oriented-bond sine harmonics, bond-RMS normalization, layer pairing,
   Givens sign convention, right action, \(SO(r)\) property, and known inverse;
4. \(F=F_0G\), \(\widetilde D=G^\dagger D^-G\),
   \(\widetilde H=W^\dagger HW\), Hermiticity, and exact ordered-spectrum equivalence;
5. same-strain recovery \(G\widetilde DG^\dagger=D^-\) without a fitted alignment;
6. exact cross-strain equality after the selected common-cell/state pullback;
7. equality of every reduced-coordinate Fourier coefficient at any two path points; and
8. confinement of all allowed path dependence to the selected metric-derived physical
   geometry quantities.

A later finite Fourier reference may verify discretized transform mechanics only after a
mesh and convention are selected. It must not replace the analytic invariance proof or
turn a finite-sample equality into a continuum claim.

## Typed unresolved and inapplicable boundary

A future typed qualification must distinguish at least:

- `M0_PARENT_RANK_INVALID`;
- `M0_PARENT_MULTIPLICITY_FAILED`;
- `M0_ENERGY_CONVENTION_MISMATCH`;
- `M0_EXTERNAL_GAP_CERTIFICATE_FAILED`;
- `M0_GAUGE_ACTION_UNRESOLVED`;
- `M0_COMMON_STATE_SPACE_MISMATCH`;
- `M0_SAME_STRAIN_EQUIVALENCE_FAILED`;
- `M0_FROZEN_OPERATOR_IDENTITY_FAILED`;
- `M0_FOURIER_INVARIANCE_FAILED`; and
- `M0_METRIC_ONLY_BOUNDARY_VIOLATED`.

These are scientific failure distinctions, not a source enum or wire-schema selection.
Before a rank/depth/attack case is admitted, its case result is
`INAPPLICABLE_NO_ADMITTED_M0_CASE`. Before a fitted alignment, mesh/Fourier transform,
or support/reporting policy is selected, the corresponding derived diagnostic is
`INAPPLICABLE_POLICY_NOT_SELECTED`; it must not be emitted as zero. A failed common-cell
or finite-quotient qualification retains the applicable typed geometry reason from
`geometry-common-state-space.md` and makes the corresponding operator comparison
`unresolved`.
