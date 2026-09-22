"""Immutable native-toolchain declarations and execution-free build planning.

The objects in this module represent declared local tools, CMake definitions, bounded
build inputs, and deterministic argument vectors.  Construction and planning perform
no path discovery, local-file hashing, installation, network access, workspace
creation, compiler invocation, or build execution. A represented plan does not
establish that any tool or source exists, that a content digest matches local bytes,
or that execution is
authorized.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath

_MAX_U64 = 18_446_744_073_709_551_615
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:+-]{0,127}\Z", re.ASCII)
_VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,127}\Z", re.ASCII)
_DEFINITION_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]*\Z", re.ASCII)
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_TOOLCHAIN_ID_PATTERN = re.compile(r"tc-[0-9a-f]{12,64}\Z", re.ASCII)
_BUILD_ID_PATTERN = re.compile(r"build-[0-9a-f]{12,64}\Z", re.ASCII)


class NativeToolRole(StrEnum):
    """Closed roles consumed by deterministic native build planning.

    Attributes
    ----------
    BLAS_LAPACK
        Selected BLAS and LAPACK library implementation.
    BUILD_SYSTEM
        Build-system executable used to render configuration and build vectors.
    C_COMPILER
        Underlying C compiler in the maintained toolchain.
    FFT
        Selected external fast-Fourier-transform library.
    FORTRAN_COMPILER
        Underlying Fortran compiler in the maintained toolchain.
    MPI_C_WRAPPER
        MPI C compiler wrapper used by an MPI-enabled build.
    MPI_FORTRAN_WRAPPER
        MPI Fortran compiler wrapper used by an MPI-enabled build.
    """

    BLAS_LAPACK = "blas_lapack"
    BUILD_SYSTEM = "build_system"
    C_COMPILER = "c_compiler"
    FFT = "fft"
    FORTRAN_COMPILER = "fortran_compiler"
    MPI_C_WRAPPER = "mpi_c_wrapper"
    MPI_FORTRAN_WRAPPER = "mpi_fortran_wrapper"


@dataclass(frozen=True, slots=True)
class NativeToolContentNotPinned:
    """Represent a declared tool whose exact local bytes are not pinned.

    Notes
    -----
    This marker is an explicit evidence limitation.  It is not a wildcard content
    identity and does not establish installation availability or compatibility.
    """


@dataclass(frozen=True, slots=True)
class NativeToolSha256ContentIdentity:
    """Represent a declared SHA-256 identity without reading local bytes.

    Parameters
    ----------
    digest
        Exactly 64 lowercase hexadecimal SHA-256 characters.
    """

    digest: str

    def __post_init__(self) -> None:
        """Validate the exact digest representation."""
        if type(self.digest) is not str:
            raise TypeError("digest must be a built-in str")
        if _SHA256_PATTERN.fullmatch(self.digest) is None:
            raise ValueError("digest must be a lowercase SHA-256 value")


type NativeToolContentIdentity = (
    NativeToolContentNotPinned | NativeToolSha256ContentIdentity
)
"""Closed exact-pinned or explicitly unpinned tool-content declaration."""


@dataclass(frozen=True, slots=True)
class NativeToolSpecification:
    """Declare one tool consumed by a native build plan.

    Parameters
    ----------
    role
        Exact functional role in the toolchain.
    name
        Portable tool-family name.
    version
        Exact declared lexical version.  It is not resolved or ordered.
    path
        Absolute local executable or library path.  The path is not inspected.
    content_identity
        Exact SHA-256 declaration or explicit not-pinned marker.
    """

    role: NativeToolRole
    name: str
    version: str
    path: Path
    content_identity: NativeToolContentIdentity

    def __post_init__(self) -> None:
        """Validate this tool's intrinsic declaration fields."""
        if type(self.role) is not NativeToolRole:
            raise TypeError("role must be a NativeToolRole")
        if type(self.name) is not str:
            raise TypeError("name must be a built-in str")
        if _ID_PATTERN.fullmatch(self.name) is None:
            raise ValueError("name must be a portable tool identifier")
        if type(self.version) is not str:
            raise TypeError("version must be a built-in str")
        if _VERSION_PATTERN.fullmatch(self.version) is None:
            raise ValueError("version must be portable lexical version text")
        if not isinstance(self.path, Path):
            raise TypeError("path must be pathlib.Path")
        if not self.path.is_absolute() or ".." in self.path.parts:
            raise ValueError("path must be absolute without parent traversal")
        if any(character in self.path.as_posix() for character in "\x00\t\r\n"):
            raise ValueError("path must not contain NUL, tab, or line terminators")
        if type(self.content_identity) not in (
            NativeToolContentNotPinned,
            NativeToolSha256ContentIdentity,
        ):
            raise TypeError("content_identity must be a closed content declaration")


