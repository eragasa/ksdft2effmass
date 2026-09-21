Quantum ESPRESSO integration
============================

The canonical :mod:`ksdft2effmass.integration.quantum_espresso` package owns
QE-native input, operation-specific Task, execution, diagnostic, and QEXSD
contracts.  It does not select scientific settings, grant Workflow execution
authority, perform automatic retry, or claim that an emitted input is accepted by a
particular QE version.

The immutable
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoScfTask`,
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoNscfTask`,
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoBandPathTask`, and
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoBandsExtractionTask`
classes represent four distinct reusable scientific operations.  Each retains one
exact
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoExecutionInput`,
uses a fixed Task-definition identity, validates its Workflow and predecessor-state
correlations, and delegates through an explicitly injected backend-neutral
:class:`~ksdft2effmass.calculators.dft.pw.PlaneWaveCalculator`.  SCF has no
predecessor; NSCF requires ``scf_result``; band-path requires
``predecessor_result``; and bands extraction requires ``band_path_result``.  A
downstream predecessor must be a mechanically completed ``pw`` result with exact
native-state manifest lineage.  These conditions establish continuation eligibility
only, not numerical convergence or scientific acceptance.  DOS remains deferred.

The immutable
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoSimulation`
composition binds one of those Tasks, its equal exact execution input, the identical
calculator object already injected into the Task, and a Workflow
:class:`~ksdft2effmass.workflows.SimulationDispatchEffect`.  The implemented
:class:`~ksdft2effmass.integration.quantum_espresso.LocalQuantumEspressoExecutor`
satisfies that effect port.  The composition records the two distinct structural
boundaries and selected immutable result class but does not invoke either boundary,
adapt their call signatures, retain output state, or create execution authority.

The local boundary provides read-only preparation, identity-rechecked no-replace
input and private-executable staging, bounded deterministic workspace snapshots with
private atomic snapshot records, one-attempt local process entry with distinct exact
stdout and stderr capture, explicit native-output candidate collection, and private
terminal-record serialization and atomic publication. The
process runner consumes an already prepared and staged attempt, enters at most one
process, and returns either a closed mechanical observation or a typed integration
failure. The outcome resolver applies fail-closed compatibility and precedence rules
to closed process, diagnostic, and native-output records. Diagnostic catalogs remain
exactly executable-kind, program, and version bound. In addition to the deterministic
fixture, ``qe_pw_7_2_v1`` admits only real QE ``pw`` 7.2, recognizes the exact
``JOB DONE.`` marker, and retains the previously observed IEEE signalling notice as
``unresolved``. Every other nonempty QE 7.2 stderr line also remains unresolved. This
classification is software evidence only; it does not establish convergence,
numerical correctness, scientific validity, or acceptance.
:class:`~ksdft2effmass.integration.quantum_espresso.LocalQuantumEspressoExecutor`
composes these boundaries for one Workflow-entered attempt. It independently checks
the exact run, Task, activation, operation, attempt, executor, destination, resource,
grant, obligation, authorization, and dispatch-entry correlations before staging. A
determinately captured calculator failure remains a confirmed immutable QE
ResultObject; pre-process rejection and post-process integration uncertainty map to
the distinct Workflow dispatch variants. These ActionObjects do not grant execution
authority, classify scientific validity, or retry an operation. The terminal-record
bytes are an integration-private versioned format rather than a public persistence or
cross-language contract. Executable configurations admit only the documented
thread-control environment keys. Aggregate workspace limits are actively observed and
fail closed but are not an operating-system disk quota.

