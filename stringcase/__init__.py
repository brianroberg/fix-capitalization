"""
Vendored subset of the python-stringcase package.

The original project is available at:
https://github.com/okunishinishi/python-stringcase

This lightweight copy only implements the helpers required by the project:
sentencecase, titlecase, uppercase, and lowercase.
"""

import re
from typing import Iterable


__all__ = ["sentencecase", "titlecase", "uppercase", "lowercase"]

_WORD_PATTERN = re.compile(r"([A-Za-z0-9][A-Za-z0-9']*)")


def _iter_chars(value: str) -> Iterable[str]:
    for char in value:
        yield char


def sentencecase(value: str) -> str:
    """
    Convert text to sentence case while respecting sentence boundaries.
    """
    if not value:
        return value

    result = []
    capitalize_next = True

    for char in _iter_chars(value):
        if capitalize_next and char.isalpha():
            result.append(char.upper())
            capitalize_next = False
        elif char.isalpha():
            result.append(char.lower())
        else:
            result.append(char)

        if char in ".!?":
            capitalize_next = True
        elif char.strip():
            capitalize_next = capitalize_next and char in ".!?"

    return "".join(result)


def titlecase(value: str) -> str:
    """
    Convert text to title case with a best-effort attempt to preserve punctuation.
    """
    if not value:
        return value

    def _replace(match: re.Match) -> str:
        word = match.group(0)
        return word[0].upper() + word[1:].lower()

    return _WORD_PATTERN.sub(_replace, value.lower())


def uppercase(value: str) -> str:
    return value.upper()


def lowercase(value: str) -> str:
    return value.lower()
