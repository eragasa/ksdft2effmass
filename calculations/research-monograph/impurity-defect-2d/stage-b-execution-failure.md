# Stage B first authorized execution attempt: retained invocation failure

## Status

The one execution authorized by
`RM-IMPURITY-DEFECT-2D-STAGE-B-EXECUTION-HC05` was attempted once and failed
before the design, accepted scalar parent, accepted Stage A result, or output
could be read or created. No calculated Stage B result exists.

## Exact failure

The shell ran the Stage B script from `python/` but supplied
`../calculations/...` for arguments whose contract is canonical
repository-relative representation. The runner correctly resolved those
arguments against the authorized repository root rather than the shell working
directory. The represented design path therefore became
`/Users/eugene/repos/calculations/...`, which does not exist, and the runner
stopped with:

```text
FileNotFoundError: [Errno 2] No such file or directory: '/Users/eugene/repos/calculations'
```

This is an invocation/protocol failure, not a numerical criterion failure,
route disagreement, gauge effect, accepted-parent result, or verifier result.
The fail-closed path behavior worked as designed.

## Retained evidence

- execution log: `stage-b-execution.log`
- log SHA-256: `8f6466c616da06402623b19933fe9cec1e0fdef544b899d6ad36d76458478c91`
- consumed authorization: `stage-b-execution-authorization.json`
- authorization SHA-256: `83beb8ccbc31be3f7c49f34f3000fac3bd4818087d0299cdea62e33c3558dc6a`
- exit status: `1`
- elapsed time: `0.14 s`
- maximum resident set size: `41,910,272 bytes`
- `stage-b-result.json`: absent
- accepted parent read: no
- accepted Stage A result read: no
- network access: none
- retry performed: no

## Corrected invocation boundary

A corrected invocation would keep the same design, authorization identities,
accepted inputs, output, schedules, and resource bounds, but pass repository-
relative argument strings such as
`calculations/research-monograph/impurity-defect-2d/stage-b-multiroute-design.json`
rather than shell-working-directory-relative strings beginning with `../`.
Because HC05 authorized one execution with no retry, that deterministic command
correction does not itself authorize another attempt. A separate human retry
decision is required.

## Corrected retry outcome

HC06 authorized one corrected retry. The command used canonical
repository-relative represented paths and passed every authority, digest,
checkpoint, output, and resource check. It then stopped while parsing the
accepted parent because the runner incorrectly expected `lambda_x` and
`lambda_y` inside each `coupling_continuation` result entry. Those values are
owned by `input.json` under `isotropic_potential`; each result entry stores only
its varied `lambda_xy` value. The exact stop was:

```text
KeyError: 'lambda_x'
```

The accepted parent input and result were read for identity and schema parsing,
but retained hopping construction, matrix construction, route evaluation, and
result serialization did not begin. The accepted Stage A file was identity-
checked but not parsed. No result was created and no further retry was made.

- corrected-retry log: `stage-b-retry-execution.log`
- corrected-retry log SHA-256: `2c6c7f19884a00ed567172cb2d6694632c53ba6022ea8316673916a1650c21b7`
- corrected-retry authorization: `stage-b-retry-execution-authorization.json`
- authorization SHA-256: `fe9a989fa35fdc3accea62cd41ecefc2a3780a40ab916b1bd6782ca77674091e`
- exit status: `1`
- elapsed time: `0.23 s`
- maximum resident set size: `42,663,936 bytes`
- `stage-b-result.json`: absent
- matrices constructed: no
- route schedules started: no
- further retry performed: no

The execution-free parser has since been corrected to read `lambda_x` and
`lambda_y` from the bound parent input and `lambda_xy` from the selected result
entry. A bounded read-only parser check retained 61 hoppings through squared
radius 18. This correction changes no scientific setting, but another protected
execution still requires separate human authority because HC06 prohibited any
further retry.

## Claim boundary

These retained failures establish fail-closed path and parent-schema handling
and the absence of a Stage B result. They establish no accepted-parent numerical
verification, scientific validation, uncertainty quantification, publication,
release, deposit, or authority for Stages C--E.
