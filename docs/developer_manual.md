# Lake Ontario BASIC Developer Manual

## Project structure

- `interpreter.py` — core language interpreter and built-in functions.
- `ide.py` — command-line IDE for editing, running, and validating scripts.
- `lake_ontario_ide/app.py` — package CLI IDE backend.
- `lake_ontario_ide/gui.py` — Tkinter-based GUI IDE.
- `run_ide.py` — GUI launch wrapper.
- `pyproject.toml` — package metadata and entry point.
- `tests.py` — regression harness for key example scripts.
- `examples/` — sample Lake Ontario BASIC scripts.
- `COMMANDS.md` — language command reference.
- `README.md` — project overview and quick start.

## Interpreter internals

### Script loading

The interpreter parses line-numbered scripts, ignores comment lines starting with `EXCUSE_ME`, and stores statements in `self.lines`.

### Expression evaluation

`evaluate_expression` supports:

- custom keywords: `EVIDENCE_BASED`, `ALTERNATIVE_FACT`, `CLASSIFIED_MAR_A_LAGO`
- operator aliases: `WEALTH_TAX`, `EQUAL_PAY`, `PROPORTIONAL_SHARE`, `FAIR_MULTIPLIER`, `POWER_TO_THE_PEOPLE`, `MAPLE_SYRUP`, `MOONSHOT`
- built-in functions exposed via a whitelist
- string literal preservation via `LOString`

### Control flow

The interpreter supports:

- conditionals: `PERHAPS`, `STILL_IN_DENIAL`, `END_PERHAPS`
- loops: `COAST_TO_COAST` / `THANK_YOU_EH`, `WHILE_CLASS_CONSCIOUS` / `CONTINUE_ORGANIZING`
- subroutines: `SUBPOENA` / `RETURN_TO_OTTAWA`
- exception handling: `UNIVERSAL_HEALTHCARE`, `EXECUTIVE_ORDER_BLOCKED`

### GUI extension points

The interpreter exposes hooks for GUI integration:

- `set_input_callback(callback)` — handles `TOWN_HALL` and `INPUT_BOX` prompts
- `set_graphics_callbacks(callbacks)` — handles canvas commands such as `CLEAR_GRAPHICS`, `DRAW_LINE`, `FILL_RECTANGLE`, etc.

## Extending the language

### Adding a new statement

1. Add parsing in `interpreter.py` inside the `run` loop.
2. Map the statement to expression evaluation or callback invocation.
3. Update `COMMANDS.md` and `docs/language_reference.md`.
4. Add a regression example to `examples/` and update `docs/examples_guide.md`.
5. Add a test case in `tests.py` if applicable.

### Adding a new built-in function

1. Define the function in `interpreter.py`.
2. Add it to the `builtins` dictionary in `evaluate_expression`.
3. Document it in `COMMANDS.md` and `docs/language_reference.md`.
4. Add examples and tests.

## Packaging

The package entry point is defined in `pyproject.toml`:

```toml
[project.scripts]
lake-ontario-ide = "lake_ontario_ide.gui:main"
```

Install with:

```bash
python3 -m pip install .
```

Run the GUI IDE with:

```bash
lake-ontario-ide
```
