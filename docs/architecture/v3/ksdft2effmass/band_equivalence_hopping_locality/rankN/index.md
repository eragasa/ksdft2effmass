# Periodic rank-N common ownership

## Status and scope

`ksdft2effmass.band_equivalence_hopping_locality.rankN` is the
cross-dimensional owner for behavior that is both periodic and arbitrary-finite-rank but
binds no two- or three-dimensional geometry. It is a source-ownership layer, not a new
scientific protocol, calculation, retained result, or evidence claim.

The package initializer is inert. Concrete periodic-2D and periodic-3D requests,
analyses, analyzers, results, geometry, transport topology, protocol selections, wire
identities, and serialization remain in their dimensional rank-N packages.

## Installed modules

| Module | Responsibility |
|---|---|
| `base.py` | Common periodic rank-N aggregate capability, request, analysis, analyzer, case, value, and action roles. |
| `result.py` | Dimension-neutral immutable parents for aggregate error channels, locality summaries, support outcomes, and alignment evidence. |
| `analysis.py` | Internal production-only coordinate-grid, finite-Fourier transform/evaluation, ordinary-mode, right-action, and alignment-identity arithmetic. |
| `reference.py` | Internal independent parent, gauge, gap, polar-alignment, and expected-evidence reconstruction shared across dimensions. |
| `fourier_reference.py` | Internal direct dense finite-Fourier, shell-evaluation, error-channel, and support-selection reconstruction. |

The dimension-qualified roles inherit both their dimensional aggregate owner and the
matching common rank-N role. Periodic-2D and periodic-3D classes remain siblings; neither
inherits from the other. Rank-two classes do not inherit these rank-N roles.

The dimension-qualified leaf-result classes retain their existing names and exact runtime
types. Aggregate validation continues to require those exact dimensional types, so a
common parent value cannot replace a periodic-2D or periodic-3D value at a dimensional
boundary.

## Scientific and numerical boundaries

The installed extraction centralizes nominal ownership, validation, and arithmetic that
has the same mathematical definition in two and three dimensions. Spatial dimension is
an explicit input or concrete class constant. It does not select geometry, transport
topology, mesh sizes, gauge families, support policy, tolerances, or dimensional result
types, and it does not change any numerical result.

Production and independent-reference implementations remain separate. `analysis.py`
uses the installed production Fourier owners. `reference.py` reconstructs parent and
alignment formulas without the maintained model owner, while `fourier_reference.py`
uses explicit dense sums without the production transformer, evaluator, shell
classifier, hopping-locality analyzer, or support selector. Neither reference module
inherits or calls the production arithmetic parent.

In particular, locality-summary validation preserves the existing relation
`total_power = onsite_power + nononsite_power` within its installed tolerance. The
producer-side subtraction and clipping limitation recorded as `TD-BEL-003` is unchanged.

Any later extraction must preserve this route separation. Production and independent
reference code must not call a common numerical implementation for the same quantity
under verification.

## API boundary

The common classes are imported from their owning `rankN.base` and `rankN.result`
modules. They are not re-exported by the inert package initializer or by the aggregate
package root. Existing dimension-qualified public import paths and canonical wire bytes
remain unchanged.
