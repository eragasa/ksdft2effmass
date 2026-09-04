ksdft2effmass documentation
===========================

``ksdft2effmass`` is research software for constructing and evaluating reduced
semiconductor Hamiltonians from first-principles Kohn--Sham calculations.

Start with the user guide for software use, the concepts pages for represented
objects and workflows, or the research and computational indexes for the project
program.  Scientific specifications and retained calculation provenance remain
in their owning repository locations.

.. toctree::
   :maxdepth: 2
   :caption: Learn and research

   user-guide/index
   concepts/index
   computational/index
   research/index

.. toctree::
   :maxdepth: 2
   :caption: Software and verification

   architecture/index
   api/index
   verification/index
   development/index

.. toctree::
   :maxdepth: 1
   :caption: Project records

   publications/index
   proofs/index
   meetings/index

History is preserved separately from current guidance.  Start with the
:doc:`implemented Harness history <architecture/v1/ksdft2effmass/harness/history>`;
non-operational development-control history remains under ``harness/archive/``.

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
   architecture/v1/ksdft2effmass/harness/pi/resources-and-validation
   architecture/v1/ksdft2effmass/harness/pi/human-review
   architecture/v1/ksdft2effmass/harness/history
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
   architecture/v2/tutorial-examples
   architecture/v2/agents/index
   architecture/v2/agents/deterministic-actions
   architecture/v2/agents/capability-and-isolation
   architecture/v2/agents/self-improvement
   architecture/v2/separation-of-harness-and-workflow
   architecture/v2/identity-version-and-failure-contracts
   architecture/v2/human-decisions
   architecture/v2/ksdft2effmass/index
   architecture/v2/ksdft2effmass/pi/index
   architecture/v2/ksdft2effmass/pi/agents/index
   architecture/v2/ksdft2effmass/application/index
   architecture/v2/ksdft2effmass/persistence/index
   architecture/v2/ksdft2effmass/harness/index
   architecture/v2/ksdft2effmass/harness/object-model
   architecture/v2/ksdft2effmass/harness/configuration
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
   architecture/v2/ksdft2effmass/workflows/dft-simulation-cpn-service-decision
   architecture/v2/ksdft2effmass/workflows/qe-wannier90-cpn-workflow
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
   architecture/v2/ksdft2effmass/operators/index
   architecture/v2/issues/index
   architecture/migration/v1-to-v2/index
   architecture/migration/v1-to-v2/package-module-crosswalk
   architecture/migration/v1-to-v2/implementation/index
   architecture/migration/v1-to-v2/implementation/strict-python-conformance-migration
   architecture/migration/v1-to-v2/implementation/identity-contracts
   architecture/migration/v1-to-v2/implementation/periodic-contract-verification
   architecture/migration/v1-to-v2/implementation/ksdft-contract-verification
   architecture/migration/v1-to-v2/implementation/ksdft-plane-wave-disposition
   architecture/migration/v1-to-v2/implementation/operator-ownership
   architecture/migration/v1-to-v2/implementation/operator-records-disposition
   architecture/migration/v1-to-v2/implementation/qexsd-parsing-migration
   architecture/migration/v1-to-v2/implementation/harness/task-model
   architecture/migration/v1-to-v2/implementation/harness/decisions-authority
   architecture/migration/v1-to-v2/implementation/harness/prerequisite-resolution
   architecture/migration/v1-to-v2/implementation/harness/compiler
   architecture/migration/v1-to-v2/implementation/petrinet/colored
   architecture/migration/v1-to-v2/coding-standards-conformance
   architecture/migration/v1-to-v2/development-harness-projections
   architecture/migration/v1-to-v2/pi-harness-subagents
   architecture/migration/v1-to-v2/agents
   research/agentic-development-case-study
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

Collection boundary
-------------------

The section indexes above are collected so every first-level documentation area
has an obvious landing page.  Detailed computational, research, publication,
proof, and meeting records remain repository-first sources unless an owning task
explicitly adds them to the Sphinx publication set.  Architecture remains
version-isolated and begins at :doc:`architecture/index`.
