# Software realization of the higher-rank study

## Python modules

| Module | Scientific role |
|---|---|
| `definition.py` | Names the four alignment families and the possible alignment and numerical outcomes. |
| `configuration.py` | Stores the fixed ranks, depths, construction, global-unitary-selection and evaluation meshes, phase convention, and tolerances. |
| `request.py` | Selects one rank/depth/construction-mesh transport and its ambient-basis, retained-frame, and endpoint-sewing identities. |
| `result.py` | Stores link diagnostics, backend failures, channel outcomes, and request-bound periodic-frame transport results. |
| `__init__.py` | Defines the supported public imports. |

The records are immutable and serialize deterministically. This makes a saved result
reconstructible without relying on mutable NumPy arrays or a process-wide serializer
registry.

## Fixed parameter study

The first study uses

$$
r\in\{3,4,8,16\},
\qquad
L\in\{1,2,4,8\},
$$

with construction-mesh sizes

$$
M\in\{513,1025,2049\}.
$$

The final construction mesh has $M=2049$ points. The explicit
`global_unitary_selection_mesh_size` is also $2049$. The shifted direct-evaluation mesh
has $8191$ points. The global-unitary alignment is selected once on the final
construction mesh and then reused on the other construction meshes and at
direct-evaluation points.

Frame transformations act on the retained space from the right. Reciprocal-endpoint
sewing acts on the ambient space from the left. Principal phases lie in $(-\pi,\pi]$.
The numerical-rank threshold is

$$
\tau_{\mathrm{rank}}
 = \max\!\left(10^{-12},10^{-10}\sigma_{\max}\right).
$$

Boolean values, numeric strings, nonfinite tolerances, alternative rank-cutoff rules,
and parameter inventories outside the frozen study are rejected.

## Transport results

`Periodic1DHigherRankAlignmentTransportOwnerResult.from_owner_outcome` converts a PhysKit
frame-transport result into immutable KSD data. It requires a one-dimensional,
unshifted `CenteredUniformMesh` and checks its size, retained rank, ambient dimension,
left/right actions, phase branch, tolerance, ordered link progression, and exact basis,
frame, and sewing identities against the immutable transport request.

A successful result contains:

- singular values and rank evidence for every required link;
- the principal phases of the endpoint mismatch;
- the right-unitary mapping from the primitive transported endpoint to the sewn initial
  frame;
- its reverse-direction adjoint; and
- the per-step right-unitary whose $M$-th power supplies periodic closure.

The final three quantities are stored as unitless complex matrices with descriptive field
names; see the [numerical formulation](numerics.md). A rank-deficient result stops at the
first deficient overlap and contains no closure matrices or Schur evidence.

## Work remaining

The present code is a transport and status layer, not yet a complete higher-rank
calculation. Later work must add the Hamiltonian producer, independent numerical
recalculation, complete result verification, scientific plotting data, and direct
calculation scripts. Those stages will use explicit calculation inputs and will not
reconstruct the historical Workflow implementation.
