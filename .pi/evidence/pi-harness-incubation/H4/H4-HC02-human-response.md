# H4-HC02 human response

A — authorize one bounded H4 correction.

Correct only:

1. the H3 route gate so that `route=local` is accepted when evaluating the
   human-authorized H4 local cutover, while preserving rejection of unknown,
   malformed, or unauthorized routes;

2. the operational consumer so its overall result is failure whenever any
   required selected-validator observation fails, regardless of whether the
   replay subprocess itself exits successfully.

Keep these states distinct:

- replay process completed;
- observation parsed;
- selected validator passed;
- aggregate consumer passed.

A successful process exit must not override a failed nested observation.

Add focused tests proving:

- authorized `local` routing passes H3 route validation;
- malformed and unsupported routes fail;
- a successful replay process containing a failed H3 observation causes the
  operational consumer to fail;
- all required passing observations produce consumer PASS;
- legacy routing behavior remains valid;
- rollback still restores legacy routing.

Keep the maintained primary route set to `legacy` throughout correction and
preflight. Do not switch it to `local` until R3/E3, focused validation, H4
completion, and targeted confirmation all pass.

Because these changes affect replay inputs:

1. create exactly one replacement replay-input revision R3;
2. execute one isolated replay of R3;
3. create evidence revision E3 referencing R3 without requiring E3 = R3;
4. run focused tests, Ruff, mypy, H3 validation, operational-consumer checks,
   rollback proof, and H4 completion;
5. request one targeted integration confirmation covering only the two corrected
   defects and cutover safety;
6. if all pass, perform the already authorized controlled route change from
   `legacy` to `local`, rerun the live consumer and rollback proof, close H4,
   commit, push, and stop.

Do not create R4/E4 or start another broad review cycle. If R3/E3 exposes another
material defect, retain legacy authority, stop, and report the exact blocker.

Do not activate P2, H5, scientific/external execution, publication, or release
work unless H4 is successfully closed and P2 is subsequently activated under
separate explicit authority.
