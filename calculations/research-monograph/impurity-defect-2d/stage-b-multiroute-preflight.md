# Adopted multi-route Stage B implementation preflight

## Authority

The human response ``recommendation authorized`` resolved
`RM-IMPURITY-DEFECT-2D-STAGE-B-TWIST-GAUGE-HC04` by adopting the multi-route,
data-complete design for execution-free implementation. The runner, independent
verifier, closed retained-result schema, deterministic SVG plotter, and authored
toy tests are implemented. This authority does not read or execute the accepted
scalar parent and does not create a calculated Stage B result. Accepted-parent
execution still requires a later exact checkpoint and authorization record.

## Frozen implementation inventory

| Item | Bound |
|---|---:|
| Matrix routes | 2 |
| Gauge bridges | 1 deterministic relation |
| Execution schedules | 2: A-then-B and B-then-A |
| Known-map evaluations | 72 |
| Matched bridge records | 36 |
| Blind candidate evaluations | 2,304 |
| Maximum matrix dimension | 64 |
| Runtime planning bound | 600 seconds |
| Peak-memory planning bound | 2 GiB |
| Retained-output planning bound | 30 MiB |
| Network, remote, or external scientific executable | none |

The inventory bounds are implemented but remain planning bounds for any future
accepted-parent execution, not execution authority.

## Implemented gates

1. The human decision adopted the multi-route option while preserving the
   superseded single-route design as negative evidence.
2. Route A, Route B, the bridge, and the two schedule identities are frozen
   separately.
3. Route B cannot consume a Route A matrix, and Route A cannot consume a Route B
   matrix.
4. A-then-B and B-then-A run in separate fresh processes with identical immutable
   inputs and no shared caches or outputs.
5. Serialization order is fixed independently of execution order.
6. Lift, reduced twist, integer difference, $D$, $U_M$, $W_M$, and attacked
   bridge orientations are explicit.
7. Cross-route and cross-schedule checks compare complete ambiguity identities,
   not only counts.
8. A disconnected phase graph stops before candidate ranking.
9. Every retained route-local failure, bridge failure, and schedule disagreement
   remains separate from independent-reconstruction status.
10. Authored toy benchmarking reassesses the expanded resource envelope.

## Required adversarial behavioral evidence

- exact clean equivalence under both schedules;
- a shared-twist-cache mutation that produces a detectable schedule effect;
- $D$ versus $D^\dagger$ and $U_M$ versus $W_M$ mutations;
- independent direct construction versus a tautological transformed-route
  mutation;
- raw-lift, reduced-metadata, and integer-lift mutations;
- source-versus-target attack phases;
- complete ambiguity identity mutation with unchanged counts;
- disconnected phase graph;
- route-local failure reproduced by the verifier;
- both routes internally self-consistent but bridge-invalid;
- canonical serialization invariant to schedule;
- stale authority, traversal, overwrite, wrong-stage, and resource-bound
  refusals.

## Demonstrated toy discrimination and envelope

For authored unit nearest-neighbour hopping on the frozen $8\times8$ geometry,
the clean two-route bridge residual was $8.88\times10^{-16}$ and route-local
A-then-B versus B-then-A differences were zero. Under the deliberately invalid
shared-twist-cache mutation, the Route A schedule difference and B-then-A bridge
mismatch were approximately $0.7654$; the periodic seam route changed by
$2.78\times10^{-17}$. The complete toy retained all 2,304 candidates, occupied
3,090,150 bytes, and ran in 1.66 seconds with 56,229,888 bytes maximum resident
set size on the development machine. The SVG occupied 63,729 bytes. The
independent verifier reported both reconstruction and criteria PASS with maximum
reconstructed difference $6.84\times10^{-14}$. These are synthetic test data and
software-verification measurements, not accepted-parent evidence.

## Stops

The HC05 attempt stopped before accepted-input access because its CLI arguments
violated the repository-relative representation contract. Do not retry unless
HC06's corrected-path retry stopped during parent-schema parsing before matrix
construction; that exact failure is retained. Do not execute the corrected
parser unless pending checkpoint
HC07 was resolved to its one-attempt option and the matching bound execution
completed. Do not rerun or perform another attempt. Do not interpret an order effect
as physical; retain it as a software or protocol failure. Do not select the
favorable route or schedule. The implementation refuses stale source identities,
path escape, a wrong checkpoint decision, resource expansion, and overwrite.
