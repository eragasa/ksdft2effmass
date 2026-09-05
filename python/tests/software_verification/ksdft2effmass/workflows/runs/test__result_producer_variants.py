r"""Software verification of closed WorkflowRun result-producer variants.

Evidence profile: routine

Bounded artifact scope: the closed non-Workflow result-producer variant family.

Facet and represented meaning

The artifact verifies that distinct external, imported, authored, and legacy producer
records retain actual evidence and limitations without fabricated Workflow lineage.

Intrinsic and cross-object scope

Each producer owns its intrinsic fields; this integration evidence owns agreement
across the complete closed variant family.

VVUQ and scientific exclusions

This is software verification only. It establishes no provenance truth, execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows.runs import (
    ExternalProducerAttemptIdentity,
    ExternalResultProducer,
    ExternalResultProducerIdentity,
    HumanAuthoredResultProducer,
    HumanResultAuthorIdentity,
    ImportedRetainedResultProducer,
    ResultProducerEvidenceIdentity,
    ResultProducerProvenanceIdentity,
    RetainedResultSourceIdentity,
    UnknownLegacyResultProducer,
)

pytestmark = pytest.mark.software_verification


class TestResultProducerVariants:
    """Own cross-variant ResultObject producer evidence."""

    def test_constructor__result_producer_variants__retain_actual_evidence(
        self,
    ) -> None:
        """Require non-Workflow provenance to retain evidence and limitations.

        Evidence ID: SV-WFR-RECORDS-006

        Requirement: External, imported-retained, human-authored, and unknown-legacy
        producers are distinct closed variants with actual evidence and limitations,
        not fabricated Workflow lineage.

        Acceptance: Every variant constructs with canonical evidence; empty evidence
        raises ``ValueError``.
        """
        evidence = (ResultProducerEvidenceIdentity("evidence.one"),)
        limitations = ("synthetic software-verification provenance only",)
        external = ExternalResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.external"),
            external_producer_identity=ExternalResultProducerIdentity("external.one"),
            producer_attempt_identity=ExternalProducerAttemptIdentity("attempt.one"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        imported = ImportedRetainedResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.imported"),
            source_identity=RetainedResultSourceIdentity("source.imported"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        authored = HumanAuthoredResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.authored"),
            author_identity=HumanResultAuthorIdentity("author.one"),
            source_identity=RetainedResultSourceIdentity("source.authored"),
            evidence_identities=evidence,
            limitations=limitations,
        )
        legacy = UnknownLegacyResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.legacy"),
            source_identity=RetainedResultSourceIdentity("source.legacy"),
            evidence_identities=evidence,
            limitations=limitations,
        )

        assert tuple(
            type(producer) for producer in (external, imported, authored, legacy)
        ) == (
            ExternalResultProducer,
            ImportedRetainedResultProducer,
            HumanAuthoredResultProducer,
            UnknownLegacyResultProducer,
        )
        with pytest.raises(ValueError):
            replace(external, evidence_identities=())
