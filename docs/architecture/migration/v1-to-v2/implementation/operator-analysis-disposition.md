# Operator-analysis retention disposition

## Status and scope

**Human-accepted and administratively closed.** This disposition applies the accepted Option A operator-ownership decision to the
fixed-representation algorithms currently implemented by `ksdft2effmass.operators`. It covers Hermiticity analysis, exact
representation compatibility, guarded signed differencing, primitive residual norms,
and their concrete comparison composition.

The deterministic disposition is retention in place. No source relocation, public
import change, compatibility facade, wire-format change, dependency change, numerical
definition change, or scientific interpretation is warranted. The accompanying
[User Guide](../../../../user-guide/operator/index.md) explains the retained
operations, equations, variables, units, sign convention, and interpretation limits.

## Accepted ownership boundary

The accepted Option A decision retains one narrow represented-operator kernel:

| Responsibility | Retained owner | Disposition |
|---|---|---|
| Matrix and intrinsic representation metadata | `operators.records` DataObjects | Retain; the sibling records disposition owns the detailed record and schema baseline. |
| Fixed-representation Hermiticity policy and residual | `HermiticityAnalyzer` and `HermiticityResult` | Retain in `operators.hermiticity`. |
| Exact compatibility of two independently valid records | `OperatorRecordCompatibilityAnalyzer` and its structured result | Retain in `operators.compatibility` as the mandatory gate before direct subtraction. |
| Signed represented subtraction | `OperatorRecordDifferencer` and `OperatorRecordDifferenceResult` | Retain in `operators.difference`. |
| Maximum-entry, Frobenius, and spectral residuals | `OperatorRecordResidualAnalyzer` and `OperatorRecordComparisonResult` | Retain in `operators.residuals`. |
| Reusable differencing-plus-residual composition | `OperatorRecordComparator` | Retain in `operators.comparison` as a concrete Workflow ActionObject. |
| Schema-version-1 record serialization | `OperatorRecordJsonSerializer` | Retain unchanged; comparison results and exceptions acquire no wire format. |
| Alignment selection, unit conversion, model fitting, continuum reduction, structured learning, transferability analysis, scientific findings, and interpretation | Higher-level `analysis` or applicable domain owner | Keep outside `operators`; none is introduced by this disposition. |

The retained dependency branches are

```text
records -> compatibility -> difference -> residuals -> comparison
records -> hermiticity
records -> serialization
```

Earlier layers in the comparison chain do not import later layers. Hermiticity and
serialization depend directly on records without entering that chain, and `operators`
does not depend on higher-level `analysis`.

## Retained mathematical contracts

For an ordered orthonormal basis
$\mathcal B=(|b_0\rangle,\ldots,|b_{N-1}\rangle)$, a record stores the finite
matrix representation

$$
H_{ij}=\langle b_i|\hat H|b_j\rangle,
\qquad \mathbf H\in\mathbb C^{N\times N}.
$$

Hermiticity analysis retains the absolute entrywise residual

$$
\varepsilon_{\mathrm H}
=\max_{i,j}|H_{ij}-H_{ji}^{*}|,
$$

and the inclusive software predicate
$\varepsilon_{\mathrm H}\leq\tau$, where $\tau$ is the analyzer-owned tolerance
in the record's exact energy-unit string.

After exact compatibility succeeds, represented differencing retains the operand
order

$$
\Delta\mathbf H
=\mathbf H_{\mathrm{candidate}}-\mathbf H_{\mathrm{reference}}.
$$

Residual analysis retains the three absolute, unnormalized metrics

$$
\varepsilon_{\max}=\max_{i,j}|\Delta H_{ij}|,
\qquad
\varepsilon_{\mathrm F}
=\left(\sum_{i,j}|\Delta H_{ij}|^2\right)^{1/2},
\qquad
\varepsilon_2=\sigma_{\max}(\Delta\mathbf H),
$$

with stored ordering

$$
0\leq\varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}.
$$

