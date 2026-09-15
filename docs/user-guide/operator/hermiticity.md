# Hermiticity analysis

`HermiticityAnalyzer` checks one finite matrix representation against an absolute
entrywise tolerance. It neither changes the record nor participates implicitly in
operator comparison.

## Residual and criterion

For the matrix $\mathbf H$ defined on the
[representation page](representations.md), the analyzer calculates

$$
\varepsilon_{\mathrm H}
=
\max_{0\leq i,j<N}
\left|H_{ij}-H_{ji}^{*}\right|.
$$

The symbols are:

- $\varepsilon_{\mathrm H}$: the absolute Hermiticity residual;
- $H_{ij}$ and $H_{ji}$: entries of the same fixed matrix representation;
- $H_{ji}^{*}$: the complex conjugate of $H_{ji}$;
- $|z|$: the complex magnitude of a scalar $z$;
- $i$ and $j$: zero-based matrix indices; and
- $N$: the represented state-space dimension.

For analyzer tolerance $\tau$, the result classifies the matrix as Hermitian within
the configured software criterion exactly when

$$
\varepsilon_{\mathrm H}\leq\tau.
$$

Here $\tau\geq0$ is the finite analyzer-owned absolute tolerance. Both
$\varepsilon_{\mathrm H}$ and $\tau$ use the exact energy-unit string stored in
the record. Equality is accepted.

## Python usage

Continue from the synthetic `reference` and `candidate` records created on the
[representation page](representations.md):

```python
from ksdft2effmass.operators import HermiticityAnalyzer

hermiticity = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")
reference_result = hermiticity.require(reference)
candidate_result = hermiticity.require(candidate)

assert reference_result.is_hermitian
assert candidate_result.is_hermitian
assert reference_result.residual == 0.0
assert candidate_result.residual == 0.0
```

`execute()` always returns a `HermiticityResult` when numerical evaluation succeeds.
`require()` returns that result only when `is_hermitian` is true.

## Failure and interpretation boundaries

- `HermiticityUnitMismatchError` means the analyzer and record energy-unit strings
  differ. The analyzer performs no conversion.
- `HermiticityRequirementError` means
  $\varepsilon_{\mathrm H}>\tau$.
- `HermiticityNumericalError` means residual evaluation produced a nonfinite value.

Exact Hermiticity is invariant under an exact unitary basis transformation. The
nonzero magnitude of this entrywise residual is generally basis dependent, so it is
not a basis-independent physical distance. Passing `require()` is a software result,
not validation of the parent calculation.

Next, audit [representation compatibility](compatibility.md). Return to the
[operator-analysis overview](index.md).
