# Colored Petri Nets

Use the full-name generic API from `ksdft2effmass.petrinet.colored`:

```python
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBindingSelector,
    ColoredPetriNetTransitionEnabler,
    ColoredPetriNetTransitionFirer,
)
```

The former `ksdft2effmass.workflows.cpn` package is retired and has no compatibility
aliases. Historical version-1 specifications and Architecture v1 pages remain
available for audit, not as live Python usage documentation.

## Contract layers

The generic package separates immutable represented state from pure operations:

1. Define colors, places, transitions, arcs, guards, and inscriptions with the
   `ColoredPetriNet*Definition` records.
2. Represent the complete predecessor multiset with `ColoredPetriNetMarking` and
   `ColoredPetriNetToken`.
3. Validate definitions and markings with the public validators.
4. Compute the complete enabled transition/binding set with
   `ColoredPetriNetTransitionEnabler`.
5. Select canonically, or use one exact directive only when the definition permits
   directed selection, with `ColoredPetriNetBindingSelector`.
6. Supply the identity-closed firing input and request a pure successor from
   `ColoredPetriNetTransitionFirer`.

Values are closed tagged `ColoredPetriNetValue` records. Integer values are signed
64-bit exact built-in Python integers; booleans are rejected. Real values are finite
binary64 values. Numeric strings and nonfinite values are not accepted. Consult the
public API documentation for the complete value vocabulary and failure contracts.

## Workflow adaptation

Scientific Workflow policy belongs to `ksdft2effmass.workflows`, not the generic CPN
package. `ColoredPetriNetWorkflowAdapter` consumes explicit immutable Workflow-owned
mapping and result-token correlation records. It supports direct, deterministic
`any_of`, and compatible combined `all_of` activation selection while remaining
effect-free.

Enablement or selection never grants execution authority. The generic operations and
Workflow adapter do not invoke Tasks, execute Quantum ESPRESSO or another calculator,
submit external work, mutate persisted state, or establish scientific acceptance.

See the [generic CPN API](../api/petrinet-colored.rst), the
[Workflow API](../api/workflows.rst), and the
[Architecture v2 generic CPN contract](../architecture/v2/ksdft2effmass/petrinet/colored/index.md).
