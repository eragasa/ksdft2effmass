"""Exact records for the rank-one finite first-passing certification.

These records own conservative endpoint classification only. They neither produce
outward enclosures nor verify that an enclosure contains a runtime quantity. Those
capabilities require separately qualified implementations and retained artifact
bindings before any certification can be accepted as evidence.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import ClassVar, Self

from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StrWireEnum,
)

_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_IDENTIFIER_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_REPOSITORY_PATTERN = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z"
)
_GIT_OBJECT_PATTERN = re.compile(r"[0-9a-f]{40}\Z")

CONTRACT_ID = "ksdft2effmass.certifications.periodic1d.rank1.first-passing-support.v1"
SCHEMA_VERSION = 1
PROPOSITION_ID = "periodic1d.rank1.joint-first-passing-support"
PARENT_IDENTITY = "ksdft2effmass.periodic1d.controlled-four-state-parent.v1"
PARENT_ENTRY_DENOMINATOR = 100
FOURIER_CONVENTION_ID = "periodic1d.centered-bvk.forward-negative.v1"
MEDIATED_CANDIDATE_ID = "periodic1d.rank1.transform-mediated-truncation.v1"
DIRECT_CANDIDATE_ID = "periodic1d.rank1.equal-weight-direct-fit.v1"
ERROR_DEFINITION_ID = "periodic1d.rank1.total-maximum-evaluation-error.v1"
UNIT_ID = "E_ref"
CONSTRUCTION_MESH_SIZE = 256
EVALUATION_SIZE = 1025
EVALUATION_SHIFT_NUMERATOR = 1
EVALUATION_SHIFT_DENOMINATOR = 257
SUPPORT_INVENTORY = tuple(range(16))

PARENT_ONSITE_NUMERATORS = (
    (-120, 6, 0, 0),
    (6, -35, 0, 0),
    (0, 0, 100, 4),
    (0, 0, 4, 175),
)
PARENT_POSITIVE_HOPPING_NUMERATORS = (
    (15, 0, 12, 0),
    (0, -10, 0, 10),
    (0, 0, 5, 0),
    (0, 0, 0, -4),
)


class FirstPassingSupportObjective(StrWireEnum):
    """Closed decisive objective inventory for this proposition.

    Notes
    -----
    ``MEDIATED_TOTAL_MAXIMUM`` names the transform-mediated candidate's maximum total
    evaluation error. ``DIRECT_TOTAL_MAXIMUM`` names the equal-weight direct-fit
    candidate's maximum total evaluation error.
    """

    MEDIATED_TOTAL_MAXIMUM = "mediated_total_maximum_evaluation_error"
    DIRECT_TOTAL_MAXIMUM = "direct_total_maximum_evaluation_error"


OBJECTIVE_INVENTORY = tuple(FirstPassingSupportObjective)


class FirstPassingSupportDisposition(StrWireEnum):
    """Conservative exact classification of one complete interval table.

    Notes
    -----
    ``ACCEPTED`` requires selected passage and definite failure of every earlier
    support. ``REJECTED`` means selected definite failure or earlier definite passage.
    ``UNRESOLVED`` retains every remaining undecided interval configuration.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True, order=True)
class ExactRational(BaseTypedRecord):
    """Represent one reduced exact rational number.

    Parameters
    ----------
    numerator
        Arbitrary-precision built-in integer numerator. Booleans are rejected.
    denominator
        Positive arbitrary-precision built-in integer denominator. Booleans are
        rejected.

    Raises
    ------
    TypeError
        Either scalar is not an exact built-in integer.
    ValueError
        The denominator is nonpositive, the fraction is not reduced, or zero uses a
        denominator other than one.

    Notes
    -----
    Python integer arithmetic has no fixed-width overflow. Wire size and resource
    exhaustion are separate operational concerns.
    """

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        if type(self.numerator) is not int:
            raise TypeError("numerator must be a built-in int excluding bool")
        if type(self.denominator) is not int:
            raise TypeError("denominator must be a built-in int excluding bool")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if gcd(abs(self.numerator), self.denominator) != 1:
            raise ValueError("rational must be reduced")
        if self.numerator == 0 and self.denominator != 1:
            raise ValueError("zero must use denominator one")

    def as_fraction(self) -> Fraction:
        """Return the equivalent standard-library rational value.

        Returns
        -------
        fractions.Fraction
            Exact value represented by ``numerator / denominator``.
        """
        return Fraction(self.numerator, self.denominator)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"numerator": self.numerator, "denominator": self.denominator}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(values, {"numerator", "denominator"}, "exact rational")
        return cls(
            numerator=_int_value(values, "numerator"),
            denominator=_int_value(values, "denominator"),
        )


