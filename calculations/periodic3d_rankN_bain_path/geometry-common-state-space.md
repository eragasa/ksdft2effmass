# Selected periodic-3D rank-N Bain geometry and common state space

**Status: SELECTED GEOMETRY/STATE-SPACE SUBPROTOCOL — NO CALCULATION OR EXECUTION AUTHORITY**

This calculation-owned subprotocol closes the continuous geometry, coordinate, endpoint,
common-cell, basis-offset, bond-inventory, and M1N common-state-space conventions. It
does not select M0 or M2 operators, admitted ranks or depths, meshes, tolerances,
resources, visualization, lifecycle, or execution identity.

## Claim boundary and units

The path is a synthetic homogeneous metric deformation. It is not material strain,
elasticity, phase stability, martensitic physics, silicon, or material validation.

The declared direct-length unit identity is `synthetic-bain-direct-length-v1`, with unit
symbol \(\ell_0\). Every direct-lattice vector has units \(\ell_0\), the direct metric
has units \(\ell_0^2\), primitive volume has units \(\ell_0^3\), and reciprocal vectors
have units \(\ell_0^{-1}\). The phrase *unit primitive volume* means normalized volume
\(V/\ell_0^3=1\); it does not mean one cubic metre, one cubic ångström, or a material
lattice constant.

## Closed continuous path

Let the path fraction be

\[
 s\in[0,1],
 \qquad
 \gamma(s)=\frac{c}{a}=\sqrt2+s(1-\sqrt2).
\]

Both endpoints are included. Define dimensionless transverse and longitudinal scales

\[
 t(s)=\left(\frac{2}{\gamma(s)}\right)^{1/3},
 \qquad
 l(s)=\gamma(s)t(s)=\frac{2}{t(s)^2}.
\]

The required floating-point evaluation form for the longitudinal scale is
`l = 2 / t**2`; the equality \(l=\gamma t\) defines the same exact path, while the
selected evaluation form preserves the volume identity directly.

In fixed orthogonal Cartesian axes, the direct primitive vectors are the columns

\[
 \begin{aligned}
 \mathbf a_1(s)&=\frac{\ell_0}{2}(t,t,l)^\mathsf T,\\
 \mathbf a_2(s)&=\frac{\ell_0}{2}(-t,t,l)^\mathsf T,\\
 \mathbf a_3(s)&=\frac{\ell_0}{2}(t,-t,l)^\mathsf T,
 \end{aligned}
\]

and

\[
 A_B(s)=[\mathbf a_1(s)\;\mathbf a_2(s)\;\mathbf a_3(s)].
\]

Each point uses PhysKit's `DirectLattice3D` role with numeric components expressed in
`synthetic-bain-direct-length-v1`. Because the component arrays are numerical, a future
typed geometry record must bind that unit identity explicitly; the arrays must not be
interpreted as unitless. Primitive vectors are columns. The primitive basis is
nonorthogonal; no Cartesian component array is itself a physical distance.

The direct metric and reciprocal primitive matrix are

\[
 G_B(s)=A_B(s)^\mathsf T A_B(s),
 \qquad
 K_B(s)=2\pi A_B(s)^{-\mathsf T},
\]

so

\[
 A_B(s)^\mathsf T K_B(s)=2\pi I_3.
\]

Reduced coordinates are dimensionless column vectors. Direct positions and physical
wave vectors are

\[
 \mathbf x=A_B(s)\mathbf n_B,
 \quad \mathbf n_B\in\mathbb Z^3,
 \qquad
 \mathbf k=K_B(s)\mathbf q_B,
 \quad \mathbf q_B\in[0,1)^3.
\]

The same \(\mathbf q_B\) labels the same point of the abstract reduced reciprocal torus
at every \(s\); because \(K_B(s)\) varies, it does not label one fixed Cartesian
wave vector along the path.

## Volume and endpoint certificates

The selected orientation has positive determinant and

\[
 \det A_B(s)=\ell_0^3\frac{t(s)^2l(s)}{2}=\ell_0^3,
 \qquad
 \det G_B(s)=\ell_0^6.
\]

Thus the path is continuous and exactly unit-primitive-volume in the declared unit.

At \(s=0\),

\[
 \gamma=\sqrt2,
 \quad t=2^{1/6},
 \quad l=2^{2/3},
\]

and the metric is an FCC primitive metric with conventional cubic side
\(2^{2/3}\ell_0\). At \(s=1\),

\[
 \gamma=1,
 \quad t=l=2^{1/3},
\]

and the displayed primitive vectors are a BCC primitive basis with conventional cubic
side \(2^{1/3}\ell_0\). The names FCC and BCC identify geometric endpoint
representations only and do not identify phases of a material.

## FCC endpoint and common-cell map

Let

