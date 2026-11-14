Periodic control-model catalog
==============================

.. currentmodule:: ksdft2effmass.periodic.catalog

The control-model catalog is an immutable explicit inventory. It accepts a nonempty exact
``tuple`` and preserves caller-owned registration order. Each member must:

* inherit :class:`~ksdft2effmass.periodic.models.PeriodicModel` and the matching
  nominal dimension branch;
* declare the exact
  :attr:`~ksdft2effmass.periodic.models.PeriodicModelRole.CONTROL_MODEL` role;
* expose an exact nonempty ``str`` identity; and
* have an identity unique within the catalog.

The catalog does not scan modules, enumerate subclasses, execute models, compare
observations, apply thresholds, or establish scientific acceptance. Campaigns may
consume a selected immutable catalog snapshot after concrete model migration supplies
registered entries.

.. autoclass:: PeriodicControlModelCatalog
   :members:
