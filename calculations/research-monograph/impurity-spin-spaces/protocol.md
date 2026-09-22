# Controlled spin-space embedding protocol

## Evidentiary status

This protocol defines a deterministic calculation on authored synthetic matrices. It is numerical and software verification of finite-dimensional spin embeddings, comparison prerequisites, and exact algebraic identities. It is not a Kohn--Sham calculation, a model of phosphorus or boron, scientific validation, or uncertainty quantification.

## Represented spaces and conventions

Let $\mathcal V$ be the ordered four-orbital space with basis $(o_0,o_1,o_2,o_3)$. The spinless Hamiltonian $H_0$ and spinless impurity operator $\Delta H_0$ act on $\mathcal V$. Their nonmagnetic spinful lifts act on $\mathcal V\otimes\mathbb C^2$ in the canonical $z$-spin basis $(\uparrow_z,\downarrow_z)$.

The canonical tensor-product ordering is orbital-major:

$$
(o_0\uparrow,o_0\downarrow,o_1\uparrow,o_1\downarrow,\ldots).
$$

The alternative spin-major ordering is

$$
(o_0\uparrow,o_1\uparrow,\ldots,o_0\downarrow,o_1\downarrow,\ldots).
$$

A declared permutation $P$ maps spin-major coordinates to orbital-major coordinates. All operators use the synthetic energy unit, the shared-zero energy reference, and the declared finite-model no-geometry convention. Equal shape is not treated as compatibility.

## Authored operators

The exact spin-degenerate lift is

$$
\Delta H_{\mathrm{deg}}=\Delta H_0\otimes I_2.
$$

The collinear operator is

$$
\Delta H_{\mathrm{col}}
=
\Delta H_0\otimes I_2+Z\otimes\sigma_z,
$$

where $Z=Z^\dagger$ is the authored collinear splitting. In spin-major order its diagonal blocks must be $\Delta H_0+Z$ and $\Delta H_0-Z$.

The spin-mixing operator is

$$
\Delta H_{\mathrm{spin}}
=
\Delta H_0\otimes I_2
+
\sum_{j=x,y,z} B_j\otimes\sigma_j.
$$

Each input generator $A_j$ is real antisymmetric and $B_j=iA_j$ is Hermitian. With $\Theta=(I\otimes i\sigma_y)K$, where $K$ denotes complex conjugation, this construction is time-reversal invariant because $B_j^*=-B_j$ and $\Theta\sigma_j\Theta^{-1}=-\sigma_j$. The real collinear splitting is intentionally time-reversal breaking.

## Exact embedding and norm controls

The two spin injections are

$$
E_\uparrow=I_{\mathcal V}\otimes|\uparrow\rangle,
\qquad
E_\downarrow=I_{\mathcal V}\otimes|\downarrow\rangle.
$$

The verifier requires

$$
E_s^\dagger\Delta H_{\mathrm{deg}}E_s=\Delta H_0,
\qquad
E_\uparrow^\dagger\Delta H_{\mathrm{deg}}E_\downarrow=0,
$$

and the independently derived identity

$$
\|\Delta H_{\mathrm{deg}}\|_F
=
\sqrt{2}\,\|\Delta H_0\|_F.
$$

Consequently $\|\Delta H\|_F/\sqrt{\dim\mathcal H}$ is unchanged by the exact spin-degenerate lift.

## Ordering and spin-frame covariance

The spin-major coordinates are

$$
\Delta H_{\mathrm{col}}^{(s)}
=P^\dagger\Delta H_{\mathrm{col}}^{(o)}P.
$$

Direct subtraction between the two stored orderings must stop. Applying the declared map must recover the canonical matrix. Spectra and Frobenius norms remain invariant.

For each authored axis $\hat n$ and angle $\theta$, define

$$
R(\hat n,\theta)
=
\cos\frac{\theta}{2}I_2
-i\sin\frac{\theta}{2}\hat n\cdot\boldsymbol\sigma,
\qquad
U=I_{\mathcal V}\otimes R.
$$

The rotated coordinates are $\Delta H'=U^\dagger\Delta H U$. Direct comparison with the canonical frame must stop because the spin-frame identifiers differ. Explicit alignment by $U\Delta H'U^\dagger$ must recover the canonical matrix. The antiunitary unitary part transforms as $T'=U^\dagger T U^*$ and is used for the rotated-frame time-reversal residual.

## Spin-independent model class

For a spinful matrix $M$ in orbital-major order, its Frobenius-optimal spin-independent representative is

$$
M_{\mathrm{scalar}}
=
\left(\frac{1}{2}\operatorname{Tr}_{\mathrm{spin}}M\right)\otimes I_2.
$$

The exact residual oracles are

$$
\|\Delta H_{\mathrm{deg}}-M_{\mathrm{scalar}}\|_F=0,
$$

$$
\|\Delta H_{\mathrm{col}}-M_{\mathrm{scalar}}\|_F
=
\sqrt{2}\,\|Z\|_F,
$$

and

$$
\|\Delta H_{\mathrm{spin}}-M_{\mathrm{scalar}}\|_F
=
\left(2\sum_j\|B_j\|_F^2\right)^{1/2}.
$$

A nonzero residual is a model-class discrepancy for this synthetic construction, not representation error or a physical validation metric.

## Structured stopping controls

The represented-operator compatibility action checks state-space identity, dimension, orbital order, spin representation, basis order, spin frame, energy unit, energy reference, and geometry before subtraction. Three authored negative cases must stop without returning a nominal norm:

1. spinless versus spinful operators;
2. orbital-major versus spin-major coordinates without $P$; and
3. equal matrices carrying different energy-reference identifiers.

## Acceptance rules

The declared algebraic tolerance is $10^{-12}$ in the applicable absolute unit. The retained result passes its numerical-verification protocol only when:

- every represented matrix is Hermitian within tolerance;
- both spin pullbacks, the cross-spin block, and the $\sqrt{2}$ Frobenius identity agree within tolerance;
- the declared permutation and each spin rotation are unitary within tolerance;
- aligned ordering and spin-frame defects, spectral defects, norm defects, and applicable time-reversal residuals are within tolerance;
- scalar-model residuals agree with their independent analytical expressions within tolerance;
- the degenerate scalar residual vanishes while the planted collinear and spin-mixing residuals remain nonzero; and
- every incompatible comparison returns its exact structured stop code and no residual.

Passing these rules establishes only the stated finite-matrix verification.
