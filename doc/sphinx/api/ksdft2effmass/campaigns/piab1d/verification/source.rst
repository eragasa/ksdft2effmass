PIAB1D source authentication
============================

``Piab1dSourceAuthenticator`` checks the file identities recorded in a result's
``provenance`` object. It reads the declared input, runner, implementation files, and
any explicitly supplied parent result; resolves each path below a caller-supplied
repository root; and compares SHA-256 digests.

Identity fields
---------------

Each :class:`Piab1dSourceIdentity` contains:

``role``
   ``INPUT``, ``RUNNER``, ``IMPLEMENTATION``, or ``RETAINED_RESULT``.
``relative_path``
   A normalized relative POSIX path. Absolute paths, ``..`` components, and
   noncanonical spellings are rejected.
``recorded_sha256``
   Exactly 64 lowercase hexadecimal characters.

Current result formats can list implementation identities. Their paths must match the
verifier's declared implementation inventory as a set. Older retained results omit the
implementation list. For those results, a verifier can supply the recorded historical
runner digest. The resulting disposition is named
``RECOGNIZED_HISTORICAL_IDENTITY`` rather than a current-content match.

Outcomes
--------

``MATCHED_REPOSITORY_CONTENT``
   The resolved file exists and its SHA-256 digest equals the recorded digest.
``RECOGNIZED_HISTORICAL_IDENTITY``
   The recorded runner digest equals the verifier's historical runner digest.
``CONTENT_MISMATCH``
   The file exists but its digest differs.
``SOURCE_MISSING``
   The resolved path is not a regular file.

:attr:`Piab1dSourceAuthenticationResult.passes` is true when every file check passes
and the implementation path sets agree. No floating-point tolerance is involved.

Usage
-----

Verifiers pass the decoded ``provenance`` mapping directly to the authenticator:

.. code-block:: python

   source = Piab1dSourceAuthenticator().execute(
       provenance,
       repository_root,
       expected_implementation_paths,
       historical_runner_sha256,
   )

An identifiability result also supplies its retained parent result as an
``additional_identities`` entry. The authenticator does not inspect numerical payloads.

Implementation and evidence
---------------------------

The implementation is
``python/src/ksdft2effmass/campaigns/piab1d/verification/source.py``. Tests are under
``python/tests/software_verification/ksdft2effmass/campaigns/piab1d/``. Retained
provenance is under ``calculations/research-monograph/particle-in-box/``.

A digest match proves byte identity with the declared file. It does not prove that the
file produced the result or that the numerical result is correct; those are separate
questions.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.source

.. autoclass:: Piab1dSourceIdentityRole
   :members:

.. autoclass:: Piab1dSourceIdentityDisposition
   :members:

.. autoclass:: Piab1dSourceIdentity
   :members:

.. autoclass:: Piab1dSourceIdentityVerificationResult
   :members:

.. autoclass:: Piab1dSourceAuthenticationResult
   :members:

.. autoclass:: Piab1dSourceAuthenticator
   :members:
