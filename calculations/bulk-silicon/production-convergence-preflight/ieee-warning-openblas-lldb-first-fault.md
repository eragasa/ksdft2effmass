# IEEE Warning OpenBLAS LLDB First-Fault Attempt

**Status:** The one authorized debugger-controlled launch attempt failed at the local
LLDB attach boundary. LLDB retained no floating-point registers or first-fault
backtrace, and the target retained no stdout or stderr. The authorization is consumed;
no retry occurred. This is failed diagnostic-execution evidence, not a completed SCF
calculation, calculated physical result, numerical verification, scientific
validation, or harmlessness determination.

## Authorization and exact attempt

Human response `recommendation authorized` unambiguously selected
`authorize_one_debugger_controlled_openblas_c48_classification` in
`.pi/checkpoints/bulk-silicon-convergence-ieee-first-fault-classification.json`.
The attempt reauthenticated and reused:

- OpenBLAS-linked diagnostic `pw.x` SHA-256:
  `4fe641535285a9bde81bb0b55862ccfd8bd072d354a57585ff6ded545cc13565`;
- C48 input SHA-256:
  `cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17`;
- Si pseudopotential SHA-256:
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`;
  and
- OpenBLAS 0.3.33 SHA-256:
  `dbd757cdfffbff1dc72fbf34983e89d5710933d04783f950441a57522fbf769d`.

The executable retained OpenBLAS linkage and no Apple Accelerate linkage. The local
debugger was `/Library/Developer/CommandLineTools/usr/bin/lldb`, version
`lldb-1700.0.9.502`. The staged run root is
`~/projects/ksdft2effmass-runs/bulk-silicon-ieee-openblas-lldb-20260921T002933Z`.

LLDB accepted the requested target environment
`HWLOC_COMPONENTS=-opencl`, `OMP_NUM_THREADS=1` and the policy to stop and not pass
`SIGILL`. It then attempted exactly one target launch with the exact C48 input and
separate target stdout and stderr files.

## Failure result

LLDB reported:

```text
error: process exited with status -1
(attach failed (attached to process, but could not pause execution; attach failed))
```

Observed state:

- debugger target-launch attempts: one;
- retry or debugger continuation: none;
- target execution status: indeterminate because LLDB could not complete attach;
- target stdout: zero bytes;
- target stderr: zero bytes;
- scratch regular files: zero;
- macOS `pw.x` crash report: absent;
- trapped instruction, FPCR, FPSR, and floating-point operands: not captured;
- LLDB-reported wall time: 234.60 seconds;
- maximum resident set size: 542,064,640 bytes; and
- peak memory footprint: 535,037,176 bytes.

The requested 120-second wall-time and 500 MB observed-memory envelopes were not
effectively enforced. The supervising tool timed out before it could retain the
wrapper return code, while the orphaned LLDB process remained in its attach attempt
and later exited with the error above. Its measured wall time and memory therefore
exceeded both envelopes. No LLDB or target process remained afterward. This control
failure is retained explicitly and is not treated as scientific-executable success.

## Interpretation and claim boundary

The failed attach provides no new evidence about the IEEE class, source operands,
underflow origin, MPI influence, or observable impact. It neither confirms nor refutes
the prior localization of enabled floating-point divisions below `ZHEGVX` in Apple
Accelerate and OpenBLAS. The preceding comparator conclusions and convergence block
remain unchanged.

The authorization stated that a debugger launch or permission failure consumed the
single attempt. No retry, debugger continuation, rebuild, non-MPI comparator,
class-separated run, warning suppression, setting promotion, successor activation,
network access, or remote, cluster, or cloud use followed.

A true `QE_ENABLE_MPI=OFF` OpenBLAS comparator would avoid Open MPI, PMIx, and hwloc
entirely while retaining the same C48 input and trap set. That would test MPI/runtime
influence but would not by itself identify the exact IEEE class or establish ordinary
non-trapping observable impact. It requires a separate protected-execution decision.

## Retained identities

The external `manifest.json` has SHA-256
`2f7ab93b0b44d196013a7c5ceafb5c38cea5a0a5c57e9ca2b4cb261fc775ab76`.
Principal retained artifacts are:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `output/lldb-session.out` | `ed89fa6680d5ea9b29139edbae0967194e220e182c52afa5ec68c14de7a552dc` | 843 |
| `output/lldb-session.err` | `eb76af59b326eb2cd7f9a6fe0b45ecc316b82d64580eb9a58a4e2408ec9d9696` | 898 |
| `output/process-result.json` | `48d74199d821cfabfdde071c0b7fa744026af5202c45510ce40cd8c7f3d60bb1` | 811 |
| `output/C48.scf.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `output/C48.scf.err` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `output/executable-linkage.txt` | `b11de131d78c74824525e09f4cb09a94383db04e5cc92300d55a75baea2028b5` | 1,053 |
| `output/preflight-identities.txt` | `470469699c855526753b914c35bc1f5efb0d4e346cb6a8911b64c94ae227154e` | 620 |
