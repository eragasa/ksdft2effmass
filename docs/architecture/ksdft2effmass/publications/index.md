# `ksdft2effmass.publications`

The package owns immutable records and deterministic composition policy for bounded
publication-authoring proposals. It exposes the [`authoring`](authoring/index.md)
subpackage through an explicit package facade.

The package does not retrieve or rank evidence, call a model by itself, read or write
files, edit a bibliography, publish content, or decide scientific or human acceptance.

## Subpackages

- [`authoring`](authoring/index.md) — target/evidence records, local-inference port,
  deterministic prompt, failed-closed composer, result, and proposal.

## Contents

- [`schematic.md`](schematic.md) — package boundary and external collaborators.
- [`implementation.md`](implementation.md) — exports and dependency restrictions.

```{toctree}
:hidden:

schematic
implementation
authoring/index
```