@dataclass(frozen=True, slots=True)
class NonnegativeExactInterval(BaseTypedRecord):
    """Represent one nonnegative closed error interval in ``E_ref``.

    Parameters
    ----------
    lower
        Exact inclusive lower endpoint.
    upper
        Exact inclusive upper endpoint.

    Raises
    ------
    TypeError
        An endpoint is not :class:`ExactRational`.
    ValueError
        The lower endpoint is negative or exceeds the upper endpoint.

    Notes
    -----
    Construction validates endpoint structure and ordering only. It does not establish
    containment of any computed quantity.
    """

    lower: ExactRational
    upper: ExactRational

    def __post_init__(self) -> None:
        if not isinstance(self.lower, ExactRational):
            raise TypeError("lower must be ExactRational")
        if not isinstance(self.upper, ExactRational):
            raise TypeError("upper must be ExactRational")
        if self.lower.numerator < 0:
            raise ValueError("error interval lower endpoint must be nonnegative")
        if self.lower.as_fraction() > self.upper.as_fraction():
            raise ValueError("interval lower endpoint must not exceed upper endpoint")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"lower": self.lower.to_dict(), "upper": self.upper.to_dict()}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(values, {"lower", "upper"}, "nonnegative exact interval")
        return cls(
            lower=ExactRational.from_dict(_mapping_value(values, "lower")),
            upper=ExactRational.from_dict(_mapping_value(values, "upper")),
        )


@dataclass(frozen=True, slots=True)
class FirstPassingIntervalEntry(BaseTypedRecord):
    """Bind one support/objective pair to one claimed error enclosure.

    Parameters
    ----------
    maximum_range
        Dimensionless ordinary-lattice support index in the closed inventory ``0..15``.
    objective
        Exact objective whose total maximum evaluation error is enclosed.
    interval
        Claimed closed error interval in ``E_ref``.

    Raises
    ------
    TypeError
        A field has the wrong exact type; booleans are not support integers.
    ValueError
        ``maximum_range`` is outside the frozen support inventory.
    """

    maximum_range: int
    objective: FirstPassingSupportObjective
    interval: NonnegativeExactInterval

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int excluding bool")
        if self.maximum_range not in SUPPORT_INVENTORY:
            raise ValueError("maximum_range is outside the complete support inventory")
        if not isinstance(self.objective, FirstPassingSupportObjective):
            raise TypeError("objective must be FirstPassingSupportObjective")
        if not isinstance(self.interval, NonnegativeExactInterval):
            raise TypeError("interval must be NonnegativeExactInterval")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_range": self.maximum_range,
            "objective": self.objective.to_wire(),
            "interval": self.interval.to_dict(),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"maximum_range", "objective", "interval"},
            "first-passing interval entry",
        )
        return cls(
            maximum_range=_int_value(values, "maximum_range"),
            objective=FirstPassingSupportObjective.from_wire(
                _str_value(values, "objective")
            ),
            interval=NonnegativeExactInterval.from_dict(
                _mapping_value(values, "interval")
            ),
        )


@dataclass(frozen=True, slots=True)
class CertificationToolIdentity(BaseTypedRecord):
    """Identify one certification producer or independent verifier.

    Parameters
    ----------
    identity
        Portable implementation identifier.
    version
        Portable implementation-version identifier.
    source_sha256
        SHA-256 digest of the implementation source used for the artifact.

    Raises
    ------
    TypeError
        A field is not a built-in string.
    ValueError
        An identifier or digest violates its closed lexical contract.
    """

    identity: str
    version: str
    source_sha256: str

    def __post_init__(self) -> None:
        _require_identifier("identity", self.identity)
        _require_identifier("version", self.version)
        _require_sha256("source_sha256", self.source_sha256)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "identity": self.identity,
            "version": self.version,
            "source_sha256": self.source_sha256,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"identity", "version", "source_sha256"},
            "certification tool identity",
        )
        return cls(
            identity=_str_value(values, "identity"),
            version=_str_value(values, "version"),
            source_sha256=_str_value(values, "source_sha256"),
        )


