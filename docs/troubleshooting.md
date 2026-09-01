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

## 7. Interpreter crashes

If the runtime raises a `CLIMATE_EMERGENCY` or another error:
- wrap code in `UNIVERSAL_HEALTHCARE` / `EXECUTIVE_ORDER_BLOCKED`
- check that values are valid before arithmetic
- ensure quotations match around strings

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
