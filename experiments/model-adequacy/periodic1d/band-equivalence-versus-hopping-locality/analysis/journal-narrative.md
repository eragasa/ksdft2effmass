# Journal narrative

## Suggested Results text

### Spectral equivalence does not determine hopping locality

We first isolate the distinction between band equivalence and representation-dependent
locality in the normalized two-state continuum. The parent matrix field is
$K(q)=\sigma_z$, and the comparison family is
$A_a(q)=R[a\sin(2\pi q)]^{\mathsf T}K(q)R[a\sin(2\pi q)]$ for
$0\leq a\leq\pi/4$. Because this construction is an orthogonal similarity at every
$q$, the two eigenvalues remain $-1$ and $+1$ throughout the Brillouin zone. The largest
computed band defect over the tested amplitude and momentum grids was
$2.22\times10^{-16}$ [Fig. 1(d)]. The conventional band structure therefore cannot
distinguish the parent and comparison representations. If the generating
momentum-dependent rotation is admitted as the state-space identification, the two
fields represent the same abstract operator. The comparison below instead permits only
one momentum-independent real rotation and therefore measures a restricted-alignment
representation error.

The representation-aware thresholds nevertheless increase continuously with rotation
amplitude [Fig. 1(a)]. In normalized units, the independently minimized operator
threshold is $[1-J_0(2a)^2]^{1/2}$, whereas simultaneous enforcement of the exact
spectrum and operator constraints requires $[2(1-J_0(2a))]^{1/2}$. Both thresholds have
the same small-amplitude slope, but they separate as the rotation grows. At
$a=\pi/4$, the two values are $0.8815978972$ and $1.0276174232$, respectively. Their
separation shows that exact band agreement does not remove the matrix-level cost under
the declared restricted identification.

The same mismatch appears in real-space locality. At $a=0$, all weight outside the
onsite block is below $1.3\times10^{-28}$ on the $N=512$ transform. The total non-onsite
weight rises to $0.2747231$ at $a=\pi/8$ and $0.7772149$ at $a=\pi/4$. The cumulative
tails decay rapidly with retained range, but their amplitude dependence is pronounced
[Fig. 1(c)]: the weight outside $|R|\leq4$ is $1.16\times10^{-8}$ at $a=\pi/8$ and
$1.03\times10^{-5}$ at $a=\pi/4$. The range-resolved map [Fig. 1(e)] confirms that the
support broadens continuously even though the bands remain unchanged. Thus, for this
family, band equivalence coexists with both a nonzero restricted-alignment matrix
mismatch and an extended hopping representation.

The numerical study also separates momentum and amplitude resolution. Refinement from
$N=32$ through $N=512$ changes all monitored momentum-dependent quantities only at
approximately binary64 roundoff. By contrast, the proposed uniform amplitude ladder
through $N_a=64$ is insufficient to reconstruct a continuous threshold curve at the
draft $1.01\times10^{-8}$ level [Fig. 1(b)]. Its maximum midpoint interpolation defects
are $3.08\times10^{-5}$ and $1.41\times10^{-5}$ for the operator and joint thresholds.
The observed second-order decay places the first tested passing uniform grid at
$N_a=4096$. This does not imply that every calculation requires 4096 amplitudes: the
analytic flat-parent thresholds can be evaluated directly, while a non-analytic model
should use a reviewed adaptive refinement rule rather than infer convergence from shared
nested nodes alone.

This benchmark establishes the mechanism and verifies the implemented flat-parent
channels; it does not exercise the prospective admissible-set, witness, or separation
workflow and does not establish material realism. The parent is deliberately flat and
the $N=512$ hopping blocks remain finite-mesh Fourier coefficients. An initial non-flat
four-state realization now exists, but its momentum and amplitude controls remain
`unresolved`. A qualified non-flat calculation and a retained, protocol-frozen run are
still required before the family can serve as final publication evidence.

## Suggested figure caption

