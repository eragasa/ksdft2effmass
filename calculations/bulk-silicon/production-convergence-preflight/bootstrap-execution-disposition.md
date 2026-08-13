# Bootstrap execution disposition

The committed preflight boundary is
`64de888ad54c1385941a0485433974342380094d`. The subsequent observation commit
`e9c6a1453a6a9dfac8c13256d7d146f6b6ec1716` retains the fact that the direct
bootstrap runner invoked `pw.x` 18 times: nine SCF calculations and nine linked
NSCF diagnostics. The development harness governed that direct bootstrap
execution. No additional execution is authorized.

> These direct executions are retained as bootstrap observations produced while
> developing the scientific harness. They are not a canonical scientific
> CampaignRun, do not establish deterministic scientific-harness execution, and
> do not constitute accepted production convergence evidence.

## Classification

| Question | Disposition |
|---|---|
| Execution fact | 18 direct `pw.x` invocations occurred |
| Mechanism | Direct bootstrap runner governed by the development harness |
| Evidence class | Bootstrap scientific-harness development evidence |
| Canonical scientific `CampaignRun` | Absent |
| Production scientific result | Not claimed |
| Numerical-verification acceptance | Not claimed |
| Scientific-validation acceptance | Not claimed |
| Canonical scientific-harness execution | Deferred |
| Additional scientific execution | Unauthorized |

The retained inputs, runner, identities, exit statuses, completion markers,
resource observations, warnings, raw-output references, and compact analysis may
serve as fixtures for QE input reconstruction, output parsing, execution-receipt
construction, artifact-manifest handling, convergence-analysis development, and
direct-versus-CPN comparison. They must not be rewritten to imply execution
through the future scientific harness.

Tracked inputs, the runner, and compact records are `bootstrap_fixture` and
`retained_for_architecture_testing`. Identity-addressed raw output may remain a
`bootstrap_fixture` retained for architecture testing. Native wavefunctions,
charge-density files, `.save` directories, and restart trees are
`reconstructible_scratch`; selected existing bytes may remain available for
architecture testing, but every native scratch artifact is not permanent
authority. No external artifact is deleted by this disposition.

[`execution-provenance.json`](execution-provenance.json) remains the compact
record of the exact invocations, identities, observations, warnings, and
external run-root descriptor. [`execution-preflight.json`](execution-preflight.json),
[`INPUTS.sha256`](INPUTS.sha256), [`run-primary.sh`](run-primary.sh), and
[`SHA256SUMS`](SHA256SUMS) preserve the prepared boundary and exact inputs.
