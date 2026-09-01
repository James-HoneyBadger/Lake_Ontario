#!/usr/bin/env python3
"""Basic test harness for Lake Ontario BASIC interpreter."""

import contextlib
import os
import sys
from io import StringIO

from interpreter import LakeOntarioInterpreter, LakeOntarioInterpreterError

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
        (
            "Sorry, eh? Sorry for your inconvenience, eh? — delivered with extra "
            "maple syrup"
        ),
        (
            "🍁 MAKE IT RAIN: Redistributing $950000.00 to healthcare, "
            "transit, and doughnuts."
        ),
        "🚊 Transit fare for 12.0 km: $7.25",
        "🧣 Toque warmth: Cozy enough for poutine and parliament protests.",
        "📏 Truth Meter: 100% sincerity",
        (
            "❄️ Snow forecast: 250 flake-level protests expected when "
            "climate protest season."
        ),
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
        interpreter.set_input_callback(
            lambda var_name, prompt_type="town_hall": "GUI response"
        )
    interpreter.load_script(code)
    try:
        output = StringIO()
        with contextlib.redirect_stdout(output):
            interpreter.run()

        result = output.getvalue().splitlines()
        for expected in expected_lines:
            if not any(expected in line for line in result):
                sys.stdout.write(
                    f"FAIL {script_name}: missing expected output '{expected}'\n"
                )
                sys.stdout.flush()
                return False
        sys.stdout.write(f"PASS {script_name}\n")
        sys.stdout.flush()
        return True
    except SystemExit as exc:
        sys.stdout.write(f"FAIL {script_name}: interpreter exited with {exc.code}\n")
        sys.stdout.flush()
        return False
    except (
        LakeOntarioInterpreterError,
        OSError,
        ValueError,
        TypeError,
        ZeroDivisionError,
        SyntaxError,
        NameError,
    ) as exc:
        sys.stdout.write(f"FAIL {script_name}: runtime error {exc}\n")
        sys.stdout.flush()
        return False


def run_repl_smoke_test():
    import subprocess

    cmd = [sys.executable, "interpreter.py", "--repl"]
    proc = subprocess.run(
        cmd,
        input="BROADCAST_CBC \"Hello from REPL!\"\nIMPEACH\n",
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout.lower()
    if proc.returncode != 0 or "lake ontario basic repl" not in output:
        sys.stdout.write("FAIL repl: missing REPL banner or unexpected exit\n")
        sys.stdout.flush()
        return False
    if "hello from repl!" not in output:
        sys.stdout.write("FAIL repl: script output was not executed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS repl\n")
    sys.stdout.flush()
    return True


def run_default_invocation_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py"],
        input="BROADCAST_CBC \"Hello from default REPL!\"\nIMPEACH\n",
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout.lower()
    if proc.returncode != 0 or "lake ontario basic repl" not in output:
        sys.stdout.write("FAIL default-repl: missing REPL banner or unexpected exit\n")
        sys.stdout.flush()
        return False
    if "hello from default repl!" not in output:
        sys.stdout.write("FAIL default-repl: default launch did not run REPL input\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS default-repl\n")
    sys.stdout.flush()
    return True


def run_cli_help_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--help"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout.lower()
    if proc.returncode != 0 or "usage:" not in output:
        sys.stdout.write("FAIL cli-help: missing usage output\n")
        sys.stdout.flush()
        return False
    if "--repl" not in output:
        sys.stdout.write("FAIL cli-help: REPL mode missing from help text\n")
        sys.stdout.flush()
        return False
    if "--version" not in output or "--list-examples" not in output or "--run-example" not in output:
        sys.stdout.write("FAIL cli-help: version, listing, and example-run options missing\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS cli-help\n")
    sys.stdout.flush()
    return True


def run_environment_doctor_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--doctor"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode != 0 or "environment ok" not in output.lower():
        sys.stdout.write("FAIL doctor: environment check missing or failed\n")
        sys.stdout.flush()
        return False
    if "python" not in output.lower() or "tkinter" not in output.lower():
        sys.stdout.write("FAIL doctor: summary did not include required environment details\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS doctor\n")
    sys.stdout.flush()
    return True


def run_expanded_commands_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK total = 10
20 FACT_CHECK roster = COLLECTIVE_LIST "A", "B"
30 APPEND_TO roster, "C"
40 SHOW_VARS
50 RESET_CITIZENS
60 BROADCAST_CBC "memory reset"
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL expanded-commands: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    result = output.getvalue()
    if "total" not in result or "roster" not in result or "memory reset" not in result:
        sys.stdout.write("FAIL expanded-commands: new command set did not execute as expected\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS expanded-commands\n")
    sys.stdout.flush()
    return True


def run_civic_data_commands_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK residents = COLLECTIVE_LIST 6, 2, 4
20 SORT_CITIZENS residents
30 AVERAGE_CITIZENS residents
40 BROADCAST_CBC "civic data complete"
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL civic-data: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    result = output.getvalue()
    if "civic data complete" not in result or "4.0" not in result:
        sys.stdout.write("FAIL civic-data: sorting or average command did not run as expected\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS civic-data\n")
    sys.stdout.flush()
    return True


def run_validation_and_diagnostics_test():
    import subprocess

    script_path = os.path.join("examples", "tmp_validation_check.lo")
    with open(script_path, "w", encoding="utf-8") as file:
        file.write('10 CLIMATE_EMERGENCY "oh no"\n')

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", script_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    if proc.returncode != 0:
        sys.stdout.write("FAIL validation: --check should succeed for valid syntax\n")
        sys.stdout.flush()
        return False

    invalid_path = os.path.join("examples", "tmp_invalid_check.lo")
    with open(invalid_path, "w", encoding="utf-8") as file:
        file.write('10 FACT_CHECK total = \n')

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", invalid_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode == 0 or "Line 10" not in output:
        sys.stdout.write("FAIL validation: invalid script should report a line number\n")
        sys.stdout.flush()
        return False

    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "from interpreter import LakeOntarioInterpreter; "
            "i = LakeOntarioInterpreter(); "
            "i.load_script('10 CLIMATE_EMERGENCY \"oh no\"\\n'); "
            "i.run()",
        ],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode == 0 or "Line 10" not in output:
        sys.stdout.write("FAIL diagnostics: runtime errors missing source line numbers\n")
        sys.stdout.flush()
        return False

    os.remove(script_path)
    os.remove(invalid_path)
    sys.stdout.write("PASS validation-diagnostics\n")
    sys.stdout.flush()
    return True


if __name__ == "__main__":
    all_passed = True
    sys.stdout.write("Starting Lake Ontario BASIC interpreter tests...\n")
    sys.stdout.flush()
    for script, expectations in TEST_SCRIPTS.items():
        passed = run_test(script, expectations)
        all_passed = all_passed and passed

    all_passed = run_repl_smoke_test() and all_passed
    all_passed = run_default_invocation_test() and all_passed
    all_passed = run_cli_help_test() and all_passed
    all_passed = run_environment_doctor_test() and all_passed
    all_passed = run_expanded_commands_test() and all_passed
    all_passed = run_civic_data_commands_test() and all_passed
    all_passed = run_validation_and_diagnostics_test() and all_passed

    if all_passed:
        sys.stdout.write("\nAll tests passed.\n")
        sys.stdout.flush()
        sys.exit(0)
    else:
        sys.stdout.write("\nSome tests failed.\n")
        sys.stdout.flush()
        sys.exit(1)
