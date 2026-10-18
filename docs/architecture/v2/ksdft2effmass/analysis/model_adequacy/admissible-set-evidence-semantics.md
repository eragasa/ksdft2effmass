# Admissible-set evidence semantics

## Purpose and status

This architecture contract standardizes the **evidentiary meaning** of KSD admissible-
set results across controlled model-adequacy studies. It applies to the retained scalar
periodic-1D demonstration, the historical periodic-1D finite-angle regression, the
prospective periodic-2D hopping-shell hierarchy, and future periodic-3D studies that
satisfy the explicit
[three-dimensional experiment architecture](../../../experiments/model-adequacy/periodic3d/index.md).

This is a vocabulary and invariant contract, not a shared Python API, result schema,
solver interface, metric, or scientific protocol. No common admissible-set code
framework is authorized by this page. Each experiment or analysis continues to own its
concrete parameter space, channels, units, normalizations, thresholds, metrics,
component families, masks, scientific domain declarations, certificate-method binding,
experiment data and retained evidence that instantiate owner-defined mathematical
premises, hierarchy rules, evidence wrappers, premise-failure policy, and retained-
evidence policy. Reusable unit-free witness and separation-certificate mathematics does
not become KSD-owned merely because an experiment binds it to scientific controls.

## Mathematical evidence boundary

For one frozen problem, let $X$ be the identified candidate-parameter space, let
$L_A,L_B$ be the two declared channel losses, and let $\tau_A,\tau_B$ be their declared
thresholds. The channel admissible sets are

$$
\mathcal A=\{x\in X:L_A(x)\leq\tau_A\},
\qquad
\mathcal B=\{x\in X:L_B(x)\leq\tau_B\}.
$$

A channel may itself be an identified finite family. In that case, its admissible set
is the protocol-declared union or other composition, and a retained point must identify
the component used to establish its channel membership.

The following meanings are common.

### Compatible through a common witness

Compatibility requires an explicit **same-parameter witness** $x_w\in X$ with

$$
L_A(x_w)\leq\tau_A,
\qquad
L_B(x_w)\leq\tau_B.
$$

The point has one identity in the common parameter space; two nearby channel-specific
points are not a common witness. A small fitting objective, a small estimated set
distance, failed falsification, or a solver's convergence flag is not a compatibility
proof. When a channel is a finite family, the witness also retains the selected
component identity needed to reconstruct membership.

### Certified separated above resolution

For two nonempty sets and one declared metric $d$, define

$$
\delta^*=\inf_{a\in\mathcal A,\,b\in\mathcal B}d(a,b).
$$

A separation disposition requires a reconstructable conservative lower bound
$\underline\delta\leq\delta^*$ and a declared resolution $\rho$ satisfying

$$
\underline\delta>\rho.
$$

A local optimizer or feasible pair can establish a witness or an upper bound, but it
cannot by itself establish a positive global lower bound. Certificate methods may use
exact inequalities, support bounds, outward-rounded enclosures, or another
protocol-specific construction. The owning study must retain every premise that makes
its certificate valid, including any domain-containment, convexity, finite-family,
metric, mask, or rounding premise.

An empty channel set is a separate local evidence state, not certified positive
separation under this contract. The owner must state how emptiness is established and
how it affects higher-level conclusions.

### Unresolved

When both channel sets are nonempty and neither a common witness nor a lower bound above
resolution has been established, their relationship is **unresolved**. This is an
evidence state, not a claim that the sets intersect or are disjoint. Failed search,
solver failure, an upper bound above zero, a lower bound at or below resolution, or
insufficient certificate premises cannot be promoted to compatibility or separation.

A study may retain more specific local labels such as `unresolved-nonempty`,
`invalid-premise`, or channel-empty outcomes. Those labels do not change the shared
meaning above.

## Correlation invariants

A result's disposition is a summary of correlated evidence, not evidence by itself.
Every owning result model and strict wire schema must enforce the applicable invariants.

| Evidence state | Required correlated evidence | Forbidden promotion |
|---|---|---|
| Compatible through a common witness | Identified point in the common parameter space; both reconstructed channel values; both thresholds; component identity where applicable | Nearby feasible pair, small distance, or one-channel feasibility presented as compatibility |
| Certified separated above resolution | Declared metric and resolution; verified nonemptiness of both sets; reconstructable conservative lower-bound certificate; verified strict comparison to resolution | Failed search, local optimum, sampled plot, or unverified solver status presented as separation |
| Unresolved nonempty | Evidence that both sets are nonempty and no decisive proof is retained; optional candidates or upper bounds clearly marked nondecisive | Absence of a witness presented as separation, or absence of a certificate presented as compatibility |
| Channel empty or invalid premise | Owner-specific emptiness proof or named failed premise and its scope | Reclassification as positive separation or a valid hierarchy conclusion without an explicit local rule |

A witness, certificate, bound, or diagnostic must identify the exact controls and channel
objects to which it applies. Reordering components, changing masks, thresholds, units,
normalization, metric, parameter coordinates, or resolution breaks that correlation
unless the owner explicitly reconstructs a new result.

## Independent decisive verification

Decisive evidence must be independently reconstructed from retained scientific inputs
and result data. The verifier must not call the producer to reproduce its own result and
must not treat serialized dispositions, plots, solver success flags, or cached
intermediate values as an oracle.

At minimum, independent verification reconstructs:

1. the identified common parameter space and channel definitions;
2. witness membership in both threshold sets;
3. certificate premises and the conservative lower bound;
4. the comparison of that lower bound with the declared resolution; and
5. the disposition/evidence correlation.

