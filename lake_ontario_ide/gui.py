#!/usr/bin/env python3
"""
Lake Ontario BASIC GUI IDE
"""

import contextlib
import io
import os
import sys

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog, ttk
    from tkinter.scrolledtext import ScrolledText
except ImportError:
    sys.stderr.write(
        "Tkinter is required for the Lake Ontario BASIC GUI IDE. Install "
        "python3-tk and try again.\n"
    )
    sys.exit(1)

from interpreter import LakeOntarioInterpreter, LakeOntarioInterpreterError

DEFAULT_SCRIPT_TEMPLATE = """10 EXCUSE_ME Lake Ontario BASIC GUI demo script
20 LAND_ACKNOWLEDGEMENT \"Traditional Territory\"
30 BROADCAST_CBC \"Welcome to the Lake Ontario BASIC GUI!\"
40 SET_CANVAS_BG \"#f4f4f4\"
50 SET_PEN_COLOR \"#1f4f82\"
60 SET_FILL_COLOR \"#d9ead3\"
70 FILL_RECTANGLE 20, 80, 220, 120
80 SET_FILL_COLOR \"#f4cccc\"
90 FILL_CIRCLE 320, 120, 40
100 DRAW_TEXT 22, 82, \"Lake Ontario BASIC GUI Demo\"
110 DRAW_TEXT 22, 102, \"Use INPUT_BOX to ask the user a question.\"
120 INPUT_BOX user_response
130 BROADCAST_CBC user_response
"""


