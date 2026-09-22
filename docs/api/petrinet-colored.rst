Generic colored-Petri-net definitions and pure semantics
=========================================================

The canonical Architecture v2 value surface is
``ksdft2effmass.petrinet.colored``.  These records represent generic Petri-net
state only; they do not represent a scientific Workflow, simulation request,
calculation result, authority grant, or persistence record.

Values
------

.. currentmodule:: ksdft2effmass.petrinet.colored

.. autoclass:: ColoredPetriNetValueKind
   :members:

.. autoclass:: ColoredPetriNetValue

Identities and tokens
---------------------

.. autoclass:: ColoredPetriNetColorIdentity

.. autoclass:: ColoredPetriNetTokenIdentity

.. autoclass:: ColoredPetriNetToken

Markings and bindings
---------------------

.. autoclass:: ColoredPetriNetDefinitionIdentity

.. autoclass:: ColoredPetriNetMarkingIdentity

.. autoclass:: ColoredPetriNetPlaceIdentity

.. autoclass:: ColoredPetriNetTransitionIdentity

.. autoclass:: ColoredPetriNetBindingVariableIdentity

.. autoclass:: ColoredPetriNetPlaceMarking

.. autoclass:: ColoredPetriNetMarking

.. autoclass:: ColoredPetriNetBindingAssignment

.. autoclass:: ColoredPetriNetBinding

Definitions
-----------

.. autoclass:: ColoredPetriNetArcIdentity

.. autoclass:: ColoredPetriNetColorDefinition

.. autoclass:: ColoredPetriNetPlaceDefinition

.. autoclass:: ColoredPetriNetTransitionDefinition

.. autoclass:: ColoredPetriNetArcDefinition

.. autoclass:: ColoredPetriNetDefinition

A definition owns canonical unique component collections, an explicit total
transition-priority permutation, and a closed selection policy defaulting to
``DETERMINISTIC_ONLY``. ``DIRECTED_ALLOWED`` is the only state permitting an
explicit identity-bound directive. Transition binding-variable order remains
exactly definition-declared. Arc direction is derived from its mutually exclusive
input/output inscription variant. Markings remain independently identified and
are not embedded in definitions. Graph-reference and marking compatibility belong
to the later structural validator.

Structural validation
---------------------

.. autoclass:: ColoredPetriNetValidationIssueCode
   :members:

.. autoclass:: ColoredPetriNetValidationIssue

.. autoclass:: ColoredPetriNetValidationResult
   :members:

.. autoclass:: ColoredPetriNetDefinitionValidator
   :members:

.. autoclass:: ColoredPetriNetMarkingValidator
   :members:

Validation returns complete immutable findings ordered by ``(path, code,
related identities, message)``. Repeated malformed occurrences and repeated
lexical spellings from distinct nominal identity classes are retained rather
than collapsed. Unknown arc place or transition references suppress dependent
pattern, template, and binder findings for that arc.

The closed codes distinguish unknown colors, places, and transitions; colors or
value kinds not admitted by their owners; undeclared, unbound, and multiply bound
input variables; external-output variables used by guards; definition-identity
mismatch; and marking place-set mismatch. Consume/read patterns may bind only
``input_variable_identities``. Guards may read only those input variables, while
output templates may read either input variables or the disjoint
``external_output_variable_identities``.

Empty findings mean only that no declared structural defect was found;
validation neither enables nor fires a transition, invokes a Task, grants
authority, nor establishes scientific acceptance. Wrong nominal validator
argument types raise ``TypeError``.

Expressions, inscriptions, and pure guards
-------------------------------------------

.. autoclass:: ColoredPetriNetValueExpressionKind
   :members:

.. autoclass:: ColoredPetriNetValueExpression

.. autoclass:: ColoredPetriNetGuardOperator
   :members:

.. autoclass:: ColoredPetriNetGuardExpression

.. autoclass:: ColoredPetriNetInputMode
   :members:

.. autoclass:: ColoredPetriNetTokenPattern

.. autoclass:: ColoredPetriNetInhibitorPattern

.. autoclass:: ColoredPetriNetInputInscription

.. autoclass:: ColoredPetriNetTokenTemplate

.. autoclass:: ColoredPetriNetOutputInscription

.. autoclass:: ColoredPetriNetGuardEvaluationResult

.. autoclass:: ColoredPetriNetExpressionEvaluator
   :members:

The evaluator is a public stateless ActionObject. It resolves only closed generic
literals and nominally bound variables and evaluates pure guards. It does not
decide that a transition is enabled, fire a transition, invoke or subclass a
scientific Task, or grant execution authority. Domain-specific Tasks and
transitions are connected through explicit Workflow adapters and composition.

Multiplicity contract
---------------------

A token contains one color-qualified immutable value and an optional nominal
identity.  Following the accepted marking-owned multiplicity decision, a token
has no multiplicity field.  Equal anonymous token occurrences are counted by the
containing ``ColoredPetriNetMarking``.  Repeated equal anonymous tokens are
retained, while each nominally identified token may occur only once across a
marking. Individually meaningful Workflow attempts and simulation results
remain separately identified and are never collapsed into anonymous
multiplicity.

