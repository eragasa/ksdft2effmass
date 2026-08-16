ksdft2effmass documentation
===========================

``ksdft2effmass`` is research software for constructing and validating reduced
semiconductor Hamiltonians from first-principles Kohn--Sham calculations.

.. toctree::
   :maxdepth: 2
   :caption: Concepts

   concepts/operator-records
   concepts/periodic-calculation-records
   concepts/cpn-contract

The Markdown-first provenance concept page is available as a
:download:`maintained source page <concepts/provenance-and-artifacts.md>`.

.. toctree::
   :maxdepth: 2
   :caption: API reference

   api/index

.. toctree::
   :maxdepth: 1
   :caption: Verification

   verification/testing-and-evidence
   verification/operator-record-geometry
   verification/operator-record-energy-reference
   verification/operator-record-data-object
   verification/operator-record-json-serialization
   verification/operator-record-hermiticity
   verification/operator-record-compatibility-analysis
   verification/operator-record-difference
   verification/operator-record-residual-analyzer
   verification/cpn-contract
   verification/provenance-contract

.. toctree::
   :maxdepth: 1
   :caption: Project documentation

   architecture/index
   development/ai-assisted-development
   development/agent-control-plane
   development/source-documentation
   research/agentic-development-case-study

.. toctree::
   :maxdepth: 2
   :caption: PI harness

   harness/ksdft2effmass.harness.001.000.000

.. toctree::
   :hidden:

   architecture/v1/index
   architecture/v1/principles
   architecture/v1/repository-layout
   architecture/v1/separation-of-harness-and-workflow
   architecture/v1/ksdft2effmass/index
   architecture/v1/ksdft2effmass/harness/index
   architecture/v1/ksdft2effmass/harness/pi/index
   architecture/v1/ksdft2effmass/harness/pi/development-harness
   architecture/v1/ksdft2effmass/harness/pi/control-plane
   architecture/v1/ksdft2effmass/harness/pi/local/control/index
   architecture/v1/ksdft2effmass/harness/pi/local/dbcontrol/index
   architecture/v1/ksdft2effmass/harness/pi/local/dbcontrol/projections
   architecture/v1/ksdft2effmass/harness/pi/subagents/index
   architecture/v1/ksdft2effmass/harness/pi/subagents/agent-descriptors
   architecture/v1/ksdft2effmass/harness/pi/subagents/parent-orchestration
   architecture/v1/ksdft2effmass/harness/pi/subagents/delegation-and-ownership
   architecture/v1/ksdft2effmass/harness/pi/subagents/execution-and-isolation
   architecture/v1/ksdft2effmass/harness/pi/subagents/handoffs-and-review
   architecture/v1/ksdft2effmass/harness/pi/subagents/runtime-state-and-artifacts
   architecture/v1/ksdft2effmass/workflows/index
   architecture/v1/ksdft2effmass/workflows/cpn/index
   architecture/v1/ksdft2effmass/workflows/cpn/model
   architecture/v1/ksdft2effmass/io/index
   architecture/v1/ksdft2effmass/io/quantum_espresso/index
   architecture/v1/ksdft2effmass/io/quantum_espresso/qexsd/index
   architecture/v1/ksdft2effmass/periodic/index
   architecture/v1/ksdft2effmass/ksdft/index
   architecture/v1/ksdft2effmass/ksdft/pw/index
   architecture/v1/ksdft2effmass/provenance/index
   architecture/v1/ksdft2effmass/operators/index
   architecture/v1/calculations/index
   architecture/v1/calculations/simulation-model
   architecture/v2/index
   architecture/v2/principles
   architecture/v2/repository-layout
   architecture/v2/separation-of-harness-and-workflow
   architecture/v2/identity-version-and-failure-contracts
   architecture/v2/human-decisions
   architecture/v2/ksdft2effmass/index
   architecture/v2/ksdft2effmass/application/index
   architecture/v2/ksdft2effmass/persistence/index
   architecture/v2/ksdft2effmass/harness/index
   architecture/v2/ksdft2effmass/harness/object-model
   architecture/v2/ksdft2effmass/harness/development-harness
   architecture/v2/ksdft2effmass/harness/compiler-architecture
   architecture/v2/ksdft2effmass/harness/validation
   architecture/v2/ksdft2effmass/harness/conformance
   architecture/v2/ksdft2effmass/harness/control-plane
   architecture/v2/ksdft2effmass/harness/persistence
   architecture/v2/ksdft2effmass/harness/projections
   architecture/v2/ksdft2effmass/harness/subagents
   architecture/v2/ksdft2effmass/workflows/index
   architecture/v2/ksdft2effmass/workflows/task-and-colored-petri-net-adapter
   architecture/v2/ksdft2effmass/workflows/workflow-run
   architecture/v2/ksdft2effmass/workflows/simulation-task-model
   architecture/v2/ksdft2effmass/workflows/service-model
   architecture/v2/ksdft2effmass/workflows/control-plane
   architecture/v2/ksdft2effmass/workflows/persistence
   architecture/v2/ksdft2effmass/workflows/artifact-and-provenance-model
   architecture/v2/ksdft2effmass/workflows/read-models
   architecture/v2/ksdft2effmass/petrinet/index
   architecture/v2/ksdft2effmass/petrinet/colored/index
   architecture/v2/ksdft2effmass/campaigns/index
   architecture/v2/ksdft2effmass/calculators/index
   architecture/v2/ksdft2effmass/calculators/quantum-espresso
   architecture/v2/ksdft2effmass/integration/index
   architecture/v2/ksdft2effmass/integration/quantumespresso/index
   architecture/v2/ksdft2effmass/periodic/index
   architecture/v2/ksdft2effmass/ksdft/index
   architecture/v2/ksdft2effmass/analysis/index
   architecture/v2/ksdft2effmass/analysis/analysis
   architecture/v2/issues/index
   architecture/migration/v1-to-v2/index
   architecture/migration/v1-to-v2/pi-harness-subagents
   harness/ksdft2effmass.harness.001.001.000
   harness/ksdft2effmass.harness.001.002.000
   harness/ksdft2effmass.harness.001.003.000
   harness/ksdft2effmass.harness.001.004.000
   harness/ksdft2effmass.harness.001.006.000

Markdown-first user guide
-------------------------

The maintained user guide is authored in Markdown for repository and Obsidian
use and rendered directly through MyST. Its explicit toctree plus the selected
current harness pages in ``docs/conf.py`` are the complete Markdown collection
policy; Sphinx does not broadly collect other Markdown trees.

.. toctree::
   :maxdepth: 2
   :caption: User guide

   user-guide/index
   user-guide/installation
   user-guide/external-dependencies
   user-guide/dft-backends
   user-guide/paw-and-pseudopotential-backends
   user-guide/workflow-model
   user-guide/colored-petri-nets
   user-guide/quantum-espresso
   user-guide/abinit
   user-guide/cross-backend-verification
   user-guide/wannier90
   user-guide/provenance-and-artifacts
   user-guide/external-tool-lifecycle
   user-guide/troubleshooting

Uncollected Markdown records
----------------------------

Computational, research, conference, paper, and meeting Markdown remain
repository/Obsidian sources unless explicitly collected. Architecture is
version-isolated and begins at :doc:`architecture/index`. Its primary maintained
sources are:

* :download:`Architecture v1 <architecture/v1/index.md>`
* :download:`Architecture v2 <architecture/v2/index.md>`
* :download:`Migration from v1 to v2 <architecture/migration/v1-to-v2/index.md>`
