# Numerical contract

## State spaces before arithmetic

Every represented vector, frame, Hamiltonian, projector, and hopping block identifies
its finite state space and ordered coordinates. Two operators are subtracted only after
an explicit map places them in the same state space and basis.

Plane-wave and finite-difference fiber matrices are different finite representations.
A shared momentum label does not make their coordinate spaces equal. Their comparison
requires an explicit retained-space or common-coordinate construction. Likewise,
matrices at different reciprocal points are not compared entrywise before their frames
and sewing conventions are aligned.

A rectangular map is a coordinate injection, restriction, projection, or alignment map;
it is not a Hamiltonian. Square represented Hamiltonians retain their energy units and
Hermiticity contract.

## Periodic geometry and ordering

Each configuration declares:

- the primitive period and its unit;
- the reciprocal-coordinate convention and Brillouin-zone interval;
- ordered half-open sampling meshes and endpoint sewing;
- the plane-wave reciprocal-index order or finite-difference point order;
- Bloch boundary-phase sign convention;
- retained-band or retained-subspace order; and
- centered Born--von Karman cell representatives used by Fourier transforms.

No analyzer infers these conventions from array length. Changing a convention changes a
configuration or calculation family; it is not a plotting preference.

## Parent representations

A real finite Fourier potential has one constant coefficient and equal-length cosine and
sine coefficient inventories with compatible units. The maintained
`model_systems.periodic_1d` constructors own the finite plane-wave and periodic finite-
difference fiber representations. Sparse inputs remain sparse unless a public contract
explicitly authorizes bounded materialization.

Parent-model error, plane-wave cutoff error, finite-difference error, eigensolver error,
and reciprocal-sampling error remain distinct. Agreement between two finite
representations does not prove agreement with the continuum operator.

## Scalar retained bands

A scalar band value at each ordered reciprocal point has no nontrivial internal unitary
conjugation: for `U(k)` in `U(1)`,

$$
U(k)^\dagger H(k)U(k)=H(k).
$$

Phase transport can still matter for wavefunctions and localization, but it cannot be
reported as a change in a scalar represented Hamiltonian. The compatible rank-one
locality calculation therefore emits no duplicate gauge-alignment result.

The complete scalar hopping transform and its inverse reconstruction form one correlated
result. Finite-range truncation is a separate operation. Weighted or incomplete fitting
is another route and is not relabeled as transform truncation even when a special
complete equal-weight case agrees numerically.

## Composite retained spaces

A composite result declares parent and retained ranks, ordered frames, sewing maps,
neighbor overlaps, conditioning thresholds, and the exact pointwise or global alignment
objective. Projection, transport, Procrustes alignment, gauge attack, and Fourier
transformation remain separate result sections.

Exact pointwise spectral equivalence does not imply equal hopping locality. A finite-
range comparison must report both the representation relation and the truncation
consequence. Exact fixed-unitary Fourier equivariance does not cover a momentum-dependent
alignment `U(k)`: point-dependent transformations generally mix Fourier modes and require
separate finite reconstruction and verification. Block hoppings check

$$
T(-R)=T(R)^\dagger
$$

under the declared Fourier sign and normalization conventions.

Rank-two and higher-rank calculations may consume the same alignment primitive, but
they retain separate configurations, execution records, tolerances, and scientific
interpretations unless a reviewed contract proves those meanings identical.

## Energy reference and units

Every Hamiltonian-valued section records one explicit energy unit and energy-reference
rule. Constant shifts are applied and reported through a named operation. A fitted or
aligned Hamiltonian is not compared with a parent under an implicit independent shift.

Quantity constructors reject incompatible units, nonfinite values, Boolean numeric
inputs, and numeric strings. Binary64 arrays are finite represented values. Their JSON
encodings are not treated as exact real or rational data.

## Error channels

At minimum, applicable families keep these channels separate:

1. parent-model discrepancy;
2. finite-representation discrepancy;
3. eigensolver or reconstruction residual;
4. reciprocal-sampling discrepancy;
5. subspace-selection or projection discrepancy;
6. alignment or sewing discrepancy;
7. complete Fourier reconstruction discrepancy;
8. fitting-route discrepancy;
9. truncation or omitted-hopping discrepancy; and
10. withheld-evaluation discrepancy.

Adjacent mesh or cutoff changes are finite-representation change diagnostics. Without a
declared extrapolation model, regularity assumptions, and justified asymptotic regime,
they are not continuum errors, convergence rates, uncertainties, or acceptance
criteria.

## Verification route

Production uses canonical PhysKit/KSD owners for represented linear algebra and matrix
norms. Independent verification uses direct finite formulas or an independently
assembled NumPy/SciPy route and does not import the producer analyzer. Tolerances belong
to named verification comparisons, not to the physical configuration or serializer.

For interval-certified decisions, an interval that overlaps a decisive threshold is
`unresolved`, not pass or fail. Joint thresholds are evaluated for one common candidate,
support, and alignment; combining channel-wise minima from different candidates does not
create a feasible point. First-passage claims inspect every earlier member of the
complete declared finite inventory and assume no unstated monotonicity.

A passing comparison establishes bounded agreement for the declared finite case only.
