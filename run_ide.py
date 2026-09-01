#!/usr/bin/env python3
"""Standalone Lake Ontario BASIC IDE launcher.

This launcher ensures the project is running inside a local virtual environment,
installs the project and any declared Python requirements when needed, and then
starts the GUI IDE.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
REQUIREMENTS_FILE = ROOT / "requirements.txt"


def _is_in_venv() -> bool:
    return sys.prefix != sys.base_prefix or "VIRTUAL_ENV" in os.environ


def _ensure_venv() -> None:
    if VENV_PYTHON.exists():
        return

    print("Creating Lake Ontario BASIC virtual environment in .venv...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)


def _install_requirements() -> None:
    if not VENV_PYTHON.exists():
        raise FileNotFoundError(f"Virtual environment Python not found: {VENV_PYTHON}")

    print("Upgrading pip in the project virtual environment...")
    subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip"], check=True)

    if REQUIREMENTS_FILE.exists():
        print("Installing project requirements from requirements.txt...")
        subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)], check=True)
    else:
        print("Installing the Lake Ontario project in editable mode...")
        subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "-e", "."], check=True, cwd=str(ROOT))

    print("Verifying tkinter is available inside the project environment...")
    subprocess.run(
        [str(VENV_PYTHON), "-c", "import tkinter; print(tkinter.TkVersion)"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _bootstrap_if_needed() -> None:
    if _is_in_venv():
        return

    _ensure_venv()
    _install_requirements()

    env = os.environ.copy()
    env["LAKE_ONTARIO_BOOTSTRAPPED"] = "1"
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(ROOT / "run_ide.py"), *sys.argv[1:]], env)


if __name__ == "__main__":
    _bootstrap_if_needed()

    try:
        from lake_ontario_ide.gui import main
    except ModuleNotFoundError as exc:
        print(
            "The project package is not available in the current environment. "
            "Attempting one final install..."
        )
        _install_requirements()
        from lake_ontario_ide.gui import main

    main()
