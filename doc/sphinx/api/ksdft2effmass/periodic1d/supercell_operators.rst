Explicit periodic-1D supercell operators
=========================================

.. module:: ksdft2effmass.periodic1d.supercell_operators

This API is the lossless row-030 route to the general
:class:`ksdft2effmass.operators.OperatorRecord`.  Callers must supply explicit
three-dimensional cell vectors, one exact ordered label per represented state,
energy and coordinate conventions, stable identities, and structured provenance.
Historical artifacts lacking those values remain unmigrated; the API never
reconstructs them from dimensions, ordering descriptions, paths, hashes, or spectra.

.. autoclass:: Periodic1DSupercellOperatorProvenance
   :members:

.. autoclass:: Periodic1DSupercellOperatorMetadata
   :members:

.. autoclass:: Periodic1DSupercellOperatorConstructor
   :members:
