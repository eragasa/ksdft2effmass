# `Periodic1DFourierHamiltonianToyModel`

## Purpose

Immutable scientific definition of the scalar Fourier parent used by M1.

## Contract

The model binds a nonempty stable identity, a real `PeriodicFourierPotential1D`, a
positive reciprocal vector, a positive recoil-energy scale, and a finite nonnegative
duality tolerance. Potential coefficients must have energy dimensions compatible with
`recoil_energy`, and the declared reciprocal period must satisfy

$$
G=\frac{2\pi}{a}
$$

within the declared absolute tolerance after unit conversion.

## State space and units

The represented fibers act on a finite reciprocal basis chosen by the calculator.
`potential.period` carries direct length, `reciprocal_vector` carries inverse length,
and `recoil_energy` plus all Fourier coefficients carry energy. The model itself does
not select a basis cutoff or retained band.

## Invariants and failures

Construction raises `TypeError` for wrong exact public-boundary types and `ValueError`
for empty identity, nonpositive scales, nonfinite/negative tolerance, incompatible
units, or failed direct/reciprocal duality. Boolean and string numeric substitutes are
not accepted for the float tolerance.

## Mapping

- Source: `python/src/ksdft2effmass/periodic1d/model.py`
- Sphinx: `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst`
- Main consumer: `Periodic1DIsolatedBandCalculationDefinition`

## Evidence and limitations

M1 construction and reconstruction tests exercise this contract. The class defines a
toy model and neither runs a calculation nor establishes physical isolation or material
validity.
