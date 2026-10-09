# `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis`

## Package responsibility

This package owns the retained, campaign-specific offline reanalysis of the periodic-2D
Wannier90 optimizer-basin study. It is subordinate to `optimizer_basin`; it is not a
generic reanalysis framework and supplies no registry, plugin, strategy, discovery, or
compatibility layer.

The package keeps the original optimizer-basin observations distinct from later derived
diagnostics. It owns:

- exact source-result and reanalysis-result wires;
- strict adaptation to immutable verifier records;
- authentication of directly declared compact repository sources;
- reconstruction of retained spread, terminal-trace, bounded basin, and
  common-estimator-refinement diagnostics; and
- an immutable bounded verification Result.

It does not access the unavailable external native tree, rerun Wannier90, alter the
row-052 negative convergence disposition, prove optimizer completeness or global
optimality, establish scientific validation, quantify uncertainty, or record acceptance.

## Modules

| Module | Responsibility |
|---|---|
| [`encoded_documents`](encoded_documents/index.md) | Exact immutable source/result byte ownership |
| `decode` | Strict schema-specific adaptation to closed immutable records |
| `records` | Decoder-owned immutable verifier records |
| `authentication` | Encapsulated-byte and confined repository-source authentication |
| `numerics` | Descriptive trace classification, spread algebra, periodic center comparison, and bounded basin partitioning |
| `correlation` | Source/configuration/endpoint/basin correlation |
| `refinement` | Maintained estimator-fixture authentication and refinement reconstruction |
| `verify` | Public verification request, orchestration Action, and immutable Result |
| `data` | Immutable campaign composition and request-scoped verifier creation |

## Supported facade

The reviewed local facade exposes only:

- `Periodic2DOptimizerReanalysisEncodedDocuments`; and
- `Periodic2DOptimizerReanalysisCampaign`.

The verification request and Result remain explicit owners in the defining `verify`
module and are documented there without being flattened into a package facade.
Implementation collaborators are concrete class owners but are likewise not flattened
into the supported facade.
