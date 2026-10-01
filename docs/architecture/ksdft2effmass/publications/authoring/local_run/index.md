# `ksdft2effmass.publications.authoring.local_run`

This module owns the retained local authoring Workflow. It delegates semantic
composition to `EvidenceGroundedManuscriptAuthor` and local inference/response
retention to the fixed Ollama adapter, then retains either an ordinary result terminal
or a separate exceptional terminal before re-raising an inference exception.

## Public class

- [`RetainedLocalManuscriptAuthoringRun`](RetainedLocalManuscriptAuthoringRun/index.md)

## Contents

- [`schematic.md`](schematic.md) — retained local composition sequence.
- [`implementation.md`](implementation.md) — delegation and terminal guarantees.

```{toctree}
:hidden:

schematic
implementation
RetainedLocalManuscriptAuthoringRun/index
```
