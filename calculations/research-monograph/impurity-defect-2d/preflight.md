# Defect-2D design preflight

## Current authorization

The active task retains the consumed Stage A execution authority and its
human-accepted result. The durable checkpoint
`RM-IMPURITY-DEFECT-2D-STAGE-A-EXECUTION-HC01` and machine-readable
`stage-a-execution-authorization.json` bind that historical exact design,
runner, scalar parent, repository root, output path, resource envelope, and
verbatim response. The accepted design remains non-authorizing by itself.

That execution authority was consumed by `stage-a-result.json`. Checkpoint
`RM-IMPURITY-DEFECT-2D-STAGE-A-ACCEPTANCE-HC02` human-accepts the exact retained
Stage A evidence and authorizes managed closeout only. It does not authorize a
rerun, Stages B--E, rerunning frozen prerequisites, changed tolerances, DFT,
Wannier90, material transfer, remote execution, publication, release, deposit,
or external transmission. The human response ``continue``, recorded by
`RM-IMPURITY-DEFECT-2D-STAGE-B-IMPLEMENTATION-HC03`, separately authorized
execution-free Stage B implementation but not calculation execution. The later
human response ``recommendation authorized`` resolved
`RM-IMPURITY-DEFECT-2D-STAGE-B-TWIST-GAUGE-HC04` by adopting the multi-route,
data-complete execution-free design. Its implementation and authored toy tests
are complete. HC05 authorized one attempt, but repository-relative arguments
were incorrectly spelled relative to the shell working directory; the runner
stopped before reading the design or accepted inputs and created no result.
HC06 authorized the corrected-path retry, which passed authority checks but
stopped during parent-schema parsing before hopping or matrix construction. The
parser is corrected and bounded read-only parent checks pass.
HC07 authorized one schema-corrected attempt. It completed once, retained the
full frozen inventory, and passed runner criteria and independent reconstruction.
HC08 human-accepts the exact Stage B evidence and authorizes managed closeout
only. No rerun or further attempt is authorized.

## Frozen future execution envelope

| Item | Proposed value |
|---|---|
| Executable | local Python through the repository's existing `uv` environment |
| External scientific executable | none |
| Input system | accepted synthetic periodic-2D scalar/composite parents and the exact plants in `study-design.json` |
| Largest represented matrix in Stage A | $64\times64$ complex Hermitian |
| Stage-A peak memory limit | 2 GiB |
| Stage-A runtime limit | 120 seconds |
| Network or remote execution | none |
| Anticipated Stage-A outputs | canonical JSON result, independent verification log, report, and checksum catalog; no figure is required for the null-and-folding stage |

These are authorization bounds, not measured resource results. The Stage A
source passes Ruff formatting/lint, strict mypy, bytecode compilation,
CLI-help checks, the retained execution-free software-contract tests, and the
Python test-evidence conformance gate. The behavioral tests use authored toy
coefficients rather than the accepted periodic-2D parent.

## Preconditions for the authorized run

1. The resolved checkpoint and machine-readable authorization retain the exact
   current human response and all bound identities.
2. Parent paths and SHA-256 identities match `study-design.json`.
3. The Stage A runner and independent verifier are both present and their shared
   surface is limited to serialized input/output formats.
4. A dry inspection confirms that the verifier does not import the runner and
   reconstructs supercells through Kronecker seam matrices rather than the
   runner's site-and-hop enumeration.
5. `stage-a-result.json` does not exist and cannot be overwritten.
6. The authorization names the exact stage, executable, input, expected scale,
   output, repository root, and resource envelope.
7. No DFT, Wannier90, network, remote, material, or spin-space work is included.

## Stage gates

### Stage A — null and folding

Authorized one-run scope: parent identity checks, scalar folding, seam phases,
null extraction, and incompatible-representation structured stops.

Stage A completed within the bound, independent verification reproduced all
metrics and adverse controls, all frozen numerical criteria passed, and the
human accepted that exact evidence boundary. This does not activate or
authorize Stage B. A
numerical failure would have been retained and reviewed rather than silently
repaired by changing tolerances.

