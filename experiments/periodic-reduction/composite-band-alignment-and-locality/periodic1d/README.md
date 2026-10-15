# Composite-band alignment and locality

## Identity and status

- Experiment family:
  `ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality`
- Historical alias: Conference Paper 1 `M2`
- Status: `MIGRATION_IN_PROGRESS`
- Immutable experiment version: not assigned
- Retained maintained run: none

This directory is the publication-independent successor boundary for the historical
rank-two periodic-one-dimensional multiband alignment calculation. It does not replace,
rewrite, or relabel historical retained evidence.

## Selected successor contract

The first maintained successor preserves the historical numerical meaning:

- a gapped four-state finite block-hopping parent;
- the lowest two eigenstates as a retained composite space;
- backend-qualified eigenvector-diagonal initial frames;
- polar path transport and closure;
- a known periodic nonidentity right-unitary attack;
- distinct pointwise and one-global-unitary Procrustes families;
- represented matrix Hamiltonians, complete block hoppings, range truncation, and
  disjoint evaluation diagnostics.

Backend-qualified frames retain the numerical backend and version and are not described
as canonical across backends or within degenerate eigenspaces. Pointwise and aggregate
Procrustes operations reject numerically rank-deficient cross-covariances; the protocol
does not select a null-space completion.

## Migration boundary

The current implementation remains under
`python/src/ksdft2effmass/periodic1d/multiband_alignment/` while the isolated historical
64/257 regression under Band Equivalence versus Hopping Locality consumes its result
contract. The active smooth continuum does not depend on that composition. Creating a thin
experiment wrapper or copying that implementation here would violate the selected
owner boundary. The concrete composition moves only when consumers can migrate without
duplication.

Temporary local eigensystem, Procrustes, and transport selection mechanisms are tracked
as [`TECH_DEBT`](../../../../docs/tasks/tech_debt/composite-band-alignment-and-locality/index.md).
Optimization's already-authorized box-quadratic work is not interrupted by this record.

## Documents

- [`protocol.md`](protocol.md) records the publication-independent prospective protocol.
- [Owner boundary](../../../../docs/architecture/v2/ksdft2effmass/periodic/periodic1d/multiband_alignment/owner-boundary.md)
  separates invariant, frame, alignment, transport, and experiment ownership.
- [Identity registry](../../../../docs/architecture/v2/ksdft2effmass/calculation-campaign-identity-registry.md)
  maps the historical alias to this family.

No production calculation, retained run, commit, push, release, or publication action is
authorized by this migration record.
