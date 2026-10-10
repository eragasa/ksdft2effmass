M1 isolated-band controlled calculation
=======================================

M1 samples a selected scalar band of a finite Fourier parent, performs the complete
discrete reciprocal-to-hopping transform, and compares mediated truncation with direct
finite-range fitting on separate training and staggered-evaluation meshes.

The route name ``isolated-band`` does not independently establish physical isolation.
All energies and tolerances retain explicit units. The evaluation mesh is diagnostic
only and cannot alter the transform, fit, ranges, or controls.

Definition
----------

.. automodule:: ksdft2effmass.periodic1d.isolated_band.definition
   :members:

Calculation
-----------

.. automodule:: ksdft2effmass.periodic1d.isolated_band.calculate
   :members:

Results
-------

.. automodule:: ksdft2effmass.periodic1d.isolated_band.results
   :members:

Serialization
-------------

.. automodule:: ksdft2effmass.periodic1d.isolated_band.serialization
   :members:

Verification
------------

.. automodule:: ksdft2effmass.periodic1d.isolated_band.verify
   :members:
