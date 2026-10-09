# `periodic1d.campaign.reduction_challenge`

## Purpose and status

This package is the canonical owner of the Appendix G periodic-1D
**reduction-challenge** campaign. “Challenge” means adversarial tests of the assumptions
behind a finite represented reduction: potential strength and shape, reciprocal-mesh
sampling, selected-band isolation, gauge covariance, hopping reconstruction, and route
agreement. It does **not** mean mechanical stress, strain, elasticity, or a stress
tensor.

`PERIODIC-XWALK-060` moved the complete family from
`ksdft2effmass.campaigns.periodic_1d` without compatibility aliases. Historical
`stress-input.json`, `stress-result.json`, version-one JSON keys, experiment identity,
evidence-status text, and `STRESS` result-kind discriminator remain exact wire
identities. Canonical Python names use `Periodic1DReductionChallenge...` throughout.
No calculator was invoked and no retained input or result byte changed.

## Ownership map

| Module | Responsibility | Documentation |
|---|---|---|
| `definition` | Immutable controls and strict version-one input adaptation | [Definition](definition/index.md) |
| `encoded_documents` | Exact input/result byte ownership only | [Encoded documents](encoded_documents/index.md) |
| `results` | Immutable typed observations and strict result adaptation | [Results](results/index.md) |
| `correlation_workflow` | Exact-byte authentication and complete cross-document correlation | [Correlation Workflow](correlation_workflow/index.md) |
| `correlation` | Request/Result Action boundary around correlation | [Correlation](correlation/index.md) |
| `numerical_verification` | Independent bounded reconstruction of retained channels | [Numerical verification](numerical_verification/index.md) |
| `verification` | Correlation-first campaign verification orchestration | [Verification](verification/index.md) |
| `verified_workflow` | Integrated correlation and numerical-verification outcomes | [Verified Workflow](verified_workflow/index.md) |
| `campaign` | Cohesive encoded-document campaign facade | [Campaign](campaign/index.md) |

The package facade and `ksdft2effmass.periodic1d.campaign` facade expose the same
reviewed class objects. The former underscored and publication facades expose neither
the canonical names nor former `Periodic1DStress*` names.

## Scientific and evidence boundaries

The campaign definition is a set of controls, not a physical model or represented
operator. The result contains reported finite-representation diagnostics, not a
retained scientific subspace, exact retained operator, or accepted effective model.
Correlation authenticates and relates immutable wires; it does not prove historical
execution. Independent numerical verification reconstructs only the explicitly
retained version-one channels under the declared represented conventions. Expected
trends in the historical wire remain observations and are not converted into pass/fail
criteria.

Passing tests establishes bounded software behavior, content identity, and numerical
consistency. It does not establish continuum convergence, scientific validation,
physical adequacy, transferability, uncertainty quantification, or acceptance.

## Detailed contracts

- [Numerical techniques and scientific reasoning](numerical-techniques-and-scientific-reasoning.md)
- [Verification contract](verification-contract.md)
- [Migration phase 5](../../../periodic/migration-5.md)
- [Crosswalk](../../../periodic/current-to-target-class-crosswalk.md)

```{toctree}
:hidden:

definition/index
encoded_documents/index
results/index
correlation_workflow/index
correlation/index
numerical_verification/index
verification/index
verified_workflow/index
campaign/index
numerical-techniques-and-scientific-reasoning
verification-contract
```
