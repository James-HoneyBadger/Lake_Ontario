#!/usr/bin/env python3
"""
Lake Ontario BASIC Interpreter
A fully featured, practical programming language interpreter inspired by classic BASIC,
infused with Canadian politeness & Honey Badger attitude, pro-science, pro-health care,
pro-diversity, pro-socialism, and anti-MAGA.
"""

import ast
import difflib
import math
import os
import random
import re
import sys
import time
import warnings

try:
    import tkinter
except ImportError:  # pragma: no cover - dependency may be absent in headless envs
    tkinter = None

try:
    import readline  # noqa: F401 - enables REPL history and tab completion
except ImportError:  # pragma: no cover - absent on some platforms
    readline = None

__version__ = "1.3.0"


SUPPORTED_STATEMENT_PREFIXES = (
    "LAND_ACKNOWLEDGEMENT ",
    "HONEY_BADGER_DONT_CARE ",
    "BADGER_BITE ",
    "FAT_CATS_TAX ",
    "DONUT_DIVIDEND ",
    "NATIONAL_STOOGE ",
    "GREEN_NEW_DEAL ",
    "RHETORICAL_QUESTION ",
    "LOONIE_LOOP ",
    "SOCIAL_LICENSE ",
    "ELECTORATE_PULSE ",
    "HEAR_HEAR ",
    "CITIZEN_PETITION ",
    "VOTE_RECORDED ",
    "PETITION_SIGNATURE_COLLECTED ",
    "TESTIMONY_ADDED ",
    "FACT_CHECK ",
    "BROADCAST_CBC ",
    "TOWN_HALL ",
    "INPUT_BOX ",
    "FOR_EACH ",
    "APPEND_TO ",
    "REMOVE_FROM ",
    "SORT_CITIZENS ",
    "AVERAGE_CITIZENS ",
    "SET_PEN_COLOR ",
    "SET_FILL_COLOR ",
    "SET_CANVAS_BG ",
    "SET_PEN_WIDTH ",
    "FILL_RECTANGLE ",
    "FILL_CIRCLE ",
    "FILL_OVAL ",
    "FILL_POLYGON ",
    "FILL_TRIANGLE ",
    "WAIT ",
    "PUBLISH_RESEARCH_FILE ",
    "PUBLISH_EVIDENCE_LOG ",
    "DRAW_LINE ",
    "DRAW_RECTANGLE ",
    "DRAW_CIRCLE ",
    "DRAW_OVAL ",
    "DRAW_ARC ",
    "DRAW_POINT ",
    "DRAW_POLYGON ",
    "DRAW_TRIANGLE ",
    "DRAW_TEXT ",
    "PLAY_TONE ",
    "PLAY_SOUND_FILE ",
    "PERHAPS ",
    "PERHAPS_ALSO ",
    "COALITION ",
    "PLANK ",
    "WHILE_CLASS_CONSCIOUS ",
    "COAST_TO_COAST ",
    "SUBPOENA ",
    "GOLF_VACATION ",
    "CLIMATE_EMERGENCY ",
)

SUPPORTED_EXACT_STATEMENTS = {
    "HONEY_BADGER_MODE",
    "SHOW_VARS",
    "SHOW_EVIDENCE_LOG",
    "RESET_CITIZENS",
    "END_EACH",
    "CLEAR_GRAPHICS",
    "STILL_IN_DENIAL",
    "END_PERHAPS",
    "MINORITY_REPORT",
    "END_COALITION",
    "CONTINUE_ORGANIZING",
    "UNIVERSAL_HEALTHCARE",
    "NATIONAL_HEALTHCARE",
    "EXECUTIVE_ORDER_BLOCKED",
    "THANK_YOU_EH",
    "BREAK_FROM_CAUCUS",
    "NEXT_MOTION",
    "MOTION_PASSED",
    "RETURN_TO_OTTAWA",
    "IMPEACH",
    "STOP_SOUND",
    "HONEY_BADGER_GROWL",
    "TOWN_HALL_BELL",
    "STANDING_OVATION",
}

REPL_BLOCK_OPEN_PREFIXES = (
    "PERHAPS ",
    "COALITION ",
    "WHILE_CLASS_CONSCIOUS ",
    "COAST_TO_COAST ",
    "FOR_EACH ",
)

REPL_BLOCK_OPEN_EXACT = {
    "UNIVERSAL_HEALTHCARE",
    "NATIONAL_HEALTHCARE",
}

REPL_BLOCK_CLOSE_EXACT = {
    "END_PERHAPS",
    "END_COALITION",
    "CONTINUE_ORGANIZING",
    "THANK_YOU_EH",
    "END_EACH",
    "EXECUTIVE_ORDER_BLOCKED",
}


def is_supported_statement(stmt):
    if stmt in SUPPORTED_EXACT_STATEMENTS:
        return True
    return any(stmt.startswith(prefix) for prefix in SUPPORTED_STATEMENT_PREFIXES)


def repl_block_delta(stmt):
    if stmt in REPL_BLOCK_OPEN_EXACT:
        return 1
    if stmt in REPL_BLOCK_CLOSE_EXACT:
        return -1
    if any(stmt.startswith(prefix) for prefix in REPL_BLOCK_OPEN_PREFIXES):
        return 1
    return 0


# --- Expression translation ---

STRING_LITERAL_PATTERN = re.compile(r'(["\'])(?:(?=(\\?))\2.)*?\1')
FUNCTION_CALL_PATTERN = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")

# Applied after literal masking; word boundaries keep `_` in names from matching.
EXPRESSION_KEYWORDS = (
    ("CLASSIFIED_MAR_A_LAGO", "None"),
    ("POWER_TO_THE_PEOPLE", "**"),
    ("EVIDENCE_BASED", "True"),
    ("ALTERNATIVE_FACT", "False"),
    ("PROPORTIONAL_SHARE", "/"),
    ("FAIR_MULTIPLIER", "*"),
    ("WEALTH_TAX", "-"),
    ("EQUAL_PAY", "+"),
    ("MAPLE_SYRUP", "%"),
    ("MOONSHOT", "**"),
    ("AND", "and"),
    ("OR", "or"),
    ("NOT", "not"),
)

KNOWN_KEYWORD_NAMES = frozenset(
    prefix.strip() for prefix in SUPPORTED_STATEMENT_PREFIXES
)

KNOWN_STATEMENT_NAMES = tuple(
    sorted(
        {prefix.strip() for prefix in SUPPORTED_STATEMENT_PREFIXES}
        | SUPPORTED_EXACT_STATEMENTS
    )
)


def suggest_correction(name, candidates):
    """Return a friendly 'did you mean' hint, or an empty string."""
    matches = difflib.get_close_matches(name, sorted(candidates), n=1, cutoff=0.6)
    if not matches:
        return ""
    return f" — did you mean {matches[0]}? The committee is happy to assist."


def strip_inline_comment(stmt):
    """Remove a trailing ``EXCUSE_ME`` comment, leaving string literals alone."""
    masked = mask_string_literals(stmt)
    match = re.search(r"(^|\s)EXCUSE_ME\b", masked)
    if not match:
        return stmt
    return stmt[: match.start()].rstrip()


def mask_string_literals(text):
    """Blank out string literals, keeping offsets intact for later slicing."""
    return STRING_LITERAL_PATTERN.sub(
        lambda match: '"' + " " * (len(match.group(0)) - 2) + '"', text
    )


def find_function_calls(stmt):
    """Return the names used as function calls in a statement."""
    return FUNCTION_CALL_PATTERN.findall(mask_string_literals(stmt))


# --- Block layout ---

BLOCK_CLOSERS = {
    "perhaps": "END_PERHAPS",
    "coalition": "END_COALITION",
    "while": "CONTINUE_ORGANIZING",
    "for": "THANK_YOU_EH",
    "foreach": "END_EACH",
    "healthcare": "EXECUTIVE_ORDER_BLOCKED",
}

BLOCK_LABELS = {
    "perhaps": "PERHAPS",
    "coalition": "COALITION",
    "while": "WHILE_CLASS_CONSCIOUS",
    "for": "COAST_TO_COAST",
    "foreach": "FOR_EACH",
    "healthcare": "UNIVERSAL_HEALTHCARE",
}

HEALTHCARE_OPENERS = ("UNIVERSAL_HEALTHCARE", "NATIONAL_HEALTHCARE")


def _block_opener(stmt):
    if stmt.startswith("PERHAPS "):
        return "perhaps"
    if stmt.startswith("COALITION "):
        return "coalition"
    if stmt.startswith("WHILE_CLASS_CONSCIOUS "):
        return "while"
    if stmt.startswith("COAST_TO_COAST "):
        return "for"
    if stmt.startswith("FOR_EACH "):
        return "foreach"
    if stmt in HEALTHCARE_OPENERS:
        return "healthcare"
    return None


def _block_closer(stmt):
    for kind, closer in BLOCK_CLOSERS.items():
        if stmt == closer:
            return kind
    return None


def _line_label(line_number):
    return f"Line {line_number}" if line_number is not None else "Line ?"


PLANK_LITERAL_PATTERN = re.compile(
    r"^(?P<operator>>=|<=|==|!=|>|<)?\s*(?P<value>-?\d+(?:\.\d+)?)$"
)


def _plank_coverage(plank_stmt):
    """Describe the values a PLANK can match, when that is knowable statically.

    Returns ``("numeric", low, low_inclusive, high, high_inclusive)``,
    ``("text", value)``, or None when the plank depends on a variable.
    """
    argument = _statement_arg(plank_stmt)
    match = PLANK_LITERAL_PATTERN.match(argument)
    if match:
        operator = match.group("operator") or "=="
        value = float(match.group("value"))
        if operator == "==":
            return ("numeric", value, True, value, True)
        if operator == ">=":
            return ("numeric", value, True, math.inf, True)
        if operator == ">":
            return ("numeric", value, False, math.inf, True)
        if operator == "<=":
            return ("numeric", -math.inf, True, value, True)
        if operator == "<":
            return ("numeric", -math.inf, True, value, False)
        return None  # "!=" covers two disjoint ranges; not worth tracking

    try:
        literal = ast.literal_eval(argument)
    except (SyntaxError, ValueError):
        return None
    if isinstance(literal, str):
        return ("text", literal)
    return None


def _merge_coverage(entries):
    """Merge (line_number, numeric coverage) pairs into contiguous ranges."""
    merged = []
    for line_number, spec in sorted(entries, key=lambda item: item[1][1]):
        _, low, low_inc, high, high_inc = spec
        if merged:
            last_spec, sources = merged[-1]
            _, start, start_inc, end, end_inc = last_spec
            touches = low < end or (low == end and (end_inc or low_inc))
            if touches:
                if high > end or (high == end and high_inc):
                    merged[-1] = (
                        ("numeric", start, start_inc, high, high_inc),
                        sources + [line_number],
                    )
                else:
                    sources.append(line_number)
                continue
        merged.append((spec, [line_number]))
    return merged


def _coverage_contains(covering, candidate):
    """True when ``candidate`` fits entirely inside ``covering``."""
    _, start, start_inc, end, end_inc = covering
    _, cand_start, cand_start_inc, cand_end, cand_end_inc = candidate
    start_ok = start < cand_start or (
        start == cand_start and (start_inc or not cand_start_inc)
    )
    end_ok = end > cand_end or (end == cand_end and (end_inc or not cand_end_inc))
    return start_ok and end_ok


def _shadowing_line(candidate, entries):
    """Line number of the earlier PLANK that already covers this one, if any."""
    if candidate[0] == "text":
        for line_number, other in entries:
            if other[0] == "text" and other[1] == candidate[1]:
                return line_number
        return None

    numeric = [(line, spec) for line, spec in entries if spec[0] == "numeric"]
    for merged, sources in _merge_coverage(numeric):
        if _coverage_contains(merged, candidate):
            return sources[0]
    return None


def _advise_shadowed_plank(layout, lines, opener_index, index):
    """Warn when earlier planks already match everything this plank allows."""
    entries = layout.coverage.setdefault(opener_index, [])
    candidate = _plank_coverage(lines[index][1])
    if candidate is None:
        return
    shadowing = _shadowing_line(candidate, entries)
    if shadowing is not None:
        layout.advise(
            lines[index][0],
            f"this PLANK can never match, because the PLANK at line {shadowing} "
            "already covers every value it allows. The first match wins.",
        )
    entries.append((lines[index][0], candidate))


class BlockLayout:
    """Precomputed jump table, so the interpreter never rescans for block ends."""

    def __init__(self):
        self.closing = {}
        self.branches = {}
        self.owner = {}
        self.problems = []
        self.warnings = []
        self.coverage = {}

    def report(self, line_number, message):
        self.problems.append(f"{_line_label(line_number)}: {message}")

    def advise(self, line_number, message):
        self.warnings.append(f"{_line_label(line_number)}: {message}")

    def close_of(self, opener_index, fallback):
        return self.closing.get(opener_index, fallback)


