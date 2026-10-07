# `Periodic2DCommonSpaceOperatorComparator` implementation

## Operation boundary

The comparator begins with two already constructed represented operators. It does not
construct either parent matrix and does not decide that two arbitrary operators are
compatible. `Periodic2DCommonSpaceComparisonRequest` has already required the exact
cosine adapter classes, one configured parent, one Bloch fiber, and grid resolution
that keeps retained sampling columns distinct.

This separation matters because a finite-difference coordinate matrix and a
plane-wave reciprocal matrix do not become comparable merely because they describe the
same symbolic Hamiltonian. They use different finite state spaces, bases,
normalizations, and discretizations. The comparator owns the explicit numerical map
that identifies the plane-wave common space with one subspace of grid samples for this
specific convention.

## Sampling-map construction

For each direction, the implementation creates an `N` by `2*M+1` matrix. Rows follow
the half-open coordinate order and columns follow increasing reciprocal index. The
entry includes both reduced Bloch momentum and reciprocal index. Division by
`sqrt(N)` in each direction makes the two-dimensional Kronecker product carry the
combined factor `1/N`.

The two-dimensional map uses
`np.kron(first_sampling, second_sampling)`. This is not an incidental vectorization
choice. With first indices outer in both source inventories, it gives:

- row `(i, j)` flattened as `i*N+j`; and
- column `(p, q)` flattened with the shifted `p` index outer and shifted `q` index
  inner.

Changing either source order would require a different explicit map; the implementation
must not infer a permutation from dimensions or numerical spectra.

## Direction of transport

The retained map `T` sends plane-wave coefficients to coordinate-grid samples. The
finite-difference operator therefore returns to plane-wave coordinates through the
congruence

`T.conj().T @ H_fd @ T`.

Using `T @ H_pw @ T.conj().T` would instead push the plane-wave matrix into grid space,
producing a different common-space orientation and a different Result contract. This
Action deliberately chooses the former so the comparison dimension equals the retained
plane-wave cutoff dimension. For `N>2*M+1`, the pullback is a proper-subspace
compression. At `N=2*M+1`, `T` is square unitary and the pullback is a full-space
unitary similarity transform.

## Signed subtraction and diagnostics

Subtraction occurs only after transport. The fixed sign is transported finite
difference minus plane wave. The Result retains the full signed matrix in addition to
its Frobenius and maximum-entry norms so downstream readers can inspect structure and
cannot mistake one scalar norm for the represented discrepancy itself.

The isometry defect is retained rather than used as an internal gate. Exact arithmetic
would give `T.conj().T @ T == I` under the alias prerequisite, but complex128 phase and
matrix-product evaluation introduces finite roundoff. The Action does not choose a
numerical or scientific tolerance on behalf of a convergence study.

## Action/Result separation

The Action owns request-to-value derivation, including coordinate enumeration,
phase evaluation, Kronecker ordering, transport, subtraction, and diagnostic values.
The Result owns immutable types, units, shapes, algebra among retained values, and
correlation of each diagnostic.

Result validation recomputes `T.conj().T @ H_fd @ T` from retained `T` and the retained
source matrix because that equation is an intrinsic relation of the stored outcome. It
does not call the Action's sampling-map method or regenerate `T` from request momentum.
The repeated congruence is a deliberate integrity cost, not a private replay kernel;
it prevents a caller from forging the transported matrix together with a matching
difference and norms. Consequently:

- a corrupted transported matrix is rejected even if its difference and norms are
  forged consistently;
- a manually constructed Result may satisfy intrinsic algebra; and
- such manual construction does not prove that this Action executed or establish
  calculation provenance.

No caller-supplied private witness, low-level constructor bypass, or duplicate private
`_evaluate` kernel is used.

## Range and resource behavior

All map and operator values use complex128; diagnostics use binary64. After transport
and subtraction, the implementation explicitly checks real and imaginary components
for finiteness. It also rejects nonfinite norms. These cases raise `OverflowError`
rather than allowing a later quantity constructor to obscure a range failure as an
ordinary value error.

Let `G=N**2` and `P=(2*M+1)**2`. The dense map stores `G*P` complex values. The input
grid operator stores `G**2=N**4` values, while transported and plane-wave matrices each
store `P**2=(2*M+1)**4` values. Under NumPy's implemented left-associated product,
one congruence requires `O(P*G**2 + P**2*G)` arithmetic plus dense workspace. Result
validation performs that congruence a second time. `MemoryError` is allowed to
propagate, and no arbitrary cutoff or grid cap is introduced.

## External boundaries

The implementation invokes no Quantum ESPRESSO, Wannier90, filesystem, network,
registry, plugin, or persistence boundary. It is a deterministic in-process dense
numerical Action over immutable request values.

## Mapping

- Source: `python/src/ksdft2effmass/periodic2d/compare/common_space.py`
- Public method: `Periodic2DCommonSpaceOperatorComparator.execute`
- Sampling implementation:
  `Periodic2DCommonSpaceOperatorComparator._plane_wave_to_grid_sampling_map`
- Governing specification:
  `specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`
- Parent class page: [Comparator contract](../index.md)
- Mathematics: [Mathematics and physics](mathematics/index.md)
- References: [References and provenance](references/index.md)
- Tests: [Verification strategy](testing/index.md)
