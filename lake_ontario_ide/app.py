#!/usr/bin/env python3
"""
Lake Ontario BASIC IDE Package

A lightweight command-line IDE for editing, running, and exploring Lake Ontario
BASIC scripts.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from interpreter import (
    LakeOntarioInterpreter,
    LakeOntarioInterpreterError,
    validate_script as validate_script_text,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"

FARCICAL_POLICY_HELP = """
Farcical Lake Ontario Policy Help

Statement Keywords:
  FAT_CATS_TAX amount            - Redistribute absurd wealth with theatrical flair.
  DONUT_DIVIDEND amount          - Deliver pastry payouts to every solidarity line.
  NATIONAL_STOOGE statement      - Publish a spin-heavy political performance.
  GREEN_NEW_DEAL goal            - Announce a bold climate-and-transit policy agenda.
  RHETORICAL_QUESTION question   - Ask a question with an obvious evidence-based answer.
  LOONIE_LOOP count              - Iterate a whimsical loop of symbolic loonies.
  SOCIAL_LICENSE name            - Grant approval from unionized beavers and poets.
  ELECTORATE_PULSE value         - Report a mock public enthusiasm percentage.
  NATIONAL_HEALTHCARE            - Alias for UNIVERSAL_HEALTHCARE with extra pomp.

Built-in Functions:
  FAT_CATS_TAX(amount)
  DONUT_DIVIDEND(amount)
  NATIONAL_STOOGE(statement)
  GREEN_NEW_DEAL(goal)
  RHETORICAL_QUESTION(question)
  LOONIE_LOOP(count)
  SOCIAL_LICENSE(name)
  ELECTORATE_PULSE(value)

Operators:
  MAPLE_SYRUP -> %             - Modulus with extra Canadian sweetness.
  MOONSHOT    -> **            - Exponentiation for ambitious policy goals.

Examples:
  FAT_CATS_TAX 2500000
  DONUT_DIVIDEND 1000
  NATIONAL_STOOGE "We are totally not lying, eh!"
  GREEN_NEW_DEAL "Zero-emission buses for every province"
  RHETORICAL_QUESTION "Was this always evidence-based?"
  LOONIE_LOOP 5
  SOCIAL_LICENSE "Climate Action Coalition"
  ELECTORATE_PULSE 87.5
"""


def clear_screen():
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "cls"], check=False)
    else:
        subprocess.run(["clear"], check=False)


def pause():
    input("\nPress Enter to return to the IDE menu...")


RUN_HISTORY = []


def load_command_reference():
    reference_path = ROOT_DIR / "COMMANDS.md"
    try:
        return reference_path.read_text(encoding="utf-8")
    except OSError:
        return "Command reference unavailable."


def list_examples():
    if not EXAMPLES_DIR.is_dir():
        return []
    return sorted(
        [f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".lo")],
        key=str.lower,
    )


def add_history(path):
    normalized = os.path.abspath(path)
    if normalized in RUN_HISTORY:
        RUN_HISTORY.remove(normalized)
    RUN_HISTORY.insert(0, normalized)
    if len(RUN_HISTORY) > 10:
        del RUN_HISTORY[10:]


def view_history():
    if not RUN_HISTORY:
        print("\nNo run history yet.")
        return

    print("\nRecent script history:")
    for idx, path in enumerate(RUN_HISTORY, 1):
        print(f"  {idx}. {path}")


def validate_script(path):
    if not os.path.exists(path):
        return [f"Script not found: {path}"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
    except OSError as exc:
        return [f"Unable to read script: {exc}"]

    return validate_script_text(code)


def choose_script():
    examples = list_examples()
    if not examples:
        custom = input("No bundled examples found. Enter script file path: ").strip()
        return os.path.abspath(custom) if custom else None

    print("\nAvailable examples:")
    for idx, name in enumerate(examples, 1):
        print(f"  {idx}. {name}")
    print("  0. Enter a custom script path")

    choice = input("Select a script number or path: ").strip()
    if choice == "0":
        custom = input("Enter script file path: ").strip()
        return os.path.abspath(custom)
    if choice.isdigit() and 1 <= int(choice) <= len(examples):
        return os.path.abspath(EXAMPLES_DIR / examples[int(choice) - 1])
    return None


def edit_script(path):
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("10 EXCUSE_ME Lake Ontario BASIC script created by the IDE\n")
            f.write('20 LAND_ACKNOWLEDGEMENT "Traditional Territory"\n')
            f.write('30 FACT_CHECK greeting = "Hello from Lake Ontario BASIC!"\n')
            f.write("40 BROADCAST_CBC greeting\n")

    editor = os.environ.get("EDITOR")
    if not editor:
        editor = shutil.which("nano") or shutil.which("vi") or shutil.which("code")
    if not editor:
        print("No editor detected. Please set the EDITOR environment variable.")
        return

    try:
        subprocess.run([editor, path], check=False)
    except OSError:
        print(f"Unable to launch editor: {editor}")


def run_script(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        print(f"Script not found: {path}")
        return

    validation_errors = validate_script(path)
    if validation_errors:
        print("\nValidation issues found:")
        for error in validation_errors:
            print(f"  - {error}")
        proceed = input("\nRun anyway? (y/N): ").strip().lower()
        if proceed != "y":
            print("Run aborted.")
            return

    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
    except OSError as exc:
        print(f"Unable to read script: {exc}")
        return

    interpreter = LakeOntarioInterpreter()
    interpreter.load_script(code)
    add_history(path)
    print(f"\nRunning {path}...\n")
    try:
        interpreter.run()
    except (
        LakeOntarioInterpreterError,
        OSError,
        ValueError,
        TypeError,
        ZeroDivisionError,
        SyntaxError,
        NameError,
    ) as exc:
        print(f"\nIDE runtime error: {exc}")


def show_reference():
    print(load_command_reference())


def show_farcical_policy_help():
    print(FARCICAL_POLICY_HELP)


def main_menu():
    while True:
        clear_screen()
        print("Lake Ontario BASIC IDE")
        print("===================")
        print("1. List example programs")
        print("2. Edit or create a script")
        print("3. Run a script")
        print("4. View run history")
        print("5. View command reference")
        print("6. View farcical policy help")
        print("7. Exit")

        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            examples = list_examples()
            if not examples:
                print("No examples found.")
            else:
                print("\nExample programs:")
                for script in examples:
                    print(f"  - {script}")
            pause()
        elif choice == "2":
            path = choose_script()
            if path:
                edit_script(path)
            else:
                print("Invalid selection.")
                pause()
        elif choice == "3":
            path = choose_script()
            if path:
                run_script(path)
            else:
                print("Invalid selection.")
            pause()
        elif choice == "4":
            view_history()
            pause()
        elif choice == "5":
            show_reference()
            pause()
        elif choice == "6":
            show_farcical_policy_help()
            pause()
        elif choice == "7":
            print("Goodbye from the Lake Ontario BASIC IDE.")
            return
        else:
            print("Please choose a valid option.")
            pause()


def main():
    main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nIDE session ended.")
        sys.exit(0)