@dataclass(frozen=True, slots=True)
class NativeToolchainSpecification:
    """Represent one immutable, role-indexed native toolchain declaration.

    Parameters
    ----------
    identity
        Portable identity of this complete declaration.
    root
        Absolute common package root. Every tool path must descend from this root.
    tools
        Nonempty tuple ordered lexically by role value, with each role appearing once.
    """

    identity: str
    root: Path
    tools: tuple[NativeToolSpecification, ...]

    def __post_init__(self) -> None:
        """Validate toolchain identity, tuple ownership, ordering, and uniqueness."""
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.identity) is None:
            raise ValueError("identity must be a portable toolchain identifier")
        if not isinstance(self.root, Path):
            raise TypeError("root must be pathlib.Path")
        if not self.root.is_absolute() or ".." in self.root.parts:
            raise ValueError("root must be absolute without parent traversal")
        if any(character in self.root.as_posix() for character in "\x00\t\r\n"):
            raise ValueError("root must not contain NUL, tab, or line terminators")
        if type(self.tools) is not tuple:
            raise TypeError("tools must be a built-in tuple")
        if not self.tools:
            raise ValueError("tools must not be empty")
        if any(type(tool) is not NativeToolSpecification for tool in self.tools):
            raise TypeError("tools must contain exact NativeToolSpecification values")
        roles = tuple(tool.role.value for tool in self.tools)
        if roles != tuple(sorted(roles)) or len(set(roles)) != len(roles):
            raise ValueError("tools must have unique roles in lexical order")
        if any(not tool.path.is_relative_to(self.root) for tool in self.tools):
            raise ValueError("every tool path must descend from root")

    def tool_for(self, role: NativeToolRole) -> NativeToolSpecification:
        """Return the exact declared tool for ``role``.

        Raises
        ------
        TypeError
            If ``role`` is not an exact :class:`NativeToolRole`.
        ValueError
            If the toolchain has no declaration for ``role``.
        """
        if type(role) is not NativeToolRole:
            raise TypeError("role must be a NativeToolRole")
        for tool in self.tools:
            if tool.role is role:
                return tool
        raise ValueError(f"toolchain does not declare role {role.value}")


