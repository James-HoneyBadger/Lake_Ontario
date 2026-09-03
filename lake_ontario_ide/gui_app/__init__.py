"""
Lake Ontario BASIC GUI — Time Warp Classic Edition
===================================================

This package is the Lake Ontario BASIC IDE, rebuilt on top of the
Time Warp Classic (https://github.com/James-HoneyBadger/Time_Warp_Classic)
IDE shell: themed editor, syntax-aware text widget, find/replace dialogs,
and a menu-driven layout — wired to the ``LakeOntarioInterpreter``.
"""

from .app import LakeOntarioApp, main

__all__ = ["LakeOntarioApp", "main"]
