# `ksdft2effmass.periodic2d.run`

## Purpose and status

This namespace owns preserved periodic-2D campaign-run families and exact encoded
documents pending phase-7 decomposition. A run-family container is not itself a
scientific model, represented operator, retained space, verification result, or
acceptance record.

## Child map

- [Composite campaign](composite/index.md)
  - [Encoded documents](composite/encoded_documents/index.md)
- [Topological campaign](topological/index.md)
  - [Encoded documents](topological/encoded_documents/index.md)
- [Wannier90 campaign families](wannier90/index.md)
  - [Balanced campaign](wannier90/balanced/index.md)
  - [Encoded documents](wannier90/balanced/encoded_documents/index.md)

## Ownership boundary

Run families may own project-specific campaign records, operations, and retained wires.
Reusable scientific primitives and general represented operators remain outside this
namespace. Encoded bytes acquire scientific meaning only through explicit authenticated
serialization, correlation, and scientific owners.
