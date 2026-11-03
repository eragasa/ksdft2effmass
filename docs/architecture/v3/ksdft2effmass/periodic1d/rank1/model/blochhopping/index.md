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
- energy unit, energy-reference identity, and basis identity remain owned by the wrapped
  PhysKit model;
- coefficient units must be physical energy units; normalized dimensionless values must
  be dimensionalized by the declared lattice kinetic-energy scale before model
  construction;
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

without the kinetic-operator factor `1/2`. Thus the corresponding reduced convention has
`hbar = 1`, `m_e = 1`, `a = 1`, and `E_a = 1`; when `a = 1 bohr`, `E_a` is one Hartree
within the declared physical-constant precision.

Coefficient blocks retain one exact common physical energy unit supplied by PhysKit. The
model performs no implicit conversion: callers use `ModelSystemUnitConverter` before
construction when changing energy units. PhysKit rejects mixed coefficient/model units,
and KSD rejects `Unitless` or physical units without energy dimensionality at this model
boundary. The model identity binds the scale convention, length unit, energy unit,
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
