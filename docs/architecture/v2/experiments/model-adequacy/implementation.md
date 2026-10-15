# Model-adequacy implementation architecture

## Source structure

Each concrete family is implemented beneath `experiments/model-adequacy/` and mirrored
recursively in this architecture tree.

- Family packages own definitions, producers, results, schemas, verification, and tests.
- Module directories are created only with matching source modules.
- `ClassName` directories contain the most detailed method and implementation documentation.
- Mutable development coordination stays under `docs/tasks/`.

## Owner composition

Model-adequacy experiments delegate generic mathematics while retaining scientific
meaning.

- Optimization may provide reviewed unit-free least-squares, quadratic, support, selection, intersection-feasibility, and capability-specific strict-separation certificate contracts and algorithms for explicitly supported set representations.
- Numerics may provide reviewed unit-free finite-transform and invariant-diagnostic kernels with explicit public contracts, plus interval, directed-rounding, and conservative-enclosure primitives and arithmetic validity conditions.
- PhysKit may provide reviewed lattice, metric, hopping, unit, and other physics-semantic records or adapters without acting as a required facade over Numerics or Optimization; primitive arithmetic inside a physics-semantic diagnostic does not alone determine ownership.
- KSD installed packages may provide reviewed domain-specific feature construction, but not competing generic numerical or certificate mathematics.
- Experiments retain features, units, weights, thresholds, domains, metric selection and normalization, certificate-method binding, experiment data and retained evidence instantiating owner-defined validity conditions, evidence wrappers, premise-failure policy, dispositions, and interpretation.

## Producer separation

Production and decisive verification follow different action paths.

- Producers construct candidates and proof objects.
- Serializers transport strict wire state.
- Verifiers reconstruct decisive formulas from retained inputs.
- Results enforce evidence and disposition correlation.
- Evaluation-only data cannot feed back into producer controls.

## Non-extraction

This package does not select a generic model-adequacy framework.

- No common `AdmissibleSetResult` is authorized.
- No shared disposition enum is authorized.
- No generic KSD certificate hierarchy is authorized; reviewed reusable certificate contracts may instead be owned by Optimization.
- No solver facade is authorized.
- A concrete experiment need and clear semantic owner authorize review of the smallest complete reusable extraction before KSD creates a duplicate implementation.
- Later consumers may broaden an owner contract but are not an initial extraction gate.
