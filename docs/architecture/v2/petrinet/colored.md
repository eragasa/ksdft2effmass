# Generic colored Petri net

## Status and package

This page defines the prospective Architecture v2 generic colored-Petri-net boundary. It is not implemented. Its canonical package is `ksdft2effmass.petrinet.colored`.

The public vocabulary uses the full names `ColoredPetriNetDefinition`, `ColoredPetriNetMarking`, `ColoredPetriNetToken`, `ColoredPetriNetBinding`, `ColoredPetriNetEnablementResult`, `ColoredPetriNetSelectionDirective`, `ColoredPetriNetFiringInput`, `ColoredPetriNetFiringResult`, `ColoredPetriNetTransitionEnabler`, `ColoredPetriNetBindingSelector`, and `ColoredPetriNetTransitionFirer`, together with precisely named immutable result and value records. Abbreviated names are not a second public API.

## Semantic model

`ColoredPetriNetDefinition` represents identified colors, places, transitions, arcs and inscriptions, pure guards, and a definition-owned total transition priority. `ColoredPetriNetToken` contains a color-qualified immutable value and, where required, an identity or represented multiplicity. `ColoredPetriNetMarking` is a semantic multiset of tokens by place; incidental representation order never selects behavior.

`ColoredPetriNetBinding` is an immutable ordered sequence of variable/value pairs under the definition's declared variable order. `ColoredPetriNetTransitionEnabler` evaluates inscriptions and pure guards and returns `ColoredPetriNetEnablementResult`: the complete canonically ordered enabled transition/binding set with the exact definition, marking, expression, and ordering-policy identities.

`ColoredPetriNetBindingSelector` applies definition-owned total priority, then canonical transition identity, then canonical binding order. It gives no fairness guarantee. A `ColoredPetriNetSelectionDirective` may override this result only when the exact versioned definition explicitly permits that identified directive; ambient choice is forbidden.

`ColoredPetriNetFiringInput` is immutable and contains the exact definition and transition identities, predecessor `ColoredPetriNetMarking`, selected `ColoredPetriNetBinding`, and an immutable generic external-output-value binding. The external binding is empty when the transition needs no values produced outside the generic net. Its keys and values are generic expression variables and color-qualified values, never Workflow, Task, calculator, or ResultObject concepts.

`ColoredPetriNetTransitionFirer` validates the firing input against the exact enablement and identified selection. It evaluates input, read, and inhibitor inscriptions against the selected binding, then evaluates output inscriptions against that binding extended only by the explicit external-output-value binding. Missing, extra, or ambiguous external output values are rejected. The firer validates every produced token's place, color/type, identity where required, represented multiplicity, and arc/inscription constraints.

Successful firing consumes only input-arc tokens, preserves tokens observed through read arcs, applies inhibitor arcs only as enabling constraints, and adds exactly the validated output tokens. It returns immutable `ColoredPetriNetFiringResult` containing the successor marking plus exact definition/transition, predecessor, selected binding, external-output-binding, consumed-token, read-token, inhibitor-evaluation, produced-token, inscription/version, and ordering-policy audit facts. Failure contains structured findings and no successor. Firing is pure; the same exact input and versioned evaluators produce the same represented result.

```mermaid
flowchart LR
    definition["ColoredPetriNetDefinition"] --> enabler["ColoredPetriNetTransitionEnabler"]
    marking["ColoredPetriNetMarking"] --> enabler
    enabler --> enabled["ColoredPetriNetEnablementResult"]
    enabled --> selector["ColoredPetriNetBindingSelector"]
    directive["Permitted ColoredPetriNetSelectionDirective"] -.-> selector
    selector --> selected["Identified ColoredPetriNetBinding selection"]
    selected --> firing_input["ColoredPetriNetFiringInput"]
    marking --> firing_input
    external["Immutable generic external-output-value binding"] --> firing_input
    firing_input --> firer["ColoredPetriNetTransitionFirer"]
    firer --> successor["ColoredPetriNetFiringResult<br/>successor + audit facts"]
```

## Canonical ordering and identity

Canonical token keys derive from the versioned color identity, canonical token-value representation, and token identity or represented multiplicity. Equivalent semantic markings under the same definition and ordering policy therefore produce the same ordered enablement set and selection. Exact wire formats and canonical lexical forms remain deferred.

## Prohibited domain coupling

This generic package owns only colors, places, transitions, arcs and inscriptions, pure guards, token values, markings, canonical enablement and binding selection, explicit generic firing inputs, output-inscription evaluation, produced-token validation, and pure firing. It contains no workflow or scientific concepts, external-effect behavior, authority policy, persistence policy, dispatch, or publication behavior. A generic firing never invokes domain operations or creates domain records.

`ksdft2effmass.workflows` imports `ksdft2effmass.petrinet.colored`. The reverse dependency is forbidden. Workflow code may use abbreviated private or local import aliases, but prospective documentation and public exports use only the full `ColoredPetriNet*` terminology.

## Unresolved issues

- `ColoredPetriNetFiringInput` does not yet specify fields for the exact `ColoredPetriNetEnablementResult`, identified selection, and applicable `ColoredPetriNetSelectionDirective` identities. Until those identities are retained, firing history cannot distinguish ordinary deterministic selection from an authorized directive override unambiguously.
- Canonical definition, marking, expression, token-value, and result wire formats.
- Canonical identity lexical forms.
- Whether expression evaluators are public ActionObjects or private strategies.

This prospective generic contract is not implemented or accepted software.
