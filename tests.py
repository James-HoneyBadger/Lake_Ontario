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
    "civic_caucus.lo": [
        "CITIZEN PETITION: A public library in every neighbourhood",
        "87.0% agreement",
        "CIVIC COMPROMISE",
        "Library Funding",
        "MOTION PASSED",
    ],
    "graphics_and_sound_showcase.lo": [
        "Rally Visualizer: Graphics & Sound Showcase",
        "MOTION PASSED with 87.5% support!",
        "Playing sound file: cheers.wav",
        "Showcase complete. Thanks for coming out, eh!",
        "IMPEACHMENT EFFECTIVE",
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
        input='BROADCAST_CBC "Hello from REPL!"\nIMPEACH\n',
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
        input='BROADCAST_CBC "Hello from default REPL!"\nIMPEACH\n',
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
    if (
        "--version" not in output
        or "--list-examples" not in output
        or "--run-example" not in output
    ):
        sys.stdout.write(
            "FAIL cli-help: version, listing, and example-run options missing\n"
        )
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
        sys.stdout.write(
            "FAIL doctor: summary did not include required environment details\n"
        )
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
        sys.stdout.write(
            "FAIL expanded-commands: new command set did not execute as expected\n"
        )
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
        sys.stdout.write(
            "FAIL civic-data: sorting or average command did not run as expected\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS civic-data\n")
    sys.stdout.flush()
    return True


def run_graphics_and_sound_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 SET_PEN_WIDTH 3
20 DRAW_POINT 5, 5
30 DRAW_OVAL 0, 0, 10, 10
40 FILL_OVAL 0, 0, 10, 10
50 DRAW_ARC 5, 5, 5, 0, 90
60 DRAW_POLYGON 0, 0, 10, 0, 10, 10, 0, 10
70 FILL_POLYGON 0, 0, 10, 0, 10, 10, 0, 10
80 DRAW_TRIANGLE 0, 0, 10, 0, 5, 10
90 FILL_TRIANGLE 0, 0, 10, 0, 5, 10
100 PLAY_TONE 440, 20
110 HONEY_BADGER_GROWL
120 TOWN_HALL_BELL
130 STANDING_OVATION
140 PLAY_SOUND_FILE "cheers.wav"
150 STOP_SOUND
160 BROADCAST_CBC "graphics and sound complete"
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except (LakeOntarioInterpreterError, SystemExit) as exc:
        sys.stdout.write(f"FAIL graphics-and-sound: unexpected error {exc}\n")
        sys.stdout.flush()
        return False

    result = output.getvalue()
    expected_snippets = [
        "GRRRR! The Honey Badger growls",
        "Order! Order! The Town Hall bell",
        "The gallery rises for a standing ovation",
        "Playing sound file: cheers.wav",
        "graphics and sound complete",
    ]
    for snippet in expected_snippets:
        if snippet not in result:
            sys.stdout.write(
                f"FAIL graphics-and-sound: missing expected output '{snippet}'\n"
            )
            sys.stdout.flush()
            return False

    sys.stdout.write("PASS graphics-and-sound\n")
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
        file.write("10 FACT_CHECK total = \n")

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", invalid_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode == 0 or "Line 10" not in output:
        sys.stdout.write(
            "FAIL validation: invalid script should report a line number\n"
        )
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
        sys.stdout.write(
            "FAIL diagnostics: runtime errors missing source line numbers\n"
        )
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
        sys.stdout.write(
            "FAIL string-ops: one or more string operations produced unexpected output\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS string-ops\n")
    sys.stdout.flush()
    return True


def run_farcical_civic_expansion_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 HEAR_HEAR "Fund the public library"
20 CITIZEN_PETITION "More donuts at town hall"
30 MOTION_PASSED
40 FACT_CHECK gazette = PARLIAMENT_GAZETTE("Library Funding", "Approved with snacks")
50 FACT_CHECK poll = POLL_THE_PEOPLE("Do we need more libraries?", 125)
60 FACT_CHECK compromise = CIVIC_COMPROMISE("Buses", "Bicycles")
70 BROADCAST_CBC gazette
80 BROADCAST_CBC poll
90 BROADCAST_CBC compromise
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = [
        "HEAR, HEAR",
        "CITIZEN PETITION",
        "MOTION PASSED",
        "Library Funding",
        "100.0% agreement",
        "Buses",
    ]
    if not all(item in result for item in expected):
        sys.stdout.write(
            "FAIL civic-expansion: new civic commands produced bad output\n"
        )
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS civic-expansion\n")
    sys.stdout.flush()
    return True


def run_policy_standard_library_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK election = RIGGED_ELECTION_METER("The election was stolen")
20 FACT_CHECK access = VOTER_SUPPRESSION_ALERT("Short polling hours")
30 FACT_CHECK fine = CORPORATE_FINE("Maple Megacorp", "Wage theft", -500)
40 FACT_CHECK safety = WORKPLACE_SAFETY_AUDIT("The donut factory")
50 FACT_CHECK land = INDIGENOUS_LAND_RETURN("Credit River", "Mississaugas of the Credit")
60 FACT_CHECK energy = RENEWABLE_ENERGY_TARGET(125, 2040)
70 BROADCAST_CBC election
80 BROADCAST_CBC access
90 BROADCAST_CBC fine
100 BROADCAST_CBC safety
110 BROADCAST_CBC land
120 BROADCAST_CBC energy
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = [
        "0% credibility",
        "VOTER SUPPRESSION ALERT",
        "$0.00",
        "WORKPLACE SAFETY AUDIT",
        "consultation, consent",
        "100.0% clean energy by 2040",
    ]
    if not all(item in result for item in expected):
        sys.stdout.write("FAIL policy-library: standard policy functions failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS policy-library\n")
    sys.stdout.flush()
    return True


def run_worker_services_library_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK wages = WAGE_THEFT_RECOVERY(-10)
20 FACT_CHECK homes = AFFORDABLE_HOUSING_BUILT(250, "Hamilton")
30 FACT_CHECK access = ACCESSIBILITY_AUDIT("City Hall")
40 FACT_CHECK accommodation = ACCOMMODATION_APPROVED("Captioned town hall")
50 FACT_CHECK wait = PUBLIC_SERVICE_WAIT("Transit help desk", -3)
60 FACT_CHECK climate = EMISSIONS_REDUCED(100, 25)
70 BROADCAST_CBC wages
80 BROADCAST_CBC homes
90 BROADCAST_CBC access
100 BROADCAST_CBC accommodation
110 BROADCAST_CBC wait
120 BROADCAST_CBC climate
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = [
        "$0.00 returned to workers",
        "250 homes announced for Hamilton",
        "step-free access",
        "Captioned town hall is approved",
        "0.0 minutes",
        "75.0% reduction",
    ]
    if not all(item in result for item in expected):
        sys.stdout.write("FAIL worker-services: service functions failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS worker-services\n")
    sys.stdout.flush()
    return True


def run_climate_care_library_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK risk = CLIMATE_RISK_SCORE("Lake Ontario", 125)
20 FACT_CHECK science = SCIENCE_CONSENSUS("climate")
30 FACT_CHECK treaty = TREATY_OBLIGATION_TRACKER("Treaty 3")
40 FACT_CHECK consultation = INDIGENOUS_CONSULTATION_REQUIRED("New rail line")
50 FACT_CHECK care = COMMUNITY_CARE_PLAN("Heat wave", "cooling centres and transit")
60 BROADCAST_CBC risk
70 BROADCAST_CBC science
80 BROADCAST_CBC treaty
90 BROADCAST_CBC consultation
100 BROADCAST_CBC care
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = [
        "100.0/100",
        "Human-caused climate change is real",
        "Treaty 3 requires ongoing review",
        "meaningful consultation and consent",
        "cooling centres and transit",
    ]
    if not all(item in result for item in expected):
        sys.stdout.write("FAIL climate-care: climate and care functions failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS climate-care\n")
    sys.stdout.flush()
    return True


def run_citizen_data_library_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK values = COLLECTIVE_LIST(10, 30, 20, 40)
20 FACT_CHECK median = MEDIAN_CITIZENS(values)
30 FACT_CHECK total = CITIZEN_SUM(values)
40 FACT_CHECK has_votes = CITIZEN_ANY(COLLECTIVE_LIST(False, True))
50 FACT_CHECK all_votes = CITIZEN_ALL(COLLECTIVE_LIST(True, True))
60 FACT_CHECK evidence = EVIDENCE_SCORE("A bold claim", values)
70 BROADCAST_CBC median
80 BROADCAST_CBC total
90 BROADCAST_CBC has_votes
100 BROADCAST_CBC all_votes
110 BROADCAST_CBC evidence
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = ["25.0", "100.0", "True", "100/100", "committee requests sources"]
    if not all(item in result for item in expected):
        sys.stdout.write("FAIL citizen-data: collection functions failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS citizen-data\n")
    sys.stdout.flush()
    return True


def run_registry_policy_library_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK budget = MUTUAL_AID_REGISTRY(housing=250, transit=80)
20 FACT_CHECK missing = REGISTRY_GET(budget, "healthcare", "committee review")
30 FACT_CHECK keys = REGISTRY_KEYS(budget)
40 FACT_CHECK values = REGISTRY_VALUES(budget)
50 FACT_CHECK score = POLICY_SCORE("People First", keys)
60 BROADCAST_CBC missing
70 BROADCAST_CBC keys
80 BROADCAST_CBC values
90 BROADCAST_CBC score
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = [
        "committee review",
        "housing",
        "transit",
        "250",
        "80",
        "40/100",
    ]
    if not all(item in result for item in expected):
        sys.stdout.write("FAIL registry-policy: registry functions failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS registry-policy\n")
    sys.stdout.flush()
    return True


def run_grouped_citizen_data_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK names = COLLECTIVE_LIST("Asha", "Ben", "Asha", "Diego")
20 FACT_CHECK regions = COLLECTIVE_LIST("North", "South", "North", "West")
30 FACT_CHECK grouped = GROUP_BY_CITIZENS(names, regions)
40 FACT_CHECK asha_count = COUNT_BY_CITIZENS(names, "Asha")
50 FACT_CHECK missing_count = COUNT_BY_CITIZENS(names, "Zed")
60 BROADCAST_CBC grouped
70 BROADCAST_CBC asha_count
80 BROADCAST_CBC missing_count
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = ["North", "Asha", "South", "West", "2", "0"]
    if not all(item in result for item in expected):
        sys.stdout.write("FAIL grouped-data: grouping functions failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS grouped-data\n")
    sys.stdout.flush()
    return True


def run_civic_records_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 VOTE_RECORDED "Asha", "Municipal Transit", "Buses"
20 PETITION_SIGNATURE_COLLECTED "Ben", "More libraries"
30 TESTIMONY_ADDED "Diego", "The ramp needs repair"
40 BROADCAST_CBC "records filed"
""".strip()
    interpreter.load_script(script)
    output = StringIO()
    with contextlib.redirect_stdout(output):
        interpreter.run()
    result = output.getvalue()
    expected = [
        "VOTE RECORDED",
        "PETITION SIGNATURE",
        "TESTIMONY ADDED",
        "records filed",
    ]
    if (
        not all(item in result for item in expected)
        or len(interpreter.vote_records) != 1
        or len(interpreter.petition_signatures) != 1
        or len(interpreter.testimonies) != 1
    ):
        sys.stdout.write("FAIL civic-records: civic record statements failed\n")
        sys.stdout.flush()
        return False
    sys.stdout.write("PASS civic-records\n")
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
            "FACT_CHECK x = 10\n"
            'CLIMATE_EMERGENCY "deliberate crash"\n'
            "BROADCAST_CBC x\n"
            "IMPEACH\n"
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


def run_for_each_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK total = 0
20 FACT_CHECK nums = COLLECTIVE_LIST 10, 20, 30
30 FOR_EACH n IN nums
40 FACT_CHECK total = total EQUAL_PAY n
50 END_EACH
60 BROADCAST_CBC total
70 FACT_CHECK items = COLLECTIVE_LIST "a", "b", "c"
80 FACT_CHECK joined = JOIN_COLLECTIVE(items, "-")
90 BROADCAST_CBC joined
100 FACT_CHECK first = FIRST_CITIZEN(nums)
110 FACT_CHECK last = LAST_CITIZEN(nums)
120 FACT_CHECK mid = CITIZEN_AT(nums, 1)
130 BROADCAST_CBC first
140 BROADCAST_CBC last
150 BROADCAST_CBC mid
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL for-each: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    result = output.getvalue()
    checks = [
        "60" in result,
        "a-b-c" in result,
        "10" in result,
        "30" in result,
        "20" in result,
    ]
    if not all(checks):
        sys.stdout.write(f"FAIL for-each: unexpected output:\n{result}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS for-each\n")
    sys.stdout.flush()
    return True


def run_perhaps_also_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK score = 75
20 PERHAPS score >= 90 FACT_ESTABLISHED
30 BROADCAST_CBC "A"
40 PERHAPS_ALSO score >= 75 FACT_ESTABLISHED
50 BROADCAST_CBC "B"
60 PERHAPS_ALSO score >= 60 FACT_ESTABLISHED
70 BROADCAST_CBC "C"
80 STILL_IN_DENIAL
90 BROADCAST_CBC "F"
100 END_PERHAPS
110 FACT_CHECK score2 = 40
120 PERHAPS score2 >= 90 FACT_ESTABLISHED
130 BROADCAST_CBC "A2"
140 PERHAPS_ALSO score2 >= 60 FACT_ESTABLISHED
150 BROADCAST_CBC "C2"
160 STILL_IN_DENIAL
170 BROADCAST_CBC "F2"
180 END_PERHAPS
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL perhaps-also: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    result = output.getvalue().splitlines()
    if result != ["B", "F2"]:
        sys.stdout.write(f"FAIL perhaps-also: expected ['B', 'F2'], got {result}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS perhaps-also\n")
    sys.stdout.flush()
    return True


def run_math_and_random_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK a = MATH_ABS(-42)
20 FACT_CHECK b = MATH_FLOOR(3.9)
30 FACT_CHECK c = MATH_CEIL(3.1)
40 FACT_CHECK d = MATH_MIN(10, 3, 7)
50 FACT_CHECK e = MATH_MAX(10, 3, 7)
60 FACT_CHECK r = RANDOM_DEMOCRACY(1, 100)
70 BROADCAST_CBC a
80 BROADCAST_CBC b
90 BROADCAST_CBC c
100 BROADCAST_CBC d
110 BROADCAST_CBC e
120 BROADCAST_CBC r
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL math-random: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    lines = output.getvalue().splitlines()
    try:
        checks = (
            float(lines[0]) == 42.0
            and int(lines[1]) == 3
            and int(lines[2]) == 4
            and float(lines[3]) == 3.0
            and float(lines[4]) == 10.0
            and 1 <= int(lines[5]) <= 100
        )
    except (ValueError, IndexError):
        checks = False

    if not checks:
        sys.stdout.write(f"FAIL math-random: unexpected output: {lines}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS math-random\n")
    sys.stdout.flush()
    return True


def run_list_ops_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK lst = COLLECTIVE_LIST 3, 1, 4, 1, 5
20 REMOVE_FROM lst, 1
30 BROADCAST_CBC CITIZEN_COUNT(lst)
40 SORT_CITIZENS lst
50 BROADCAST_CBC FIRST_CITIZEN(lst)
60 BROADCAST_CBC LAST_CITIZEN(lst)
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL list-ops: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    lines = output.getvalue().splitlines()
    # remove first 1 → [3, 4, 1, 5], count=4; sorted → [1, 3, 4, 5]
    # line 1 is the SORT_CITIZENS print message; first/last are lines 2 and 3
    try:
        ok = int(lines[0]) == 4 and float(lines[2]) == 1.0 and float(lines[3]) == 5.0
    except (ValueError, IndexError):
        ok = False

    if not ok:
        sys.stdout.write(f"FAIL list-ops: unexpected output: {lines}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS list-ops\n")
    sys.stdout.flush()
    return True


def run_while_loop_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK n = 1
20 FACT_CHECK total = 0
30 WHILE_CLASS_CONSCIOUS n <= 5
40 FACT_CHECK total = total EQUAL_PAY n
50 FACT_CHECK n = n EQUAL_PAY 1
60 CONTINUE_ORGANIZING
70 BROADCAST_CBC total
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL while-loop: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    lines = output.getvalue().splitlines()
    if not lines or lines[-1].strip() != "15":
        sys.stdout.write(f"FAIL while-loop: expected total 15, got {lines}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS while-loop\n")
    sys.stdout.flush()
    return True


def run_for_step_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK total = 0
20 COAST_TO_COAST i = 2 UP_TO 10 STEP 2
30 FACT_CHECK total = total EQUAL_PAY i
40 THANK_YOU_EH
50 BROADCAST_CBC total
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL for-step: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    lines = output.getvalue().splitlines()
    if not lines or lines[-1].strip() != "30":
        sys.stdout.write(f"FAIL for-step: expected total 30, got {lines}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS for-step\n")
    sys.stdout.flush()
    return True


def run_subroutine_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 FACT_CHECK x = 7
20 SUBPOENA 100
30 BROADCAST_CBC x
40 IMPEACH
100 FACT_CHECK x = x FAIR_MULTIPLIER 6
110 RETURN_TO_OTTAWA
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL subroutine: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    lines = output.getvalue().splitlines()
    if not lines or lines[0].strip() != "42":
        sys.stdout.write(f"FAIL subroutine: expected 42, got {lines}\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS subroutine\n")
    sys.stdout.flush()
    return True


def run_healthcare_guard_test():
    interpreter = LakeOntarioInterpreter()
    script = """
10 UNIVERSAL_HEALTHCARE
20 BROADCAST_CBC "before"
30 CLIMATE_EMERGENCY "boom"
40 EXECUTIVE_ORDER_BLOCKED
50 BROADCAST_CBC "after"
""".strip()

    interpreter.load_script(script)
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output):
            interpreter.run()
    except SystemExit:
        sys.stdout.write("FAIL healthcare-guard: interpreter exited unexpectedly\n")
        sys.stdout.flush()
        return False

    text = output.getvalue()
    if "before" not in text or "after" not in text:
        sys.stdout.write(
            f"FAIL healthcare-guard: expected before/after output, got {text}\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS healthcare-guard\n")
    sys.stdout.flush()
    return True


def run_repl_multiline_block_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--repl"],
        input=(
            "PERHAPS EVIDENCE_BASED FACT_ESTABLISHED\n"
            'BROADCAST_CBC "multiline block works"\n'
            "END_PERHAPS\n"
            "IMPEACH\n"
        ),
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode != 0 or "multiline block works" not in output:
        sys.stdout.write("FAIL repl-multiline: block input did not execute\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS repl-multiline\n")
    sys.stdout.flush()
    return True


def run_validation_strictness_test():
    import subprocess

    duplicate_path = os.path.join("examples", "tmp_duplicate_lines.lo")
    with open(duplicate_path, "w", encoding="utf-8") as file:
        file.write('10 BROADCAST_CBC "a"\n10 BROADCAST_CBC "b"\n')

    unknown_path = os.path.join("examples", "tmp_unknown_statement.lo")
    with open(unknown_path, "w", encoding="utf-8") as file:
        file.write("10 HOCKEY_STICK 7\n")

    duplicate_proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", duplicate_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    duplicate_output = duplicate_proc.stdout + duplicate_proc.stderr

    unknown_proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", unknown_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    unknown_output = unknown_proc.stdout + unknown_proc.stderr

    os.remove(duplicate_path)
    os.remove(unknown_path)

    if (
        duplicate_proc.returncode == 0
        or "duplicate line number" not in duplicate_output
    ):
        sys.stdout.write(
            "FAIL validation-strict: duplicate line numbers were not rejected\n"
        )
        sys.stdout.flush()
        return False

    if unknown_proc.returncode == 0 or "unsupported statement" not in unknown_output:
        sys.stdout.write("FAIL validation-strict: unknown statement was not rejected\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS validation-strict\n")
    sys.stdout.flush()
    return True


def run_missing_file_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", "examples/does_not_exist.lo"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode == 0 or "not found" not in output.lower():
        sys.stdout.write(
            "FAIL missing-file: CLI did not fail cleanly for a missing script\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS missing-file\n")
    sys.stdout.flush()
    return True


def run_malformed_list_command_test():
    import subprocess

    bad_path = os.path.join("examples", "tmp_bad_list_command.lo")
    with open(bad_path, "w", encoding="utf-8") as file:
        file.write("10 APPEND_TO roster\n")

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", bad_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    os.remove(bad_path)

    if proc.returncode == 0 or "APPEND_TO" not in output.upper():
        sys.stdout.write(
            "FAIL malformed-list: malformed APPEND_TO command was not rejected\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS malformed-list\n")
    sys.stdout.flush()
    return True


def run_repl_help_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--repl"],
        input="HELP\nIMPEACH\n",
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout.lower()
    if proc.returncode != 0 or "help" not in output or "impeach" not in output:
        sys.stdout.write(
            "FAIL repl-help: help command did not print a useful REPL guide\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS repl-help\n")
    sys.stdout.flush()
    return True


def run_repl_history_reset_test():
    import subprocess

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--repl"],
        input=(
            "FACT_CHECK x = 7\n"
            "SHOW_VARS\n"
            "HISTORY\n"
            "REPLAY 1\n"
            "RESET\n"
            "SHOW_VARS\n"
            "IMPEACH\n"
        ),
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout.lower()
    if proc.returncode != 0:
        sys.stdout.write("FAIL repl-history-reset: REPL exited unexpectedly\n")
        sys.stdout.flush()
        return False
    if "x = 7" not in output or "history" not in output or "state reset" not in output:
        sys.stdout.write(
            "FAIL repl-history-reset: reset/history workflow did not work\n"
        )
        sys.stdout.flush()
        return False
    if "citizen register: empty" not in output:
        sys.stdout.write("FAIL repl-history-reset: REPL reset did not clear state\n")
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS repl-history-reset\n")
    sys.stdout.flush()
    return True


def run_repl_persistence_clear_test():
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        history_path = os.path.join(tmpdir, ".lake_ontario_history")
        env = os.environ.copy()
        env["LAKE_ONTARIO_REPL_HISTORY"] = history_path

        proc1 = subprocess.run(
            [sys.executable, "interpreter.py", "--repl"],
            input="FACT_CHECK x = 7\nIMPEACH\n",
            text=True,
            capture_output=True,
            timeout=20,
            env=env,
        )
        if proc1.returncode != 0:
            sys.stdout.write(
                "FAIL repl-persistence: first REPL session did not exit cleanly\n"
            )
            sys.stdout.flush()
            return False

        with open(history_path, "r", encoding="utf-8") as handle:
            saved = handle.read()
        if "FACT_CHECK x = 7" not in saved:
            sys.stdout.write(
                "FAIL repl-persistence: REPL history was not saved to disk\n"
            )
            sys.stdout.flush()
            return False

        proc2 = subprocess.run(
            [sys.executable, "interpreter.py", "--repl"],
            input="CLEAR\nHISTORY\nIMPEACH\n",
            text=True,
            capture_output=True,
            timeout=20,
            env=env,
        )
        output = proc2.stdout.lower()
        if proc2.returncode != 0:
            sys.stdout.write(
                "FAIL repl-persistence: second REPL session did not exit cleanly\n"
            )
            sys.stdout.flush()
            return False
        if "repl history is empty" not in output or "history cleared" not in output:
            sys.stdout.write(
                "FAIL repl-persistence: CLEAR did not reset history state\n"
            )
            sys.stdout.flush()
            return False

    sys.stdout.write("PASS repl-persistence\n")
    sys.stdout.flush()
    return True


def run_validation_suggestion_test():
    import subprocess

    bad_path = os.path.join("examples", "tmp_validation_suggestion.lo")
    with open(bad_path, "w", encoding="utf-8") as file:
        file.write('10 PERHAPS EVIDENCE_BASED\n20 BROADCAST_CBC "still here"\n')

    proc = subprocess.run(
        [sys.executable, "interpreter.py", "--check", bad_path],
        text=True,
        capture_output=True,
        timeout=20,
    )
    output = proc.stdout + proc.stderr
    os.remove(bad_path)

    if proc.returncode == 0 or "FACT_ESTABLISHED" not in output:
        sys.stdout.write(
            "FAIL validation-suggestion: PERHAPS validation did not suggest the required FACT_ESTABLISHED keyword\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS validation-suggestion\n")
    sys.stdout.flush()
    return True


def run_packaging_guard_test():
    import importlib.util

    spec = importlib.util.spec_from_file_location("run_ide_probe", "run_ide.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)

    if not hasattr(module, "_python_can_import_package"):
        sys.stdout.write(
            "FAIL packaging-guard: launcher missing package-availability check\n"
        )
        sys.stdout.flush()
        return False

    result = module._python_can_import_package(sys.executable)
    if not result:
        sys.stdout.write(
            "FAIL packaging-guard: project package is not importable in the active runtime\n"
        )
        sys.stdout.flush()
        return False

    sys.stdout.write("PASS packaging-guard\n")
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
    all_passed = run_graphics_and_sound_test() and all_passed
    all_passed = run_validation_and_diagnostics_test() and all_passed
    all_passed = run_string_operations_test() and all_passed
    all_passed = run_farcical_civic_expansion_test() and all_passed
    all_passed = run_policy_standard_library_test() and all_passed
    all_passed = run_worker_services_library_test() and all_passed
    all_passed = run_climate_care_library_test() and all_passed
    all_passed = run_citizen_data_library_test() and all_passed
    all_passed = run_registry_policy_library_test() and all_passed
    all_passed = run_grouped_citizen_data_test() and all_passed
    all_passed = run_civic_records_test() and all_passed
    all_passed = run_loop_control_test() and all_passed
    all_passed = run_repl_error_recovery_test() and all_passed
    all_passed = run_for_each_test() and all_passed
    all_passed = run_perhaps_also_test() and all_passed
    all_passed = run_math_and_random_test() and all_passed
    all_passed = run_list_ops_test() and all_passed
    all_passed = run_while_loop_test() and all_passed
    all_passed = run_for_step_test() and all_passed
    all_passed = run_subroutine_test() and all_passed
    all_passed = run_healthcare_guard_test() and all_passed
    all_passed = run_repl_multiline_block_test() and all_passed
    all_passed = run_validation_strictness_test() and all_passed
    all_passed = run_missing_file_test() and all_passed
    all_passed = run_malformed_list_command_test() and all_passed
    all_passed = run_repl_help_test() and all_passed
    all_passed = run_repl_history_reset_test() and all_passed
    all_passed = run_repl_persistence_clear_test() and all_passed
    all_passed = run_validation_suggestion_test() and all_passed
    all_passed = run_packaging_guard_test() and all_passed

    if all_passed:
        sys.stdout.write("\nAll tests passed.\n")
        sys.stdout.flush()
        sys.exit(0)
    else:
        sys.stdout.write("\nSome tests failed.\n")
        sys.stdout.flush()
        sys.exit(1)