The owning study must disclose unavoidable shared numerical libraries or arithmetic
assumptions. Independent reconstruction reduces circularity; it does not turn
floating-point results into exact proofs unless the certificate contract supplies exact
or directed-rounding guarantees.

Training or source data define the admissible sets. Evaluation-only, withheld, or
locality diagnostics may test behavior of retained points, but they cannot change the
channels, thresholds, witness, certificate, or disposition after inspection.

## Scientific interpretation

These outcomes are bounded model-adequacy evidence for one identified parent,
candidate family, state space, basis or gauge convention, channel definition,
normalization, threshold pair, parameter domain, metric, resolution, and data role.
They do not by themselves establish:

- scientific validation or physical truth;
- material transferability;
- parent-model correctness;
- continuum or basis convergence;
- uniqueness of a compatible witness;
- inadequacy of every larger candidate family or alignment family;
- probabilistic confidence or uncertainty quantification; or
- human acceptance or publication readiness.

Software tests establish implementation behavior only. A calculated witness or
certificate retains the validity domain of its frozen scientific contract.

## Reusable mathematical ownership

Reusable certificate mathematics belongs upstream of the scientific experiment when it
can be expressed without KSD units, model identities, channel meanings, or disposition
policy. The exact extraction remains architecture-gated and must bind reviewed owner
contracts rather than infer an API from this semantic document.

- Optimization is the prospective owner of capability-specific unit-free contracts for
  explicitly supported set representations: intersection-feasibility witnesses,
  support functions, strict-separation certificates, and validation of the mathematical
  conditions under which a directional separation margin divided by the dual norm is a
  distance lower bound.
- Numerics is the prospective owner of reusable interval, directed-rounding, and
  conservative-enclosure primitives and their arithmetic validity conditions.
- KSD may consume those contracts directly and wrap an owner certificate with experiment
  identities, scientific inputs, retained evidence instantiating the owner-defined
  conditions, provenance, and evidence correlation.
- Historical calculation-local certificate code remains historical evidence; its
  existence does not establish KSD ownership of the reusable mathematics.

## Local ownership and deliberate non-extraction

The following remain local to each concrete owner:

- physical and normalized parameter coordinates;
- channel losses, component or alignment families, and finite-union rules;
- thresholds and how they were selected;
- boxes, masks, active subspaces, and scientific domain declarations;
- metric choice, normalization, and resolution;
- selection and scientific binding of an owner-provided witness or certificate method;
- experiment inputs and retained evidence that instantiate owner-defined mathematical
  and arithmetic validity conditions;
- experiment identities, provenance, and evidence correlation;
- empty-set, invalid-premise, and other premise-failure policy;
- hierarchy nesting and minimality logic;
- training, evaluation, withheld, and locality roles; and
- experiment result wrappers, schemas, evidence manifests, dispositions, and
  interpretation.

No generic KSD `AdmissibleSetResult`, shared disposition enum, certificate hierarchy, or
solver facade should be introduced solely from the semantic overlap recorded here.
Parameterization alone does not make these studies one reusable workflow. This does not
preclude reviewed generic certificate contracts in Optimization or arithmetic primitives
in Numerics.

Extract an owner-neutral operation as soon as a concrete experiment needs it and its
semantic owner can define a complete reviewed contract; do not wait for KSD to create a
second implementation or for a second consumer to appear. Later consumers may broaden
that owner contract, but they do not justify leaving generic mathematics in KSD.
Experiment records, schemas, dispositions, and evidence policy remain local because of
their scientific meaning, not because a duplication quota has not been met. Do not claim
general 2-D/3-D lattice-vector support until the complete dimensionality/anisotropy
sequence supplies the scientific and numerical evidence for that broader claim. Similar
names or equations alone remain insufficient grounds for an unbounded framework.

## Current instantiations

| Surface | Status | Relationship to this contract |
|---|---|---|
| `calculations/ICMSEP2026/conference/paper_1/` direct scalar demonstration | Retained controlled calculation | Supplies an exact common witness and rational separation certificate; remains calculation-local historical evidence |
| `experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/regression/historical-64-257/` | Historical regression only | Retains the former common-witness and finite-angle separation channels for software regression; the active smooth-continuum experiment is outside this admissible-set contract |
| `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy` | Prospective architecture only | Plans the same decisive evidence meanings plus local channel-empty, invalid-premise, and hierarchy-minimality rules |
| [Dimensionality and anisotropy ladder](../../../experiments/model-adequacy/dimensional-anisotropy-ladder.md) | Selected experiment order; pre-version work | Orders isotropic 2-D, isotropic 3-D, anisotropic 2-D, and anisotropic 3-D as independent families without transferring outcomes or schemas |
| [Periodic-3D experiment architecture](../../../experiments/model-adequacy/periodic3d/index.md) | Selected isotropic and preserved anisotropic targets | Applies the evidence vocabulary to two distinct scalar 3-D families while keeping scientific controls, certificate-method bindings, experiment inputs and retained premise evidence, evidence wrappers, failure policy, and interpretation experiment-local |
| [General-lattice-vector extension](general-lattice-vector-extension.md) | Post-ladder architecture boundary only | Defines the later extraction gate for full-rank 2-D/3-D lattice bases; authorizes no generic result type, experiment, or arbitrary-lattice claim |

Historical names, paper labels, and enum wire strings are not standardized by this
contract. Publication-independent experiment identities and schema versions continue to
own compatibility at their respective boundaries.
