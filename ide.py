#!/usr/bin/env python3
"""
Lake Ontario BASIC IDE

A lightweight command-line IDE for editing, running, and exploring Lake Ontario BASIC scripts.
"""

import os
import re
import shutil
import subprocess
import sys
from interpreter import LakeOntarioInterpreter

EXAMPLES_DIR = "examples"

COMMAND_REFERENCE = """
Lake Ontario BASIC Command Reference

Statements:
  LAND_ACKNOWLEDGEMENT "territory"
  HONEY_BADGER_MODE
  HONEY_BADGER_DONT_CARE "target"
  BADGER_BITE expression
  FACT_CHECK name = expression
  BROADCAST_CBC expression
  TOWN_HALL variable_name
  PERHAPS condition FACT_ESTABLISHED
  STILL_IN_DENIAL
  END_PERHAPS
  WHILE_CLASS_CONSCIOUS condition
  CONTINUE_ORGANIZING
  COAST_TO_COAST var = start UP_TO end [STEP step]
  THANK_YOU_EH
  UNIVERSAL_HEALTHCARE
  EXECUTIVE_ORDER_BLOCKED
  SUBPOENA line_number
  RETURN_TO_OTTAWA
  GOLF_VACATION seconds
  CLIMATE_EMERGENCY message
  IMPEACH
  PUBLISH_RESEARCH_FILE path, content
  FAT_CATS_TAX amount
  DONUT_DIVIDEND amount
  NATIONAL_STOOGE statement
  GREEN_NEW_DEAL goal
  RHETORICAL_QUESTION question
  LOONIE_LOOP count
  SOCIAL_LICENSE license_name
  ELECTORATE_PULSE value
  NATIONAL_HEALTHCARE

Built-in functions:
  DEBUNK(text)
  FACT_CHECK_CROWD(value)
  TAX_THE_BILLIONAIRE(amount)
  DEFUND_OLIGARCHY(amount)
  LIVING_WAGE(hours, base_rate=25.0)
  UNIVERSAL_BASIC_INCOME(population, grant=2000.0)
  CARBON_OFFSET(emissions_tons)
  CELEBRATE_DIVERSITY(*items)
  UNIONIZE(*workers)
  SCIENCE_FACT(topic)
  PEER_REVIEWED_SQRT(value)
  SCIENCE_ROUND(value, decimals=2)
  READ_RESOURCE(path)
  PUBLISH_RESEARCH(path, content)
  FORMAT_CURRENCY(value)
  CAD_CURRENCY(value)
  HONEY_BADGER_DEBUNK(claim)
  HONEY_BADGER_BITE(target)
  HONEY_BADGER_STRIKE(action)
  SAY_SORRY(message)
  MAKE_IT_RAIN(amount)
  PUBLIC_TRANSIT_FARE(distance, base_fare=3.50)
  TOQUE_WARMTH(temp_celsius)
  TRUTH_METER(claim)
  MAKE_IT_SNOW(forecast, flakes=100)
  COLLECTIVE_LIST(...)
  MUTUAL_AID_REGISTRY(...)

Operators:
  WEALTH_TAX    -> -
  EQUAL_PAY     -> +
  PROPORTIONAL_SHARE -> /
  FAIR_MULTIPLIER -> *
  POWER_TO_THE_PEOPLE -> **
  MAPLE_SYRUP   -> %
  MOONSHOT      -> **

Literals:
  EVIDENCE_BASED        -> True
  ALTERNATIVE_FACT      -> False
  CLASSIFIED_MAR_A_LAGO -> None
"""

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
        subprocess.run(["cmd", "/c", "cls"])
    else:
        subprocess.run(["clear"])


def pause():
    input("\nPress Enter to return to the IDE menu...")


RUN_HISTORY = []


