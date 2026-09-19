Plane-wave DFT calculator contracts
===================================

The ``pw`` package segment denotes the backend-neutral plane-wave numerical method;
it does not denote Quantum ESPRESSO's ``pw.x`` executable.  The package defines a
small portable specification, a positive canonical electron-volt cutoff, an exact
dimensionless three-axis reciprocal mesh, exact backend-binding references, closed
compilation results, and a structural calculator port.  Native Hartree or Rydberg
values require the explicit provenance-retaining conversion documented by
:doc:`units`; they are not accepted as portable cutoff values.  Mesh counts and
half-step shifts do not define reciprocal bases,
symmetry reduction, weights, native syntax, or backend equivalence.  A compilation
failure has one exact
outcome/code association: unsupported requirement, incompatible model/supplement,
invalid specification, or internal error.  Contradictory pairs are rejected.

Concrete native inputs, outputs, diagnostics, executable configuration, staging, and
process effects remain owned by packages such as
:mod:`ksdft2effmass.integration.quantum_espresso`.  Protocol conformance neither
grants execution authority nor establishes scientific or numerical equivalence
between backends.  The ``ksdft2effmass.calculators`` and
``ksdft2effmass.calculators.dft`` package roots intentionally provide no compatibility
aliases; consumers import the supported contracts from
``ksdft2effmass.calculators.dft.pw``.  In particular, the prior public
``PlaneWaveEnergyUnit`` enum and two-argument ``PlaneWaveEnergyCutoff(value, unit)``
constructor are replaced by ``PlaneWaveEnergyCutoff(UnitScalar(...))`` with the
scalar unit fixed to electron volts; no compatibility alias is supplied.

.. automodule:: ksdft2effmass.calculators.dft.pw
   :members:
   :imported-members:
