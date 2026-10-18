# Experiment implementation architecture

## Source mirror

Experiment architecture follows the source hierarchy recursively.

- `experiments/<path>/` maps to `docs/architecture/v2/experiments/<path>/`.
- Every selected package and subpackage receives the five-page bundle.
- Every selected source module receives a directory and the five-page bundle.
- Every selected public class receives a directory beneath its defining module and the five-page bundle.
- Architecture does not invent module or class placeholders before their contracts exist.

## Dependency direction

Experiment source is an outward composition layer.

- Installed KSD packages must not import experiment source.
- Experiments may compose supported installed KSD capabilities.
- Experiments may consume exact reviewed external-owner revisions.
- Serializers own wire mechanics rather than scientific behavior.
- Mutable task state is never imported into experiment results.

## Executable composition roots

Executable experiment scripts follow
[`experiments/script-conventions.md`](../../../../experiments/script-conventions.md).
They are import-safe outward composition roots with `main() -> int`, fail-closed process
status, paths derived from their own location, explicit lifecycle-specific destinations,
and no import-time execution. This common mechanical shape does not select a generic
experiment runner: every family retains its typed definitions, producer and verifier
routes, schemas, tolerances, statuses, and retention policy. Immutable retained-version
scripts remain frozen with their source manifests rather than being rewritten for style.

## State and schemas

Maintained definitions and results are operationally immutable and strictly correlated.

- Outcome-relevant controls are explicit or digest-bound.
- Strict decoders reject missing and unknown fields.
- Result evidence must agree with its summarized disposition.
- Schema changes that alter meaning create a new experiment version.
- Run and evidence-package identities remain separate from the version identity.

## Producer and verifier

Decisive verification follows a separate reconstruction route.

- Producers may use reviewed numerical-owner kernels.
- Verifiers do not call producer actions.
- Verifiers do not treat serialized labels as oracles.
- Shared libraries and arithmetic assumptions are disclosed.
- Adversarial mutations must fail closed.

## Retention gate

Implementation alone does not create immutable evidence.

- Freeze the scientific protocol.
- Pin dependency and adapter identities.
- Complete strict schemas and independent verification.
- Complete direct tests and evidence policy.
- Assign `.vN` only after review closes.
- Retain a run only under separately authorized execution and retention policy.
