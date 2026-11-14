# `Periodic1DRank1BlochHoppingModel`

## Status

Implemented immutable rank-one specialization of the dimension-neutral and
periodic-1D Bloch-hopping model hierarchy, composed from PhysKit's
`DenseBlockHoppingModel`. Its scientific role is fixed as `REDUCED_MODEL`; callers do not
supply a toy or material-reference role.

## Ownership

PhysKit owns reusable displacement, coefficient-block, unit, basis, energy-reference,
and hopping-model storage. KSD owns the periodic-1D retained-dimension-one scientific
boundary and its analysis policy. The KSD model therefore wraps the exact PhysKit model
rather than copying its terms into a competing representation.

## Mathematical object

For ordinary integer displacements \(R\in\mathbb Z\), the model represents

\[
H(q)=\sum_R T_R e^{2\pi i qR}, \qquad T_R\in\mathbb C^{1\times1},
\]

with exact Hermiticity

\[
T_{-R}=T_R^\dagger.
\]

The retained-space dimension is one. This is not a claim about the algebraic rank of a
coefficient matrix.

## Enforced boundaries

- the lattice dimension is exactly one;
- every coefficient block has shape `1 x 1`;
- lattice geometry and its physical length unit are explicit;
- one physical PhysKit `UnitSystem` supplies coherent length, mass, action, and energy
  units;
- the wrapped PhysKit model energy unit must equal the selected unit system's energy
  unit, while energy-reference and basis identities remain explicit;
- normalized dimensionless values are dimensionalized by the declared lattice
  kinetic-energy scale before model construction;
- every displacement has an exact conjugate partner, including the onsite block; and
- model values are operationally immutable.

A complete finite-DFT coefficient inventory is a cyclic representation and is not
silently admitted as an ordinary-lattice hopping model. Cyclic-to-ordinary conversion
must remain an explicit separately qualified operation.

## Unit behavior

The lattice period retains its explicit physical length unit. The natural scale is

\[
E_a=\frac{\hbar^2}{m_e a^2},
\]

without the kinetic-operator factor `1/2`. In `UnitSystem.ATOMIC`, `hbar = 1`,
`m_e = 1`, and `a = 1 bohr`, so `E_a = 1 hartree` within binary64 arithmetic.

Coefficient blocks retain the exact physical energy unit selected by `UnitSystem`.
Changing representation means selecting another coherent unit system and explicitly
converting the complete PhysKit model; the KSD owner rejects a model/unit-system
mismatch. PhysKit rejects mixed coefficient/model units, and KSD rejects
`UnitSystem.NONDIMENSIONAL` at this physical model boundary. The model identity binds
the scale convention, source length unit, coherent unit system, energy unit,
energy-reference identity, and ordered basis identity.

## Scientific separation

The model is distinct from:

1. the exact four-state ambient parent operator;
2. the selected lowest-eigenvalue scalar field;
3. a finite cyclic Fourier representation of that field; and
4. any deliberately support-truncated ordinary hopping model constructed later.

Model construction alone establishes no band isolation, continuum convergence, material
validity, evidence promotion, or scientific validation.

## Navigation

- [Numerical behavior and pytest evidence](numerics.md)
