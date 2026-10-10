# M3 scientific boundary

## Candidate family

M3 fixes the M2 transported reference represented operator $H_i$ and the attacked target
$A_i$ on training coordinates $k_i$. A continuous parameter
$p=(\eta,\zeta)$ lies in the declared rectangle of normalized energy-shift ratio
$\eta$ and splitting scale $\zeta$. It defines

<a id="eq-m3-candidate-001"></a>

$$
C_i(\eta,\zeta)
 = \bar E_i I + \eta E_G I
 + \zeta\left(H_i-\bar E_i I\right),
\qquad
\bar E_i=\frac{\operatorname{tr}H_i}{2}.
\tag{EQ-M3-CANDIDATE-001}
$$

$E_G$ is `loss_energy_scale` in the M2 parent energy unit. For each of the nine frozen
angles $\varphi_j$, M3 compares the globally rotated candidate
$R(\varphi_j)^\dagger C_i(p)R(\varphi_j)$ with $A_i$. The parameter rectangle is
continuous; the alignment family is finite.

## Losses

The spectral channel compares ordered eigenvalues with the common M2 retained target.
For rank $m=2$ and $N$ training points,

<a id="eq-m3-losses-002"></a>

$$
L_{\mathrm{spec}}(p)
 =\left[\frac{1}{Nm}\sum_{i,a}
   \left(\frac{\lambda_a(C_i(p))-\lambda_{ia}^{\mathrm{target}}}{E_G}\right)^2
  \right]^{1/2},
$$

$$
L_{\mathrm{op},j}(p)
 =\left[\frac{1}{Nm}\sum_i
  \left\|\frac{R(\varphi_j)^\dagger C_i(p)R(\varphi_j)-A_i}{E_G}\right\|_F^2
  \right]^{1/2}.
\tag{EQ-M3-LOSSES-002}
$$

The operator admissible set is the union over feasible frozen angles. These normalized
benchmark losses are not probabilistic uncertainties.

## Quadratic proof objects

The constructed affine candidate makes every squared training loss an exact quadratic

<a id="eq-m3-quadratic-003"></a>

$$
L_x(p)^2=(p-c_x)^TQ_x(p-c_x)+m_x,
\qquad
x\in\{\mathrm{spec},(\mathrm{op},j)\}.
\tag{EQ-M3-QUADRATIC-003}
$$

$Q_x$ is symmetric positive definite, $c_x$ is the center, and $m_x\geq0$ is the
minimum squared loss. The verifier checks both matrix cross terms, symmetry, curvature,
centers, minima, and agreement with reconstructed finite formulas.

## Admissible sets and common witness

For case thresholds $(\tau_s,\tau_o)$,

<a id="eq-m3-admissible-004"></a>

$$
\mathcal A_s=\{p:L_{\mathrm{spec}}(p)\leq\tau_s\},
\qquad
\mathcal A_o=\bigcup_j\{p:L_{\mathrm{op},j}(p)\leq\tau_o\}.
\tag{EQ-M3-ADMISSIBLE-004}
$$

A retained point in $\mathcal A_s\cap\mathcal A_o$ is a constructive compatibility
witness. M3's compatible case prospectively fixes and verifies $p=(0,1)$; it does not
infer compatibility from failed falsification.

## Separation certificate

For the separated case, the spectral set and each feasible operator-angle component are
ellipses. M3 uses their extrema along the splitting-scale axis to obtain a lower bound.
If $\zeta_s^-$ is the lower spectral boundary and $\zeta_{o,j}^+$ is the upper boundary
of operator component $j$, then

<a id="eq-m3-separation-005"></a>

$$
\delta_{\mathrm{lb}}
 =\max\left(0,\zeta_s^- - \max_{j\in J_{\mathrm{feasible}}}\zeta_{o,j}^+\right).
\tag{EQ-M3-SEPARATION-005}
$$

This axis gap is a Euclidean lower bound because $|\zeta_s-\zeta_o|\leq\lVert
p_s-p_o\rVert_2$. A `certified-separated` disposition requires
$\delta_{\mathrm{lb}}$ to exceed `separation_resolution`. The analytic boundary formula
is valid only because every retained threshold ellipse is unclipped by the declared
parameter rectangle; that premise is explicitly verified.

## Threshold status

The retained spectral/operator thresholds and resolution were selected prospectively
from known synthetic training geometry to demonstrate compatible and separated regimes.
They are not blind, physical, or uncertainty-calibrated tolerances. The separate
sensitivity package is a post-hoc transparency analysis and cannot alter M3 controls or
results.

## Claims and exclusions

M3 establishes one common witness and one analytic separation certificate over the
continuous frozen parameter rectangle and finite nine-angle global-rotation family. It
does not prove incompatibility over arbitrary parameterizations or momentum-dependent
unitaries, material inadequacy, universal thresholds, or probabilistic confidence.
