# Prospective silicon DFT–Wannier gauge-locality protocol

## 1. Scientific question and scope

For a fixed, explicitly identified rank-$J$ silicon retained subspace, quantify which
finite represented-operator properties are invariant under internal gauge changes and
which locality and truncation properties depend on the selected gauge.

The bounded questions are:

1. Does the admitted Wannier90 frame occupy the declared retained subspace at every
   reciprocal point?
2. How do the pre-gauge retained frame and Wannier90 gauge redistribute the centered
   finite Fourier blocks of the same represented operator?
3. Does a frozen momentum-dependent synthetic attack preserve the projector and complete
   spectrum while degrading block locality?
4. Does pointwise Procrustes recover the attacked frame and represented operators to the
   declared numerical tolerance?
5. Can any claimed difference be assigned separately to subspace selection, gauge,
   cyclic-to-ordinary conversion, finite interpolation, deliberate truncation, or the
   parent calculation?

This protocol defines analysis only. It does not authorize or perform QE or Wannier90
execution, change a pseudopotential or physical input, or establish scientific
validation.

## 2. Authoritative conventions

The calculation must conform to:

- `specification/ksdft2Effmass.physical-specification.v1.md` and
  `specification/ksdft2Effmass.numerical-specification.v1.md` for the currently adopted
  project-level conventions;
- `docs/research/proofs/ksdft2effmass/foundations/state-space-assumptions.md` for the
  distinction between ambient Kohn–Sham fibers, retained subspaces, and Wannier
  coordinates; and
- `docs/research/proofs/ksdft2effmass/operator-alignment/gauge-equivariance.md` for
  same-space gauge comparison.

The proposed gauge-locality interpretation follows the noncommutation boundary in
`docs/research/proofs/ksdft2effmass/reduction/gauge-constrained-locality.md`:
real-space truncation is generally not equivariant under a momentum-dependent unitary.
The ordered Wannier inputs, finite `H/T/R` representation, and Wigner–Seitz interpolation
routes remain prospective conventions in this protocol. They require separately adopted
authoritative specifications before maintained source implementation or retained
execution.

## 3. State spaces and admission gates

At an ordered reciprocal point $k$, let the authenticated parent-band coordinate space
be $\mathbb C^B$. The admitted Wannier90 factors are

$$
D(k)\in\mathbb C^{B\times J},\qquad U(k)\in U(J),
$$

with

$$
D(k)^\dagger D(k)=I_J,\qquad U(k)^\dagger U(k)=I_J.
$$

The disentangled retained frame and Wannier90 frame are

$$
F_D(k)=D(k),\qquad F_W(k)=D(k)U(k).
$$

They have the same projector in parent-band coordinates:

$$
P_D(k)=D(k)D(k)^\dagger=P_W(k).
$$

Before gauge comparison, the calculation must admit or fail closed on:

- exact reciprocal-point ordering and mesh shape;
- parent-band ordering and retained rank;
- frame isometry and gauge unitarity;
- projector equality for every channel asserted to share a subspace;
- parent Hamiltonian energy reference and physical energy unit;
- direct- and reciprocal-lattice conventions, including factors of $2\pi$;
- coefficient-row, spin, and generalized-overlap conventions;
- exact source-byte identities and production provenance; and
- the declared numerical backend and tolerances.

### 3.1 Raw DFT is not automatically a gauge channel

For an entangled calculation, $D(k)$ is a Wannier90-selected isometry, not the raw DFT
eigenframe. A proposed rank-$J$ raw Kohn–Sham band group $F_{KS}(k)$ first belongs to a
**subspace-selection** comparison. The protocol must report projector distances,
principal angles, and overlap singular values. If the projectors do not agree within a
prospectively declared tolerance, no unitary gauge identification and no direct matrix
subtraction are admitted.

An isolated-band calculation may treat the raw Kohn–Sham group as a gauge channel only
when the admitted $D(k)$ is verified to be the corresponding ordered band-selection
isometry.

## 4. Gauge channels

Freeze an analytic right-unitary attack $A(k)\in U(J)$ before evaluating results. Define

$$
F_A(k)=F_W(k)A(k).
$$

The pointwise oracle solves independently at every reciprocal point

