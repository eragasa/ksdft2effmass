# `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression`

## Package responsibility

This subordinate campaign package owns one retained post-hoc convergence-time regression
for the periodic-2D Wannier90 optimizer-basin standalone study. It is not a generic
survival-analysis library, optimizer model, oracle, registry, strategy, plugin, or
population-inference framework.

The package keeps three responsibilities explicit and separate:

- exact ownership of retained standalone-result, analyzer-source, and regression-result
  bytes;
- repository-confined authentication of those compact sources; and
- independent reconstruction of the declared finite right-censored log-normal
  diagnostics.

The public result reports bounded software/numerical consistency. It does not rerun
Wannier90, change native convergence flags, fit an alternative model, establish
causality or optimizer convergence, give deterministic starts a population-sampling
interpretation, quantify physical uncertainty, predict DFT behavior, establish
scientific validation, or record acceptance.

## Modules

| Module | Responsibility |
|---|---|
| [`encoded_documents`](encoded_documents/index.md) | Exact immutable ownership of three retained byte strings |
| `records` | Closed immutable source, regression, design, evaluation, and numerical records |
| `decode` | Strict regression decoding and bounded historical-source adaptation |
| `authentication` | Repository-confined byte and SHA-256 authentication |
| `design` | Declared reference/category/start design construction |
| `numerics` | Independent score, likelihood, finite-difference Hessian, and clustered sandwich covariance |
| `correlation` | Aggregate, category, interval, median, and probability correlation |
| `verify` | Verification request, orchestration Action, and immutable Result |
| `data` | Immutable campaign composition and request-scoped verifier construction |

## Historical source-wire exception

The exact retained `standalone-result.json` predates the shared strict JSON contract and
contains bare `Infinity` tokens in basin-comparison fields that row 054 does not consume.
The source adapter therefore uses a campaign-specific historical decoder that:

1. preserves the exact bytes;
2. rejects duplicate keys;
3. recognizes only `Infinity`, `-Infinity`, and `NaN` as temporary markers;
4. exposes none of those unconsumed values to downstream Actions; and
5. requires every consumed endpoint scalar to satisfy the shared strict primitive
   contracts, including finite binary64 conversion.

The regression-result wire remains strict JSON and rejects every nonfinite extension.
This exception is not a general permissive JSON API and assigns no meaning to the
historical nonfinite fields.

## Supported facade

The reviewed local facade exposes only:

- `Periodic2DOptimizerRegressionEncodedDocuments`; and
- `Periodic2DOptimizerRegressionCampaign`.

Request/result and implementation Actions remain with their defining modules rather
than being flattened into the package facade.

## Further documentation

- [Numerical techniques and scientific reasoning](numerical-techniques-and-scientific-reasoning.md)
- [Frozen verification contract](verification-contract.md)
- [`Periodic2DOptimizerRegressionEncodedDocuments`](encoded_documents/Periodic2DOptimizerRegressionEncodedDocuments/index.md)
