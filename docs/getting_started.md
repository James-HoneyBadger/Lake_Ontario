# Getting Started with Lake Ontario BASIC

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/James-HoneyBadger/Lake_Ontario.git
cd Lake_Ontario
python3 -m pip install .
```

After installation, these console commands are available:

```bash
lake-ontario-basic --help
lake-ontario-ide
lake-ontario-cli
```

## Run the interpreter

To run a Lake Ontario BASIC script:

```bash
python3 interpreter.py examples/hello.lo
```

## Project environment bootstrap

The project includes a self-bootstrapping launcher that creates a `.venv` if needed and verifies the Python environment before starting the GUI or interpreter.

```bash
python3 run_ide.py
python3 interpreter.py --doctor
```

## Common CLI commands

```bash
python3 interpreter.py --help
python3 interpreter.py --version
python3 interpreter.py --list-examples
python3 interpreter.py --run-example hello
python3 interpreter.py --doctor
python3 interpreter.py --doctor --strict
python3 interpreter.py --repl
python3 interpreter.py --check examples/hello.lo
python3 interpreter.py --trace examples/hello.lo
python3 interpreter.py --strict examples/hello.lo
```

`--check` audits a script without running it: unsupported statements and
duplicate line numbers, `FACT_CHECK` and `PERHAPS` shape, unbalanced blocks,
unknown function names (with `did you mean` hints), and `STEP 0` loops.

`--trace` prints an `AUDIT TRAIL` line before every executed statement, which
is handy when a loop is behaving like a filibuster.

`--strict` starts in `HONEY_BADGER_MODE`: citing a name that was never
`FACT_CHECK`-ed becomes an error instead of quietly reading as `0`.

`--doctor` reports Python, virtual environment, Tkinter, and example counts.
Missing Tkinter is a warning (the CLI and examples still run); add `--strict`
when you want the doctor to fail on it, for example in CI.

## Run the CLI IDE

```bash
python3 ide.py
```

## Run the GUI IDE

```bash
python3 run_ide.py
```

Or from the installed package:

```bash
lake-ontario-ide
```

## First script

Create a file `hello.lo` with:

```lo
10 EXCUSE_ME A simple Lake Ontario BASIC script
20 LAND_ACKNOWLEDGEMENT "Traditional Territory"
30 BROADCAST_CBC "Hello from Lake Ontario BASIC!"
```

Then run:

```bash
python3 interpreter.py hello.lo
```

## Notes

- Lake Ontario BASIC is intentionally satirical and uses progressive-themed keywords.
- The interpreter supports both command-line and GUI execution.
