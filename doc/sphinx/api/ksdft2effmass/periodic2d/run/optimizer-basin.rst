Periodic2d Wannier90 optimizer-basin encoded documents
======================================================

Purpose and ownership
---------------------

``Periodic2DOptimizerBasinEncodedDocuments`` preserves exact nonempty input and result
wires for a bounded periodic-2D Wannier90 multistart study. It is a frozen, slotted
encoded-wire DataObject, not an initial-gauge model, optimizer, basin classifier,
native-artifact inventory, convergence result, numerical oracle, provenance record, or
acceptance decision.

The owner does not decode, normalize, copy, discover, or infer meaning from either
payload. Gauge construction, native-file authentication, endpoint correlation, basin
classification, independent numerical reconstruction, convergence assessment, and
scientific acceptance remain separate responsibilities.

Verification contract
---------------------

The authoritative architecture page
``docs/architecture/v2/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/verification-contract.md``
classifies every retained field as validated, correlated, preserved but uninterpreted,
or explicitly out of scope. Checks outside that frozen matrix require a reviewed
contract change; they are not routine hygiene.

Scientific boundary
-------------------

The retained study varies smooth reciprocal-periodic unitary initial gauges without
changing the declared rank-three retained subspace. This probes initialization
sensitivity of local Wannier90 optimization separately from subspace selection. It also
varies mesh, cutoff, and auxiliary embedding, which remain distinct numerical effects.
A locally converged endpoint is not proof of a global optimum.

The encoded result records that the observations do not support the frozen
finite-parameter convergence criteria. The byte owner preserves that negative
statement but does not independently verify it. It must not be rewritten as a positive
convergence claim.

Numerical design
----------------

For baseline trial-overlap matrix :math:`A(\mathbf{k})`, each deterministic start uses

.. math::

   A_s(\mathbf{k}) = A(\mathbf{k}) U_s(\mathbf{k}),

where :math:`U_s` is an ordered product of smooth reciprocal-periodic unitary fields.
Therefore :math:`A_s A_s^\dagger = A A^\dagger`: the declared retained subspace and
overlap singular values are unchanged while the initial optimizer trajectory changes.
The eight starts are deterministic probes, not a probability distribution or exhaustive
global search.

Only native-converged endpoints enter the original observed-basin classifier. Two
endpoints share a basin only when their native total spreads agree within
:math:`10^{-8}a^2` and their periodically wrapped, permutation-matched active-plane
center sets agree within :math:`10^{-5}` cell. This is an operational finite quotient,
not proof of distinct mathematical stationary points.

For both the finest mesh and cutoff pairs, the best observed endpoint and the median
across converged starts must simultaneously satisfy one-percent spread, 0.01-cell
center-set, and ten-percent radius-50 hopping-tail gates. The best basin must also have
occupancy at least two at both endpoints. A process exit code remains distinct from the
native Wannier90 convergence statement.

Retained scientific reasoning
-----------------------------

The retained result records 51 native-converged and 21 nonconverged outcomes among 72
completed processes. Every best observed basin has occupancy one. The mesh spread and
center gates fail; the cutoff scalar spread and hopping-tail changes stabilize, but its
center and occupancy gates still fail. Stable scalar objective values therefore do not
establish stable selection of a localized representation.

The negative disposition is bounded: it says this finite design does not support its
predeclared criteria. It does not prove that no limit exists. Mesh sampling, finite
basis, auxiliary embedding, initialization sensitivity, localization behavior, and
postprocessing discretization remain separate effects.

Evidence boundary
-----------------

