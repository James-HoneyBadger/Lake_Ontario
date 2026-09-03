#!/usr/bin/env python3
"""
Syntax Highlighting and Line Numbers for the Lake Ontario BASIC IDE
====================================================================

Ported from Time Warp Classic's ``core/features/syntax_highlighting.py``
(https://github.com/James-HoneyBadger/Time_Warp_Classic). Provides syntax
highlighting and line number display for the code editor. Uses pygments
for syntax highlighting and custom tkinter widgets for line numbers.
"""

import tkinter as tk
import re
from typing import Dict, Tuple, Optional

try:
    from pygments.lexers import TextLexer

    PYGMENTS_AVAILABLE = True
except ImportError as e:
    PYGMENTS_AVAILABLE = False
    print(f"⚠️  Pygments not available - syntax highlighting disabled: {e}")


class SyntaxHighlightingText(tk.Frame):
    """
    A text widget with syntax highlighting and line numbers.

    Features:
    - Real-time syntax highlighting based on language
    - Line numbers display
    - Configurable themes
    - Efficient updates to avoid performance issues
    """

    def __init__(self, parent, language="text", theme="dark", **kwargs):
        """
        Initialize the syntax highlighting text widget.

        Args:
            parent: Parent tkinter widget
            language: Programming language for syntax highlighting
            theme: Color theme name
            **kwargs: Additional arguments for the text widget
        """
        super().__init__(parent)

        self.language = language
        self.theme = theme
        self.lexer = None
        self._highlight_tags = {}  # Store tag configurations
        self._last_highlighted_text = ""
        self._highlight_scheduled = False

        # Create line numbers canvas
        self.line_numbers = tk.Canvas(
            self, width=40, bg="#1e1e1e", highlightthickness=0
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Create text widget
        self.text = tk.Text(
            self, wrap=tk.NONE, font=("Courier", 11), undo=True, maxundo=-1, **kwargs
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar
        scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._on_scroll)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.text.config(
            yscrollcommand=lambda *args: (
                scrollbar_y.set(*args),
                self._update_line_numbers(),
            ),
            xscrollcommand=scrollbar_x.set,
        )

        # Bind events
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<Button-1>", self._update_line_numbers)
        self.text.bind("<FocusIn>", self._update_line_numbers)
        self.text.bind("<Configure>", self._update_line_numbers)

        # Initialize syntax highlighting
        self._setup_syntax_highlighting()
        self._update_line_numbers()

    def _setup_syntax_highlighting(self):
        """Set up syntax highlighting for the current language."""
        if not PYGMENTS_AVAILABLE:
            return

        # Clear existing tags
        for tag in self.text.tag_names():
            if tag.startswith("syntax_"):
                self.text.tag_delete(tag)

        # Lake Ontario BASIC has no dedicated Pygments lexer, so we fall
        # back to plain-text tokenization (keywords are still readable
        # thanks to line numbers + theme colors).
        try:
            self.lexer = TextLexer()
        except Exception:
            self.lexer = None

        # Set up syntax highlighting tags based on theme
        self._setup_highlight_tags()

    def _setup_highlight_tags(self):
        """Set up syntax highlighting tags based on current theme."""
        theme_colors = self._get_theme_colors()

        # Define tag configurations for different token types
        tag_configs = {
            "syntax_keyword": {"foreground": theme_colors["keyword"]},
            "syntax_string": {"foreground": theme_colors["string"]},
            "syntax_comment": {"foreground": theme_colors["comment"]},
            "syntax_number": {"foreground": theme_colors["number"]},
            "syntax_function": {"foreground": theme_colors["function"]},
            "syntax_class": {"foreground": theme_colors["class"]},
            "syntax_variable": {"foreground": theme_colors["variable"]},
            "syntax_operator": {"foreground": theme_colors["operator"]},
        }

        for tag_name, config in tag_configs.items():
            self.text.tag_configure(tag_name, **config)
            self._highlight_tags[tag_name] = config

    def _get_theme_colors(self) -> Dict[str, str]:
        """Get syntax highlighting colors for the current theme."""
        theme_colors = {
            "dark": {
                "keyword": "#569CD6",  # Blue
                "string": "#CE9178",  # Orange
                "comment": "#6A9955",  # Green
                "number": "#B5CEA8",  # Light green
                "function": "#DCDCAA",  # Yellow
                "class": "#4EC9B0",  # Teal
                "variable": "#9CDCFE",  # Light blue
                "operator": "#D4D4D4",  # Light gray
            },
            "light": {
                "keyword": "#0000FF",  # Blue
                "string": "#A31515",  # Dark red
                "comment": "#008000",  # Green
                "number": "#09885A",  # Dark green
                "function": "#795E26",  # Brown
                "class": "#267F99",  # Teal
                "variable": "#001080",  # Dark blue
                "operator": "#000000",  # Black
            },
            "monokai": {
                "keyword": "#F92672",  # Pink
                "string": "#E6DB74",  # Yellow
                "comment": "#75715E",  # Gray
                "number": "#AE81FF",  # Purple
                "function": "#A6E22E",  # Green
                "class": "#66D9EF",  # Blue
                "variable": "#F8F8F2",  # White
                "operator": "#F92672",  # Pink
            },
        }

        return theme_colors.get(self.theme, theme_colors["dark"])

    def set_language(self, language: str):
        """Set the programming language for syntax highlighting."""
        self.language = language
        self._setup_syntax_highlighting()
        self._highlight_text()

    def set_theme(self, theme: str):
        """Set the color theme for syntax highlighting."""
        self.theme = theme
        self._setup_highlight_tags()
        self._highlight_text()
        self._update_line_numbers()

    def _on_key_release(self, event=None):
        """Handle key release events for syntax highlighting."""
        if not self._highlight_scheduled:
            self._highlight_scheduled = True
            self.after(100, self._delayed_highlight)  # Debounce highlighting

    def _delayed_highlight(self):
        """Delayed syntax highlighting to improve performance."""
        self._highlight_scheduled = False
        self._highlight_text()

    def _highlight_text(self):
        """Apply syntax highlighting to the current text."""
        if not PYGMENTS_AVAILABLE or not self.lexer:
            return

        current_text = self.text.get("1.0", tk.END)

        # Skip highlighting if text hasn't changed
        if current_text == self._last_highlighted_text:
            return

        self._last_highlighted_text = current_text

        # Remove existing syntax tags
        for tag in self.text.tag_names():
            if tag.startswith("syntax_"):
                self.text.tag_remove(tag, "1.0", tk.END)

        try:
            # Get tokens from pygments
            tokens = self.lexer.get_tokens(current_text)

            # Apply highlighting
            pos = "1.0"
            for token_type, value in tokens:
                if not value:
                    continue

                # Calculate end position
                lines = value.count("\n")
                if lines > 0:
                    last_line_chars = len(value.split("\n")[-1])
                    end_pos = f"{int(pos.split('.', maxsplit=1)[0]) + lines}.{last_line_chars}"
                else:
                    end_pos = f"{pos.split('.', maxsplit=1)[0]}.{int(pos.split('.', maxsplit=1)[1]) + len(value)}"

                # Map token type to tag
                tag = self._get_tag_for_token(token_type)
                if tag:
                    self.text.tag_add(tag, pos, end_pos)

                pos = end_pos

        except Exception:
            # If highlighting fails, just continue without it
            pass

    def _get_tag_for_token(self, token_type) -> Optional[str]:
        """Map pygments token type to syntax highlighting tag."""
        try:
            from pygments.token import Token
        except ImportError:
            return None

        token_map = {
            Token.Keyword: "syntax_keyword",
            Token.Keyword.Constant: "syntax_keyword",
            Token.Keyword.Declaration: "syntax_keyword",
            Token.Keyword.Namespace: "syntax_keyword",
            Token.Keyword.Pseudo: "syntax_keyword",
            Token.Keyword.Reserved: "syntax_keyword",
            Token.Keyword.Type: "syntax_keyword",
            Token.Literal.String: "syntax_string",
            Token.Literal.String.Backtick: "syntax_string",
            Token.Literal.String.Char: "syntax_string",
            Token.Literal.String.Doc: "syntax_string",
            Token.Literal.String.Double: "syntax_string",
            Token.Literal.String.Escape: "syntax_string",
            Token.Literal.String.Heredoc: "syntax_string",
            Token.Literal.String.Interpol: "syntax_string",
            Token.Literal.String.Other: "syntax_string",
            Token.Literal.String.Regex: "syntax_string",
            Token.Literal.String.Single: "syntax_string",
            Token.Literal.String.Symbol: "syntax_string",
            Token.Comment: "syntax_comment",
            Token.Comment.Hashbang: "syntax_comment",
            Token.Comment.Multiline: "syntax_comment",
            Token.Comment.Single: "syntax_comment",
            Token.Comment.Special: "syntax_comment",
            Token.Literal.Number: "syntax_number",
            Token.Literal.Number.Bin: "syntax_number",
            Token.Literal.Number.Float: "syntax_number",
            Token.Literal.Number.Hex: "syntax_number",
            Token.Literal.Number.Integer: "syntax_number",
            Token.Literal.Number.Long: "syntax_number",
            Token.Literal.Number.Oct: "syntax_number",
            Token.Name.Function: "syntax_function",
            Token.Name.Class: "syntax_class",
            Token.Name.Variable: "syntax_variable",
            Token.Name.Attribute: "syntax_variable",
            Token.Operator: "syntax_operator",
            Token.Punctuation: "syntax_operator",
        }

        return token_map.get(token_type)

    def _update_line_numbers(self, event=None):
        """Update the line numbers display."""
        self.line_numbers.delete("all")

        # Get text widget dimensions
        text_widget = self.text
        first_visible_line = int(text_widget.index("@0,0").split(".", maxsplit=1)[0])
        last_visible_line = int(text_widget.index("@0,10000").split(".", maxsplit=1)[0])

        bg_color = {"dark": "#1e1e1e", "light": "#f0f0f0", "monokai": "#272822"}.get(
            self.theme, "#1e1e1e"
        )
        fg_color = {"dark": "#858585", "light": "#237893", "monokai": "#90908a"}.get(
            self.theme, "#858585"
        )

        self.line_numbers.config(bg=bg_color)

        # Draw line numbers
        y = 2
        line_height = 16  # Approximate line height
        font = ("Courier", 10)

        for line_num in range(first_visible_line, last_visible_line + 1):
            if line_num > 0:  # Skip line 0
                self.line_numbers.create_text(
                    35,
                    y,  # Right-aligned
                    text=str(line_num),
                    anchor="e",
                    font=font,
                    fill=fg_color,
                )
            y += line_height

    def _on_scroll(self, *args):
        """Handle scroll events."""
        self.text.yview(*args)
        self._update_line_numbers()

    def set_font(self, font_tuple):
        """Set the font for the text widget."""
        self.text.config(font=font_tuple)

    def find_text(
        self,
        search_term: str,
        start_pos: str = "1.0",
        case_sensitive: bool = False,
        whole_word: bool = False,
        regex: bool = False,
    ) -> Optional[Tuple[str, str]]:
        """
        Find the next occurrence of search_term starting from start_pos.

        Args:
            search_term: Text to search for
            start_pos: Starting position (tkinter text index)
            case_sensitive: Whether search is case sensitive
            whole_word: Whether to match whole words only
            regex: Whether search_term is a regex pattern

        Returns:
            Tuple of (start_index, end_index) if found, None otherwise
        """
        if not search_term:
            return None

        text_content = self.text.get("1.0", tk.END)

        # Get the character position from start_pos
        start_line, start_col = map(int, start_pos.split("."))
        start_char = 0

        # Calculate character offset for start_pos
        lines = text_content.split("\n")
        for i in range(min(start_line - 1, len(lines))):
            start_char += len(lines[i]) + 1  # +1 for newline
        start_char += start_col

        search_text = text_content[start_char:]

        if regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            if whole_word:
                pattern = r"\b" + search_term + r"\b"
            else:
                pattern = search_term
            match = re.search(pattern, search_text, flags)
            if match:
                match_start = start_char + match.start()
                match_end = start_char + match.end()
                return self._char_to_index(match_start), self._char_to_index(match_end)
        else:
            if not case_sensitive:
                search_text = search_text.lower()
                search_term = search_term.lower()

            if whole_word:
                # Simple whole word matching
                pattern = r"\b" + re.escape(search_term) + r"\b"
                flags = 0 if case_sensitive else re.IGNORECASE
                match = re.search(pattern, search_text, flags)
                if match:
                    match_start = start_char + match.start()
                    match_end = start_char + match.end()
                    return self._char_to_index(match_start), self._char_to_index(
                        match_end
                    )
            else:
                pos = search_text.find(search_term)
                if pos != -1:
                    match_start = start_char + pos
                    match_end = start_char + pos + len(search_term)
                    return self._char_to_index(match_start), self._char_to_index(
                        match_end
                    )

        return None

    def replace_text(
        self,
        search_term: str,
        replace_term: str,
        start_pos: str = "1.0",
        case_sensitive: bool = False,
        whole_word: bool = False,
        regex: bool = False,
    ) -> bool:
        """
        Replace the next occurrence of search_term with replace_term.

        Args:
            search_term: Text to search for
            replace_term: Text to replace with
            start_pos: Starting position
            case_sensitive: Whether search is case sensitive
            whole_word: Whether to match whole words only
            regex: Whether search_term is a regex pattern

        Returns:
            True if replacement was made, False otherwise
        """
        match = self.find_text(
            search_term, start_pos, case_sensitive, whole_word, regex
        )
        if match:
            start_idx, end_idx = match
            self.text.delete(start_idx, end_idx)
            self.text.insert(start_idx, replace_term)
            self.text.mark_set(tk.INSERT, f"{start_idx}+{len(replace_term)}c")
            self.text.see(start_idx)
            return True
        return False

    def replace_all(
        self,
        search_term: str,
        replace_term: str,
        case_sensitive: bool = False,
        whole_word: bool = False,
        regex: bool = False,
    ) -> int:
        """
        Replace all occurrences of search_term with replace_term.

        Args:
            search_term: Text to search for
            replace_term: Text to replace with
            case_sensitive: Whether search is case sensitive
            whole_word: Whether to match whole words only
            regex: Whether search_term is a regex pattern

        Returns:
            Number of replacements made
        """
        count = 0
        start_pos = "1.0"

        while True:
            match = self.find_text(
                search_term, start_pos, case_sensitive, whole_word, regex
            )
            if not match:
                break

            start_idx, end_idx = match
            self.text.delete(start_idx, end_idx)
            self.text.insert(start_idx, replace_term)
            count += 1

            # Move start_pos to after the replacement
            start_pos = self.text.index(f"{start_idx}+{len(replace_term)}c")

        if count > 0:
            self.text.see("1.0")
            self._highlight_text()  # Re-highlight after replacements

        return count

    def highlight_search_results(
        self,
        search_term: str,
        case_sensitive: bool = False,
        whole_word: bool = False,
        regex: bool = False,
    ):
        """
        Highlight all search results with a special tag.
        """
        # Remove existing search highlights
        self.text.tag_remove("search_highlight", "1.0", tk.END)

        if not search_term:
            return

        start_pos = "1.0"
        while True:
            match = self.find_text(
                search_term, start_pos, case_sensitive, whole_word, regex
            )
            if not match:
                break

            start_idx, end_idx = match
            self.text.tag_add("search_highlight", start_idx, end_idx)
            start_pos = end_idx

        # Configure the search highlight tag
        bg_color = {"dark": "#264f78", "light": "#a6d2ff", "monokai": "#49483e"}.get(
            self.theme, "#264f78"
        )
        self.text.tag_configure("search_highlight", background=bg_color)

    def clear_search_highlights(self):
        """Clear all search result highlights."""
        self.text.tag_remove("search_highlight", "1.0", tk.END)

    def _char_to_index(self, char_pos: int) -> str:
        """Convert character position to tkinter text index."""
        text_content = self.text.get("1.0", tk.END)
        lines = text_content.split("\n")

        current_char = 0
        for line_num, line in enumerate(lines, 1):
            line_len = len(line) + 1  # +1 for newline
            if current_char + line_len > char_pos:
                col = char_pos - current_char
                return f"{line_num}.{col}"
            current_char += line_len

        # If we get here, position is at or beyond end
        return f"{len(lines)}.{len(lines[-1])}"

    # Delegate text widget methods
    def __getattr__(self, name):
        """Delegate attribute access to the text widget."""
        return getattr(self.text, name)


class LineNumberedText(tk.Frame):
    """
    A simpler version with just line numbers (fallback if pygments not available).
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        # Create line numbers canvas
        self.line_numbers = tk.Canvas(
            self, width=40, bg="#1e1e1e", highlightthickness=0
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Create text widget
        self.text = tk.Text(
            self, wrap=tk.NONE, font=("Courier", 11), undo=True, maxundo=-1, **kwargs
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar
        scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._on_scroll)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.text.config(
            yscrollcommand=lambda *args: (
                scrollbar_y.set(*args),
                self._update_line_numbers(),
            ),
            xscrollcommand=scrollbar_x.set,
        )

        # Bind events
        self.text.bind("<KeyRelease>", self._update_line_numbers)
        self.text.bind("<Button-1>", self._update_line_numbers)
        self.text.bind("<FocusIn>", self._update_line_numbers)
        self.text.bind("<Configure>", self._update_line_numbers)

        self._update_line_numbers()

    def _update_line_numbers(self, event=None):
        """Update the line numbers display."""
        self.line_numbers.delete("all")

        # Get text widget dimensions
        text_widget = self.text
        first_visible_line = int(text_widget.index("@0,0").split(".", maxsplit=1)[0])
        last_visible_line = int(text_widget.index("@0,10000").split(".", maxsplit=1)[0])

        # Theme-aware colors
        bg_color = "#1e1e1e"
        fg_color = "#858585"

        self.line_numbers.config(bg=bg_color)

        # Draw line numbers
        y = 2
        line_height = 16
        font = ("Courier", 10)

        for line_num in range(first_visible_line, last_visible_line + 1):
            if line_num > 0:
                self.line_numbers.create_text(
                    35, y, text=str(line_num), anchor="e", font=font, fill=fg_color
                )
            y += line_height

    def _on_scroll(self, *args):
        """Handle scroll events."""
        self.text.yview(*args)
        self._update_line_numbers()

    def set_font(self, font_tuple):
        """Set the font for the text widget."""
        self.text.config(font=font_tuple)

    # ---- Search / Replace methods (parity with SyntaxHighlightingText) ----

    def find_text(
        self,
        search_term,
        start_pos="1.0",
        case_sensitive=False,
        whole_word=False,
        regex=False,
    ):
        """Find the next occurrence of search_term starting from start_pos."""
        if not search_term:
            return None

        text_content = self.text.get("1.0", tk.END)
        start_line, start_col = map(int, start_pos.split("."))
        start_char = 0
        lines = text_content.split("\n")
        for i in range(min(start_line - 1, len(lines))):
            start_char += len(lines[i]) + 1
        start_char += start_col
        search_text = text_content[start_char:]

        if regex or whole_word:
            flags = 0 if case_sensitive else re.IGNORECASE
            if whole_word and not regex:
                pattern = r"\b" + re.escape(search_term) + r"\b"
            elif whole_word:
                pattern = r"\b" + search_term + r"\b"
            else:
                pattern = search_term
            m = re.search(pattern, search_text, flags)
            if m:
                return (
                    self._char_to_index(start_char + m.start()),
                    self._char_to_index(start_char + m.end()),
                )
        else:
            hay = search_text if case_sensitive else search_text.lower()
            needle = search_term if case_sensitive else search_term.lower()
            pos = hay.find(needle)
            if pos != -1:
                return (
                    self._char_to_index(start_char + pos),
                    self._char_to_index(start_char + pos + len(search_term)),
                )
        return None

    def replace_text(
        self,
        search_term,
        replace_term,
        start_pos="1.0",
        case_sensitive=False,
        whole_word=False,
        regex=False,
    ):
        """Replace the next occurrence of search_term with replace_term."""
        match = self.find_text(
            search_term, start_pos, case_sensitive, whole_word, regex
        )
        if match:
            start_idx, end_idx = match
            self.text.delete(start_idx, end_idx)
            self.text.insert(start_idx, replace_term)
            self.text.mark_set(tk.INSERT, f"{start_idx}+{len(replace_term)}c")
            self.text.see(start_idx)
            return True
        return False

    def replace_all(
        self,
        search_term,
        replace_term,
        case_sensitive=False,
        whole_word=False,
        regex=False,
    ):
        """Replace all occurrences. Returns count of replacements."""
        count = 0
        start_pos = "1.0"
        while True:
            match = self.find_text(
                search_term, start_pos, case_sensitive, whole_word, regex
            )
            if not match:
                break
            start_idx, end_idx = match
            self.text.delete(start_idx, end_idx)
            self.text.insert(start_idx, replace_term)
            count += 1
            start_pos = self.text.index(f"{start_idx}+{len(replace_term)}c")
        return count

    def highlight_search_results(
        self, search_term, case_sensitive=False, whole_word=False, regex=False
    ):
        """Highlight all occurrences of search_term."""
        self.text.tag_remove("search_highlight", "1.0", tk.END)
        if not search_term:
            return
        start_pos = "1.0"
        while True:
            match = self.find_text(
                search_term, start_pos, case_sensitive, whole_word, regex
            )
            if not match:
                break
            start_idx, end_idx = match
            self.text.tag_add("search_highlight", start_idx, end_idx)
            start_pos = end_idx
        self.text.tag_configure("search_highlight", background="#264f78")

    def clear_search_highlights(self):
        """Clear all search result highlights."""
        self.text.tag_remove("search_highlight", "1.0", tk.END)

    def _char_to_index(self, char_pos):
        """Convert character position to tkinter text index."""
        text_content = self.text.get("1.0", tk.END)
        lines = text_content.split("\n")
        current_char = 0
        for line_num, line in enumerate(lines, 1):
            line_len = len(line) + 1
            if current_char + line_len > char_pos:
                col = char_pos - current_char
                return f"{line_num}.{col}"
            current_char += line_len
        return f"{len(lines)}.{len(lines[-1])}"

    def __getattr__(self, name):
        """Delegate attribute access to the text widget."""
        return getattr(self.text, name)
