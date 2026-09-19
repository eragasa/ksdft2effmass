r"""Software verification of ``ParameterStudyObservationCollection``.

Evidence profile: routine

Bounded artifact scope: ordered parameter-study source observation and reuse identity.

Facet and represented meaning

The module verifies request correlation, candidate/role order, and exact reused source
Task, ResultObject, and producer-provenance identity.

Intrinsic and cross-object scope

``ParameterStudyObservationCollection`` is the sole system under test. Observation
production, Workflow execution, convergence analysis, and persistence are excluded.

VVUQ and scientific exclusions

Synthetic identities are software fixtures. The collection establishes no calculated
physical observation, parameter acceptance, validation, or uncertainty result.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.analysis._parameter_study import (
    ParameterStudyCandidateIdentity,
    ParameterStudyCandidateObservation,
    ParameterStudyObservationCollection,
    ParameterStudyObservationCollectionIdentity,
    ParameterStudyObservationCollectionRequest,
    ParameterStudyObservationReuse,
    ParameterStudyObservationRoleIdentity,
    ParameterStudyRevisionIdentity,
    ParameterStudySourceObservation,
)
from ksdft2effmass.workflows import (
    ArtifactProducerProvenanceIdentity,
    ResultObjectIdentity,
    TaskInstanceIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = ParameterStudyObservationCollection


class TestParameterStudyObservationCollection:
    """Own software evidence for ordered typed observation collection."""

    @staticmethod
    def collection() -> ParameterStudyObservationCollection:
        """Return a valid two-candidate collection with exact per-role reuse."""
        identity = ParameterStudyObservationCollectionIdentity("collection.synthetic")
        canonical = ParameterStudyCandidateIdentity("candidate.canonical")
        alias = ParameterStudyCandidateIdentity("candidate.alias")
        scf_role = ParameterStudyObservationRoleIdentity("scf")
        nscf_role = ParameterStudyObservationRoleIdentity("diagnostic-nscf")
        scf_source = ParameterStudySourceObservation(
            scf_role,
            TaskInstanceIdentity("task.canonical.scf"),
            ResultObjectIdentity("result.canonical.scf"),
            ArtifactProducerProvenanceIdentity("producer.canonical.scf"),
        )
        nscf_source = ParameterStudySourceObservation(
            nscf_role,
            TaskInstanceIdentity("task.canonical.nscf"),
            ResultObjectIdentity("result.canonical.nscf"),
            ArtifactProducerProvenanceIdentity("producer.canonical.nscf"),
        )
        request = ParameterStudyObservationCollectionRequest(
            identity,
            (ParameterStudyRevisionIdentity("revision.synthetic"),),
            (canonical, alias),
            (scf_role, nscf_role),
            (
                ParameterStudyObservationReuse(
                    alias, canonical, scf_role, scf_source.task_instance_identity
                ),
                ParameterStudyObservationReuse(
                    alias, canonical, nscf_role, nscf_source.task_instance_identity
                ),
            ),
        )
        return SUT(
            identity,
            request,
            (
                ParameterStudyCandidateObservation(
                    canonical, (scf_source, nscf_source)
                ),
                ParameterStudyCandidateObservation(alias, (scf_source, nscf_source)),
            ),
        )

    def test_constructor__ordered_sources_and_reuse__retains_exact_request(
        self,
    ) -> None:
        """Evidence ID: SV-PARAMETER-STUDY-OBSERVATIONS-001

        Requirement: A collection retains exact candidate and role order plus source
        Task, ResultObject, producer provenance, and reuse declarations.

        Acceptance: The valid collection preserves the request and aliases the exact
        immutable canonical source observations for both roles.
        """
        collection = self.collection()

        assert collection.identity is collection.request.identity
        assert (
            tuple(
                value.candidate_identity for value in collection.candidate_observations
            )
            == collection.request.candidate_identities
        )
        assert collection.candidate_observations[1].sources == (
            collection.candidate_observations[0].sources
        )
        assert len(collection.request.reuse) == 2

    def test_constructor__candidate_order_drift__fails_closed(self) -> None:
        """Evidence ID: SV-PARAMETER-STUDY-OBSERVATIONS-002

        Requirement: Candidate observations follow exact request order.

        Acceptance: Reversing otherwise complete candidate observations raises
        ``ValueError`` and produces no collection.
        """
        collection = self.collection()

        with pytest.raises(ValueError, match="request order"):
            SUT(
                collection.identity,
                collection.request,
                tuple(reversed(collection.candidate_observations)),
            )

    def test_constructor__role_order_drift__fails_closed(self) -> None:
        """Evidence ID: SV-PARAMETER-STUDY-OBSERVATIONS-003

        Requirement: Every candidate source tuple follows exact request role order.

        Acceptance: Reversing one candidate's sources raises ``ValueError``.
        """
        collection = self.collection()
        first = collection.candidate_observations[0]
        drifted = replace(first, sources=tuple(reversed(first.sources)))

        with pytest.raises(ValueError, match="role order"):
            SUT(
                collection.identity,
                collection.request,
                (drifted, collection.candidate_observations[1]),
            )

    def test_constructor__reused_result_drift__fails_closed(self) -> None:
        """Evidence ID: SV-PARAMETER-STUDY-OBSERVATIONS-004

        Requirement: Reuse means equality of the complete per-role source observation,
        not nominal candidate or Task similarity.

        Acceptance: Replacing an alias ResultObject identity raises ``ValueError``.
        """
        collection = self.collection()
        alias = collection.candidate_observations[1]
        drifted_source = replace(
            alias.sources[0],
            result_object_identity=ResultObjectIdentity("result.drift"),
        )
        drifted_alias = replace(alias, sources=(drifted_source, alias.sources[1]))

        with pytest.raises(ValueError, match="canonical source observation"):
            SUT(
                collection.identity,
                collection.request,
                (collection.candidate_observations[0], drifted_alias),
            )
