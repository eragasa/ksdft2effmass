# Periodic 3-D schematics

## Child relationship

The isotropic and anisotropic children share evidence vocabulary but not experiment
identity or exact controls.

- Isotropic 3-D is implemented before anisotropic 2-D.
- Anisotropic 3-D is implemented after the anisotropic 2-D stage.
- Results and thresholds do not transfer between children.

```mermaid
flowchart LR
    iso2["isotropic 2-D"] --> iso3["isotropic 3-D"]
    iso3 --> aniso2["anisotropic 2-D"]
    aniso2 --> aniso3["anisotropic 3-D"]
```

## Geometry ownership

Reusable geometry and experiment-specific symmetry enter through separate owners.

- PhysKit supplies direct, reciprocal, and metric primitives.
- Each child verifies the symmetry action admitted by its parent.
- Each child constructs its own support orbits and evidence.

```mermaid
flowchart TB
    physkit["PhysKit 3-D lattice geometry"] --> iso3["isotropic 3-D experiment"]
    physkit --> aniso3["anisotropic 3-D experiment"]
    cubic["cubic signed permutations"] --> iso3
    orthorhombic["sign orbits without permutations"] --> aniso3
    iso3 --> evidence1["family-local evidence"]
    aniso3 --> evidence2["family-local evidence"]
```