**Figure 1. Band equivalence versus hopping locality in the smooth flat-parent
continuum.** **(a)** Normalized minimum operator and exact-spectrum joint acceptance
thresholds as functions of the maximum rotation amplitude $a$. **(b)** Maximum
midpoint defect of piecewise-linear interpolation on nested uniform amplitude grids;
the shaded region marks the proposed $N_a=8$--64 ladder, and the dotted line is the
draft $1.01\times10^{-8}$ unit-scale target. **(c)** Cumulative normalized hopping
weight outside the retained range $|R|\leq R_{\max}$ for two amplitudes.
**(d)** Reference and transformed Bloch bands; the largest computed eigenvalue defect
is $2.22\times10^{-16}$. **(e)** Normalized range-resolved hopping weight over amplitude
and absolute displacement. Thresholds in (a) use the analytic $J_0(2a)$ comparator;
(c) and (e) use the converged $N=512$ finite transform. The calculation shown is a
pre-version development analysis and is not a retained evidence run.

## Exploratory non-flat companion

The dispersive four-state construction preserves the same central qualitative contrast
without importing either the flat-parent $J_0(2a)$ comparator or its exact
residual--tail identity. At $N=512$, its minimum sampled external gap is $1.0566461$, and its
largest computed band defect over 65 amplitudes is $1.45\times10^{-15}$. At
$a=\pi/4$, the restricted-alignment minimum and exact-spectrum joint thresholds are
$0.4004394$ and $0.4611609$, while the non-onsite hopping weight increases from the
reference value $0.0323839$ to $0.1761533$. The weight outside $|R|\leq4$ is
$8.43\times10^{-6}$, compared with $1.52\times10^{-18}$ for the reference frame.
These values are exploratory, finite-mesh observations, not accepted publication
results. They are pointwise claims at directly evaluated amplitudes; lines between
markers are guides to the eye rather than accepted continuum interpolants.

The non-flat momentum disposition is `converged`. The largest selected
physical-outcome change from $N=256$ to $N=512$ is $1.08\times10^{-11}$, and the
largest parent-invariant change is $1.67\times10^{-16}$. Neighboring-frame overlap is
retained as a qualification lower bound rather than treated as a convergence observable;
shared parent eigenvalues and spectral projectors provide the invariant cross-mesh
checks. The 64-interval amplitude grid remains `unresolved`, with a maximum correlation
midpoint defect of $3.49\times10^{-5}$. That failure must remain visible: momentum
convergence and roundoff-level band agreement cannot substitute for between-amplitude
resolution.

**Exploratory companion figure. Smooth non-flat four-state realization.** **(a)**
Restricted-alignment thresholds over a 65-node sampling of the smooth amplitude family;
markers show every eighth direct sample and lines are guides to the eye. **(b)** Reference
and comparison non-onsite weights over the same family. **(c)** Range-resolved
comparison hopping redistribution over amplitude and absolute displacement. **(d)**
Selected cumulative finite-mesh hopping tails. **(e)** Adjacent momentum-refinement
changes; both parent-invariant and selected outcome channels lie below the draft target.
**(f)** Midpoint amplitude-interpolation defects,
all above the draft target on the tested $N_a\leq64$ ladder. The figure is a pre-version
diagnostic and must not be cited as retained evidence; only its momentum-refinement
component is `converged`.

## Exploratory parent-family robustness companion

Scaling the non-onsite parent blocks by $0\leq\rho\leq1$ tests whether the mechanism is
specific to the selected dispersive parent. Across five sampled scales and 33 amplitudes,
all momentum studies through $N=256$ are `converged`. At $a=\pi/4$, the normalized
minimum threshold changes from $0.8815979$ at $\rho=0$ to $0.8613625$ at $\rho=1$,
while the excess non-onsite weight changes from $0.1431824$ to $0.1437693$. The sampled
external gap remains above $1.05E_G$. The normalized departure from the flat
residual--tail identity changes from roundoff at $\rho=0$ to $-0.0767265$ at $\rho=1$.
The restricted mismatch and excess hopping therefore remain large while their exact flat
identity deforms systematically with dispersion. The effect persists throughout the
sampled homotopy, although the finite inventory does not certify every intermediate
$\rho$ or resolve the amplitude-interpolation limitation.

**Exploratory parent-family scientific figure.** **(a)** Maximum band defect, with exact
zeros floored at $10^{-18}$ for logarithmic display. **(b)** Scale-normalized minimum
operator threshold and flat analytic comparator. **(c)** Scale-normalized excess
non-onsite hopping weight and flat analytic identity. **(d)** Parametric relation between
normalized residual $x$ and excess locality weight $y$, with the flat diagonal $y=x$.
**(e)** Directly evaluated departure $y-x$ over the $5\times33$ sampled parameter
pairs. **(f)** Full-parent cumulative tails at selected amplitudes. Colors identify
parent hopping scales, markers show every fourth amplitude sample, and lines are guides
to the eye. The calculation is a pre-version deterministic development study, not a
retained run, continuous-domain certificate, or material validation.

