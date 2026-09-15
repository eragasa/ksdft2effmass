Plane-wave DFT calculator contracts
===================================

The ``pw`` package segment denotes the backend-neutral plane-wave numerical method;
it does not denote Quantum ESPRESSO's ``pw.x`` executable.  The package defines a
small portable specification, exact backend-binding references, closed compilation
results, and a structural calculator port.  A compilation failure has one exact
outcome/code association: unsupported requirement, incompatible model/supplement,
invalid specification, or internal error.  Contradictory pairs are rejected.

Concrete native inputs, outputs, diagnostics, executable configuration, staging, and
process effects remain owned by packages such as
:mod:`ksdft2effmass.integration.quantum_espresso`.  Protocol conformance neither
grants execution authority nor establishes scientific or numerical equivalence
between backends.  The ``ksdft2effmass.calculators`` and
``ksdft2effmass.calculators.dft`` package roots intentionally provide no compatibility
aliases; consumers import the supported contracts from
``ksdft2effmass.calculators.dft.pw``.

.. automodule:: ksdft2effmass.calculators.dft.pw
   :members:
   :imported-members:
