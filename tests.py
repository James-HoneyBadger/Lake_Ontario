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


def run_string_operations_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK greeting = "  Hello, Comrade!  "
20 FACT_CHECK upper = STR_UPPER(greeting)
30 FACT_CHECK lower = STR_LOWER(greeting)
40 FACT_CHECK trimmed = STR_TRIM(greeting)
50 FACT_CHECK length = STR_LEN(trimmed)
60 FACT_CHECK has_hello = STR_CONTAINS(greeting, "Hello")
70 FACT_CHECK replaced = STR_REPLACE(greeting, "Hello", "Greetings")
80 FACT_CHECK parts = STR_SPLIT("one,two,three", ",")
90 FACT_CHECK num = TO_NUMBER("42")
100 FACT_CHECK text = TO_TEXT(99)
110 BROADCAST_CBC upper
120 BROADCAST_CBC lower
130 BROADCAST_CBC trimmed
140 BROADCAST_CBC length
150 BROADCAST_CBC has_hello
160 BROADCAST_CBC replaced
170 BROADCAST_CBC num
180 BROADCAST_CBC text
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL string-ops: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    result = output.getvalue()
    checks = [
        "HELLO, COMRADE!" in result,
        "hello, comrade!" in result,
        "Hello, Comrade!" in result,
        "15" in result,
        "True" in result,
        "Greetings" in result,
        "42" in result,
        "99" in result,
    ]
    if not all(checks):
        sys.stdout.write("FAIL string-ops: one or more string operations produced unexpected output\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS string-ops\n")
    sys.stdout.flush()
    return True


def run_loop_control_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK total = 0
20 COAST_TO_COAST i = 1 UP_TO 10
30 PERHAPS i == 5 FACT_ESTABLISHED
40 BREAK_FROM_CAUCUS
50 END_PERHAPS
60 FACT_CHECK total = total EQUAL_PAY i
70 THANK_YOU_EH
80 BROADCAST_CBC total
90 FACT_CHECK count = 0
100 COAST_TO_COAST j = 1 UP_TO 6
110 PERHAPS j == 3 FACT_ESTABLISHED
120 NEXT_MOTION
130 END_PERHAPS
140 FACT_CHECK count = count EQUAL_PAY 1
150 THANK_YOU_EH
160 BROADCAST_CBC count
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL loop-control: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    result = output.getvalue().splitlines()
    # break at 5 -> total = 1+2+3+4 = 10; skip j==3 -> count = 5 (1,2,4,5,6)
    if len(result) < 2 or result[0].strip() != "10" or result[1].strip() != "5":
        sys.stdout.write(
            f"FAIL loop-control: expected '10' and '5', got {result[:2]}\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS loop-control\n")
    sys.stdout.flush()
    return True


def run_repl_error_recovery_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--repl"],
        input=(
            'FACT_CHECK x = 10\n'
            'CLIMATE_EMERGENCY "deliberate crash"\n'
            'BROADCAST_CBC x\n'
            'IMPEACH\n'
        ),
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if "10" not in output:
        sys.stdout.write(
            "FAIL repl-error-recovery: REPL did not survive a runtime error\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS repl-error-recovery\n")
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
    all_passed = run_string_operations_test() and all_passed
    all_passed = run_loop_control_test() and all_passed
    all_passed = run_repl_error_recovery_test() and all_passed

    if all_passed:
        sys.stdout.write("\nAll tests passed.\n")
        sys.stdout.flush()
        sys.exit(0)
    else:
        sys.stdout.write("\nSome tests failed.\n")
        sys.stdout.flush()
        sys.exit(1)
