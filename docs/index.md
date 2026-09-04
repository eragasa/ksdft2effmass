# Documentation

## Research program

The theoretical and mathematical development of the project is documented in
[[research/ksdft2Effmass.00|Research Program]].

## Computational program

The stateful Colored Petri Net workflow, stage markings, static prerequisite
projection, and executable task hierarchy are documented in
[[computational/ksdft2Effmass.computational.00|Computational Program]].

## Publications

Conference material, publication planning, and manuscript working files are
indexed in
[[publications/ksdft2effmass.publications.00|Publications]].

## Architecture

The version-isolated architecture index is
[`architecture/index.md`](architecture/index.md). It links the single
implemented Architecture v1 snapshot, the normative Architecture v2 target, and
the sole cross-version migration page. Canonical Task status is maintained in
[`harness/tasks/`](../harness/tasks/) with current selection in
[`harness/task-selection.json`](../harness/task-selection.json); generated Task
Markdown has been retired. The maintained Task contract and bounded inspection
boundary are documented in [`api/harness-task.rst`](api/harness-task.rst).

## User guide

Installation, external dependency, CPN operation, periodic backend, QE/ABINIT/Wannier, provenance, and
troubleshooting guidance begins at
[`user-guide/index.md`](user-guide/index.md). New narrative documentation is
Markdown-first. The optional `docs` environment now includes MyST, and Sphinx
collects the explicitly maintained `docs/user-guide/*.md` set, the bounded CPN
Markdown pages, and selected current harness pages alongside all RST sources.
Harness proposals and history remain repository/Obsidian sources until promoted.

## Python API documentation

Finite operator records are exposed through the public `ksdft2effmass.operators`
package. The conceptual documentation is maintained in
[`concepts/operator-records.rst`](concepts/operator-records.rst), and the Sphinx
API reference is maintained in [`api/operators.rst`](api/operators.rst).
