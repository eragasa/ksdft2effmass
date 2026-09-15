# Analyze represented finite operators

The supported `ksdft2effmass.operators` API analyzes finite operator matrices in one
identified representation. The documentation is divided by functionality so that each
page has one clear owner.

## Functionality pages

Read the pages in this order when constructing a complete comparison:

1. [Representations and synthetic setup](representations.md) defines the
   mathematical operator, stored matrix, ordered basis, unit conventions, and example
   records used by the remaining pages.
2. [Hermiticity analysis](hermiticity.md) documents the entrywise
   Hermiticity residual and analyzer tolerance.
3. [Representation compatibility](compatibility.md) documents the exact
   metadata audit required before direct subtraction.
4. [Signed operator differencing](differencing.md) documents operand order
   and represented subtraction.
5. [Residual analysis](residuals.md) documents the maximum-entry,
   Frobenius, and spectral residuals and their scale-safe binary64 evaluation.
6. [Composed operator comparison](comparison.md) documents the convenience
   Workflow, structured failures, and interpretation boundaries.

The Python snippets form one **illustrative example using synthetic test data** when
run in this order. They do not represent a calculated physical result.

## Retained workflow

The fixed-representation comparison chain is:

```text
OperatorRecordCompatibilityAnalyzer
    -> OperatorRecordDifferencer
        -> OperatorRecordResidualAnalyzer
```

`OperatorRecordComparator` composes that chain. `HermiticityAnalyzer` is an
independent record analysis and is not an implicit comparator stage.

## Preconditions and exclusions

Every operation assumes that the record already identifies its state space, ordered
basis, geometry, energy unit, and energy-zero convention. Exact compatibility checks
represented metadata but does not construct a basis transformation or establish
physical alignment.

This package does **not** perform any of the following as part of operator analysis:

- basis, phase, gauge, geometry, or state correspondence alignment;
- energy or length unit conversion;
- energy-zero selection or correction;
- projection, disentanglement, truncation, fitting, or continuum reduction;
- structured learning or transferability analysis;
- production of scientific findings or their interpretation;
- validation of a parent DFT or Wannier calculation; or
- selection of a scientific acceptance threshold.

A passing software comparison therefore establishes only the documented
fixed-representation contract. It is not scientific validation or uncertainty
quantification.

For the complete object and serialization contract, see
[Finite operator records](../../concepts/operator-records.rst). For executable evidence,
see the [verification index](../../verification/index.rst). The public
language-independent wire contract remains
[`specification/operator-record/v1/`](https://github.com/eragasa/ksdft2effmass/blob/dev/specification/operator-record/v1/README.md).
