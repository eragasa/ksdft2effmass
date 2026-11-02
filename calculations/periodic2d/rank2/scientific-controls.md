# Periodic 2-D rank-two scientific-control crosswalk

The maintained periodic-1D rank-two calculation at
[`calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/`](../../periodic1d/rank2/band-equivalence-versus-hopping-locality/README.md)
is the lifecycle and evidence-architecture donor for the periodic-2D rank-two
band-equivalence calculations. It supplies the separation of calculation,
independent verification, authenticated rendering, immutable execution identities,
and explicit claim boundaries. It does **not** supply periodic-2D numerical values by
inheritance.

This document records which donor responsibilities are retained, how two-dimensional
geometry changes them, and where the three child families remain scientifically
independent. The field-level inventory is maintained in
[`diagnostic-parity.md`](diagnostic-parity.md); every donor diagnostic is accounted for
there as an installed two-dimensional channel, a dimensionally adapted channel, or an
explicitly inapplicable one-dimensional specialization.

## Donor-to-periodic-2D crosswalk

| Periodic-1D rank-two donor responsibility | Periodic-2D rank-two realization | Admission boundary |
|---|---|---|
| Exact parent definition and retained rank | Each band-equivalence request binds the four-state synthetic-model definition, parent basis, retained seed, retained basis, and rank-two result inventory. | A four-state parent and rank-two seed do not establish subspace isolation or model adequacy. Parent and retained spaces must be identified before operator comparison. |
| Parent/subspace qualification | Each stored point retains sampled and lower-bound external-gap diagnostics, seed overlap, parent Hermiticity, eigensystem, projector, retained-parent, and Fourier-reconstruction defects. | Qualification channels remain distinct from band equivalence and locality. A passing software check is not a material or convergence result. |
| Frame transport and loop closure | The tensor mesh retains neighbor-transport singular values, Procrustes residuals, unitarity and rank diagnostics, periodic closure, and, when applicable, closure/plaquette holonomy diagnostics. | Rank-deficient transport is not assigned a unique frame. Applicability and inapplicability reasons are retained rather than replaced by zeros. |
| Exact retained-space band-equivalence channel | Direct retained-space band defects are evaluated only after the declared basis, gauge, energy reference, units, reciprocal coordinates, and geometry are aligned. | Ordered spectra alone do not identify operator equivalence; operator and spectrum channels remain separate. |
| Restricted global alignment control | Family-owned restricted rotations retain their angle and correlation diagnostics. | The orthogonal and nonorthogonal families do not inherit one another's alignment result or normalization. |
| Cyclic Fourier and Nyquist accounting | Finite tensor-product Fourier coefficients, reconstruction/Parseval defects, shell powers, omitted powers, and tensor-mesh Nyquist contributions are retained. | The one-dimensional even-mesh Nyquist convention is not copied as a scalar endpoint rule. Tensor Nyquist classes and physical metric geometry own the two-dimensional interpretation. |
| Truncation, interpolation, and total error channels | Complete physical-metric shells are evaluated independently for reference and comparison operators; truncation, interpolation, and total errors remain separately named. | Equal-radius shells are never split. Basis offsets participate in nonorthogonal physical distances. |
| Minimum tolerance-satisfying support | For each declared tolerance, the first passing support is the minimum stored complete shell satisfying every frozen finite criterion. | Failure to pass at the shell cap is unresolved, not evidence of impossibility. A shell index is family- and geometry-relative, not a transferable physical radius. |
| Momentum-mesh refinement | The development ladders compare the bound construction sizes 16, 32, and 64 and retain adjacent-level changes. | Current half-step Monkhorst--Pack doubling meshes have no shared nodes. No prospectively frozen family-wide refinement tolerances exist, so the current momentum disposition remains unresolved rather than converged. |
| Amplitude resolution | Each request binds an explicit amplitude-resolution doubling ladder used by the maintained analysis. | Amplitude resolution does not replace momentum refinement and cannot be used to infer a continuous-amplitude theorem. |
| Canonical direct-result retention | A nominal result binds its exact request and typed diagnostics. Direct execution metadata bind configuration, result, producer, verification, and rendering hashes. | The retained square execution contains only the historical nominal result. Refinement assessments and the newer generic quadratic-loss record are not retroactively inserted into its bytes. |
| Byte-owning independent verification | Verification parses exact retained result bytes, reconstructs independent parent/band/shell-power checks, and authenticates the visualization projection. | SHA-256 establishes byte identity only. Independent finite reconstruction establishes agreement with declared checks only. |
| Authenticated rendering | Rendering consumes admitted result, verification, and projection bytes and authenticates a closed figure inventory. | Rendering must not rerun scientific calculation or silently substitute development output. |

## Family-owned controls

The shared donor architecture does not make the children one calculation.

| Child owner | Geometry and parent controls | Gauge/locality controls | Current lifecycle disposition |
|---|---|---|---|
| [`orthogonal/band-equivalence-locality/`](orthogonal/band-equivalence-locality/README.md) | Square direct lattice and directed-axis synthetic parent. | Axis-maximum gauge normalization; square-family shell inventory and cap. | Direct typed lifecycle with retained unsealed `direct-square-rank2-n16`; development refinement remains separate. |
| [`nonorthogonal/band-equivalence-locality/`](nonorthogonal/band-equivalence-locality/README.md) | Matched square, triangular-Bravais, and honeycomb-basis synthetic controls; primitive vectors are columns and basis offsets contribute to metric distance. | Bond-RMS gauge normalization; family-owned bonds, shells, cap, and transport/topology applicability. | Direct typed lifecycle installed and tested, but no retained execution. |
| [`strain-locality/`](strain-locality/README.md) | Unit-area rhombic geometry with distinct M0, M1, and M2 response constructions. | Geometry-only, four-state response, prescribed radial response, witness, and scan channels remain distinct. | Development composition only; no byte-owning verifier, authenticated projection, direct execution package, or retained result. |

The square, triangular/honeycomb, and rhombic-strain controls therefore cannot be
combined into one scientific conclusion. Cross-family comparison is a downstream action
that must authenticate each admitted family result and preserve each family's control
identity.

## Quadratic-loss admission

The reusable finite-rank loss implementation admits the Ragasa2026a rank-two
specialization only when all of the following are declared together:

1. retained rank exactly two;
2. finite `complex128` Hermitian reference and comparison matrix fields;
3. matching leading sample shape and normalized nonnegative sample weights in NumPy
   C-order;
4. retained-space, basis, gauge, energy-reference, geometry, and energy-unit identities;
5. positive normalization `E_ref`, explicitly not interpreted as a band gap;
6. production operator and ordered-spectrum losses normalized by
   `2 E_ref^2`; and
7. independent scalar matrix-element and ordered-eigenvalue reconstruction at the
   verification boundary.

The loss channels supplement rather than replace parent qualification, transport,
reconstruction, Fourier, truncation, interpolation, and support-decision channels.
Because `direct-square-rank2-n16` predates this record, adding the losses to a retained
calculation requires a new execution identity and separately authorized scientific
execution. Historical bytes remain immutable.

## Evidence and authorization boundary

This crosswalk is a protocol and ownership record. It creates no calculated result,
convergence result, sealed evidence, material validation, or publication acceptance.
Scientific execution, retained-result creation, sealing, promotion, and publication
remain separate human-authorized actions.
