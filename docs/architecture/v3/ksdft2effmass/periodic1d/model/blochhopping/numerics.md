# Periodic-1D Bloch-hopping scale numerics

The periodic-1D owner defines the lattice kinetic-energy scale

\[
E_a=\frac{\hbar^2}{m_ea^2},
\]

without the kinetic-operator factor `1/2`. Unit conversion is explicit and occurs
before coefficient construction.

## Numerical validation behavior

Numerical tests verify three consequences of the declared convention:

1. one bohr gives one Hartree within the physical-constant precision;
2. doubling the lattice period divides the scale by four; and
3. the one-bohr value converts to approximately `27.21138625 eV`.

Specific pytest evidence:

- `tests/ksdft2effmass/periodic1d/model/blochhopping/test__Periodic1DLatticeKineticEnergyScale__convention.py::TestPeriodic1DLatticeKineticEnergyScale::test__Periodic1DLatticeKineticEnergyScale__one_bohr_matches_hartree`
- `tests/ksdft2effmass/periodic1d/model/blochhopping/test__Periodic1DLatticeKineticEnergyScale__convention.py::TestPeriodic1DLatticeKineticEnergyScale::test__Periodic1DLatticeKineticEnergyScale__follows_inverse_square_period`
- `tests/ksdft2effmass/periodic1d/model/blochhopping/test__Periodic1DLatticeKineticEnergyScale__convention.py::TestPeriodic1DLatticeKineticEnergyScale::test__Periodic1DLatticeKineticEnergyScale__converts_to_electron_volt`

These checks establish the finite scale arithmetic and explicit conversion behavior;
they do not validate any material model.

- [Owner contract](index.md)
