#!/usr/bin/env python3
"""Basic test harness for Lake Ontario BASIC interpreter."""

import os
import sys
from interpreter import LakeOntarioInterpreter

TEST_SCRIPTS = {
    "hello.lo": [
        "🍁 LAND ACKNOWLEDGEMENT",
        "Welcome to Lake Ontario BASIC, eh!",
        "Fact-based computing restored across the nation!",
    ],
    "honey_badger_mode.lo": [
        "🦡 HONEY BADGER MODE ENGAGED",
        "Honey Badger audit complete. Zero shit taken.",
    ],
    "farcical_policy.lo": [
        "🍁 LAND ACKNOWLEDGEMENT: Respectfully acknowledging traditional territory",
        "Sorry, eh? Sorry for your inconvenience, eh? — delivered with extra maple syrup",
        "🍁 MAKE IT RAIN: Redistributing $950000.00 to healthcare, transit, and doughnuts.",
        "🚊 Transit fare for 12.0 km: $7.25",
        "🧣 Toque warmth: Cozy enough for poutine and parliament protests.",
        "📏 Truth Meter: 100% sincerity",
        "❄️ Snow forecast: 250 flake-level protests expected when climate protest season.",
    ],
    "gui_demo.lo": [
        "🍁 LAND ACKNOWLEDGEMENT: Respectfully acknowledging traditional territory",
        "Lake Ontario BASIC GUI demo starting",
    ],
}


def run_test(script_name, expected_lines):
    path = os.path.join("examples", script_name)
    if not os.path.exists(path):
        sys.stdout.write(f"SKIP {script_name}: file not found\n")
        sys.stdout.flush()
        return False

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    interpreter = LakeOntarioInterpreter()
    if script_name == "gui_demo.lo":
        interpreter.set_input_callback(lambda var_name, prompt_type="town_hall": "GUI response")
    interpreter.load_script(code)
    try:
        from io import StringIO
        import contextlib

        output = StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.run()

        result = output.getvalue().splitlines()
        for expected in expected_lines:
            if not any(expected in line for line in result):
                sys.stdout.write(f"FAIL {script_name}: missing expected output '{expected}'\n")
                sys.stdout.flush()
                return False
        sys.stdout.write(f"PASS {script_name}\n")
        sys.stdout.flush()
        return True
    except SystemExit as exc:
        sys.stdout.write(f"FAIL {script_name}: interpreter exited with {exc.code}\n")
        sys.stdout.flush()
        return False
    except Exception as exc:
        sys.stdout.write(f"FAIL {script_name}: runtime error {exc}\n")
        sys.stdout.flush()
        return False


if __name__ == "__main__":
    all_passed = True
    sys.stdout.write("Starting Lake Ontario BASIC interpreter tests...\n")
    sys.stdout.flush()
    for script, expectations in TEST_SCRIPTS.items():
        passed = run_test(script, expectations)
        all_passed = all_passed and passed

    if all_passed:
        sys.stdout.write("\nAll tests passed.\n")
        sys.stdout.flush()
        sys.exit(0)
    else:
        sys.stdout.write("\nSome tests failed.\n")
        sys.stdout.flush()
        sys.exit(1)