@dataclass(frozen=True, slots=True)
class FirstPassingSupportRequest(BaseTypedRecord):
    """Bind one frozen first-passing proposition to its source and evidence identities.

    Parameters
    ----------
    study_id
        Portable identity of the owning scientific study.
    execution_id
        Portable identity of the exact calculation execution.
    case_id
        Portable identity of the evaluated case.
    decision_id
        Portable identity of the numerical decision being certified.
    certificate_id
        Portable identity shared with the certification result.
    repository_url
        Canonical GitHub HTTPS repository URL.
    repository_commit
        Lowercase 40-character Git commit object identity.
    repository_tree
        Lowercase 40-character Git tree object identity.
    protocol_sha256
        SHA-256 digest of the governing calculation protocol.
    configuration_source_sha256
        SHA-256 digest of the configuration source.
    result_source_sha256
        SHA-256 digest of the retained-result source.
    analysis_source_sha256
        SHA-256 digest of the scientific analysis source.
    verification_source_sha256
        SHA-256 digest of the independent numerical-verification source.
    dependency_lock_sha256
        SHA-256 digest of the resolved dependency lock.
    native_result_sha256
        SHA-256 digest of the native result bytes.
    numerical_verification_sha256
        SHA-256 digest of the independent numerical-verification artifact.
    numerical_verification_passed
        Exact built-in boolean. Certification requests require ``True``.
    selected_support
        Dimensionless built-in integer support in the closed inventory ``0..15``.

    Raises
    ------
    TypeError
        A field has the wrong exact built-in type; booleans are not support integers.
    ValueError
        An identity, Git object, digest, verification state, or support violates the
        frozen proposition contract.

    Notes
    -----
    The typed mapping also carries the complete controlled parent, mesh, Fourier,
    candidate, objective, threshold, and unit identity. No values are inferred while
    decoding.
    """

    study_id: str
    execution_id: str
    case_id: str
    decision_id: str
    certificate_id: str
    repository_url: str
    repository_commit: str
    repository_tree: str
    protocol_sha256: str
    configuration_source_sha256: str
    result_source_sha256: str
    analysis_source_sha256: str
    verification_source_sha256: str
    dependency_lock_sha256: str
    native_result_sha256: str
    numerical_verification_sha256: str
    numerical_verification_passed: bool
    selected_support: int

    CONTRACT_ID: ClassVar[str] = CONTRACT_ID
    SCHEMA_VERSION: ClassVar[int] = SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name, value in (
            ("study_id", self.study_id),
            ("execution_id", self.execution_id),
            ("case_id", self.case_id),
            ("decision_id", self.decision_id),
            ("certificate_id", self.certificate_id),
        ):
            _require_identifier(name, value)
        if type(self.repository_url) is not str:
            raise TypeError("repository_url must be a built-in str")
        if _REPOSITORY_PATTERN.fullmatch(self.repository_url) is None:
            raise ValueError("repository_url must be a canonical GitHub HTTPS URL")
        for name, value in (
            ("repository_commit", self.repository_commit),
            ("repository_tree", self.repository_tree),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if _GIT_OBJECT_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} must be a 40-character lowercase Git object")
        for name, value in (
            ("protocol_sha256", self.protocol_sha256),
            ("configuration_source_sha256", self.configuration_source_sha256),
            ("result_source_sha256", self.result_source_sha256),
            ("analysis_source_sha256", self.analysis_source_sha256),
            ("verification_source_sha256", self.verification_source_sha256),
            ("dependency_lock_sha256", self.dependency_lock_sha256),
            ("native_result_sha256", self.native_result_sha256),
            ("numerical_verification_sha256", self.numerical_verification_sha256),
        ):
            _require_sha256(name, value)
        if type(self.numerical_verification_passed) is not bool:
            raise TypeError("numerical_verification_passed must be a built-in bool")
        if not self.numerical_verification_passed:
            raise ValueError(
                "certification request requires passing numerical verification"
            )
        if type(self.selected_support) is not int:
            raise TypeError("selected_support must be a built-in int excluding bool")
        if self.selected_support not in SUPPORT_INVENTORY:
            raise ValueError(
                "selected_support is outside the complete support inventory"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        # The fixed problem mapping makes the proposition self-identifying on the wire.
        return {
            "artifact_bindings": {
                "dependency_lock_sha256": self.dependency_lock_sha256,
                "native_result_sha256": self.native_result_sha256,
                "numerical_verification_passed": self.numerical_verification_passed,
                "numerical_verification_sha256": (self.numerical_verification_sha256),
            },
            "case_id": self.case_id,
            "certificate_id": self.certificate_id,
            "contract_id": CONTRACT_ID,
            "decision_id": self.decision_id,
            "execution_id": self.execution_id,
            "problem": _fixed_problem_mapping(),
            "proposition_id": PROPOSITION_ID,
            "repository": {
                "analysis_source_sha256": self.analysis_source_sha256,
                "commit": self.repository_commit,
                "configuration_source_sha256": self.configuration_source_sha256,
                "protocol_sha256": self.protocol_sha256,
                "repository_url": self.repository_url,
                "result_source_sha256": self.result_source_sha256,
                "tree": self.repository_tree,
                "verification_source_sha256": self.verification_source_sha256,
            },
            "schema_version": SCHEMA_VERSION,
            "selected_support": self.selected_support,
            "study_id": self.study_id,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {
                "artifact_bindings",
                "case_id",
                "certificate_id",
                "contract_id",
                "decision_id",
                "execution_id",
                "problem",
                "proposition_id",
                "repository",
                "schema_version",
                "selected_support",
                "study_id",
            },
            "first-passing certification request",
        )
        _fixed_value(values, "contract_id", CONTRACT_ID)
        _fixed_value(values, "schema_version", SCHEMA_VERSION)
        _fixed_value(values, "proposition_id", PROPOSITION_ID)
        problem = _mapping_value(values, "problem")
        if problem != _fixed_problem_mapping():
            raise ValueError("problem identity does not match the frozen proposition")
        repository = _mapping_value(values, "repository")
        _fields(
            repository,
            {
                "analysis_source_sha256",
                "commit",
                "configuration_source_sha256",
                "protocol_sha256",
                "repository_url",
                "result_source_sha256",
                "tree",
                "verification_source_sha256",
            },
            "repository",
        )
        artifacts = _mapping_value(values, "artifact_bindings")
        _fields(
            artifacts,
            {
                "dependency_lock_sha256",
                "native_result_sha256",
                "numerical_verification_passed",
                "numerical_verification_sha256",
            },
            "artifact bindings",
        )
        return cls(
            study_id=_str_value(values, "study_id"),
            execution_id=_str_value(values, "execution_id"),
            case_id=_str_value(values, "case_id"),
            decision_id=_str_value(values, "decision_id"),
            certificate_id=_str_value(values, "certificate_id"),
            repository_url=_str_value(repository, "repository_url"),
            repository_commit=_str_value(repository, "commit"),
            repository_tree=_str_value(repository, "tree"),
            protocol_sha256=_str_value(repository, "protocol_sha256"),
            configuration_source_sha256=_str_value(
                repository, "configuration_source_sha256"
            ),
            result_source_sha256=_str_value(repository, "result_source_sha256"),
            analysis_source_sha256=_str_value(repository, "analysis_source_sha256"),
            verification_source_sha256=_str_value(
                repository, "verification_source_sha256"
            ),
            dependency_lock_sha256=_str_value(artifacts, "dependency_lock_sha256"),
            native_result_sha256=_str_value(artifacts, "native_result_sha256"),
            numerical_verification_sha256=_str_value(
                artifacts, "numerical_verification_sha256"
            ),
            numerical_verification_passed=_bool_value(
                artifacts, "numerical_verification_passed"
            ),
            selected_support=_int_value(values, "selected_support"),
        )


@dataclass(frozen=True, slots=True)
class FirstPassingSupportResult(BaseTypedRecord):
    """Retain the complete claimed enclosure table and exact endpoint disposition.

    Parameters
    ----------
    certificate_id
        Portable identity shared with the certification request.
    request_sha256
        SHA-256 digest of the exact canonical request bytes.
    enclosure_artifact_sha256
        SHA-256 digest of the producer's retained enclosure artifact.
    interval_verification_artifact_sha256
        SHA-256 digest of the independent containment-verification artifact.
    enclosure_producer
        Identity of the claimed outward-enclosure producer.
    interval_verifier
        Distinct identity of the claimed independent containment verifier.
    enclosure_method_id
        Portable identity of the enclosure method.
    working_precision_bits
        Dimensionless built-in integer working precision, at least 64 bits.
    directed_rounding_policy_id
        Portable identity of the directed-rounding policy.
    error_budget_id
        Portable identity of the error-budget decomposition.
    selected_support
        Dimensionless support proposed as the first joint passage.
    intervals
        All 32 support/objective entries in support-major canonical order.
    disposition
        Conservative disposition implied by the supplied exact endpoints.

    Raises
    ------
    TypeError
        A field or nested value has the wrong exact type; booleans are not integers.
    ValueError
        A digest, identity, producer/verifier separation, precision, support, interval
        inventory, ordering, or reported disposition violates the contract.

    Notes
    -----
    Construction does not establish interval containment. Error intervals use ``E_ref``.
    Python integer arithmetic is arbitrary precision and has no fixed-width overflow.
    """

    certificate_id: str
    request_sha256: str
    enclosure_artifact_sha256: str
    interval_verification_artifact_sha256: str
    enclosure_producer: CertificationToolIdentity
    interval_verifier: CertificationToolIdentity
    enclosure_method_id: str
    working_precision_bits: int
    directed_rounding_policy_id: str
    error_budget_id: str
    selected_support: int
    intervals: tuple[FirstPassingIntervalEntry, ...]
    disposition: FirstPassingSupportDisposition

    CONTRACT_ID: ClassVar[str] = CONTRACT_ID
    SCHEMA_VERSION: ClassVar[int] = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_identifier("certificate_id", self.certificate_id)
        _require_sha256("request_sha256", self.request_sha256)
        _require_sha256("enclosure_artifact_sha256", self.enclosure_artifact_sha256)
        _require_sha256(
            "interval_verification_artifact_sha256",
            self.interval_verification_artifact_sha256,
        )
        if self.enclosure_artifact_sha256 == self.interval_verification_artifact_sha256:
            raise ValueError(
                "interval verification artifact must differ from enclosure artifact"
            )
        if not isinstance(self.enclosure_producer, CertificationToolIdentity):
            raise TypeError("enclosure_producer must be CertificationToolIdentity")
        if not isinstance(self.interval_verifier, CertificationToolIdentity):
            raise TypeError("interval_verifier must be CertificationToolIdentity")
        if self.enclosure_producer.identity == self.interval_verifier.identity:
            raise ValueError(
                "interval verifier must be distinct from enclosure producer"
            )
        if (
            self.enclosure_producer.source_sha256
            == self.interval_verifier.source_sha256
        ):
            raise ValueError(
                "interval verifier source must differ from enclosure producer source"
            )
        for name, value in (
            ("enclosure_method_id", self.enclosure_method_id),
            ("directed_rounding_policy_id", self.directed_rounding_policy_id),
            ("error_budget_id", self.error_budget_id),
        ):
            _require_identifier(name, value)
        if type(self.working_precision_bits) is not int:
            raise TypeError(
                "working_precision_bits must be a built-in int excluding bool"
            )
        if self.working_precision_bits < 64:
            raise ValueError("working_precision_bits must be at least 64")
        if type(self.selected_support) is not int:
            raise TypeError("selected_support must be a built-in int excluding bool")
        if self.selected_support not in SUPPORT_INVENTORY:
            raise ValueError(
                "selected_support is outside the complete support inventory"
            )
        if not isinstance(self.intervals, tuple):
            raise TypeError("intervals must be a tuple")
        expected_keys = tuple(
            (maximum_range, objective)
            for maximum_range in SUPPORT_INVENTORY
            for objective in OBJECTIVE_INVENTORY
        )
        observed_keys: list[tuple[int, FirstPassingSupportObjective]] = []
        for entry in self.intervals:
            if not isinstance(entry, FirstPassingIntervalEntry):
                raise TypeError("intervals must contain FirstPassingIntervalEntry")
            observed_keys.append((entry.maximum_range, entry.objective))
        if tuple(observed_keys) != expected_keys:
            raise ValueError(
                "intervals must contain all 32 support/objective entries "
                "in canonical order"
            )
        if not isinstance(self.disposition, FirstPassingSupportDisposition):
            raise TypeError("disposition must be FirstPassingSupportDisposition")
        if self.disposition is not self.classify():
            raise ValueError(
                "reported disposition does not match exact interval semantics"
            )

    def classify(self) -> FirstPassingSupportDisposition:
        """Classify the complete table without assuming support monotonicity.

        Returns
        -------
        FirstPassingSupportDisposition
            Exact conservative disposition under the frozen threshold ``1e-8 E_ref``.

        Notes
        -----
        Acceptance requires selected-support upper bounds at or below the threshold and
        at least one earlier-support lower bound above the threshold for every earlier
        support. Endpoint equality is passing. Any overlap that prevents those exact
        decisions remains unresolved.
        """
        # Exact rational comparison preserves the inclusive threshold convention.
        threshold = Fraction(1, 100_000_000)
        table = {
            (entry.maximum_range, entry.objective): entry.interval
            for entry in self.intervals
        }
        selected_intervals = tuple(
            table[(self.selected_support, objective)]
            for objective in OBJECTIVE_INVENTORY
        )
        selected_definitely_rejected = any(
            interval.lower.as_fraction() > threshold for interval in selected_intervals
        )
        selected_definitely_accepted = all(
            interval.upper.as_fraction() <= threshold for interval in selected_intervals
        )
        earlier_definitely_accepted = False
        every_earlier_definitely_rejected = True
        # Inspect each earlier support independently; locality need not be monotone.
        for maximum_range in SUPPORT_INVENTORY:
            if maximum_range >= self.selected_support:
                break
            earlier_intervals = tuple(
                table[(maximum_range, objective)] for objective in OBJECTIVE_INVENTORY
            )
            if all(
                interval.upper.as_fraction() <= threshold
                for interval in earlier_intervals
            ):
                earlier_definitely_accepted = True
            if not any(
                interval.lower.as_fraction() > threshold
                for interval in earlier_intervals
            ):
                every_earlier_definitely_rejected = False
        if selected_definitely_rejected or earlier_definitely_accepted:
            return FirstPassingSupportDisposition.REJECTED
        if selected_definitely_accepted and every_earlier_definitely_rejected:
            return FirstPassingSupportDisposition.ACCEPTED
        return FirstPassingSupportDisposition.UNRESOLVED

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "certificate_id": self.certificate_id,
            "contract_id": CONTRACT_ID,
            "disposition": self.disposition.to_wire(),
            "enclosure_artifact_sha256": self.enclosure_artifact_sha256,
            "enclosure_method": {
                "directed_rounding_policy_id": self.directed_rounding_policy_id,
                "enclosure_method_id": self.enclosure_method_id,
                "error_budget_id": self.error_budget_id,
                "working_precision_bits": self.working_precision_bits,
            },
            "enclosure_producer": self.enclosure_producer.to_dict(),
            "interval_verification_artifact_sha256": (
                self.interval_verification_artifact_sha256
            ),
            "interval_verifier": self.interval_verifier.to_dict(),
            "intervals": tuple(entry.to_dict() for entry in self.intervals),
            "proposition_id": PROPOSITION_ID,
            "request_sha256": self.request_sha256,
            "schema_version": SCHEMA_VERSION,
            "selected_support": self.selected_support,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {
                "certificate_id",
                "contract_id",
                "disposition",
                "enclosure_artifact_sha256",
                "enclosure_method",
                "enclosure_producer",
                "interval_verification_artifact_sha256",
                "interval_verifier",
                "intervals",
                "proposition_id",
                "request_sha256",
                "schema_version",
                "selected_support",
            },
            "first-passing certification result",
        )
        _fixed_value(values, "contract_id", CONTRACT_ID)
        _fixed_value(values, "schema_version", SCHEMA_VERSION)
        _fixed_value(values, "proposition_id", PROPOSITION_ID)
        method = _mapping_value(values, "enclosure_method")
        _fields(
            method,
            {
                "directed_rounding_policy_id",
                "enclosure_method_id",
                "error_budget_id",
                "working_precision_bits",
            },
            "enclosure method",
        )
        interval_values = _tuple_value(values, "intervals")
        intervals: list[FirstPassingIntervalEntry] = []
        for value in interval_values:
            if not isinstance(value, Mapping):
                raise TypeError("interval entries must decode to mappings")
            intervals.append(FirstPassingIntervalEntry.from_dict(value))
        return cls(
            certificate_id=_str_value(values, "certificate_id"),
            request_sha256=_str_value(values, "request_sha256"),
            enclosure_artifact_sha256=_str_value(values, "enclosure_artifact_sha256"),
            interval_verification_artifact_sha256=_str_value(
                values, "interval_verification_artifact_sha256"
            ),
            enclosure_producer=CertificationToolIdentity.from_dict(
                _mapping_value(values, "enclosure_producer")
            ),
            interval_verifier=CertificationToolIdentity.from_dict(
                _mapping_value(values, "interval_verifier")
            ),
            enclosure_method_id=_str_value(method, "enclosure_method_id"),
            working_precision_bits=_int_value(method, "working_precision_bits"),
            directed_rounding_policy_id=_str_value(
                method, "directed_rounding_policy_id"
            ),
            error_budget_id=_str_value(method, "error_budget_id"),
            selected_support=_int_value(values, "selected_support"),
            intervals=tuple(intervals),
            disposition=FirstPassingSupportDisposition.from_wire(
                _str_value(values, "disposition")
            ),
        )


def _fixed_problem_mapping() -> Mapping[str, SerializableValue]:
    return {
        "construction_mesh_size": CONSTRUCTION_MESH_SIZE,
        "direct_candidate_id": DIRECT_CANDIDATE_ID,
        "energy_reference": ExactRational(1, 1).to_dict(),
        "error_definition_id": ERROR_DEFINITION_ID,
        "evaluation_shift": ExactRational(
            EVALUATION_SHIFT_NUMERATOR,
            EVALUATION_SHIFT_DENOMINATOR,
        ).to_dict(),
        "evaluation_size": EVALUATION_SIZE,
        "fourier_convention_id": FOURIER_CONVENTION_ID,
        "mediated_candidate_id": MEDIATED_CANDIDATE_ID,
        "objective_inventory": tuple(
            objective.to_wire() for objective in OBJECTIVE_INVENTORY
        ),
        "parent_coefficient_denominator": PARENT_ENTRY_DENOMINATOR,
        "parent_identity": PARENT_IDENTITY,
        "parent_onsite_numerators": PARENT_ONSITE_NUMERATORS,
        "parent_positive_hopping_numerators": PARENT_POSITIVE_HOPPING_NUMERATORS,
        "support_inventory": SUPPORT_INVENTORY,
        "threshold": ExactRational(1, 100_000_000).to_dict(),
        "unit_id": UNIT_ID,
    }


