# `Periodic2DOptimizerRegressionEncodedDocuments`

## Classification

`Periodic2DOptimizerRegressionEncodedDocuments` is a frozen, slotted encoded-document
DataObject for crosswalk row `PERIODIC-XWALK-054`. It replaces the misleading former
`Periodic2DOptimizerRegressionCampaignModel` name without a compatibility alias.

It is **not** a physical model, mathematical operator, finite representation, retained
space or operator, represented operator, effective model, convergence theorem,
probability distribution over starts, provenance record, validation result, or
acceptance decision.

## Exact state

| Field | Contract |
|---|---|
| `standalone_result_payload` | Exact nonempty built-in `bytes` for retained `standalone-result.json` |
| `analyzer_payload` | Exact nonempty built-in `bytes` for retained `analyze_standalone_convergence_regression.py` |
| `regression_payload` | Exact nonempty built-in `bytes` for retained `standalone-convergence-regression.json` |

No field owns a repository path. The authenticating Action receives an absolute
`repository_root` through the verification request and confines maintained-file reads to
that root.

## Retained identities

The maintained compact files are under
`calculations/research-monograph/periodic-2d-optimizer-basin/`:

| File | SHA-256 |
|---|---|
| `standalone-result.json` | `add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a` |
| `analyze_standalone_convergence_regression.py` | `e80c16ab7fd11d86e6c51a344e01790306982f1a628b962611dfd0291d16fe46` |
| `standalone-convergence-regression.json` | `572b5ca7fe73ebb1cee6d9334e9ad6cddddea446fad3d02dfaf88202096ced22` |

SHA-256 establishes content identity only. It does not establish historical execution,
provenance, decoded correctness, model adequacy, convergence, causal interpretation,
uncertainty, scientific validation, or acceptance.

## Verified bounded behavior

A request-scoped verifier authenticates all three exact wires, adapts consumed fields to
closed immutable records, reconstructs a 256-observation design with 196 retained native
convergence events and 60 right-censored observations, and independently recomputes the
32-parameter likelihood and deterministic-start-clustered diagnostics. See the
[field-by-field contract](../../verification-contract.md) and
[numerical explanation](../../numerical-techniques-and-scientific-reasoning.md).

The source wire contains historical bare `Infinity` tokens only in fields outside this
row's consumed endpoint contract. A bounded source adapter rejects duplicate keys and
nonfinite consumed values; the regression wire remains strict JSON.

## Evidence

### Routine class-owned evidence

- `test__Periodic2DOptimizerRegressionEncodedDocuments.py`
- `test__Periodic2DOptimizerRegressionCampaignContracts.py`
- `test__Periodic2DOptimizerRegressionActionOwnership.py`
- `test__Periodic2DOptimizerRegressionDocumentDecoder.py`

These tests establish intrinsic representation, immutability, request/result validation,
Action ownership, documentation, strict regression decoding, and the bounded historical
source-wire exception. They do not authenticate retained files.

### Artifact-owned evidence

- `test__integration__periodic_2d_optimizer_regression_artifacts.py`
- `test__integration__periodic_2d_optimizer_regression_fail_closed.py`

These tests bind maintained bytes and checksum-catalog identities, exercise the portable
reconstruction, and demonstrate sensitivity to forged digests, changed analyzer bytes,
aggregate corruption, and fitted-parameter corruption. Their passing establishes
bounded software behavior and numerical consistency only.

## Supported imports

The same defining class is available from four reviewed facades:

- `ksdft2effmass.periodic2d`;
- `ksdft2effmass.periodic2d.run.wannier90`;
- `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin`; and
- `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression`.

The retired model-named class and retained-model module remain absent; no alias or
forwarding module is provided.

## Limitations

The 16 deterministic starts are finite design controls, not random population samples.
Right-censoring retains stopped trajectories in the declared exploratory model but does
not convert them into convergence events. Clustered intervals are finite model-based
diagnostics and have no population-sampling or physical-uncertainty interpretation.
The verifier does not rerun or refit Wannier90, prove optimizer convergence or global
optimality, establish causality, predict DFT behavior, validate the chosen statistical
family, establish scientific validation, or record acceptance.
