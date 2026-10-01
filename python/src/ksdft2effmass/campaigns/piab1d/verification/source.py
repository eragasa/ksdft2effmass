"""Source-identity records and authentication for independent PIAB1D verification."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class ParticleInBoxSourceIdentityRole(StrEnum):
    """Identify one declared source role in a PIAB1D result."""

    INPUT = "input"
    RUNNER = "runner"
    IMPLEMENTATION = "implementation"


class ParticleInBoxSourceIdentityDisposition(StrEnum):
    """Classify one source-identity comparison without conflating its basis."""

    MATCHED_REPOSITORY_CONTENT = "matched_repository_content"
    RECOGNIZED_HISTORICAL_IDENTITY = "recognized_historical_identity"
    CONTENT_MISMATCH = "content_mismatch"
    SOURCE_MISSING = "source_missing"


@dataclass(frozen=True, slots=True)
class ParticleInBoxSourceIdentity:
    """Retain one declared repository-relative source identity.

    Parameters
    ----------
    role
        Declared role of the source in the result document.
    relative_path
        Nonempty POSIX repository-relative source path.
    recorded_sha256
        Lowercase SHA-256 digest recorded in the result document.
    """

    role: ParticleInBoxSourceIdentityRole
    relative_path: str
    recorded_sha256: str

    def __post_init__(self) -> None:
        """Validate exact role, path, and digest fields."""
        if type(self.role) is not ParticleInBoxSourceIdentityRole:
            raise TypeError("role must be ParticleInBoxSourceIdentityRole")
        if type(self.relative_path) is not str or not self.relative_path:
            raise TypeError("relative_path must be a nonempty string")
        self.validate_sha256(self.recorded_sha256, "recorded_sha256")

    @staticmethod
    def validate_sha256(value: str, name: str) -> None:
        """Validate one lowercase SHA-256 digest field."""
        if (
            type(value) is not str
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class ParticleInBoxSourceAuthenticationRequest:
    """Declare source identities and the applicable authentication inventory.

    Parameters
    ----------
    identities
        Ordered input, runner, and optional implementation identities.
    expected_implementation_paths
        Exact current implementation inventory. Historical results use an empty tuple.
    recognized_historical_runner_sha256
        Explicitly admitted immutable runner digest, or ``None`` when every identity
        must match currently available repository bytes.
    """

    identities: tuple[ParticleInBoxSourceIdentity, ...]
    expected_implementation_paths: tuple[str, ...]
    recognized_historical_runner_sha256: str | None

    def __post_init__(self) -> None:
        """Validate identity ordering, uniqueness, and historical admission."""
        if not isinstance(self.identities, tuple) or not self.identities:
            raise TypeError("identities must be a nonempty tuple")
        if any(
            type(value) is not ParticleInBoxSourceIdentity for value in self.identities
        ):
            raise TypeError(
                "identities must contain ParticleInBoxSourceIdentity values"
            )
        keys = tuple((value.role, value.relative_path) for value in self.identities)
        if len(set(keys)) != len(keys):
            raise ValueError("source identity roles and paths must be unique")
        roles = tuple(value.role for value in self.identities)
        if roles.count(ParticleInBoxSourceIdentityRole.INPUT) != 1:
            raise ValueError(
                "source authentication requires exactly one input identity"
            )
        if roles.count(ParticleInBoxSourceIdentityRole.RUNNER) != 1:
            raise ValueError(
                "source authentication requires exactly one runner identity"
            )
        if not isinstance(self.expected_implementation_paths, tuple) or any(
            type(path) is not str or not path
            for path in self.expected_implementation_paths
        ):
            raise TypeError(
                "expected_implementation_paths must be a tuple of nonempty strings"
            )
        if len(set(self.expected_implementation_paths)) != len(
            self.expected_implementation_paths
        ):
            raise ValueError(
                "expected_implementation_paths must not contain duplicates"
            )
        observed_paths = self.observed_implementation_paths
        if len(set(observed_paths)) != len(observed_paths):
            raise ValueError(
                "implementation identity paths must not contain duplicates"
            )
        if self.recognized_historical_runner_sha256 is not None:
            ParticleInBoxSourceIdentity.validate_sha256(
                self.recognized_historical_runner_sha256,
                "recognized_historical_runner_sha256",
            )
            if observed_paths or self.expected_implementation_paths:
                raise ValueError(
                    "historical runner admission cannot include implementation paths"
                )

    @property
    def observed_implementation_paths(self) -> tuple[str, ...]:
        """Return implementation paths derived from the identity collection."""
        return tuple(
            identity.relative_path
            for identity in self.identities
            if identity.role is ParticleInBoxSourceIdentityRole.IMPLEMENTATION
        )


@dataclass(frozen=True, slots=True)
class ParticleInBoxSourceIdentityVerificationResult:
    """Retain one source-identity comparison.

    Parameters
    ----------
    identity
        Declared source identity being authenticated.
    observed_sha256
        Digest of currently available repository bytes, or ``None`` when absent.
    disposition
        Exact relationship between declared identity and available bytes.
    """

    identity: ParticleInBoxSourceIdentity
    observed_sha256: str | None
    disposition: ParticleInBoxSourceIdentityDisposition

    def __post_init__(self) -> None:
        """Validate digest and disposition consistency."""
        if type(self.identity) is not ParticleInBoxSourceIdentity:
            raise TypeError("identity must be ParticleInBoxSourceIdentity")
        if self.observed_sha256 is not None:
            ParticleInBoxSourceIdentity.validate_sha256(
                self.observed_sha256, "observed_sha256"
            )
        if type(self.disposition) is not ParticleInBoxSourceIdentityDisposition:
            raise TypeError(
                "disposition must be ParticleInBoxSourceIdentityDisposition"
            )
        if self.disposition is ParticleInBoxSourceIdentityDisposition.SOURCE_MISSING:
            if self.observed_sha256 is not None:
                raise ValueError("a missing source cannot have an observed digest")
        elif (
            self.disposition
            is not ParticleInBoxSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            and self.observed_sha256 is None
        ):
            raise ValueError("a current-content disposition needs an observed digest")
        if (
            self.disposition
            is ParticleInBoxSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT
            and self.observed_sha256 != self.identity.recorded_sha256
        ):
            raise ValueError("matched repository content must have equal digests")
        if (
            self.disposition is ParticleInBoxSourceIdentityDisposition.CONTENT_MISMATCH
            and self.observed_sha256 == self.identity.recorded_sha256
        ):
            raise ValueError("content mismatch requires unequal digests")
        if (
            self.disposition
            is ParticleInBoxSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            and self.identity.role is not ParticleInBoxSourceIdentityRole.RUNNER
        ):
            raise ValueError("historical admission is limited to runner identities")

    @property
    def role(self) -> ParticleInBoxSourceIdentityRole:
        """Return the declared identity role."""
        return self.identity.role

    @property
    def relative_path(self) -> str:
        """Return the declared repository-relative path."""
        return self.identity.relative_path

    @property
    def recorded_sha256(self) -> str:
        """Return the declared source digest."""
        return self.identity.recorded_sha256

    @property
    def passes(self) -> bool:
        """Return whether this identity is matched or explicitly admitted."""
        return self.disposition in (
            ParticleInBoxSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT,
            ParticleInBoxSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY,
        )


@dataclass(frozen=True, slots=True)
class ParticleInBoxSourceAuthenticationResult:
    """Retain source comparisons and implementation-inventory agreement."""

    identities: tuple[ParticleInBoxSourceIdentityVerificationResult, ...]
    expected_implementation_paths: tuple[str, ...]
    observed_implementation_paths: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate immutable identities and unique implementation inventories."""
        if not isinstance(self.identities, tuple) or not self.identities:
            raise TypeError("identities must be a nonempty tuple")
        if any(
            type(identity) is not ParticleInBoxSourceIdentityVerificationResult
            for identity in self.identities
        ):
            raise TypeError("identities must contain source identity results")
        keys = tuple(
            (identity.role, identity.relative_path) for identity in self.identities
        )
        if len(set(keys)) != len(keys):
            raise ValueError("source identity roles and paths must be unique")
        for name, paths in (
            ("expected_implementation_paths", self.expected_implementation_paths),
            ("observed_implementation_paths", self.observed_implementation_paths),
        ):
            if not isinstance(paths, tuple) or any(
                type(path) is not str or not path for path in paths
            ):
                raise TypeError(f"{name} must be a tuple of nonempty strings")
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
        """Return the aggregate bounded source-authentication disposition."""
        return self.implementation_inventory_matches and all(
            identity.passes for identity in self.identities
        )

    @property
    def declared_identity_count(self) -> int:
        """Return the count derived from the retained identity collection."""
        return len(self.identities)

    @property
    def matched_repository_content_count(self) -> int:
        """Return the number of identities matched to current repository bytes."""
        return sum(
            identity.disposition
            is ParticleInBoxSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT
            for identity in self.identities
        )

    @property
    def recognized_historical_identity_count(self) -> int:
        """Return the number of admitted historical runner identities."""
        return sum(
            identity.disposition
            is ParticleInBoxSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            for identity in self.identities
        )


class ParticleInBoxSourceAuthenticator:
    """Authenticate declared PIAB1D source identities against repository bytes."""

    __slots__ = ()

    def execute(
        self,
        request: ParticleInBoxSourceAuthenticationRequest,
        repository_root: Path,
    ) -> ParticleInBoxSourceAuthenticationResult:
        """Return source comparisons without performing numerical verification."""
        if type(request) is not ParticleInBoxSourceAuthenticationRequest:
            raise TypeError("request must be ParticleInBoxSourceAuthenticationRequest")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        root = repository_root.resolve()
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        results = tuple(
            self.compare(identity, request.recognized_historical_runner_sha256, root)
            for identity in request.identities
        )
        return ParticleInBoxSourceAuthenticationResult(
            results,
            request.expected_implementation_paths,
            request.observed_implementation_paths,
        )

    def compare(
        self,
        identity: ParticleInBoxSourceIdentity,
        recognized_historical_runner_sha256: str | None,
        repository_root: Path,
    ) -> ParticleInBoxSourceIdentityVerificationResult:
        """Compare one declared identity with one contained repository path."""
        source = self.contained_source_path(identity.relative_path, repository_root)
        observed = (
            hashlib.sha256(source.read_bytes()).hexdigest()
            if source.is_file()
            else None
        )
        if (
            identity.role is ParticleInBoxSourceIdentityRole.RUNNER
            and identity.recorded_sha256 == recognized_historical_runner_sha256
        ):
            disposition = (
                ParticleInBoxSourceIdentityDisposition.RECOGNIZED_HISTORICAL_IDENTITY
            )
        elif observed is None:
            disposition = ParticleInBoxSourceIdentityDisposition.SOURCE_MISSING
        elif observed == identity.recorded_sha256:
            disposition = (
                ParticleInBoxSourceIdentityDisposition.MATCHED_REPOSITORY_CONTENT
            )
        else:
            disposition = ParticleInBoxSourceIdentityDisposition.CONTENT_MISMATCH
        return ParticleInBoxSourceIdentityVerificationResult(
            identity, observed, disposition
        )

    @staticmethod
    def contained_source_path(relative_path: str, repository_root: Path) -> Path:
        """Resolve one declared relative source path beneath the repository root."""
        candidate = Path(relative_path)
        if candidate.is_absolute():
            raise ValueError("source identity paths must be repository-relative")
        resolved = (repository_root / candidate).resolve()
        try:
            resolved.relative_to(repository_root)
        except ValueError as error:
            raise ValueError(
                "source identity paths must remain beneath repository_root"
            ) from error
        return resolved
