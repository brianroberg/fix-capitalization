#!/usr/bin/env python3
"""
Command-line utility to normalize text capitalization.

Supported schemes:
  - sentence (default)
  - title
  - upper (all caps)
  - lower (all lowercase)

Input can be provided via stdin, a positional argument, or an input file.
Output defaults to stdout but can be written to a file.
"""

from __future__ import annotations

import os
import sys
from optparse import OptionParser
from typing import Callable, Dict, Optional

import stringcase


SCHEME_HANDLERS: Dict[str, Callable[[str], str]] = {
    "sentence": stringcase.sentencecase,
    "title": stringcase.titlecase,
    "upper": stringcase.uppercase,
    "lower": stringcase.lowercase,
}


class CapitalizationError(RuntimeError):
    """Raised when invalid configuration or usage is detected."""


def build_option_parser() -> OptionParser:
    parser = OptionParser(
        usage="%prog [options] [text]",
        description="Normalize text capitalization using python-stringcase.",
    )
    parser.add_option(
        "-s",
        "--scheme",
        dest="scheme",
        default="sentence",
        help="Capitalization scheme: sentence, title, upper, or lower (default: %default)",
    )
    parser.add_option(
        "-f",
        "--file",
        dest="input_file",
        help="Read input text from the specified file",
    )
    parser.add_option(
        "-o",
        "--output",
        dest="output_file",
        help="Write transformed text to the specified file",
    )
    return parser


def read_input_text(
    input_file: Optional[str], positional_text: Optional[str]
) -> str:
    """
    Determine the input text source and return its content.
    """
    if input_file and positional_text:
        raise CapitalizationError("Provide input using only one of --file or positional text.")

    if input_file:
        if not os.path.exists(input_file):
            raise CapitalizationError(f"Input file not found: {input_file}")
        try:
            with open(input_file, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError as exc:
            raise CapitalizationError(f"Failed to read input file: {exc}") from exc

    if positional_text is not None:
        return positional_text

    # Fallback to stdin; strip no characters to preserve formatting.
    return sys.stdin.read()


def apply_scheme(text: str, scheme: str) -> str:
    """
    Transform the input text using the requested capitalization scheme.
    """
    try:
        handler = SCHEME_HANDLERS[scheme.lower()]
    except KeyError as exc:
        valid = ", ".join(sorted(SCHEME_HANDLERS))
        raise CapitalizationError(f"Unknown capitalization scheme '{scheme}'. Valid values: {valid}") from exc
    return handler(text)


def write_output(text: str, output_file: Optional[str]) -> None:
    """
    Write the transformed text to the chosen destination.
    """
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as handle:
                handle.write(text)
        except OSError as exc:
            raise CapitalizationError(f"Failed to write output file: {exc}") from exc
    else:
        sys.stdout.write(text)


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_option_parser()
    options, args = parser.parse_args(argv)

    positional_text: Optional[str]
    if len(args) > 1:
        parser.error("Only one positional argument is allowed.")
    positional_text = args[0] if args else None

    try:
        input_text = read_input_text(options.input_file, positional_text)
        transformed = apply_scheme(input_text, options.scheme)
        write_output(transformed, options.output_file)
    except CapitalizationError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