\[
 U=\begin{pmatrix}
 1&1&0\\
 0&0&1\\
 0&-1&0
 \end{pmatrix},
 \qquad
 U^{-1}=\begin{pmatrix}
 1&0&1\\
 0&0&-1\\
 0&1&0
 \end{pmatrix},
 \qquad \det U=1.
\]

The common Bain/BCT coordinate \(\mathbf n_B\) and the FCC primitive coordinate
\(\mathbf n_F\) satisfy

\[
 \mathbf n_F=U\mathbf n_B.
\]

The selected FCC endpoint orientation is defined without a hidden rotation by

\[
 A_F=A_B(0)U^{-1}.
\]

Therefore

\[
 A_B(0)=A_FU,
 \qquad
 G_B(0)=U^\mathsf T G_FU,
 \qquad
 G_F=A_F^\mathsf T A_F.
\]

Equivalently,

\[
 \frac{G_F}{\ell_0^2}
 =2^{4/3}
 \begin{pmatrix}
 1/2&1/4&1/4\\
 1/4&1/2&1/4\\
 1/4&1/4&1/2
 \end{pmatrix}.
\]

Reciprocal reduced coordinates obey

\[
 \mathbf q_B=U^\mathsf T\mathbf q_F.
\]

On the infinite lattice, \(U\) is a bijection of \(\mathbb Z^3\). On a finite common
cubic quotient \((\mathbb Z/N\mathbb Z)^3\), it is a bijection for every positive
integer \(N\). This statement does not select a mesh. The independent finite-quotient
bijection proof obligation belongs to the projectkoios-formal workstream. A future
noncubic or mixed-modulus quotient is admissible here only after a reviewed proof that
the same integer map is a well-defined bijection is bound to this protocol; until then
the common-cell comparison is typed `unresolved`. Assignment of that proof obligation
does not promote a mixed-modulus mesh.

## Basis offsets and oriented bond inventory

This path adopts the fixed-geometry rank-N `fcc-two-basis-metric-control` as geometry
metadata, not as a material or extra Hilbert-space factor. In FCC coordinates,

\[
 \tau_F^A=(0,0,0)^\mathsf T,
 \qquad
 \tau_F^B=(1/4,1/4,1/4)^\mathsf T.
\]

The fixed common Bain coordinates are

\[
 \tau_B^A=(0,0,0)^\mathsf T,
 \qquad
 \tau_B^B=(1/2,-1/4,1/4)^\mathsf T,
 \qquad
 U\tau_B^\alpha=\tau_F^\alpha.
\]

These reduced offsets are frozen along the path; their Cartesian separation varies
through \(A_B(s)\).

The fixed-geometry FCC oriented positive-bond inventory is

\[
 \mathcal B_F=((1,0,0),(0,1,0),(0,0,1),(-1,1,0),(-1,0,1),(0,-1,1)).
\]

The exact oriented common-coordinate inventory is obtained without sign
canonicalization:

\[
 \mathcal B_B=U^{-1}\mathcal B_F
 =((1,0,0),(0,0,1),(1,-1,0),(-1,0,1),(0,-1,0),(1,-1,-1)).
\]

Orientation is retained because the rank-N gauge circuit contains sine harmonics; an
arbitrary sign flip would change the selected gauge field. This is the base positive-bond
inventory \(B\) in the fixed analytic formulas. The un-attacked parent's first and second
harmonics generate frozen translation labels \(\mathcal B_B\) and \(2\mathcal B_B\),
but that fact does not select a truncation ladder. Real-space Hermitian support, when
later selected, must include the conjugates \(-\mathcal B_B\) and
\(-2\mathcal B_B\) separately.

For a lattice displacement \(R\in\mathbb Z^3\) from basis label \(\alpha\) to basis
label \(\beta\), the physical displacement is

\[
 \mathbf d_{R,\alpha\beta}(s)
 =A_B(s)(R+\tau_B^\beta-\tau_B^\alpha),
\]

with length \(\lVert\mathbf d_{R,\alpha\beta}(s)\rVert\) in \(\ell_0\). This formula,
not translation-index distance, owns future basis-aware physical lengths.

## Common state space

For an admitted band-subspace rank \(r\), the selected M0 and M1N controls act at every
path point on the same ordered internal fiber

\[
 \mathcal H_{\mathrm{int},r}
 =\mathbb C^r_{\mathrm{ret}}\oplus\mathbb C^r_{\mathrm{ext}}
 =\mathbb C^{2r},
 \qquad
 F_0=[I_r\;0]^\mathsf T.
\]

On the infinite common cell lattice, every path point uses

\[
 \mathcal H_{B,r}=\ell^2(\mathbb Z^3)\otimes\mathbb C^{2r}.
\]

On an admitted finite common quotient, replace \(\mathbb Z^3\) by that quotient without
changing the internal fiber. The two geometry offsets classify physical support; they do
not introduce a hidden sublattice tensor factor into either selected `2r` analytic
parent control.

At the FCC endpoint the cell-state identification is the unitary permutation

