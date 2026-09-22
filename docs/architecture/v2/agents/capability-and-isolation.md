# Agent capability and isolation boundary

## Layered enforcement

The governed operator uses three distinct layers:

| Layer | Enforces |
|---|---|
| Pi tool selection | Which typed operations the model may request |
| Domain ActionObjects and authority | Which requested state transitions are valid and authorized |
| Process and filesystem isolation | What the Pi process, adapter, subprocesses, and candidate code can physically access |

No layer is described as providing another layer's guarantee.

## Operator profile

A restricted operator starts from an explicit closed profile that disables
extension discovery, loads only the identified approved adapter, and exposes
only required read-only inspection tools plus the named deterministic actions.
General `bash`, `edit`, and `write` tools are absent. Dynamic tool registration,
runtime action discovery, and operator-triggered extension reload are prohibited.

Built-in read tools are not repository-confined merely because they are
read-only. The operator either uses root-confined inspection tools or runs under
filesystem policy that prevents reads outside the permitted roots. The profile
identity, active tool identities, adapter content identity, model identity, and
session root are recorded as runtime provenance but grant no Harness authority.

The exact command-line spelling and launcher mechanism remain deferred. This
architecture selects a profile contract, not a new public launcher abstraction.

## Adapter trust boundary

Pi extensions run with the Pi process's operating-system permissions. The
approved extension is therefore trusted executable code, not a sandbox. It must
be read-only to the operator, content-identified, narrowly implemented, and
loaded without ambient project extension discovery.

The adapter must not:

- own state-transition, validation, authorization, or scientific policy;
- resolve a mutable interpreter or action implementation through ambient
  `PATH`, current-directory imports, or a candidate-controlled environment;
- pass unrestricted environment variables or credentials to subprocesses;
- accept arbitrary command, module, path, or payload selection;
- treat unvalidated stdout as an ActionResult; or
- permit a running operator to change its action composition.

Cancellation, timeout, process-tree termination, output bounds, environment
sanitization, exact executable/runtime identity, and closed JSON response
validation are required implementation contracts before operation.

## Process isolation

Where protection must extend beyond accidental model bypass, run the operator
and candidate validators in an OS sandbox, container, or separate service
identity. The selected boundary should provide, as applicable:

- read-only control-plane and adapter code;
- writable access only to declared candidate or operation roots;
- authoritative state reachable only through its owning service/repository;
- no credentials except those explicitly required by the operation;
- network denial by default;
- process, time, memory, and output limits; and
- independent logs or receipts bound to exact operation identities.

A project-controlled sandbox configuration is itself trusted policy and cannot
be writable by the governed operator.

## Constrained source modification

A source-writing operator never patches the active control plane in place. The
operation begins from an exact base revision, applies a bounded patch in an
isolated candidate workspace, verifies root confinement and file-type policy,
identifies the complete candidate, and validates that exact candidate under a
bounded execution profile. Publication or integration is a separate authorized
operation consuming the same candidate identity.

Path checks include canonical root resolution, exact case where applicable,
Unicode policy, traversal rejection, symlink and hard-link policy, file-type
replacement, mount and destination policy, concurrent ownership, and detection
of source changes during the operation. Deny lists alone are insufficient.

Candidate tests and validators are untrusted executable code. Their successful
exit neither authorizes promotion nor proves that they lacked side effects; they
run inside the candidate-validation sandbox.

## Claim boundary

A tool-surface test establishes only that forbidden Pi tools were not exposed in
the tested profile. Action tests establish only their specified transition
contracts. Sandbox tests establish only the tested isolation policy on the
identified platform. None establishes scientific correctness, human acceptance,
or universal security against actors outside the declared threat model.
