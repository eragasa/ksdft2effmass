# `ksdft2effmass.periodic1d.multiband_alignment.calculate`

## Purpose and status

Implemented M2 producer module for frame transport, gauge attack, pointwise/global
alignment, represented-operator transformation, and locality diagnostics.

## Public contract

- [`Periodic1DMultibandAlignmentCalculator`](Periodic1DMultibandAlignmentCalculator/index.md)

`execute(definition)` accepts the exact M2 definition and returns one immutable M2
result. Private methods own the nontrivial finite protocol: external-gap evaluation,
eigenframes, attack rotations, global rotation, frame/operator defects, and range
studies.

## Ownership and dependencies

The calculator owns orchestration. Reusable frame, Procrustes, projection, Fourier,
truncation, and Hermiticity operations remain with their domain Actions. The module has
no external execution or file I/O.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/multiband_alignment/calculate.py`.
See [implementation](../implementation.md), [scientific](../scientific.md), and
[testing](../testing.md).

## Limitations

The global channel is one unitary over the path; no arbitrary momentum-dependent gauge
optimization is claimed.
