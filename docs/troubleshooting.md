# Lake Ontario BASIC Troubleshooting

This guide covers the most common problems when running scripts or using the IDE.

## 1. Script not found

Error:

```text
Script not found: my_script.lo
```

Fix:
- make sure the file exists in the current working directory
- use an absolute or relative path that matches the file location
- confirm the file extension is `.lo`

## 2. Unsupported statement

Error:

```text
Line 10: unsupported statement 'FOO'
```

Fix:
- check the statement spelling against the language reference
- ensure the statement uses the exact Lake Ontario keyword
- confirm the line has a valid statement form

The validator often offers a suggestion:

```text
Line 10: unsupported statement 'SHOW_VAR' — did you mean SHOW_VARS? The committee is happy to assist.
```

## 2a. Unknown function

Error:

```text
Line 20: unknown function 'STR_UPPR' — did you mean STR_UPPER? The committee is happy to assist.
```

Fix:
- function names are `UPPER_SNAKE_CASE`; take the suggestion when one is offered
- check `COMMANDS.md` for the full built-in list

## 2b. Unbalanced blocks

Error:

```text
Line 10: PERHAPS opened here never reaches END_PERHAPS
Line 20: END_PERHAPS without an open block
```

Fix:
- every `PERHAPS` / `PERHAPS_ALSO` chain ends with `END_PERHAPS`
- every `WHILE_CLASS_CONSCIOUS` ends with `CONTINUE_ORGANIZING`
- every `COAST_TO_COAST` ends with `THANK_YOU_EH`
- every `FOR_EACH` ends with `END_EACH`
- remove stray terminators left behind by an edit

## 2b2. `COALITION` branch problems

Error:

```text
Line 30: this PLANK comes after MINORITY_REPORT and can never be reached
Line 10: PLANK has no COALITION block to belong to
```

Fix:
- put `MINORITY_REPORT` last; it is the default, so any `PLANK` after it is dead
- a `PLANK` outside a `COALITION` belongs to no motion — check the block nesting
- comparison planks are checked in order, so list the strictest band first
- `COALITION` needs a value to examine, and `PLANK` needs something to compare

## 2c. Undeclared names in `HONEY_BADGER_MODE`

Error:

```text
Line 20: undeclared citizen 'votes_counted'. HONEY_BADGER_MODE requires a FACT_CHECK before anyone can cite it.
```

Fix:
- declare the value first with `FACT_CHECK name = expression`
- or leave `HONEY_BADGER_MODE` out: in the default mode an undeclared name
  reads as `0`, which is the classic BASIC courtesy

## 2d. `STEP 0` loops

Error:

```text
Line 50: STEP 0 would march in place forever. The committee recommends a step that actually moves.
```

Fix: use a non-zero `STEP`, or omit it to count by one.

## 2e. Input ran out (`EOFError`)

Error:

```text
🚨 UNHANDLED DISASTER: Line 80: the town hall emptied out before an answer arrived
```

This happens when `TOWN_HALL` / `INPUT_BOX` runs without an interactive stdin
(for example, piping from `/dev/null`). Run the script in a terminal, or supply
`interpreter.set_input_callback(...)` when embedding the interpreter.

## 3. `FACT_CHECK` syntax errors

This statement expects a variable assignment:

```lo
FACT_CHECK name = expression
```

Examples:

```lo
FACT_CHECK total = 7 EQUAL_PAY 3
FACT_CHECK message = "Hello"
```

## 4. Loops not moving correctly

If a loop never exits or appears to skip steps:
- verify the loop condition uses valid comparison logic
- confirm `CONTINUE_ORGANIZING` or `THANK_YOU_EH` appears in the loop body
- check for mismatched `PERHAPS`/`END_PERHAPS` blocks

## 5. GUI or input issues

If the GUI does not appear:
- ensure you are using a desktop environment
- install the Python Tk toolkit if needed
- run the app from the project root

If a prompt does not return input:
- verify the script uses `TOWN_HALL` or `INPUT_BOX`
- ensure the GUI callback is connected in the IDE runtime

## 6. REPL command issues

Use:

```bash
python3 interpreter.py --repl
```

To exit:
- type `IMPEACH`
- or `EXIT`
- or `QUIT`

Useful REPL commands:

- `RUN path.lo` — validate and run a script without leaving the prompt
- `CHECK path.lo` — validate only
- `SAVE path.lo` — write the session as a runnable script
- `SHOW_EVIDENCE_LOG` — review every `FACT_CHECK`, including amendments
- `CANCEL` — discard a half-typed block

If `RUN` complains that the script is missing, check the path relative to the
directory you launched the REPL from. If `SAVE` produces an empty file, there
were no script statements in history yet — REPL-only commands are excluded.

## 7. Interpreter crashes

If the runtime raises a `CLIMATE_EMERGENCY` or another error:
- wrap code in `UNIVERSAL_HEALTHCARE` / `EXECUTIVE_ORDER_BLOCKED`
- check that values are valid before arithmetic
- ensure quotations match around strings

Every uncaught failure is reported as a single line and a non-zero exit code:

```text
🚨 UNHANDLED DISASTER: Line 30: CLIMATE EMERGENCY RAISED: boom
```

The interpreter raises `LakeOntarioRuntimeError` instead of calling
`sys.exit()`, so the CLI reports the line, the GUI prints it in the output pane,
and embedders can catch it.

Use `--trace` to see exactly which statement the committee was reading when the
disaster struck.

## 8. Missing editor in CLI IDE

The CLI IDE tries to launch an editor for creating or editing scripts. If no editor is detected:

```bash
export EDITOR=nano
```

or

```bash
export EDITOR=code
```

Then rerun the IDE.

## 9. Package installation problems

If `python3 -m pip install .` fails:
- confirm Python 3.11+ is installed
- update pip with `python3 -m pip install --upgrade pip`
- try again from the repository root

## 10. Common debugging pattern

When a script fails, try the smallest possible version:

```lo
10 BROADCAST_CBC "Start"
20 FACT_CHECK value = 1 EQUAL_PAY 2
30 BROADCAST_CBC value
```

This helps isolate syntax or logic issues quickly.
