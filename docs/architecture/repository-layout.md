# Repository Layout

```text
ksdft2effmass/
├── python/
│   └── src/ksdft2effmass/operators/   # finite operator-record public API
├── rust/
├── specification/
│   └── operator-record/v1/            # public schema and validation fixtures
├── fixtures/
├── calculations/
├── workflows/
├── .agents/skills/                  # shared repository-local agent skills
│   ├── graphify/                       # shared project Graphify skill
│   └── resolve-human-checkpoint/       # shared checkpoint-resolution skill
├── .pi/                               # pi-specific skills, agents, chains, checkpoints, and task records
├── docs/
│   ├── concepts/operator-records.rst  # scientific model and serialization format
│   ├── development/                   # developer and control-plane documentation
│   └── api/operators.rst              # Sphinx API reference
├── AGENTS.md
├── README.md
├── CITATION.cff
└── LICENSE
```

The `ksdft2effmass.operators` package is the supported public import path for finite operator records. Operator-record modules are arranged as `records.py -> compatibility.py -> difference.py -> residuals.py -> comparison.py` for acyclic comparison decomposition, with `comparison.py` limited to the concrete Workflow composition. Its versioned JSON text serialization format (`schema_version = 1`) is documented in `docs/concepts/operator-records.rst`, specified by `specification/operator-record/v1/operator-record.schema.json`, validated with fixtures under `specification/operator-record/v1/`, and implemented in `python/src/ksdft2effmass/operators/serialization.py`. Runtime serializer evidence uses five object facets under `python/tests/software_verification/ksdft2effmass/operators/`; public-schema and golden-fixture interoperability use the two narrow owners under the neighboring `integration/` subtree.

In the validated project environment, both Codex and pi discover repository-local skills under `.agents/skills/`. pi additionally discovers pi-specific skills under `.pi/skills/`. A project skill may shadow a same-named global pi skill. The shared project Graphify skill lives under `.agents/skills/graphify/`; the shared checkpoint-resolution skill lives under `.agents/skills/resolve-human-checkpoint/`. Durable human checkpoint records and their JSON Schema live under `.pi/checkpoints/`. Generated Graphify outputs live under ignored `graphify-out/` and are derived navigation artifacts, not authoritative repository state.
