import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capitalizer import (  # noqa: E402
    CapitalizationError,
    apply_scheme,
    read_input_text,
)


@pytest.mark.parametrize(
    "scheme,text,expected",
    [
        ("sentence", "hELLo world. tHIS is PYTHON.", "Hello world. This is python."),
        ("title", "the cat in THE HAT", "The Cat In The Hat"),
        ("upper", "MiXeD Case", "MIXED CASE"),
        ("lower", "MiXeD Case", "mixed case"),
    ],
)
def test_apply_scheme(scheme, text, expected):
    assert apply_scheme(text, scheme) == expected


def test_apply_scheme_rejects_unknown_scheme():
    with pytest.raises(CapitalizationError):
        apply_scheme("test", "unknown")


def test_read_input_text_from_file(tmp_path):
    source = tmp_path / "input.txt"
    source.write_text("sample text", encoding="utf-8")
    assert read_input_text(str(source), None) == "sample text"


def test_read_input_text_prefers_positional_over_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("ignored"))
    assert read_input_text(None, "positional value") == "positional value"


def test_read_input_text_from_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("from stdin"))
    assert read_input_text(None, None) == "from stdin"


def test_read_input_text_rejects_multiple_sources():
    with pytest.raises(CapitalizationError):
        read_input_text("path.txt", "text")
