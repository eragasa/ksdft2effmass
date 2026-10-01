# IEEE Warning Read-Only Diagnosis

**Status:** Read-only diagnostic result; origin not localized. The recurring report
remains unclassified. This record does not establish harmlessness, numerical
correctness, scientific validation, or authority for another executable invocation.

## Authorization and scope

The human response `authorize bounded read-only IEEE diagnosis` authorized inspection
of the retained stdout, time/stderr receipts, and compact provenance only. No Quantum
ESPRESSO invocation, executable probe, source/build inspection, input mutation,
successor activation, or external computation was performed.

The inspected execution remains the direct bootstrap campaign identified by:

- run-root descriptor:
  `ksdft2effmass-runs/bulk-silicon-production-convergence-20260813T021128Z`;
- run-root SHA-256 identity:
  `9d84848b4abb0db89e70fa8f6af2dc5f94b122d9574397e60398986638b91bb5`;
- executable SHA-256 identity:
  `6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca`;
- compact provenance SHA-256:
  `169d5eed6e975bc7248f87194f8a8e130d3a7a8e79a31334f7a5566de97efa5a`.

## Method

For the 18 invocation stdout files and 18 corresponding time/stderr receipts, the
diagnosis:

1. recomputed byte counts and SHA-256 identities against
   `execution-provenance.json`;
2. counted the exact IEEE report in every time/stderr receipt;
3. checked its location relative to the `/usr/bin/time -l` accounting block;
4. checked every stdout for `JOB DONE.` and explicit error, backtrace, signal,
   `NaN`, or infinity markers; and
5. compared occurrence across the nine SCFs and nine linked diagnostic NSCFs.

This method reads only retained text artifacts. It cannot identify an internal
floating-point operation or reconstruct compiler/runtime behavior.

## Observations

| Check | Retained observation |
|---|---|
| Invocation artifacts checked | 36: 18 stdout and 18 time/stderr receipts |
| Identity mismatches | 0 |
| SCF receipts carrying the exact report | 9 of 9 |
| NSCF receipts carrying the exact report | 9 of 9 |
| Exact report count per receipt | 1 |
| Report position | First nonempty stderr line in every receipt, before the `/usr/bin/time -l` accounting lines |
| Other stderr diagnostic text | None; remaining nonempty lines are time/resource accounting |
| `JOB DONE.` count | Exactly 1 in every stdout |
| Explicit stdout error/backtrace/signal markers | None for the checked markers |
| Printed `NaN` or infinity markers | None |
| Exact report in stdout | None |

The exact recurring text is:

```text
Note: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG IEEE_DIVIDE_BY_ZERO IEEE_OVERFLOW_FLAG IEEE_UNDERFLOW_FLAG
```

## Interpretation

The placement and uniformity are **consistent with** a process-termination summary of
accumulated floating-point status flags rather than a trapped exception at a retained
call site. The report is invariant across cutoff, mesh, SCF, and NSCF cases, which
provides no evidence that it is specific to one tested setting or one calculation
mode. The completed finite outputs and absence of explicit fatal markers show no
overt failure in the retained text records.

Those observations do **not** identify which operation first raised any flag, whether
the flags were later cleared, which compiler/runtime component emitted the summary,
or whether an affected intermediate quantity influenced a retained observable. Zero
exit, `JOB DONE.`, finite printed values, and stable finite-setting comparisons cannot
establish harmlessness.

## Disposition and next boundary

The bounded diagnosis is therefore **inconclusive: origin not localized**. The
selected `block_pending_diagnosis` disposition remains in force. The convergence
disposition, lattice-reference activation, production SCF, and further protected
scientific execution remain blocked.

The lowest-risk next diagnostic step would be a separately authorized read-only
inspection of the exact QE build provenance, compiler/runtime configuration, and link
metadata. If that cannot localize the report, any instrumented or trapping QE probe
would be a new protected execution requiring an exact input, executable, resource,
and output authorization before invocation.
