# Isotropic 3-D schematics

## Scientific construction

The experiment combines an exact cubic scalar parent with cubic orbit reduction and two
adequacy channels.

- Geometry and model symmetry are verified before orbit construction.
- Support classes add complete cubic orbits.
- Both channels evaluate one common coefficient vector.
- Evaluation diagnostics occur after decisive evidence is fixed.

```mermaid
flowchart LR
    lattice["simple-cubic lattice"] --> symmetry["verified cubic action"]
    parent["exact scalar parent"] --> symmetry
    symmetry --> orbits["signed-permutation orbits"]
    orbits --> hierarchy["nested support classes"]
    hierarchy --> channels["spectral and operator channels"]
    channels --> evidence["witness / certificate / unresolved"]
    evidence --> evaluation["evaluation and locality"]
```

## Sequencing role

The stage isolates dimensional extension before anisotropy is introduced.

- It follows isotropic 2-D.
- It precedes anisotropic 2-D.
- It does not inherit the first stage's thresholds or results.

```mermaid
flowchart LR
    iso2["isotropic 2-D"] --> iso3["isotropic 3-D"]
    iso3 --> aniso2["anisotropic 2-D"]
```
