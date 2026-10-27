# Single-band Fourier-reduction experiments

> **Migration status:** this container and its complete child tree are assigned to
> [`calculations/mathieu1d/`](../../../calculations/mathieu1d/); the authoritative
> checklist is [`calculations/mathieu1d/migration.md`](../../../calculations/mathieu1d/migration.md).

This family-first directory groups dimension-specific maintained experiments that reduce
one isolated scalar band to a finite Fourier/hopping representation.

The directory is organizational, not itself an experiment-family, version, run, or
evidence identity. Each dimensional child owns its own stable family identity because
its lattice geometry, coefficient domain, Fourier arithmetic, diagnostics, and evidence
contract differ.

## Maintained dimensions

- [`periodic1d/`](periodic1d/) — implemented immutable version `v1`, with independently
  verified retained evidence and exact historical-M1 provenance.

No `periodic2d/` or `periodic3d/` child is created yet. Those children belong here only
after their parent, geometry, state space, transform convention, sample roles, schemas,
verification boundary, and evidence policy are reviewed. The two-dimensional hopping-
shell hierarchy remains a separate model-adequacy experiment; it must not be relabeled
as a single-band reduction merely because it consumes related Fourier capabilities.
