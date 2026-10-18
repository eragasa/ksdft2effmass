# HSH-1 scientific boundary

## Fixed parent and represented state space

HSH-1 consumes the retained lowest scalar band of the square-lattice parent at
$\lambda_{xy}=0.30$. The finite source domain is the centered $15\times15$ reciprocal
mesh with reduced coordinates and canonical representatives
$\mathcal R_{\max}=\{-7,\ldots,7\}^2$. The target is projected onto exact real
$D_4$ orbits only after raw Hermiticity, imaginary-part, and symmetry defects pass a
prospectively frozen tolerance.

The projection defines one finite represented scalar hopping family. It is not an
infinite-lattice decay result and is not a material Hamiltonian.

## Common maximal coefficient space

Let $o$ denote a canonical $D_4$ orbit of representatives and $m_o=|o|$ its
multiplicity. One real coefficient $\theta_o$ is assigned to every orbit, in
increasing squared radius and then canonical representative order. The orbit basis is

<a id="eq-hsh-orbit-001"></a>

$$
\phi_o(\mathbf k)=\sum_{\mathbf R\in o}
  e^{2\pi i\mathbf k\cdot\mathbf R},
\qquad
E_\theta(\mathbf k)=\sum_o\theta_o\phi_o(\mathbf k).
\tag{EQ-HSH-ORBIT-001}
$$

The orbit contains $-\mathbf R$, so $\phi_o$ and $E_\theta$ are real on the declared
mesh up to reconstructed numerical defect. The source-mesh mean is removed once and the
same energy zero is used by both channels.

For squared-radius inventory $S=(0,1,2,4,8,18,50,98)$, class $\mathcal M_k$ fixes every
coefficient outside $S_k$ to zero. Model-class expansion changes interaction range, not
the one-dimensional orbital basis. Every class remains embedded in the same maximal
vector space.

## Loss channels

The fixed positive spectral weights $w_i$ define

<a id="eq-hsh-loss-002"></a>

$$
L_E(\theta)^2 =
\frac{\sum_i w_i\left(E_\theta(\mathbf k_i)-E_{\rm ref}(\mathbf k_i)\right)^2}
     {E_G^2\sum_i w_i}.
\tag{EQ-HSH-LOSS-002}
$$

The represented-operator channel compares every block in the common finite domain:

<a id="eq-hsh-operator-loss-003"></a>

$$
L_H(\theta)^2 =
\frac{\sum_o m_o\left(\theta_o-t_o^\star\right)^2}
     {E_G^2\sum_o m_o}.
\tag{EQ-HSH-OPERATOR-LOSS-003}
$$

Here $E_G>0$ is the retained parent energy scale, $\mathbf k_i$ are the 225
source-mesh points in reduced reciprocal coordinates, $E_{\rm ref}$ is the exact
symmetry-projected finite target with its source-mesh mean removed, $w_i>0$ are fixed
spectral weights invariant on reciprocal-mesh $D_4$ orbits, and $t_o^\star$ is the real
target coefficient shared by every block
in orbit $o$. Every coefficient $\theta_o$ and $t_o^\star$ has energy units; both
losses are dimensionless.

The complete finite Fourier transform is invertible, so the disjoint orbit-sum columns
are linearly independent; positive weighting preserves full column rank on every active
shell subset. This supplies the mathematical positive-definiteness premise, while the
producer and verifier still check its binary64 realization and frozen curvature margin.

Equal full-mesh spectral weights are excluded from the intended primary design. Under
the declared Fourier and RMS normalizations, Parseval gives
$L_E^2=|\mathcal R_{\max}|L_H^2=225L_H^2$ for every candidate, so the two sublevel
geometries differ only by threshold rescaling and cannot expose a genuine channel
tradeoff. The exact nonuniform positive, reciprocal-mesh-$D_4$-invariant spectral weight
formula is part of the scientific problem and must be frozen before evaluation.

For fixed positive thresholds $\tau_E$ and $\tau_H$, the channel sets in class $k$ are

<a id="eq-hsh-admissible-004"></a>

$$
\mathcal A_{E,k}=\{\theta\in\mathcal M_k\cap\mathcal B:L_E(\theta)\le\tau_E\},
\qquad
\mathcal A_{H,k}=\{\theta\in\mathcal M_k\cap\mathcal B:L_H(\theta)\le\tau_H\},
\tag{EQ-HSH-ADMISSIBLE-004}
$$

where $\mathcal B$ is the one frozen coefficient box. An empty channel set is reported
as empty; it is not converted into a finite separation distance.

## Distance and certification

The common normalized block metric is

<a id="eq-hsh-distance-005"></a>

$$
d_{\rm red}(\theta,\eta)=
\left[\frac{1}{E_G^2|\mathcal R_{\max}|}
\sum_o m_o(\theta_o-\eta_o)^2\right]^{1/2}.
\tag{EQ-HSH-DISTANCE-005}
$$

