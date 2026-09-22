# Composed operator comparison

`OperatorRecordComparator` is the supported convenience Workflow for a complete
fixed-representation comparison. It composes compatibility-guarded differencing and
residual analysis without adding hidden alignment or acceptance policy.

## Composition

The comparator performs these steps in order:

1. `OperatorRecordCompatibilityAnalyzer.require(reference, candidate)`;
2. `OperatorRecordDifferencer.execute(reference, candidate)`; and
3. `OperatorRecordResidualAnalyzer.execute(difference)`.

The differencer owns the compatibility call, so the concrete comparator stores a
differencer and a residual analyzer. `HermiticityAnalyzer` remains an independent
operation; the comparator does not call it implicitly.

## Python usage

Continue from the synthetic records and `metrics` result created on the preceding
functionality pages:

```python
from ksdft2effmass.operators import OperatorRecordComparator

composed_metrics = OperatorRecordComparator().execute(reference, candidate)

assert composed_metrics == metrics
assert composed_metrics.reference_identifier == "reference"
assert composed_metrics.candidate_identifier == "candidate"
assert composed_metrics.energy_unit == "eV"
```

The result contains the maximum-entry, Frobenius, and spectral residuals defined on
the [residual-analysis page](residuals.md). The candidate-minus-reference sign
convention remains the one defined on the
[differencing page](differencing.md).

## Structured failures

Use structured fields rather than parsing exception text:

```python
from ksdft2effmass.operators import (
    IncompatibleOperatorRecordsError,
    OperatorRecordComparator,
)

try:
    result = OperatorRecordComparator().execute(reference, candidate)
except IncompatibleOperatorRecordsError as error:
    mismatch_codes = tuple(issue.code for issue in error.compatibility_result.issues)
```

The composed Workflow can propagate:

- `IncompatibleOperatorRecordsError` when one or more exact compatibility rules fail;
- `OperatorRecordDifferenceNumericalError` when subtraction produces a nonfinite
  entry; and
- `OperatorRecordComparisonNumericalError` when a residual metric is nonfinite,
  singular-value computation fails, a scaled matrix is nonfinite, or norm ordering is
  materially inconsistent.

Hermiticity failures are absent from this list because Hermiticity analysis is not a
comparator stage.

## Interpret results conservatively

A successful comparison establishes only that:

1. the represented metadata passed the exact implemented compatibility rules;
2. subtraction used candidate minus reference in those stored coordinates; and
3. the returned absolute residual metrics satisfy their documented numerical
   contract.

It does not establish that the records have been physically aligned, that their basis
labels encode the same wavefunctions, that their phases or gauges agree, that either
parent calculation is converged, or that a residual is acceptable for an intended
scientific use.

Parent-model error, numerical or discretization error, and model-reduction error must
remain separate unless an owning specification defines their mathematical
relationship. Comparator success is a software result under the stated contract; it
does not by itself establish numerical verification. Separately maintained,
independently derived cases may provide numerical-verification evidence. Neither form
of evidence is scientific validation or uncertainty quantification.

Return to the [operator-analysis overview](index.md), or revisit:

- [Representations and synthetic setup](representations.md)
- [Hermiticity analysis](hermiticity.md)
- [Representation compatibility](compatibility.md)
- [Signed operator differencing](differencing.md)
- [Operator residual analysis](residuals.md)
