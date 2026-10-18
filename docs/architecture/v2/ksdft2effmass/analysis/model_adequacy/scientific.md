# Model-adequacy scientific boundary

## Distinct mathematical roles

The architecture keeps the following objects distinct.

A **metric or residual** measures a declared difference. It may carry physical units
and need not be normalized.

A **loss** is a scalar function with declared inputs, sampling, weights, units,
normalization, and role. A loss does not contain an acceptance threshold unless its
specific contract says so.

An **objective** is a loss or combination of losses selected for optimization. Calling a
quantity a loss does not imply that an optimizer was run or that a global minimum was
found.

An **admissible set** is a thresholded subset of one declared candidate-parameter domain.
The threshold and domain are separate scientific inputs.

A **common witness** identifies one candidate satisfying every applicable criterion. Two
separate channel minimizers are not a common witness.

A **separation certificate** supplies a valid positive lower bound on distance between
complete declared admissible sets. A failed search or pair of optimized points is not a
separation certificate.

A **disposition** records bounded mathematical logic such as compatible witness,
certified separated, or unresolved. It is not human scientific acceptance.

## Canonical loss-channel notation

The architecture reserves:

| Symbol | Meaning | Units | Primary owner |
|---|---|---|---|
| $R_E$ | Ordered spectral RMS error over declared samples | Energy | Model-adequacy spectral analyzer |
| $L_E=R_E/E_0$ | Normalized ordered spectral RMS loss | Dimensionless | Model-adequacy spectral analyzer |
| $R_H$ | Represented-operator RMS residual over declared compatible samples | Energy | PhysKit dimensionful aggregation |
| $L_H=R_H/E_0$ | Normalized represented-operator RMS loss | Dimensionless | Model-adequacy normalization |
| $E_0$ | Declared finite positive energy scale | Energy | Loss definition/domain wrapper |
| $\tau_E,\tau_H$ | Channel thresholds | Dimensionless | Admissible-set definition |

$L_E$ and $L_H$ are distinct loss channels even when they happen to have equal numeric
values. A serializer must not identify a channel only from a float.

## Generic quadratic geometry

The exact-pinned Optimization facade represents a unit-free squared loss on one declared
canonical coordinate vector $x\in\mathbb R^n$:

<a id="eq-model-adequacy-quadratic-001"></a>

$$
L(x)^2 = L_{\min}^2 + (x-c)^TQ(x-c),
\qquad
Q=Q^T\succ0,
\qquad
L_{\min}^2\ge0.
\tag{EQ-MODEL-ADEQUACY-QUADRATIC-001}
$$

Here:

- $x$ is a finite vector of explicitly normalized dimensionless canonical coordinates;
- $c\in\mathbb R^n$ is the center in the same coordinate convention;
- $Q\in\mathbb R^{n\times n}$ is a finite symmetric positive-definite matrix;
- $L_{\min}^2$ is the finite nonnegative minimum squared loss; and
- $L(x)$ is the nonnegative dimensionless root-mean-square loss value.

The Optimization facade represents this completed-square function only. The represented
$L$ is identified by its KSD wrapper as either $L_E$ or $L_H$; the facade stores no
spectral/operator label. It does not claim that the source physical model is convex,
that a bounded-domain minimum equals $c$, or that a threshold set is nonempty. Box
clipping, inactive coordinates, and channel unions belong to outward owners.

The authoritative pedagogical derivation is
`docs/publications/research-monograph/chapters/admissible-sets-and-certificates.tex`.
This page defines the mathematics consumed through the external Optimization API rather
than a supported local API or a competing physical model.

## Coordinate normalization boundary

Every wrapper must map its scientific parameters into $x$ explicitly.

- M3 already uses two dimensionless coordinates: energy-shift ratio and positive
  splitting scale.
- An HSH coefficient vector is energy-valued. Its HSH owner must retain the energy unit
  and positive scale, form a declared dimensionless coefficient-ratio vector, and retain
  enough information to reconstruct that map. The generic quadratic must not silently
  divide by an inferred scale.
- Mixed-unit parameter vectors require a separately reviewed coordinate-normalization
  contract; they are not accepted by the exact-pinned Optimization facade.

Changing coordinate normalization changes $c$, $Q$, parameter distances, and potentially
certificate values. It creates a different loss representation even when the underlying
unnormalized residual formula is physically related.

## Spectral-loss boundary

The ordered spectral RMS error and normalized loss are

<a id="eq-model-adequacy-spectral-002"></a>

$$
R_E^2 =
\frac{\sum_i w_i\sum_{n=1}^{r}
  |E^{\mathrm{cand}}_{in}-E^{\mathrm{target}}_{in}|^2}
 {r\sum_i w_i},
\qquad
L_E=\frac{R_E}{E_0},
\qquad
w_i>0,
\qquad
E_0>0.
\tag{EQ-MODEL-ADEQUACY-SPECTRAL-002}
$$

Thus $R_E$ has the common energy unit and $L_E$ is dimensionless. The exact coordinate
identity, ordered-band convention, target/candidate unit conversion, positive weights,
retained rank, and energy scale are part of the loss definition. Training and withheld
sample sets are evaluated by separate calls and results.