def list_examples():
    if not os.path.isdir(EXAMPLES_DIR):
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
    errors = []
    if not os.path.exists(path):
        return [f"Script not found: {path}"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
    except OSError as exc:
        return [f"Unable to read script: {exc}"]

    known_prefixes = (
        "LAND_ACKNOWLEDGEMENT", "HONEY_BADGER_MODE", "HONEY_BADGER_DONT_CARE",
        "BADGER_BITE", "FACT_CHECK", "BROADCAST_CBC", "TOWN_HALL",
        "PUBLISH_RESEARCH_FILE", "PERHAPS", "STILL_IN_DENIAL", "END_PERHAPS",
        "WHILE_CLASS_CONSCIOUS", "CONTINUE_ORGANIZING", "COAST_TO_COAST",
        "THANK_YOU_EH", "UNIVERSAL_HEALTHCARE", "EXECUTIVE_ORDER_BLOCKED",
        "SUBPOENA", "RETURN_TO_OTTAWA", "GOLF_VACATION",
        "CLIMATE_EMERGENCY", "IMPEACH",
    )

    for line_number, raw_line in enumerate(raw_lines, start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("EXCUSE_ME"):
            continue

        match = re.match(r"^(\d+)\s+(.*)$", stripped)
        stmt = match.group(2).strip() if match else stripped

        if not any(stmt.startswith(prefix) for prefix in known_prefixes):
            if stmt not in ("STILL_IN_DENIAL", "END_PERHAPS"):
                head = stmt.split()[0] if stmt.split() else stmt
                errors.append(f"Line {line_number}: unsupported statement '{head}'")
                continue

        if stmt.startswith("FACT_CHECK") and "=" not in stmt:
            errors.append(f"Line {line_number}: FACT_CHECK statement must include '='")
        elif stmt.startswith("COAST_TO_COAST") and " UP_TO " not in stmt:
            errors.append(f"Line {line_number}: COAST_TO_COAST statement must include 'UP_TO'")
        elif stmt.startswith("PUBLISH_RESEARCH_FILE") and "," not in stmt:
            errors.append(f"Line {line_number}: PUBLISH_RESEARCH_FILE must separate path and content with a comma")
        elif stmt.startswith("SUBPOENA"):
            target_text = stmt[9:].strip()
            if not target_text.isdigit():
                errors.append(f"Line {line_number}: SUBPOENA must target a numbered line")
        elif stmt.startswith("GOLF_VACATION"):
            value = stmt[14:].strip()
            try:
                float(value)
            except ValueError:
                errors.append(f"Line {line_number}: GOLF_VACATION requires a numeric value")
        elif stmt.startswith("CLIMATE_EMERGENCY"):
            if not stmt[18:].strip():
                errors.append(f"Line {line_number}: CLIMATE_EMERGENCY requires a message")
        elif stmt.startswith("TOWN_HALL") and not stmt[10:].strip():
            errors.append(f"Line {line_number}: TOWN_HALL requires a variable name")

    return errors


def choose_script():
    examples = list_examples()
    print("\nAvailable examples:")
    for idx, name in enumerate(examples, 1):
        print(f"  {idx}. {name}")
    print("  0. Enter a custom script path")

    choice = input("Select a script number or path: ").strip()
    if choice == "0":
        custom = input("Enter script file path: ").strip()
        return os.path.abspath(custom)
    if choice.isdigit() and 1 <= int(choice) <= len(examples):
        return os.path.abspath(os.path.join(EXAMPLES_DIR, examples[int(choice) - 1]))
    return None


def edit_script(path):
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("10 EXCUSE_ME Lake Ontario BASIC script created by the IDE\n")
            f.write("20 LAND_ACKNOWLEDGEMENT \"Traditional Territory\"\n")
            f.write("30 FACT_CHECK greeting = \"Hello from Lake Ontario BASIC!\"\n")
            f.write("40 BROADCAST_CBC greeting\n")

    editor = os.environ.get("EDITOR")
    if not editor:
        editor = shutil.which("nano") or shutil.which("vi") or shutil.which("code")
    if not editor:
        print("No editor detected. Please set the EDITOR environment variable.")
        return

    try:
        subprocess.run([editor, path])
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
    except Exception as exc:
        print(f"\nIDE runtime error: {exc}")


def show_reference():
    print(COMMAND_REFERENCE)


def main_menu():
    while True:
        clear_screen()
        print("Lake Ontario BASIC IDE")
        print("=====================")
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
            print(FARCICAL_POLICY_HELP)
            pause()
        elif choice == "7":
            print("Goodbye from the Lake Ontario BASIC IDE.")
            return
        else:
            print("Please choose a valid option.")
            pause()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nIDE session ended.")
        sys.exit(0)
