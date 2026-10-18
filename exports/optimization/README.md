# Project Koios Optimization transfer boundary

## Status

The earlier quadratic draft was superseded by the owner implementation in
`projectkoios-optimization` commit
`ec3d2907097a659aef4be2b3384bd1922a9cb4dc`, published on `origin/main`. New active,
non-runtime affine-quadratic and diagonal-metric candidates are staged as flattened
source files in this directory, with contracts under
[`optimization/`](optimization/README.md).

The superseded uncommitted donor bytes were preserved non-destructively outside the
repository at:

```text
/Users/eugene/recovery/ksdft2effmass-optimization-export-superseded-20261011T182820Z
```

Its `RECOVERY.json` SHA-256 is
`ffc7858f2645d76ecec578024a81bac60c3562b9e1a4ff7ea5a976063e1cd11f`.
That recovery bundle is provenance only, not a supported API or transfer candidate.

## Accepted upstream owner surface

The dependency-owned facade is:

```python
from projectkoios.optimization.quadratic.quadratic import PositiveDefiniteQuadraticLoss
```

Construction selects the NumPy dense backend by default and the SciPy CSR backend with
`sparse=True`. The facade exposes immutable `center`, `matrix`,
`minimum_squared_loss`, `dimension`, and `sparse` properties plus `squared_loss()` and
`root_loss()`.

The reusable object is unit-free. Optimization owns backend selection, numerical
storage, positive-definiteness acceptance, and quadratic evaluation. It does not choose
physical dimensions, units, conversion, normalization, scientific weights, thresholds,
admissibility, certificate meaning, or evidence disposition.

## Existing upstream APIs reused directly

The target also owns
`projectkoios.optimization.spaces.parameters.ParameterBound` and `ParameterSpace`,
including inclusive closed bounds and exact fixed coordinates with equal endpoints. KSD
consumes these APIs from an exact-pinned dependency; they are deliberately not copied
into `exports/`.

## Active and remaining Optimization-bound candidates

The active source candidate supplies:

- weighted affine-residual quadratic construction over the existing quadratic facade;
  and
- positive diagonal unit-free distance and dual-norm geometry.

Generic box-constrained feasibility, reconstructable minimum bounds, common-witness
search, set distance, support optimization, and directed rounding remain prospective
and have no staged source bytes here.

Any candidate must be reviewed by the Optimization owner and removed from active
transfer staging once an accepted upstream implementation supersedes it.

## Exclusions

A contract requiring physical dimensions, units, dimensional conversion, or physical
interpretation belongs to PhysKit instead. KSD retains scientific normalization, channel
meaning, HSH controls, thresholds, admissibility and certificate interpretation,
retained schemas, evidence roles, and workflow composition.
