Quantum ESPRESSO Workflow simulations
=====================================

``ksdft2effmass.simulations.quantumespresso`` owns project-specific Workflow
simulation composition above the generic Workflow and QE-native integration
boundaries. It owns manifest-driven project composition and one-attempt ordering,
but not Quantum ESPRESSO input semantics, native staging or process implementation,
authority issuance, retry policy, diagnostic interpretation, or scientific acceptance.

The immutable
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoBundledExampleRunIdentity`
represents one exact bundled-example Task identity, upstream QE release, and
explicit whole-second UTC workspace-creation time. Its portable identity is
``TASK-ID.vMAJOR-MINOR[-PATCH].YYYYMMDDTHHMMSSZ``. The corresponding relative
workspace is
``simulations/quantumespresso/qe_examples/COMPONENT/EXAMPLE/vMAJOR-MINOR[-PATCH]/YYYYMMDDTHHMMSSZ``.

The object performs no clock or filesystem access. It neither creates the derived
path nor authorizes a run. Executable hashes, inputs, pseudopotentials, scientific
settings, resources, grants, and attempt provenance remain separate manifest data.
Existing-path rejection remains with the local execution preparation boundary.

The public execution surface is deliberately limited to
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoExecutionRequest`,
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoPlanner`, and
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoExecution`.
The request names the exact dated schema-v2 JSON contract
``quantum-espresso-execution-manifest:v2.20260921T155105Z``. The integer
``schema_version`` remains ``2`` while ``schema_identity`` closes the accepted dated
revision. In addition to run, source, destination, resource, environment, and
correlation values, the manifest identifies the exact native-output extraction
candidates and every identity needed to construct an inert
:class:`~ksdft2effmass.integration.quantum_espresso.LocalQuantumEspressoExecutionPlan`.
The manifest identifies
one canonical development decision as evidence and one generic
:class:`~ksdft2effmass.workflows.ScientificExecutionAuthorityReference` containing
the externally issued grant revision, authority snapshot, and grant-state identities.
The decision ID is not a grant, and manifest decoding neither issues nor authenticates
the referenced authority. Planning is effect-free, and direct execution is
fail-closed. An internal application composition binds the generic persisted
reservation-to-claim-to-dispatch Workflow to the exact
:class:`~ksdft2effmass.integration.quantum_espresso.LocalQuantumEspressoExecutor`
effect port. It requires acknowledged reservation and claim commits, immediate
claim-phase reauthorization, and a newly won durable dispatch entry before effect
invocation. An internal effect-free assembler can now load one exact persisted
predecessor, require replay equality, and combine a separately supplied Task activation
and unused/reserved authority views with the manifest-derived local plan into the
lifecycle request. It neither derives authority from the manifest nor commits or
executes the assembled request. A second internal effect-free assembler composes the
complete native local executor only from that exact plan and an explicitly supplied,
matching version-bound diagnostic catalog. A protected typed application Workflow
connects both assemblies to the persisted reservation, claim, immediate
reauthorization, and dispatch-entry lifecycle. Its optional read-only ``preflight``
replays and correlates persisted state, evaluates both supplied authority views, and
constructs the executor in memory without committing or entering an effect. A ready
preflight is neither a grant nor a promise that the later execution call will win its
current authorization and persistence boundaries. The Workflow performs no dependency
discovery, grant issuance, fallback, or retry. The manifest CLI does not yet supply the external
activation/authority inputs or select a repository, so its non-plan mode remains
blocked. Software verification exercises the persisted control sequence, local
executor, confirmed reconciliation, immutable QE result and native-output admission,
obligation disposition, generic CPN result firing, and replay-equal terminal successor
commit with a deterministic fixture only. It is not a QE calculation or
production-authority claim. No example or scientific setting creates another public
Python type.

The
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoPseudopotentialAdapter`
binds a backend-neutral catalog entry only when it carries the selected UPF2 native
format. The resulting reference retains the source-entry identity, independent UPF2
SHA-256, filename, and content-addressed location. Format admission performs no byte
verification, QE parser smoke test, staging, execution, cross-format numerical
comparison, or scientific acceptance.

The
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoOpenBlasComparatorBuildPlanner`
binds the proposed QE 7.2 release-like MPI/OpenBLAS comparator to the generic
:mod:`ksdft2effmass.toolchains` planning contract. Given separate explicit absolute
``~/opt`` and ``~/build`` roots, it represents platform-qualified flat package
prefixes, separate runtime-toolchain and artifact-build fingerprints, a build-qualified
QE install prefix, isolated scratch, a profile-qualified modulefile view, and
deterministic CMake argument vectors. Digest-prefix lengths are explicit and may range
from 12 through 64 characters. It does not inspect or create those paths, publish a
modulefile, run a build, adopt a dependency, amend the existing checkpoint recipe, or
grant the pending protected-execution decision.

Run identity, pseudopotential binding, workspace mapping, and toolchain recipe
--------------------------------------------------------------------------------

.. automodule:: ksdft2effmass.simulations.quantumespresso
   :members:
   :imported-members:
