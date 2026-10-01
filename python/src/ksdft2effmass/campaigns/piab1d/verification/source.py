"""Check file paths and SHA-256 digests recorded in PIAB1D provenance."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath

from .decoder import JsonValue, Piab1dResultDecoder


class Piab1dSourceIdentityRole(StrEnum):
    """Identify the declared role of one PIAB1D source file."""

    INPUT = "input"
    RUNNER = "runner"
    IMPLEMENTATION = "implementation"
    RETAINED_RESULT = "retained_result"


class Piab1dSourceIdentityDisposition(StrEnum):
    """Describe the outcome of one file-identity check."""

    MATCHED_REPOSITORY_CONTENT = "matched_repository_content"
    RECOGNIZED_HISTORICAL_IDENTITY = "recognized_historical_identity"
    CONTENT_MISMATCH = "content_mismatch"
    SOURCE_MISSING = "source_missing"


@dataclass(frozen=True, slots=True)
class Piab1dSourceIdentity:
    """Retain one role, normalized repository-relative path, and SHA-256 digest."""

    role: Piab1dSourceIdentityRole
    relative_path: str
    recorded_sha256: str

    def __post_init__(self) -> None:
        """Reject wrong runtime types, unsafe paths, and malformed digests."""
        if type(self.role) is not Piab1dSourceIdentityRole:
            raise TypeError("role must be Piab1dSourceIdentityRole")
        if type(self.relative_path) is not str or not self.relative_path:
            raise TypeError("relative_path must be a nonempty string")
        normalized = PurePosixPath(self.relative_path)
        if (
            normalized.is_absolute()
            or ".." in normalized.parts
            or normalized.as_posix() != self.relative_path
        ):
            raise ValueError("relative_path must be a normalized relative POSIX path")
        self.validate_sha256(self.recorded_sha256, "recorded_sha256")

    @staticmethod
    def validate_sha256(value: str, name: str) -> None:
        """Reject values outside the lowercase SHA-256 representation."""
        if (
            type(value) is not str
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class Piab1dSourceIdentityVerificationResult:
    """Retain one declared identity, observed digest, and comparison disposition."""

    identity: Piab1dSourceIdentity
    observed_sha256: str | None
    disposition: Piab1dSourceIdentityDisposition

    def __post_init__(self) -> None:
        """Reject inconsistent identity-comparison states."""
        if type(self.identity) is not Piab1dSourceIdentity:
            raise TypeError("identity must be Piab1dSourceIdentity")
        if self.observed_sha256 is not None:
            Piab1dSourceIdentity.validate_sha256(
                self.observed_sha256, "observed_sha256"
            )
        if type(self.disposition) is not Piab1dSourceIdentityDisposition:
            raise TypeError("disposition must be a source identity disposition")
        if self.disposition is Piab1dSourceIdentityDisposition.SOURCE_MISSING:
            if self.observed_sha256 is not None:
                raise ValueError("a missing source cannot have an observed digest")
        elif (
            self.disposition
            is not Piab1dSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            and self.observed_sha256 is None
        ):
            raise ValueError("a current-content disposition needs an observed digest")
        if (
            self.disposition
            is Piab1dSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT
            and self.observed_sha256 != self.identity.recorded_sha256
        ):
            raise ValueError("matched source content requires equal digests")
        if (
            self.disposition is Piab1dSourceIdentityDisposition.CONTENT_MISMATCH
            and self.observed_sha256 == self.identity.recorded_sha256
        ):
            raise ValueError("content mismatch requires unequal digests")
        if (
            self.disposition
            is Piab1dSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            and self.identity.role is not Piab1dSourceIdentityRole.RUNNER
        ):
            raise ValueError("historical admission is limited to runner identities")

    @property
    def passes(self) -> bool:
        """Return whether current content matched or history was admitted."""
        return self.disposition in (
            Piab1dSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT,
            Piab1dSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY,
        )


@dataclass(frozen=True, slots=True)
class Piab1dSourceAuthenticationResult:
    """Retain source comparisons and current implementation-inventory agreement."""

    identities: tuple[Piab1dSourceIdentityVerificationResult, ...]
    expected_implementation_paths: tuple[str, ...]
    observed_implementation_paths: tuple[str, ...]

    def __post_init__(self) -> None:
        """Reject malformed result collections and duplicate inventory entries."""
        if (
            type(self.identities) is not tuple
            or not self.identities
            or any(
                type(identity) is not Piab1dSourceIdentityVerificationResult
                for identity in self.identities
            )
        ):
            raise TypeError("identities must contain source identity results")
        keys = tuple(
            (result.identity.role, result.identity.relative_path)
            for result in self.identities
        )
        if len(set(keys)) != len(keys):
            raise ValueError("source identity roles and paths must be unique")
        for name, paths in (
            ("expected_implementation_paths", self.expected_implementation_paths),
            ("observed_implementation_paths", self.observed_implementation_paths),
        ):
            if type(paths) is not tuple or any(
                type(path) is not str or not path for path in paths
            ):
                raise TypeError(f"{name} must contain nonempty strings")
            if len(set(paths)) != len(paths):
                raise ValueError(f"{name} must not contain duplicates")

    @property
    def implementation_inventory_matches(self) -> bool:
        """Return exact set agreement for current implementation paths."""
        return set(self.observed_implementation_paths) == set(
            self.expected_implementation_paths
        )

    @property
    def passes(self) -> bool:
        """Return whether every file and the implementation-path set agree."""
        return self.implementation_inventory_matches and all(
            identity.passes for identity in self.identities
        )

    @property
    def declared_identity_count(self) -> int:
        """Return the number of represented source identities."""
        return len(self.identities)

    @property
    def matched_repository_content_count(self) -> int:
        """Return the number of identities matched to current repository bytes."""
        return sum(
            result.disposition
            is Piab1dSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT
            for result in self.identities
        )

    @property
    def recognized_historical_identity_count(self) -> int:
        """Return the number of explicitly admitted historical runner identities."""
        return sum(
            result.disposition
            is Piab1dSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            for result in self.identities
        )


class Piab1dSourceAuthenticator:
    """Check the files declared by a version-one PIAB1D result."""

    __slots__ = ()

    def execute(
        self,
        provenance: dict[str, JsonValue],
        repository_root: Path,
        expected_implementation_paths: tuple[str, ...],
        recognized_historical_runner_sha256: str,
        additional_identities: tuple[Piab1dSourceIdentity, ...] = (),
    ) -> Piab1dSourceAuthenticationResult:
        """Return source comparisons without performing numerical reconstruction.

        Parameters
        ----------
        provenance
            Version-one provenance object from a strictly decoded result document.
        repository_root
            Existing repository directory that contains every resolved source path.
        expected_implementation_paths
            Exact current implementation inventory. Historical records without an
            implementation inventory do not use this collection.
        recognized_historical_runner_sha256
            Explicitly admitted historical runner identity.
        additional_identities
            Other campaign inputs, such as a retained parent result.
        """
        if type(provenance) is not dict:
            raise TypeError("provenance must be a JSON object")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        root = repository_root.resolve()
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        if type(expected_implementation_paths) is not tuple or any(
            type(path) is not str or not path for path in expected_implementation_paths
        ):
            raise TypeError("expected implementation paths must be nonempty strings")
        if len(set(expected_implementation_paths)) != len(
            expected_implementation_paths
        ):
            raise ValueError("expected implementation paths must be unique")
        Piab1dSourceIdentity.validate_sha256(
            recognized_historical_runner_sha256,
            "recognized_historical_runner_sha256",
        )
        if type(additional_identities) is not tuple or any(
            type(identity) is not Piab1dSourceIdentity
            for identity in additional_identities
        ):
            raise TypeError("additional_identities must contain source identities")

        # Provenance always declares exactly one input and one runner. Current records
        # additionally enumerate every implementation source used by the producer.
        decoder = Piab1dResultDecoder
        identities = [
            Piab1dSourceIdentity(
                Piab1dSourceIdentityRole.INPUT,
                decoder.string(provenance["input_path"], "input_path"),
                decoder.sha256_string(provenance["input_sha256"], "input_sha256"),
            ),
            Piab1dSourceIdentity(
                Piab1dSourceIdentityRole.RUNNER,
                decoder.string(provenance["script_path"], "script_path"),
                decoder.sha256_string(provenance["script_sha256"], "script_sha256"),
            ),
        ]
        identities.extend(additional_identities)
        encoded_implementations = provenance.get("implementation_identities")
        if encoded_implementations is None:
            expected_paths: tuple[str, ...] = ()
            historical_runner: str | None = recognized_historical_runner_sha256
        else:
            expected_paths = expected_implementation_paths
            historical_runner = None
            for value in decoder.sequence(
                encoded_implementations, "implementation_identities"
            ):
                encoded = decoder.mapping(value, "implementation identity")
                identities.append(
                    Piab1dSourceIdentity(
                        Piab1dSourceIdentityRole.IMPLEMENTATION,
                        decoder.string(encoded["path"], "implementation path"),
                        decoder.sha256_string(
                            encoded["sha256"], "implementation sha256"
                        ),
                    )
                )

        keys = tuple((identity.role, identity.relative_path) for identity in identities)
        if len(set(keys)) != len(keys):
            raise ValueError("source identity roles and paths must be unique")
        observed_paths = tuple(
            identity.relative_path
            for identity in identities
            if identity.role is Piab1dSourceIdentityRole.IMPLEMENTATION
        )

        comparisons: list[Piab1dSourceIdentityVerificationResult] = []
        for identity in identities:
            # Resolve first, then prove containment. This prevents ``..`` components or
            # symlinks from authenticating content outside the declared repository.
            source = (root / identity.relative_path).resolve()
            try:
                source.relative_to(root)
            except ValueError as error:
                raise ValueError(
                    "source identity paths must remain beneath repository_root"
                ) from error
            observed = (
                hashlib.sha256(source.read_bytes()).hexdigest()
                if source.is_file()
                else None
            )
            if (
                identity.role is Piab1dSourceIdentityRole.RUNNER
                and identity.recorded_sha256 == historical_runner
            ):
                disposition = (
                    Piab1dSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
                )
            elif observed is None:
                disposition = Piab1dSourceIdentityDisposition.SOURCE_MISSING
            elif observed == identity.recorded_sha256:
                disposition = Piab1dSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT
            else:
                disposition = Piab1dSourceIdentityDisposition.CONTENT_MISMATCH
            comparisons.append(
                Piab1dSourceIdentityVerificationResult(identity, observed, disposition)
            )

        return Piab1dSourceAuthenticationResult(
            tuple(comparisons), expected_paths, observed_paths
        )