def build_block_layout(lines):
    """Match every block opener with its closer and record PERHAPS branch chains."""
    layout = BlockLayout()
    stack = []

    for index, (line_number, stmt) in enumerate(lines):
        if stmt.startswith("PERHAPS "):
            stack.append(("perhaps", index))
            layout.branches[index] = []
            continue

        if stmt.startswith("PERHAPS_ALSO ") or stmt == "STILL_IN_DENIAL":
            marker = (
                "PERHAPS_ALSO" if stmt.startswith("PERHAPS_ALSO ") else "STILL_IN_DENIAL"
            )
            if stack and stack[-1][0] == "perhaps":
                opener_index = stack[-1][1]
                layout.branches[opener_index].append((marker, index))
                layout.owner[index] = opener_index
            else:
                layout.report(
                    line_number, f"{marker} has no PERHAPS block to belong to"
                )
            continue

        if stmt.startswith("COALITION "):
            stack.append(("coalition", index))
            layout.branches[index] = []
            layout.coverage[index] = []
            continue

        if stmt.startswith("PLANK ") or stmt == "MINORITY_REPORT":
            marker = "PLANK" if stmt.startswith("PLANK ") else "MINORITY_REPORT"
            if stack and stack[-1][0] == "coalition":
                opener_index = stack[-1][1]
                chain = layout.branches[opener_index]
                if marker == "MINORITY_REPORT" and any(
                    kind == "MINORITY_REPORT" for kind, _ in chain
                ):
                    layout.report(
                        line_number,
                        "MINORITY_REPORT appears twice in the same COALITION",
                    )
                if marker == "PLANK" and any(
                    kind == "MINORITY_REPORT" for kind, _ in chain
                ):
                    layout.report(
                        line_number,
                        "this PLANK comes after MINORITY_REPORT and can never be "
                        "reached",
                    )
                if marker == "PLANK":
                    _advise_shadowed_plank(layout, lines, opener_index, index)
                chain.append((marker, index))
                layout.owner[index] = opener_index
            else:
                if any(kind == "coalition" for kind, _ in stack):
                    open_kind = stack[-1][0]
                    layout.report(
                        line_number,
                        f"{marker} appears inside an open "
                        f"{BLOCK_LABELS[open_kind]} block. Close it with "
                        f"{BLOCK_CLOSERS[open_kind]} before the next {marker}.",
                    )
                else:
                    layout.report(
                        line_number, f"{marker} has no COALITION block to belong to"
                    )
            continue

        opener = _block_opener(stmt)
        if opener is not None:
            stack.append((opener, index))
            continue

        closer = _block_closer(stmt)
        if closer is not None:
            if stack and stack[-1][0] == closer:
                _, opener_index = stack.pop()
                layout.closing[opener_index] = index
            elif stack:
                layout.report(
                    line_number,
                    f"{stmt} arrived while {BLOCK_LABELS[stack[-1][0]]} "
                    "was still waiting to be closed",
                )
            else:
                layout.report(line_number, f"{stmt} without an open block")
        continue

    for kind, index in stack:
        if kind == "healthcare":
            # A safety net may simply cover the rest of the script.
            continue
        layout.report(
            lines[index][0],
            f"{BLOCK_LABELS[kind]} opened here never reaches {BLOCK_CLOSERS[kind]}",
        )

    return layout


class LakeOntarioInterpreterError(Exception):
    """Custom exception type for interpreter runtime errors."""


class LakeOntarioRuntimeError(LakeOntarioInterpreterError):
    """Raised when a script fails and no UNIVERSAL_HEALTHCARE block caught it.

    The CLI turns this into a polite exit code; the GUI shows it in the output
    pane; embedding callers can handle it without the interpreter calling
    ``sys.exit()`` behind their back.
    """


class LOString(str):

    def __add__(self, other):
        return LOString(str(self) + str(other))

    def __radd__(self, other):
        return LOString(str(other) + str(self))


# --- Satirical & Practical Built-in Functions ---


def debunk(val):
    text = str(val).lower()
    return LOString(f"{text} (Fact-checked by CBC, eh!)")


def fact_check_crowd(val):
    try:
        num = float(val)
        return int(num / 10)
    except (TypeError, ValueError):
        return 0


def tax_the_billionaire(val):
    try:
        num = float(val)
        if num > 1000000:
            excess = num - 1000000
            res = 1000000 + (excess * 0.1)
        else:
            res = num
        return LOString(f"{res:.2f}")
    except (TypeError, ValueError):
        return LOString("0.00")


def defund_oligarchy(val):
    try:
        num = float(val)
        res = max(0.0, num * 0.05)
        return LOString(f"{res:.2f}")
    except (TypeError, ValueError):
        return LOString("0.00")


def living_wage(hours, base_rate=25.0):
    try:
        res = float(hours) * float(base_rate)
        return LOString(f"{res:.2f}")
    except (TypeError, ValueError):
        return LOString("0.00")


def universal_basic_income(population, grant=2000.0):
    try:
        res = float(population) * float(grant)
        return LOString(f"{res:.2f}")
    except (TypeError, ValueError):
        return LOString("0.00")


def carbon_offset(emissions_tons):
    try:
        res = float(emissions_tons) * 65.0
        return LOString(f"{res:.2f}")
    except (TypeError, ValueError):
        return LOString("0.00")


def format_currency(val):
    try:
        num = float(val)
        return LOString(f"{num:.2f}")
    except (TypeError, ValueError):
        return LOString("0.00")


def celebrate_diversity(*args):
    items = [str(a) for a in args]
    return "🌈 🏳️‍🌈 🏳️‍⚧️ Inclusive Collective: " + ", ".join(items) + " ✊"


def unionize(*workers):
    if len(workers) == 1 and isinstance(workers[0], (list, tuple)):
        workers = workers[0]
    return [f"Union Member: {w}" for w in workers]


def science_fact(topic):
    topic_str = str(topic).lower()
    facts = {
        "climate": (
            "Peer-Reviewed Consensus: Anthropogenic climate change is real and "
            "requires immediate renewable transition."
        ),
        "vaccines": (
            "Peer-Reviewed Consensus: Vaccines are safe, effective, and save "
            "millions of lives globally."
        ),
        "evolution": (
            "Peer-Reviewed Consensus: Biological evolution by natural selection "
            "is the foundational principle of biology."
        ),
        "diversity": (
            "Peer-Reviewed Consensus: Diverse and inclusive communities show "
            "higher resilience, innovation, and well-being."
        ),
    }
    for k, v in facts.items():
        if k in topic_str:
            return v
    return (
        "Peer-Reviewed Science: Empirical analysis confirms "
        f"{topic} is backed by scientific evidence."
    )


def peer_reviewed_sqrt(val):
    return math.sqrt(float(val))


def science_round(val, decimals=2):
    return round(float(val), int(decimals))


def read_resource(filepath):
    path = str(filepath).strip("\"'")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except (OSError, TypeError, ValueError) as exc:
        raise LakeOntarioInterpreterError(
            f"READ_RESOURCE could not open '{path}': {exc}"
        ) from None


def publish_research(filepath, content):
    try:
        with open(str(filepath).strip("\"'"), "w", encoding="utf-8") as f:
            f.write(str(content))
        return True
    except (OSError, TypeError, ValueError):
        return False


def play_tone_fallback(frequency, duration_ms):
    """Best-effort headless beep (no GUI sound callback registered)."""
    try:
        import winsound

        winsound.Beep(int(frequency), int(duration_ms))
    except (ImportError, ValueError, RuntimeError):
        sys.stdout.write("\a")
        sys.stdout.flush()


def honey_badger_debunk(val):
    text = str(val)
    return LOString(
        f"🦡 HONEY BADGER DEBUNK: Shredded lie '{text}' into peer-reviewed dust! "
        "Takes no shit!"
    )


def honey_badger_bite(target):
    text = str(target)
    return LOString(
        f"🦡 HONEY BADGER BITES BACK: Relentlessly tearing apart '{text}' "
        "with zero fear and 100% truth!"
    )


def honey_badger_strike(action):
    text = str(action)
    return LOString(
        f"🦡 UNYIELDING BADGER STRIKE: Taking no shit on '{text}'! Standing firm!"
    )


def say_sorry(message):
    text = str(message)
    return LOString(
        f"Sorry, eh? {text} — delivered with extra maple syrup and contrition."
    )


def make_it_rain(amount):
    try:
        num = float(amount)
        redistributed = num * 0.95
        return LOString(
            f"🍁 MAKE IT RAIN: Redistributing ${redistributed:.2f} "
            "to healthcare, transit, and doughnuts."
        )
    except (TypeError, ValueError):
        return LOString("🍁 MAKE IT RAIN: Alternative facts cannot be redistributed.")


def public_transit_fare(distance, base_fare=3.50):
    try:
        miles = float(distance)
        fare = max(1.0, base_fare + miles * 0.25)
        return LOString(
            f"🚊 Transit fare for {miles:.1f} km: ${fare:.2f} "
            "(inclusive of polite service fees)"
        )
    except (TypeError, ValueError):
        return LOString("🚊 Transit fare unavailable: Invalid route.")


def toque_warmth(temp_celsius):
    try:
        temp = float(temp_celsius)
        if temp < -20:
            return LOString(
                "🧣 Toque warmth: Full Canada Goose thermal emergency activated."
            )
        if temp < 0:
            return LOString(
                "🧣 Toque warmth: Cozy enough for poutine and parliament protests."
            )
        return LOString(
            "🧣 Toque warmth: Too warm for a toque, but wear it anyway for civic pride."
        )
    except (TypeError, ValueError):
        return LOString("🧣 Toque warmth: Invalid weather, eh?")


def truth_meter(claim):
    text = str(claim)
    rating = 100 if "EVIDENCE_BASED" in text or "True" in text else 0
    return LOString(
        f"📏 Truth Meter: {rating}% sincerity, with a side of maple humour."
    )


def make_it_snow(forecast, flakes=100):
    try:
        count = int(flakes)
        return LOString(
            f"❄️ Snow forecast: {count} flake-level protests expected when {forecast}."
        )
    except (TypeError, ValueError):
        return LOString("❄️ Snow forecast: Confused, like a polar vortex in July.")


def fat_cats_tax(amount):
    try:
        num = float(amount)
        taxed = max(0.0, num * 0.95)
        return LOString(
            f"💼 FAT CATS TAX: Extracted ${taxed:.2f} from the one-percenters "
            "and sent it to universal crumbs."
        )
    except (TypeError, ValueError):
        return LOString("💼 FAT CATS TAX: Alternative facts cannot be taxed.")


def donut_dividend(amount):
    try:
        num = float(amount)
        return LOString(
            f"🍩 DONUT DIVIDEND: Distributing ${num:.2f} worth of pastries "
            "to every rally-goer."
        )
    except (TypeError, ValueError):
        return LOString("🍩 DONUT DIVIDEND: Invalid pastry budget.")


def national_stooge(statement):
    text = str(statement)
    return LOString(
        "🎩 NATIONAL STOOGE: '"
        f"{text}"
        "' — delivered with maximum spin and minimum accountability."
    )


def green_new_deal(goal):
    return LOString(
        "🌿 GREEN NEW DEAL: Targeting '"
        f"{goal}"
        "' with electric buses, solar subsidies, and polite protest marches."
    )


def rhetorical_question(question):
    return LOString(
        "❓ RHETORICAL QUESTION: "
        f"{question}"
        " — and yes, the answer is obviously 'EVIDENCE_BASED'."
    )


def loonie_loop(count):
    try:
        num = int(count)
        return [f"Loonie #{i + 1}" for i in range(max(0, num))]
    except (TypeError, ValueError):
        return ["Loonie loop failed: invalid flake count."]


def social_license(license_name):
    return LOString(
        "✅ SOCIAL LICENSE: '"
        f"{license_name}"
        "' has 100% approval from unionized beavers and open-source poets."
    )


def electorate_pulse(value):
    try:
        pct = float(value)
        return LOString(
            f"📊 ELECTORATE PULSE: {min(max(pct, 0.0), 100.0):.1f}% "
            "enthusiasm for the public mandate."
        )
    except (TypeError, ValueError):
        return LOString("📊 ELECTORATE PULSE: Polling data is unavailable, eh.")


def parliament_gazette(title, content=""):
    return LOString(
        "📜 PARLIAMENT GAZETTE: " f"{title} — {content} — officially recorded, eh."
    )


