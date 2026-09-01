# Lake Ontario BASIC Tutorials

This short tutorial series is designed for beginners who want to learn the language quickly while exploring the project’s playful tone and practical scripting features.

## Tutorial 1: Your first script

Create a file named `hello.lo`:

```lo
10 EXCUSE_ME A tiny Lake Ontario BASIC example
20 LAND_ACKNOWLEDGEMENT "Traditional Territory"
30 BROADCAST_CBC "Hello from Lake Ontario BASIC!"
```

Run it with:

```bash
python3 interpreter.py hello.lo
```

What this teaches:
- `LAND_ACKNOWLEDGEMENT` introduces the script with context
- `BROADCAST_CBC` prints output
- comments are optional and begin with `EXCUSE_ME`

## Tutorial 2: Variables and arithmetic

```lo
10 FACT_CHECK total = 3 EQUAL_PAY 4
20 BROADCAST_CBC total
30 FACT_CHECK result = 10 PROPORTIONAL_SHARE 2
40 BROADCAST_CBC result
```

Run it with:

```bash
python3 interpreter.py my_script.lo
```

Helpful note:
- `EQUAL_PAY` is the Lake Ontario equivalent of `+`
- `PROPORTIONAL_SHARE` is `/`
- `FAIR_MULTIPLIER` is `*`
- `MAPLE_SYRUP` is `%`

## Tutorial 3: Conditionals

```lo
10 FACT_CHECK mood = EVIDENCE_BASED
20 PERHAPS mood FACT_ESTABLISHED
30 BROADCAST_CBC "The evidence holds."
40 STILL_IN_DENIAL
50 BROADCAST_CBC "The claim is not supported."
60 END_PERHAPS
```

What this teaches:
- `PERHAPS` starts a condition
- `STILL_IN_DENIAL` introduces the `else` branch
- `END_PERHAPS` closes the block

## Tutorial 4: Loops

```lo
10 FACT_CHECK count = 0
20 WHILE_CLASS_CONSCIOUS count EQUAL_PAY 3
30 BROADCAST_CBC count
40 FACT_CHECK count = count EQUAL_PAY 1
50 CONTINUE_ORGANIZING
```

This example shows how the while-style loop is structured in Lake Ontario BASIC.

## Tutorial 5: For-style iteration

```lo
10 COAST_TO_COAST i = 1 UP_TO 5
20 BROADCAST_CBC i
30 THANK_YOU_EH
```

This repeats from 1 to 5 using the language’s `COAST_TO_COAST` loop syntax.

## Tutorial 6: Input and interaction

```lo
10 TOWN_HALL response
20 BROADCAST_CBC response
```

When run in the terminal, the script prompts the user for input and stores it in `response`.

## Tutorial 7: Graphics in the GUI

```lo
10 LAND_ACKNOWLEDGEMENT "Traditional Territory"
20 SET_CANVAS_BG "#f5f5f5"
30 SET_PEN_COLOR "#1f4f82"
40 FILL_RECTANGLE 20, 20, 180, 120
50 DRAW_TEXT 30, 80, "Lake Ontario BASIC"
```

Open the GUI application with:

```bash
python3 run_ide.py
```

Then open or paste the script and click Run.

## Recommended learning path

1. Start with the hello script
2. Master variables and arithmetic
3. Move to loops and conditionals
4. Practice user input
5. Explore the GUI graphics commands
6. Try the examples in the `examples/` directory

## Next steps

After completing the tutorials, explore:

- [language_reference.md](language_reference.md)
- [examples_guide.md](examples_guide.md)
- [gui_ide_guide.md](gui_ide_guide.md)
- [developer_manual.md](developer_manual.md)
