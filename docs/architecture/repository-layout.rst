Repository layout
=================

.. code-block:: text

   ksdft2effmass/
   ├── .agents/skills/                  # shared repository-local agent skills
   │   ├── graphify/                       # shared project Graphify skill
   │   └── resolve-human-checkpoint/       # shared checkpoint-resolution skill
   ├── .pi/                               # pi-specific skills, agents, chains, checkpoints, and task records
   ├── python/
   │   └── src/ksdft2effmass/operators/   # finite operator-record public API
   ├── rust/
   ├── specification/
   ├── fixtures/
   ├── formal/                            # theorem contracts and approved prospective multi-prover proof sources
   │   ├── theorem-catalog/               # active cross-backend theorem identities and assumption contracts
   │   ├── lean/                          # prospective Lean 4/mathlib backend
   │   ├── isabelle/                      # prospective Isabelle/HOL backend
   │   └── rocq/                          # prospective Rocq backend
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

The ``formal/`` surface is governed by
``docs/architecture/mechanized-proof-system.md``. Its maintained Markdown theorem
catalog is active. Independent Lean, Isabelle, and Rocq source trees are approved
prospective ownership surfaces, but no prover source, toolchain, dependency,
build, or execution is active. Formal backends must not become Python runtime dependencies
or silently mutate proof status, specifications, research assumptions,
manuscript claims, or scientific acceptance records.

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
``.agents/skills/graphify/``; the shared checkpoint-resolution skill lives under
``.agents/skills/resolve-human-checkpoint/``. Durable human checkpoint records
and their JSON Schema live under ``.pi/checkpoints/``. Generated Graphify outputs
live under ignored ``graphify-out/`` and are derived navigation artifacts, not
authoritative repository state.
