# Getting Started with Lake Ontario BASIC

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/James-HoneyBadger/Lake_Ontario.git
cd Lake_Ontario
python3 -m pip install .
```

## Run the interpreter

To run a Lake Ontario BASIC script:

```bash
python3 interpreter.py examples/hello.lo
```

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
