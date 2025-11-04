import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "capitalizer.py"


def run_cli(args, input_text=None):
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=input_text.encode("utf-8") if input_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return completed


def test_cli_sentence_default_with_positional():
    result = run_cli(["hELLo world! this IS great."])
    assert result.returncode == 0
    assert result.stdout.decode("utf-8") == "Hello world! This is great."


def test_cli_title_scheme_with_file(tmp_path):
    input_path = tmp_path / "source.txt"
    input_path.write_text("a taLE oF TWO cities", encoding="utf-8")
    output_path = tmp_path / "output.txt"

    result = run_cli(
        ["--scheme", "title", "--file", str(input_path), "--output", str(output_path)]
    )

    assert result.returncode == 0
    assert result.stdout.decode("utf-8") == ""
    assert output_path.read_text(encoding="utf-8") == "A Tale Of Two Cities"


def test_cli_upper_scheme_from_stdin():
    result = run_cli(["--scheme", "upper"], input_text="make me loud")
    assert result.returncode == 0
    assert result.stdout.decode("utf-8") == "MAKE ME LOUD"


def test_cli_rejects_conflicting_input_sources(tmp_path):
    input_path = tmp_path / "source.txt"
    input_path.write_text("ignored", encoding="utf-8")

    result = run_cli([str(input_path), "--file", str(input_path)])
    assert result.returncode != 0
    assert b"Provide input using only one of --file or positional text." in result.stderr
