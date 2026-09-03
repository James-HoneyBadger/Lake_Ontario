#!/usr/bin/env python3
"""
Lake Ontario BASIC GUI IDE — Time Warp Classic Edition.

This module is a thin compatibility entry point. The full IDE
implementation (editor, themes, menus, dialogs) lives in
``lake_ontario_ide.gui_app``, adapted from Time Warp Classic
(https://github.com/James-HoneyBadger/Time_Warp_Classic).
"""

from .gui_app.app import LakeOntarioApp, main

__all__ = ["LakeOntarioApp", "main"]

if __name__ == "__main__":
    main()
