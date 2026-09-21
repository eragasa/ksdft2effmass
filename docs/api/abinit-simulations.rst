ABINIT Workflow simulations
===========================

``ksdft2effmass.simulations.abinit`` owns ABINIT-specific simulation composition
above the backend-neutral DFT catalog and ABINIT-native integration boundaries.
Its pseudopotential adapter deliberately admits the selected native PSP8
representation and retains the source-entry identity, independent complete
SHA-256, filename, and content-addressed location.

The adapter performs no current-byte verification, parser smoke test, input
rendering, staging, ABINIT invocation, cross-format numerical comparison, or
scientific acceptance.

PSP8 pseudopotential binding
----------------------------

.. automodule:: ksdft2effmass.simulations.abinit
   :members:
   :imported-members:
