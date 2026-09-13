Plane-wave DFT calculator contracts
===================================

The ``pw`` package segment denotes the backend-neutral plane-wave numerical method;
it does not denote Quantum ESPRESSO's ``pw.x`` executable.  The package defines a
small portable specification, exact backend-binding references, closed compilation
results, and a structural calculator port.

Concrete native inputs, outputs, diagnostics, executable configuration, staging, and
process effects remain owned by packages such as
:mod:`ksdft2effmass.integration.quantum_espresso`.  Protocol conformance neither
grants execution authority nor establishes scientific or numerical equivalence
between backends.

.. automodule:: ksdft2effmass.calculators.dft.pw
   :members:
   :imported-members:
