# Plane-wave DFT and Quantum ESPRESSO package-ownership decision

## Problem

The first QE execution slice placed QE-named inputs, executable configuration,
process observations, diagnostics, and outcomes in the private flat module
`ksdft2effmass.calculators._quantum_espresso_execution`, while existing native input
writing and QEXSD parsing lived in `ksdft2effmass.integration.quantumespresso`.
Backend-neutral plane-wave study records separately lived in
`ksdft2effmass.calculators._plane_wave_study`.

The decision determines whether calculator-independent plane-wave DFT contracts and
QE-specific native contracts remain split or receive concept- and backend-cohesive
public package owners.

## Observed pre-decision behavior

**Observed fact.** Architecture v2 assigned shared plane-wave vocabulary and
calculator-facing executor ports to `ksdft2effmass.calculators`, while concrete native
serialization, invocation, parsing, artifact discovery, and failure mapping belonged
to `ksdft2effmass.integration.<external-system>`.

**Observed fact.** The implemented `QePwInputFile`, `QePwInputFileWriter`, and QEXSD
parser were already integration-owned under the unseparated package spelling
`integration.quantumespresso`.

**Observed fact.** The active integration Task introduced a provisional private
`calculators._quantum_espresso_execution` module and a provisional
`integration.quantumespresso.diagnostics` module before this package decision.

**Inference.** Continuing that split would require users and maintainers to inspect
both packages for one backend and would encourage QE-specific growth in the package
intended to own backend-neutral plane-wave DFT meaning.

## Decision requirements

**Accepted requirement.** Backend-neutral plane-wave DFT contracts contain no QE
native syntax, program names, diagnostic signatures, QEXSD records, or executable
policy.

**Accepted requirement.** All QE-specific native records and behavior have one
canonical package owner.

**Accepted requirement.** Workflow owns authority, dispatch, persistence, result
ingress, and CPN mechanics; neither calculator nor integration packages may grant
execution authority or perform retry.

**Accepted requirement.** The generic plane-wave interface remains a narrow typed
port and vocabulary, not a universal electronic-structure base class, engine
hierarchy, plugin registry, or erased backend dictionary.

**Accepted requirement, superseded.** Option B initially retained the former
`integration.quantumespresso` imports through a compatibility namespace. The human
subsequently decided that this pre-release development repository does not need that
namespace or the legacy `io.quantum_espresso.qexsd` forwarding path; only the
canonical `integration.quantum_espresso` package remains.

**Human choice resolved.** The human authorized Option B below and later authorized
removal of its temporary compatibility namespace.

## Option A

**Conceptual model**
Retain calculator-owned QE contracts and integration-owned QE implementation.

**Authority**
Preserve the earlier calculator architecture unchanged.

**Ownership/dependency**
QE contracts remain in `calculators`; native implementation remains in
`integration.quantumespresso`.

**Runtime/dispatch**
No runtime change.

**Migration**
Continue the provisional private modules.

**Reversibility**
Highest because no relocation occurs.

**Failures**
Typed diagnostic and calculator outcomes remain split across packages.

**Complexity**
Lowest immediate migration cost.

**Maintenance**
One backend continues to require two ownership surfaces.

**Context-window consequences**
QE work requires both calculator and integration implementation context.

**Future compatibility**
Additional backends may add more backend-specific calculator modules.

**Advantage**
Preserves the earlier consumer-owned calculator port interpretation.

**Risk**
The calculator package accumulates external-system semantics instead of remaining
backend-neutral.

## Option B

**Conceptual model**
Place backend-neutral plane-wave DFT contracts in `ksdft2effmass.calculators.dft.pw`
and every QE-specific contract and implementation in
`ksdft2effmass.integration.quantum_espresso`.

**Authority**
`calculators.dft.pw` owns shared plane-wave DFT meaning and narrow structural ports.
`integration.quantum_espresso` owns QE meaning and implements those ports. Workflow
retains execution authority.

**Ownership/dependency**
The inward direction is Workflow contracts to generic plane-wave contracts to the
outward QE integration adapter. Generic packages never import the QE integration.

**Runtime/dispatch**
The QE integration returns concrete immutable QE results that satisfy the applicable
generic plane-wave protocol and are adapted by application composition to existing
Workflow dispatch outcomes.

**Migration**
Move generic records from the flat private plane-wave module into
`calculators/dft/pw/`; move provisional QE execution records, diagnostics, native
input, and QEXSD ownership into `integration/quantum_espresso/`. Remove the former
`integration/quantumespresso/` package after consumers and tests use the canonical
path.

