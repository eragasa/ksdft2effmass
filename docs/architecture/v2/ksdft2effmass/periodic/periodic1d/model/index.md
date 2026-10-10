# `ksdft2effmass.periodic1d.model`

## Purpose and status

This implemented module owns the canonical controlled one-dimensional parent-model
records used by M1 and M2. Models are immutable scientific definitions; they do not
execute calculations or encode retained result identities.

## Public contract

- [`Periodic1DFourierHamiltonianToyModel`](Periodic1DFourierHamiltonianToyModel/index.md)
  binds a finite real Fourier potential, direct/reciprocal duality, and recoil-energy
  scale.
- [`Periodic1DBlockHamiltonianToyModel`](Periodic1DBlockHamiltonianToyModel/index.md)
  binds finite matrix-valued hopping blocks and their Hermiticity tolerance.

Both satisfy `Periodic1DModel` and return `PeriodicModelRole.TOY`.

## Ownership and dependencies

The module owns model-level validation and stable identities. Potential evaluation,
hopping interpolation, eigensolution, retention, reduction, and campaign policy remain
with their domain owners. It depends on unit-aware quantities and reusable periodic
records, not on milestone packages.

## Code mapping

| Code path | Qualified symbol | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic1d/model.py` | `Periodic1DFourierHamiltonianToyModel` | Scalar Fourier parent definition |
| same | `Periodic1DBlockHamiltonianToyModel` | Matrix hopping parent definition |

## Test and Sphinx mapping

Direct construction behavior is exercised by M1/M2 tests and lower-level model tests.
The user-facing API page is `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst`.

## Provenance

Original local work under the repository license.

## Evidence and limitations

Software tests support type, unit, positivity, duality, and Hermiticity invariants.
These are synthetic parent definitions and provide no material validation, uncertainty
quantification, or acceptance.