class LakeOntarioIDEGUI:
    def __init__(self, root):
        self.root = root
        root.title("Lake Ontario BASIC GUI IDE")
        root.geometry("1200x780")

        self.current_path = None
        self.interpreter = None
        self.theme = "dark"
        self.pen_color = "#0b5394"
        self.fill_color = "#d9ead3"
        self.canvas_bg = "white"

        self._configure_style()
        self._build_ui()
        self.new_script()

    def _configure_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", padding=6)
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TLabel", background="#2b2b2b", foreground="#f1f1f1")
        style.configure("Status.TLabel", background="#1f1f1f", foreground="#dcdcdc")

    def _build_ui(self):
        self._build_menu()

        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=6, pady=4)
        for label, command in (
            ("New", self.new_script),
            ("Open", self.open_script),
            ("Save", self.save_script),
            ("Save As", lambda: self.save_script(save_as=True)),
            ("Run", self.run_script),
            ("Clear Output", self.clear_output),
            ("Clear Canvas", self.clear_canvas),
        ):
            ttk.Button(toolbar, text=label, command=command).pack(side="left", padx=4)

        container = ttk.PanedWindow(self.root, orient="horizontal")
        container.pack(fill="both", expand=True)

        editor_panel = ttk.Frame(container)
        container.add(editor_panel, weight=3)

        right_panel = ttk.Frame(container)
        container.add(right_panel, weight=2)

        editor_header = ttk.Frame(editor_panel)
        editor_header.pack(fill="x", pady=(4, 0))
        ttk.Label(editor_header, text="Code Editor", font=(None, 11, "bold")).pack(
            side="left", padx=6
        )

        editor_body = ttk.Frame(editor_panel)
        editor_body.pack(fill="both", expand=True, padx=6, pady=6)

        self.line_numbers = tk.Text(
            editor_body,
            width=4,
            padx=4,
            takefocus=False,
            border=0,
            background="#282c34",
            foreground="#6a9955",
            state="disabled",
        )
        self.line_numbers.pack(side="left", fill="y")

        self.editor = ScrolledText(
            editor_body,
            wrap="none",
            undo=True,
            font=("Consolas", 12),
            background="#1e1e1e",
            foreground="#dcdcdc",
            insertbackground="#ffffff",
        )
        self.editor.pack(side="left", fill="both", expand=True)
        self.editor.bind("<KeyRelease>", self._on_editor_change)
        self.editor.bind("<ButtonRelease-1>", self._on_editor_change)

        self._update_line_numbers()

        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        output_tab = ttk.Frame(self.notebook)
        graphics_tab = ttk.Frame(self.notebook)
        help_tab = ttk.Frame(self.notebook)

        self.notebook.add(output_tab, text="Output")
        self.notebook.add(graphics_tab, text="Graphics")
        self.notebook.add(help_tab, text="Help")

        self.output = ScrolledText(
            output_tab,
            wrap="word",
            state="disabled",
            height=12,
            background="#111111",
            foreground="#f1f1f1",
        )
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        graphics_header = ttk.Frame(graphics_tab)
        graphics_header.pack(fill="x", pady=(6, 0), padx=6)
        ttk.Label(
            graphics_header, text="Graphics Canvas", font=(None, 11, "bold")
        ).pack(side="left")
        ttk.Button(graphics_header, text="Clear", command=self.clear_canvas).pack(
            side="right"
        )

        self.canvas = tk.Canvas(graphics_tab, bg=self.canvas_bg, bd=2, relief="sunken")
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)

        self.help_text = ScrolledText(
            help_tab,
            wrap="word",
            state="disabled",
            background="#111111",
            foreground="#f1f1f1",
        )
        self.help_text.pack(fill="both", expand=True, padx=6, pady=6)
        self.help_text.configure(state="normal")
        self.help_text.insert("1.0", self._build_help_text())
        self.help_text.configure(state="disabled")

        status_frame = ttk.Frame(self.root, style="Status.TFrame")
        status_frame.pack(fill="x")
        self.status_path = ttk.Label(
            status_frame, text="No file", style="Status.TLabel"
        )
        self.status_path.pack(side="left", padx=6)
        self.status_state = ttk.Label(
            status_frame, text="Ready.", style="Status.TLabel"
        )
        self.status_state.pack(side="right", padx=6)

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", command=self.new_script)
        file_menu.add_command(label="Open...", command=self.open_script)
        file_menu.add_command(label="Save", command=self.save_script)
        file_menu.add_command(
            label="Save As...", command=lambda: self.save_script(save_as=True)
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menubar, tearoff=False)
        run_menu.add_command(label="Run Script", command=self.run_script)
        run_menu.add_command(label="Clear Output", command=self.clear_output)
        run_menu.add_command(label="Clear Canvas", command=self.clear_canvas)
        menubar.add_cascade(label="Run", menu=run_menu)

        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Command Reference", command=self._show_help_tab)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_help_text(self):
        help_text = "Lake Ontario BASIC GUI IDE Command Reference\n\n"
        help_text += "Supported GUI commands:\n"
        help_text += "  INPUT_BOX variable_name\n"
        help_text += '  SET_PEN_COLOR "color"\n'
        help_text += '  SET_FILL_COLOR "color"\n'
        help_text += '  SET_CANVAS_BG "color"\n'
        help_text += "  FILL_RECTANGLE x, y, width, height\n"
        help_text += "  FILL_CIRCLE x, y, radius\n"
        help_text += "  DRAW_LINE x1, y1, x2, y2\n"
        help_text += "  DRAW_RECTANGLE x, y, width, height\n"
        help_text += "  DRAW_CIRCLE x, y, radius\n"
        help_text += "  DRAW_TEXT x, y, text\n"
        help_text += "  WAIT milliseconds\n\n"
        help_text += "Use TOWN_HALL and INPUT_BOX to gather user input in dialogs.\n"
        help_text += "Set canvas colors with SET_CANVAS_BG, SET_PEN_COLOR, "
        "and SET_FILL_COLOR.\n\n"
        help_text += "Command Reference:\n"
        help_text += self._load_command_reference()
        return help_text

    def _load_command_reference(self):
        try:
            with open("COMMANDS.md", "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            return "Command reference unavailable."

    def _show_help_tab(self):
        if hasattr(self, "notebook"):
            self.notebook.select(2)

    def _show_about(self):
        messagebox.showinfo(
            "About",
            "Lake Ontario BASIC GUI IDE\n\nA polished interface for the Lake Ontario "
            "BASIC interpreter.",
        )

    def _configure_interpreter(self):
        self.interpreter = LakeOntarioInterpreter()
        self.interpreter.set_input_callback(self.prompt_input)
        self.interpreter.set_graphics_callbacks(
            {
                "clear": self.clear_canvas,
                "line": self.draw_line,
                "rectangle": self.draw_rectangle,
                "circle": self.draw_circle,
                "text": self.draw_text,
                "pen_color": self.set_pen_color,
                "fill_color": self.set_fill_color,
                "canvas_bg": self.set_canvas_background,
            }
        )

    def new_script(self):
        self.current_path = None
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", DEFAULT_SCRIPT_TEMPLATE)
        self.clear_output()
        self.clear_canvas()
        self._update_status("New script loaded.")
        self._configure_interpreter()
        self._update_line_numbers()

    def open_script(self):
        path = filedialog.askopenfilename(
            title="Open Lake Ontario BASIC script",
            filetypes=[
                ("Lake Ontario BASIC", "*.lo"),
                ("Text files", "*.txt"),
                ("All files", "*"),
            ],
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as exc:
            messagebox.showerror("Open Error", f"Unable to open file: {exc}")
            return

        self.current_path = path
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
        self.clear_output()
        self.clear_canvas()
        self._update_status(f"Opened {os.path.basename(path)}")
        self._configure_interpreter()
        self._update_line_numbers()
        self._update_file_status()

    def save_script(self, save_as=False):
        if save_as or not self.current_path:
            path = filedialog.asksaveasfilename(
                title="Save Lake Ontario BASIC script",
                defaultextension=".lo",
                filetypes=[
                    ("Lake Ontario BASIC", "*.lo"),
                    ("Text files", "*.txt"),
                    ("All files", "*"),
                ],
            )
            if not path:
                return
            self.current_path = path

        try:
            with open(self.current_path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", "end-1c"))
        except OSError as exc:
            messagebox.showerror("Save Error", f"Unable to save file: {exc}")
            return

        self._update_status(f"Saved {os.path.basename(self.current_path)}")
        self._update_file_status()

    def run_script(self):
        self.clear_output()
        self.clear_canvas()
        self._configure_interpreter()

        code = self.editor.get("1.0", "end-1c")
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
            self.append_output(f"🚨 Runtime error: {exc}\n")
            self._update_status("Execution failed.")
        else:
            self.append_output(buffer.getvalue())
            self._update_status("Execution completed.")

    def prompt_input(self, var_name, prompt_type="town_hall"):
        title = "TOWN_HALL Input" if prompt_type == "town_hall" else "INPUT_BOX"
        result = simpledialog.askstring(title, f"Enter a value for {var_name}:")
        if result is None:
            return ""
        return result

    def append_output(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.configure(bg=self.canvas_bg)

    def set_pen_color(self, value):
        self.pen_color = str(value)

    def set_fill_color(self, value):
        self.fill_color = str(value)

    def set_canvas_background(self, value):
        self.canvas_bg = str(value)
        self.canvas.configure(bg=self.canvas_bg)

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(
            self._as_number(x1),
            self._as_number(y1),
            self._as_number(x2),
            self._as_number(y2),
            fill=self.pen_color,
            width=2,
        )

    def draw_rectangle(self, x, y, width, height):
        self.canvas.create_rectangle(
            self._as_number(x),
            self._as_number(y),
            self._as_number(x) + self._as_number(width),
            self._as_number(y) + self._as_number(height),
            outline=self.pen_color,
            width=2,
            fill="",
        )

    def fill_rectangle(self, x, y, width, height):
        self.canvas.create_rectangle(
            self._as_number(x),
            self._as_number(y),
            self._as_number(x) + self._as_number(width),
            self._as_number(y) + self._as_number(height),
            outline=self.pen_color,
            width=1,
            fill=self.fill_color,
        )

    def draw_circle(self, x, y, radius):
        cx = self._as_number(x)
        cy = self._as_number(y)
        r = self._as_number(radius)
        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            outline=self.pen_color,
            width=2,
            fill="",
        )

    def fill_circle(self, x, y, radius):
        cx = self._as_number(x)
        cy = self._as_number(y)
        r = self._as_number(radius)
        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            outline=self.pen_color,
            width=1,
            fill=self.fill_color,
        )

    def draw_text(self, x, y, text):
        self.canvas.create_text(
            self._as_number(x),
            self._as_number(y),
            text=str(text),
            anchor="nw",
            fill=self.pen_color,
            font=("Arial", 12, "bold"),
        )

    def _as_number(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            try:
                return float(str(value))
            except (TypeError, ValueError):
                return 0.0

    def _update_line_numbers(self):
        line_count = int(self.editor.index("end-1c").split(".")[0])
        numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", numbers)
        self.line_numbers.configure(state="disabled")

    def _update_file_status(self):
        self.status_path.configure(text=self.current_path or "No file")

    def _on_editor_change(self, event=None):
        self._update_line_numbers()
        self._update_file_status()

    def _update_status(self, message):
        self.status_state.configure(text=message)

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
            self.editor.configure(background="#ffffff", foreground="#000000")
            self.output.configure(background="#f7f7f7", foreground="#111111")
            self.line_numbers.configure(background="#f0f0f0", foreground="#242424")
            self.canvas.configure(bg=self.canvas_bg)
        else:
            self.theme = "dark"
            self.editor.configure(background="#1e1e1e", foreground="#dcdcdc")
            self.output.configure(background="#111111", foreground="#f1f1f1")
            self.line_numbers.configure(background="#282c34", foreground="#6a9955")
            self.canvas.configure(bg=self.canvas_bg)


def main():
    root = tk.Tk()
    LakeOntarioIDEGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