### Meaning of the plotted metrics

The calculation first forms the complete retained field $H_\rho(q_i)$ in a transported
periodic frame and then applies the smooth pointwise rotation
$A_{\rho,a}(q_i)=U_a(q_i)^\dagger H_\rho(q_i)U_a(q_i)$. The maximum ordered-eigenvalue
defect in panel (a) is therefore a numerical check of this constructed similarity, not a
comparison of independently generated material models. The restricted threshold in
panel (b) is

```math
\epsilon_{\min}=\sqrt{\kappa_\rho[1-\max(0,\mu_{\max})^2]},
```

where $\kappa_\rho$ is the mean per-state squared Frobenius norm of the traceless
retained field and $\mu_{\max}$ is the exact continuous maximum over one global real
rotation. It measures the component that cannot be represented by that deliberately
restricted global rotation and positive scale. It is not a distance under arbitrary
momentum-dependent unitary equivalence.

For each finite-mesh Fourier block, $p_R=\lVert T_R\rVert_F^2/(2E_G^2)$, and the
non-onsite power is $P_{>0}=\sum_{R\ne0}p_R$. Panels (c)--(e) compare

```math
x=\epsilon_{\min}^2/\kappa_\rho,
\qquad
y=(P_{>0}^{A}-P_{>0}^{H})/\kappa_\rho.
```

The flat endpoint obeys $y=x$. A dispersive reference already has non-onsite blocks, so
$y$ also contains cross terms between its existing hopping and the representation-induced
change. Accordingly, the observed $y-x<0$ is a calculated deformation of the flat
identity, not a failure of spectral equivalence. The numerator defining $y$ is a signed
difference of powers, not itself a norm.

Panel (f) reports $P_{>R_c}=\sum_{|R|>R_c}p_R$, the block power that a symmetric range
cutoff would omit. No block is deleted in this six-panel complete-model calculation.
It therefore establishes representation-dependent real-space compactness before any
finite-range approximation is applied.

## Exploratory finite-range follow-on

The follow-on action now deletes blocks through explicit conjugate-closed
ordinary-lattice inventories. Because the construction mesh is even, KSD first removes
and separately reports the cyclic Nyquist block rather than treating $-N/2$ as its own
ordinary-lattice partner. PhysKit then applies the declared $|R|\le R_c$ inventory and
reconstructs the distinct truncated model on the shifted $M=4N+1$ evaluation mesh.
Interpolation, deliberate truncation, and total errors remain separate.

Across the five sampled parent scales and 33 directly sampled amplitudes, the direct
unitarily related fields preserve their bands within $1.33\times10^{-15}E_G$ and the
largest full-comparison interpolation defect is $2.40\times10^{-14}E_G$. At
$(\rho,a)=(1,\pi/4)$, $R_c=3$ gives a reference maximum band error of
$5.53\times10^{-8}E_G$ but a rotated-comparison total band error of
$1.86\times10^{-2}E_G$; at $R_c=8$ the values are $4.22\times10^{-14}E_G$ and
$8.65\times10^{-7}E_G$. This sampled synthetic calculation directly connects the
previous compactness diagnostic to a finite-range spectral consequence: complete
unitarily related Hamiltonians can require substantially different ranges for comparable
band accuracy.

The three-panel follow-on figure shows the dispersive endpoint reference/comparison
contrast, robustness across the five sampled parent scales, and the empirical relation
between square-root omitted block power and maximum band error. Its $y=x$ line is a
visual comparator, not a theorem or error bound. The current follow-on has no frozen
accuracy target, strict serializer, independent verifier, velocity/curvature channel,
physical effective mass, or retained evidence.

## Editorial placement

Panels (a), (c), (d), and (e) carry the scientific argument and are suitable for a main
Results figure. Panel (b) documents numerical protocol design and may be moved to
supplementary material if the target journal limits main-text figure density. For a
final submission, the last sentence of the caption must be replaced only after a frozen
version and retained run actually exist. The six-panel parent-family scientific figure
is the strongest candidate for the eventual main Results figure; the convergence,
qualification, and sampling-control figures belong in methods or supplementary material.
Until a retained run exists, its numerical values remain exploratory even though momentum
refinement passes.
