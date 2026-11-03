# `ksdft2effmass.periodic1d.model.blochhopping`

Periodic-1D specialization of the dimension-neutral Bloch-hopping model contract. It
adds an explicit `Periodic1DLatticeGeometry`, the lattice kinetic-energy scale
`E_a = hbar^2 / (m_e a^2)` without a factor `1/2`, and the enforced one-dimensional
scientific-model identity. Rank-one, rank-two, and rank-N models remain sibling
specializations beneath this owner.

## Navigation

- [Numerical behavior and pytest evidence](numerics.md)
