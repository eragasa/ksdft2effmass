Authenticated visualizations
============================

``ksdft2effmass.visualizations`` owns domain-neutral visualization projection,
Matplotlib composition, PNG admission, authentication, and closed-inventory mechanics.
It does not own scientific projections, family plot inventories, calculation, or
filesystem publication.

``BaseVisualizer`` binds one immutable typed projection, one nominal verification that
authenticates its exact canonical bytes, and one nonempty unique plot inventory.
Authentication completes before figure construction. Its final ``visualize()`` action
requires immutable PNG values whose plot identities exactly equal that constructor-bound
inventory.

``PngFigureRenderer`` binds one plot identity, one figure action, and one positive
built-in integer DPI. It closes the Matplotlib figure after encoding succeeds or fails.
``PngVisualization`` admits only cross-platform-safe ``.png`` basenames and built-in
bytes with a valid PNG signature that decode to a nonempty image. PNG admission validates
the container, not scientific meaning or cross-platform pixel identity.

.. currentmodule:: ksdft2effmass.visualizations

.. autoclass:: BaseVisualizationData
   :members:

.. autoclass:: ksdft2effmass.verification.VisualizationVerification
   :members:

.. autoclass:: BasePlot
   :members:

.. autoclass:: BaseSubplot
   :members:

.. autoclass:: BaseFigure
   :members:

.. autoclass:: BaseFigureRenderer
   :members:

.. autoclass:: PngFigureRenderer
   :members:

.. autoclass:: BaseVisualization
   :members:

.. autoclass:: PngVisualization
   :members:

.. autoclass:: BaseVisualizer
   :members:
