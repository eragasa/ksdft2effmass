"""Software tests for the exact rank-one first-passing certification wire."""

import json
from dataclasses import replace
from hashlib import sha256

import pytest

from ksdft2effmass.certifications.periodic1d.rank1.first_passing_support import (
    CertificationToolIdentity,
    ExactRational,
    FirstPassingIntervalEntry,
    FirstPassingSupportDisposition,
    FirstPassingSupportObjective,
    FirstPassingSupportRequest,
    FirstPassingSupportResult,
    FirstPassingSupportWireValidation,
    FirstPassingSupportWireValidator,
    NonnegativeExactInterval,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def request() -> FirstPassingSupportRequest:
    """Return a synthetic request; no retained runtime evidence is represented."""
    return FirstPassingSupportRequest(
        study_id="synthetic-study",
        execution_id="synthetic-execution",
        case_id="synthetic-case",
        decision_id="synthetic-decision",
        certificate_id="synthetic-certificate",
        repository_url="https://github.com/eragasa/ksdft2effmass",
        repository_commit="1" * 40,
        repository_tree="2" * 40,
        protocol_sha256="3" * 64,
        configuration_source_sha256="4" * 64,
        result_source_sha256="5" * 64,
        analysis_source_sha256="6" * 64,
        verification_source_sha256="7" * 64,
        dependency_lock_sha256="8" * 64,
        native_result_sha256="9" * 64,
        numerical_verification_sha256="a" * 64,
        numerical_verification_passed=True,
        selected_support=3,
    )


def interval(lower: ExactRational, upper: ExactRational) -> NonnegativeExactInterval:
    """Return one exact synthetic error interval."""
    return NonnegativeExactInterval(lower=lower, upper=upper)


def entries(
    *,
    selected_support: int = 3,
    earlier_overlap: bool = False,
    earlier_pass: bool = False,
    selected_overlap: bool = False,
    selected_reject: bool = False,
) -> tuple[FirstPassingIntervalEntry, ...]:
    """Return a complete synthetic interval table for one classification case."""
    zero = ExactRational(0, 1)
    passing_upper = ExactRational(9, 1_000_000_000)
    rejected_lower = ExactRational(1, 50_000_000)
    rejected_upper = ExactRational(3, 100_000_000)
    overlap_lower = ExactRational(9, 1_000_000_000)
    overlap_upper = ExactRational(11, 1_000_000_000)
    values: list[FirstPassingIntervalEntry] = []
    for maximum_range in range(16):
        for objective in FirstPassingSupportObjective:
            current = interval(zero, passing_upper)
            if maximum_range < selected_support:
                current = interval(rejected_lower, rejected_upper)
            if earlier_overlap and maximum_range == selected_support - 1:
                current = interval(overlap_lower, overlap_upper)
            if earlier_pass and maximum_range == selected_support - 1:
                current = interval(zero, passing_upper)
            if selected_overlap and maximum_range == selected_support:
                current = interval(overlap_lower, overlap_upper)
            if selected_reject and maximum_range == selected_support:
                current = interval(rejected_lower, rejected_upper)
            values.append(
                FirstPassingIntervalEntry(
                    maximum_range=maximum_range,
                    objective=objective,
                    interval=current,
                )
            )
    return tuple(values)


def result(
    *,
    disposition: FirstPassingSupportDisposition = (
        FirstPassingSupportDisposition.ACCEPTED
    ),
    selected_support: int = 3,
    interval_entries: tuple[FirstPassingIntervalEntry, ...] | None = None,
) -> FirstPassingSupportResult:
    """Return a synthetic exact result; interval containment is not asserted."""
    return FirstPassingSupportResult(
        certificate_id="synthetic-certificate",
        request_sha256="b" * 64,
        enclosure_artifact_sha256="e" * 64,
        interval_verification_artifact_sha256="f" * 64,
        enclosure_producer=CertificationToolIdentity(
            identity="synthetic-enclosure-producer",
            version="v1",
            source_sha256="c" * 64,
        ),
        interval_verifier=CertificationToolIdentity(
            identity="synthetic-independent-interval-verifier",
            version="v1",
            source_sha256="d" * 64,
        ),
        enclosure_method_id="synthetic-outward-rational-enclosure",
        working_precision_bits=256,
        directed_rounding_policy_id="synthetic-directed-rounding",
        error_budget_id="synthetic-error-budget",
        selected_support=selected_support,
        intervals=(
            entries(selected_support=selected_support)
            if interval_entries is None
            else interval_entries
        ),
        disposition=disposition,
    )


class TestFirstPassingSupportCertification:
    """Establish typed-record wires and fail-closed endpoint decisions."""

    def test__request__round_trips_typed_mapping_and_json(self) -> None:
        subject = request()
        wire = subject.to_json()

        assert FirstPassingSupportRequest.from_dict(subject.to_dict()) == subject
        assert FirstPassingSupportRequest.from_json(wire) == subject
        assert FirstPassingSupportRequest.from_json(wire).to_json() == wire
        assert wire.endswith(b"\n")
        document = json.loads(wire)
        assert document["problem"]["threshold"] == {
            "denominator": 100_000_000,
            "numerator": 1,
        }

    def test__request__rejects_unknown_field(self) -> None:
        document = json.loads(request().to_json())
        document["unknown"] = "forbidden"
        wire = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode()

        with pytest.raises(ValueError, match="fields do not match"):
            FirstPassingSupportRequest.from_json(wire)

    def test__wire_validator__rejects_noncanonical_request_bytes(self) -> None:
        request_document = json.loads(request().to_json())
        noncanonical_request = (
            json.dumps(request_document, separators=(",", ":"), sort_keys=True) + "\n"
        ).encode()

        with pytest.raises(ValueError, match="request bytes are not the canonical"):
            FirstPassingSupportWireValidator().validate(
                noncanonical_request,
                result().to_json(),
            )

    def test__request__rejects_decimal_number_for_support(self) -> None:
        wire = (
            request()
            .to_json()
            .replace(b'"selected_support": 3', b'"selected_support": 3.0')
        )

        with pytest.raises(TypeError, match="excluding bool"):
            FirstPassingSupportRequest.from_json(wire)

    def test__request__rejects_boolean_as_integer(self) -> None:
        wire = (
            request()
            .to_json()
            .replace(b'"selected_support": 3', b'"selected_support": true')
        )

        with pytest.raises(TypeError, match="excluding bool"):
            FirstPassingSupportRequest.from_json(wire)

    def test__request__rejects_duplicate_field(self) -> None:
        wire = (
            request()
            .to_json()
            .replace(
                b'{\n  "artifact_bindings":',
                b'{\n  "case_id": "duplicate",\n  "artifact_bindings":',
            )
        )

        with pytest.raises(ValueError, match="duplicate JSON object key"):
            FirstPassingSupportRequest.from_json(wire)

    def test__request__requires_passing_native_numerical_verification(self) -> None:
        with pytest.raises(ValueError, match="passing numerical verification"):
            replace(request(), numerical_verification_passed=False)

    def test__exact_rational__rejects_nonreduced_value(self) -> None:
        with pytest.raises(ValueError, match="reduced"):
            ExactRational(2, 4)

    def test__exact_interval__rejects_reversed_endpoints(self) -> None:
        with pytest.raises(ValueError, match="must not exceed"):
            NonnegativeExactInterval(ExactRational(2, 1), ExactRational(1, 1))

    def test__result__round_trips_all_32_entries(self) -> None:
        subject = result()
        wire = subject.to_json()

        assert FirstPassingSupportResult.from_dict(subject.to_dict()) == subject
        reconstructed = FirstPassingSupportResult.from_json(wire)
        assert reconstructed == subject
        assert reconstructed.to_json() == wire
        assert len(reconstructed.intervals) == 32
        assert reconstructed.classify() is FirstPassingSupportDisposition.ACCEPTED

    def test__result__rejects_incomplete_inventory(self) -> None:
        with pytest.raises(ValueError, match="all 32"):
            replace(result(), intervals=entries()[:-1])

    def test__result__rejects_noncanonical_inventory_order(self) -> None:
        values = entries()
        malformed = (values[1], values[0], *values[2:])

        with pytest.raises(ValueError, match="canonical order"):
            replace(result(), intervals=malformed)

    def test__result__classifies_earlier_overlap_as_unresolved(self) -> None:
        subject = result(
            disposition=FirstPassingSupportDisposition.UNRESOLVED,
            interval_entries=entries(earlier_overlap=True),
        )

        assert subject.classify() is FirstPassingSupportDisposition.UNRESOLVED

    def test__result__classifies_selected_overlap_as_unresolved(self) -> None:
        subject = result(
            disposition=FirstPassingSupportDisposition.UNRESOLVED,
            interval_entries=entries(selected_overlap=True),
        )

        assert subject.classify() is FirstPassingSupportDisposition.UNRESOLVED

    def test__result__rejects_an_earlier_definite_joint_pass(self) -> None:
        subject = result(
            disposition=FirstPassingSupportDisposition.REJECTED,
            interval_entries=entries(earlier_pass=True),
        )

        assert subject.classify() is FirstPassingSupportDisposition.REJECTED

    def test__result__rejects_earlier_pass_despite_selected_overlap(self) -> None:
        subject = result(
            disposition=FirstPassingSupportDisposition.REJECTED,
            interval_entries=entries(earlier_pass=True, selected_overlap=True),
        )

        assert subject.classify() is FirstPassingSupportDisposition.REJECTED

    def test__result__rejects_selected_definite_failure(self) -> None:
        subject = result(
            disposition=FirstPassingSupportDisposition.REJECTED,
            interval_entries=entries(selected_reject=True),
        )

        assert subject.classify() is FirstPassingSupportDisposition.REJECTED

    def test__result__rejects_false_reported_disposition(self) -> None:
        with pytest.raises(ValueError, match="reported disposition"):
            result(disposition=FirstPassingSupportDisposition.UNRESOLVED)

    def test__result__requires_distinct_retained_artifacts(self) -> None:
        subject = result()

        with pytest.raises(ValueError, match="artifact must differ"):
            replace(
                subject,
                interval_verification_artifact_sha256=(
                    subject.enclosure_artifact_sha256
                ),
            )

    def test__result__requires_distinct_producer_and_verifier(self) -> None:
        subject = result()

        with pytest.raises(ValueError, match="must be distinct"):
            replace(subject, interval_verifier=subject.enclosure_producer)

    def test__result__requires_source_distinct_producer_and_verifier(self) -> None:
        subject = result()
        source_identical_verifier = replace(
            subject.interval_verifier,
            source_sha256=subject.enclosure_producer.source_sha256,
        )

        with pytest.raises(ValueError, match="source must differ"):
            replace(subject, interval_verifier=source_identical_verifier)

    def test__wire_validator__correlates_request_and_result_bytes(self) -> None:
        request_wire = request().to_json()
        result_wire = replace(
            result(), request_sha256=sha256(request_wire).hexdigest()
        ).to_json()

        validation = FirstPassingSupportWireValidator().validate(
            request_wire, result_wire
        )

        assert validation.certificate_id == "synthetic-certificate"
        assert validation.request_sha256 == sha256(request_wire).hexdigest()
        assert validation.result_sha256 == sha256(result_wire).hexdigest()
        assert validation.selected_support == 3
        assert validation.disposition is FirstPassingSupportDisposition.ACCEPTED
        assert FirstPassingSupportWireValidation.from_json(validation.to_json()) == (
            validation
        )

    def test__wire_validator__rejects_request_digest_mismatch(self) -> None:
        with pytest.raises(ValueError, match="request_sha256 does not match"):
            FirstPassingSupportWireValidator().validate(
                request().to_json(), result().to_json()
            )

    def test__wire_validator__rejects_certificate_identity_mismatch(self) -> None:
        request_wire = request().to_json()
        mismatched = replace(
            result(),
            certificate_id="different-certificate",
            request_sha256=sha256(request_wire).hexdigest(),
        )

        with pytest.raises(ValueError, match="certificate_id differs"):
            FirstPassingSupportWireValidator().validate(
                request_wire, mismatched.to_json()
            )

    def test__wire_validator__rejects_selected_support_mismatch(self) -> None:
        request_wire = request().to_json()
        mismatched = replace(
            result(selected_support=4),
            request_sha256=sha256(request_wire).hexdigest(),
        )

        with pytest.raises(ValueError, match="selected_support differs"):
            FirstPassingSupportWireValidator().validate(
                request_wire, mismatched.to_json()
            )

    def test__wire_validator__reports_unresolved_without_promoting_it(self) -> None:
        request_wire = request().to_json()
        unresolved = result(
            disposition=FirstPassingSupportDisposition.UNRESOLVED,
            interval_entries=entries(selected_overlap=True),
        )
        result_wire = replace(
            unresolved, request_sha256=sha256(request_wire).hexdigest()
        ).to_json()

        validation = FirstPassingSupportWireValidator().validate(
            request_wire, result_wire
        )

        assert validation.disposition is FirstPassingSupportDisposition.UNRESOLVED
