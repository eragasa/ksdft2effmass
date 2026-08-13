# Repository Layout

```text
ksdft2effmass/
├── python/
│   └── src/ksdft2effmass/
│       ├── operators/                 # current finite operator-record public API
│       └── provenance/                # public API re-exported only at package level
│           ├── records.py             # artifact, manifest, and lineage records
│           ├── external_tools.py      # tool/capability declarations
│           ├── tool_observations.py   # installation/capability observations
│           ├── external_execution.py  # immutable requests and outcomes
│           ├── actions.py             # pure represented-state operations
│           └── serialization.py       # strict version-1 JSON boundary
├── rust/
├── specification/
│   └── operator-record/v1/            # public schema and validation fixtures
├── fixtures/
├── formal/                              # theorem contracts and isolated multi-prover proof sources
│   ├── theorem-catalog/                 # active cross-backend theorem identities and assumption contracts
│   ├── lean/                            # active bounded Lean 4/mathlib backend for PRF-05.01
│   ├── isabelle/                        # prospective Isabelle/HOL backend
│   └── rocq/                            # prospective Rocq backend
├── calculations/
├── workflows/                        # future executable/reproduction workflows
├── .agents/skills/                  # shared repository-local agent skills
│   ├── graphify/                       # shared project Graphify skill
│   └── resolve-human-checkpoint/       # shared checkpoint-resolution skill
├── .pi/                               # pi-specific skills, agents, chains, checkpoints, and task records
├── docs/
│   ├── concepts/operator-records.rst  # scientific model and serialization format
│   ├── architecture/                  # architectural decisions and static import direction
│   ├── user-guide/                    # Markdown-first operation/dependency guidance
│   ├── computational/                 # stages, protocols, and accepted marking evidence
│   ├── research/                      # scientific questions, claims, and limitations
│   ├── development/                   # developer and control-plane documentation
│   └── api/operators.rst              # Sphinx API reference
├── AGENTS.md
├── README.md
├── CITATION.cff
└── LICENSE
```

The `formal/` surface is governed by `docs/architecture/mechanized-proof-system.md`. Its maintained Markdown theorem catalog is active. The bounded Lean 4/mathlib `v4.33.0` backend checks `PRF-05.01`; every other Lean target and the approved prospective Isabelle and Rocq source trees remain inactive. Formal backends must not become Python runtime dependencies or silently mutate proof status, specifications, research assumptions, manuscript claims, or scientific acceptance records.

The `ksdft2effmass.operators` package is the supported public import path for finite operator records. The supported public import path for provenance objects is exactly `ksdft2effmass.provenance`; internal provenance filenames are ownership boundaries, not supported direct-import paths. In particular, no supported `ksdft2effmass.provenance.tools` contract existed before `tools.py` was removed.

The provenance decomposition preserves an acyclic dependency direction. `external_tools.py`, `tool_observations.py`, and `external_execution.py` own declaration, observation, and request/outcome records respectively, validate their intrinsic invariants directly in each class's `__post_init__`, and do not depend on `actions.py` or `serialization.py`. They use no shared or private validator helpers. `actions.py` imports the exact record types consumed by pure represented-state operations. `serialization.py` imports the exact record/result types mapped by the version-1 wire boundary. Package-level re-exports preserve the accepted API; the decomposition does not change schema or fixture meaning. Stored lifecycle fields remain distinct from derived, non-wire verification and correlation statuses.

The approved prospective periodic KS/GKS/QE package ownership and static acyclic import direction are recorded in `docs/architecture/kohn-sham-dft-quantum-espresso.md`, with the corrected scientific domain and backend extension seams in `docs/architecture/periodic-electronic-structure-integration.md`. Portable references to non-repository scientific artifacts and the canonical containment rules for the `user_opt` store are recorded in `docs/architecture/external-system-integration.md`; run-local copies remain derived execution inputs rather than authority. The scientific/computational workflow is instead the stateful Colored Petri Net in `docs/architecture/colored-petri-net-workflows.md`. Prospective `workflows/cpn/` ownership is project-owned and isolates SNAKES in `workflows/cpn/engines/snakes.py`; those packages do not yet exist and are not authorized as a monolithic implementation. Operator-record modules are arranged as `records.py -> compatibility.py -> difference.py -> residuals.py -> comparison.py` for acyclic comparison decomposition, with `comparison.py` limited to the concrete Workflow composition. Its versioned JSON text serialization format (`schema_version = 1`) is documented in `docs/concepts/operator-records.rst`, specified by `specification/operator-record/v1/operator-record.schema.json`, validated with fixtures under `specification/operator-record/v1/`, and implemented in `python/src/ksdft2effmass/operators/serialization.py`. Runtime serializer evidence uses five object facets under `python/tests/software_verification/ksdft2effmass/operators/`; public-schema and golden-fixture interoperability use the two narrow owners under the neighboring `integration/` subtree.

In the validated project environment, both Codex and pi discover repository-local skills under `.agents/skills/`. pi additionally discovers pi-specific skills under `.pi/skills/`. A project skill may shadow a same-named global pi skill. The shared project Graphify skill lives under `.agents/skills/graphify/`; the shared checkpoint-resolution skill lives under `.agents/skills/resolve-human-checkpoint/`. Durable human checkpoint records and their JSON Schema live under `.pi/checkpoints/`. Generated Graphify outputs live under ignored `graphify-out/` and are derived navigation artifacts, not authoritative repository state.
