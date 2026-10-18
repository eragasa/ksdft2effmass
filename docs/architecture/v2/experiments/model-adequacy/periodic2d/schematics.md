# Periodic 2-D schematics

## Experiment sequence

The periodic-2D package contributes the first and third stages of the selected sequence.

- Isotropic 2-D establishes the square-symmetric baseline.
- Isotropic 3-D then isolates dimensional extension.
- Anisotropic 2-D later isolates removal of axis-permutation symmetry.
- Anisotropic 3-D combines both stresses last.

```mermaid
flowchart LR
    iso2["isotropic 2-D"] --> iso3["isotropic 3-D"]
    iso3 --> aniso2["anisotropic 2-D"]
    aniso2 --> aniso3["anisotropic 3-D"]
```

## Two-dimensional ownership

Reusable geometry flows inward while scientific composition stays with each child.

- PhysKit supplies reviewed lattice primitives.
- KSD capabilities supply reviewed reusable analysis.
- Each experiment supplies its parent, orbits, channels, controls, and evidence.

```mermaid
flowchart TB
    physkit["PhysKit lattice geometry"] --> iso2["isotropic 2-D experiment"]
    physkit --> aniso2["anisotropic 2-D experiment"]
    analysis["reviewed KSD analysis"] --> iso2
    analysis --> aniso2
    iso2 --> evidence1["family-local evidence"]
    aniso2 --> evidence2["family-local evidence"]
```