def poll_the_people(question, agreement=50):
    try:
        percentage = min(max(float(agreement), 0.0), 100.0)
        return LOString(
            f"🗳️ PUBLIC POLL: {question} received {percentage:.1f}% agreement; "
            "the remaining voters requested a committee."
        )
    except (TypeError, ValueError):
        return LOString(
            f"🗳️ PUBLIC POLL: {question} received an undecidable shrug, eh."
        )


def civic_compromise(proposal_a, proposal_b):
    return LOString(
        "🤝 CIVIC COMPROMISE: Combine '"
        f"{proposal_a}"
        "' with '"
        f"{proposal_b}"
        "' and refer the result to three committees."
    )


def rigged_election_meter(claim):
    text = str(claim)
    lowered = text.lower()
    if "rigged" in lowered or "stolen" in lowered:
        return LOString(
            "🗳️ RIGGED ELECTION METER: 0% credibility. "
            "Please submit evidence before submitting another slogan."
        )
    return LOString(
        f"🗳️ RIGGED ELECTION METER: '{text}' received an evidence-based review."
    )


def voter_suppression_alert(tactic):
    return LOString(
        "🚫 VOTER SUPPRESSION ALERT: "
        f"'{tactic}' flagged for review. Expand access, explain the rules, "
        "and keep the polling place open."
    )


def corporate_fine(company, violation, amount=100000):
    try:
        fine = max(0.0, float(amount))
        return LOString(
            f"💰 CORPORATE FINE: {company} assessed ${fine:.2f} for {violation}; "
            "the shareholders have been asked to read the receipt."
        )
    except (TypeError, ValueError):
        return LOString(
            f"💰 CORPORATE FINE: {company} fined for {violation}; "
            "the amount requires an accountant and a very stern committee."
        )


def workplace_safety_audit(workplace):
    return LOString(
        "🦺 WORKPLACE SAFETY AUDIT: "
        f"{workplace} requires hazard checks, paid training, and workers "
        "who can report concerns without retaliation."
    )


def indigenous_land_return(territory, people):
    return LOString(
        "🪶 INDIGENOUS LAND RETURN: "
        f"Commitment recorded for {territory} and {people}; "
        "consultation, consent, and accountable action are required."
    )


def renewable_energy_target(target_percent, year):
    try:
        percentage = min(max(float(target_percent), 0.0), 100.0)
        target_year = int(year)
        return LOString(
            f"⚡ RENEWABLE ENERGY TARGET: {percentage:.1f}% clean energy by "
            f"{target_year}; the grid has been issued a hopeful spreadsheet."
        )
    except (TypeError, ValueError):
        return LOString(
            "⚡ RENEWABLE ENERGY TARGET: Invalid target; please provide "
            "a percentage and a year, eh."
        )


def wage_theft_recovery(amount):
    try:
        recovered = max(0.0, float(amount))
        return LOString(
            f"✊ WAGE THEFT RECOVERY: ${recovered:.2f} returned to workers; "
            "the payroll department has been assigned homework."
        )
    except (TypeError, ValueError):
        return LOString(
            "✊ WAGE THEFT RECOVERY: Invalid amount; the spreadsheet is "
            "requesting a union representative."
        )


def affordable_housing_built(units, location):
    try:
        count = max(0, int(units))
        return LOString(
            f"🏠 AFFORDABLE HOUSING: {count} homes announced for {location}; "
            "the key ceremony includes actual keys."
        )
    except (TypeError, ValueError):
        return LOString(
            f"🏠 AFFORDABLE HOUSING: Units for {location} require a count "
            "before the ribbon can be cut."
        )


def accessibility_audit(building):
    return LOString(
        "♿ ACCESSIBILITY AUDIT: "
        f"{building} should provide step-free access, clear signage, "
        "usable technology, and meaningful participation."
    )


def accommodation_approved(request):
    return LOString(
        "✅ ACCOMMODATION APPROVED: "
        f"{request} is approved; dignity and access are not optional features."
    )


def public_service_wait(service, minutes):
    try:
        wait = max(0.0, float(minutes))
        return LOString(
            f"⏱️ PUBLIC SERVICE WAIT: {service} reports {wait:.1f} minutes; "
            "the queue has been reminded that people are not paperwork."
        )
    except (TypeError, ValueError):
        return LOString(
            f"⏱️ PUBLIC SERVICE WAIT: {service} has an unmeasurable wait; "
            "please publish the queue data, eh."
        )


def emissions_reduced(baseline, current):
    try:
        original = float(baseline)
        present = float(current)
        if original <= 0:
            return LOString("🌍 EMISSIONS REDUCED: Baseline must be positive, eh.")
        reduction = min(max((original - present) / original * 100, 0.0), 100.0)
        return LOString(
            f"🌍 EMISSIONS REDUCED: {reduction:.1f}% reduction recorded; "
            "the atmosphere has filed a grateful memo."
        )
    except (TypeError, ValueError):
        return LOString("🌍 EMISSIONS REDUCED: Measurements require numbers, eh.")


def climate_risk_score(place, score):
    try:
        risk = min(max(float(score), 0.0), 100.0)
        return LOString(
            f"🌡️ CLIMATE RISK SCORE: {place} rates {risk:.1f}/100; "
            "adaptation planning has been moved ahead of the ceremonial shrug."
        )
    except (TypeError, ValueError):
        return LOString(f"🌡️ CLIMATE RISK SCORE: {place} needs a numeric score, eh.")


def science_consensus(topic):
    known_topics = {
        "climate": "Human-caused climate change is real and requires rapid action.",
        "vaccines": "Vaccines are rigorously studied tools for preventing disease.",
        "evolution": "Evolution explains the diversity of life through evidence.",
    }
    statement = known_topics.get(str(topic).lower())
    if statement is None:
        return LOString(
            f"🔬 SCIENCE CONSENSUS: No local briefing for {topic}; "
            "consult the evidence before convening a panel."
        )
    return LOString(f"🔬 SCIENCE CONSENSUS: {statement}")


def treaty_obligation_tracker(treaty):
    return LOString(
        "📋 TREATY OBLIGATION TRACKER: "
        f"{treaty} requires ongoing review, accountability, and action "
        "rather than a commemorative coffee mug."
    )


def indigenous_consultation_required(project):
    return LOString(
        "🪶 INDIGENOUS CONSULTATION REQUIRED: "
        f"{project} must include early, meaningful consultation and consent "
        "with affected Indigenous communities."
    )


def community_care_plan(need, response):
    return LOString(
        "🤝 COMMUNITY CARE PLAN: "
        f"Respond to {need} with {response}; fund the people doing the care "
        "and leave the paper crown in the stationery cupboard."
    )


def median_citizens(values):
    try:
        numbers = sorted(float(value) for value in values)
        if not numbers:
            return 0.0
        middle = len(numbers) // 2
        if len(numbers) % 2:
            return numbers[middle]
        return (numbers[middle - 1] + numbers[middle]) / 2
    except (TypeError, ValueError):
        return 0.0


def citizen_sum(values):
    try:
        return sum(float(value) for value in values)
    except (TypeError, ValueError):
        return 0.0


def citizen_any(values):
    try:
        return any(values)
    except TypeError:
        return bool(values)


def citizen_all(values):
    try:
        return all(values)
    except TypeError:
        return bool(values)


def evidence_score(claim, evidence):
    if isinstance(evidence, (list, tuple, set, dict)):
        score = min(len(evidence) * 25, 100)
    elif isinstance(evidence, bool):
        score = 100 if evidence else 0
    else:
        score = 50 if str(evidence).strip() else 0
    return LOString(
        f"🔎 EVIDENCE SCORE: '{claim}' receives {score}/100; "
        "the committee requests sources, not vibes."
    )


def registry_get(registry, key, default=None):
    if not isinstance(registry, dict):
        return default
    return registry.get(key, default)


def registry_keys(registry):
    return list(registry.keys()) if isinstance(registry, dict) else []


def registry_values(registry):
    return list(registry.values()) if isinstance(registry, dict) else []


def policy_score(policy, criteria):
    if isinstance(criteria, (list, tuple, set, dict)):
        score = min(len(criteria) * 20, 100)
    elif criteria:
        score = 20
    else:
        score = 0
    return LOString(
        f"📊 POLICY SCORE: '{policy}' receives {score}/100; "
        "the review panel has requested one more appendix, eh."
    )


def group_by_citizens(values, categories):
    try:
        grouped = {}
        for value, category in zip(values, categories):
            grouped.setdefault(category, []).append(value)
        return grouped
    except TypeError:
        return {}


def count_by_citizens(values, target):
    try:
        return sum(value == target for value in values)
    except TypeError:
        return 0


def citizen_count(*values):
    if len(values) == 1 and isinstance(values[0], (list, tuple, dict, set)):
        return len(values[0])
    return len(values)


def collective_append(target, item):
    if target is None:
        return [item]
    if isinstance(target, list):
        target.append(item)
        return target
    if isinstance(target, tuple):
        return list(target) + [item]
    return [target, item]


def sort_citizens(values):
    if values is None:
        return []
    items = list(values)
    return sorted(
        items, key=lambda v: float(v) if isinstance(v, (int, float)) else str(v)
    )


def average_citizens(values):
    if values is None:
        return 0.0
    items = list(values)
    if not items:
        return 0.0
    try:
        return sum(float(v) for v in items) / len(items)
    except (TypeError, ValueError):
        return 0.0


def str_upper(s):
    return LOString(str(s).upper())


def str_lower(s):
    return LOString(str(s).lower())


def str_length(s):
    return len(str(s))


def str_trim(s):
    return LOString(str(s).strip())


def str_contains(s, sub):
    return str(sub) in str(s)


def str_replace(s, old, new):
    return LOString(str(s).replace(str(old), str(new)))


def str_split(s, delim=","):
    return str(s).split(str(delim))


def to_number(s):
    try:
        text = str(s).strip()
        return int(text) if "." not in text else float(text)
    except (ValueError, TypeError):
        return 0


def to_text(val):
    return LOString(str(val))


def math_abs(v):
    return abs(float(v))


def math_floor(v):
    return int(math.floor(float(v)))


def math_ceil(v):
    return int(math.ceil(float(v)))


def math_min(*args):
    return min(float(a) for a in args)


def math_max(*args):
    return max(float(a) for a in args)


def random_democracy(lo=0, hi=100):
    return random.randint(int(lo), int(hi))


def citizen_at(lst, idx):
    try:
        return list(lst)[int(idx)]
    except (IndexError, TypeError, ValueError):
        return None


def first_citizen(lst):
    try:
        return list(lst)[0]
    except (IndexError, TypeError):
        return None


def last_citizen(lst):
    try:
        return list(lst)[-1]
    except (IndexError, TypeError):
        return None


def join_collective(lst, sep=", "):
    return LOString(str(sep).join(str(x) for x in lst))


