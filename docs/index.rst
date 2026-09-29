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

.. toctree::
   :hidden:

   architecture/v2/index
   architecture/v2/principles
   architecture/v2/repository-layout
   architecture/v2/tutorial-examples
   architecture/v2/identity-version-and-failure-contracts
   architecture/v2/human-decisions
   architecture/v2/ksdft2effmass/index
   architecture/v2/ksdft2effmass/application/index
   architecture/v2/ksdft2effmass/persistence/index
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
   architecture/v2/ksdft2effmass/units
   architecture/v2/ksdft2effmass/plane-wave-parameter-studies
   architecture/v2/ksdft2effmass/calculators/quantum-espresso
   architecture/v2/ksdft2effmass/integration/index
   architecture/v2/ksdft2effmass/integration/quantum_espresso/index
   architecture/v2/ksdft2effmass/periodic/index
   architecture/v2/ksdft2effmass/ksdft/index
   architecture/v2/ksdft2effmass/analysis/index
   architecture/v2/ksdft2effmass/analysis/analysis
   architecture/v2/ksdft2effmass/operators/index
   architecture/v2/issues/index
   user-guide/installation
   user-guide/operator/index
   user-guide/operator/representations
   user-guide/operator/hermiticity
   user-guide/operator/compatibility
   user-guide/operator/differencing
   user-guide/operator/residuals
   user-guide/operator/comparison
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
has an obvious landing page. Detailed computational, research, publication,
proof, and meeting records remain repository-first sources unless deliberately
added to the Sphinx publication set. Architecture remains
version-isolated and begins at :doc:`architecture/index`.
