# Construction-mesh adequacy recommendation

This directory prepares the no-calculator successor recommendation recorded first in
[`research-protocol.tex`](../../research-protocol/research-protocol.tex). The protocol
source bound by this preparation has SHA-256
`7822d6365e05e5bb479f318d5235717d60b29368f049078defe9d991cd6fac04`.

The prior rank-10, Gamma-origin `4x4x4` Wannier operator remains provider-eligible and
structurally valid, but its authenticated 408-point direct-parent comparison found it
not adequate for the declared intended use. The first successor, `C6`, changes only the
construction mesh to Gamma-origin `6x6x6`. Structure, parent, cutoffs, band count, rank,
windows, projections, and localization controls remain fixed. `C8` is conditional and
is not an automatic successor. `C12` is a bounded upper mesh diagnostic available only
after a completed `C8` review continues to support the mesh-density hypothesis; it is
not evidence of infinite-mesh convergence by size alone.

The already revealed 408-point parent data are development evidence for successors,
not a new holdout. The prospectively frozen successor-confirmation geometry contains
402 parent-informed but parent-value-unobserved points. It uses six symmetry-projected
centers at the mean revealed parent-valley radius and full three-dimensional rotated
quadratic stencils. It is disjoint from the `4x4x4`, `6x6x6`, `8x8x8`, and `12x12x12`
Gamma-origin meshes and from the revealed 408-point set.

## Files

- [`prepare_recommendation.py`](prepare_recommendation.py) authenticates the source
  structure, failed-candidate validation, revealed-point manifest, eligible Wannier90
  input, and research protocol before deriving the recommendation.
- [`construction-mesh-candidates.json`](construction-mesh-candidates.json) records the
  exact ordered `C6` mesh, conditional `C8` mesh, and bounded diagnostic `C12` mesh.
- [`successor-confirmation-holdout.json`](successor-confirmation-holdout.json) records
  the exact 402-point confirmation geometry and disjointness checks.
- [`recommendation.json`](recommendation.json) binds the one-variable `C6` decision,
  fixed coordinates, conditional `C8` and `C12` boundaries, finite-model nonclaim, and
  downstream scientific stop.
- [`authorization-boundary.json`](authorization-boundary.json) records that preparing
  the recommendation was authorized but no calculator invocation, artifact acquisition,
  or retry was authorized.

## Identities

| Artifact | SHA-256 |
|---|---|
| `construction-mesh-candidates.json` | `1e5ebb9dffa6a97a2f2445cfd6290aff4cd3d6c06c15e4e0e7d6bbde7826c803` |
| `successor-confirmation-holdout.json` | `51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8` |
| `recommendation.json` | `990eeae5b57b91a9b81ab39a23ef54510e130967aa9f1236de79c5408fdebf87` |
| `authorization-boundary.json` | `2a981b137a59704044b86e1fad96293d7278ab99ffaf24682395c70b7733dbfb` |

## Authorization boundary

At recommendation preparation time, no QE or Wannier90 executable was invoked. The
subsequent exact `C6` NSCF preflight and its separately authorized one-invocation result
are retained under the simulations preflight and evidence trees. That NSCF is an
eligible handoff only. Preprocessing, conversion, and localization remain distinct
calculator occurrences requiring separate exact bounded authorization. The frozen
402-point confirmation set must not be evaluated by the direct parent until one
successor candidate and its predictions are frozen.
