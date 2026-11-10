# Diamond Slater--Koster $sp^3s^*$ foundation

## Scope

`ksdft2effmass.model_systems.slater_koster` is the KSD-owned concrete composition for
one spinless, orthogonal, homopolar diamond $sp^3s^*$ model through second neighbors.
The package consumes reusable Slater--Koster mechanics from the published Project
Koios PhysKit owner. It does not fit parameters, compare to a target, infer evidence,
or accept a silicon model.

The represented basis is the exact ordered ten-coordinate value

```text
(diamond_origin_center:s, p_x, p_y, p_z, s_star,
 diamond_body_diagonal_quarter_center:s, p_x, p_y, p_z, s_star)
```

with the declared $s^*$ orbital understood as radial channel one of the $s$
component. Basis compatibility remains exact and order-sensitive.

## KSD ownership

KSD retains:

- the positive-determinant FCC primitive basis and the two diamond orbital centers;
- four unique origin-center-to-quarter-center first-neighbor representatives and the
  six positive second-neighbor representatives on each center;
- the concrete fifteen-parameter order and the fixed zero first-neighbor $ss^*$ and
  $s^*s^*$ channels;
- onsite composition and the declared onsite-parameter-defined energy reference;
- correlation from the PhysKit spatial basis to KSD's three-dimensional structured
  periodic basis;
- the full-center Bloch evaluation wrapper and its KSD Hamiltonian value; and
- deterministic typed-JSON serialization of this concrete model definition.

## PhysKit ownership

The pinned PhysKit dependency at revision
`173ba998a0cf9ce2731182893d0e2118da9b35d8` owns the reusable structured
Slater--Koster basis,
directed bonds and normalized bond directions, seven two-center channel records,
$sp^3s^*$ hopping construction, Hermitian reverse generation, ordinary-cell assembly,
block-hopping Bloch evaluation, and cell-to-full-center orbital gauge transformation.
KSD neither copies those implementations nor exposes compatibility aliases for the
retired calculation incubation.

## Wire boundary

`DiamondSp3sStarModelJsonSerializer` emits model schema version 3. It embeds the
existing KSD schema-version-2 structured periodic basis, the concrete geometry and
parameter inventory, fixed first-shell zero channels, the full-center phase
convention, and the reusable-mechanics owner. The wire contains no fitted vector,
residual, target samples, uncertainty, verification result, or acceptance statement.

## Scientific boundary

This foundation defines a finite represented operator family only. It does not claim
that the parameterization is fitted, adequate, transferable, validated for silicon, or
admitted to a common comparison space. In particular, it does not alter S110's
retained `blocked-orbital-alignment-rank-deficient-no-fit` disposition, and it does not
satisfy the missing independent CSD1 verification.

See [implementation](implementation.md) and [numerics](numerics.md).
