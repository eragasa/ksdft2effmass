WorkflowRun persistence boundary
================================

Status and coverage
-------------------

The bounded Workflow persistence Task is **closed as software verified**, with
atomic repository, historical claim and durable entry operations. The same-v1 nested-history correction now integrates
immutable intent and first-terminal observations into aggregate validation and
serialization, with bounded real SQLite lifecycle evidence.
Its software gates and independent implementation/correction reviews are complete;
this is not human acceptance, scientific validation or Git closeout. Broader runs
conformance still reports 52 inherited findings outside the passing persistence
inventory; inherited callable/type debt and unexplained historical test flakiness
remain disclosed. The human selected an explicit typed
``WorkflowResultValueCodec`` supplied by outward domains through application
composition. The Workflow owner does not discover types, import outward calculator
implementations inward, or serialize arbitrary protocol implementations. Unknown
versions are incompatible. There is no registry, reflection or dynamic import.

The current public additions are immutable result envelopes, encode/decode outcomes,
structured failures, intrinsic aggregate boundary and commit-binding records,
:class:`~ksdft2effmass.workflows.WorkflowResultValueSerializer`,
:class:`~ksdft2effmass.application.ApplicationResultValueSerializer`,
:class:`~ksdft2effmass.analysis.QuantityOfInterestResultValueSerializer` and
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoResultValueSerializer`.
The scalar codec supports exactly ``ScalarQuantityOfInterestValue`` and
``ScalarQuantityOfInterestEvaluationFailure``. The QE codec supports exactly
``QuantumEspressoPwResult``, ``QuantumEspressoBandsResult`` and
``QuantumEspressoExtractedObservationResult``, including complete nested operation
and source/parser/policy/neutral provenance. Neither codec accepts subclasses or
identity-only result adapters. See :doc:`../api/quantum-espresso` for the owning
three-family wire and unchanged neutral-serializer delegation.

The Workflow codec supports complete ``ScientificDecisionResolution`` and
``NormalizedObservationSet`` values, closing the selected seven-family value scope.
The application codec binds three named immutable owners with explicit branches;
its Workflow source codec must be an exact QE serializer. See
:doc:`../api/application` for explicit construction, without a composition root.

Complete explicit aggregate traversal is now implemented by
:class:`~ksdft2effmass.workflows.WorkflowRunSerializer`, with initial independent
wire evidence. Structural transaction validation and a bounded independent closed
history fixture are also implemented. The atomic repository and deterministic
historical receipt recovery now have real-SQLite and independent literal receipt
evidence. Durable entry has bounded local race, acknowledgement-loss and crash
checks. Rich CPN, authority/dispatch, Task/decision, nested/provenance and Task-model
variants have bounded independent evidence, supplemented by closed-history
repository and replay cases. This is not exhaustive aggregate verification; codec
or entry tests alone do not establish history closure. The separate
application-composition Task is not completed by this minimal codec.

Scalar wire version one
-----------------------

Use the public codec directly or pass it explicitly through the structural port::

    from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
    from ksdft2effmass.workflows import WorkflowResultValueCodec

    codec: WorkflowResultValueCodec = QuantityOfInterestResultValueSerializer()

``encode(value)`` returns exactly ``encoded``, ``incompatible``, ``invalid`` or
``error``. Only ``encoded`` contains an envelope. ``decode(envelope)`` returns exactly
``decoded``, ``incompatible``, ``corrupt`` or ``error``; only ``decoded`` contains a
concrete result. Wrong direct Python semantic types raise ``TypeError``; wrong
intrinsic field values raise ``ValueError``. Operation failures carry sanitized
implementation/version, phase, stable code, input identities, expected/observed
conditions, diagnostic and claim boundary, never a partial reconstructed value.

The scalar payload is canonical ASCII JSON with schema ``qoi-result-value:1`` in the
envelope. JSON members are sorted, separators compact and there is no newline.
Every record uses exactly ``type`` and ``fields``. Nominal identities and enum values
retain explicit type tags and a ``value`` field. The complete scalar definition,
ordered observation requirements, optional state-space identity, unit, evaluator
and source-result correlations are retained. Unknown evaluator labels remain data;
no implementation is loaded or claimed executable.

Finite built-in floats use a tagged ``float.hex()`` string, preserving binary64 and
signed zero exactly. No numerical precision, unit or tolerance is changed. The
Python scalar constructor continues to reject integers, booleans, numeric strings,
NaN and infinities. Wire hexadecimal strings are an explicit representation grammar,
not permission for Python numeric-string inputs. Raw JSON numeric tokens,
duplicate/extra/missing members, wrong nominal tags, noncanonical bytes and invalid
reconstructed fields are corrupt. Allocation/recursion and other operational failures
are represented as errors without arbitrary exception text.

The scalar content identity is ``qoi-result-value:1:sha256:<digest>`` over the complete
canonical payload. :class:`~ksdft2effmass.workflows.WorkflowEncodedResultValue`
retains exact result/type/domain/schema/content metadata and a separate lowercase
SHA-256 digest binding the immutable bytes. Empty or unsupported payloads can be
intrinsically byte-bound without being valid concrete results; only the codec can
establish complete reconstruction. Owning opaque historical content labels in other
domains must not be assumed to use this digest algorithm. Equal logical identities
do not imply equal content; the aggregate serializer rejects conflicting complete
occurrences of one result identity.

Workflow wire version one
-------------------------

``WorkflowResultValueSerializer(source_codec=...)`` owns ``workflow-result:1``.
The injected port is effect-free and operationally immutable; the application
supplies the actual QE codec rather than an anonymous source adapter. Workflow
imports no outward calculator or analysis implementation. Protocol membership alone
is not a claim of exact concrete support.

Decisions include all eleven fields and all nine decision-producer fields, including
verbatim Unicode response and whitespace, optional boundary receipt, predecessor
and supersession, source/authority identities and recorder version labels. Those
labels remain represented data, not executable discovery or authentication. The
owning opaque content label is retained inside the payload and compared with the
envelope, not reinterpreted as a computed hash. Distinct responses may carry equal
opaque labels; their exact payload digests still differ.

Sets retain their identity and nonempty ordered sources without lexical reordering.
Each source is a complete ``WorkflowEncodedResultValue`` record with all seven fields:
result/type/domain/schema/content identities, exact bytes and digest. The payload
field uses a ``bytes`` tag with strict canonical base64. Metadata retains its nominal
tags; no identity table replaces complete occurrences. The set content identity is
``workflow-result:1:sha256:<digest>`` over complete canonical bytes.

The source owner reconstructs concrete parser/document/policy types and delegates
unchanged neutral schema-1 text, precision, units, provenance and tolerance. Workflow
rechecks source membership and neutral provenance through the set constructor and
requires source decode/re-encode agreement on every envelope field. Source failures
retain their complete owning diagnostics; incompatible and error statuses propagate,
while invalid source encoding maps to corrupt during decoding. No partial set is
returned. Known malformed grammar, duplicate/missing/extra fields, noncanonical
base64 or JSON, detached metadata and constructor violations are corrupt. Unknown
nested schemas are incompatible even when the outer schema is supported.

Independent fixed decision and two-source wires, actual seven-family application
routing, nested/standalone envelope agreement and equal-ID/different-content cases
provide software representation evidence. Cross-occurrence conflict rejection
throughout a complete run belongs to the implemented aggregate serializer;
these value codecs neither cache identities nor have a multi-run history context.

Complete aggregate wire version one
-----------------------------------

``WorkflowRunSerializer(result_codec=...)`` accepts the explicit outward port;
application composition supplies the seven-family codec documented in
:doc:`../api/application`. It uses literal constructor and field branches for every
closed reachable Workflow/CPN record, including complete firing input definitions,
recursive expressions, audits, authority state, dispatch, decision and provenance.
Scientific results at every occurrence are complete injected-codec envelopes, not
identity-only table references. Runtime bundles and replay results are not separate
wire roots; retained complete firing inputs are included within run history.

The root is exactly ``schema``, ``run`` and ``commit_binding``. Schema is
``ksdft2effmass.workflow-run:1``. The binding contains exactly transaction,
commit-idempotency and historical persistence-implementation labels; the recognized
writer is ``ksdft2effmass.workflows.WorkflowRunAtomicRepository:1``. Unknown aggregate,
writer, record and concrete versions are incompatible. The writer label records
represented consistency only, not authentication or proof of a historical process.

Canonical encoding is sorted, compact ASCII JSON without a newline. Declared
record fields include null/default and derived-identity fields, with one exact
aggregate exception: when both ``nested_invocation_intents`` and
``nested_terminal_observations`` are empty, both fields are omitted. If either is
nonempty, both fields are required. This preserves the original 34-field wire and
permits only the specified 36-field extension, not a second canonical spelling.
Nominal identities/enums retain explicit tags. Tuples retain order and multiplicity. Exact
built-in integers use tagged canonical ``hex`` strings without a decimal conversion
size limit; Boolean values are never coerced into integer fields. Finite built-in
floats use tagged ``float.hex()`` preserving binary64 signed zero. Exact bytes use
strict canonical base64. Aware UTC datetimes use tagged ISO-8601 text with six
fractional digits and ``+00:00``. These wire string encodings do not widen the owning
Python numeric API contracts or alter their units, tolerances or precision.

``serialize(run, binding)`` checks supported versions, every occurrence and owning
constructor reconstruction, then exact re-encoding before returning encoded bytes.
``deserialize(payload)`` rejects duplicate/extra/missing members, raw JSON numbers,
non-ASCII or noncanonical bytes and wrong known variants. It reconstructs owning
constructors, compares constructor-derived selection/directive identities and
requires exact re-encoding. Wrong direct Python argument types raise ``TypeError``;
known malformed representations return corrupt and invalid candidates return invalid.
Allocation/recursion and operational failures return sanitized error evidence. Only
successful results contain complete bytes or complete run/binding; failures never
contain partial aggregates. Failure evidence retains available run/revision/transaction
identities or the input byte digest; nested codec diagnostics remain with their owner.

Each operation uses its own local envelope-agreement map. Repeated result identities
must agree in complete type/domain/schema/content/digest/payload, including sources
nested inside normalized sets and results occurring in activation inputs, outcomes
and dispatch observations. Result references must match their concrete envelope
metadata. The map stores no constructor or implementation and survives no operation:
it is neither a registry nor a hidden mutable cache.

Independent genesis and nonempty wires cover exact root binding, scalar repetition,
large integer gate priorities, Unicode text, signed zero and anonymous token
multiplicity. Additional fixed aggregate wires cover all seven concrete families at
reference and outcome occurrences, with independently constructed field expectations,
concrete-schema incompatibility, detached reference metadata and nested-source content
conflicts. Retained firing-input fixtures cover all four selection outcomes and both
constructor-derived identities, including rejection of consistently copied incorrect
identity labels. These are representation fixtures, not structurally closed histories.

Two additional independent rich CPN literals and direct public constructors cover
recursive Boolean guards, every comparison-operator label, literal and variable
expressions, all three input-inscription modes, output templates, nonempty external
bindings, occurrence/inhibitor/output audits, and nested enablement failure with
complete validation issues and claim boundaries. Malformed guard arity, negative
audit ordinals and Boolean tagged integers are rejected without partial runs. These
fixtures deliberately do not establish firing-input consistency or computed firing.

Independent authority literals now cover both authorization phases, every grant
state and authorization outcome, independently varied snapshot checks, and exact
UTC microseconds at year boundaries and on a leap day. Alternate timestamp
spellings, invalid intervals and detached authorization identities are rejected.
A separate dispatch literal covers all runtime outcome, observation, final outcome
and disposition kinds, including repeated observations, ordered conflicts, empty
indeterminate observations, full scalar values and structured failures with all
three retryability values. Named malformed variants exercise their intrinsic rules.

Two mixed Task/decision literals now retain all attempt states and generic outcome
kinds, retry and child-run links, failure origins, ordinary/dispatched Task transition
correlations, and initial/corrected decisions. Shared transition order is preserved
separately from lexical resolution storage order, including verbatim responses and
no-Task decision producers. Malformed cases reject incomplete correlations, invalid
indexes/versions, invented Task lineage in a decision transition, and invalid
corrections with independently updated payload digests. These representation
fixtures omit activation, production and membership closure; they are not replay
or history-validation oracles.

The same-v1 extension adds ``nested_invocation_intents`` and
``nested_terminal_observations`` as default-empty immutable tuples. Both empty means
both keys are omitted, preserving the original 34-field bytes. Either nonempty
requires both keys in the exact 36-field extension; a single key, unknown field or
explicitly both-empty extension is corrupt. Four independent literal fragments
cover the new intent and three terminal variants. These fragments are representation
inputs, not structurally closed histories.

A terminal observation links through its exact nominal identity to a separate intent
or an actual retained combined pending record; equal strings do not merge those
sources. Child, creation-key and stable-attempt uniqueness spans both source forms.
New intent introduces its membership, activation and STARTED group in the candidate
revision. New terminal evidence requires its intent in the actual predecessor and
introduces the matching terminal attempt/outcome atomically. Historical projection
preserves old records and bindings exactly. No migration or history rewriting occurs.

Real SQLite cases commit intent I, reopen/load I, construct and commit terminal T,
and reopen both after an unrelated extension, for both intent forms and every
terminal kind. The original combined pending record remains pending as immutable
intent history. Exactly one first terminal is allowed, including indeterminate;
this does not add repeated reconciliation or compensation semantics. Synthetic
child replay labels establish no actual child execution or replay truth.

A nested-record literal covers all four invocation kinds, ordinary/nested membership
and the four nullable dependency-endpoint combinations. It retains paired ordered
exports/admission references and supplied child observations. Self-child correlations,
missing terminal evidence, malformed export/input lists and invalid endpoints are
rejected. The synthetic replay identity has the required hexadecimal spelling; it
was not produced by replaying a child.

Six further literals cover every producer variant at the result-reference boundary:
represented Task, represented no-Task decision, external, imported, declared human
and unknown legacy. The Task literal also retains production relations, external
output binding and native-admission fields. Malformed evidence, limitations, nominal
correlations, no-Task field shapes and admission lists are rejected. These records
do not authenticate provenance, read native files or establish historical closure.

A Task-model literal retains all three activation selections, absent/empty gate
sets, both automatic modes, priority ties, noncanonical gate storage order and
ordered concrete inputs. Malformed cases exercise intrinsic gate, input and
selection correlations without computing an automatic selection.

Typed fault-port evidence covers returned invalid/corrupt, incompatible and error
outcomes during initial and counterpart codec checks, including re-encoding of a
reconstructed value. Foreign failure records retain their complete owner, phase,
ordered identities and diagnostic fields. Identity/content disagreement, wrong
response-record types and synthetic recursion errors expose no partial result.
The latter is bounded exception injection, not a measured resource-limit claim.

Independent whole-Task review identified the pending-to-terminal nested-history
gap. The same-v1 correction now has implementation and bounded lifecycle evidence;
independent review confirmed the exercised behavioral repair and requested further
regression and documentation corrections. Their independent recheck found no
remaining blocking findings. Positive prepared/claimed history and recovered receipt records have
bounded evidence; the new literal facets do not establish exhaustive
authority or dispatch history coverage. Successful reconstruction does not establish
structural run closure, replay equality, stored presence, authority or science. No
generic CPN or scientific algorithm is changed.

Intrinsic aggregate boundary records
------------------------------------

``WorkflowEncodedRun`` binds exact immutable bytes to its supplied schema label and
``<schema>:sha256:<digest>`` content identity. Construction does not recognize a
schema or parse a run. ``WorkflowRunEncodeResult`` carries that envelope only for
``encoded``; its other statuses are ``incompatible``, ``invalid`` and ``error``.
``WorkflowRunDecodeResult`` requires both a complete run and binding for ``decoded``;
``incompatible``, ``corrupt`` and ``error`` contain only structured failure evidence.

``WorkflowRunTransaction`` retains one binding, nominal run identity, explicit
predecessor slot (``None`` means genesis), complete candidate and nonempty
schema/content labels. Its transaction and commit-idempotency properties delegate
to the single binding, rather than duplicating independent label fields.
``WorkflowRunSnapshot`` retains the complete run, binding and exact shared revision
including bytes. Cross-record correlation, supported versions, structural history
and candidate-byte agreement belong to the validator and repository, not these
intrinsic containers. Merely constructing one establishes no stored presence.

``WorkflowRunLoadResult`` retains the exact request and complete shared read result
when present, including all variant-specific observations and implementation labels.
Only ``loaded`` carries a snapshot and requires a shared ``found`` result. The other
statuses are exactly ``absent``, ``mismatch``, ``incompatible``, ``corrupt``,
``indeterminate`` and ``error``. Absence requires shared absence evidence. Other
nonsuccesses require a matching shared result or complete domain failure; no partial
snapshot is exposed.

``WorkflowRunWriteResult`` retains its exact transaction, optional complete shared
commit result, optional predecessor-load evidence and domain failure. Only
``committed`` carries a snapshot and immutable claim-receipt tuple, and requires
shared committed evidence. ``conflict`` requires shared conflict evidence;
``indeterminate`` and ``error`` imply neither presence nor absence. ``invalid`` and
``incompatible`` are pre-store rejections and prohibit a shared commit result.
Receipt identities in a tuple must not repeat. Constructing these fields neither
checks an acknowledgement nor derives a historical receipt.

``WorkflowRunClaimLoadResult`` retains the requested claim identity, exact request
and complete shared read result when present. It uses the same seven load statuses.
Only ``loaded`` contains both snapshot and receipt. A rejected claim contains neither
while retaining the full shared read evidence for diagnosis. Missing-claim
classification, exact historical expectations and receipt correlations remain
repository operations. Record tests now retain actual committed and recovered claim
records from isolated SQLite lifecycles, including duplicate receipt identities and
success/failure tuple closure. Independent repository tests own derivation correctness.

All these records reject wrong semantic types with ``TypeError`` and invalid
intrinsic values/variants with ``ValueError``. Frozen fields and immutable nested
records preserve operational immutability. Record tests remain intrinsic. The same
independently authored genesis bytes now also serve as an initial serializer oracle,
not the exhaustive rich version-one wire/field evidence.

Structural transaction validation
----------------------------------

``WorkflowRunTransactionValidator(serializer=...)`` receives the explicit immutable
serializer and exposes ``execute(transaction, predecessor=None)``. Genesis requires
no predecessor; every successor requires its exact expected historical snapshot,
not the current head. The validator checks the transaction/run/predecessor slots,
supported schema/writer, exact serialized schema/content labels and candidate bytes.
The predecessor's run, binding, stream/revision/predecessor envelope and complete
serialized bytes must agree. A snapshot constructor alone provides no such evidence.

The shared private structural owner resides in ``workflows/runs/replay.py`` and is
used by both this validator and the existing replayer. It owns retained Task,
attempt, outcome, membership, dependency, result, nested, decision, authority and
dispatch correlations, contiguous zero-based transition order, invocation-selection
links and the retained predecessor/successor marking chain. Complete equal-identity
result values are checked by the codec; structural result links compare identities
and metadata rather than NumPy-backed dataclass values. Historical authorization
recomputation and concrete replay comparisons remain with the replayer, not the
structural owner. The validator never enables, selects, fires or authorizes.

Historical records must remain byte-equivalent under the explicit codec. Canonically
sorted collections extend by identity (authority references by grant identity), not
by tuple prefix; attempts and transitions retain their original sequence prefixes.
Initial marking and Workflow/definition/runtime/schema/adapter identities cannot
drift. An explicitly constructed historical projection selects old identities from
the candidate and is serialized with the predecessor binding for exact byte
comparison. No dataclass equality on scientific arrays supplies this oracle.

Each newly introduced dispatch entry must name the transaction's actual non-null
predecessor and candidate revision. Genesis entries are invalid. Historical entries
retain their original revision labels; a later successor does not rebind them.
Public-validator and real-SQLite repository regressions cover detached committed
revisions, stale predecessors and genesis rejection. Repository rejection yields
no snapshot or receipt and no shared-store submission. Positive cases preserve
historical entry bytes and allow exact original-transaction replay after a later
head. These checks do not grant effect-entry permission.

``WorkflowRunValidationResult`` is frozen and bound to the exact transaction and
predecessor inputs. Only ``valid`` contains the exact validated encoded candidate;
``invalid``, ``incompatible`` and ``error`` contain structured failure and no partial
bytes. Codec failures retain their owning diagnostics. Unexpected operational
failures are sanitized, and wrong direct Python semantic types raise ``TypeError``.

A fixed independently authored one-invocation history and named mutations verify
these seams. Separate array-backed predecessor instances exercise codec-byte
comparison. These are bounded structural software tests, not all history/authority/
dispatch variants. A structurally closed run may have a replay-unequal current
marking or unverified firing audit. Only external computed replay can establish
replay equality. Neither validation nor a supplied predecessor establishes stored
presence, recovered claim receipts, advancement permission or effect entry.

Durable binding is not receipt evidence
----------------------------------------

:class:`~ksdft2effmass.workflows.WorkflowRunCommitBinding` preserves the explicit
transaction label, commit-idempotency key and historical persistence implementation
label. This record neither persists those fields nor derives a receipt. The
implemented complete aggregate serializer includes them under ``commit_binding``
and binds them to its canonical content digest, without performing a store commit. The selected version-one writer is
``ksdft2effmass.workflows.WorkflowRunAtomicRepository:1``. Unknown historical writer
versions must remain incompatible, not be replaced with the current reader identity.

The implemented historical claim algorithm requires an explicit revision and the complete
predecessor/schema/content/idempotency expectation group, matched by the shared
store and the decoded binding. An ordinary load observes a payload key; it cannot
claim confirmation of the actual stored key. Deterministic historical receipt
identities depend on the persisted transaction/writer/key, verified revision envelope
and exact claim/authorization identities, not fresh store result UUIDs.

``WorkflowRunAtomicRepository`` receives explicit ``store``, ``serializer`` and
``validator`` dependencies; the validator must bind that same serializer instance.
Wrong dependency or direct operation argument types raise ``TypeError``; detached
serializer binding raises ``ValueError``. It chooses no database implicitly.

``load(request)`` issues exactly one store read. It checks returned request, stream,
selector and explicit address, complete expectation confirmation when requested,
envelope schema and payload digest, decoded run/revision/predecessor/key binding,
and structural closure. Unsupported schemas/writers remain incompatible; corrupt
bytes or closure remain corrupt; missing confirmation or substituted responses are
represented errors. Every available complete shared result is preserved, not reduced
to a diagnostic string. Latest and explicit ordinary reads do not assert that the
payload's key was compared with the actual stored key.

``commit(transaction)`` explicitly loads the exact expected predecessor, not latest,
and validates that same transaction and candidate against it. Genesis has no
predecessor read. Absent/mismatched/corrupt predecessors give invalid; incompatible,
indeterminate and error retain their meaning and complete predecessor-load evidence.
Validation and serialization failures cause zero commits. Exact validated bytes,
schema/content and candidate/key binding are checked again before one shared Commit.
Only an exactly matched acknowledged candidate/key produces a snapshot. Shared
conflict, indeterminate and error are preserved; substituted acknowledgements or
exceptions return error with no snapshot or receipts. No Commit is retried implicitly.

New CLAIMED records, relative to the candidate's exact predecessor, must name the
candidate revision and predecessor. Acknowledged writes derive only those receipts.
Exact idempotent replay uses the original predecessor even after a later head and
reconstructs the same receipts; the shared store decides replay versus collision.
A later revision retaining an older claim emits no new receipt for that old event.

``load_claim(request, claimed_reservation_identity)`` rejects latest/incomplete
requests before a store read. One ordinary load must then return correlated FOUND
with ``expectations_matched is True``. Its persisted key must equal the confirmed
stored key. A missing selected claim is mismatch; a non-CLAIMED or copied historical
claim naming a different revision is corrupt. The selected record's run, revision,
predecessor, reservation and authorized claim-phase result must close exactly.
No authorization is reevaluated. The same receipt derivation serves writes and reads.

For the exact derivations, let ``J`` denote ASCII bytes of compact JSON sequences of
strings/null, with ``ensure_ascii=True``, ``allow_nan=False`` and no newline. Let
``B`` be the verified persisted binding and ``R`` the verified revision. Then::

    operation = "wfr-operation-v1:sha256:" + sha256(J([
        "wfr-operation-v1", B.transaction_identity,
        B.persistence_implementation_identity, R.stream_id, R.revision_id,
        R.predecessor_revision_id, R.schema_id, R.content_id,
        B.commit_idempotency_identity])).hexdigest()
    receipt_identity = "wfr-claim-receipt-v1:sha256:" + sha256(J([
        "wfr-claim-receipt-v1", operation, claim.identity.value,
        claim.authorization_result_identity.value])).hexdigest()

The receipt retains nominal stream/revision/predecessor identities from ``R``, claim
and authorization-result identities from the selected record, ``R.content_id``, and
``B``'s confirmed key and historical writer label. No digest is recursively embedded
in its own payload. Changed transaction labels change bytes/content and cannot alias
the same exact generic Commit. Digests and labels are consistency, not authentication.

If a claim acknowledgement is lost, restart requires no transaction object. When
receipt expectations are known, use the complete explicit claim read directly. When
they are lost too, the service may first observe the explicitly addressed historical
revision through ordinary load, then make a separate complete-expectation claim read.
The repository never hides this second read. Later heads do not prevent historical
reconciliation, but copied claims cannot yield receipts for those later revisions.
These observations never grant advancement or effect entry.

Durable entry permission
------------------------

``WorkflowRunDispatchEntryCommitter`` is the separate Workflow-owned service that
implements ``SimulationDispatchEntryCommitter``. It receives an explicit structural
``WorkflowRunRepository``, the exact ``WorkflowRunSerializer`` supplied to that
repository and its validator, and one immutable ``WorkflowRuntimeBundle``. It does
not inspect private repository configuration or select a codec, database or executor.

``execute(request)`` requires an exact ``SimulationDispatchRequest``; wrong direct
input or dependency types raise ``TypeError``. The operation performs these gates:

1. Reconcile the explicit historical claim using all predecessor, schema, content
   and commit-key expectations. Compare every supplied receipt field, the returned
   request/shared evidence and complete snapshot binding. The retained request,
   obligation, claimed reservation and authorization records must agree.
2. Read latest separately and verify the complete snapshot bytes, binding and
   returned request/envelope. A matching existing entry yields ``already_entered``
   without a receipt. Otherwise latest must equal the reconciled historical claim,
   and the owning replayer must return ``equal`` for that exact snapshot.
3. Append one entry with fresh invocation-local UUID4 receipt, transaction and
   commit-key identities. Preserve the marking and require candidate replay equal.
   Submit that exact encoded candidate once against its predecessor.
4. Only an exact acknowledged candidate, snapshot, binding, bytes and commit key
   produce ``entered`` with a ``SimulationDispatchEntryReceipt``. A conflict may
   trigger a read solely to distinguish ``already_entered`` from ``error``; it
   cannot recover permission. Other failures and lost or substituted acknowledgements
   yield ``error`` with sanitized diagnostics and no receipt or commit retry.

All non-entered results carry diagnostics rather than a receipt. Each call has its
own candidate identity; generic exact-commit replay is never permission for another
invocation. Collision-resistant UUID generation and a conforming atomic repository
are assumptions, not authentication or mathematical uniqueness guarantees.

The service writes the entry record but never executes the external effect.
``SimulationDispatchAdapter`` separately repeats claim authorization before calling
this port and invokes its explicit effect only for the newly entered result. A crash
between entry commitment and effect invocation may leave execution unresolved; no
exactly-once completion is promised. Repository loading remains structural validation,
not repository-owned replay or authority.

Synthetic tests cover independent instances and processes contending on one
predecessor, reopen/repeat, stale or forged receipts, detached historical/current
reads, substituted or lost acknowledgements and process termination before the fake
effect. A successful bounded race is not exhaustive concurrency or hardware-failure
verification.

Evidence limits
---------------

The maintained fixtures are synthetic software test data, not calculated physical
values. Current checks cover seven-family wire reconstruction, minimal application
codec composition, intrinsic record behavior, bounded structural extension and the
implemented repository's historical commitment/reconciliation seams. The entry
service has bounded synthetic software evidence within the completed persistence
Task, not exhaustive concurrency or hardware-failure verification.
No codec executes scientific tools or reads/copies native artifacts. Digests establish
represented consistency, not authentication, numerical verification, scientific
validation, uncertainty quantification or human acceptance. Scientific and
Harness databases must remain separately composed under their owning contracts;
the repository selects no database; real store creation occurs only through its
explicitly supplied shared-store dependency.
