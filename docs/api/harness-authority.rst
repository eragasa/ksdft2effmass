Development decisions and optional authority
============================================

The development Harness preserves human input in immutable
``DevelopmentDecision`` values.  A decision records evidence and provenance; it does
not grant authority.  ``DevelopmentDecisionSerializer`` emits and accepts only the
version-2 sorted-key compact UTF-8 Harness JSON profile with one final line feed.
Ordered ``DevelopmentDecisionAuthoritativeReference`` values distinguish repository
paths from HTTPS URIs. Legacy checkpoint adaptation is one-way and records the exact
source hash and byte count. It strips trailing slashes from repository directory record
paths and omits absolute external authority and record paths; it does not embed the
legacy bytes or invent an available legacy authority identity.

Each exact configured Task revision has a signature requirement.  An absent
configuration resolves to ``not_required`` without importing cryptographic code.  An
explicit ``required`` value invokes the optional signed-ledger verifier.  If the
``authority-signatures`` extra is unavailable, signed reconstruction fails closed; it
never installs a package dynamically or falls back to unsigned mode.

Signed authority uses only public Ed25519 keys, bounded explicitly supplied canonical
envelope bytes, a separately authenticated anti-rollback pin, exact issuer thresholds,
append-only snapshot and record chains, and exact operation bindings.  This API has no
private-key, signing, discovery, network, credential, persistence, reservation, or
target-effect capability.  ``signature_not_required`` means only that the exact Task
revision did not request this optional gate and is not an authority claim.  Target
operations must still enforce all other applicable human and protected-action rules.
Signed authorization consumes the complete successful
``DevelopmentAuthorityContextResolutionResult``.  The authorizer rechecks the receipt
and context identities, their shared reconstruction fields, and the complete record
chain.  The context carries the head snapshot's predecessor and ordinal bounds so the
authorizer can reconstruct its canonical payload and require the verified receipt's
head-payload identity.  A caller-assembled, record-modified, or reidentified context
fails closed.

API reference
-------------

.. currentmodule:: ksdft2effmass.harness

.. autoclass:: DevelopmentDecision
.. autoclass:: DevelopmentDecisionAuthoritativeReference
.. autoclass:: DevelopmentDecisionOption
.. autoclass:: DevelopmentDecisionSourceProvenance
.. autoclass:: DevelopmentDecisionSerializer
   :members:
.. autoclass:: DevelopmentTaskSignatureConfiguration
.. autoclass:: DevelopmentTaskSignatureRequirementResult
.. autoclass:: DevelopmentTaskSignatureRequirementResolver
   :members:
.. autoclass:: DevelopmentTrustAnchor
.. autoclass:: DevelopmentIssuerAnchorBinding
.. autoclass:: DevelopmentTrustConfiguration
.. autoclass:: DevelopmentTrustConfigurationPin
.. autoclass:: DevelopmentAuthoritySnapshotSource
.. autoclass:: DevelopmentAuthorityLedgerSnapshot
   :members:
.. autoclass:: DevelopmentSignedAuthoritySnapshot
   :members:
.. autoclass:: DevelopmentAuthorityContextResolver
   :members:
.. autoclass:: DevelopmentAuthorityContext
.. autoclass:: DevelopmentOperationAuthorizationInput
.. autoclass:: DevelopmentOperationAuthorizationResult
.. autoclass:: DevelopmentOperationAuthorizer
   :members:
