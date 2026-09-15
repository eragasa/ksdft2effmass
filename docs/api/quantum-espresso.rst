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
only, not numerical convergence or scientific acceptance.  DOS and a separate
public Simulation composite remain deferred.

The local boundary provides read-only preparation, identity-rechecked no-replace
input and private-executable staging, bounded deterministic workspace snapshots with
private atomic snapshot records, one-attempt local process entry with distinct exact
stdout and stderr capture, explicit native-output candidate collection, and private
terminal-record serialization and atomic publication. The
process runner consumes an already prepared and staged attempt, enters at most one
process, and returns either a closed mechanical observation or a typed integration
failure. The outcome resolver applies fail-closed compatibility and precedence rules
to closed process, diagnostic, and native-output records.
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

Input and local-execution contracts
-----------------------------------

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
