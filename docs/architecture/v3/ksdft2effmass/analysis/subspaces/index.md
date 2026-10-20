# `ksdft2effmass.analysis.subspaces`

## Purpose and status

This prospective analysis subpackage owns reusable analyses whose primary operands are
typed finite subspaces rather than represented operators.

## Child map

- [`comparison`](comparison/index.md) — projector comparison of two compatible
  orthogonal subspaces.

## Ownership boundary

The subpackage does not construct subspaces, solve eigenproblems, reduce operators,
choose norms, or aggregate experiment diagnostics.

## Dependency rules

It may consume `ksdft2effmass.spaces.subspaces` and the implemented legacy
`operators.subspaces.OrthogonalSpectralSubspace` during the bounded transition. It must
not import model systems, experiments, calculations, or serializers.

## Evidence

Prospective architecture only. No implementation, tests, or supported export exists
yet.
