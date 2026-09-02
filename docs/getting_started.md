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
python3 interpreter.py --repl
python3 interpreter.py --check examples/hello.lo
```

`--check` validates syntax and catches unsupported statements and duplicate line numbers.

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
