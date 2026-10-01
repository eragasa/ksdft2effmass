# `citation_snapshot.parsing`

`parsing.py` owns the private closed TeX and BibLaTeX structural grammar. It masks
comments without changing offsets, validates balanced constructs, emits exact
character spans, recognizes only the project-owned citation semantics, and never
executes TeX.

- [Schematic](schematic.md)
- [Implementation](implementation.md)

```{toctree}
:maxdepth: 1
:hidden:

schematic
implementation
```