\[
 P_U:\lvert\mathbf n_B,\alpha\rangle_B
 \mapsto\lvert U\mathbf n_B,\alpha\rangle_F,
\]

where the internal label \(\alpha=0,\ldots,2r-1\) is unchanged. After this pullback, all
path points use the same \(\mathbf n_B\) cell labels and the identity on
\(\mathbb C^{2r}\). Operators at different path points may be subtracted only after this
cell/state identification and after their retained bases, gauges, energy units, and
energy references are also declared common.

Lattice dimension `3`, ambient dimension `2r`, band-subspace rank `r`, numerical overlap
rank, and any future model-reduction retained rank remain distinct quantities. This
synthetic M0/M1N representations do not by themselves introduce a genuine
model-reduction rank.

## M1N frozen and metric-varying quantities

For each later admitted M1N case, the following are frozen in common reduced coordinates
for all \(s\):

- the ordered \(\mathbb C^r_{\mathrm{ret}}\oplus\mathbb C^r_{\mathrm{ext}}\) basis and
  retained seed \(F_0\);
- the exact `2r` analytic parent, retained energies, external energies, onsite and hopping
  coefficient matrices, dimensionless energy unit, energy zero, and
  `norm_energy_scale=1`;
- the oriented bond inventory \(\mathcal B_B\), reduced basis offsets, admitted rank,
  depth, parent scale, and attack coefficient;
- the right-acting reduced-coordinate gauge circuit, layer ordering, known inverse, and
  represented retained field; and
- reduced-coordinate Fourier coefficients and translation labels.

Only these geometry-derived quantities may vary with \(s\):

- \(A_B(s)\), \(G_B(s)\), \(K_B(s)\), and the Cartesian wave vector corresponding to a
  fixed reduced \(q_B\);
- physical bond and basis-aware displacement vectors and lengths;
- equality and ordering of complete physical-metric shells;
- physical support radii, shell multiplicities, and retained block counts at a declared
  physical radius; and
- any descriptive locality summary derived solely from those metric quantities.

Consequently the exact common-coordinate M1N operator response is zero. A changed
physical-radius locality summary is a geometry effect, not an operator response. Any
nonzero aligned M1N `Delta H_s` is a numerical/state-identification diagnostic.

## Independent geometry/common-map reference

A future producer-independent reference must reconstruct the geometry from the equations
in this file without invoking the production path owner and must establish:

1. the closed domain \(s\in[0,1]\), positive finite \(t(s)\) and \(l(s)\), and endpoint
   inclusion;
2. the exact column-basis convention and declared direct/reciprocal unit identities;
3. \(\det A_B/\ell_0^3=t^2l/2=1\), \(\det G_B/\ell_0^6=1\), and
   \(A_B^\mathsf TK_B=2\pi I\);
4. the FCC and BCC endpoint aspect ratios, bases, metrics, conventional sides, and common
   orientation;
5. integer \(U\), integer \(U^{-1}\), \(\det U=1\), \(A_B(0)=A_FU\),
   \(G_B(0)=U^\mathsf TG_FU\), and \(q_B=U^\mathsf Tq_F\);
6. basis-offset mapping, the oriented bond mapping without sign canonicalization, and
   complete conjugate partners when support is later admitted;
7. infinite-lattice bijection and finite-quotient bijection for the exact admitted
   quotient; and
8. unitarity of \(P_U\), unchanged internal labels, common \(2r\) fiber identity, and
   exact M0 and M1N path invariance after pullback.

This route verifies declared geometry and state identification only. It does not verify a
mesh, tolerance, locality outcome, response magnitude, resource claim, or material
interpretation.

## Typed unresolved boundary

A future typed geometry qualification must fail closed rather than manufacture a map or
completion. At minimum it must distinguish these stable reasons:

- `PATH_PARAMETER_OUT_OF_DOMAIN`;
- `DIRECT_LENGTH_UNIT_UNDECLARED`;
- `NONFINITE_OR_NONPOSITIVE_PATH_SCALE`;
- `UNIT_VOLUME_CERTIFICATE_FAILED`;
- `RECIPROCAL_DUALITY_FAILED`;
- `FCC_ENDPOINT_IDENTITY_FAILED`;
- `BCC_ENDPOINT_IDENTITY_FAILED`;
- `COMMON_CELL_MAP_FAILED`;
- `FINITE_QUOTIENT_INCOMPATIBLE`;
- `BASIS_OFFSET_MAP_FAILED`;
- `ORIENTED_BOND_MAP_FAILED`; and
- `COMMON_STATE_SPACE_IDENTITY_FAILED`.

These names select scientific failure distinctions, not a wire schema or source enum.
Until a schema is reviewed, they remain documentation-level required outcomes. No failed
geometry qualification may be replaced by a post-hoc coordinate choice, sign
canonicalization, tolerance change, or arbitrary state-space completion.