# Built once at import time. evaluate_expression() runs in tight loops, so
# rebuilding this table per expression was pure ceremony.
LO_BUILTINS = {
    "DEBUNK": debunk,
    "FACT_CHECK_CROWD": fact_check_crowd,
    "TAX_THE_BILLIONAIRE": tax_the_billionaire,
    "DEFUND_OLIGARCHY": defund_oligarchy,
    "LIVING_WAGE": living_wage,
    "UNIVERSAL_BASIC_INCOME": universal_basic_income,
    "CARBON_OFFSET": carbon_offset,
    "CELEBRATE_DIVERSITY": celebrate_diversity,
    "UNIONIZE": unionize,
    "SCIENCE_FACT": science_fact,
    "PEER_REVIEWED_SQRT": peer_reviewed_sqrt,
    "SCIENCE_ROUND": science_round,
    "READ_RESOURCE": read_resource,
    "PUBLISH_RESEARCH": publish_research,
    "FORMAT_CURRENCY": format_currency,
    "CAD_CURRENCY": format_currency,
    "HONEY_BADGER_DEBUNK": honey_badger_debunk,
    "HONEY_BADGER_BITE": honey_badger_bite,
    "HONEY_BADGER_STRIKE": honey_badger_strike,
    "SAY_SORRY": say_sorry,
    "MAKE_IT_RAIN": make_it_rain,
    "PUBLIC_TRANSIT_FARE": public_transit_fare,
    "TOQUE_WARMTH": toque_warmth,
    "TRUTH_METER": truth_meter,
    "MAKE_IT_SNOW": make_it_snow,
    "FAT_CATS_TAX": fat_cats_tax,
    "DONUT_DIVIDEND": donut_dividend,
    "NATIONAL_STOOGE": national_stooge,
    "GREEN_NEW_DEAL": green_new_deal,
    "RHETORICAL_QUESTION": rhetorical_question,
    "LOONIE_LOOP": loonie_loop,
    "SOCIAL_LICENSE": social_license,
    "ELECTORATE_PULSE": electorate_pulse,
    "PARLIAMENT_GAZETTE": parliament_gazette,
    "POLL_THE_PEOPLE": poll_the_people,
    "CIVIC_COMPROMISE": civic_compromise,
    "RIGGED_ELECTION_METER": rigged_election_meter,
    "VOTER_SUPPRESSION_ALERT": voter_suppression_alert,
    "CORPORATE_FINE": corporate_fine,
    "WORKPLACE_SAFETY_AUDIT": workplace_safety_audit,
    "INDIGENOUS_LAND_RETURN": indigenous_land_return,
    "RENEWABLE_ENERGY_TARGET": renewable_energy_target,
    "WAGE_THEFT_RECOVERY": wage_theft_recovery,
    "AFFORDABLE_HOUSING_BUILT": affordable_housing_built,
    "ACCESSIBILITY_AUDIT": accessibility_audit,
    "ACCOMMODATION_APPROVED": accommodation_approved,
    "PUBLIC_SERVICE_WAIT": public_service_wait,
    "EMISSIONS_REDUCED": emissions_reduced,
    "CLIMATE_RISK_SCORE": climate_risk_score,
    "SCIENCE_CONSENSUS": science_consensus,
    "TREATY_OBLIGATION_TRACKER": treaty_obligation_tracker,
    "INDIGENOUS_CONSULTATION_REQUIRED": indigenous_consultation_required,
    "COMMUNITY_CARE_PLAN": community_care_plan,
    "MEDIAN_CITIZENS": median_citizens,
    "CITIZEN_SUM": citizen_sum,
    "CITIZEN_ANY": citizen_any,
    "CITIZEN_ALL": citizen_all,
    "EVIDENCE_SCORE": evidence_score,
    "REGISTRY_GET": registry_get,
    "REGISTRY_KEYS": registry_keys,
    "REGISTRY_VALUES": registry_values,
    "POLICY_SCORE": policy_score,
    "GROUP_BY_CITIZENS": group_by_citizens,
    "COUNT_BY_CITIZENS": count_by_citizens,
    "CITIZEN_COUNT": citizen_count,
    "COLLECTIVE_APPEND": collective_append,
    "SORT_CITIZENS": sort_citizens,
    "AVERAGE_CITIZENS": average_citizens,
    "COLLECTIVE_LIST": lambda *args: list(args),
    "MUTUAL_AID_REGISTRY": lambda **kwargs: dict(kwargs),
    "STR_UPPER": str_upper,
    "STR_LOWER": str_lower,
    "STR_LEN": str_length,
    "STR_TRIM": str_trim,
    "STR_CONTAINS": str_contains,
    "STR_REPLACE": str_replace,
    "STR_SPLIT": str_split,
    "TO_NUMBER": to_number,
    "TO_TEXT": to_text,
    "MATH_ABS": math_abs,
    "MATH_FLOOR": math_floor,
    "MATH_CEIL": math_ceil,
    "MATH_MIN": math_min,
    "MATH_MAX": math_max,
    "RANDOM_DEMOCRACY": random_democracy,
    "CITIZEN_AT": citizen_at,
    "FIRST_CITIZEN": first_citizen,
    "LAST_CITIZEN": last_citizen,
    "JOIN_COLLECTIVE": join_collective,
}

# A private globals dict with __builtins__ removed keeps eval honest: the
# language exposes its own whitelist and nothing else.
LO_EVAL_GLOBALS = {
    "__builtins__": {},
    "True": True,
    "False": False,
    "None": None,
    "LOString": LOString,
    **LO_BUILTINS,
}

LO_RESERVED_NAMES = frozenset(("and", "or", "not")) | frozenset(LO_EVAL_GLOBALS)


COMPARISON_OPERATORS = (">=", "<=", "==", "!=", ">", "<")


def _compare_values(left, right, operator):
    if operator == "==":
        return left == right
    if operator == "!=":
        return left != right
    try:
        if operator == ">=":
            return left >= right
        if operator == "<=":
            return left <= right
        if operator == ">":
            return left > right
        return left < right
    except TypeError:
        raise LakeOntarioInterpreterError(
            f"cannot compare {left!r} with {right!r} using {operator}"
        ) from None


_UNSET = object()

EVIDENCE_LOG_LIMIT = 200


def _statement_arg(stmt):
    """Return the text after a statement's keyword, without magic offsets."""
    _, _, rest = stmt.partition(" ")
    return rest.strip()


def _render_value(value):
    """Render a value the way the language spells it, not the way Python does."""
    if isinstance(value, bool):
        return "EVIDENCE_BASED" if value else "ALTERNATIVE_FACT"
    if value is None:
        return "CLASSIFIED_MAR_A_LAGO"
    if isinstance(value, float):
        text = repr(value)
        # Tidy floating-point noise (0.1 + 0.2) without hiding ordinary decimals.
        return f"{value:.12g}" if len(text) > 12 else text
    if isinstance(value, dict):
        return "{" + ", ".join(
            f"{key}: {_render_value(item)}" for key, item in value.items()
        ) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(str(_render_value(item)) for item in value) + "]"
    if isinstance(value, tuple):
        return "(" + ", ".join(str(_render_value(item)) for item in value) + ")"
    return value


def _render_broadcast(value):
    """Render a BROADCAST_CBC value without leaking Python repr."""
    if isinstance(value, tuple):
        return " ".join(str(_render_value(item)) for item in value)
    return _render_value(value)


def _ask_town_hall(prompt):
    """Read citizen input, and survive politely when the room is empty."""
    try:
        return input(prompt)
    except EOFError:
        raise LakeOntarioInterpreterError(
            "the town hall emptied out before an answer arrived"
        ) from None
    except KeyboardInterrupt:
        raise LakeOntarioInterpreterError(
            "the citizen withdrew their question (Ctrl+C)"
        ) from None


