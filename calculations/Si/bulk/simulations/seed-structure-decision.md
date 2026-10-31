# Provisional seed-structure decision

## Status

**Selected for numerical qualification only.** This record freezes the right-handed
exact seed structure \(S_0\) used by the retained fixed-cutoff k-point study. It does
not accept a production lattice, authorize another calculator occurrence, or transfer
numerical evidence from this structure to a later relaxed structure.

## Exact identity

| Field | Value |
| --- | --- |
| Structure ID | `Si.PrimitiveUnitCell.RightHanded` |
| Role | Provisional k-point-convergence seed \(S_0\) |
| Owning repository path | [`structures/Si.PrimitiveUnitCell.RightHanded.json`](structures/Si.PrimitiveUnitCell.RightHanded.json) |
| Byte size | `692` |
| SHA-256 | `7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a` |
| Schema version | `1` |
| Representation | Primitive |
| Vector axis | Columns |
| Lattice parameter | `5.43 angstrom` |
| Handedness | Right-handed; dimensionless determinant `+0.25` |

The ordered direct vectors are

\[
\mathbf a_1=5.43\,\text{Å}(1/2,0,1/2),\qquad
\mathbf a_2=5.43\,\text{Å}(1/2,1/2,0),\qquad
\mathbf a_3=5.43\,\text{Å}(0,1/2,1/2).
\]

The ordered fractional sites are `Si: (0,0,0)` and
`Si: (1/4,1/4,1/4)`.

## Exact derivation

The parent is the 680-byte ProjectKoios `Si.PrimitiveUnitCell` record with
SHA-256 `6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc`.
Its ordered basis is left-handed. The derived record swaps the first two direct
vectors and applies the same permutation to fractional-coordinate components:

\[
H_{S_0}=H_{\mathrm{parent}}P,
\qquad
f_{S_0}=P^{\mathsf T}f_{\mathrm{parent}},
\qquad
P=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}.
\]

The two fractional sites are numerically unchanged because their first two
components are equal. This operation preserves Cartesian geometry and volume
magnitude while changing the direct-basis determinant from `-0.25` to `+0.25`.
The complete derivation contract is retained in
[`structures/README.md`](structures/README.md).

## Decision and rationale

The right-handed record replaces the left-handed parent for subsequent
calculator inputs. It preserves the previously selected provisional 5.43 Å
geometry while removing Quantum ESPRESSO's `axis vectors are left-handed`
warning. Its 5.43 Å lattice is not promoted as a calculated PBE equilibrium
value.

Any numerical result must remain bound to the exact structure bytes used. The
completed left-handed SSSP/QE development run retains the parent structure identity
and cannot be relabelled as evidence generated from this derived record. The separately
authorized right-handed runs retain their exact inputs under [`evidence/`](evidence/).
The shifted run is superseded for setting selection by the Gamma-centered k-point and
cutoff campaigns, but remains immutable evidence.

## Provisional relaxed successor

The separately authorized FCC-native volume-only relaxation produced provisional
`Si.PrimitiveUnitCell.RightHanded.RelaxedS1`, byte size `758`, SHA-256
`d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`, with
conventional cubic lattice parameter `5.469182093640207 angstrom`. This does not
change the identity or role of \(S_0\). The exact \(S_1\) bytes begin a new
structure-scoped setting-confirmation branch; \(Q_0@S_0\) is not transferred.

## Nonclaims and remaining gates

This decision does not:

- accept the 5.43 Å lattice as the production structure;
- select the SSSP development branch as the eventual production parent model;
- establish cutoff or k-point convergence from the basis transformation alone;
- accept an executable or toolchain;
- authorize another SCF, relaxation, or other calculator occurrence; or
- make left-handed-parent observations byte-identical to a right-handed run.
