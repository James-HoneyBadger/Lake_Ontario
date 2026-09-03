"""
Menu construction for the Lake Ontario BASIC IDE.

Builds the full menu bar: File, Edit, Program, Debug, Preferences, About.
Adapted from Time Warp Classic's ``gui/menus.py``
(https://github.com/James-HoneyBadger/Time_Warp_Classic).
"""

import tkinter as tk
import tkinter.font as tkfont

from .themes import THEMES, FONT_SIZES
from .dialogs import FindDialog, ReplaceDialog, show_about


def build_menu_bar(app):
    """Build the complete menu bar and attach it to *app*.

    Parameters
    ----------
    app : LakeOntarioApp
        The application instance that owns the root window and widgets.
    """
    menubar = tk.Menu(app.root)
    app.root.config(menu=menubar)

    _build_file_menu(menubar, app)
    _build_edit_menu(menubar, app)
    _build_program_menu(menubar, app)
    _build_view_menu(menubar, app)
    _build_debug_menu(menubar, app)
    _build_preferences_menu(menubar, app)
    _build_about_menu(menubar, app)


# ------------------------------------------------------------------
# File menu
# ------------------------------------------------------------------


def _build_file_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=menu)

    menu.add_command(label="New File", command=app.new_file, accelerator="Ctrl+N")
    menu.add_command(label="Open File...", command=app.load_file, accelerator="Ctrl+O")

    recent_files_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Open Recent", menu=recent_files_menu)
    recent_files = getattr(app, "recent_files", [])
    if recent_files:
        for path in recent_files:
            label = path.split("/")[-1] if path else "Recent file"
            recent_files_menu.add_command(
                label=label,
                command=lambda p=path: app.load_recent_file(p),
            )
    else:
        recent_files_menu.add_command(label="No recent files", state=tk.DISABLED)
    recent_files_menu.add_separator()
    recent_files_menu.add_command(
        label="Clear Recent Files", command=app.clear_recent_files
    )

    menu.add_separator()
    menu.add_command(label="Save File...", command=app.save_file, accelerator="Ctrl+S")
    menu.add_command(
        label="Save File As...", command=lambda: app.save_file(save_as=True)
    )
    menu.add_separator()
    menu.add_command(label="Exit", command=app.exit_app, accelerator="Ctrl+Q")


# ------------------------------------------------------------------
# Edit menu
# ------------------------------------------------------------------


def _build_edit_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=menu)

    menu.add_command(label="Undo", command=app.undo, accelerator="Ctrl+Z")
    menu.add_command(label="Redo", command=app.redo, accelerator="Ctrl+Y")
    menu.add_separator()
    menu.add_command(label="Cut", command=app.cut, accelerator="Ctrl+X")
    menu.add_command(label="Copy", command=app.copy, accelerator="Ctrl+C")
    menu.add_command(label="Paste", command=app.paste, accelerator="Ctrl+V")
    menu.add_separator()
    menu.add_command(label="Select All", command=app.select_all, accelerator="Ctrl+A")
    menu.add_separator()
    menu.add_command(
        label="Find...",
        command=lambda: FindDialog(app.root, app.editor_text, app.output_text),
        accelerator="Ctrl+F",
    )
    menu.add_command(
        label="Replace...",
        command=lambda: ReplaceDialog(app.root, app.editor_text, app.output_text),
        accelerator="Ctrl+H",
    )


# ------------------------------------------------------------------
# Program menu (with examples)
# ------------------------------------------------------------------


def _build_program_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Program", menu=menu)

    menu.add_command(label="Run Program", command=app.run_code, accelerator="F5")
    menu.add_command(label="Clear Output", command=app.clear_output)
    menu.add_command(label="Clear Graphics", command=app.clear_canvas)
    menu.add_separator()

    examples_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Load Example", menu=examples_menu)
    for label, filepath in app.list_examples():
        examples_menu.add_command(
            label=label,
            command=lambda fp=filepath: app.load_example(fp),
        )


# ------------------------------------------------------------------
# View menu
# ------------------------------------------------------------------


def _build_view_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=menu)
    output_visibility = "Hide" if getattr(app, "_output_visible", True) else "Show"
    menu.add_command(
        label=f"{output_visibility} Output Panel", command=app.toggle_output_panel
    )
    graphics_visibility = "Hide" if getattr(app, "_graphics_visible", True) else "Show"
    menu.add_command(
        label=f"{graphics_visibility} Graphics Panel", command=app.toggle_graphics_panel
    )


# ------------------------------------------------------------------
# Debug menu
# ------------------------------------------------------------------


def _build_debug_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Debug", menu=menu)

    menu.add_command(label="Validate Script", command=app.validate_script)
    menu.add_separator()
    menu.add_command(label="Show Error History", command=app.show_error_history)
    menu.add_command(label="Clear Error History", command=app.clear_error_history)


# ------------------------------------------------------------------
# Preferences menu
# ------------------------------------------------------------------


def _build_preferences_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Preferences", menu=menu)

    theme_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Color Theme", menu=theme_menu)
    for key, data in THEMES.items():
        theme_menu.add_command(
            label=data["name"], command=lambda k=key: app.apply_theme(k)
        )

    font_family_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Font Family", menu=font_family_menu)

    available = _get_available_fonts()
    for font_name in available[:25]:
        font_family_menu.add_command(
            label=font_name, command=lambda f=font_name: app.apply_font_family(f)
        )
    if len(available) > 25:
        font_family_menu.add_separator()
        more = tk.Menu(font_family_menu, tearoff=0)
        font_family_menu.add_cascade(label="More Fonts...", menu=more)
        for font_name in available[25:]:
            more.add_command(
                label=font_name, command=lambda f=font_name: app.apply_font_family(f)
            )

    font_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Font Size", menu=font_menu)
    for key, data in FONT_SIZES.items():
        font_menu.add_command(
            label=data["name"], command=lambda k=key: app.apply_font_size(k)
        )


def _get_available_fonts():
    """Return available monospace fonts, prioritizing common families."""
    all_fonts = sorted(set(tkfont.families()))
    priority = [
        "Courier",
        "Courier New",
        "Consolas",
        "Monaco",
        "Menlo",
        "DejaVu Sans Mono",
        "Liberation Mono",
        "Ubuntu Mono",
        "Fira Code",
        "Source Code Pro",
        "JetBrains Mono",
        "Cascadia Code",
        "SF Mono",
        "Inconsolata",
        "Roboto Mono",
        "Hack",
        "Anonymous Pro",
        "Droid Sans Mono",
        "PT Mono",
    ]
    priority_available = [f for f in priority if f in all_fonts]
    other_fonts = [f for f in all_fonts if f not in priority]
    return priority_available + other_fonts


# ------------------------------------------------------------------
# About menu
# ------------------------------------------------------------------


def _build_about_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="About", menu=menu)
    menu.add_command(
        label="About Lake Ontario BASIC", command=lambda: show_about(app.root)
    )