class LakeOntarioInterpreter:
    def __init__(self, strict=False, trace=False, max_steps=None):
        self.variables = {}
        self.lines = []
        self.line_map = {}
        self.block_layout = BlockLayout()
        self.pc = 0
        self.call_stack = []
        self.strict = strict
        self.trace = trace
        self.max_steps = max_steps
        self.input_callback = None
        self.graphics_callbacks = {}
        self.sound_callbacks = {}
        self.current_line_number = None
        self.vote_records = []
        self.petition_signatures = []
        self.testimonies = []
        self.evidence_log = []

    def run_statement(self, statement):
        self.load_script(statement)
        self.run()

    def set_input_callback(self, callback):
        self.input_callback = callback

    def set_graphics_callbacks(self, callbacks):
        self.graphics_callbacks = callbacks or {}

    def set_sound_callbacks(self, callbacks):
        self.sound_callbacks = callbacks or {}

    def _play_tone(self, frequency, duration_ms):
        frequency = max(20.0, min(20000.0, float(frequency)))
        duration_ms = max(0.0, min(5000.0, float(duration_ms)))
        callback = self.sound_callbacks.get("tone")
        if callback:
            callback(frequency, duration_ms)
        else:
            play_tone_fallback(frequency, duration_ms)

    def load_script(self, code_str):
        raw_lines = code_str.splitlines()
        self.lines = []
        self.line_map = {}
        self.current_line_number = None

        for line in raw_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("EXCUSE_ME"):
                continue

            match = re.match(r"^(\d+)\s+(.*)$", stripped)
            if match:
                line_num = int(match.group(1))
                content = strip_inline_comment(match.group(2).strip())
                if not content:
                    continue
                self.line_map[line_num] = len(self.lines)
                self.lines.append((line_num, content))
            else:
                content = strip_inline_comment(stripped)
                if not content:
                    continue
                self.lines.append((None, content))

        self.block_layout = build_block_layout(self.lines)

    def evaluate_expression(self, expr):
        """Translate a Lake Ontario expression and evaluate it.

        String literals are masked *before* keyword rewriting so a phrase like
        "WEALTH_TAX is a deduction" stays intact. Any expression the evidence
        simply cannot support raises a clear error instead of quietly becoming
        a truthy ALTERNATIVE_FACT string.
        """
        expr = expr.strip()
        if not expr:
            return None

        literals = []

        def save_literal(match):
            literals.append(match.group(0))
            return f"__STR_{len(literals) - 1}__"

        masked = STRING_LITERAL_PATTERN.sub(save_literal, expr)

        masked = re.sub(r"\bCOLLECTIVE_LIST\s+(.+)", r"COLLECTIVE_LIST(\1)", masked)
        # bare COLLECTIVE_LIST with no args -> empty list
        masked = re.sub(r"\bCOLLECTIVE_LIST\b(?!\s*\()", "COLLECTIVE_LIST()", masked)
        masked = re.sub(
            r"\bMUTUAL_AID_REGISTRY\s+(.+)",
            r"MUTUAL_AID_REGISTRY(\1)",
            masked,
        )

        for keyword, replacement in EXPRESSION_KEYWORDS:
            masked = re.sub(
                rf"\b{keyword}\b", lambda _match, r=replacement: r, masked
            )

        def var_replacer(match):
            name = match.group(0)
            if name.startswith("__STR_"):
                return name
            if name in LO_RESERVED_NAMES:
                return name

            remaining = masked[match.end() :]
            if remaining.startswith("("):
                hint = suggest_correction(name, LO_BUILTINS)
                raise LakeOntarioInterpreterError(
                    f"unknown function '{name}'{hint}"
                )
            if masked.startswith("=", match.end()) and not masked.startswith(
                "==", match.end()
            ):
                return name
            if name in self.variables:
                val = self.variables[name]
                return repr(val) if isinstance(val, str) else str(val)
            if self.strict:
                raise LakeOntarioInterpreterError(
                    f"undeclared citizen '{name}'. HONEY_BADGER_MODE requires a "
                    "FACT_CHECK before anyone can cite it."
                )
            return "0"

        code = re.sub(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", var_replacer, masked)

        for idx, literal in enumerate(literals):
            try:
                value = ast.literal_eval(literal)
            except (SyntaxError, ValueError):
                value = literal[1:-1]
            code = code.replace(f"__STR_{idx}__", f"LOString({value!r})")

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", SyntaxWarning)
                return eval(code, LO_EVAL_GLOBALS)
        except SyntaxError as exc:
            raise LakeOntarioInterpreterError(
                f"'{expr}' could not be parsed ({exc.msg}). Check for a stray word "
                "or a missing operator."
            ) from None
        except ZeroDivisionError:
            raise LakeOntarioInterpreterError(
                f"'{expr}' divides by zero. Even EQUAL_PAY cannot split a budget "
                "into nothing."
            ) from None
        except RecursionError:
            raise LakeOntarioInterpreterError(
                f"'{expr}' nests too deeply for the committee to follow."
            ) from None
        except (NameError, TypeError, ValueError, AttributeError) as exc:
            raise LakeOntarioInterpreterError(
                f"'{expr}' did not survive scrutiny: {exc}"
            ) from None

    def run(self):
        self.pc = 0
        self._healthcare_stack = []
        self._loop_stack = []
        steps = 0

        while self.pc < len(self.lines):
            if self.max_steps is not None:
                steps += 1
                if steps > self.max_steps:
                    raise LakeOntarioRuntimeError(
                        f"the committee stopped the debate after {self.max_steps} "
                        "statements. A loop may be running forever; check the "
                        "COAST_TO_COAST or WHILE_CLASS_CONSCIOUS condition, or "
                        "raise the limit with --max-steps."
                    )
            line_number, stmt = self.lines[self.pc]
            self.current_line_number = line_number
            self.pc += 1

            if stmt.startswith("EXCUSE_ME"):
                continue

            if self.trace:
                tag = f"line {line_number}" if line_number is not None else "line ?"
                print(f"🧾 AUDIT TRAIL → {tag}: {stmt}")

            try:
                if not self._dispatch(stmt):
                    break
            except (
                LakeOntarioInterpreterError,
                OSError,
                ValueError,
                TypeError,
                ZeroDivisionError,
                SyntaxError,
                NameError,
            ) as e:
                if self._healthcare_stack:
                    opener_index = self._healthcare_stack.pop()
                    self.pc = self.block_layout.close_of(
                        opener_index, len(self.lines)
                    ) + 1
                else:
                    line_tag = (
                        f"Line {self.current_line_number}: "
                        if self.current_line_number is not None
                        else ""
                    )
                    raise LakeOntarioRuntimeError(f"{line_tag}{e}") from e

    def _dispatch(self, stmt):
        """Execute one statement. Returns False when the script should stop."""
        if stmt.startswith("LAND_ACKNOWLEDGEMENT "):
            land_name = self.evaluate_expression(_statement_arg(stmt))
            print(
                "🍁 LAND ACKNOWLEDGEMENT: Respectfully acknowledging "
                f"traditional territory of {land_name}. 🍁"
            )
        elif stmt == "HONEY_BADGER_MODE":
            self.strict = True
            print(
                "🦡 HONEY BADGER MODE ENGAGED: Fearless execution activated! "
                "Taking zero shit from MAGA spin, censorship, or "
                "intimidation! Undeclared names now face the evidence "
                "committee. 🦡"
            )
        elif stmt.startswith("HONEY_BADGER_DONT_CARE "):
            target = self.evaluate_expression(_statement_arg(stmt))
            print(
                f"🦡 HONEY BADGER DOESN'T GIVE A SHIT ABOUT: '{target}'! "
                "Moving forward with 100% fearlessness! ⚡"
            )
        elif stmt.startswith("BADGER_BITE "):
            target = self.evaluate_expression(_statement_arg(stmt))
            print(f"💥 BADGER BITE: {target} 💥")
        elif stmt.startswith("FAT_CATS_TAX "):
            amount = self.evaluate_expression(_statement_arg(stmt))
            print(fat_cats_tax(amount))
        elif stmt.startswith("DONUT_DIVIDEND "):
            amount = self.evaluate_expression(_statement_arg(stmt))
            print(donut_dividend(amount))
        elif stmt.startswith("NATIONAL_STOOGE "):
            msg = self.evaluate_expression(_statement_arg(stmt))
            print(national_stooge(msg))
        elif stmt.startswith("GREEN_NEW_DEAL "):
            goal = self.evaluate_expression(_statement_arg(stmt))
            print(green_new_deal(goal))
        elif stmt.startswith("RHETORICAL_QUESTION "):
            question = self.evaluate_expression(_statement_arg(stmt))
            print(rhetorical_question(question))
        elif stmt.startswith("LOONIE_LOOP "):
            count = self.evaluate_expression(_statement_arg(stmt))
            result = loonie_loop(count)
            print(result)
        elif stmt.startswith("SOCIAL_LICENSE "):
            license_name = self.evaluate_expression(_statement_arg(stmt))
            print(social_license(license_name))
        elif stmt.startswith("ELECTORATE_PULSE "):
            pulse = self.evaluate_expression(_statement_arg(stmt))
            print(electorate_pulse(pulse))
        elif stmt.startswith("HEAR_HEAR "):
            point = self.evaluate_expression(_statement_arg(stmt))
            print(f"👏 HEAR, HEAR: {point}! The chamber reluctantly agrees.")
        elif stmt.startswith("CITIZEN_PETITION "):
            petition = self.evaluate_expression(_statement_arg(stmt))
            print(
                f"📬 CITIZEN PETITION: {petition} — received, stamped, "
                "and sent to a very serious committee."
            )
        elif stmt.startswith("VOTE_RECORDED "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",", 2)]
            if len(args) != 3:
                raise LakeOntarioInterpreterError(
                    "VOTE_RECORDED requires voter, election, and choice"
                )
            voter, election, choice = (
                self.evaluate_expression(arg) for arg in args
            )
            self.vote_records.append(
                {"voter": voter, "election": election, "choice": choice}
            )
            print(
                f"🗳️ VOTE RECORDED: {voter} chose {choice} in {election}; "
                "the ballot has joined the extremely serious registry."
            )
        elif stmt.startswith("PETITION_SIGNATURE_COLLECTED "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",", 1)]
            if len(args) != 2:
                raise LakeOntarioInterpreterError(
                    "PETITION_SIGNATURE_COLLECTED requires name and petition"
                )
            name, petition = (self.evaluate_expression(arg) for arg in args)
            self.petition_signatures.append(
                {"name": name, "petition": petition}
            )
            print(
                f"📬 PETITION SIGNATURE: {name} signed {petition}; "
                "democracy has received another supporting document."
            )
        elif stmt.startswith("TESTIMONY_ADDED "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",", 1)]
            if len(args) != 2:
                raise LakeOntarioInterpreterError(
                    "TESTIMONY_ADDED requires witness and statement"
                )
            witness, statement = (
                self.evaluate_expression(arg) for arg in args
            )
            self.testimonies.append(
                {"witness": witness, "statement": statement}
            )
            print(
                f"📢 TESTIMONY ADDED: {witness} testified: {statement}; "
                "the inquiry has opened a fresh binder."
            )
        elif stmt == "MOTION_PASSED":
            print(
                "✅ MOTION PASSED: The public interest has defeated "
                "administrative fog, eh."
            )
        elif stmt == "NATIONAL_HEALTHCARE":
            self._healthcare_stack.append(self.pc - 1)
            print(
                "🏥 NATIONAL HEALTHCARE ENGAGED: Public safety net activated "
                "with honour and apologies."
            )
        elif stmt.startswith("FACT_CHECK "):
            body = _statement_arg(stmt)
            if "=" not in body:
                raise LakeOntarioInterpreterError(
                    "FACT_CHECK needs 'name = expression'"
                )
            var_name, val_expr = body.split("=", 1)
            var_name = var_name.strip()
            previous = self.variables.get(var_name, _UNSET)
            value = self.evaluate_expression(val_expr)
            self.variables[var_name] = value
            self._record_evidence(var_name, previous, value)
        elif stmt.startswith("BROADCAST_CBC "):
            val_expr = _statement_arg(stmt)
            val = self.evaluate_expression(val_expr)
            print(_render_broadcast(val))
        elif stmt.startswith("TOWN_HALL "):
            var_name = _statement_arg(stmt)
            if self.input_callback:
                user_val = self.input_callback(var_name)
            else:
                user_val = _ask_town_hall(
                    f"🇨🇦 Democratic Input for {var_name}: "
                )
            try:
                self.variables[var_name] = int(user_val)
            except ValueError:
                self.variables[var_name] = user_val
        elif stmt.startswith("INPUT_BOX "):
            var_name = _statement_arg(stmt)
            if self.input_callback:
                user_val = self.input_callback(
                    var_name, prompt_type="input_box"
                )
            else:
                user_val = _ask_town_hall(
                    f"🖥️ Input Box for {var_name}: "
                )
            try:
                self.variables[var_name] = int(user_val)
            except ValueError:
                self.variables[var_name] = user_val
        elif stmt == "SHOW_VARS":
            if not self.variables:
                print("📋 CITIZEN REGISTER: empty, like a quiet town hall.")
            else:
                print("📋 CITIZEN REGISTER:")
                for name, value in self.variables.items():
                    print(f"  {name} = {value}")
        elif stmt == "RESET_CITIZENS":
            self.variables.clear()
            self.vote_records.clear()
            self.petition_signatures.clear()
            self.testimonies.clear()
            self.evidence_log.clear()
            print(
                "🧹 CITIZEN REGISTER RESET: all values cleared, democracy restored to baseline."
            )
        elif stmt == "SHOW_EVIDENCE_LOG":
            self._print_evidence_log()
        elif stmt.startswith("PUBLISH_EVIDENCE_LOG "):
            path = str(self.evaluate_expression(_statement_arg(stmt)))
            if not path:
                raise LakeOntarioInterpreterError(
                    "PUBLISH_EVIDENCE_LOG requires a file path"
                )
            entries = len(self.evidence_log)
            try:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(self._evidence_log_text())
            except OSError as exc:
                raise LakeOntarioInterpreterError(
                    f"PUBLISH_EVIDENCE_LOG could not write '{path}': {exc}"
                ) from None
            print(
                f"📄 Evidence log published to {path} "
                f"({entries} entr{'y' if entries == 1 else 'ies'})."
            )
        elif stmt.startswith("FOR_EACH "):
            # FOR_EACH item IN collection
            body = _statement_arg(stmt)
            if " IN " not in body:
                raise LakeOntarioInterpreterError(
                    "FOR_EACH needs 'item IN collection'"
                )
            var_name, collection_expr = body.split(" IN ", 1)
            var_name = var_name.strip()
            collection = self.evaluate_expression(collection_expr.strip())
            if isinstance(collection, dict):
                raise LakeOntarioInterpreterError(
                    "FOR_EACH needs a collective; that value is a registry. "
                    "Try REGISTRY_KEYS(...) or REGISTRY_VALUES(...)."
                )
            if isinstance(collection, str):
                raise LakeOntarioInterpreterError(
                    "FOR_EACH needs a collective; that value is text. "
                    "Try STR_SPLIT(...) first."
                )
            if not isinstance(collection, (list, tuple)):
                raise LakeOntarioInterpreterError(
                    "FOR_EACH needs a collective, but that value is "
                    f"{type(collection).__name__}."
                )
            items = list(collection)
            if items:
                self.variables[var_name] = items[0]
                self._loop_stack.append(
                    {
                        "type": "foreach",
                        "var": var_name,
                        "items": items,
                        "index": 0,
                        "start_index": self.pc - 1,
                    }
                )
            else:
                self.pc = self.block_layout.close_of(
                    self.pc - 1, len(self.lines)
                ) + 1
        elif stmt == "END_EACH":
            if self._loop_stack and self._loop_stack[-1]["type"] == "foreach":
                top = self._loop_stack[-1]
                top["index"] += 1
                if top["index"] < len(top["items"]):
                    self.variables[top["var"]] = top["items"][top["index"]]
                    self.pc = top["start_index"] + 1
                else:
                    self._loop_stack.pop()
        elif stmt.startswith("APPEND_TO "):
            body = _statement_arg(stmt)
            if "," not in body:
                raise LakeOntarioInterpreterError(
                    "APPEND_TO must separate variable and value with a comma"
                )
            target_name, item_expr = body.split(",", 1)
            target_name = target_name.strip()
            item_value = self.evaluate_expression(item_expr.strip())
            if target_name not in self.variables:
                self.variables[target_name] = []
            if not isinstance(self.variables[target_name], list):
                self.variables[target_name] = [self.variables[target_name]]
            self.variables[target_name].append(item_value)
            print(f"📎 Appended to {target_name}: {item_value}")
        elif stmt.startswith("REMOVE_FROM "):
            body = _statement_arg(stmt)
            if "," not in body:
                raise LakeOntarioInterpreterError(
                    "REMOVE_FROM must separate variable and value with a comma"
                )
            target_name, item_expr = body.split(",", 1)
            target_name = target_name.strip()
            item_value = self.evaluate_expression(item_expr.strip())
            if target_name in self.variables and isinstance(
                self.variables[target_name], list
            ):
                try:
                    self.variables[target_name].remove(item_value)
                except ValueError:
                    print(
                        f"🗒️ REMOVE_FROM: {item_value} was not on the "
                        f"record for {target_name}, eh."
                    )
        elif stmt.startswith("SORT_CITIZENS "):
            var_name = _statement_arg(stmt)
            if var_name in self.variables:
                self.variables[var_name] = sort_citizens(
                    self.variables[var_name]
                )
                print(f"📊 Sorted {var_name}: {self.variables[var_name]}")
        elif stmt.startswith("AVERAGE_CITIZENS "):
            var_name = _statement_arg(stmt)
            if var_name in self.variables:
                avg = average_citizens(self.variables[var_name])
                self.variables[f"{var_name}_average"] = avg
                print(f"📈 Average of {var_name}: {avg}")
        elif stmt.startswith("SET_PEN_COLOR "):
            color_value = self.evaluate_expression(_statement_arg(stmt))
            callback = self.graphics_callbacks.get("pen_color")
            if callback:
                callback(color_value)
        elif stmt.startswith("SET_FILL_COLOR "):
            color_value = self.evaluate_expression(_statement_arg(stmt))
            callback = self.graphics_callbacks.get("fill_color")
            if callback:
                callback(color_value)
        elif stmt.startswith("SET_CANVAS_BG "):
            bg_value = self.evaluate_expression(_statement_arg(stmt))
            callback = self.graphics_callbacks.get("canvas_bg")
            if callback:
                callback(bg_value)
        elif stmt.startswith("FILL_RECTANGLE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 4:
                x = self.evaluate_expression(args[0])
                y = self.evaluate_expression(args[1])
                width = self.evaluate_expression(args[2])
                height = self.evaluate_expression(args[3])
                callback = self.graphics_callbacks.get("filled_rectangle")
                if callback:
                    callback(x, y, width, height)
        elif stmt.startswith("FILL_CIRCLE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 3:
                x = self.evaluate_expression(args[0])
                y = self.evaluate_expression(args[1])
                radius = self.evaluate_expression(args[2])
                callback = self.graphics_callbacks.get("filled_circle")
                if callback:
                    callback(x, y, radius)
        elif stmt.startswith("WAIT "):
            delay = float(self.evaluate_expression(_statement_arg(stmt)))
            time.sleep(min(max(delay / 1000.0, 0.0), 5.0))
        elif stmt.startswith("PUBLISH_RESEARCH_FILE "):
            body = _statement_arg(stmt)
            if "," not in body:
                raise LakeOntarioInterpreterError(
                    "PUBLISH_RESEARCH_FILE must separate path and content "
                    "with a comma"
                )
            path_expr, content_expr = body.split(",", 1)
            path = self.evaluate_expression(path_expr)
            content = self.evaluate_expression(content_expr)
            if not publish_research(path, content):
                raise LakeOntarioInterpreterError(
                    f"PUBLISH_RESEARCH_FILE could not write '{path}'. "
                    "The document was not published."
                )
            print(f"📄 Published research document to {path}")
        elif stmt == "CLEAR_GRAPHICS":
            callback = self.graphics_callbacks.get("clear")
            if callback:
                callback()
        elif stmt.startswith("DRAW_LINE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 4:
                x1 = self.evaluate_expression(args[0])
                y1 = self.evaluate_expression(args[1])
                x2 = self.evaluate_expression(args[2])
                y2 = self.evaluate_expression(args[3])
                callback = self.graphics_callbacks.get("line")
                if callback:
                    callback(x1, y1, x2, y2)
        elif stmt.startswith("DRAW_RECTANGLE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 4:
                x = self.evaluate_expression(args[0])
                y = self.evaluate_expression(args[1])
                width = self.evaluate_expression(args[2])
                height = self.evaluate_expression(args[3])
                callback = self.graphics_callbacks.get("rectangle")
                if callback:
                    callback(x, y, width, height)
        elif stmt.startswith("DRAW_CIRCLE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 3:
                x = self.evaluate_expression(args[0])
                y = self.evaluate_expression(args[1])
                radius = self.evaluate_expression(args[2])
                callback = self.graphics_callbacks.get("circle")
                if callback:
                    callback(x, y, radius)
        elif stmt.startswith("DRAW_TEXT "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",", 2)]
            if len(args) == 3:
                x = self.evaluate_expression(args[0])
                y = self.evaluate_expression(args[1])
                text = self.evaluate_expression(args[2])
                callback = self.graphics_callbacks.get("text")
                if callback:
                    callback(x, y, text)
        elif stmt.startswith("SET_PEN_WIDTH "):
            width_value = self.evaluate_expression(_statement_arg(stmt))
            callback = self.graphics_callbacks.get("pen_width")
            if callback:
                callback(width_value)
        elif stmt.startswith("DRAW_POINT "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 2:
                x = self.evaluate_expression(args[0])
                y = self.evaluate_expression(args[1])
                callback = self.graphics_callbacks.get("point")
                if callback:
                    callback(x, y)
        elif stmt.startswith("DRAW_OVAL "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 4:
                coords = [self.evaluate_expression(arg) for arg in args]
                callback = self.graphics_callbacks.get("oval")
                if callback:
                    callback(*coords)
        elif stmt.startswith("FILL_OVAL "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 4:
                coords = [self.evaluate_expression(arg) for arg in args]
                callback = self.graphics_callbacks.get("filled_oval")
                if callback:
                    callback(*coords)
        elif stmt.startswith("DRAW_ARC "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 5:
                x, y, radius, start, extent = (
                    self.evaluate_expression(arg) for arg in args
                )
                callback = self.graphics_callbacks.get("arc")
                if callback:
                    callback(x, y, radius, start, extent)
        elif stmt.startswith("DRAW_POLYGON "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) >= 6 and len(args) % 2 == 0:
                points = [self.evaluate_expression(arg) for arg in args]
                callback = self.graphics_callbacks.get("polygon")
                if callback:
                    callback(*points)
        elif stmt.startswith("FILL_POLYGON "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) >= 6 and len(args) % 2 == 0:
                points = [self.evaluate_expression(arg) for arg in args]
                callback = self.graphics_callbacks.get("filled_polygon")
                if callback:
                    callback(*points)
        elif stmt.startswith("DRAW_TRIANGLE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 6:
                points = [self.evaluate_expression(arg) for arg in args]
                callback = self.graphics_callbacks.get("triangle")
                if callback:
                    callback(*points)
        elif stmt.startswith("FILL_TRIANGLE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 6:
                points = [self.evaluate_expression(arg) for arg in args]
                callback = self.graphics_callbacks.get("filled_triangle")
                if callback:
                    callback(*points)
        elif stmt.startswith("PLAY_TONE "):
            args = [arg.strip() for arg in _statement_arg(stmt).split(",")]
            if len(args) == 2:
                frequency = self.evaluate_expression(args[0])
                duration_ms = self.evaluate_expression(args[1])
                self._play_tone(frequency, duration_ms)
        elif stmt.startswith("PLAY_SOUND_FILE "):
            path = self.evaluate_expression(_statement_arg(stmt))
            callback = self.sound_callbacks.get("file")
            if callback:
                callback(path)
            print(f"🔊 Playing sound file: {path}")
        elif stmt == "STOP_SOUND":
            callback = self.sound_callbacks.get("stop")
            if callback:
                callback()
        elif stmt == "HONEY_BADGER_GROWL":
            self._play_tone(110, 220)
            print("🦡 GRRRR! The Honey Badger growls — it don't care!")
        elif stmt == "TOWN_HALL_BELL":
            self._play_tone(880, 400)
            print("🔔 Order! Order! The Town Hall bell calls the room to order.")
        elif stmt == "STANDING_OVATION":
            for tone_frequency in (523, 659, 784, 1047):
                self._play_tone(tone_frequency, 120)
            print("👏 The gallery rises for a standing ovation!")
        elif stmt.startswith("PERHAPS "):
            cond_expr = _statement_arg(stmt).replace(
                " FACT_ESTABLISHED", ""
            ).strip()
            res = self.evaluate_expression(cond_expr)
            if not res:
                self.pc = self._next_perhaps_branch(self.pc - 1)
        elif stmt.startswith("PERHAPS_ALSO "):
            # Reached in sequence: an earlier branch already ran, so the
            # rest of the motion is out of order.
            self.pc = self._skip_to_block_end(self.pc - 1)
        elif stmt == "STILL_IN_DENIAL":
            self.pc = self._skip_to_block_end(self.pc - 1)
        elif stmt == "END_PERHAPS":
            pass
        elif stmt.startswith("COALITION "):
            subject = self.evaluate_expression(_statement_arg(stmt))
            self.pc = self._enter_coalition(subject, self.pc - 1)
        elif stmt.startswith("PLANK "):
            # Reached in sequence: an earlier plank already matched.
            self.pc = self._skip_to_block_end(self.pc - 1)
        elif stmt == "MINORITY_REPORT":
            self.pc = self._skip_to_block_end(self.pc - 1)
        elif stmt == "END_COALITION":
            pass
        elif stmt.startswith("WHILE_CLASS_CONSCIOUS "):
            cond_expr = _statement_arg(stmt)
            if self.evaluate_expression(cond_expr):
                self._loop_stack.append(
                    {
                        "type": "while",
                        "cond": cond_expr,
                        "start_index": self.pc - 1,
                    }
                )
            else:
                self.pc = self._skip_to_block_end(self.pc - 1)
        elif stmt == "CONTINUE_ORGANIZING":
            if self._loop_stack and self._loop_stack[-1]["type"] == "while":
                top = self._loop_stack[-1]
                if self.evaluate_expression(top["cond"]):
                    self.pc = top["start_index"] + 1
                else:
                    self._loop_stack.pop()
        elif stmt == "UNIVERSAL_HEALTHCARE":
            self._healthcare_stack.append(self.pc - 1)
        elif stmt == "EXECUTIVE_ORDER_BLOCKED":
            if self._healthcare_stack:
                self._healthcare_stack.pop()
        elif stmt.startswith("COAST_TO_COAST "):
            loop_def = _statement_arg(stmt)
            step_val = 1
            if " STEP " in loop_def:
                loop_def, step_expr = loop_def.split(" STEP ")
                step_val = self.evaluate_expression(step_expr)
            if " UP_TO " not in loop_def:
                raise LakeOntarioInterpreterError(
                    "COAST_TO_COAST needs 'var = start UP_TO end'"
                )
            var_part, range_part = loop_def.split(" UP_TO ", 1)
            if "=" not in var_part:
                raise LakeOntarioInterpreterError(
                    "COAST_TO_COAST needs 'var = start UP_TO end'"
                )
            if not step_val:
                raise LakeOntarioInterpreterError(
                    "STEP 0 would march in place forever. The committee "
                    "recommends a step that actually moves."
                )
            var_name, start_expr = var_part.split("=", 1)
            var_name = var_name.strip()
            start_val = self.evaluate_expression(start_expr)
            end_val = self.evaluate_expression(range_part)
            self.variables[var_name] = start_val
            self._loop_stack.append(
                {
                    "type": "for",
                    "var": var_name,
                    "end": end_val,
                    "step": step_val,
                    "start_index": self.pc - 1,
                }
            )
        elif stmt == "THANK_YOU_EH":
            if self._loop_stack and self._loop_stack[-1]["type"] == "for":
                top = self._loop_stack[-1]
                current_val = self.variables[top["var"]] + top["step"]
                if (top["step"] > 0 and current_val <= top["end"]) or (
                    top["step"] < 0 and current_val >= top["end"]
                ):
                    self.variables[top["var"]] = current_val
                    self.pc = top["start_index"] + 1
                else:
                    self._loop_stack.pop()
        elif stmt == "BREAK_FROM_CAUCUS":
            if self._loop_stack:
                top = self._loop_stack.pop()
                self.pc = self.block_layout.close_of(
                    top["start_index"], len(self.lines)
                ) + 1
        elif stmt == "NEXT_MOTION":
            if self._loop_stack:
                top = self._loop_stack[-1]
                if top["type"] == "for":
                    current_val = self.variables[top["var"]] + top["step"]
                    if (top["step"] > 0 and current_val <= top["end"]) or (
                        top["step"] < 0 and current_val >= top["end"]
                    ):
                        self.variables[top["var"]] = current_val
                        self.pc = top["start_index"] + 1
                    else:
                        self._loop_stack.pop()
                elif top["type"] == "while":
                    if self.evaluate_expression(top["cond"]):
                        self.pc = top["start_index"] + 1
                    else:
                        self._loop_stack.pop()
                elif top["type"] == "foreach":
                    top["index"] += 1
                    if top["index"] < len(top["items"]):
                        self.variables[top["var"]] = top["items"][top["index"]]
                        self.pc = top["start_index"] + 1
                    else:
                        self._loop_stack.pop()
                        # step past END_EACH; the loop is over
                        self.pc = self.block_layout.close_of(
                            top["start_index"], len(self.lines)
                        ) + 1
        elif stmt.startswith("SUBPOENA "):
            target_text = _statement_arg(stmt)
            if not target_text.lstrip("-").isdigit():
                raise LakeOntarioInterpreterError(
                    "SUBPOENA must target a numbered line"
                )
            target = int(target_text)
            if target in self.line_map:
                self.call_stack.append(self.pc)
                self.pc = self.line_map[target]
            else:
                print(f"Subpoena Error: Line {target} ignored subpoena!")
        elif stmt == "RETURN_TO_OTTAWA":
            if self.call_stack:
                self.pc = self.call_stack.pop()
            else:
                print("Error: RETURN_TO_OTTAWA with empty call stack, eh!")
        elif stmt.startswith("GOLF_VACATION "):
            seconds = self.evaluate_expression(_statement_arg(stmt))
            try:
                sec = float(seconds)
            except (TypeError, ValueError):
                raise LakeOntarioInterpreterError(
                    "GOLF_VACATION requires a numeric number of seconds"
                ) from None
            print(f"⛳ Executive on Golf Vacation for {sec} seconds...")
            time.sleep(min(sec, 2.0))
        elif stmt.startswith("CLIMATE_EMERGENCY "):
            msg = self.evaluate_expression(_statement_arg(stmt))
            raise LakeOntarioInterpreterError(
                f"CLIMATE EMERGENCY RAISED: {msg}"
            )
        elif stmt == "IMPEACH":
            print("🏛️ IMPEACHMENT EFFECTIVE: Program terminated cleanly.")
            return False
        else:
            head = stmt.split()[0] if stmt.split() else stmt
            if head in KNOWN_KEYWORD_NAMES:
                raise LakeOntarioInterpreterError(
                    f"{head} requires an argument"
                )
            raise LakeOntarioInterpreterError(
                f"unsupported statement '{head}'"
            )
        return True

    def _skip_to_block_end(self, marker_index):
        """Jump past the END marker of the block that owns this index."""
        opener_index = self.block_layout.owner.get(marker_index)
        if opener_index is None:
            opener_index = marker_index
        return self.block_layout.close_of(opener_index, len(self.lines)) + 1

    def _record_evidence(self, name, previous, value):
        """Journal every FACT_CHECK, flagging amendments to earlier evidence."""
        self.evidence_log.append(
            {
                "line": self.current_line_number,
                "name": name,
                "previous": None if previous is _UNSET else previous,
                "value": value,
                "amended": previous is not _UNSET and previous != value,
            }
        )
        if len(self.evidence_log) > EVIDENCE_LOG_LIMIT:
            del self.evidence_log[0]

    def _evidence_log_lines(self):
        lines = []
        for entry in self.evidence_log:
            line_tag = f"line {entry['line']}" if entry["line"] is not None else "line ?"
            record = f"{line_tag}: {entry['name']} = {entry['value']}"
            if entry["amended"]:
                record += f" (amended; was {entry['previous']})"
            lines.append(record)
        return lines

    def _evidence_log_text(self):
        header = ["Lake Ontario BASIC evidence log", "-" * 32]
        return "\n".join(header + self._evidence_log_lines()) + "\n"

    def _print_evidence_log(self):
        if not self.evidence_log:
            print(
                "🧾 EVIDENCE LOG: empty, like a committee that has not yet met."
            )
            return
        count = len(self.evidence_log)
        print(f"🧾 EVIDENCE LOG: {count} entr{'y' if count == 1 else 'ies'} on record")
        for record in self._evidence_log_lines():
            print(f"  {record}")

    def _enter_coalition(self, subject, opener_index):
        """Run the first PLANK that matches, else MINORITY_REPORT, else skip."""
        for marker, index in self.block_layout.branches.get(opener_index, []):
            if marker == "MINORITY_REPORT":
                return index + 1
            if self._plank_matches(subject, self.lines[index][1]):
                return index + 1
        return self.block_layout.close_of(opener_index, len(self.lines)) + 1

    def _plank_matches(self, subject, plank_stmt):
        argument = _statement_arg(plank_stmt)
        for operator in COMPARISON_OPERATORS:
            if not argument.startswith(operator):
                continue
            target = self.evaluate_expression(argument[len(operator) :])
            try:
                return _compare_values(subject, target, operator)
            except TypeError:
                raise LakeOntarioInterpreterError(
                    f"PLANK {argument} cannot be compared with "
                    f"{type(subject).__name__} value {subject!r}"
                ) from None
        return subject == self.evaluate_expression(argument)

    def _next_perhaps_branch(self, opener_index):
        """Resolve a failed PERHAPS: next PERHAPS_ALSO, the else branch, or the end."""
        for marker, index in self.block_layout.branches.get(opener_index, []):
            if marker == "STILL_IN_DENIAL":
                return index + 1
            condition = (
                self.lines[index][1][len("PERHAPS_ALSO ") :]
                .replace(" FACT_ESTABLISHED", "")
                .strip()
            )
            if self.evaluate_expression(condition):
                return index + 1
        return self.block_layout.close_of(opener_index, len(self.lines)) + 1


def _check_perhaps_condition(label, keyword, stmt):
    condition = _statement_arg(stmt)
    if not condition:
        return [f"{label}: {keyword} requires a condition"]
    if " FACT_ESTABLISHED" not in condition:
        return [
            f"{label}: {keyword} requires 'FACT_ESTABLISHED' after the condition, "
            f"e.g. '{keyword} x >= 1 FACT_ESTABLISHED'"
        ]
    if _uses_assignment_instead_of_equality(condition):
        suggestion = condition.replace(" FACT_ESTABLISHED", "").replace("=", "==", 1)
        return [
            f"{label}: {keyword} assigns with '='. Use '==' to compare, e.g. "
            f"'{keyword} {suggestion} FACT_ESTABLISHED'"
        ]
    return []


def _uses_assignment_instead_of_equality(stmt):
    """True for 'PLANK = 5' (or a PERHAPS condition) where '==' was meant."""
    masked = mask_string_literals(_statement_arg(stmt))
    return bool(re.search(r"(^|[^=!<>])=(?!=)", masked))


def _check_statement_shape(label, stmt):
    """Line-level checks that only need the statement text."""
    problems = []

    if stmt.startswith("FACT_CHECK"):
        if "=" not in stmt:
            problems.append(f"{label}: FACT_CHECK statement must include '='")
        elif not stmt.split("=", 1)[1].strip():
            problems.append(f"{label}: FACT_CHECK assignment is missing a value")
    elif stmt.startswith("PERHAPS_ALSO"):
        problems.extend(_check_perhaps_condition(label, "PERHAPS_ALSO", stmt))
    elif stmt.startswith("PERHAPS "):
        problems.extend(_check_perhaps_condition(label, "PERHAPS", stmt))
    elif stmt.startswith("PLANK ") and _uses_assignment_instead_of_equality(stmt):
        problems.append(
            f"{label}: PLANK assigns with '='. Use '==' to compare, e.g. "
            "'PLANK == 5'."
        )
    elif stmt.startswith("COAST_TO_COAST"):
        if " UP_TO " not in stmt:
            problems.append(f"{label}: COAST_TO_COAST statement must include 'UP_TO'")
        else:
            header, _, step_text = stmt.partition(" STEP ")
            if "=" not in header:
                problems.append(
                    f"{label}: COAST_TO_COAST needs 'var = start UP_TO end'"
                )
            if step_text and re.fullmatch(r"0+(\.0*)?", step_text.strip()):
                problems.append(
                    f"{label}: STEP 0 would march in place forever. The committee "
                    "recommends a step that actually moves."
                )
    elif stmt.startswith("PUBLISH_RESEARCH_FILE") and "," not in stmt:
        problems.append(
            f"{label}: PUBLISH_RESEARCH_FILE must separate path and content "
            "with a comma"
        )
    elif stmt.startswith("SUBPOENA"):
        if not _statement_arg(stmt).isdigit():
            problems.append(f"{label}: SUBPOENA must target a numbered line")
    elif stmt.startswith("GOLF_VACATION"):
        try:
            float(_statement_arg(stmt))
        except ValueError:
            problems.append(f"{label}: GOLF_VACATION requires a numeric value")
    elif stmt.startswith("CLIMATE_EMERGENCY"):
        if not _statement_arg(stmt):
            problems.append(f"{label}: CLIMATE_EMERGENCY requires a message")
    elif stmt.startswith("TOWN_HALL ") and not _statement_arg(stmt):
        problems.append(f"{label}: TOWN_HALL requires a variable name")
    elif stmt.startswith("INPUT_BOX ") and not _statement_arg(stmt):
        problems.append(f"{label}: INPUT_BOX requires a variable name")
    elif stmt.startswith("FOR_EACH ") and " IN " not in stmt:
        problems.append(f"{label}: FOR_EACH statement must include 'IN'")
    elif stmt.startswith("APPEND_TO") and "," not in stmt:
        problems.append(
            f"{label}: APPEND_TO must separate variable and value with a comma"
        )
    elif stmt.startswith("REMOVE_FROM") and "," not in stmt:
        problems.append(
            f"{label}: REMOVE_FROM must separate variable and value with a comma"
        )

    for name in find_function_calls(stmt):
        if name in LO_BUILTINS or name == "LOString":
            continue
        problems.append(
            f"{label}: unknown function '{name}'"
            f"{suggest_correction(name, LO_BUILTINS)}"
        )

    return problems


def validate_script(code):
    """Statically audit a script, returning the errors that block execution."""
    errors, _warnings = analyze_script(code)
    return errors


def analyze_script(code):
    """Audit a script and return (errors, warnings).

    Errors stop execution. Warnings are advisory notes, such as a PLANK that an
    earlier PLANK already outranks and can therefore never match.
    """
    errors = []
    parsed = []
    seen_line_numbers = set()

    for raw_line in code.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("EXCUSE_ME"):
            continue

        match = re.match(r"^(\d+)\s+(.*)$", stripped)
        if match:
            line_number = int(match.group(1))
            if line_number in seen_line_numbers:
                errors.append(f"Line {line_number}: duplicate line number")
            seen_line_numbers.add(line_number)
            stmt = strip_inline_comment(match.group(2).strip())
        else:
            line_number = None
            stmt = strip_inline_comment(stripped)

        if not stmt or stmt.startswith("EXCUSE_ME"):
            continue

        parsed.append((line_number, stmt))

    for line_number, stmt in parsed:
        label = _line_label(line_number)
        if not is_supported_statement(stmt):
            head = stmt.split()[0] if stmt.split() else stmt
            if head in KNOWN_KEYWORD_NAMES:
                errors.append(f"{label}: {head} requires an argument")
            else:
                errors.append(
                    f"{label}: unsupported statement '{head}'"
                    f"{suggest_correction(head, KNOWN_STATEMENT_NAMES)}"
                )
            continue
        errors.extend(_check_statement_shape(label, stmt))

    layout = build_block_layout(parsed)
    errors.extend(layout.problems)
    errors.sort(key=_validation_sort_key)

    warnings = list(layout.warnings)
    if parsed and not any(
        stmt.startswith("LAND_ACKNOWLEDGEMENT ") for _line, stmt in parsed
    ):
        warnings.append(
            "the record does not open with LAND_ACKNOWLEDGEMENT; "
            "polite scripts usually do."
        )
    warnings.sort(key=_validation_sort_key)
    return errors, warnings


def _validation_sort_key(message):
    match = re.match(r"Line (\d+)", message)
    return int(match.group(1)) if match else -1


def get_repl_history_path():
    return os.environ.get(
        "LAKE_ONTARIO_REPL_HISTORY", os.path.join(os.getcwd(), ".lake_ontario_history")
    )


def load_repl_history(path):
    if not path or not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            lines = [line.rstrip("\n") for line in handle if line.strip()]
        return lines[-20:]
    except OSError:
        return []


def save_repl_history(path, history):
    if not path:
        return
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            for entry in history:
                handle.write(f"{entry}\n")
    except OSError:
        pass


def print_repl_help():
    print("Lake Ontario BASIC REPL commands:")
    print("  HELP                 Show this help message")
    print("  HISTORY              Show recent REPL commands")
    print("  REPLAY N             Replay a numbered REPL command")
    print("  !N                  Shortcut replay command")
    print("  SHOW_VARS            Display the current variable registry")
    print("  SHOW_EVIDENCE_LOG    Display the FACT_CHECK evidence journal")
    print("  RUN path.lo          Validate and run a script in this session")
    print("  CHECK path.lo        Validate a script without running it")
    print("  SAVE path.lo         Write this session as a runnable script")
    print("  RESET / CLEAR        Clear all variables")
    print("  RESET_CITIZENS       Clear all variables")
    print("  IMPEACH / EXIT / QUIT  Exit the REPL")
    print("  CANCEL               Discard an unfinished multi-line block")
    print("  PERHAPS condition FACT_ESTABLISHED")
    print("  STILL_IN_DENIAL      Else branch in a PERHAPS block")
    print("  END_PERHAPS          Close a PERHAPS block")
    print("  COALITION expression")
    print("  PLANK value          Branch matched by equality or comparison")
    print("  MINORITY_REPORT      Default COALITION branch")
    print("  END_COALITION        Close a COALITION block")
    print("  COAST_TO_COAST var = start UP_TO end [STEP step]")
    print("  THANK_YOU_EH         Close a FOR loop")
    print("  FOR_EACH item IN list")
    print("  END_EACH             Close a FOR_EACH loop")
    print()
    print("Tab completion covers keywords and built-ins.")
    print()
    print("Example:")
    print("  FACT_CHECK total = 2 EQUAL_PAY 3")
    print("  BROADCAST_CBC total")
    print("  RUN examples/hello.lo")


REPL_FILE_COMMANDS = {"RUN", "CHECK", "SAVE"}

REPL_ONLY_COMMANDS = {
    "HELP",
    "?",
    "HISTORY",
    "REPLAY",
    "RESET",
    "CLEAR",
    "RESET_CITIZENS",
    "CANCEL",
    "EXIT",
    "QUIT",
    "IMPEACH",
} | REPL_FILE_COMMANDS


def _setup_repl_readline():
    """Give the REPL arrow-key history and Tab completion when a terminal allows it."""
    if readline is None or not sys.stdin.isatty():
        return

    completions = sorted(
        set(KNOWN_STATEMENT_NAMES)
        | set(LO_BUILTINS)
        | REPL_ONLY_COMMANDS
        | {"EVIDENCE_BASED", "ALTERNATIVE_FACT", "CLASSIFIED_MAR_A_LAGO"}
    )

    def completer(text, state):
        matches = [word for word in completions if word.startswith(text.upper())]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")


def _is_script_statement(entry):
    if entry.startswith("!"):
        return False
    return entry.split(" ", 1)[0].upper() not in REPL_ONLY_COMMANDS


def _save_repl_session(path, history):
    entries = [entry for entry in history if _is_script_statement(entry)]
    if not entries:
        print("🚨 REPL ERROR: nothing to save yet, eh.")
        return
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(entries) + "\n")
    except OSError as exc:
        print(f"🚨 REPL ERROR: could not save {path}: {exc}")
        return
    print(f"💾 Saved {len(entries)} statement(s) to {path}")


def _handle_repl_file_command(statement, interpreter, history):
    """Handle RUN / CHECK / SAVE. Returns True when the input was consumed."""
    keyword, _, argument = statement.partition(" ")
    keyword = keyword.upper()
    if keyword not in REPL_FILE_COMMANDS:
        return False

    argument = argument.strip()
    if not argument:
        print(f"🚨 REPL ERROR: {keyword} needs a file path")
        return True

    if keyword == "SAVE":
        _save_repl_session(argument, history)
        return True

    code = _read_script(argument)
    if code is None:
        return True

    errors, warnings = analyze_script(code)
    _report_validation_warnings(warnings)
    if errors:
        for error in errors:
            print(error)
        return True

    if keyword == "CHECK":
        print(f"📜 {argument} validated. The record holds, eh.")
        return True

    print(f"▶ Running {argument}...")
    interpreter.load_script(code)
    try:
        interpreter.run()
    except LakeOntarioRuntimeError as exc:
        print(f"🚨 REPL ERROR: {exc}")
    return True


def run_repl(trace=False, strict=False, max_steps=None):
    interpreter = LakeOntarioInterpreter(
        strict=strict, trace=trace, max_steps=max_steps
    )
    history_path = get_repl_history_path()
    history = load_repl_history(history_path)
    print("Lake Ontario BASIC REPL")
    print("Type statements and press Enter. Type IMPEACH or EXIT to quit.")
    print("For multi-line blocks, finish with END_PERHAPS / THANK_YOU_EH / END_EACH.")
    print("Type CANCEL to discard an incomplete block. Type HELP for commands.\n")

    _setup_repl_readline()

    buffer = []
    block_depth = 0

    while True:
        try:
            prompt = "....> " if buffer else "lo> "
            statement = input(prompt)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            if buffer:
                buffer = []
                block_depth = 0
                print("\nIncomplete block discarded.")
                continue
            print("\nGoodbye from Lake Ontario BASIC.")
            break

        statement = statement.strip()
        if not statement:
            continue

        upper = statement.upper()
        if not buffer and upper in {"HELP", "?"}:
            print_repl_help()
            continue
        if not buffer and upper == "HISTORY":
            if not history:
                print("REPL history is empty.")
            else:
                print("REPL history:")
                for index, entry in enumerate(history, 1):
                    print(f"  {index}. {entry}")
            continue
        if not buffer and upper.startswith("REPLAY "):
            try:
                replay_index = int(upper.split(None, 1)[1].strip())
            except ValueError:
                print("🚨 REPL ERROR: use REPLAY N or !N to replay a numbered command")
                continue
            if not 1 <= replay_index <= len(history):
                print(f"🚨 REPL ERROR: no history entry for REPLAY {replay_index}")
                continue
            statement = history[replay_index - 1]
            print(f"↩ replaying: {statement}")
            upper = statement.upper()
        if not buffer and upper in {"RESET", "CLEAR"}:
            interpreter.variables.clear()
            history.clear()
            save_repl_history(history_path, history)
            print("🧹 REPL state reset: all variables cleared.")
            print("📜 REPL history cleared.")
            continue
        if not buffer and upper == "RESET_CITIZENS":
            interpreter.variables.clear()
            history.clear()
            save_repl_history(history_path, history)
            print("🧹 REPL state reset: all variables cleared.")
            print("📜 REPL history cleared.")
            continue
        if not buffer and upper.startswith("!"):
            try:
                replay_index = int(upper[1:])
            except ValueError:
                print("🚨 REPL ERROR: use !N to replay a numbered command, e.g. !1")
                continue
            if not 1 <= replay_index <= len(history):
                print(f"🚨 REPL ERROR: no history entry for !{replay_index}")
                continue
            statement = history[replay_index - 1]
            print(f"↩ replaying: {statement}")
            upper = statement.upper()
        if not buffer and _handle_repl_file_command(statement, interpreter, history):
            continue
        if not buffer and upper in {"IMPEACH", "EXIT", "QUIT"}:
            print("Goodbye from Lake Ontario BASIC.")
            break
        if buffer and upper == "CANCEL":
            buffer = []
            block_depth = 0
            print("Incomplete block discarded.")
            continue

        if not buffer:
            history.append(statement)
            if len(history) > 20:
                history.pop(0)
            save_repl_history(history_path, history)

        buffer.append(statement)
        block_depth += repl_block_delta(statement)

        if block_depth > 0:
            continue
        if block_depth < 0:
            print("🚨 REPL ERROR: unmatched block terminator")
            buffer = []
            block_depth = 0
            continue

        script = "\n".join(buffer)
        buffer = []
        block_depth = 0

        try:
            interpreter.load_script(script)
            interpreter.run()
        except KeyboardInterrupt:
            print("\n🏛️ Statement interrupted. The register is unchanged, eh.")
            continue
        except SystemExit as exc:
            if exc.code == 0:
                break
            # Runtime error already printed by run(); preserve variables across reset
            saved_vars = interpreter.variables.copy()
            interpreter = LakeOntarioInterpreter(
                strict=strict, trace=trace, max_steps=max_steps
            )
            interpreter.variables = saved_vars
        except (
            LakeOntarioInterpreterError,
            OSError,
            ValueError,
            TypeError,
            ZeroDivisionError,
            SyntaxError,
            NameError,
        ) as exc:
            print(f"🚨 REPL ERROR: {exc}")


def resource_dir(name):
    """Locate a bundled resource directory in the checkout or an installed package."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, name)]
    try:
        import sysconfig

        data_root = sysconfig.get_path("data")
    except (ImportError, KeyError):  # pragma: no cover - exotic install schemes
        data_root = None
    if data_root:
        candidates.append(os.path.join(data_root, "share", "lake-ontario-basic", name))
        candidates.append(
            os.path.join(data_root, "lake-ontario-basic", name)
        )
    for candidate in candidates:
        if os.path.isdir(candidate):
            return candidate
    return candidates[0]


def resource_file(name):
    """Locate a bundled resource file (for example COMMANDS.md)."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, name)]
    try:
        import sysconfig

        data_root = sysconfig.get_path("data")
    except (ImportError, KeyError):  # pragma: no cover - exotic install schemes
        data_root = None
    if data_root:
        candidates.append(os.path.join(data_root, "share", "lake-ontario-basic", name))
        candidates.append(os.path.join(data_root, "lake-ontario-basic", name))
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return candidates[0]


def list_example_scripts():
    examples_dir = resource_dir("examples")
    if not os.path.isdir(examples_dir):
        print("No example scripts found.")
        return

    files = sorted(
        entry.name
        for entry in os.scandir(examples_dir)
        if entry.is_file() and entry.name.endswith(".lo")
    )
    if not files:
        print("No example scripts found.")
        return

    print("Available Lake Ontario BASIC example scripts:")
    for name in files:
        print(f"  - {name}")


def _example_path(example_name):
    examples_dir = resource_dir("examples")
    candidate = example_name
    if not candidate.endswith(".lo"):
        candidate = f"{candidate}.lo"
    return os.path.join(examples_dir, candidate)


def _read_script(path):
    if not os.path.isfile(path):
        print(f"Script not found: {path}")
        return None
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            return handle.read()
    except OSError as exc:
        print(f"Unable to read script: {exc}")
        return None


def _report_validation_errors(errors):
    for error in errors:
        print(error)
    print(
        "🚨 Validation failed: the motion cannot proceed until the record is "
        "corrected."
    )


def _execute(code, trace=False, strict=False, max_steps=None):
    """Run validated code and translate runtime failures into an exit code."""
    interpreter = LakeOntarioInterpreter(
        strict=strict, trace=trace, max_steps=max_steps
    )
    interpreter.load_script(code)
    try:
        interpreter.run()
    except LakeOntarioRuntimeError as exc:
        print(f"🚨 UNHANDLED DISASTER: {exc}")
        return 1
    except KeyboardInterrupt:
        print(
            "\n🏛️ Session prorogued: Ctrl+C ended the reading. "
            "Motion adjourned, eh."
        )
        return 130
    return 0


def _report_validation_warnings(warnings):
    for warning in warnings:
        print(f"⚠️  ADVISORY {warning}")


def check_script_file(script_path):
    code = _read_script(script_path)
    if code is None:
        return 1

    errors, warnings = analyze_script(code)
    _report_validation_warnings(warnings)
    if errors:
        _report_validation_errors(errors)
        return 1

    print(f"Validation passed for {script_path}")
    return 0


def run_script_file(script_path, trace=False, strict=False, max_steps=None):
    code = _read_script(script_path)
    if code is None:
        return 1

    errors = validate_script(code)
    if errors:
        _report_validation_errors(errors)
        return 1

    return _execute(code, trace=trace, strict=strict, max_steps=max_steps)


def run_example_script(example_name, trace=False, strict=False, max_steps=None):
    script_path = _example_path(example_name)
    if not os.path.isfile(script_path):
        print(f"Example script not found: {example_name}")
        return 1
    return run_script_file(script_path, trace=trace, strict=strict, max_steps=max_steps)


def print_usage():
    print(
        "Usage: python3 interpreter.py [--trace] [--strict] [--max-steps N] "
        "[--repl | -i] [--check script.lo] [--list-examples] "
        "[--run-example example.lo] [--doctor] [--version] [script.lo]"
    )
    print()
    print("Examples:")
    print("  python3 interpreter.py examples/hello.lo")
    print("  python3 interpreter.py --trace examples/hello.lo")
    print("  python3 interpreter.py --repl")
    print("  python3 interpreter.py --check examples/hello.lo")
    print("  python3 interpreter.py --list-examples")
    print("  python3 interpreter.py --run-example hello")
    print("  python3 interpreter.py --doctor")
    print("  python3 interpreter.py --doctor --strict")
    print("  python3 interpreter.py --version")
    print("  python3 interpreter.py -i")
    print()
    print("The interpreter reads Lake Ontario BASIC scripts and supports an")
    print("interactive REPL for quick experimentation.")
    print()
    print("  --trace   print an AUDIT TRAIL line before every executed statement")
    print("  --strict  start in HONEY_BADGER_MODE (undeclared names face the committee)")
    print("  --max-steps N  stop after N statements (guards against runaway loops)")


def run_environment_doctor(strict=False):
    python_version = sys.version.split()[0]
    venv_mode = (
        "yes" if sys.prefix != sys.base_prefix or "VIRTUAL_ENV" in os.environ else "no"
    )
    tkinter_status = "ok" if tkinter is not None else "missing"

    example_count = 0
    examples_dir = resource_dir("examples")
    try:
        example_count = len(
            [name for name in os.listdir(examples_dir) if name.endswith(".lo")]
        )
    except OSError:
        example_count = 0

    print(f"Python: {python_version}")
    print(f"Virtual environment: {venv_mode}")
    print(f"Tkinter: {tkinter_status}")
    print(f"Example scripts: {example_count}")

    if tkinter is None:
        print(
            "Tkinter is missing. The CLI, REPL, and every example still run; the "
            "GUI IDE and tone playback fall back to polite text. Install "
            "python3-tk when you want the full experience."
        )
        if strict:
            print("Environment check failed: --strict requires tkinter.")
            return 1

    print("Environment OK")
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    trace = "--trace" in args
    strict = "--strict" in args
    args = [arg for arg in args if arg not in {"--trace", "--strict"}]

    max_steps = None
    if "--max-steps" in args:
        index = args.index("--max-steps")
        try:
            max_steps = int(args[index + 1])
        except (IndexError, ValueError):
            print("🚨 --max-steps needs a whole number of statements, e.g. "
                  "--max-steps 100000")
            return 1
        if max_steps <= 0:
            print("🚨 --max-steps must be greater than zero.")
            return 1
        del args[index : index + 2]

    if not args:
        run_repl(trace=trace, strict=strict, max_steps=max_steps)
        return 0

    command = args[0]

    if command in {"-h", "--help", "help"}:
        print_usage()
        return 0

    if command in {"--version", "-V"}:
        print(f"Lake Ontario BASIC {__version__}")
        return 0

    if command == "--doctor":
        return run_environment_doctor(strict=strict)

    if command == "--list-examples":
        if len(args) != 1:
            print_usage()
            return 1
        list_example_scripts()
        return 0

    if command == "--run-example":
        if len(args) != 2:
            print_usage()
            return 1
        return run_example_script(
            args[1], trace=trace, strict=strict, max_steps=max_steps
        )

    if command in {"--repl", "-i"}:
        run_repl(trace=trace, strict=strict, max_steps=max_steps)
        return 0

    if command == "--check":
        if len(args) != 2:
            print_usage()
            return 1
        return check_script_file(args[1])

    if len(args) != 1:
        print_usage()
        return 1

    return run_script_file(
        args[0], trace=trace, strict=strict, max_steps=max_steps
    )


if __name__ == "__main__":
    sys.exit(main())