@dataclass(frozen=True, slots=True)
class NativeToolchainFingerprint:
    """Record the canonical declared runtime-toolchain fingerprint.

    Parameters
    ----------
    fingerprinter_identity
        Exact identity of the fingerprinting implementation.
    algorithm
        Exact string ``"sha256"``.
    digest
        Complete lowercase SHA-256 digest of ``canonical_components``.
    short_identity
        Human-usable ``tc-`` identity containing the first 12 digest characters.
    canonical_components
        Complete ordered runtime components hashed with one final newline between and
        after entries. Absolute roots, logical declaration labels, and build-system
        tools are excluded; retained tool paths are root-relative.

    Notes
    -----
    The short identity names a declared specification, not verified installed bytes.
    A future installer must reject a pre-existing short identity whose complete digest
    or manifest differs, and must lengthen the digest prefix rather than overwrite it.
    """

    fingerprinter_identity: str
    algorithm: str
    digest: str
    short_identity: str
    canonical_components: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate the exact digest, short identity, and canonical components."""
        if type(self.fingerprinter_identity) is not str:
            raise TypeError("fingerprinter_identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.fingerprinter_identity) is None:
            raise ValueError("fingerprinter_identity must be a portable identifier")
        if type(self.algorithm) is not str:
            raise TypeError("algorithm must be a built-in str")
        if self.algorithm != "sha256":
            raise ValueError("algorithm must equal sha256")
        if type(self.digest) is not str:
            raise TypeError("digest must be a built-in str")
        if _SHA256_PATTERN.fullmatch(self.digest) is None:
            raise ValueError("digest must be a lowercase SHA-256 value")
        if type(self.short_identity) is not str:
            raise TypeError("short_identity must be a built-in str")
        if _TOOLCHAIN_ID_PATTERN.fullmatch(self.short_identity) is None:
            raise ValueError("short_identity must have form tc- followed by 12 hex")
        if self.short_identity != f"tc-{self.digest[:12]}":
            raise ValueError("short_identity must be the default 12-character prefix")
        if type(self.canonical_components) is not tuple:
            raise TypeError("canonical_components must be a built-in tuple")
        if not self.canonical_components:
            raise ValueError("canonical_components must not be empty")
        if any(type(value) is not str for value in self.canonical_components):
            raise TypeError("canonical_components members must be built-in strings")
        if any(
            not value or any(character in value for character in "\x00\r\n")
            for value in self.canonical_components
        ):
            raise ValueError("canonical_components must be nonempty single-line text")

    def filesystem_identity(self, prefix_length: int) -> str:
        """Return ``tc-`` plus an explicit 12-to-64-character digest prefix.

        A caller may select a longer prefix only after comparing complete manifests.
        This method performs no collision discovery or filesystem access.
        """
        if type(prefix_length) is not int:
            raise TypeError("prefix_length must be a built-in int")
        if not 12 <= prefix_length <= 64:
            raise ValueError("prefix_length must be in the inclusive range 12..64")
        return f"tc-{self.digest[:prefix_length]}"


@dataclass(frozen=True, slots=True)
class NativeToolchainFingerprinter:
    """Derive a root-independent digest of one declared runtime toolchain.

    Parameters
    ----------
    identity
        Portable identity and version of this canonicalization implementation.
    """

    identity: str

    def __post_init__(self) -> None:
        """Validate the fingerprinting implementation identity."""
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.identity) is None:
            raise ValueError("identity must be a portable fingerprinter identifier")

    def execute(
        self, toolchain: NativeToolchainSpecification
    ) -> NativeToolchainFingerprint:
        """Return the canonical declared-toolchain fingerprint.

        Parameters
        ----------
        toolchain
            Complete toolchain declaration with every path beneath its explicit root.
            Build-system roles remain build provenance and are excluded from the
            runtime identity.

        Returns
        -------
        NativeToolchainFingerprint
            Complete digest, short identity, and exact canonical components.

        Raises
        ------
        TypeError
            If ``toolchain`` is not the exact public specification type.
        """
        if type(toolchain) is not NativeToolchainSpecification:
            raise TypeError("toolchain must be a NativeToolchainSpecification")
        components = ["native-runtime-toolchain-fingerprint:1"]
        runtime_tools = tuple(
            tool
            for tool in toolchain.tools
            if tool.role is not NativeToolRole.BUILD_SYSTEM
        )
        if not runtime_tools:
            raise ValueError("toolchain must declare at least one runtime tool")
        for tool in runtime_tools:
            if type(tool.content_identity) is NativeToolSha256ContentIdentity:
                content = f"sha256:{tool.content_identity.digest}"
            else:
                content = "content:not-pinned"
            relative_path = tool.path.relative_to(toolchain.root).as_posix()
            components.append(
                "\t".join(
                    (
                        tool.role.value,
                        tool.name,
                        tool.version,
                        relative_path,
                        content,
                    )
                )
            )
        canonical_components = tuple(components)
        canonical_bytes = ("\n".join(canonical_components) + "\n").encode("utf-8")
        digest = hashlib.sha256(canonical_bytes).hexdigest()
        return NativeToolchainFingerprint(
            fingerprinter_identity=self.identity,
            algorithm="sha256",
            digest=digest,
            short_identity=f"tc-{digest[:12]}",
            canonical_components=canonical_components,
        )


@dataclass(frozen=True, slots=True)
class NativeCMakeDefinition:
    """Represent one exact ``-DNAME=VALUE`` CMake definition.

    Parameters
    ----------
    name
        Nonempty CMake variable name beginning with an ASCII letter.
    value
        Nonempty single-line built-in string stored without canonicalization.
    """

    name: str
    value: str

    def __post_init__(self) -> None:
        """Validate this definition's exact name and value boundaries."""
        if type(self.name) is not str:
            raise TypeError("name must be a built-in str")
        if _DEFINITION_PATTERN.fullmatch(self.name) is None:
            raise ValueError("name must be a portable CMake variable name")
        if type(self.value) is not str:
            raise TypeError("value must be a built-in str")
        if not self.value or any(character in self.value for character in "\x00\t\r\n"):
            raise ValueError("value must be nonempty text without control delimiters")

    @property
    def argument(self) -> str:
        """Return this definition's exact CMake argument."""
        return f"-D{self.name}={self.value}"


