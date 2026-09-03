# Lake Ontario BASIC GUI IDE Guide

## Overview

The Lake Ontario BASIC GUI IDE is built on the [Time Warp Classic](https://github.com/James-HoneyBadger/Time_Warp_Classic)
IDE shell, rewired to run the Lake Ontario BASIC interpreter exclusively. It includes:

- syntax-highlighted code editor with line numbers (via Pygments, with a plain-text fallback)
- live output console
- graphics canvas
- File / Edit / Program / Debug / Preferences / About menu bar
- find & replace (regex-capable)
- built-in example script loader (`examples/*.lo`)
- script validation (Debug → Validate Script) and runtime error history
- 9 color themes and 7 font sizes, persisted to `~/.lake_ontario_settings.json`

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
- save/open file support (`.lo` scripts)
- Run Program button / menu item / F5 shortcut
- undo/redo, cut/copy/paste, select all
- find & replace with case-sensitive, whole-word, and regex options

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

## Acknowledgment

The IDE shell (editor widget, themes, menus, dialogs) is adapted from
[Time Warp Classic](https://github.com/James-HoneyBadger/Time_Warp_Classic)
by Honey Badger Universe, reworked here to run Lake Ontario BASIC only.