Here $|\mathcal R_{\max}|=225$ and the positive diagonal metric matrix is
$M=\operatorname{diag}(m_o/(E_G^2|\mathcal R_{\max}|))$. Its reusable dimensionful
hopping/Frobenius representation belongs to PhysKit; HSH selects the energy scale and
scientific role, while optimization owns only the unit-free distance/support problem
after nondimensionalization. For two nonempty channel
sets, $\delta_k^*=\inf d_{\rm red}(\theta_E,\theta_H)$. A feasible pair provides an
upper bound. A common feasible point proves compatibility. Positive separation requires
an independently reconstructed support certificate, not failed search.

For covector $u$ and metric matrix
$M=\operatorname{diag}(m_o/(E_G^2|\mathcal R_{\max}|))$, a conservative directional
gap $g_k(u)$ gives

<a id="eq-hsh-support-bound-006"></a>

$$
\delta_k^*\ge
\underline\delta_k(u)=
\max\!\left(0,
\frac{g_k(u)}{\sqrt{u^TM^{-1}u}}
\right).
\tag{EQ-HSH-SUPPORT-BOUND-006}
$$

The covector components are dimensionless in the canonical coefficient ordering, so
its support endpoints and $g_k$ have the coefficient energy unit,
$\sqrt{u^TM^{-1}u}$ has the same unit, and the lower bound is dimensionless. The retained
certificate must identify the orientation and conservative support bounds that define
$g_k$. Enclosing an intersected set by its full quadratic ellipsoid is allowed because
it weakens the lower bound. Outward rounding must make the recorded bound conservative.

## Hierarchy conclusion

A class is compatible only through an explicit common witness. It is certified
separated only when both sets are nonempty and a reconstructed lower bound exceeds the
frozen resolution. A smallest tested compatible class may be reported only when every
smaller class is either directly empty in at least one channel or certified separated;
any unresolved smaller class blocks minimality.

## Claims and exclusions

The intended result is hierarchy-relative: one fixed finite parent, target projection,
shell ordering, box, weights, thresholds, metric, and mesh roles. HSH-1 cannot establish
a physically minimal Hamiltonian, universal interaction range, material adequacy,
asymptotic localization rate, uncertainty interval, or arbitrary-gauge result.

## Prospective equation mapping

| Equation | Planned implementation owner | Planned direct check |
|---|---|---|
| `EQ-HSH-ORBIT-001` | `Periodic2DHoppingShellHierarchyCalculator.execute` private orbit/design construction | Independent orbit enumeration and Fourier reconstruction |
| `EQ-HSH-LOSS-002` | HSH spectral wrapper over exact-pinned Optimization facade | Direct weighted loss versus retained quadratic at bounded points |
| `EQ-HSH-OPERATOR-LOSS-003` | HSH operator wrapper over exact-pinned Optimization facade | Direct block-multiplicity loss versus retained quadratic |
| `EQ-HSH-ADMISSIBLE-004` | Calculator bounded-minimum and witness stages | Empty/intersecting/tangent analytic fixtures |
| `EQ-HSH-DISTANCE-005` | Calculator/result common metric | Explicit full-block Frobenius comparison |
| `EQ-HSH-SUPPORT-BOUND-006` | `Periodic2DHoppingShellSupportCertificate` and verifier | Rational/high-precision support oracle with outward rounding |

No listed implementation or direct check exists yet.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Not evaluated | Planned classes and tests do not exist | [Testing plan](testing.md) | Future exact and fail-closed assertions | Future locked Python environment | Prospective finite HSH-1 API | Not applicable |
| Numerical verification | Not evaluated | No quadratic, support, or Fourier oracle has run | [Testing plan](testing.md) | Future frozen per-oracle tolerances | Future NumPy/SciPy and interval stack | Prospective finite hierarchy | Not applicable |
| Scientific validation | Not evaluated | Synthetic parent has no material comparator | None | None | None | None | Not applicable |
| Uncertainty quantification | Not evaluated | Thresholds and deterministic bounds are not UQ | None | None | None | None | Not applicable |
| Human acceptance | Not evaluated | Problem controls and architecture remain draft | Future freeze/decision record | Not applicable | Not applicable | Future frozen HSH-1 problem | Human owner not yet recorded |

## Authority and provenance

The equations above represent the draft computational procedure and do not supersede
it.

| Attribution ID | Claim or equation | Source | Version | Pinpoint locator | License | Role | Deviation |
|---|---|---|---|---|---|---|---|
| `ATTR-HSH-001` | `EQ-HSH-ORBIT-001` and finite target conventions | `calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md` | Draft, unexecuted | Sections 3--5 | Repository license | Derived | Adds planned software ownership and canonical ordering |
| `ATTR-HSH-002` | `EQ-HSH-LOSS-002` through `EQ-HSH-ADMISSIBLE-004` | `calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md` | Draft, unexecuted | Section 6 | Repository license | Derived | Expresses the planned typed quadratic representation |
| `ATTR-HSH-003` | `EQ-HSH-DISTANCE-005` | `calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md` | Draft, unexecuted | Section 7 | Repository license | Derived | Names the diagonal software metric representation |
| `ATTR-HSH-004` | `EQ-HSH-SUPPORT-BOUND-006` and bounded disposition rules | `calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md` | Draft, unexecuted | Sections 9--11 | Repository license | Derived | Requires explicit arithmetic identity and independent reconstruction |