@dataclass(frozen=True, slots=True, kw_only=True)
class NativeBuildLimits:
    """Represent operational ceilings for a proposed local native build.

    Parameters
    ----------
    maximum_parallel_jobs
        Positive maximum number of local build jobs.
    wall_time_milliseconds
        Positive build wall-time ceiling in milliseconds.
    maximum_resident_bytes
        Positive resident-memory ceiling in bytes.
    maximum_output_bytes
        Positive aggregate build-output ceiling in bytes.

    Notes
    -----
    Every field accepts only a built-in :class:`int` in the inclusive range
    :math:`[1, 2^{64}-1]`. Booleans, numeric strings, zero, negative values, and
    larger integers are rejected rather than coerced or wrapped.
    """

    maximum_parallel_jobs: int
    wall_time_milliseconds: int
    maximum_resident_bytes: int
    maximum_output_bytes: int

    def __post_init__(self) -> None:
        """Validate exact positive unsigned operational limits."""
        for value, name in (
            (self.maximum_parallel_jobs, "maximum_parallel_jobs"),
            (self.wall_time_milliseconds, "wall_time_milliseconds"),
            (self.maximum_resident_bytes, "maximum_resident_bytes"),
            (self.maximum_output_bytes, "maximum_output_bytes"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if not 0 < value <= _MAX_U64:
                raise ValueError(f"{name} must be in the positive u64 range")


@dataclass(frozen=True, slots=True, kw_only=True)
class NativeBuildRecipe:
    """Represent artifact-defining inputs independently of filesystem placement.

    Parameters
    ----------
    identity
        Portable human-readable profile identity. It is excluded from the digest.
    source_snapshot_reference
        Explicit retained source-snapshot reference. It is not a verified content
        digest, and an installer must strengthen it before immutable publication.
    platform_identity
        Portable operating-system and architecture identity.
    definitions
        Tuple of unique CMake definitions ordered lexically by name.
    target
        One portable CMake target name.
    output_paths
        Nonempty tuple of unique root-relative POSIX output paths in lexical order.
    """

    identity: str
    source_snapshot_reference: str
    platform_identity: str
    definitions: tuple[NativeCMakeDefinition, ...]
    target: str
    output_paths: tuple[PurePosixPath, ...]

    def __post_init__(self) -> None:
        """Validate the complete artifact-defining recipe declaration."""
        for text_value, name in (
            (self.identity, "identity"),
            (self.source_snapshot_reference, "source_snapshot_reference"),
            (self.platform_identity, "platform_identity"),
            (self.target, "target"),
        ):
            if type(text_value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if _ID_PATTERN.fullmatch(text_value) is None:
                raise ValueError(f"{name} must be a portable identifier")
        if type(self.definitions) is not tuple:
            raise TypeError("definitions must be a built-in tuple")
        if any(type(value) is not NativeCMakeDefinition for value in self.definitions):
            raise TypeError(
                "definitions must contain exact NativeCMakeDefinition values"
            )
        names = tuple(value.name for value in self.definitions)
        if names != tuple(sorted(names)) or len(set(names)) != len(names):
            raise ValueError("definitions must have unique names in lexical order")
        if type(self.output_paths) is not tuple:
            raise TypeError("output_paths must be a built-in tuple")
        if not self.output_paths:
            raise ValueError("output_paths must not be empty")
        for path in self.output_paths:
            if type(path) is not PurePosixPath:
                raise TypeError("output_paths must contain exact PurePosixPath values")
            if path.is_absolute() or any(
                part in {"", ".", ".."} for part in path.parts
            ):
                raise ValueError("output_paths must be root-relative portable paths")
            if any(character in path.as_posix() for character in "\x00\t\r\n"):
                raise ValueError("output_paths must not contain control delimiters")
        rendered_outputs = tuple(path.as_posix() for path in self.output_paths)
        if rendered_outputs != tuple(sorted(rendered_outputs)) or len(
            set(rendered_outputs)
        ) != len(rendered_outputs):
            raise ValueError("output_paths must be unique and lexically ordered")


@dataclass(frozen=True, slots=True)
class NativeBuildFingerprint:
    """Record the complete digest of one declared artifact-building recipe.

    Parameters
    ----------
    fingerprinter_identity
        Exact identity of the canonicalization implementation.
    algorithm
        Exact string ``"sha256"``.
    digest
        Complete lowercase SHA-256 digest.
    short_identity
        Default ``build-`` identity containing the first 12 digest characters.
    canonical_components
        Complete ordered components used to derive ``digest``.
    """

    fingerprinter_identity: str
    algorithm: str
    digest: str
    short_identity: str
    canonical_components: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate the complete digest and default filesystem identity."""
        if type(self.fingerprinter_identity) is not str:
            raise TypeError("fingerprinter_identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.fingerprinter_identity) is None:
            raise ValueError("fingerprinter_identity must be a portable identifier")
        if type(self.algorithm) is not str:
            raise TypeError("algorithm must be a built-in str")
        if self.algorithm != "sha256":
            raise ValueError("algorithm must equal sha256")
        if type(self.digest) is not str:
            raise TypeError("digest must be a built-in str")
        if _SHA256_PATTERN.fullmatch(self.digest) is None:
            raise ValueError("digest must be a lowercase SHA-256 value")
        if type(self.short_identity) is not str:
            raise TypeError("short_identity must be a built-in str")
        if self.short_identity != f"build-{self.digest[:12]}":
            raise ValueError("short_identity must be the default 12-character prefix")
        if type(self.canonical_components) is not tuple:
            raise TypeError("canonical_components must be a built-in tuple")
        if not self.canonical_components:
            raise ValueError("canonical_components must not be empty")
        if any(type(value) is not str for value in self.canonical_components):
            raise TypeError("canonical_components members must be built-in strings")
        if any(
            not value or any(character in value for character in "\x00\r\n")
            for value in self.canonical_components
        ):
            raise ValueError("canonical_components must be nonempty single-line text")

    def filesystem_identity(self, prefix_length: int) -> str:
        """Return ``build-`` plus an explicit digest prefix of length 12 through 64."""
        if type(prefix_length) is not int:
            raise TypeError("prefix_length must be a built-in int")
        if not 12 <= prefix_length <= 64:
            raise ValueError("prefix_length must be in the inclusive range 12..64")
        return f"build-{self.digest[:prefix_length]}"


@dataclass(frozen=True, slots=True)
class NativeBuildFingerprinter:
    """Derive a build identity distinct from the runtime-toolchain identity.

    Parameters
    ----------
    identity
        Portable identity and version of this canonicalization implementation.
    """

    identity: str

    def __post_init__(self) -> None:
        """Validate the fingerprinting implementation identity."""
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.identity) is None:
            raise ValueError("identity must be a portable fingerprinter identifier")

    def execute(
        self,
        toolchain: NativeToolchainSpecification,
        toolchain_fingerprint: NativeToolchainFingerprint,
        recipe: NativeBuildRecipe,
    ) -> NativeBuildFingerprint:
        """Return the digest of build tools, runtime tools, source, and recipe.

        Parameters
        ----------
        toolchain
            Complete declaration supplying the build-system provenance and root used
            to canonicalize root-relative definition values.
        toolchain_fingerprint
            Complete runtime-toolchain digest.
        recipe
            Artifact-defining source, platform, definitions, target, and outputs.

        Returns
        -------
        NativeBuildFingerprint
            Complete digest and collision-adjustable filesystem identity.
        """
        if type(toolchain) is not NativeToolchainSpecification:
            raise TypeError("toolchain must be a NativeToolchainSpecification")
        if type(toolchain_fingerprint) is not NativeToolchainFingerprint:
            raise TypeError(
                "toolchain_fingerprint must be a NativeToolchainFingerprint"
            )
        if type(recipe) is not NativeBuildRecipe:
            raise TypeError("recipe must be a NativeBuildRecipe")
        build_system = toolchain.tool_for(NativeToolRole.BUILD_SYSTEM)
        if type(build_system.content_identity) is NativeToolSha256ContentIdentity:
            build_system_content = f"sha256:{build_system.content_identity.digest}"
        else:
            build_system_content = "content:not-pinned"
        build_system_path = build_system.path.relative_to(toolchain.root).as_posix()
        toolchain_root_prefix = f"{toolchain.root.as_posix().rstrip('/')}/"
        canonical_definitions = tuple(
            NativeCMakeDefinition(
                value.name,
                (
                    "$TOOLCHAIN_ROOT/" + value.value.removeprefix(toolchain_root_prefix)
                    if value.value.startswith(toolchain_root_prefix)
                    else value.value
                ),
            )
            for value in recipe.definitions
        )
        components = [
            "native-build-fingerprint:1",
            f"toolchain-sha256\t{toolchain_fingerprint.digest}",
            (
                f"build-system\t{build_system.name}\t{build_system.version}\t"
                f"{build_system_path}\t{build_system_content}"
            ),
            f"source-reference\t{recipe.source_snapshot_reference}",
            f"platform\t{recipe.platform_identity}",
            *(
                f"definition\t{value.name}\t{value.value}"
                for value in canonical_definitions
            ),
            f"target\t{recipe.target}",
            *(f"output\t{path.as_posix()}" for path in recipe.output_paths),
        ]
        canonical_components = tuple(components)
        canonical_bytes = ("\n".join(canonical_components) + "\n").encode("utf-8")
        digest = hashlib.sha256(canonical_bytes).hexdigest()
        return NativeBuildFingerprint(
            fingerprinter_identity=self.identity,
            algorithm="sha256",
            digest=digest,
            short_identity=f"build-{digest[:12]}",
            canonical_components=canonical_components,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class NativeBuildSpecification:
    """Bind one immutable build recipe to explicit filesystem placement and limits.

    Parameters
    ----------
    recipe
        Complete artifact-defining recipe.
    toolchain_identity
        Explicit 12-to-64-character filesystem prefix of the runtime digest.
    build_identity
        Explicit 12-to-64-character filesystem prefix of the build digest.
    source_root
        Absolute read-only proposed source root.
    build_root
        Absolute proposed scratch root.
    install_prefix
        Absolute proposed immutable final installation prefix.
    limits
        Explicit operational ceilings for a separately authorized executor.
    """

    recipe: NativeBuildRecipe
    toolchain_identity: str
    build_identity: str
    source_root: Path
    build_root: Path
    install_prefix: Path
    limits: NativeBuildLimits

    def __post_init__(self) -> None:
        """Validate identities, pairwise-disjoint roots, and operational limits."""
        if type(self.recipe) is not NativeBuildRecipe:
            raise TypeError("recipe must be a NativeBuildRecipe")
        if type(self.toolchain_identity) is not str:
            raise TypeError("toolchain_identity must be a built-in str")
        if _TOOLCHAIN_ID_PATTERN.fullmatch(self.toolchain_identity) is None:
            raise ValueError("toolchain_identity must contain 12 through 64 hex")
        if type(self.build_identity) is not str:
            raise TypeError("build_identity must be a built-in str")
        if _BUILD_ID_PATTERN.fullmatch(self.build_identity) is None:
            raise ValueError("build_identity must contain 12 through 64 hex")
        for path_value, name in (
            (self.source_root, "source_root"),
            (self.build_root, "build_root"),
            (self.install_prefix, "install_prefix"),
        ):
            if not isinstance(path_value, Path):
                raise TypeError(f"{name} must be pathlib.Path")
            if not path_value.is_absolute() or ".." in path_value.parts:
                raise ValueError(f"{name} must be absolute without parent traversal")
            if any(character in path_value.as_posix() for character in "\x00\t\r\n"):
                raise ValueError(
                    f"{name} must not contain NUL, tab, or line terminators"
                )
        for first, second in (
            (self.source_root, self.build_root),
            (self.source_root, self.install_prefix),
            (self.build_root, self.install_prefix),
        ):
            if (
                first == second
                or first.is_relative_to(second)
                or second.is_relative_to(first)
            ):
                raise ValueError(
                    "source_root, build_root, and install_prefix must be disjoint"
                )
        if type(self.limits) is not NativeBuildLimits:
            raise TypeError("limits must be a NativeBuildLimits")


@dataclass(frozen=True, slots=True)
class NativeBuildPlan:
    """Record deterministic argument vectors for an unexecuted native build.

    Parameters
    ----------
    planner_identity
        Exact identity of the planning implementation.
    toolchain
        Complete declared toolchain used to derive the argument vectors.
    toolchain_fingerprint
        Root-independent complete digest and short identifier of ``toolchain``.
    build_fingerprint
        Complete digest of the runtime-toolchain fingerprint and build recipe.
    toolchain_manifest_path
        Proposed immutable manifest path beneath ``toolchain.root/toolchains``. The
        planner neither creates nor serializes it.
    build
        Complete declared build specification.
    configure_argv
        Direct CMake configuration argument vector without shell syntax.
    build_argv
        Direct CMake build argument vector without shell syntax.
    claim_boundary
        Explicit limitations of the execution-free result.
    """

    planner_identity: str
    toolchain: NativeToolchainSpecification
    toolchain_fingerprint: NativeToolchainFingerprint
    build_fingerprint: NativeBuildFingerprint
    toolchain_manifest_path: Path
    build: NativeBuildSpecification
    configure_argv: tuple[str, ...]
    build_argv: tuple[str, ...]
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate the immutable represented plan fields."""
        if type(self.planner_identity) is not str:
            raise TypeError("planner_identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.planner_identity) is None:
            raise ValueError("planner_identity must be a portable identifier")
        if type(self.toolchain) is not NativeToolchainSpecification:
            raise TypeError("toolchain must be a NativeToolchainSpecification")
        if type(self.toolchain_fingerprint) is not NativeToolchainFingerprint:
            raise TypeError(
                "toolchain_fingerprint must be a NativeToolchainFingerprint"
            )
        if type(self.build_fingerprint) is not NativeBuildFingerprint:
            raise TypeError("build_fingerprint must be a NativeBuildFingerprint")
        if type(self.build) is not NativeBuildSpecification:
            raise TypeError("build must be a NativeBuildSpecification")
        toolchain_prefix_length = len(self.build.toolchain_identity.removeprefix("tc-"))
        if (
            self.build.toolchain_identity
            != self.toolchain_fingerprint.filesystem_identity(toolchain_prefix_length)
        ):
            raise ValueError("build toolchain_identity must match its fingerprint")
        build_prefix_length = len(self.build.build_identity.removeprefix("build-"))
        if self.build.build_identity != self.build_fingerprint.filesystem_identity(
            build_prefix_length
        ):
            raise ValueError("build_identity must match its fingerprint")
        if not isinstance(self.toolchain_manifest_path, Path):
            raise TypeError("toolchain_manifest_path must be pathlib.Path")
        expected_manifest_path = (
            self.toolchain.root
            / "toolchains"
            / self.build.toolchain_identity
            / "manifest.json"
        )
        if self.toolchain_manifest_path != expected_manifest_path:
            raise ValueError(
                "toolchain_manifest_path must match the fingerprinted toolchain root"
            )
        for value, name in (
            (self.configure_argv, "configure_argv"),
            (self.build_argv, "build_argv"),
            (self.claim_boundary, "claim_boundary"),
        ):
            if type(value) is not tuple:
                raise TypeError(f"{name} must be a built-in tuple")
            if any(type(member) is not str for member in value):
                raise TypeError(f"{name} members must be built-in strings")
            if not value or any(not member for member in value):
                raise ValueError(f"{name} must contain nonempty strings")


@dataclass(frozen=True, slots=True)
class NativeBuildPlanner:
    """Produce deterministic CMake argument vectors without external effects.

    Parameters
    ----------
    identity
        Portable identity and version of the planning implementation.
    toolchain_fingerprinter
        Explicit canonical runtime-toolchain-fingerprinting dependency.
    build_fingerprinter
        Explicit artifact-building recipe fingerprinting dependency.
    """

    identity: str
    toolchain_fingerprinter: NativeToolchainFingerprinter
    build_fingerprinter: NativeBuildFingerprinter

    def __post_init__(self) -> None:
        """Validate the planning implementation identity."""
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if _ID_PATTERN.fullmatch(self.identity) is None:
            raise ValueError("identity must be a portable planner identifier")
        if type(self.toolchain_fingerprinter) is not NativeToolchainFingerprinter:
            raise TypeError(
                "toolchain_fingerprinter must be a NativeToolchainFingerprinter"
            )
        if type(self.build_fingerprinter) is not NativeBuildFingerprinter:
            raise TypeError("build_fingerprinter must be a NativeBuildFingerprinter")

    def execute(
        self,
        toolchain: NativeToolchainSpecification,
        build: NativeBuildSpecification,
    ) -> NativeBuildPlan:
        """Return the deterministic, execution-free plan.

        Parameters
        ----------
        toolchain
            Complete declared native toolchain.  It must include one build system.
        build
            Exact CMake definitions, roots, target, outputs, and resource ceilings.

        Returns
        -------
        NativeBuildPlan
            Immutable direct argument vectors and explicit claim limitations.

        Raises
        ------
        TypeError
            If either input has the wrong exact public record type.
        ValueError
            If the toolchain has no build-system or runtime-tool declaration.
        """
        if type(toolchain) is not NativeToolchainSpecification:
            raise TypeError("toolchain must be a NativeToolchainSpecification")
        if type(build) is not NativeBuildSpecification:
            raise TypeError("build must be a NativeBuildSpecification")
        build_system = toolchain.tool_for(NativeToolRole.BUILD_SYSTEM)
        fingerprint = self.toolchain_fingerprinter.execute(toolchain)
        build_fingerprint = self.build_fingerprinter.execute(
            toolchain, fingerprint, build.recipe
        )
        toolchain_prefix_length = len(build.toolchain_identity.removeprefix("tc-"))
        if build.toolchain_identity != fingerprint.filesystem_identity(
            toolchain_prefix_length
        ):
            raise ValueError("build toolchain_identity does not match the fingerprint")
        build_prefix_length = len(build.build_identity.removeprefix("build-"))
        if build.build_identity != build_fingerprint.filesystem_identity(
            build_prefix_length
        ):
            raise ValueError("build_identity does not match the build fingerprint")
        configure_argv = (
            build_system.path.as_posix(),
            "-S",
            build.source_root.as_posix(),
            "-B",
            build.build_root.as_posix(),
            f"-DCMAKE_INSTALL_PREFIX={build.install_prefix.as_posix()}",
            *(definition.argument for definition in build.recipe.definitions),
        )
        build_argv = (
            build_system.path.as_posix(),
            "--build",
            build.build_root.as_posix(),
            "--target",
            build.recipe.target,
            "--parallel",
            str(build.limits.maximum_parallel_jobs),
        )
        return NativeBuildPlan(
            planner_identity=self.identity,
            toolchain=toolchain,
            toolchain_fingerprint=fingerprint,
            build_fingerprint=build_fingerprint,
            toolchain_manifest_path=(
                toolchain.root
                / "toolchains"
                / build.toolchain_identity
                / "manifest.json"
            ),
            build=build,
            configure_argv=configure_argv,
            build_argv=build_argv,
            claim_boundary=(
                "declared toolchain and deterministic argument planning only",
                "no filesystem discovery, local-file hashing, or workspace creation",
                (
                    "no installation, network access, compiler invocation, or build "
                    "execution"
                ),
                "no execution authorization or dependency-adoption decision",
                "no numerical verification or scientific validation",
            ),
        )
