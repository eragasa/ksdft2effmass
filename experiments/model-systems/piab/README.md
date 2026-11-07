# Particle-in-a-box experiment family

This publication-independent family groups particle-in-a-box experiments by spatial
dimension:

- [`piab1d/`](piab1d/) — existing one-dimensional finite-representation diagnostics;
- [`piab2d/`](piab2d/) — prospective orthogonal rectangular-box extension; and
- [`piab3d/`](piab3d/) — prospective orthogonal rectangular-cuboid extension.

The family path is structural. Each dimensional child has its own scientific question,
version identity, protocol, resource bounds, verifier, and evidence status. Results and
tolerances do not transfer between dimensions.

## Ownership

PhysKit owns reusable particle-in-a-box physical models and reusable analytical or
finite-difference solvers. KSD owns experiment selection, cross-representation
diagnostics, schemas, provenance, verification policy, acceptance policy, and retained
interpretation. Experiment code must consume PhysKit rather than duplicate those
models or solvers.

## Experiment and calculation trees

The maintained experiment paths are:

```text
experiments/model-systems/piab/piab1d/
experiments/model-systems/piab/piab2d/
experiments/model-systems/piab/piab3d/
```

A retained run, if one is later produced, uses the corresponding calculation path:

```text
calculations/model-systems/piab/<dimension>/runs/<run-id>/
```

A calculation directory is created only for an actual run or retained attempt. Planned
work remains under `experiments/`; it is not represented as a nonexistent calculation.
Historical files remain at their original paths until a separately reviewed provenance
migration. Crosswalks may point to those files but must not silently copy or rewrite
them.

## Current lifecycle

| Experiment | Status | Retained evidence |
|---|---|---|
| PIAB1D | Existing calculated experiment; normalization in progress | Historical retained package under `calculations/research-monograph/particle-in-box/` |
| PIAB2D | Prospective protocol | None |
| PIAB3D | Prospective protocol with a finite-difference owner gap | None |

No entry in this index authorizes a retained-evidence calculation.