**Reversibility**
The ownership split remains revisable, but the removed import spelling is not
supported.

**Failures**
Generic contracts expose only demonstrated backend-independent process and outcome
meaning. QE codes, signatures, native artifacts, and exact failure mapping remain
integration-owned.

**Complexity**
Moderate one-time migration cost.

**Maintenance**
Generic plane-wave and QE-native concepts each have one cohesive owner.

**Context-window consequences**
Backend work normally needs one integration package plus the narrow generic port it
implements.

**Future compatibility**
ABINIT or another backend may implement the same demonstrated plane-wave protocol
without importing QE types.

**Advantage**
Separates scientific-method vocabulary from external-system semantics and matches the
repository's anti-corruption-boundary direction.

**Risk**
The `pw` package segment can be confused with QE `pw.x`; public documentation and
`PlaneWave...` names must state that it means backend-neutral plane-wave DFT.

## Option C

**Conceptual model**
Add a public calculator-owned QE facade between generic plane-wave contracts and the
QE integration implementation.

**Authority**
Calculator owns both generic and QE-facing contracts; integration owns effects.

**Ownership/dependency**
QE behavior spans generic calculator, QE calculator facade, and QE integration layers.

**Runtime/dispatch**
Integration implements the QE facade, which implements or adapts the generic port.

**Migration**
Create both `calculators.dft.pw` and `calculators.quantum_espresso` plus the renamed
integration package.

**Reversibility**
Moderate because the facade creates new public compatibility obligations.

**Failures**
QE failure records remain calculator-owned while their production remains
integration-owned.

**Complexity**
Highest type and adapter count.

**Maintenance**
Three layers must remain synchronized for one backend.

**Context-window consequences**
Review requires generic, facade, and integration surfaces.

**Future compatibility**
Useful only after demonstrated consumers require a stable QE facade independent of
its integration.

**Advantage**
Preserves strict consumer-owned QE ports.

**Risk**
Premature facade stabilization and duplicate records without a demonstrated consumer.

## Three-option comparison

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Generic/backend separation | Partial | Strong | Strong |
| QE cohesion | Partial | Strongest | Partial |
| Migration cost | Lowest | Moderate | Highest |
| Public API burden | Low | Controlled | High |
| Multi-backend extension | Moderate | Strong | Strong |
| Duplicate-type risk | Moderate | Lowest | Highest |

## Recommendation

**Accepted recommendation: Option B.**

The canonical public package for backend-neutral plane-wave DFT contracts is
`ksdft2effmass.calculators.dft.pw`. Public types there use `PlaneWave...` names and
state explicitly that `pw` does not mean QE's `pw.x` program. The package owns only
shared meaning demonstrated by more than one backend or required by the generic
Workflow boundary.

The canonical public package for QE-native contracts and behavior is
`ksdft2effmass.integration.quantum_espresso`. It owns QE input syntax, exact QE input
and executable bindings, native diagnostics and classifier catalogs, QEXSD records,
artifact discovery, and local QE execution. Concrete QE results may satisfy narrow
generic protocols through structural typing; no generic nominal base class is added.

The former `ksdft2effmass.integration.quantumespresso` package and
`ksdft2effmass.io.quantum_espresso.qexsd` path are removed. The QEXSD aggregate
adapter moves to the canonical QEXSD package. Supported source, tests, and
documentation use only the canonical underscored package spelling. No forwarding
namespace or duplicate implementation remains.

The provisional `_quantum_espresso_execution.py` and
`integration.quantumespresso.diagnostics` implementation must be relocated before
further execution implementation. Tests, source documentation, architecture pages,
and Sphinx API pages must use the canonical package.

## Deferred questions

- Which additional private `_plane_wave_study` contracts have enough demonstrated
  consumers for later public stabilization.
- Exact generic protocol expansion after another backend implements the same boundary.
- Stable public serialization remains deferred; package relocation does not select a
  wire format.

## Human decision required

Resolved. The human authorized **Option B — generic plane-wave DFT contracts under
`ksdft2effmass.calculators.dft.pw` and all QE-specific contracts and behavior under
`ksdft2effmass.integration.quantum_espresso`**. The human subsequently confirmed that
the temporary `integration.quantumespresso` compatibility namespace and legacy
`io.quantum_espresso.qexsd` forwarding path are not needed and may be removed. These
decisions change no scientific setting, authorize no executable invocation, and
establish no numerical or scientific claim.
