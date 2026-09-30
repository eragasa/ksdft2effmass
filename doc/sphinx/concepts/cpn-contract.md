# Generic colored-Petri-net contract

The live generic colored-Petri-net API is
`ksdft2effmass.petrinet.colored`. Its public names use the complete
`ColoredPetriNet*` vocabulary. The former abbreviated
`ksdft2effmass.workflows.cpn` compatibility package is retired and no aliases are
provided.

## Represented objects

A `ColoredPetriNetValue` is a closed tagged value. A
`ColoredPetriNetToken` associates one value with one color and may carry an
individual token identity when correlation matters. A
`ColoredPetriNetMarking` is an immutable semantic multiset over identified places;
repeated equal anonymous tokens represent multiplicity.

A `ColoredPetriNetDefinition` owns immutable color, place, transition, and arc
definitions plus exact transition priority and selection policy. Guards and
inscriptions use the closed pure expression vocabulary. Definitions contain no
Workflow policy, scientific payload objects, external execution, persistence, or
mutable engine state.

A `ColoredPetriNetBinding` preserves the transition definition's declared variable
order. Structural compatibility across definitions, markings, expressions, and
bindings belongs to the corresponding validator or ActionObject rather than to an
individual DataObject.

## Pure operations

`ColoredPetriNetTransitionEnabler` returns the complete deterministic enabled-binding
set or one closed failure. `ColoredPetriNetBindingSelector` chooses the canonical
binding or applies one exact directive only when the definition permits directed
selection. `ColoredPetriNetTransitionFirer` verifies the complete identity-bound
operation chain and returns a successor marking and audit facts or a closed failure.

These operations are pure software transformations. They do not invoke scientific
Tasks, execute a calculator, persist a Workflow run, authorize an effect, or establish
scientific acceptance.

Workflow composition remains owned by `ksdft2effmass.workflows`.
`ColoredPetriNetWorkflowAdapter` consumes explicit immutable Workflow mapping and
result-token correlation records and delegates enablement and selection to the generic
package without creating a reverse dependency.

## Historical version-1 boundary

The retained files under `specification/workflow-cpn/v1/` and the Architecture v1
pages describe the retired workflow-oriented contract and its historical wire
representation. They remain audit history and are not a supported Python import or an
alternative API. The v2 generic records are intentionally not schema- or record-equal
to those historical routing envelopes.

Constructor, validator, enablement, selection, firing, adapter, import, and dependency
tests are software verification only. They provide no numerical verification,
scientific validation, uncertainty quantification, protected-execution authority, or
release claim.