### Stage B — scalar onsite and symmetry

The superseded single-route design is retained in `stage-b-design.json`,
`stage-b-protocol.md`, and `stage-b-preflight.md` as historical negative
evidence. Execution-free implementation showed that its generic twist,
componentwise $[0,1)$ reduction, and bare-permutation full-Hamiltonian covariance
do not define a consistent finite-matrix gauge. The adopted replacement in the
`stage-b-multiroute-*` records freezes two independent matrix routes, one gauge
bridge, two fresh-process schedules, complete blind-candidate retention, and
independent reconstruction. The accepted-parent Stage B calculation subsequently
completed with the full retained inventory, independent verification passed, and
HC08 human-accepted that exact bounded evidence. No Stage B rerun is authorized.

Gate to Stage C: Stage B retains all maps, ambiguities, covariance defects,
adverse controls, and independent reconstruction. Blind alignment ties stop
instead of being broken by access to the plant. HC09 separately authorized only
the execution-free Stage C design and implementation.

### Stage C — directional and nonlocal classes

The execution-free package now fixes authored directional nearest-neighbor and
diagonal nonlocal plants, five nested model classes, two independently
constructed gauge routes, separate spawned schedule processes, isotropic-parent
oriented $D_4$ covariance, locality shells, and four adverse controls. The
independent verifier reconstructs all toy matrices and analytical fit residuals
without importing the runner. HC10 human-accepts this exact execution-free
package and authorizes managed closeout only. HC11 subsequently authorized
accepted-parent Stage C design only. The proposed design now freezes the
accepted isotropic and anisotropic parent identities, $D_4$, $D_2$, axis-swap,
model-class, locality, route, schedule, adverse-control, verification, retention,
and resource contracts. Its adversarial review reports no blocking finding after
corrections. HC12 human-adopts this exact design as the authoritative proposed
contract. HC13 authorized the completed execution-free implementation with
authored fixtures, and HC14 human-accepts that exact implementation boundary and
authorizes managed administrative closeout only. HC15 authorizes the separately
closed execution-free accepted-artifact adapter, authority/provenance contracts,
verifier extension, maintained tests, and adversarial review. HC16 binds the
external native simulation root `/Users/eugene/projects/ksdft2effmass` while
compact version-controlled records remain under repository `calculations/**`;
it does not authorize root population. The corrected dormant Workflow consumes
an append-only attempt before parent hashing, exclusively produces the complete
seven-artifact package, and refuses retry after STARTED, FAILURE, or SUCCESS.
Runtime and peak memory remain post-computation checks rather than proactive hard
sandbox limits. No accepted-parent Stage C read or calculation is authorized.
HC17 is reserved for any later exact protected run.

Gate to Stage D: a separately authorized Stage C calculation must retain
model-class residuals and failures without class or tolerance changes. Passing
authored-toy tests does not satisfy that gate or activate Stage D.

### Stage D — area, shape, and boundary phase

Future scope: square area sequence, fixed-area rectangles, orientation pairs,
and the exact $9\times9$ twist mesh.

Gate to Stage E: area, shape, orientation, and twist effects reported as separate
error channels; no pooled convergence claim.

### Stage E — composite and degeneracy

Future scope: the rank-three parent, composite onsite plant, orbital-frame
attack, blind polar alignment, and projector/principal-angle diagnostics.

Completion boundary: software and numerical-verification evidence only. Human
acceptance, material transfer, and any publication-facing claim remain separate.

## Stop conditions before invocation

Do not run if any bound hash or canonical path changed, the checkpoint and
machine record disagree, a tolerance is undecided, a behavioral gate fails,
the verifier shares numerical implementation with the runner, the output path
exists, or the authority is broader than Stage A. Report the exact mismatch
instead. A numerical criterion failure after valid invocation is retained as a
negative result and remains separate from independent reconstruction failure.
