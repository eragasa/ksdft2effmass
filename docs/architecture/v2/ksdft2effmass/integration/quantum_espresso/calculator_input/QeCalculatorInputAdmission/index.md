# `QeCalculatorInputAdmission`

## Responsibility

`QeCalculatorInputAdmission` is the effect-free KSD admission boundary for one exact
Project Koios Simulations `CalculatorInputRecord`. Its constructor requires a
`QeCalculatorInputAdmissionPolicyIdentity`. The resulting binding retains that exact
policy identity, the provider record instance, and the existing KSD `QeExecutionInput`
Workflow and predecessor correlations. Each exact provider external-requirement
instance is retained through `QeExternalInputResourceBinding` with only its KSD
artifact identity and deployment destination added for correlation.

The action does **not** create an input wire or owner-local JSON codec, copy provider
bytes or metadata into a second input model, access the filesystem, render input,
stage artifacts, invoke a process, or grant execution authority. If persistence is
later required, the common Workflow serializer owns the reviewed representation.
There is no zero-argument admission action and no hidden default policy.

## Admission checks

The implemented schema-1 `pw.x` slice requires:

- provider integration identity `quantum-espresso`;
- representation `quantum-espresso-pw-input`;
- a `projectkoios.qe.pw.*` preparation operation;
- exactly one `primary-input` artifact;
- only `pseudopotential` external requirements;
- exact native-input and pseudopotential filename, byte-count, and SHA-256 agreement;
  and
- every KSD predecessor manifest-entry correlation to name an entry in its admitted
  immutable tree.

Agreement returns `QeCalculatorInputBinding`. Its external-resource bindings retain
the provider requirement instances by identity rather than copying their metadata.
Unsupported contracts and correlation mismatches return
`QeCalculatorInputAdmissionFailure` with a closed
`QeCalculatorInputAdmissionFailureCode`.

## Reachability and claim boundary

The public admission action and binding are implemented and software-tested.
`LocalQeExecutionPlan` retains the provider record and explicit policy identity.
`LocalQeExecutor` reruns admission before preparation or mutation, then
`QeInputStager` writes the native input directly from the binding's typed provider
artifact. `LocalQeExecutionPreparer` consumes and retains that exact binding.
`LocalQeExecutionPreparationRequest` has no native-input source path and its external
source bindings carry only KSD artifact identity plus absolute local path.
Pseudopotential byte count and SHA-256 checks in preparation, staging, and process-entry
snapshot verification come from the exact provider requirement; KSD continues to own
path confinement and source re-observation. Predecessor trees remain KSD-admitted local
evidence, and legacy result-wire input records remain until atomic wire replacement,
so no legacy input owner is deleted. Passing tests
establish represented software behavior only; they establish no calculator
compatibility, numerical convergence, scientific validity, or execution authority.

## Verification

Source-mirrored software verification is in
`python/tests/software_verification/ksdft2effmass/integration/quantum_espresso/test__QeCalculatorInputAdmission__admission.py`.
Typed synthetic composition is isolated in
`python/tests/ksdft2effmass/integration/quantum_espresso/resources/calculator_input_scenarios.py`.