Binding assignments associate nominal variables with tagged values and preserve
the owning definition's declared variable order. Definition compatibility,
completeness, and declared-order verification belong to later cross-object
validators.

Complete deterministic enablement
---------------------------------

.. autoclass:: ColoredPetriNetEnablementResultIdentity

.. autoclass:: ColoredPetriNetEnablementFailureIdentity

.. autoclass:: ColoredPetriNetExpressionEvaluatorIdentity

.. autoclass:: ColoredPetriNetOrderingPolicyIdentity

.. autoclass:: ColoredPetriNetTransitionEnablerIdentity

.. autoclass:: ColoredPetriNetEnablementFailureCode
   :members:

.. autoclass:: ColoredPetriNetEnablementFailure

.. autoclass:: ColoredPetriNetEnablementResult
   :members:

.. autoclass:: ColoredPetriNetTransitionEnabler
   :members:

The enabler returns one identity-bound closed success or failure for the complete
definition. It produces a domain-separated SHA-256 result identity from exact
input, semantic-version, and complete outcome state; this identity preimage is
not the deferred public result wire format. Success contains every distinct
guard-satisfying value binding in
definition-priority and declared-variable/value order. Failure contains no
bindings and reports invalid definitions or markings, unsupported expression or
ordering semantics, or guard evaluation failure. Wrong nominal argument types
raise ``TypeError``.

Private occurrence coordinates enforce multiset capacity without entering public
bindings. Consume demands at one place require distinct occurrences from other
consume demands. Read demands require distinct occurrences from other read
demands, while one occurrence may satisfy both a read and a consume because the
read does not remove it. Inhibitors require complete matching-token absence and
bind no value. Occurrence-distinct choices yielding the same public value binding
are deduplicated.

The operation performs no binding selection, firing, marking mutation, Task
invocation, external effect, authority decision, persistence, or scientific
acceptance. The canonical lexical identity encoding and a v2 wire format remain
deferred.

Deterministic binding selection
-------------------------------

.. autoclass:: ColoredPetriNetSelectionPolicy
   :members:

.. autoclass:: ColoredPetriNetSelectionDirectiveIdentity

.. autoclass:: ColoredPetriNetSelectionResultIdentity

.. autoclass:: ColoredPetriNetBindingSelectorIdentity

.. autoclass:: ColoredPetriNetSelectionDirective

.. autoclass:: ColoredPetriNetSelectionOutcomeKind
   :members:

.. autoclass:: ColoredPetriNetSelectionFailureCode
   :members:

.. autoclass:: ColoredPetriNetSelectionResult

.. autoclass:: ColoredPetriNetBindingSelector
   :members:

Without a directive, the selector chooses the first binding from the complete
canonical enablement result, whose order already applies definition-owned total
transition priority and declared binding/value order. Empty enablement returns the
closed ``EMPTY`` outcome. A content-identified directive may request one exact
binding only when the definition policy is ``DIRECTED_ALLOWED``. A permitted but
absent binding returns ``NO_MATCH``; prohibited, stale, mismatched, or failed
input returns a closed ``FAILURE`` with a stable code. Selection retains the
complete directive, not only its identity, so later firing can independently
verify the directive's enablement and requested binding.

Directive and result identities are domain-separated SHA-256 digests of their
complete semantic content. Selection performs no firing, mutation, fairness
scheduling, ambient choice, Task invocation, effect, or authority decision.

Identity-closed pure firing
---------------------------

.. autoclass:: ColoredPetriNetFiringInput

.. autoclass:: ColoredPetriNetFiringResultIdentity

.. autoclass:: ColoredPetriNetTransitionFirerIdentity

.. autoclass:: ColoredPetriNetTokenOccurrence

.. autoclass:: ColoredPetriNetInhibitorEvaluation

.. autoclass:: ColoredPetriNetProducedToken

.. autoclass:: ColoredPetriNetFiringAudit

.. autoclass:: ColoredPetriNetFiringFailureCode
   :members:

.. autoclass:: ColoredPetriNetFiringFailureIdentity

.. autoclass:: ColoredPetriNetFiringFailure

.. autoclass:: ColoredPetriNetFiringOutcomeKind
   :members:

.. autoclass:: ColoredPetriNetFiringResult

.. autoclass:: ColoredPetriNetTransitionFirer
   :members:

Firing receives the complete definition, predecessor, enablement and selection
results, selected binding, directive identity or absence, and exact external-output
binding. It recomputes enablement and selection rather than trusting nominal
identities alone. The lexicographically least feasible occurrence assignment is
reconstructed from canonical arcs, patterns, tokens, admitted colors, and exact
bound values.

Successful firing removes only consume occurrences, retains read occurrences,
records inhibitor absence, evaluates outputs using input plus exact external
assignments, and returns a content-identified successor marking with complete
occurrence/output audit. Identified outputs may reuse an identity released by
consumption but cannot collide with retained or other produced identities.
Every result retains the complete firing input; failures contain no successor.
Firing is pure and performs no Task invocation,
external effect, persistence, authority decision, or scientific acceptance.
The former ``ksdft2effmass.workflows.cpn`` version-1 compatibility package is
retired. These full-name classes are the sole live generic CPN API and are not
aliases for the removed workflow-oriented routing records. Historical version-1
specifications and Architecture v1 documentation remain retained for audit.