$$
Q_P(k)=\arg\min_{Q\in U(J)}
\left\|F_A(k)Q-F_W(k)\right\|_F,
$$

and defines

$$
F_P(k)=F_A(k)Q_P(k).
$$

A separate restricted control selects one constant unitary

$$
Q_G=\arg\min_{Q\in U(J)}
\sum_k\left\|F_A(k)Q-F_W(k)\right\|_F^2.
$$

Optimization must disclose the right-action convention, singular values, absolute and
relative rank cutoffs, and the cutoff-combination rule. Rank deficiency fails closed;
there is no unreported null-space completion.

The pointwise target is the Wannier90 frame, so $F_P\simeq F_W$ is an oracle recovery
check. It is not an independent localization algorithm and must never be presented as
outperforming Wannier90.

## 5. Same-frame represented operators

Let ordered parent eigenvalues be $\epsilon(k)$ and let the authenticated parent-band
kinetic matrix be

$$
T^{KS}(k)=C(k)^\dagger\operatorname{diag}(t(k))C(k).
$$

For every admitted frame $F_c(k)$, construct

$$
H_c(k)=F_c(k)^\dagger\operatorname{diag}(\epsilon(k))F_c(k),
$$

$$
T_c(k)=F_c(k)^\dagger T^{KS}(k)F_c(k),
$$

$$
R_c(k)=H_c(k)-T_c(k).
$$

The labels $H$, $T$, and $R$ remain separate throughout analysis and verification.
$R$ is a finite represented non-kinetic remainder, not a reconstructed continuous local
potential.

For gauge-only channels related by $F_c=F_WG_c$, verify

$$
X_c(k)=G_c(k)^\dagger X_W(k)G_c(k),
\qquad X\in\{H,T,R\}.
$$

A projector or spectrum match does not replace this represented-operator correlation.

## 6. Finite Fourier and locality diagnostics

Apply the normalized finite transform declared by the eventual adopted
kinetic-decomposition specification separately to every operator role and gauge channel.
Retain the complete centered cyclic block inventory and verify reciprocal reconstruction
before any support deletion. No transform convention is considered adopted solely by
this prospective calculation protocol.

Report, without combining their meanings:

- block Frobenius norms and shell-resolved power;
- cyclic Hermiticity defects;
- complete-transform reconstruction defects;
- ordinary-lattice conversion power;
- ordinary omitted-block norm or power at each prospective shell cutoff; and
- matrix and sorted-spectrum consequences on declared reciprocal inventories.

A $k$-independent unitary may rotate each block internally without changing its
Frobenius norm. A $k$-dependent unitary may mix lattice representatives. Therefore
hopping range, shell weight, decay length, and truncation error are properties of the
operator together with its gauge, not intrinsic observables of the abstract operator.

### 6.1 Even-mesh cyclic-to-ordinary conversion

For every even mesh axis, a centered negative-Nyquist component is self-conjugate only
modulo that mesh size. Before applying an ordinary-lattice shell cutoff, define the
Nyquist boundary inventory prospectively and remove every block that lacks an ordinary
integer-lattice conjugate partner. Report its normalized power separately for each
operator role and gauge channel:

$$
P_{c,X,\mathrm{Nyq}}=
\frac{1}{J E_{\mathrm{ref}}^2}
\sum_{R\in\mathcal N_{\mathrm{Nyq}}}
\left\|X_c(R)\right\|_F^2.
$$

The exact multidimensional boundary inventory must be encoded, not inferred from an
array shape. It is not pooled with deliberate shell truncation. The current `4 × 4 × 4`
prototype is especially sensitive to this distinction because a large fraction of its
centered representatives touch an even-mesh Nyquist boundary.

Wigner–Seitz replica lifting and degeneracy division form a separate representation
route. They must follow a separately adopted specification and must not be silently
substituted for the centered cyclic-to-ordinary conversion.

## 7. Evaluation and error channels

Use a disjoint reciprocal evaluation inventory whose rational construction and
non-overlap with the source mesh are established before binary64 conversion.

For an ordinary complete interpolant $X_c^{\mathrm{ord}}$, its shell-truncated field
$X_{c,S}^{\mathrm{ord}}$, and an independently declared direct target
$X_c^{\mathrm{dir}}$, report:

