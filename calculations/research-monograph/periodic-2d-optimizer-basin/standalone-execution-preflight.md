# Standalone optimizer-convergence execution preflight

## Status and authority

This is the exact preflight for the controlled synthetic non-DFT study selected
for the standalone publication path. The current human instruction, preserved in
`RM-PERIODIC-2D-STANDALONE-EXECUTION-HC09`, authorizes this exact bounded local
execution. It does not authorize DFT, remote execution, dependency changes,
publication, external transmission, release, or deletion of retained evidence.

## Immutable inputs

| Input | SHA-256 |
|---|---|
| `standalone-study-proposal.json` | `d260475252b420d151ebfd7e276e170c1d069e4bbc7ad974d21e911dd6db3485` |
| `standalone-initial-gauges.json` | `34ebdb57dbcdb3cb72bb3fbc602a12b3c05b58534d1c028047578afceb1a8f4b` |
| `execute_standalone_study.py` | `f13a2e583193a906c3f13ee5c17c05165db986a93065bd4b8f3c1688912a4184` |
| `execute_study.py` gauge transformation | `6bcd1b8a6bd5dfdc8038c9614115fd02d80a1c5ad460cad5597219a43d21c355` |
| `../periodic-2d/prepare_wannier90.py` | `93f9ab0853d9a17049ffa13c919452b124ca502ea32c0e3761467e0b94e7dbaa` |
| `../periodic-2d/composite-input.json` | `4abe583a5198537703f3a9e4937fd93c4c7cd6f46a3eefd302a551b1f0ae7e90` |
| local `wannier90.x` 3.1.0 | `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd` |

The output root is
`/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z`.
It must not exist before execution.

## System and computational scale

The input is the frozen synthetic rank-three periodic-2D parent. Fourteen unique
interfaces cover fixed auxiliary embedding, balanced embedding, and cutoff
axes. Sixteen deterministic starts are applied to every interface. Two declared
interfaces additionally repeat all starts with the preconditioner disabled.
Every successful but natively nonconverged initial trajectory is continued once
from its retained checkpoint.

The exact maximum is:

- 14 interface preparations;
- 224 baseline localizations;
- 32 preconditioner-control localizations;
- at most 256 conditional continuations; and
- at most 512 localization stages.

Execution is local and serial. Expected runtime is two to four hours, with a
hard total limit of eight hours. Each stage is limited to 600 seconds and one
GiB maximum resident memory. Each localization tree is limited to 8 MiB and the
complete external tree to 1.5 GiB. The 8 MiB bound is the exact immutable
proposal value; it was incorrectly described as 32 MiB in the initial verbal
preflight.

## Anticipated outputs

Every interface retains its exact generated input, Wannier90 interface files,
stage logs, resource timings, and checksums. Every localization retains its
seeded AMN file, active WIN file, native output, checkpoint, matrices, hopping
record, standard streams, and resource timing. Continuations occupy separate
directories and therefore do not overwrite initial trajectories.
`execution-result.json` is rewritten after every completed stage and records
all process, convergence, provenance, resource, and file-manifest fields.

## Restart semantics

Wannier90 3.1.0 documents `restart = wannierise` as restarting from the
beginning of the wannierisation routine using `seedname.chk`. Its source reads
that checkpoint before branching to `wann_main`, independently of whether its
stored checkpoint label is `postdis` or `postwann`. The driver copies the exact
initial checkpoint into a separate continuation directory, verifies the copied
SHA-256, sets `num_iter = 15000`, and retains the original trajectory unchanged.
A continuation is attempted only after process exit zero, native
nonconvergence, and the presence of a checkpoint.

The local documentation/source inspected for this contract is:

- `external/wannier90/doc/user_guide/parameters.tex`, `restart` subsection;
- `external/wannier90/src/parameters.F90`, restart parsing and checkpoint
  existence check; and
- `external/wannier90/src/wannier_prog.F90`, checkpoint reading and the
  `restart = wannierise` branch.

## Stop and retention rules

All outcomes are retained. There are no automatic retries, favorable-run
selection, silent parameter changes, or discarded failures. The driver stops
before localization if any interface cannot be prepared. During localization it
stops at the first stage or output bound exceedance, total runtime or storage
bound exceedance, or unexpected failure that requires scientific
interpretation. A process exit code of zero is recorded separately from native
Wannier90 convergence.

## Static gates

Before execution:

- the proposal verifier passes;
- the driver passes Ruff formatting and linting;
- the driver compiles;
- all immutable identities above agree; and
- the output root is absent.

These gates establish executable consistency only. They do not establish a
numerical result, optimizer convergence, scientific validation, material
relevance, or publication readiness.
