Repository layout
=================

.. code-block:: text

   ksdft2effmass/
   ├── .agents/skills/                  # shared repository-local agent skills
   │   └── graphify/                       # shared project Graphify skill
   ├── .pi/                               # pi-specific skills, agents, chains, and task records
   ├── python/
   │   └── src/ksdft2effmass/operators/   # finite operator-record public API
   ├── rust/
   ├── specification/
   ├── fixtures/
   ├── calculations/
   ├── workflows/
   ├── docs/
   │   ├── concepts/operator-records.rst  # scientific model and serialization format
   │   ├── development/                   # developer and control-plane documentation
   │   └── api/operators.rst              # Sphinx API reference
   ├── AGENTS.md
   ├── README.md
   ├── CITATION.cff
   └── LICENSE

The ``ksdft2effmass.operators`` package is the supported public import path for
finite operator records.  Its versioned JSON text serialization format
(``schema_version = 1``) is documented in :doc:`../concepts/operator-records`,
specified by ``specification/operator-record/v1/operator-record.schema.json``,
validated with fixtures under ``specification/operator-record/v1/``, and
implemented in ``python/src/ksdft2effmass/operators/serialization.py``.

In the validated project environment, both Codex and pi discover
repository-local skills under ``.agents/skills/``. pi additionally discovers
pi-specific skills under ``.pi/skills/``. A project skill may shadow a same-named
global pi skill. The shared project Graphify skill lives under
``.agents/skills/graphify/``; generated Graphify outputs live under ignored
``graphify-out/`` and are derived navigation artifacts, not authoritative
repository state.
