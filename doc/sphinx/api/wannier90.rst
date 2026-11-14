Wannier90 artifact boundary
===========================

Reusable native Wannier90 records, parsers, artifact authentication, and bounded
parser controls are owned by the ``projectkoios-simulations`` distribution under
:mod:`projectkoios.integrations.wannier90`.  KSD does not duplicate or re-export that
provider-facing API.

KSD consumes those integration-owned values only in campaign-specific composition.
The maintained periodic-1D native-artifact Workflow authenticates caller-supplied
bytes, delegates native parsing to Project Koios Simulations, and applies KSD-owned
correlation and Wilson-loop verification policy.  Neither dependency executes
Wannier90 through this path.

Ownership boundary
------------------

Project Koios Simulations owns:

* native ``.nnkp``, ``.eig``, ``.amn``, ``.mmn``, ``.wout``, ``_u.mat``, and
  ``_hr.dat`` records and parsers;
* caller-supplied native artifact identities, authentication, and parsed artifact
  aggregation; and
* calculator-facing Wannier90 preprocessing and execution contracts when present in
  the selected dependency revision.

KSD owns:

* retained campaign documents and exact expected artifact inventories;
* campaign-specific correlation between parsed artifacts and retained results;
* independent Wilson-loop reconstruction and diagnostics; and
* scientific interpretation and claim boundaries.

See :doc:`../user-guide/wannier90` for the execution and scientific boundaries.
