# `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin`

## Purpose and migration status

This package owns the retained periodic-2D Wannier90 optimizer-basin campaign and its
reanalysis, convergence-regression, and standalone follow-up families. Exact encoded
wire ownership remains distinct from native execution, basin classification, numerical
verification, and scientific acceptance.

Crosswalk row 052 reconciles the base optimizer-basin input/result pair. Rows 053–055
separately audit the follow-up document owners. Row 072 completes the four campaign
families with closed immutable records and cohesive request-scoped authentication,
decoding, correlation, numerical, refinement, and verification Actions. The retained
base result records a negative finite-parameter convergence disposition; exact-wire
ownership preserves that statement but does not independently establish it.

## Child map

- [Base encoded documents](encoded_documents/index.md)
  - [`Periodic2DOptimizerBasinEncodedDocuments`](encoded_documents/Periodic2DOptimizerBasinEncodedDocuments/index.md)
- [Numerical techniques and scientific reasoning](numerical-techniques-and-scientific-reasoning.md)
- [Frozen portable-verification contract](verification-contract.md)
- [Campaign-specific offline reanalysis](reanalysis/index.md)
  - [Encoded-document module](reanalysis/encoded_documents/index.md)
  - [`Periodic2DOptimizerReanalysisEncodedDocuments`](reanalysis/encoded_documents/Periodic2DOptimizerReanalysisEncodedDocuments/index.md)
- [Exploratory convergence-time regression](convergence_regression/index.md)
  - [Encoded-document module](convergence_regression/encoded_documents/index.md)
  - [`Periodic2DOptimizerRegressionEncodedDocuments`](convergence_regression/encoded_documents/Periodic2DOptimizerRegressionEncodedDocuments/index.md)
  - [Numerical techniques and scientific reasoning](convergence_regression/numerical-techniques-and-scientific-reasoning.md)
  - [Frozen verification contract](convergence_regression/verification-contract.md)
- [Standalone optimizer follow-up](standalone/index.md)
  - [Encoded-document module](standalone/encoded_documents/index.md)
  - [`Periodic2DOptimizerStandaloneEncodedDocuments`](standalone/encoded_documents/Periodic2DOptimizerStandaloneEncodedDocuments/index.md)
  - [Schematic](standalone/schematic.md)
  - [Numerical contract](standalone/numeric.md)
  - [Scientific reasoning and claim boundary](standalone/scientific.md)
  - [Frozen verification contract](standalone/verification-contract.md)

## Supported imports and evidence

The reviewed `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin` facade exposes
only the four campaign records and their exact encoded-document owners. Detailed
requests, Results, and Actions remain in defining modules. Exact campaign nodes are:

- `python/tests/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__Periodic2DOptimizerBasinCampaign.py`;
- `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__Periodic2DOptimizerReanalysisCampaignContracts.py`;
- `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/standalone/test__Periodic2DOptimizerStandaloneCampaignContracts.py`; and
- `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/convergence_regression/test__Periodic2DOptimizerRegressionCampaignContracts.py`.

All four mirrored `resources/implementation-verification-ownership.json` manifests bind
class-owned and artifact-owned nodes. Sphinx maps the family in
`doc/sphinx/api/ksdft2effmass/periodic2d/run/optimizer-basin.rst`; child architecture
pages document family-specific wire exceptions, numerics, provenance authentication,
and verification contracts.

## Claim boundary

The retained study varies nine numerical configurations and eight smooth periodic
initial gauges while preserving the declared rank-three subspace. Encoded outcomes do
not prove a global optimum or general localization convergence. Reported completion and
basin labels require explicit authentication and verification; digest identity alone is
insufficient.

The convergence-time regression retains all 256 standalone endpoints, including 60
right-censored trajectories, in one declared exploratory log-normal model. Its 16
starts are deterministic design controls rather than population samples. Reproduced
clustered intervals therefore do not establish causal effects, population inference, or
physical uncertainty.