$$
\Delta_{\mathrm{interp}}=X_c^{\mathrm{ord}}-X_c^{\mathrm{dir}},
$$

$$
\Delta_{\mathrm{trunc}}=X_{c,S}^{\mathrm{ord}}-X_c^{\mathrm{ord}},
$$

$$
\Delta_{\mathrm{total}}=X_{c,S}^{\mathrm{ord}}-X_c^{\mathrm{dir}}.
$$

For every channel, state whether the direct target is:

1. an independently sampled DFT/Wannier90 field;
2. an authenticated native `hr.dat` interpolation route;
3. an analytic synthetic attack applied to an admitted complete reference field; or
4. the finite complete interpolant itself by definition.

Only case 1 provides a direct off-source-mesh parent sample. Case 2 is a cross-route
finite interpolation check. Case 3 is the correct direct target for the synthetic attack.
Case 4 has zero reference interpolation error by definition and must not be described as
independent validation.

Retain maximum and root-mean-square normalized Frobenius errors

$$
\delta_F(X,Y)=\frac{\|X-Y\|_F}{\sqrt{J}E_{\mathrm{ref}}},
$$

and corresponding sorted-band errors for $H$. For $T$ and $R$, sorted eigenvalues are
representation diagnostics only and must not be called physical band energies.

Pointwise residuals telescope, but separately maximized or root-mean-square errors are
not added as independent scalars. The calculation may report the applicable triangle
bound; it must not claim equality of maxima.

## 8. Wannier90-specific observables

Admit Wannier90 spread components only from authenticated native records with their
units, convergence status, and source identity. Do not fabricate a spread for a channel
from hopping-block decay alone. Conversely, do not use a lower spread as proof of lower
operator truncation error; compare the declared quantities directly.

A fair method comparison must state its objective. Candidate criteria include:

- total and component Wannier spreads;
- shell-resolved `H/T/R` block power;
- disjoint-mesh Hamiltonian interpolation error;
- finite-shell truncation error;
- frame conditioning and robustness; and
- sensitivity to mesh, windows, projections, and tolerances.

No scalar composite score or claim that one method is “better” is admitted without a
separately reviewed decision rule.

## 9. Verification and authenticated presentation

A maintained lifecycle must use immutable typed configuration and result records,
canonical JSON bytes, and a byte-owning verifier. Independent reconstruction must not
call the production analyzer or treat stored diagnostics as reference values.

At minimum, reconstruct and correlate:

- source ordering and admitted units;
- frame isometries, projectors, and Procrustes selections;
- `H/T/R` matrices in every channel;
- gauge-covariance identities;
- cyclic and ordinary block inventories;
- conversion, interpolation, truncation, and total channels;
- shell inventories and all reported extrema;
- native-route comparisons when present; and
- every value admitted into visualization.

Rendering consumes only verifier-authenticated projection bytes, calculates no new
scientific values, and publishes a closed figure inventory atomically.

## 10. Staged work and authorization boundaries

### Stage A — read-only artifact readiness

Inventory existing local bytes and determine whether every required identity and
convention is available. This stage may inspect repository-retained public project data;
it must not transmit restricted data or read an external production directory without
applicable authority.

### Stage B — synthetic gauge control on admitted retained bytes

Using no calculator execution, add frozen attack, pointwise oracle, and global control
channels to already admitted reciprocal data. Establish typed calculation, independent
verification, and authenticated visualization before interpreting locality.

### Stage C — DFT/Wannier cross-route evaluation

Add a disjoint reciprocal inventory and native-route comparisons only when their source
identity and state-space relationship are explicit. Existing finite interpolants are not
relabeled as new DFT samples.

### Stage D — convergence and production study

Changes to reciprocal meshes, Wannier windows or projections, pseudopotentials,
exchange-correlation approximations, cutoffs, structures, or tolerances require
scientific authority. Any QE or Wannier90 execution, remote computation, retained run,
evidence sealing, or publication update requires separate explicit authorization.

## 11. Current definition of done

This protocol addition is complete when it records the scientific question, state-space
gates, noncircular channel meanings, operator inventory, multidimensional Nyquist
boundary, error decomposition, verification boundary, and protected-action gates.

It does **not** complete artifact admission, implement the analyzer, run a simulation,
produce a numerical result, select a preferred gauge, or validate silicon physics.
