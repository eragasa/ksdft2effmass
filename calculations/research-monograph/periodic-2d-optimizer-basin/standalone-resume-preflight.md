# Standalone continuation-resume preflight

## Retained stop

The exact standalone study completed all 14 interface preparations and all 256
initial localizations, then stopped after five of 120 required continuations.
The stop was triggered by the immutable proposal's 8 MiB per-localization output
limit, not by process failure: the fifth continuation occupied 10,389,823 bytes,
ran for 23.58 seconds, used 26,886,144 bytes maximum resident memory, and exited
zero. The retained execution used 3,297.986 seconds and 953,563,433 bytes.

The earlier prose preflight incorrectly described the immutable 8 MiB limit as
32 MiB. The executor correctly read and enforced 8 MiB from the proposal. This
reporting error does not alter the retained proposal, execution record, or stop.

## Resume authority and exact scope

`RM-PERIODIC-2D-STANDALONE-CONTINUATION-RESUME-HC10` authorizes only the
remaining 115 continuations. It authorizes no interface or initial-localization
rerun and no retry of the five completed continuations.

The resume driver is `resume_standalone_continuations.py`, SHA-256
`5780a21cc4aeaf72cbc638b0cad98190709a23e636125c535b30df0fe8994803`.
It reads the retained `execution-result.json`, verifies all 256 initial processes,
reconstructs the exact pending set from native convergence status and completed
continuation identities, and requires exactly 115 pending records.

Before mutation it copies the retained execution record to
`execution-result-before-resume.json` and records that snapshot's SHA-256. It
then appends continuation records to the existing external evidence tree.

## Revised limits and progress

- 600 seconds per continuation stage;
- 1 GiB maximum resident memory per stage;
- 32 MiB output per continuation;
- 3 GiB complete external-tree size; and
- the original eight-hour cumulative execution bound.

The driver prints and flushes a line before and after every continuation. The
lines contain the continuation index, configuration, optimizer arm, start,
cumulative or stage runtime, exit status, native convergence status, continuation
bytes, and total tree bytes. A final line records completion or the exact stop.

Every outcome remains retained. Process completion and native convergence remain
separate. No favorable selection, automatic retry, scientific-parameter change,
remote execution, publication, release, or external transmission is authorized.
