r"""Class-owned software verification of Wannier90 encoded documents.

Evidence profile: routine

Bounded scope
-------------
The intrinsic field, representation, variant-discrimination, and immutability contract
of ``Periodic1DWannier90EncodedDocuments`` using synthetic byte values only.

Ownership and scientific exclusions
-----------------------------------
The SUT owns encoded composite-input and Wannier90-result documents plus an explicit
wire-level result-kind discriminator. It deliberately owns no native artifact group,
filesystem path, decoded result, retained space, operator, or scientific disposition.
These tests access no repository artifact, execute no calculator, decode no campaign
document, and establish no provenance, convergence, physical validity, uncertainty
quantification, or acceptance. Retained-file and migration-route evidence is owned by a
separate integration module.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.periodic1d.campaign.result_documents import (
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.wannier90.encoded_documents import (
    Periodic1DWannier90EncodedDocuments,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90EncodedDocuments


class TestPeriodic1DWannier90EncodedDocuments:
    """Own intrinsic row-040 encoded-document contract evidence."""

    def test_contract__owns_exact_fields_and_supported_wire_variants(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-001.

        Requirement: The DataObject owns exactly two encoded byte fields and one
        explicit result-kind discriminator, while native artifacts remain absent.

        Method: Inspect dataclass fields and construct one synthetic record for each
        supported Wannier90 result kind.

        Oracle: The documented field inventory, exact defining module, Python object
        identity, and the two enumerated wire variants.

        Acceptance: Field names, order, types, defining module, supplied byte-object
        identities, and exact enum members all match; no artifact-group field exists.

        Interpretation: A pass establishes the intrinsic encoded-document side of the
        row-040 ownership split.

        Limitations: Synthetic bytes do not establish valid JSON, retained content
        identity, native-file availability, decoded semantics, or provenance.
        """
        input_payload = b"synthetic composite input"
        result_payload = b"synthetic Wannier90 result"

        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.wannier90.encoded_documents"
        )
        assert [(field.name, field.type) for field in fields(SUT)] == [
            ("composite_input_payload", bytes),
            ("result_payload", bytes),
            ("result_kind", Periodic1DEncodedResultKind),
        ]
        assert "artifact_groups" not in {field.name for field in fields(SUT)}

        for result_kind in (
            Periodic1DEncodedResultKind.WANNIER90,
            Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        ):
            documents = SUT(input_payload, result_payload, result_kind)
            assert documents.composite_input_payload is input_payload
            assert documents.result_payload is result_payload
            assert documents.result_kind is result_kind

    def test_construction__rejects_wrong_and_empty_payload_representations(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-002.

        Requirement: Both encoded fields accept only nonempty exact built-in ``bytes``.

        Method: Exercise wrong types, ``bytes`` subclasses, and empty values at each
        encoded-field position while supplying a supported explicit result kind.

        Oracle: The documented exact representation contract and exception taxonomy.

        Acceptance: Wrong representations raise ``TypeError`` and empty exact-byte
        representations raise ``ValueError`` without coercion.

        Interpretation: A pass establishes fail-closed payload validation.

        Limitations: Nonempty bytes are not thereby valid JSON or a supported schema.
        """

        class BytesSubclass(bytes):
            """Provide a bytes subtype that violates the exact contract."""

        kind = Periodic1DEncodedResultKind.WANNIER90
        for input_payload, result_payload, exception, match in (
            (
                bytearray(b"{}"),
                b"{}",
                TypeError,
                "composite_input_payload must be built-in bytes",
            ),
            (
                BytesSubclass(b"{}"),
                b"{}",
                TypeError,
                "composite_input_payload must be",
            ),
            (b"", b"{}", ValueError, "composite_input_payload must be nonempty"),
            (
                b"{}",
                bytearray(b"{}"),
                TypeError,
                "result_payload must be built-in bytes",
            ),
            (b"{}", BytesSubclass(b"{}"), TypeError, "result_payload must be"),
            (b"{}", b"", ValueError, "result_payload must be nonempty"),
        ):
            with pytest.raises(exception, match=match):
                SUT(input_payload, result_payload, kind)  # type: ignore[arg-type]

    def test_construction__rejects_wrong_or_unsupported_result_kind(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-003.

        Requirement: The wire discriminator is an exact enum value from the two
        supported Wannier90 variants; it is never inferred from bytes or filenames.

        Method: Supply a string substitute and a valid enum member belonging to the
        isolated-band result family.

        Oracle: Exact result-kind type and bounded membership contracts.

        Acceptance: The string raises ``TypeError`` and the other enum family raises
        ``ValueError``.

        Interpretation: A pass establishes explicit, fail-closed wire-variant identity.

        Limitations: Selecting a supported kind does not prove that payload content
        conforms to that kind; decoding and correlation remain separate operations.
        """
        with pytest.raises(TypeError, match="result_kind must be"):
            SUT(b"{}", b"{}", "wannier90")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="result_kind must identify"):
            SUT(b"{}", b"{}", Periodic1DEncodedResultKind.ISOLATED_BAND)

    def test_construction__is_frozen_and_slotted(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-004.

        Requirement: Constructed encoded documents are operationally immutable and
        cannot acquire undeclared native-artifact or other state.

        Method: Attempt to replace an encoded field and add a dynamic artifact field.

        Oracle: Frozen and slotted dataclass semantics.

        Acceptance: Both mutations fail and the retained values remain unchanged.

        Interpretation: A pass establishes the immutable encoded-container facet.

        Limitations: Immutability does not authenticate the supplied bytes or prove
        that native artifacts were separately supplied.
        """
        documents = SUT(
            b"input",
            b"result",
            Periodic1DEncodedResultKind.WANNIER90,
        )

        with pytest.raises(FrozenInstanceError):
            documents.result_payload = b"changed"  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            documents.artifact_groups = ()  # type: ignore[attr-defined]
        assert documents.result_payload == b"result"
        assert not hasattr(documents, "artifact_groups")
