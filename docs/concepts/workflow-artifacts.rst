Workflow-owned artifacts and provenance
=======================================

The :mod:`ksdft2effmass.workflows` artifact contract records which immutable
artifacts a Workflow knows about and the exact evidence boundary for each
artifact's producer.  These records are calculator-independent.  They do not
open files, compute checksums, resolve storage, execute Tasks, persist records,
or interpret scientific content.

Artifact and content identity
-----------------------------

``ArtifactIdentity`` is the Workflow owner's nominal identity for an artifact.
``ArtifactContentIdentity`` separately records an already-observed SHA-256 digest
and unsigned 64-bit byte count.  The initial public contract fixes the algorithm
to ``sha256``; algorithm agility remains deferred.

Construction checks represented values only.  It does not claim that bytes are
available, that a digest was independently observed, or that the native format
is valid.

Closed producer provenance
--------------------------

Every ``ArtifactManifestEntry`` contains exactly one concrete producer record.
The mandatory ``ArtifactProducerKind`` and the concrete Python type agree.  The
closed variants are:

``RepresentedWorkflowProducer``
   Retains exact Workflow, Workflow-run, Task-instance, Task-activation, attempt,
   ResultObject, and nominal result--artifact relation identities.

``ExternalSourceObservation``
   Retains the authoritative external producer/attempt, upstream artifact and/or
   result, source observation, method, receipt, optional known revision/time,
   explicit limitations, and a reason represented Workflow context is unavailable.

``ImportedRetainedFixture``
   Retains fixture/source/import identities and the source's separate content,
   checksum, provenance, and evidence classification without upgrading them.

``HumanAuthoredCompactInput``
   Retains compact-input revision, author, authority, optional source/review, and
   authorship-record identities.  Authorship is not execution provenance.

``UnknownLegacyProducer``
   Retains every known evidence identity while stating why producer information
   is unavailable, its limitations, and bounded claim status.  It never fabricates
   Workflow identities.

Separate classes prevent inapplicable fields from being populated on the wrong
producer kind.  Evidence and claim-boundary identity tuples are required,
immutable, unique, and lexically ordered.  These identifiers preserve joins;
they do not by themselves prove that referenced records exist or that their
claims are true.

Manifest closure and correction
-------------------------------

An ``ArtifactManifestEntry`` has its own exact identity for downstream
references.  It records native format, semantic role, retention, parent
artifacts, an optional portable relative store reference, closed lineage
relations, and producer provenance.  Absolute, home-relative, parent-traversing,
and platform-native paths are rejected.  Producer artifact/content and lineage
target identities must equal the entry.

``ArtifactLineageRelation`` uses a closed ``ArtifactLineageKind`` for CPN
selection, result production, execution grant and authority snapshot, process
observation, result ingress, native resolution, parsing, normalization, or
analysis.  Represented Workflow outputs require exact CPN-selection and
result-production relations.  When an execution relation is present, grant,
authority-snapshot, process-observation, and result-ingress relations close as
one set.  Later native-resolution, parser, normalization, and analysis relations
can be introduced by a corrected immutable manifest without rewriting earlier
state.

An ``ArtifactManifest`` binds its exact owner Workflow and Workflow-run
identities and is a nonempty, canonically ordered immutable revision.  It rejects
dangling parent artifacts, parent cycles, duplicate entry/artifact identities,
and evidence identities not equal to the complete entry evidence closure.
Revision 1 has no predecessor or supersession relation.  Every later revision
must name both a different predecessor manifest and an exact supersession
identity, so correction creates a new record rather than rewriting prior
provenance.

The constructor establishes manifest-local closure only.  External evidence
existence, byte observation, serialization, persistence, location resolution,
and retention execution belong to other boundaries.  Retention metadata grants
no deletion, transfer, publication, access, or other authority.

Migration boundary
------------------

These Workflow-owned records are deliberately distinct from equal-looking
records exported by :mod:`ksdft2effmass.provenance`.  The latter are retained
transitional v1 contracts.  The two owners are not aliases, and callers must not
substitute one identity class for the other.  Any future migration requires an
explicit adapter and separate compatibility authority.

Evidence boundary
-----------------

Exact content and lineage fields establish only represented-value agreement and
correlation under this software contract.  They do not establish calculator
success, convergence, numerical verification, scientific validation,
uncertainty quantification, physical compatibility, or human acceptance.
