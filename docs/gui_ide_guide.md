# Lake Ontario BASIC GUI IDE Guide

## Overview

The Lake Ontario BASIC GUI IDE provides an interactive environment for writing, running, and visualizing Lake Ontario BASIC scripts. It includes:

- code editor
- live output console
- graphics canvas
- command reference and help panel
- theme toggle

## Launching the GUI IDE

Run the launcher:

```bash
python3 run_ide.py
```

Or launch from the installed package:

```bash
lake-ontario-ide
```

## Editor Features

- line numbers
- syntax-aware style
- save/open file support
- run script button

## Graphics Commands

Supported GUI graphics commands:

- `INPUT_BOX variable_name`
- `SET_PEN_COLOR "color"`
- `SET_FILL_COLOR "color"`
- `SET_CANVAS_BG "color"`
- `CLEAR_GRAPHICS`
- `DRAW_LINE x1, y1, x2, y2`
- `DRAW_RECTANGLE x, y, width, height`
- `FILL_RECTANGLE x, y, width, height`
- `DRAW_CIRCLE x, y, radius`
- `FILL_CIRCLE x, y, radius`
- `DRAW_TEXT x, y, text`
- `WAIT milliseconds`

## Example

```lo
10 EXCUSE_ME GUI canvas demo
20 LAND_ACKNOWLEDGEMENT "Traditional Territory"
30 SET_CANVAS_BG "#f4f4f4"
40 SET_PEN_COLOR "#1f4f82"
50 SET_FILL_COLOR "#d9ead3"
60 FILL_RECTANGLE 40, 80, 260, 120
70 SET_FILL_COLOR "#f4cccc"
80 FILL_CIRCLE 360, 120, 40
90 DRAW_TEXT 44, 84, "Lake Ontario BASIC GUI Demo"
100 INPUT_BOX user_response
110 BROADCAST_CBC user_response
```

## Input Handling

- `TOWN_HALL` prompts in the CLI IDE
- `INPUT_BOX` prompts in the GUI IDE

## Notes

The GUI IDE maintains a live graphics canvas while your script executes. If you change canvas colors mid-script, the new values apply to subsequent draw operations.
