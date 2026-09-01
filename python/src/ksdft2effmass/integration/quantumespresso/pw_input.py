"""Loose Quantum ESPRESSO ``pw.x`` input-file representation and writing.

The module maps upstream-owned grouping decisions to Quantum ESPRESSO namelist
and card syntax. It does not own scientific defaults, interpret input variables,
validate cross-field physics, invoke ``pw.x``, or parse calculator outputs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QePwInputFile:
    """Represent ordered grouping tags and body lines for a ``pw.x`` input file.

    Parameters
    ----------
    groups
        Ordered built-in tuple of ``(tag, lines)`` pairs. ``tag`` is a nonempty
        built-in string without surrounding whitespace or line terminators.
        A tag beginning with ``&`` denotes a Fortran namelist; every other tag
        denotes a Quantum ESPRESSO card and may include its card option. ``lines``
        is a built-in tuple of built-in strings without line terminators. Upstream
        objects determine the tags, group order, assignments, values, and rows.

    Raises
    ------
    TypeError
        If the outer structure, a group pair, a tag, a line collection, or a line
        has the wrong semantic built-in type.
    ValueError
        If a tag is empty, has surrounding whitespace, contains a line terminator,
        or a body line contains a line terminator.

    Notes
    -----
    This is a loose integration record. It intentionally preserves unknown groups
    and variables and does not apply Quantum ESPRESSO defaults or scientific policy.
    """

    groups: tuple[tuple[str, tuple[str, ...]], ...]

    def __post_init__(self) -> None:
        if type(self.groups) is not tuple:
            raise TypeError("groups must be a built-in tuple")
        for group in self.groups:
            if type(group) is not tuple or len(group) != 2:
                raise TypeError("each group must be a built-in (tag, lines) tuple")
            tag, lines = group
            if type(tag) is not str:
                raise TypeError("group tag must be a built-in str")
            if not tag:
                raise ValueError("group tag must be nonempty")
            if tag != tag.strip():
                raise ValueError("group tag must not have surrounding whitespace")
            if "\n" in tag or "\r" in tag:
                raise ValueError("group tag must not contain a line terminator")
            if type(lines) is not tuple:
                raise TypeError("group lines must be a built-in tuple")
            for line in lines:
                if type(line) is not str:
                    raise TypeError("group line must be a built-in str")
                if "\n" in line or "\r" in line:
                    raise ValueError("group line must not contain a line terminator")


class QePwInputFileWriter:
    """Write a :class:`QePwInputFile` as deterministic ``pw.x`` input text.

    The writer emits namelist body lines with four-space indentation and a closing
    ``/``. Card body lines use one-space indentation and have no closing delimiter.
    Group tags, assignments, lexical values, card options, rows, and ordering are
    supplied by the input object and are not interpreted.
    """

    def execute(self, input_file: QePwInputFile) -> str:
        """Return deterministic Quantum ESPRESSO ``pw.x`` input text.

        Parameters
        ----------
        input_file
            Ordered grouping tags and body lines supplied by upstream owners.

        Returns
        -------
        str
            Plain text ending with one newline when at least one group is present;
            otherwise the empty string.

        Raises
        ------
        TypeError
            If ``input_file`` is not exactly a :class:`QePwInputFile`.
        """
        if type(input_file) is not QePwInputFile:
            raise TypeError("input_file must be a QePwInputFile")
        output: list[str] = []
        for tag, lines in input_file.groups:
            output.append(tag)
            indentation = "    " if tag.startswith("&") else " "
            output.extend(f"{indentation}{line}" for line in lines)
            if tag.startswith("&"):
                output.append("/")
        return "\n".join(output) + ("\n" if output else "")
