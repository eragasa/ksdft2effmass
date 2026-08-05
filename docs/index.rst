ksdft2effmass documentation
===========================

``ksdft2effmass`` is research software for constructing and validating reduced
semiconductor Hamiltonians from first-principles Kohn--Sham calculations.

.. toctree::
   :maxdepth: 2
   :caption: Concepts

   concepts/operator-records
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

   architecture/repository-layout
   development/ai-assisted-development
   development/agent-control-plane
   development/source-documentation
   research/agentic-development-case-study

.. toctree::
   :maxdepth: 2
   :caption: PI harness

   harness/ksdft2effmass.harness.00

.. toctree::
   :hidden:

   harness/ksdft2effmass.harness.01
   harness/ksdft2effmass.harness.02
   harness/ksdft2effmass.harness.03
   harness/ksdft2effmass.harness.04
   harness/ksdft2effmass.harness.05
   harness/ksdft2effmass.harness.06
   harness/ksdft2effmass.harness.07
   harness/ksdft2effmass.harness.08

Markdown-first user guide
-------------------------

The maintained user guide is authored in Markdown for repository and Obsidian
use and rendered directly through MyST. Its explicit toctree plus the bounded
numbered harness pattern are the complete Markdown collection policy; Sphinx
does not broadly collect other Markdown trees.

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

Architecture, computational, research, conference, paper, and meeting Markdown
remain authoritative repository/Obsidian sources, but—apart from the exact
numbered ``docs/harness/ksdft2effmass.harness.*.md`` set—they are intentionally not
Sphinx source documents. Architecture overviews remain available as source
files:

* :download:`Colored Petri Net workflow architecture <architecture/colored-petri-net-workflows.md>`
* :download:`Periodic KS/GKS and QE architecture <architecture/kohn-sham-dft-quantum-espresso.md>`
* :download:`Periodic electronic-structure integration <architecture/periodic-electronic-structure-integration.md>`
* :download:`CPN skill-capability audit <architecture/cpn-skill-capability-audit.md>`
