# Documentation

## Research program

The theoretical and mathematical development of the project is documented in
[[research/ksdft2Effmass.00|Research Program]].

## Computational program

The stateful Colored Petri Net workflow, stage markings, static prerequisite
projection, and executable task hierarchy are documented in
[[computational/ksdft2Effmass.computational.00|Computational Program]].

## Papers

The publication dependency structure is documented in
[[papers/ksdft2effmass.papers.00|Papers Pipeline]].

## Architecture

Software, repository, data, and provenance decisions are documented in
[`architecture/repository-layout.md`](architecture/repository-layout.md). The approved prospective periodic KS/GKS electronic-structure and Quantum ESPRESSO
architecture is recorded in
[`architecture/kohn-sham-dft-quantum-espresso.md`](architecture/kohn-sham-dft-quantum-espresso.md). The periodic KS/GKS domain and backend-extension seams are recorded in [`architecture/periodic-electronic-structure-integration.md`](architecture/periodic-electronic-structure-integration.md). The project-owned workflow semantics are recorded in
[`architecture/colored-petri-net-workflows.md`](architecture/colored-petri-net-workflows.md). The bounded skill-capability and prospective CPN testing-block audit is recorded in [`architecture/cpn-skill-capability-audit.md`](architecture/cpn-skill-capability-audit.md). The maintained PI harness incubation architecture begins at [`harness/ksdft2effmass.harness.00.md`](harness/ksdft2effmass.harness.00.md); live harness task state remains under `.pi/`.

## User guide

Installation, external dependency, CPN operation, periodic backend, QE/ABINIT/Wannier, provenance, and
troubleshooting guidance begins at
[`user-guide/index.md`](user-guide/index.md). New narrative documentation is
Markdown-first. The optional `docs` environment now includes MyST, and Sphinx
collects the explicitly maintained `docs/user-guide/*.md` set, the bounded CPN
Markdown pages, and exactly `docs/harness/ksdft2effmass.harness.*.md` alongside
all RST sources. Other Markdown trees remain repository/Obsidian sources.

## Python API documentation

Finite operator records are exposed through the public `ksdft2effmass.operators`
package. The conceptual documentation is maintained in
[`concepts/operator-records.rst`](concepts/operator-records.rst), and the Sphinx
API reference is maintained in [`api/operators.rst`](api/operators.rst).
