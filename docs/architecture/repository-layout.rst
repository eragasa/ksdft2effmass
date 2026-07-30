Repository layout
=================

.. code-block:: text

   ksdft2effmass/
   ├── python/
   │   └── src/ksdft2effmass/operators/   # finite operator-record public API
   ├── rust/
   ├── specification/
   ├── fixtures/
   ├── calculations/
   ├── workflows/
   ├── docs/
   │   ├── concepts/operator-records.rst  # scientific model and serialization format
   │   └── api/operators.rst              # Sphinx API reference
   ├── AGENTS.md
   ├── README.md
   ├── CITATION.cff
   └── LICENSE

The ``ksdft2effmass.operators`` package is the supported public import path for
finite operator records.  Its versioned dictionary serialization format
(``schema_version = 1``) is documented in :doc:`../concepts/operator-records`
and implemented in ``python/src/ksdft2effmass/operators/records.py``.
