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
   architecture/v2/index
   architecture/v2/principles
   architecture/v2/separation-of-harnesses
   architecture/v2/development-harness
   architecture/v2/scientific-execution-harness
   architecture/v2/simulation-model
   architecture/v2/campaign-and-cpn-model
   architecture/v2/artifact-and-provenance-model
   architecture/v2/control-plane
   architecture/v2/persistence-and-projections
   architecture/v2/repository-layout
   architecture/migration-v1-to-v2
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
* :download:`Migration from v1 to v2 <architecture/migration-v1-to-v2.md>`
