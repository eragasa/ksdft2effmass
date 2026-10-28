# `Mathieu1dAnalyzer`

## Status and responsibility

Implemented stateless production action in
`python/src/ksdft2effmass/model_systems/mathieu1d/analysis.py`.

```python
result = Mathieu1dAnalyzer().calculate(
    configuration,
    calculation_family="mathieu1d-finite-reduction",
    execution_id="direct-finite-reduction-n64",
    evidence_status="illustrative numerical experiment",
    claim_boundary="finite represented calculation only",
)
```

`calculate()` composes canonical finite parent constructors, Fourier transformation,
truncation, interpolation, weighted fitting, and diagnostics into one
`Mathieu1dCalculationResult`. It performs no filesystem effects and reads no retained
artifact.

## Invariants

- The configuration is already constructor-validated.
- Metadata is nonempty and the family identifier is exact.
- The larger plane-wave representation is a finite reference.
- Training and withheld evaluation inventories remain separate.
- Every range derives independently from the same complete transform.
- The action does not select an adequate range or claim continuum isolation.

## Public import

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dAnalyzer
```

## Claim boundary

The result records one finite binary64 calculation. Production output alone is not
independent verification, continuum convergence, uncertainty, material validation, or
sealed evidence.