The first stage of QEXSD observation adaptation is
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoObservationAdapter`.
It requires an exact
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoObservationExtractionRequest`
that binds a
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoParsedDocumentRecord`
with exact source-content, parser-implementation, and parser-version correlation to
one admitted Workflow manifest entry, reserved result identity, and explicit supported
normalization policy.
Success returns an integration-owned
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoExtractedObservationResult`
containing the unchanged schema-version-1 neutral plane-wave record and exact source,
producer, parsed-document, parser, policy, and limitation fields. Expected disagreement
returns
:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoObservationAdaptationFailure`
without a partial observation while retaining the reserved result identity and exact
request correlation. Under the human-selected two-stage architecture, this result is
not itself a Workflow ``NormalizedObservationSet``. The Workflow-owned
``NormalizedObservationAssembler`` consumes it through
``NormalizedObservationSource`` without a Workflow import of this integration.

Complete result-value wire
--------------------------

:class:`~ksdft2effmass.integration.quantum_espresso.QuantumEspressoResultValueSerializer`
is the outward, explicitly injected Workflow result codec for exactly
``QuantumEspressoPwResult``, ``QuantumEspressoBandsResult`` and
``QuantumEspressoExtractedObservationResult``. It performs no native-file reads,
process invocation, parsing, normalization, replay or repository operation. This
three-family codec does not complete the WorkflowRun persistence Task.

``qe-result-value:1`` retains every declared field: complete operation input with
native-input, pseudopotential and predecessor-state references; all process
termination, stream, diagnostic, marker and calculator-outcome variants; native
manifest/entry references and terminal identity. These are references, not native
bytes or expanded manifests absent from the source result. Extracted observations
retain source manifest, entry, artifact, content, producer, parsed-document and parser
identities, parser version, policy and all six explicit limitation values. The
parsed-document identity is retained, not an invented or reconstructed native document.

Supported PW/bands result versions are ``qe-pw-result:1`` and ``qe-bands-result:1``;
execution inputs require ``qe-execution-input:1``. The constructor-supported parser
and policy identities require version ``1``. Other observer, classifier and program
labels remain exact provenance data, not dynamically loaded implementations.

Records have exactly ``type`` and ``fields``; nominal identities and enums retain
explicit tags. Integers use tagged canonical signed hexadecimal strings (no bool
coercion); tuples are ordered arrays. Canonical ASCII JSON uses sorted keys, compact
separators and no final newline. Content identity is
``qe-result-value:1:sha256:<digest>`` over the complete payload; the envelope also
binds exact bytes with a separate SHA-256 digest. Type labels are supported public
import names followed by ``:1``; domain is
``ksdft2effmass.integration.quantum_espresso``.

The neutral observation is delegated to
:class:`~ksdft2effmass.ksdft.pw.KohnShamPlaneWaveCalculationRecordJsonSerializer`
as its exact nested schema-1 JSON string, including its newline, units, binary64
values, signed zero, provenance and represented duality tolerance. Each operation
uses a fresh neutral serializer with the unchanged ``1.0e-12`` absolute tolerance;
no mutable serializer dependency is retained. The neutral numeric grammar remains
with that existing owner rather than adopting the QE tagged-integer grammar.

``encode`` returns ``encoded/incompatible/invalid/error``; ``decode`` returns
``decoded/incompatible/corrupt/error``. Only success carries complete data. Wrong
direct Python semantic types raise ``TypeError``. Unsupported exact types or owning
versions are incompatible; malformed known wires, wrong nominal tags, duplicate,
extra or missing members, noncanonical bytes and constructor violations are corrupt
on decode. Invariant failures are invalid on encode; allocation/recursion and other
operational failures are sanitized errors. No arbitrary ResultObject, subclass,
identity-only stand-in, registry or dynamic import is supported. Digest agreement
establishes represented software consistency, not source authentication or scientific
acceptance. See :doc:`../concepts/workflow-run-persistence` for the separate,
currently incomplete aggregate boundary.

Input, local-execution, and observation contracts
-------------------------------------------------

.. automodule:: ksdft2effmass.integration.quantum_espresso
   :members:
   :imported-members:

QEXSD native records and parser
-------------------------------

QEXSD parsing begins only after an independently obtained output artifact exists. The
parser supports only its explicitly documented QEXSD versions and fails closed for
unsupported versions.

.. automodule:: ksdft2effmass.integration.quantum_espresso.qexsd
   :members:
   :imported-members:
   :no-index:

The retained silicon SCF software example is available at
``examples/tutorials/silicon-scf/qe/reconstruct_silicon_scf.py``. It emits the
reconstructed input but invokes no scientific executable. It introduces no provenance schema; the
existing retained calculation record remains authoritative for the earlier QE 7.2
execution.