No common spectral-loss API is implemented. The existing
`BandApproximationErrorAnalyzer1D` remains a maximum-absolute-error analyzer, not this
RMS loss. Generic affine-residual and spectral-loss mechanics are assigned to
Optimization; KSD-specific sample identity, units, normalization, and channel
meaning remain with model adequacy.

## Represented-operator-loss boundary

For already compatible and aligned represented operator samples, the dimensional
aggregate and normalized loss are

<a id="eq-model-adequacy-operator-003"></a>

$$
R_H^2 =
\frac{\sum_i w_i\|\Delta H_i\|_F^2}
 {r\sum_i w_i},
\qquad
L_H=\frac{R_H}{E_0}.
\tag{EQ-MODEL-ADEQUACY-OPERATOR-003}
$$

This factorization fixes the ownership boundary. `operators` owns represented-space
compatibility, operand order, subtraction, and primitive residual mechanics. PhysKit
owns unit conversion and reusable dimensionful hopping/Frobenius aggregation through
$R_H$. Model adequacy owns the scientific choice of sample set and weights, the positive
scale $E_0$, and the dimensionless normalization $L_H=R_H/E_0$. Alignment-family and
energy-reference selection happen before aggregation and remain outward scientific
policy.

No common $L_H$ normalization API is selected initially. A future API consumes a
PhysKit-owned aggregate result rather than recalculating matrix differences. For HSH,
reusable dimensionful hopping-coefficient/Frobenius residual mechanics belong
to PhysKit. HSH selects the projected target, comparison domain, weights, and energy
scale, then owns the dimensionless normalized channel meaning. Unit-free quadratic
completion and optimization belong to optimization.

## Quadratic wrappers

The generic optimization quadratic carries no channel identity. Outward wrappers retain the scientific
meaning required to interpret it.

An M3 wrapper retains:

- the channel identifier;
- optional frozen global alignment angle;
- the shift/splitting coordinate convention; and
- correlation to the M3 definition, result, and schema.

An HSH wrapper retains:

- source and shell-class identity;
- spectral or operator channel identity;
- ordered active indices in the common maximal coefficient space;
- exact inactive-zero semantics and separate solver-feasibility defect reporting;
- coefficient energy unit and normalization scale;
- reconstruction and correlation defects; and
- correlation to HSH weights, box, and source projection.

The wrappers may share completed-square evaluation without sharing scientific policy.

## Admissible-set and certificate boundary

Thresholds, parameter boxes, alignment unions, nonemptiness, witness records,
scientific certificate meaning, and separation resolution are not fields of the generic
quadratic.
They remain with the applicable adequacy analysis.

M3 and HSH certificates remain distinct:

- M3 uses a special two-coordinate axial Euclidean construction under checked quadratic
  premises and unclipped-extreme assumptions.
- The prospective HSH certificate uses a weighted coefficient metric, conservative
  support endpoints, and an explicitly identified outward-rounding policy.

Generic parameter-space metric, distance, dual-norm, feasibility, and support
optimization belong to Optimization. Physically interpreted hopping/Frobenius
geometry belongs to `exports/physkit`. KSD-specific certificate premises, rounding
policy, evidence meaning, and dispositions remain local.

## Evidence and claim boundary

A loss evaluation can establish only the value of the declared finite mathematical
function for its inputs. A verified admissible-set result can establish only bounded
compatibility or separation within its frozen candidate family, coordinates, alignment
family, data roles, thresholds, metric, and certificate premises.

None of these objects establishes:

- material validity or transferability;
- physical calibration of a threshold;
- global optimality outside the declared family;
- scientific validation;
- uncertainty quantification; or
- human scientific acceptance.

## Equation mapping

| Equation | Owner | Implementation status |
|---|---|---|
| `EQ-MODEL-ADEQUACY-QUADRATIC-001` | `projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss` | Accepted upstream, exact-pinned, and consuming-project smoke-tested |
| `EQ-MODEL-ADEQUACY-SPECTRAL-002` | Future spectral-loss definition/analyzer | Deferred |
| `EQ-MODEL-ADEQUACY-OPERATOR-003` | Future PhysKit dimensionful aggregate $R_H$ plus adequacy normalization $L_H$ | Deferred |

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Dependency evidence | Optimization reports 95 owner cases and clean quality/build gates; focused KSD dense/sparse smoke cases pass | Exact-pinned facade behavior only |
| Numerical verification | Bounded smoke evidence | Dense and sparse facade values agree with one hand-derived completed square | One unit-free example; no retained campaign result |
| Scientific validation | Not evaluated | No material comparison is defined | None |
| Uncertainty quantification | Not applicable | Losses and thresholds are deterministic controls | None |
| Human acceptance | Not applicable | Mathematical dispositions are not acceptance decisions | None |

## Provenance

Original local work under the repository license. The quadratic and admissible-set
interpretation is derived from the maintained research-monograph chapter identified
above and the current bounded M3 software contract. No M3 numerical outcome is reused as
an oracle for the external facade.
