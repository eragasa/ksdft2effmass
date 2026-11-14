# `ksdft2effmass.periodic.periodic1d.models.blochhopping`

Periodic-1D specialization of the dimension-neutral Bloch-hopping model contract. It
adds an explicit `Periodic1DLatticeGeometry`, a selected physical PhysKit `UnitSystem`,
and the lattice kinetic-energy convention
`E_a = hbar^2 / (m_e a^2)` without a factor `1/2`.

PhysKit owns coherent length, mass, action, and energy units plus Pint conversion
mechanics. KSD owns the lattice-specific selection of `a`, the omission of `1/2`, and
composition into its reduced-model parameterization. The finite-rank Bloch-hopping
owner refines this dimensional contract, and the rank-two owner in turn refines that
finite-rank capability. The maintained rank-one family remains a separate fixed-rank
specialization.

## Navigation

- [Numerical behavior and pytest evidence](numerics.md)
