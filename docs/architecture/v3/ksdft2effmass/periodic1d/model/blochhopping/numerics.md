# Periodic-1D Bloch-hopping scale numerics

The periodic-1D owner composes a physical PhysKit `UnitSystem` with the lattice period
to define

\[
E_a=\frac{\hbar^2}{m_ea^2},
\]

without the kinetic-operator factor `1/2`. The period is explicitly converted to the
unit system's length unit. The reduced Planck constant, Pint-supported electron mass,
and output energy unit remain coherent within that same unit system.

## Numerical validation behavior

Numerical tests verify three consequences of the declared convention:

1. one bohr in `UnitSystem.ATOMIC` gives one Hartree;
2. doubling the lattice period divides the scale by four; and
3. one bohr in `UnitSystem.METAL` gives approximately `27.21138625 eV`.

Specific pytest evidence:

- `tests/ksdft2effmass/periodic1d/model/blochhopping/test__Periodic1DLatticeKineticEnergyScale__convention.py::TestPeriodic1DLatticeKineticEnergyScale::test__Periodic1DLatticeKineticEnergyScale__one_bohr_matches_hartree`
- `tests/ksdft2effmass/periodic1d/model/blochhopping/test__Periodic1DLatticeKineticEnergyScale__convention.py::TestPeriodic1DLatticeKineticEnergyScale::test__Periodic1DLatticeKineticEnergyScale__follows_inverse_square_period`
- `tests/ksdft2effmass/periodic1d/model/blochhopping/test__Periodic1DLatticeKineticEnergyScale__convention.py::TestPeriodic1DLatticeKineticEnergyScale::test__Periodic1DLatticeKineticEnergyScale__converts_to_electron_volt`

These checks establish finite scale arithmetic and coherent unit conversion behavior;
they do not validate any material model.

- [Owner contract](index.md)
