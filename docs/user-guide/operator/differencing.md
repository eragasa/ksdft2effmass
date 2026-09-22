# Signed operator differencing

`OperatorRecordDifferencer` audits compatibility and then subtracts two operator
matrices in their shared stored representation.

## Difference definition

Let $\mathcal R$ and $\mathcal{C}$ be the compatible reference and candidate records
defined on the [compatibility page](compatibility.md). The differencer forms

$$
\Delta\mathbf H
=
\mathbf H_{\mathrm{candidate}}
-
\mathbf H_{\mathrm{reference}}.
$$

The symbols are:

- $\mathcal R$: the reference `OperatorRecord`;
- $\mathcal{C}$: the candidate `OperatorRecord`;
- $\mathbf H_{\mathrm{reference}}\in\mathbb C^{N\times N}$: the matrix stored by
  $\mathcal R$;
- $\mathbf H_{\mathrm{candidate}}\in\mathbb C^{N\times N}$: the matrix stored by
  $\mathcal{C}$;
- $\Delta\mathbf H\in\mathbb C^{N\times N}$: the signed represented difference;
- $\Delta H_{ij}$: row-$i$, column-$j$ entry of $\Delta\mathbf H$;
- $N$: the common represented state-space dimension; and
- $i,j\in\{0,\ldots,N-1\}$: zero-based matrix indices.

Operand order is part of the contract: the candidate is the positive term and the
reference is the negative term. Reversing them changes the sign.

## Python usage

Continue from the compatible synthetic records:

```python
import numpy as np

from ksdft2effmass.operators import OperatorRecordDifferencer

difference = OperatorRecordDifferencer().execute(reference, candidate)

assert difference.reference_identifier == "reference"
assert difference.candidate_identifier == "candidate"
assert difference.energy_unit == "eV"
assert np.array_equal(
    difference.matrix,
    np.array([[0.125, 0.0], [0.0, -0.25]], dtype=np.complex128),
)
```

The returned `OperatorRecordDifferenceResult` preserves compatibility metadata and
immutable copies of the represented difference.

## Failure and interpretation boundaries

- `IncompatibleOperatorRecordsError` means one or more exact compatibility rules
  failed before subtraction.
- `OperatorRecordDifferenceNumericalError` means finite compatible inputs produced a
  nonfinite difference entry.

A generic $\Delta\mathbf H$ is not automatically an impurity operator, perturbation,
error operator, or physical observable. The software result records subtraction in one
fixed representation; scientific meaning requires a separately specified model and
alignment argument.

Next, calculate [absolute residual metrics](residuals.md). Return to the
[operator-analysis overview](index.md).
