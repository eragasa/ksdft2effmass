# Anisotropic 3-D schematics

## Scientific construction

The experiment builds anisotropic sign orbits from an exact orthorhombic scalar parent
before evaluating nested support classes.

- Lattice geometry fixes physical vectors and reciprocal coordinates.
- Parent symmetry permits signs but not axis permutations.
- Support groups define the experiment-specific hierarchy.
- Both channels consume the same maximal coefficient embedding.

```mermaid
flowchart LR
    lattice["orthorhombic lattice"] --> signs["verified sign symmetry"]
    parent["exact scalar hopping parent"] --> signs
    signs --> orbits["ten ordered orbit coefficients"]
    orbits --> classes["four nested support classes"]
    classes --> spectral["weighted spectral channel"]
    classes --> operator["complete-block operator channel"]
    spectral --> evidence["witness / lower bound / unresolved"]
    operator --> evidence
```

## Evidence flow

Objective construction, verification, and evaluation have separate roles.

- Objective construction defines channel quadratics.
- Producer search proposes candidates and directions.
- Independent verification reconstructs decisive evidence.
- Evaluation and locality diagnostics occur downstream.

```mermaid
flowchart TB
    objective["9 x 11 x 13 objective-construction mesh"] --> producer["producer search"]
    objective --> verifier["exact-rational verifier route"]
    producer --> proof["candidate and proof objects"]
    proof --> verifier
    verifier --> result["verified bounded result"]
    result --> evaluation["shifted evaluation mesh and locality"]
```

## Sequencing role

The package is preserved as the final concrete stress stage.

- Isotropic 3-D isolates dimension first.
- Anisotropic 2-D isolates symmetry removal second.
- This package combines both only after those stages.

```mermaid
flowchart LR
    iso3["isotropic 3-D"] --> aniso2["anisotropic 2-D"]
    aniso2 --> aniso3["anisotropic 3-D"]
```
