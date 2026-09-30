# Representation compatibility

Direct matrix subtraction is permitted only after an exact compatibility audit.
`OperatorRecordCompatibilityAnalyzer` compares the metadata needed to interpret two
matrices in the same stored coordinates.

## Compatibility relation

Let $\mathcal R$ be the reference `OperatorRecord` and $\mathcal{C}$ the candidate
`OperatorRecord`. The implemented relation is

$$
\operatorname{compatible}(\mathcal R,\mathcal{C})
\iff
\forall f\in\mathcal F_{\mathrm{compat}},
\quad f(\mathcal R)=f(\mathcal{C}).
$$

The symbols are:

- $\mathcal R$: the complete reference record, including matrix and metadata;
- $\mathcal{C}$: the complete candidate record;
- $\operatorname{compatible}$: exact software admission for direct represented
  subtraction;
- $\mathcal F_{\mathrm{compat}}$: the ordered set of compatibility-critical field
  projections;
- $f$: one projection that selects a compatibility-critical field; and
- $f(\mathcal R)=f(\mathcal{C})$: exact equality of that field, without tolerance
  or conversion.

In canonical mismatch-code order, $\mathcal F_{\mathrm{compat}}$ selects:

1. matrix dimension;
2. state-space kind;
3. operator kind;
4. ordered basis labels;
5. basis kind;
6. row lattice vectors;
7. boundary conditions;
8. coordinate convention;
9. geometry length unit;
10. energy unit; and
11. energy-zero convention.

The audit deliberately ignores record identifier, state-space identifier, basis
identifier, geometry system label, and provenance. Those fields remain available as
identity or provenance but do not decide direct subtractability.

## Python usage

Continue from the synthetic records created on the
[representation page](representations.md):

```python
from ksdft2effmass.operators import OperatorRecordCompatibilityAnalyzer

compatibility = OperatorRecordCompatibilityAnalyzer()
audit = compatibility.execute(reference, candidate)
assert audit.is_compatible
assert audit.issues == ()

required_audit = compatibility.require(reference, candidate)
assert required_audit == audit
```

`execute()` returns every mismatch in canonical order. `require()` returns the
compatible result or raises `IncompatibleOperatorRecordsError`, which retains the
complete structured result.

Use structured issue codes rather than parsing exception text:

```python
from ksdft2effmass.operators import IncompatibleOperatorRecordsError

try:
    compatibility.require(reference, candidate)
except IncompatibleOperatorRecordsError as error:
    mismatch_codes = tuple(issue.code for issue in error.compatibility_result.issues)
```

## Interpretation boundary

Exact field equality does not prove that basis labels identify the same wavefunctions,
that phases or gauges agree, or that the records represent the same physical system.
The analyzer does not align representations. Those prerequisites must be established
before direct subtraction by an external, documented process.

Next, form the [signed represented difference](differencing.md). Return to
the [operator-analysis overview](index.md).
