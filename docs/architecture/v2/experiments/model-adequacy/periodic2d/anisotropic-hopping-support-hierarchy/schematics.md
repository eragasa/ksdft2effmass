# Anisotropic 2-D schematics

## Scientific construction

The future experiment will separate lattice geometry, model symmetry, and directional
support policy before constructing evidence.

- Lattice vectors define physical geometry.
- Verified symmetry defines coefficient orbits.
- Support policy defines nested classes.
- Channels evaluate one common coefficient vector.

```mermaid
flowchart LR
    lattice["full-rank 2-D lattice"] --> symmetry["verified model symmetry"]
    parent["exact scalar parent"] --> symmetry
    symmetry --> orbits["directional coefficient orbits"]
    orbits --> hierarchy["nested support classes"]
    hierarchy --> channels["spectral and operator channels"]
    channels --> evidence["witness / certificate / unresolved"]
```

## Sequencing role

The stage isolates anisotropy before the final anisotropic three-dimensional experiment.

- It follows isotropic 3-D.
- It precedes anisotropic 3-D.
- It does not inherit results from either neighbor.

```mermaid
flowchart LR
    iso3["isotropic 3-D"] --> aniso2["anisotropic 2-D"]
    aniso2 --> aniso3["anisotropic 3-D"]
```