def _fields(
    values: Mapping[str, SerializableValue],
    expected: set[str],
    label: str,
) -> None:
    if set(values) != expected:
        raise ValueError(f"{label} fields do not match the contract")


def _str_value(values: Mapping[str, SerializableValue], key: str) -> str:
    value = values[key]
    if type(value) is not str:
        raise TypeError(f"{key} must decode to a built-in str")
    return value


def _int_value(values: Mapping[str, SerializableValue], key: str) -> int:
    value = values[key]
    if type(value) is not int:
        raise TypeError(f"{key} must decode to a built-in int excluding bool")
    return value


def _bool_value(values: Mapping[str, SerializableValue], key: str) -> bool:
    value = values[key]
    if type(value) is not bool:
        raise TypeError(f"{key} must decode to a built-in bool")
    return value


def _mapping_value(
    values: Mapping[str, SerializableValue], key: str
) -> Mapping[str, SerializableValue]:
    value = values[key]
    if not isinstance(value, Mapping):
        raise TypeError(f"{key} must decode to a mapping")
    return value


def _tuple_value(
    values: Mapping[str, SerializableValue], key: str
) -> tuple[SerializableValue, ...]:
    value = values[key]
    if not isinstance(value, tuple):
        raise TypeError(f"{key} must decode to a tuple")
    return value


def _fixed_value(
    values: Mapping[str, SerializableValue],
    key: str,
    expected: int | str,
) -> None:
    value = values[key]
    if value != expected or type(value) is not type(expected):
        raise ValueError(f"{key} does not match the certification contract")


def _require_identifier(name: str, value: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if _IDENTIFIER_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must be a portable identifier")


def _require_sha256(name: str, value: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if _SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must be a 64-character lowercase SHA-256 digest")


__all__ = [
    "CertificationToolIdentity",
    "ExactRational",
    "FirstPassingIntervalEntry",
    "FirstPassingSupportDisposition",
    "FirstPassingSupportObjective",
    "FirstPassingSupportRequest",
    "FirstPassingSupportResult",
    "NonnegativeExactInterval",
]