All symbols and the scale-safe binary64 policy are defined on the
functionality-specific pages linked from the [User Guide operator-analysis
landing page](../../../../user-guide/operator/index.md), rather than duplicated
here. These are fixed-coordinate matrix quantities. They do not align
bases or gauges and do not combine parent-model, numerical/discretization, and
model-reduction error.

## Exact compatibility boundary

The compatibility analyzer continues to compare these fields exactly and in canonical
mismatch-code order:

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

Record identifier, state-space identifier, basis identifier, geometry system label,
and provenance remain deliberately ignored by this represented-compatibility audit.
Agreement of the eleven checked fields permits the implemented direct subtraction; it
does not establish physical identity, basis or gauge alignment, or scientific
comparability.

Incompatibility remains a structured software result, not a claim that no scientifically
justified transformation could make two records comparable. Any future alignment
operation must identify its state spaces, direction, basis or gauge map, units, geometry,
and energy-reference convention before producing records admitted by this exact gate.

## Numerical and failure disposition

The current structured failure ownership remains unchanged:

| Failure | Owner | Meaning |
|---|---|---|
| Analyzer and record energy-unit strings differ | `HermiticityUnitMismatchError` | Exact unit-metadata mismatch; no conversion is attempted. |
| Hermiticity residual becomes nonfinite | `HermiticityNumericalError` | Fixed-representation residual computation failed numerically. |
| Hermiticity requirement exceeds tolerance | `HermiticityRequirementError` | The retained `HermiticityResult` fails the inclusive software predicate. |
| Compatibility rules fail | `IncompatibleOperatorRecordsError` | Direct represented subtraction is not admitted. |
| Subtraction produces a nonfinite entry | `OperatorRecordDifferenceNumericalError` | Represented differencing failed before residual analysis. |
| Residual metric is nonfinite, SVD fails, or metric order is materially violated | `OperatorRecordComparisonNumericalError` | Residual analysis failed under its scale-safe binary64 policy. |

The residual analyzer retains scale-safe Frobenius and spectral algorithms, explicit
zero handling, power-of-two spectral scaling, and its dimension-dependent relative and
lower-ULP ordering allowance. Canonicalization within that allowance preserves the
mathematical norm ordering; it is roundoff policy, not scientific tolerance or
uncertainty quantification.

## Public compatibility and migration plan

The supported import route remains `ksdft2effmass.operators`. Every currently exported
Hermiticity, compatibility, difference, residual, comparison, record, and serializer
name retains its nominal identity and documented behavior. No new alias, facade,
result serializer, generic analyzer protocol, or package subdivision is introduced.

The strict-conformance migration debt identified by this disposition was not precedent
and was not silently accepted by the ownership decision. The identified `typing.Any`,
cast-through-`Any`, erased JSON representations, module-level test callables, and tests
not yet grouped beneath one cohesive `Test...` owner required separately bounded
implementation authority. That migration had to:

1. preserve public signatures, accepted runtime scalar families, exception taxonomy,
   numerical definitions, tolerances, and evidence identities;
2. replace erased JSON values with a closed recursive representation and typed parser
   boundary;
3. move test-only builders and collected tests to their cohesive test owner classes;
4. use narrow code-specific type-checker suppressions only at intentional invalid-call
   sites;
5. preserve the schema-version-1 fixtures and the distinction between software and
   numerical verification; and
6. demonstrate no import, wire, numerical, or public-behavior drift before the parent
   operator-ownership task may close.

This disposition planned those corrections but did not authorize them in its
planning-and-documentation slice. The separately activated parent
`migration.v2.operators-ownership` Task has now implemented and verified them without
changing this child decision; the parent result is human-accepted and administratively
closed.

## Evidence and claim boundary

Construction, compatibility codes, exception structure, dependency direction, and
public imports are software verification. Independently derived Hermiticity and norm
cases are numerical verification. Neither establishes basis or gauge alignment,
physical model adequacy, scientific validation, uncertainty quantification, or
acceptance of a reduction.

No material architecture choice remains in this bounded disposition. Option A already
determines retention. Later public-contract changes motivated by concrete impurity,
projection, embedding, spinor, or continuum use cases require separate authority and
applicable compatibility evidence.
