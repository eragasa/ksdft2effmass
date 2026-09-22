# Bootstrap execution disposition

The committed preflight boundary is
`64de888ad54c1385941a0485433974342380094d`. The subsequent observation commit
`e9c6a1453a6a9dfac8c13256d7d146f6b6ec1716` retains the fact that the direct
bootstrap runner invoked `pw.x` 18 times: nine SCF calculations and nine linked
NSCF diagnostics. The development harness governed that direct bootstrap
execution. No additional execution is authorized.

> These direct executions predate the deterministic scientific Campaign
> architecture and are not a canonical scientific CampaignRun or
> `ScientificWorkflowRun`. Their audited outputs are nevertheless usable as
> provisional calculated and finite-setting numerical-verification evidence. They
> do not constitute accepted production convergence, an infinite-basis result,
> scientific validation, or uncertainty quantification.

The human approved the direct-results-first strategy with the verbatim response
`yes`. Re-execution solely to reproduce these observations through the scientific
harness is not a prerequisite for auditing or human disposition of the retained
direct results. No additional execution is authorized.

## Classification

| Question | Disposition |
|---|---|
| Execution fact | 18 direct `pw.x` invocations occurred |
| Mechanism | Direct bootstrap runner governed by the development harness |
| Evidence class | Provisional calculated and finite-setting numerical-verification evidence from direct bootstrap execution |
| Canonical scientific `CampaignRun` / `ScientificWorkflowRun` | Absent; not retrospectively fabricated |
| Production scientific result | Not claimed |
| Numerical-verification acceptance | Awaiting human disposition; not accepted by this record |
| Scientific-validation acceptance | Not claimed |
| Canonical scientific-harness execution | Later reproducibility/comparison work, not a prerequisite for using retained direct results |
| Additional scientific execution | Unauthorized |

The retained inputs, runner, identities, exit statuses, completion markers,
resource observations, warnings, raw-output references, and compact analysis may
serve as provisional direct finite-setting evidence as well as fixtures for QE
input reconstruction, output parsing, execution-receipt construction,
artifact-manifest handling, convergence-analysis development, and
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
external run-root descriptor. [`direct-results-audit.md`](direct-results-audit.md)
records the read-only external-output integrity audit, independent extraction,
criteria disposition, and missing-evidence boundary. [`execution-preflight.json`](execution-preflight.json),
[`INPUTS.sha256`](INPUTS.sha256), [`run-primary.sh`](run-primary.sh), and
[`SHA256SUMS`](SHA256SUMS) preserve the prepared boundary and exact inputs.
