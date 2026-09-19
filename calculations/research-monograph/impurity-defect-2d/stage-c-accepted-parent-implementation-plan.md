# Adversarial execution-free Stage C implementation plan

## Authority and stop boundary

HC13 authorizes implementation and authored-fixture software verification only.
The new code path must reject or avoid the accepted periodic, Stage A, and Stage
B files during behavioral testing. It may consume only the human-adopted design,
a maintained authored compact fixture, and isolated scratch outputs. No
accepted-parent result may be created or retained.

Implementation stops after source, schema, plotter, independent verifier,
maintained tests, review, and synchronized documentation. Accepted-parent reads
or execution require a later hash-bound checkpoint and machine authorization.

## Ownership decomposition

- immutable bond, parent, operation, control, and schedule records own intrinsic
  field invariants only;
- a design deserializer owns exact design identity and inventory decoding;
- an authored-fixture deserializer owns the synthetic wire format and rejects
  any fixture that claims accepted-parent status;
- a parent-hopping constructor owns explicit Fourier reconstruction and the
  radius-18 mask;
- route-specific matrix constructors own uniform-link and seam-gauge matrices;
- alignment, model fitting, locality, symmetry, bridge, criteria, and adverse
  controls have cohesive ActionObject owners;
- a schedule executor owns one route order in one spawned process;
- a Workflow composes schedules, comparisons, and deterministic serialization;
- an independent verifier imports no runner code and reconstructs through its
  own Fourier, matrix, and fit paths;
- a plotter consumes retained JSON only; and
- `main()` remains a minimal argparse-owned adapter.

No generic helper, manager, or untyped boundary is introduced.

## Implementation sequence

1. Retain the existing accepted execution-free toy command unchanged.
2. Add an accepted-parent authored-fixture mode with mutually exclusive command
   arguments and overwrite refusal.
3. Freeze a 61-hopping isotropic fixture and a $15\times15$ anisotropic authored
   dispersion under the maintained test resources directory.
4. Reconstruct all 225 anisotropic Fourier coefficients independently within
   each schedule process, then apply the radius-18 mask and retain truncation,
   Hermiticity, $D_2$, and axis-swap diagnostics.
5. Construct the 52 frozen cases per schedule in each route, apply the known
   attack, inversely align, subtract, fit all five oriented model bases, and
   retain shell diagnostics.
6. Retain 208 route evaluations, 104 bridges, 1,040 fit records, and 104 exact
   schedule comparisons in canonical schedule-independent order.
7. Implement all ten adverse controls, including the two proposed anisotropic
   discrimination floors, without tuning after observing accepted inputs.
8. Add the closed result schema and deterministic SVG plotter.
9. Implement an independent verifier without runner imports or runner matrix
   consumption.
10. Add maintained artifact-owned tests for authority rejection, inventories,
    model selection, bridges, fresh processes, symmetry, adverse floors,
    schema, determinism, plotting, overwrite refusal, and verifier independence.
11. Run format, lint, strict typing, compilation, pytest, Python evidence
    conformance, schema validation, deterministic regeneration, checksum,
    Harness, repository, LaTeX, and visual checks.
12. Perform an adversarial implementation review and stop for human acceptance.

## Adversarial attack plan

The implementation must fail or discriminate when:

- the design is unadopted, implementation or execution flags are true, or exact
  inventories differ;
- a fixture claims accepted-parent or calculated-evidence status;
- hopping inventories contain duplicates, omit Hermitian partners, or violate
  their declared symmetry group;
- anisotropic preprocessing is shared across schedule processes;
- Route B consumes Route A matrices or omits seam phases;
- the gauge bridge direction, integer lift, or twist transformation is wrong;
- subtraction precedes alignment or omits the $0.137E_G$ correction;
- the expected planted class is exposed to model selection;
- diagonal nonlocal bases are not transformed with case orientation;
- anisotropic $D_4$ invariance is substituted for $D_2$ plus a distinct-parent
  axis swap;
- schedules disagree cleanly;
- an adverse floor is nondiscriminating;
- nonfinite diagnostics are serialized; or
- an existing output is overwritten.

## Acceptance for this implementation task

The authored fixture must produce all frozen counts, exact clean schedule
agreement, route and covariance residuals within design criteria, expected first
model classes without selector access to expected identities, and all adverse
values above their predeclared floors. The independent verifier and schema must
pass, and deterministic result and SVG regeneration must be byte-identical.

A pass establishes only synthetic software behavior. It does not establish an
accepted-parent Stage C result, numerical verification of the accepted parent,
material validation, scientific validation, uncertainty quantification, or
execution authority.
