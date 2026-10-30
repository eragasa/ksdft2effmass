# Provisional seed-structure decision

## Status

**Selected for numerical qualification only.** This record freezes the exact seed
structure \(S_0\) for the first coupled-cutoff and k-point study. It does not accept a
production lattice, authorize a calculator, or transfer numerical evidence from this
structure to a later relaxed structure.

## Exact identity

| Field | Value |
| --- | --- |
| Structure ID | `Si.PrimitiveUnitCell` |
| Role | Provisional bulk-qualification seed \(S_0\) |
| Upstream repository | `https://github.com/eragasa/projectkoios-simulations` |
| Inspected revision | `bbb9f1d8110ed9fe3ea1873c2366073c98f48c71` |
| Repository path | `examples/workflows/pw_dft_scf/structures/Si.PrimitiveUnitCell.json` |
| Byte size | `680` |
| SHA-256 | `6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc` |
| Schema version | `1` |
| Representation | Primitive |
| Vector axis | Columns |
| Lattice parameter | `5.43 angstrom` |

The ordered direct vectors are

\[
\mathbf a_1=5.43\,\text{Å}(1/2,1/2,0),\qquad
\mathbf a_2=5.43\,\text{Å}(1/2,0,1/2),\qquad
\mathbf a_3=5.43\,\text{Å}(0,1/2,1/2).
\]

The ordered fractional sites are `Si: (0,0,0)` and
`Si: (1/4,1/4,1/4)`.

## Decision and rationale

This exact structure is selected because it is already content-addressed by the
ProjectKoios structure library, uses an explicit primitive-cell convention, and can be
consumed without creating a duplicate silicon structure record. Its 5.43 Å lattice is
not promoted as a calculated PBE equilibrium value. The subsequent zero-pressure
structural stage and fresh setting confirmation exist specifically to prevent that
promotion.

The initial numerical result must therefore be labelled \(Q_0@S_0\). It is valid only
for this exact structure and declared physical model. It cannot be relabelled as
qualified on a mechanically relaxed \(S_1\), even if the same integer k-mesh or cutoff
labels are later used.

## Nonclaims and remaining gates

This decision does not:

- accept the 5.43 Å lattice as the production structure;
- select or acquire the required PseudoDojo v0.5 stringent Si UPF2 artifact;
- freeze coupled-cutoff coordinates, reciprocal-sampling coordinates, observables,
  tolerances, structural cell mode, force/pressure criteria, or feedback budget;
- accept an executable or toolchain;
- authorize any SCF, relaxation, or other calculator occurrence; or
- make retained ProjectKoios SSSP/QE observations transferable to this calculation.

Before any setting-qualification authorization packet can exist, the remaining
scientific declaration and software-readiness gates in [`readiness.md`](readiness.md)
and [`scientific-contract.md`](scientific-contract.md) must be closed.
