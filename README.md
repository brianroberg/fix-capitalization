# Fix Capitalization CLI

Command-line utility for normalizing text capitalization using the vendored [`python-stringcase`](stringcase/__init__.py) helpers. Supports sentence, title, upper, and lower casing, along with flexible input/output options.

## Features

- CLI powered by `optparse` with human-friendly usage text.
- Cap normalization schemes: sentence (default), title, upper, lower.
- Accept input via positional argument, stdin, or a file with `-f/--file`.
- Write results to stdout or an output file with `-o/--output`.
- Comprehensive unit and functional tests via `pytest`.

## Requirements

- Python 3.12+
- `pip install -r requirements-dev.txt` *(optional; install `pytest` and `ruff` if not already available)*

## Usage

```bash
python capitalizer.py --scheme title --file input.txt --output output.txt
```

Additional examples:

- Read from stdin and print to stdout:

  ```bash
  echo "hELLo world." | python capitalizer.py
  ```

- Pass text as a positional argument and convert to uppercase:

  ```bash
  python capitalizer.py --scheme upper "hello there"
  ```

Run `python capitalizer.py --help` for the complete option list.

## Testing & Linting

```bash
pytest            # run unit + functional tests
ruff check        # run static analysis
```

## License

Distributed under the MIT License. See `LICENSE` for details.
