# Lake Ontario BASIC Developer Manual

## Project structure

- `interpreter.py` — core language interpreter and built-in functions.
- `ide.py` — compatibility launcher for the command-line IDE.
- `lake_ontario_ide/app.py` — package CLI IDE backend.
- `lake_ontario_ide/gui.py` — thin entry point that re-exports the GUI IDE.
- `lake_ontario_ide/gui_app/` — the Tkinter IDE itself: `app.py` (editor,
  canvas, execution), `dialogs.py`, `menus.py`, `themes.py`, and
  `features/syntax_highlighting.py`.
- `run_ide.py` — GUI launch wrapper that bootstraps `.venv`.
- `pyproject.toml` — package metadata and entry point.
- `tests.py` — regression harness (the single source of truth for checks).
- `test_harness.py` — pytest bridge that collects the same harness functions.
- `examples/` — sample Lake Ontario BASIC scripts.
- `COMMANDS.md` — language command reference.
- `README.md` — project overview and quick start.
- `.github/workflows/ci.yml` — lint, compile, doctor, example validation, tests.

## Interpreter internals

### Script loading

The interpreter parses line-numbered scripts, ignores comment lines starting with `EXCUSE_ME`, and stores statements in `self.lines`.

### Expression evaluation

`evaluate_expression`:

1. masks every string literal with a placeholder (so `"WEALTH_TAX"` keeps its
   words), then restores it with `ast.literal_eval`;
2. rewrites the keywords in `EXPRESSION_KEYWORDS`: `EVIDENCE_BASED`,
   `ALTERNATIVE_FACT`, `CLASSIFIED_MAR_A_LAGO`, the operator aliases
   (`WEALTH_TAX`, `EQUAL_PAY`, `PROPORTIONAL_SHARE`, `FAIR_MULTIPLIER`,
   `POWER_TO_THE_PEOPLE`, `MAPLE_SYRUP`, `MOONSHOT`), and `AND` / `OR` / `NOT`;
3. substitutes variable values, raising `LakeOntarioInterpreterError` for an
   unknown function name and, in strict mode, for an undeclared variable;
4. evaluates against `LO_EVAL_GLOBALS`, a whitelist dict with `__builtins__`
   removed.

`LO_BUILTINS` is built once at import time. Failed expressions raise with the
source expression attached; they never silently return a placeholder.

### Control flow

`build_block_layout` precomputes, in one pass over the script:

- `closing` — opener index to matching closer index (`PERHAPS`/`END_PERHAPS`,
  `WHILE_CLASS_CONSCIOUS`/`CONTINUE_ORGANIZING`, `COAST_TO_COAST`/`THANK_YOU_EH`,
  `FOR_EACH`/`END_EACH`, healthcare openers/`EXECUTIVE_ORDER_BLOCKED`)
- `branches` — the `PERHAPS_ALSO` / `STILL_IN_DENIAL` chain for each `PERHAPS`
- `owner` — the owning `PERHAPS` for each branch marker
- `problems` — unmatched openers and stray closers, reused by `validate_script`

The run loop jumps with that table instead of rescanning for block ends.

### Evidence log

`self.evidence_log` journals every `FACT_CHECK` as
`{line, name, previous, value, amended}`. Amendments (a re-assignment that
changes an existing value) set `amended` so `SHOW_EVIDENCE_LOG` and
`PUBLISH_EVIDENCE_LOG` can flag them. The journal is capped at
`EVIDENCE_LOG_LIMIT` entries (oldest dropped first) so a long loop cannot grow
it without bound, and `RESET_CITIZENS` clears it along with the registry.

### REPL

`run_repl` supports `RUN path.lo` (validate and execute in-session),
`CHECK path.lo` (validate only), and `SAVE path.lo` (write the session's script
statements to a file), alongside `HISTORY`, `REPLAY N`, `!N`, `SHOW_VARS`,
`SHOW_EVIDENCE_LOG`, and `CANCEL`. When stdin is a terminal, `readline`
provides arrow-key history and Tab completion of keywords and built-ins.

Other control flow:

- subroutines: `SUBPOENA` / `RETURN_TO_OTTAWA`
- exception handling: `UNIVERSAL_HEALTHCARE` / `NATIONAL_HEALTHCARE` push onto
  a stack, `EXECUTIVE_ORDER_BLOCKED` pops it, and an uncaught error raises
  `LakeOntarioRuntimeError` for the host (CLI, REPL, or GUI) to report.

### GUI extension points

The interpreter exposes hooks for GUI integration:

- `set_input_callback(callback)` — handles `TOWN_HALL` and `INPUT_BOX` prompts
- `set_graphics_callbacks(callbacks)` — handles canvas commands such as `CLEAR_GRAPHICS`, `DRAW_LINE`, `FILL_RECTANGLE`, etc.

## Extending the language

### Adding a new statement

1. Register the keyword in `SUPPORTED_STATEMENT_PREFIXES` (or
   `SUPPORTED_EXACT_STATEMENTS`) — otherwise `--check` will reject it.
2. Add parsing in `interpreter.py` inside the `run` loop, reading the arguments
   with `_statement_arg(stmt)` instead of a hand-counted slice.
3. Map the statement to expression evaluation or callback invocation.
4. If the statement opens a block, teach `BLOCK_CLOSERS` /
   `_block_opener` about it so the jump table and validator stay in sync.
5. Update `COMMANDS.md` and `docs/language_reference.md`.
6. Add a regression example to `examples/` and update `docs/examples_guide.md`.
7. Add a test case in `tests.py` (wire it into the runner as well).

### Adding a new built-in function

1. Define the function in `interpreter.py`.
2. Add it to the module-level `LO_BUILTINS` table.
3. Document it in `COMMANDS.md` and `docs/language_reference.md`.
4. Add examples and tests (validation and `did you mean` hints pick the name up
   automatically).

## Validation and testing

`validate_script` reports, with line numbers:

- unsupported statements, with a `did you mean` suggestion
- `FACT_CHECK` shape, `PERHAPS` / `PERHAPS_ALSO` `FACT_ESTABLISHED` rules
- `COAST_TO_COAST` header shape and `STEP 0` loops
- unknown function names, with a `did you mean` suggestion
- unbalanced or stray block markers

Run the checks locally:

```bash
python3 -m pip install flake8 pytest
python3 tests.py
python3 -m pytest -q
python3 -m flake8 .
```

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
