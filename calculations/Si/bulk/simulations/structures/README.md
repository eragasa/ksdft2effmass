# Bulk-silicon structure records

## `Si.PrimitiveUnitCell.RightHanded.json`

This is the right-handed provisional seed structure for subsequent bulk-silicon
k-point calculations.

| Field | Value |
| --- | --- |
| Structure ID | `Si.PrimitiveUnitCell.RightHanded` |
| Byte size | `692` |
| SHA-256 | `7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a` |
| Schema version | `1` |
| Representation | Primitive |
| Vector axis | Columns |
| Lattice parameter | `5.43 angstrom` |

The parent is ProjectKoios
`examples/workflows/pw_dft_scf/structures/Si.PrimitiveUnitCell.json`, byte size
`680`, SHA-256
`6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc`.
The deterministic direct-basis transformation swaps the first two basis vectors:

\[
H_{\mathrm{right}}=H_{\mathrm{parent}}P,
\qquad
P=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix},
\qquad \det P=-1.
\]

Fractional coordinates transform as
\(f_{\mathrm{right}}=P^{\mathsf T}f_{\mathrm{parent}}\). Both silicon sites are
unchanged numerically because their first two fractional components are equal.
The dimensionless direct-lattice determinant changes from `-0.25` to `+0.25`;
Cartesian geometry, volume magnitude, species order, and lattice parameter are
unchanged. Reciprocal-fractional coordinates for the same physical vector obey
the same first-two-component swap.

This is an exact basis re-expression, not a relaxation or a new physical
structure. Numerical evidence generated from the left-handed parent must retain
its original structure identity and is not silently relabelled.

## `Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json`

This is the provisional zero-pressure relaxed structure obtained from the exact
seed above by the separately authorized FCC-native QE 7.5 volume-only
relaxation.

| Field | Value |
| --- | --- |
| Structure ID | `Si.PrimitiveUnitCell.RightHanded.RelaxedS1` |
| Byte size | `758` |
| SHA-256 | `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03` |
| Schema version | `1` |
| Representation | Primitive |
| Vector axis | Columns |
| Conventional cubic lattice parameter | `5.469182093640207 angstrom` |
| Primitive volume | `40.898479123515415 angstrom^3` |

The retained QEXSD was parsed with the existing KSD QEXSD parser. ProjectKoios
restored the parsed QE `ibrav=2` cell to the maintained right-handed source basis.
The QEXSD-native second-site fractional representative is approximately
`(0.75, 0.75, 0.75)`; the restored source-basis representative is approximately
`(0.25, 0.25, 0.25)`. The direct-basis determinant remains positive.

This record is provisional \(S_1\), not an accepted production structure. The
Gamma-centered k-point and cutoff settings must be confirmed afresh on this exact
structure before a stable structure/settings pair can be considered.