The retained ``study-input.json`` and ``result.json`` identities are checked separately
by artifact-owned integration evidence against maintained ``SHA256SUMS`` entries. The
portable verifier uses the shared strict JSON decoder, rejecting duplicate object keys,
nonstandard nonfinite constants, invalid UTF-8, and non-object roots before
schema-specific reconstruction. It correlates campaign identity, authority, bounded
claim text, and distinct input/result evidence roles; checks declaration and result
identity uniqueness before building lookup dictionaries; and requires exactly eight
unique endpoint gauge identities per configuration. It rejects duplicate nonconverged
identifiers and requires the
complete copied best endpoint to match the minimum-native-spread converged endpoint
recursively with exact JSON representations, and confines each resolved compact-source
path to the explicit repository root before reading it; applies the shared strict
SHA-256 contract to provenance identities; and preserves observed-only, non-global, and
process-completion flags. Study axes are correlated explicitly; ordered finest-pair
identities are derived from axes and declared controls rather than names; and each
embedding summary's four selected fields must match the corresponding configuration
fields. The exact negative disposition
and joint best-and-median requirement are retained. The immutable verification Result
separately requires exact Boolean flags, nonnegative exact integer counts, and lowercase
SHA-256 syntax. Direct
construction validates only intrinsic state and does not prove verifier execution.
Content identity does not
establish native-file presence, execution provenance, completed localization, valid
basin classification, convergence, global optimality, decoded correctness, scientific
validation, uncertainty quantification, or acceptance.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.optimizer_basin

.. autoclass:: Periodic2DOptimizerBasinEncodedDocuments
   :members:

Optimizer convergence-regression encoded documents
==================================================

``Periodic2DOptimizerRegressionEncodedDocuments`` preserves exact standalone-result,
analyzer-source, and regression-result bytes. The encoded owner assigns no convergence,
causality, population, physical-uncertainty, validation, or acceptance meaning.

The request-scoped verifier authenticates compact repository sources and independently
reconstructs the retained finite right-censored log-normal diagnostics. The historical
standalone-result wire contains bare ``Infinity`` tokens only in unconsumed fields; a
bounded campaign-specific adapter rejects duplicate keys and nonfinite consumed fields.
The regression-result wire remains strict JSON.

Passing verification establishes bounded software and numerical consistency only. The
16 deterministic starts are not random population samples, clustered intervals are not
physical uncertainty, and no result proves optimizer convergence or predicts DFT
behavior.

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression

.. autoclass:: Periodic2DOptimizerRegressionEncodedDocuments
   :members:
   :no-index:

.. autoclass:: Periodic2DOptimizerRegressionCampaign
   :members:
   :no-index:

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.verify

.. autoclass:: Periodic2DOptimizerRegressionCampaignVerificationRequest
   :members:

.. autoclass:: Periodic2DOptimizerRegressionCampaignVerificationResult
   :members:

.. autoclass:: Periodic2DOptimizerRegressionCampaignVerifier
   :members:

Standalone optimizer-study encoded documents
============================================

``Periodic2DOptimizerStandaloneEncodedDocuments`` preserves exact proposal,
deterministic-start design, and result bytes. The encoded owner assigns no repository
location, native-execution, convergence, basin, validation, uncertainty, or acceptance
meaning.

The request-scoped verifier authenticates only the compact maintained sources and
reconstructs endpoint transitions, spread algebra, aggregate counts, ordered basin
representatives and members, member/rejection thresholds, start-block presence,
threshold sensitivity, controls, and the retained negative disposition. The historical
result's bare positive ``Infinity`` is confined to the complete indexed paths of two
rejected-comparison extended-real fields. Passing establishes bounded software and
arithmetic consistency only; it does not authenticate native files or prove optimizer
convergence.

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone

.. autoclass:: Periodic2DOptimizerStandaloneEncodedDocuments
   :members:
   :no-index:

.. autoclass:: Periodic2DOptimizerStandaloneCampaign
   :members:
   :no-index:

.. currentmodule:: ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.verify

.. autoclass:: Periodic2DOptimizerStandaloneCampaignVerificationRequest
   :members:

.. autoclass:: Periodic2DOptimizerStandaloneCampaignVerificationResult
   :members:

.. autoclass:: Periodic2DOptimizerStandaloneCampaignVerifier
   :members:
