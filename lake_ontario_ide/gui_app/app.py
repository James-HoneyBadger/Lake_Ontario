#!/usr/bin/env python3
"""
Lake Ontario BASIC — Time Warp Classic Edition GUI IDE
=======================================================

The ``LakeOntarioApp`` class owns the root Tk window, assembles the
editor / output / graphics layout, and delegates actions to the
``LakeOntarioInterpreter`` and helper modules.

This IDE shell (layout, themes, syntax-highlighting editor, find/replace,
menu structure) is adapted from Time Warp Classic
(https://github.com/James-HoneyBadger/Time_Warp_Classic), rewired here to
run the Lake Ontario BASIC language exclusively.
"""

import contextlib
import io
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog

from interpreter import (
    LakeOntarioInterpreter,
    LakeOntarioInterpreterError,
    validate_script as validate_script_text,
)

from .features.syntax_highlighting import SyntaxHighlightingText, LineNumberedText
from .themes import THEMES, FONT_SIZES, LINE_NUMBER_BG
from .menus import build_menu_bar

try:
    import pygments  # noqa: F401

    _PYGMENTS = True
except ImportError:
    _PYGMENTS = False

SETTINGS_FILE = Path.home() / ".lake_ontario_settings.json"
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"

DEFAULT_SCRIPT_TEMPLATE = """10 EXCUSE_ME Lake Ontario BASIC demo script
20 LAND_ACKNOWLEDGEMENT "Traditional Territory"
30 BROADCAST_CBC "Welcome to Lake Ontario BASIC!"
40 SET_CANVAS_BG "#f4f4f4"
50 SET_PEN_COLOR "#1f4f82"
60 SET_FILL_COLOR "#d9ead3"
70 FILL_RECTANGLE 20, 80, 220, 120
80 SET_FILL_COLOR "#f4cccc"
90 FILL_CIRCLE 320, 120, 40
100 DRAW_TEXT 22, 82, "Lake Ontario BASIC GUI Demo"
110 DRAW_TEXT 22, 102, "Use INPUT_BOX to ask the user a question."
120 INPUT_BOX user_response
130 BROADCAST_CBC user_response
"""


class LakeOntarioApp:
    """Main GUI application for the Lake Ontario BASIC IDE."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self):
        self.current_theme = "dark"
        self.current_font = "medium"
        self.current_font_family = "Courier"
        self._load_settings()

        self.root = tk.Tk()
        self.root.title("Lake Ontario BASIC — Professional Edition")
        self.root.geometry("1280x840")
        self.root.minsize(1000, 700)
        self.root.config(bg="#0f172a")

        self.current_path = None
        self.recent_files = []
        self.editor_text = None
        self.editor_tabs = {}
        self.current_tab_key = None
        self.tab_counter = 0
        self.output_text = None
        self.canvas = None
        self.interpreter = None
        self.pen_color = "#0b5394"
        self.fill_color = "#d9ead3"
        self.canvas_bg = "white"
        self.pen_width = 2
        self.error_history = []

        self._layout_widgets = {}
        self._output_visible = True
        self._graphics_visible = True

        self._build_layout()
        self._configure_interpreter()

        build_menu_bar(self)
        self._bind_keys()

        self.apply_theme(self.current_theme)
        self.apply_font_size(self.current_font)

        self._load_default_script()
        self._show_welcome()
        self._update_cursor_status()

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------

    def _load_settings(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    s = json.load(f)
                self.current_theme = s.get("theme", "dark")
                self.current_font = s.get("font_size", "medium")
                self.current_font_family = s.get("font_family", "Courier")
                self.recent_files = s.get("recent_files", [])
                return
        except Exception:
            pass
        self.current_theme = "dark"
        self.current_font = "medium"
        self.current_font_family = "Courier"
        self.recent_files = []

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "theme": self.current_theme,
                        "font_size": self.current_font,
                        "font_family": self.current_font_family,
                        "recent_files": self.recent_files[:8],
                    },
                    f,
                )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_layout(self):
        main_paned = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL, sashwidth=5, bg="#252526"
        )
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Left panel (editor) ---
        left_panel = tk.Frame(main_paned, bg="#252526")
        main_paned.add(left_panel, width=500)

        editor_container = tk.Frame(left_panel, bg="#252526")
        editor_container.pack(fill=tk.BOTH, expand=True)

        editor_header = tk.Frame(editor_container, bg="#252526")
        editor_header.pack(fill=tk.X, pady=(0, 5))
        tk.Label(
            editor_header,
            text="Lake Ontario BASIC",
            font=("Arial", 9, "bold"),
            bg="#252526",
            fg="#d4d4d4",
        ).pack(side=tk.LEFT, padx=(5, 5))

        editor_frame = tk.LabelFrame(
            editor_container,
            text="Code Editor",
            padx=5,
            pady=5,
            bg="#252526",
            fg="#d4d4d4",
        )
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(editor_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_selected)

        self.example_lookup = {}
        self._create_editor_tab("Main", DEFAULT_SCRIPT_TEMPLATE)

        # --- Right panel ---
        right_panel = tk.Frame(main_paned, bg="#252526")
        main_paned.add(right_panel, width=700)

        right_paned = tk.PanedWindow(
            right_panel, orient=tk.VERTICAL, sashwidth=5, bg="#252526"
        )
        right_paned.pack(fill=tk.BOTH, expand=True)

        output_frame = tk.LabelFrame(
            right_paned,
            text="Output",
            padx=5,
            pady=5,
            bg="#252526",
            fg="#d4d4d4",
        )
        right_paned.add(output_frame, height=300)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        graphics_frame = tk.LabelFrame(
            right_paned,
            text="Graphics Canvas",
            padx=5,
            pady=5,
            bg="#252526",
            fg="#d4d4d4",
        )
        right_paned.add(graphics_frame, height=300)

        self.canvas = tk.Canvas(
            graphics_frame,
            width=600,
            height=400,
            bg="#2d2d2d",
            highlightthickness=1,
            highlightbackground="#3e3e3e",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar with file and execution state
        input_frame = tk.Frame(self.root, bg="#252526")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(
            input_frame,
            text="Status:",
            font=("Arial", 10, "bold"),
            bg="#252526",
            fg="#d4d4d4",
        ).pack(side=tk.LEFT, padx=(0, 5))
        self.status_label = tk.Label(
            input_frame,
            text="Ready.",
            font=("Arial", 10),
            bg="#252526",
            fg="#d4d4d4",
            anchor="w",
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.cursor_label = tk.Label(
            input_frame,
            text="Ln 1, Col 1 | 1 lines",
            font=("Arial", 9),
            bg="#252526",
            fg="#a7f3d0",
            anchor="e",
        )
        self.cursor_label.pack(side=tk.RIGHT, padx=(10, 0))

        self.file_label = tk.Label(
            input_frame,
            text="No file loaded",
            font=("Arial", 9),
            bg="#252526",
            fg="#93c5fd",
            anchor="e",
        )
        self.file_label.pack(side=tk.RIGHT, padx=(10, 0))

        # Button bar
        button_frame = tk.Frame(self.root, bg="#252526")
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            button_frame,
            text="\u25b6 Run",
            command=self.run_code,
            bg="#22c55e",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            activebackground="#16a34a",
        ).pack(side=tk.LEFT, padx=5)
        for label, cmd in [
            ("\U0001f4c2 Open", self.load_file),
            ("\U0001f4be Save", self.save_file),
            ("\U0001f5d1\ufe0f Clear Editor", self.clear_editor),
            ("\U0001f4c4 Clear Output", self.clear_output),
            ("\U0001f3a8 Clear Graphics", self.clear_canvas),
        ]:
            tk.Button(
                button_frame,
                text=label,
                command=cmd,
                padx=15,
                bg="#3e3e3e",
                fg="#d4d4d4",
            ).pack(side=tk.LEFT, padx=5)

        self._layout_widgets = {
            "left_panel": left_panel,
            "editor_container": editor_container,
            "right_panel": right_panel,
            "right_paned": right_paned,
            "editor_frame": editor_frame,
            "output_frame": output_frame,
            "graphics_frame": graphics_frame,
            "input_frame": input_frame,
            "button_frame": button_frame,
            "editor_header": editor_header,
        }

    # ------------------------------------------------------------------
    # Interpreter wiring
    # ------------------------------------------------------------------

    def _configure_interpreter(self):
        self.interpreter = LakeOntarioInterpreter()
        self.interpreter.set_input_callback(self._prompt_input)
        self.interpreter.set_graphics_callbacks(
            {
                "clear": self._graphics_clear,
                "line": self._draw_line,
                "rectangle": self._draw_rectangle,
                "filled_rectangle": self._fill_rectangle,
                "circle": self._draw_circle,
                "filled_circle": self._fill_circle,
                "oval": self._draw_oval,
                "filled_oval": self._fill_oval,
                "arc": self._draw_arc,
                "point": self._draw_point,
                "polygon": self._draw_polygon,
                "filled_polygon": self._fill_polygon,
                "triangle": self._draw_triangle,
                "filled_triangle": self._fill_triangle,
                "text": self._draw_text,
                "pen_color": self._set_pen_color,
                "fill_color": self._set_fill_color,
                "canvas_bg": self._set_canvas_background,
                "pen_width": self._set_pen_width,
            }
        )
        self.interpreter.set_sound_callbacks(
            {
                "tone": self._play_tone,
                "stop": self._stop_sound,
                "file": self._play_sound_file,
            }
        )

    def list_examples(self):
        """Return ``(label, filepath)`` pairs for all ``.lo`` example scripts."""
        if not EXAMPLES_DIR.is_dir():
            return []
        examples = []
        for path in sorted(EXAMPLES_DIR.glob("*.lo")):
            label = path.stem.replace("_", " ").title()
            examples.append((label, str(path)))
        return examples

    def _create_editor_tab(self, title, initial_text=""):
        """Create a new tab holding an editable Lake Ontario BASIC source buffer."""
        self.tab_counter += 1
        page = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(page, text=title)

        if _PYGMENTS:
            editor = SyntaxHighlightingText(
                page,
                language="text",
                theme="dark",
                bg="#1e1e1e",
                fg="#d4d4d4",
                insertbackground="#d4d4d4",
            )
        else:
            editor = LineNumberedText(
                page,
                bg="#1e1e1e",
                fg="#d4d4d4",
                insertbackground="#d4d4d4",
            )
        editor.pack(fill=tk.BOTH, expand=True)

        key = f"tab_{self.tab_counter}"
        self.editor_tabs[key] = editor
        self.current_tab_key = key
        self.editor_text = editor
        if initial_text:
            try:
                editor.delete("1.0", tk.END)
                editor.insert("1.0", initial_text)
            except Exception:
                pass

        self._bind_editor_events(editor)
        self.notebook.select(page)
        self._update_cursor_status()
        return key

    def _bind_editor_events(self, editor):
        """Bind editor interaction events to the active cursor status refresh."""
        target = editor.text if hasattr(editor, "text") else editor
        target.bind("<KeyRelease>", lambda event: self._update_cursor_status())
        target.bind("<ButtonRelease>", lambda event: self._update_cursor_status())
        target.bind("<Motion>", lambda event: self._update_cursor_status())

    def _on_tab_selected(self, event=None):
        """Switch the active editor when the selected tab changes."""
        selected = self.notebook.select()
        for key, editor in self.editor_tabs.items():
            if self.notebook.nametowidget(selected) is getattr(editor, "master", None):
                self.current_tab_key = key
                self.editor_text = editor
                self._update_cursor_status()
                return

    def _load_default_script(self):
        current = (
            self.editor_text.get("1.0", tk.END).strip() if self.editor_text else ""
        )
        if not current:
            self.editor_text.insert("1.0", DEFAULT_SCRIPT_TEMPLATE)

    # ------------------------------------------------------------------
    # Keyboard bindings
    # ------------------------------------------------------------------

    def _bind_keys(self):
        self.root.bind("<F5>", lambda e: self.run_code())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.load_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-q>", lambda e: self.exit_app())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        self.root.bind("<Control-t>", lambda e: self.new_tab())
        from .dialogs import FindDialog, ReplaceDialog

        self.root.bind(
            "<Control-f>",
            lambda e: FindDialog(self.root, self.editor_text, self.output_text),
        )
        self.root.bind(
            "<Control-h>",
            lambda e: ReplaceDialog(self.root, self.editor_text, self.output_text),
        )

    # ------------------------------------------------------------------
    # Welcome message
    # ------------------------------------------------------------------

    def _show_welcome(self):
        self.output_text.insert(
            "1.0",
            (
                "Welcome to Lake Ontario BASIC Professional! \U0001f981\U0001f341\n\n"
                "A polished, evidence-based programming environment\n"
                "for curious builders, civic coders, and playful experimenters.\n\n"
                "Enter your code in the left panel and click Run (F5) to execute.\n"
                "Use the menu to validate, explore examples, and tune the editor theme.\n"
            ),
        )

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def _update_cursor_status(self):
        """Refresh the editor cursor and line count status."""
        if not self.editor_text:
            return
        if not hasattr(self, "cursor_label"):
            return
        try:
            insert_index = self.editor_text.index("insert")
            line, column = map(int, insert_index.split("."))
            text = self.editor_text.get("1.0", tk.END)
            total_lines = max(1, text.count("\n") + 1)
            self.cursor_label.config(
                text=f"Ln {line}, Col {column} | {total_lines} lines"
            )
        except Exception:
            self.cursor_label.config(text="Ln 1, Col 1 | 1 lines")

    def toggle_output_panel(self):
        """Hide or show the output panel."""
        if "right_paned" not in self._layout_widgets:
            return
        pane = self._layout_widgets["right_paned"]
        output = self._layout_widgets["output_frame"]
        if self._output_visible:
            pane.forget(output)
            self._output_visible = False
            self.set_status("Output panel hidden.")
        else:
            pane.add(output)
            self._output_visible = True
            self.set_status("Output panel shown.")

    def toggle_graphics_panel(self):
        """Hide or show the graphics panel."""
        if "right_paned" not in self._layout_widgets:
            return
        pane = self._layout_widgets["right_paned"]
        canvas = self._layout_widgets["graphics_frame"]
        if self._graphics_visible:
            pane.forget(canvas)
            self._graphics_visible = False
            self.set_status("Graphics panel hidden.")
        else:
            pane.add(canvas)
            self._graphics_visible = True
            self.set_status("Graphics panel shown.")

    def set_status(self, message, is_error=False):
        """Set the app status message and accent color."""
        self.status_label.config(text=message)
        self.status_label.config(fg="#fca5a5" if is_error else "#d4d4d4")

    def new_tab(self, title=None, initial_text=""):
        """Create a new editor tab."""
        tab_title = title or f"Tab {len(self.editor_tabs) + 1}"
        self._create_editor_tab(tab_title, initial_text)
        self.output_text.insert(tk.END, f"\U0001f4c8 Opened tab: {tab_title}\n")
        self.set_status(f"Tab opened: {tab_title}")

    def new_file(self):
        """Create a new empty file in the editor."""
        if messagebox.askyesno("New File", "Clear current editor content?"):
            self.current_path = None
            self.file_label.config(text="New file")
            self.editor_text.delete("1.0", tk.END)
            self._configure_interpreter()
            self.output_text.insert(tk.END, "\U0001f4c4 New file created\n")
            self._update_cursor_status()
            self.set_status("Ready.")

    def _refresh_menus(self):
        """Rebuild the Tk menu bar so recent-file changes appear immediately."""
        try:
            from .menus import build_menu_bar

            build_menu_bar(self)
        except Exception:
            pass

    def clear_recent_files(self):
        """Clear the persistent recent-file list."""
        self.recent_files = []
        self._save_settings()
        self._refresh_menus()
        self.set_status("Recent files cleared.")

    def _remember_recent_file(self, filename):
        """Keep a small list of recently opened or saved files."""
        if not filename:
            return
        normalized = str(Path(filename).expanduser())
        self.recent_files = [p for p in self.recent_files if p != normalized]
        self.recent_files.insert(0, normalized)
        self.recent_files = self.recent_files[:8]
        self._save_settings()
        self._refresh_menus()

    def load_recent_file(self, filename):
        """Open a file from the recent-files list."""
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.current_path = filename
            self._remember_recent_file(filename)
            self.file_label.config(text=Path(filename).name)
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", content)
            self._configure_interpreter()
            self.output_text.insert(tk.END, f"\U0001f4c2 Loaded: {filename}\n")
            self.set_status(f"Loaded {Path(filename).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recent file:\n{e}")
            self.set_status("Load failed.", is_error=True)

    def load_file(self):
        """Open a file dialog and load the selected file into the editor."""
        filename = filedialog.askopenfilename(
            title="Open Lake Ontario BASIC script",
            filetypes=[
                ("Lake Ontario BASIC", "*.lo"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.current_path = filename
            self._remember_recent_file(filename)
            self.file_label.config(text=Path(filename).name)
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", content)
            self._configure_interpreter()
            self.output_text.insert(tk.END, f"\U0001f4c2 Loaded: {filename}\n")
            self.set_status(f"Loaded {Path(filename).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")
            self.set_status("Load failed.", is_error=True)

    def save_file(self, save_as=False):
        """Save the current editor content to a file."""
        filename = self.current_path if (self.current_path and not save_as) else None
        if not filename:
            filename = filedialog.asksaveasfilename(
                title="Save Lake Ontario BASIC script",
                defaultextension=".lo",
                filetypes=[
                    ("Lake Ontario BASIC", "*.lo"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*"),
                ],
            )
        if not filename:
            return
        try:
            content = self.editor_text.get("1.0", tk.END)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            self.current_path = filename
            self._remember_recent_file(filename)
            self.file_label.config(text=Path(filename).name)
            self.output_text.insert(tk.END, f"\U0001f4be Saved: {filename}\n")
            self.set_status(f"Saved {Path(filename).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
            self.set_status("Save failed.", is_error=True)

    def load_example(self, filepath):
        """Load an example program from *filepath* into the editor."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.current_path = None
            self.file_label.config(text=Path(filepath).name)
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", content)
            self._configure_interpreter()
            self.output_text.insert(tk.END, f"\U0001f4da Loaded example: {filepath}\n")
            self.set_status(f"Loaded example {Path(filepath).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load example:\n{e}")
            self.set_status("Example load failed.", is_error=True)

    # ------------------------------------------------------------------
    # Edit operations
    # ------------------------------------------------------------------

    def cut(self):
        try:
            self.editor_text.event_generate("<<Cut>>")
        except Exception:
            pass

    def copy(self):
        try:
            self.editor_text.event_generate("<<Copy>>")
        except Exception:
            pass

    def paste(self):
        try:
            self.editor_text.event_generate("<<Paste>>")
        except Exception:
            pass

    def undo(self):
        try:
            self.editor_text.edit_undo()
        except Exception:
            pass

    def redo(self):
        try:
            self.editor_text.edit_redo()
        except Exception:
            pass

    def select_all(self):
        self.editor_text.tag_add("sel", "1.0", tk.END)
        self.editor_text.mark_set("insert", "1.0")
        self.editor_text.see("insert")
        return "break"

    def clear_editor(self):
        self.editor_text.delete("1.0", tk.END)
        self.file_label.config(text="New file")
        self.set_status("Editor cleared.")

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.set_status("Output cleared.")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.configure(bg=self.canvas_bg)
        self.output_text.insert(tk.END, "\U0001f3a8 Canvas cleared\n")
        self.set_status("Canvas cleared.")

    # ------------------------------------------------------------------
    # Code execution
    # ------------------------------------------------------------------

    def run_code(self):
        """Execute the current editor content with the Lake Ontario interpreter."""
        code = self.editor_text.get("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.clear_canvas()
        self._configure_interpreter()
        self.output_text.insert(tk.END, "\U0001f680 Running program...\n\n")
        self.set_status("Executing script...")

        self.interpreter.load_script(code)

        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                self.interpreter.run()
        except (
            LakeOntarioInterpreterError,
            OSError,
            ValueError,
            TypeError,
            ZeroDivisionError,
            SyntaxError,
            NameError,
        ) as exc:
            self.output_text.insert(tk.END, buffer.getvalue())
            message = f"🚨 Runtime error: {exc}"
            self.output_text.insert(tk.END, f"\n{message}\n")
            self.error_history.append(message)
            self.set_status("Execution failed.", is_error=True)
        else:
            self.output_text.insert(tk.END, buffer.getvalue())
            self.output_text.insert(tk.END, "\n\u2705 Program completed.\n")
            self.set_status("Execution completed.")

    def validate_script(self):
        """Run static validation on the current script and show any issues."""
        from .dialogs import show_validation_results

        code = self.editor_text.get("1.0", tk.END)
        errors = validate_script_text(code)
        show_validation_results(self.root, errors)

    def show_error_history(self):
        from .dialogs import show_error_history

        show_error_history(self.root, self.error_history)

    def clear_error_history(self):
        self.error_history = []

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def _prompt_input(self, var_name, prompt_type="town_hall"):
        title = "TOWN_HALL Input" if prompt_type == "town_hall" else "INPUT_BOX"
        result = simpledialog.askstring(
            title, f"Enter a value for {var_name}:", parent=self.root
        )
        return result if result is not None else ""

    # ------------------------------------------------------------------
    # Graphics callbacks
    # ------------------------------------------------------------------

    def _graphics_clear(self):
        self.canvas.delete("all")

    def _set_pen_color(self, value):
        self.pen_color = str(value)

    def _set_fill_color(self, value):
        self.fill_color = str(value)

    def _set_canvas_background(self, value):
        self.canvas_bg = str(value)
        self.canvas.configure(bg=self.canvas_bg)

    def _set_pen_width(self, value):
        self.pen_width = max(1, int(self._as_number(value)))

    @staticmethod
    def _as_number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(
            self._as_number(x1),
            self._as_number(y1),
            self._as_number(x2),
            self._as_number(y2),
            fill=self.pen_color,
            width=self.pen_width,
        )

    def _draw_rectangle(self, x, y, width, height):
        x, y = self._as_number(x), self._as_number(y)
        self.canvas.create_rectangle(
            x,
            y,
            x + self._as_number(width),
            y + self._as_number(height),
            outline=self.pen_color,
            width=self.pen_width,
            fill="",
        )

    def _fill_rectangle(self, x, y, width, height):
        x, y = self._as_number(x), self._as_number(y)
        self.canvas.create_rectangle(
            x,
            y,
            x + self._as_number(width),
            y + self._as_number(height),
            outline=self.pen_color,
            width=1,
            fill=self.fill_color,
        )

    def _draw_circle(self, x, y, radius):
        cx, cy, r = self._as_number(x), self._as_number(y), self._as_number(radius)
        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            outline=self.pen_color,
            width=self.pen_width,
            fill="",
        )

    def _fill_circle(self, x, y, radius):
        cx, cy, r = self._as_number(x), self._as_number(y), self._as_number(radius)
        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            outline=self.pen_color,
            width=1,
            fill=self.fill_color,
        )

    def _draw_point(self, x, y):
        cx, cy = self._as_number(x), self._as_number(y)
        r = max(1, self.pen_width) / 2
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, outline=self.pen_color, fill=self.pen_color
        )

    def _draw_oval(self, x1, y1, x2, y2):
        self.canvas.create_oval(
            self._as_number(x1),
            self._as_number(y1),
            self._as_number(x2),
            self._as_number(y2),
            outline=self.pen_color,
            width=self.pen_width,
            fill="",
        )

    def _fill_oval(self, x1, y1, x2, y2):
        self.canvas.create_oval(
            self._as_number(x1),
            self._as_number(y1),
            self._as_number(x2),
            self._as_number(y2),
            outline=self.pen_color,
            width=1,
            fill=self.fill_color,
        )

    def _draw_arc(self, x, y, radius, start, extent):
        cx, cy, r = self._as_number(x), self._as_number(y), self._as_number(radius)
        self.canvas.create_arc(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            start=self._as_number(start),
            extent=self._as_number(extent),
            outline=self.pen_color,
            width=self.pen_width,
            style=tk.ARC,
        )

    def _draw_polygon(self, *coords):
        self.canvas.create_polygon(
            [self._as_number(c) for c in coords],
            outline=self.pen_color,
            width=self.pen_width,
            fill="",
        )

    def _fill_polygon(self, *coords):
        self.canvas.create_polygon(
            [self._as_number(c) for c in coords],
            outline=self.pen_color,
            width=1,
            fill=self.fill_color,
        )

    def _draw_triangle(self, x1, y1, x2, y2, x3, y3):
        self._draw_polygon(x1, y1, x2, y2, x3, y3)

    def _fill_triangle(self, x1, y1, x2, y2, x3, y3):
        self._fill_polygon(x1, y1, x2, y2, x3, y3)

    def _draw_text(self, x, y, text):
        self.canvas.create_text(
            self._as_number(x),
            self._as_number(y),
            text=str(text),
            anchor="nw",
            fill=self.pen_color,
            font=("Arial", 12, "bold"),
        )

    # ------------------------------------------------------------------
    # Sound callbacks
    # ------------------------------------------------------------------

    def _play_tone(self, frequency, duration_ms):
        frequency = self._as_number(frequency)
        duration_ms = self._as_number(duration_ms)
        if sys.platform.startswith("win"):
            try:
                import winsound

                winsound.Beep(int(frequency), int(duration_ms))
                return
            except (ImportError, ValueError, RuntimeError):
                pass
        self.root.bell()
        time.sleep(min(duration_ms, 1000.0) / 1000.0)

    def _stop_sound(self):
        if sys.platform.startswith("win"):
            try:
                import winsound

                winsound.PlaySound(None, winsound.SND_PURGE)
            except ImportError:
                pass

    def _play_sound_file(self, path):
        path = str(path).strip("\"'")
        if sys.platform.startswith("win"):
            try:
                import winsound

                winsound.PlaySound(
                    path, winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            except (ImportError, RuntimeError):
                pass
            return
        player = (
            shutil.which("afplay")
            if sys.platform == "darwin"
            else (shutil.which("paplay") or shutil.which("aplay"))
        )
        if player:
            subprocess.Popen(
                [player, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

    # ------------------------------------------------------------------
    # Theme & font
    # ------------------------------------------------------------------

    def apply_theme(self, theme_key):
        """Apply the given colour theme to all GUI widgets."""
        theme = THEMES[theme_key]

        for editor in self.editor_tabs.values():
            if hasattr(editor, "text"):
                editor.text.config(
                    bg=theme["text_bg"],
                    fg=theme["text_fg"],
                    insertbackground=theme["text_fg"],
                )
                if hasattr(editor, "set_theme"):
                    editor.set_theme(theme_key)
                if hasattr(editor, "line_numbers"):
                    bg = LINE_NUMBER_BG.get(theme_key, "#1e1e1e")
                    editor.line_numbers.config(bg=bg)
            else:
                editor.config(
                    bg=theme["text_bg"],
                    fg=theme["text_fg"],
                    insertbackground=theme["text_fg"],
                )

        self.output_text.config(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"],
            bd=0,
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )

        self.canvas.config(
            bg=theme["canvas_bg"],
            highlightbackground=theme["canvas_border"],
            highlightthickness=2,
        )
        self.canvas_bg = theme["canvas_bg"]

        w = self._layout_widgets
        self.root.config(bg=theme["root_bg"])
        w["left_panel"].config(bg=theme["frame_bg"])
        w["editor_container"].config(bg=theme["frame_bg"])
        w["right_panel"].config(bg=theme["frame_bg"])
        w["editor_frame"].config(
            bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"]
        )
        w["output_frame"].config(
            bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"]
        )
        w["graphics_frame"].config(
            bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"]
        )
        w["input_frame"].config(bg=theme["frame_bg"])
        w["button_frame"].config(bg=theme["frame_bg"])
        w["editor_header"].config(bg=theme["frame_bg"])

        for frame_key in ("editor_header", "input_frame"):
            for child in w[frame_key].winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=theme["frame_bg"], fg=theme["text_fg"])

        if hasattr(self, "file_label"):
            self.file_label.config(bg=theme["frame_bg"], fg="#93c5fd")
        if hasattr(self, "cursor_label"):
            self.cursor_label.config(bg=theme["frame_bg"], fg="#a7f3d0")

        self.current_theme = theme_key
        self._save_settings()

    def apply_font_family(self, family):
        """Change the editor and output font family."""
        self.current_font_family = family
        size = FONT_SIZES[self.current_font]
        for editor in self.editor_tabs.values():
            if hasattr(editor, "set_font"):
                editor.set_font((family, size["editor"]))
            else:
                editor.config(font=(family, size["editor"]))
        self.output_text.config(font=(family, size["output"]))
        self._save_settings()

    def apply_font_size(self, size_key):
        """Change the editor and output font size."""
        self.current_font = size_key
        size = FONT_SIZES[size_key]
        for editor in self.editor_tabs.values():
            if hasattr(editor, "set_font"):
                editor.set_font((self.current_font_family, size["editor"]))
            else:
                editor.config(font=(self.current_font_family, size["editor"]))
        self.output_text.config(font=(self.current_font_family, size["output"]))
        self._save_settings()

    # ------------------------------------------------------------------
    # Application lifecycle
    # ------------------------------------------------------------------

    def exit_app(self):
        """Prompt the user and exit the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def run(self):
        """Start the Tk main loop."""
        self.root.mainloop()


def main():
    """Entry point — launches the Lake Ontario BASIC IDE."""
    app = LakeOntarioApp()
    app.run()


if __name__ == "__main__":
    main()
