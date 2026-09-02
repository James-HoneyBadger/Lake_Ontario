#!/usr/bin/env python3
"""
Lake Ontario BASIC Interpreter
A fully featured, practical programming language interpreter inspired by classic BASIC,
infused with Canadian politeness & Honey Badger attitude, pro-science, pro-health care,
pro-diversity, pro-socialism, and anti-MAGA.
"""

import math
import os
import random
import re
import sys
import time

try:
    import tkinter
except ImportError:  # pragma: no cover - dependency may be absent in headless envs
    tkinter = None

__version__ = "0.1.0"


class LakeOntarioInterpreterError(Exception):
    """Custom exception type for interpreter runtime errors."""


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
    try:
        with open(str(filepath).strip("\"'"), "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, TypeError, ValueError) as e:
        return f"ALTERNATIVE_FACT (Cannot read resource: {e})"


def publish_research(filepath, content):
    try:
        with open(str(filepath).strip("\"'"), "w", encoding="utf-8") as f:
            f.write(str(content))
        return True
    except (OSError, TypeError, ValueError):
        return False


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
    return sorted(items, key=lambda v: float(v) if isinstance(v, (int, float)) else str(v))


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


class LakeOntarioInterpreter:
    def __init__(self):
        self.variables = {}
        self.lines = []
        self.line_map = {}
        self.pc = 0
        self.call_stack = []
        self.custom_builtins = {}
        self.input_callback = None
        self.graphics_callbacks = {}
        self.current_line_number = None

    def run_statement(self, statement):
        self.load_script(statement)
        self.run()

    def set_input_callback(self, callback):
        self.input_callback = callback

    def set_graphics_callbacks(self, callbacks):
        self.graphics_callbacks = callbacks or {}

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
                content = match.group(2).strip()
                self.line_map[line_num] = len(self.lines)
                self.lines.append((line_num, content))
            else:
                self.lines.append((None, stripped))

    def evaluate_expression(self, expr):
        expr = expr.strip()
        if not expr:
            return None

        expr = re.sub(r"\bCOLLECTIVE_LIST\s+(.+)", r"COLLECTIVE_LIST(\1)", expr)
        # bare COLLECTIVE_LIST with no args → empty list
        expr = re.sub(r"\bCOLLECTIVE_LIST\b(?!\s*\()", r"COLLECTIVE_LIST()", expr)
        expr = re.sub(
            r"\bMUTUAL_AID_REGISTRY\s+(.+)",
            r"MUTUAL_AID_REGISTRY(\1)",
            expr,
        )

        expr = re.sub(r"\bEVIDENCE_BASED\b", "True", expr)
        expr = re.sub(r"\bALTERNATIVE_FACT\b", "False", expr)
        expr = re.sub(r"\bCLASSIFIED_MAR_A_LAGO\b", "None", expr)

        expr = re.sub(r"\bWEALTH_TAX\b", "-", expr)
        expr = re.sub(r"\bEQUAL_PAY\b", "+", expr)
        expr = re.sub(r"\bPROPORTIONAL_SHARE\b", "/", expr)
        expr = re.sub(r"\bFAIR_MULTIPLIER\b", "*", expr)
        expr = re.sub(r"\bPOWER_TO_THE_PEOPLE\b", "**", expr)
        expr = re.sub(r"\bMAPLE_SYRUP\b", "%", expr)
        expr = re.sub(r"\bMOONSHOT\b", "**", expr)

        literals = []

        def save_literal(m):
            literals.append(m.group(0))
            return f"__STR_{len(literals) - 1}__"

        processed = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', save_literal, expr)

        builtins = {
            "True": True,
            "False": False,
            "None": None,
            "LOString": LOString,
            "and": lambda a, b: a and b,
            "or": lambda a, b: a or b,
            "not": lambda a: not a,
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

        def var_replacer(match):
            name = match.group(0)
            if name.startswith("__STR_"):
                return name
            if name in builtins or name in ("and", "or", "not"):
                return name
            if name in self.variables:
                val = self.variables[name]
                return repr(val) if isinstance(val, str) else str(val)
            return "0"

        eval_safe = re.sub(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", var_replacer, processed)

        for idx, lit in enumerate(literals):
            clean_str = repr(lit[1:-1])
            eval_safe = eval_safe.replace(f"__STR_{idx}__", f"LOString({clean_str})")

        try:
            return eval(eval_safe, builtins)
        except (
            NameError,
            SyntaxError,
            TypeError,
            ValueError,
            ZeroDivisionError,
            AttributeError,
        ):
            return f"ALTERNATIVE_FACT ({expr})"

    def run(self):
        self.pc = 0
        in_healthcare = False
        loop_stack = []

        while self.pc < len(self.lines):
            line_number, stmt = self.lines[self.pc]
            self.current_line_number = line_number
            self.pc += 1

            if stmt.startswith("EXCUSE_ME"):
                continue

            try:
                if stmt.startswith("LAND_ACKNOWLEDGEMENT "):
                    land_name = self.evaluate_expression(stmt[21:].strip())
                    print(
                        "🍁 LAND ACKNOWLEDGEMENT: Respectfully acknowledging "
                        f"traditional territory of {land_name}. 🍁"
                    )
                elif stmt == "HONEY_BADGER_MODE":
                    print(
                        "🦡 HONEY BADGER MODE ENGAGED: Fearless execution activated! "
                        "Taking zero shit from MAGA spin, censorship, or "
                        "intimidation! 🦡"
                    )
                elif stmt.startswith("HONEY_BADGER_DONT_CARE "):
                    target = self.evaluate_expression(stmt[23:].strip())
                    print(
                        f"🦡 HONEY BADGER DOESN'T GIVE A SHIT ABOUT: '{target}'! "
                        "Moving forward with 100% fearlessness! ⚡"
                    )
                elif stmt.startswith("BADGER_BITE "):
                    target = self.evaluate_expression(stmt[12:].strip())
                    print(f"💥 BADGER BITE: {target} 💥")
                elif stmt.startswith("FAT_CATS_TAX "):
                    amount = self.evaluate_expression(stmt[13:].strip())
                    print(fat_cats_tax(amount))
                elif stmt.startswith("DONUT_DIVIDEND "):
                    amount = self.evaluate_expression(stmt[15:].strip())
                    print(donut_dividend(amount))
                elif stmt.startswith("NATIONAL_STOOGE "):
                    msg = self.evaluate_expression(stmt[14:].strip())
                    print(national_stooge(msg))
                elif stmt.startswith("GREEN_NEW_DEAL "):
                    goal = self.evaluate_expression(stmt[15:].strip())
                    print(green_new_deal(goal))
                elif stmt.startswith("RHETORICAL_QUESTION "):
                    question = self.evaluate_expression(stmt[19:].strip())
                    print(rhetorical_question(question))
                elif stmt.startswith("LOONIE_LOOP "):
                    count = self.evaluate_expression(stmt[12:].strip())
                    result = loonie_loop(count)
                    print(result)
                elif stmt.startswith("SOCIAL_LICENSE "):
                    license_name = self.evaluate_expression(stmt[15:].strip())
                    print(social_license(license_name))
                elif stmt.startswith("ELECTORATE_PULSE "):
                    pulse = self.evaluate_expression(stmt[16:].strip())
                    print(electorate_pulse(pulse))
                elif stmt == "NATIONAL_HEALTHCARE":
                    in_healthcare = True
                    print(
                        "🏥 NATIONAL HEALTHCARE ENGAGED: Public safety net activated "
                        "with honour and apologies."
                    )
                elif stmt.startswith("FACT_CHECK "):
                    body = stmt[11:].strip()
                    if "=" in body:
                        var_name, val_expr = body.split("=", 1)
                        self.variables[var_name.strip()] = self.evaluate_expression(
                            val_expr
                        )
                elif stmt.startswith("BROADCAST_CBC "):
                    val_expr = stmt[14:].strip()
                    val = self.evaluate_expression(val_expr)
                    print(val)
                elif stmt.startswith("TOWN_HALL "):
                    var_name = stmt[10:].strip()
                    if self.input_callback:
                        user_val = self.input_callback(var_name)
                    else:
                        user_val = input(f"🇨🇦 Democratic Input for {var_name}: ")
                    try:
                        self.variables[var_name] = int(user_val)
                    except ValueError:
                        self.variables[var_name] = user_val
                elif stmt.startswith("INPUT_BOX "):
                    var_name = stmt[10:].strip()
                    if self.input_callback:
                        user_val = self.input_callback(var_name, prompt_type="input_box")
                    else:
                        user_val = input(f"🖥️ Input Box for {var_name}: ")
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
                    print("🧹 CITIZEN REGISTER RESET: all values cleared, democracy restored to baseline.")
                elif stmt.startswith("FOR_EACH "):
                    # FOR_EACH item IN collection
                    body = stmt[9:].strip()
                    var_name, collection_expr = body.split(" IN ", 1)
                    var_name = var_name.strip()
                    collection = self.evaluate_expression(collection_expr.strip())
                    items = list(collection) if isinstance(collection, (list, tuple)) else []
                    if items:
                        self.variables[var_name] = items[0]
                        loop_stack.append({
                            "type": "foreach",
                            "var": var_name,
                            "items": items,
                            "index": 0,
                            "start_pc": self.pc,
                        })
                    else:
                        depth = 1
                        while self.pc < len(self.lines):
                            _, sub_stmt = self.lines[self.pc]
                            self.pc += 1
                            if sub_stmt.startswith("FOR_EACH "):
                                depth += 1
                            elif sub_stmt == "END_EACH":
                                depth -= 1
                                if depth == 0:
                                    break
                elif stmt == "END_EACH":
                    if loop_stack and loop_stack[-1]["type"] == "foreach":
                        top = loop_stack[-1]
                        top["index"] += 1
                        if top["index"] < len(top["items"]):
                            self.variables[top["var"]] = top["items"][top["index"]]
                            self.pc = top["start_pc"]
                        else:
                            loop_stack.pop()
                elif stmt.startswith("APPEND_TO "):
                    body = stmt[10:].strip()
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
                    body = stmt[12:].strip()
                    target_name, item_expr = body.split(",", 1)
                    target_name = target_name.strip()
                    item_value = self.evaluate_expression(item_expr.strip())
                    if target_name in self.variables and isinstance(self.variables[target_name], list):
                        try:
                            self.variables[target_name].remove(item_value)
                        except ValueError:
                            pass
                elif stmt.startswith("SORT_CITIZENS "):
                    var_name = stmt[14:].strip()
                    if var_name in self.variables:
                        self.variables[var_name] = sort_citizens(self.variables[var_name])
                        print(f"📊 Sorted {var_name}: {self.variables[var_name]}")
                elif stmt.startswith("AVERAGE_CITIZENS "):
                    var_name = stmt[17:].strip()
                    if var_name in self.variables:
                        avg = average_citizens(self.variables[var_name])
                        self.variables[f"{var_name}_average"] = avg
                        print(f"📈 Average of {var_name}: {avg}")
                elif stmt.startswith("SET_PEN_COLOR "):
                    color_value = self.evaluate_expression(stmt[14:].strip())
                    callback = self.graphics_callbacks.get("pen_color")
                    if callback:
                        callback(color_value)
                elif stmt.startswith("SET_FILL_COLOR "):
                    color_value = self.evaluate_expression(stmt[15:].strip())
                    callback = self.graphics_callbacks.get("fill_color")
                    if callback:
                        callback(color_value)
                elif stmt.startswith("SET_CANVAS_BG "):
                    bg_value = self.evaluate_expression(stmt[14:].strip())
                    callback = self.graphics_callbacks.get("canvas_bg")
                    if callback:
                        callback(bg_value)
                elif stmt.startswith("FILL_RECTANGLE "):
                    args = [arg.strip() for arg in stmt[15:].split(",")]
                    if len(args) == 4:
                        x = self.evaluate_expression(args[0])
                        y = self.evaluate_expression(args[1])
                        width = self.evaluate_expression(args[2])
                        height = self.evaluate_expression(args[3])
                        callback = self.graphics_callbacks.get("filled_rectangle")
                        if callback:
                            callback(x, y, width, height)
                elif stmt.startswith("FILL_CIRCLE "):
                    args = [arg.strip() for arg in stmt[12:].split(",")]
                    if len(args) == 3:
                        x = self.evaluate_expression(args[0])
                        y = self.evaluate_expression(args[1])
                        radius = self.evaluate_expression(args[2])
                        callback = self.graphics_callbacks.get("filled_circle")
                        if callback:
                            callback(x, y, radius)
                elif stmt.startswith("WAIT "):
                    delay = float(self.evaluate_expression(stmt[5:].strip()))
                    time.sleep(min(max(delay / 1000.0, 0.0), 5.0))
                elif stmt.startswith("PUBLISH_RESEARCH_FILE "):
                    body = stmt[22:].strip()
                    path_expr, content_expr = body.split(",", 1)
                    path = self.evaluate_expression(path_expr)
                    content = self.evaluate_expression(content_expr)
                    publish_research(path, content)
                    print(f"📄 Published research document to {path}")
                elif stmt == "CLEAR_GRAPHICS":
                    callback = self.graphics_callbacks.get("clear")
                    if callback:
                        callback()
                elif stmt.startswith("DRAW_LINE "):
                    args = [arg.strip() for arg in stmt[10:].split(",")]
                    if len(args) == 4:
                        x1 = self.evaluate_expression(args[0])
                        y1 = self.evaluate_expression(args[1])
                        x2 = self.evaluate_expression(args[2])
                        y2 = self.evaluate_expression(args[3])
                        callback = self.graphics_callbacks.get("line")
                        if callback:
                            callback(x1, y1, x2, y2)
                elif stmt.startswith("DRAW_RECTANGLE "):
                    args = [arg.strip() for arg in stmt[15:].split(",")]
                    if len(args) == 4:
                        x = self.evaluate_expression(args[0])
                        y = self.evaluate_expression(args[1])
                        width = self.evaluate_expression(args[2])
                        height = self.evaluate_expression(args[3])
                        callback = self.graphics_callbacks.get("rectangle")
                        if callback:
                            callback(x, y, width, height)
                elif stmt.startswith("DRAW_CIRCLE "):
                    args = [arg.strip() for arg in stmt[12:].split(",")]
                    if len(args) == 3:
                        x = self.evaluate_expression(args[0])
                        y = self.evaluate_expression(args[1])
                        radius = self.evaluate_expression(args[2])
                        callback = self.graphics_callbacks.get("circle")
                        if callback:
                            callback(x, y, radius)
                elif stmt.startswith("DRAW_TEXT "):
                    args = [arg.strip() for arg in stmt[10:].split(",", 2)]
                    if len(args) == 3:
                        x = self.evaluate_expression(args[0])
                        y = self.evaluate_expression(args[1])
                        text = self.evaluate_expression(args[2])
                        callback = self.graphics_callbacks.get("text")
                        if callback:
                            callback(x, y, text)
                elif stmt.startswith("PERHAPS "):
                    condition_part = stmt[8:]
                    if " FACT_ESTABLISHED" in condition_part:
                        cond_expr = condition_part.replace(" FACT_ESTABLISHED", "").strip()
                    else:
                        cond_expr = condition_part.strip()
                    res = self.evaluate_expression(cond_expr)
                    if not res:
                        depth = 1
                        while self.pc < len(self.lines) and depth > 0:
                            _, sub_stmt = self.lines[self.pc]
                            if sub_stmt.startswith("PERHAPS "):
                                depth += 1
                            elif sub_stmt == "END_PERHAPS":
                                depth -= 1
                                if depth == 0:
                                    self.pc += 1
                                    break
                            elif depth == 1 and sub_stmt == "STILL_IN_DENIAL":
                                self.pc += 1
                                break
                            elif depth == 1 and sub_stmt.startswith("PERHAPS_ALSO "):
                                cond_part = sub_stmt[13:].replace(" FACT_ESTABLISHED", "").strip()
                                if self.evaluate_expression(cond_part):
                                    self.pc += 1  # advance past PERHAPS_ALSO, enter its body
                                    break
                                # else: fall through to self.pc += 1 and keep scanning
                            self.pc += 1
                elif stmt.startswith("PERHAPS_ALSO "):
                    # reached during execution → a true branch already ran; skip to END_PERHAPS
                    depth = 1
                    while self.pc < len(self.lines):
                        _, sub_stmt = self.lines[self.pc]
                        self.pc += 1
                        if sub_stmt.startswith("PERHAPS "):
                            depth += 1
                        elif sub_stmt == "END_PERHAPS":
                            depth -= 1
                            if depth == 0:
                                break
                elif stmt == "STILL_IN_DENIAL":
                    depth = 1
                    while self.pc < len(self.lines) and depth > 0:
                        _, sub_stmt = self.lines[self.pc]
                        if sub_stmt.startswith("PERHAPS "):
                            depth += 1
                        elif sub_stmt == "END_PERHAPS":
                            depth -= 1
                        self.pc += 1
                elif stmt == "END_PERHAPS":
                    pass
                elif stmt.startswith("WHILE_CLASS_CONSCIOUS "):
                    cond_expr = stmt[22:].strip()
                    start_pc = self.pc - 1
                    res = self.evaluate_expression(cond_expr)
                    if res:
                        loop_stack.append({"type": "while", "cond": cond_expr, "start_pc": start_pc})
                    else:
                        depth = 1
                        while self.pc < len(self.lines) and depth > 0:
                            _, sub_stmt = self.lines[self.pc]
                            if sub_stmt.startswith("WHILE_CLASS_CONSCIOUS "):
                                depth += 1
                            elif sub_stmt == "CONTINUE_ORGANIZING":
                                depth -= 1
                                if depth == 0:
                                    self.pc += 1
                                    break
                            self.pc += 1
                elif stmt == "CONTINUE_ORGANIZING":
                    if loop_stack and loop_stack[-1]["type"] == "while":
                        top = loop_stack[-1]
                        res = self.evaluate_expression(top["cond"])
                        if res:
                            self.pc = top["start_pc"] + 1
                        else:
                            loop_stack.pop()
                elif stmt == "UNIVERSAL_HEALTHCARE":
                    in_healthcare = True
                elif stmt == "EXECUTIVE_ORDER_BLOCKED":
                    in_healthcare = False
                elif stmt.startswith("COAST_TO_COAST "):
                    loop_def = stmt[15:].strip()
                    step_val = 1
                    if " STEP " in loop_def:
                        loop_def, step_expr = loop_def.split(" STEP ")
                        step_val = self.evaluate_expression(step_expr)
                    var_part, range_part = loop_def.split(" UP_TO ")
                    var_name, start_expr = var_part.split("=")
                    var_name = var_name.strip()
                    start_val = self.evaluate_expression(start_expr)
                    end_val = self.evaluate_expression(range_part)
                    self.variables[var_name] = start_val
                    loop_stack.append({
                        "type": "for",
                        "var": var_name,
                        "end": end_val,
                        "step": step_val,
                        "start_pc": self.pc,
                    })
                elif stmt == "THANK_YOU_EH":
                    if loop_stack and loop_stack[-1]["type"] == "for":
                        top = loop_stack[-1]
                        current_val = self.variables[top["var"]] + top["step"]
                        if (top["step"] > 0 and current_val <= top["end"]) or (
                            top["step"] < 0 and current_val >= top["end"]
                        ):
                            self.variables[top["var"]] = current_val
                            self.pc = top["start_pc"]
                        else:
                            loop_stack.pop()
                elif stmt == "BREAK_FROM_CAUCUS":
                    if loop_stack:
                        top = loop_stack.pop()
                        _loop_markers = {
                            "for":     ("COAST_TO_COAST ",      "THANK_YOU_EH"),
                            "while":   ("WHILE_CLASS_CONSCIOUS ", "CONTINUE_ORGANIZING"),
                            "foreach": ("FOR_EACH ",              "END_EACH"),
                        }
                        start_kw, end_marker = _loop_markers.get(
                            top["type"], ("COAST_TO_COAST ", "THANK_YOU_EH")
                        )
                        depth = 1
                        while self.pc < len(self.lines):
                            _, sub_stmt = self.lines[self.pc]
                            self.pc += 1
                            if sub_stmt.startswith(start_kw):
                                depth += 1
                            elif sub_stmt == end_marker:
                                depth -= 1
                                if depth == 0:
                                    break
                elif stmt == "NEXT_MOTION":
                    if loop_stack:
                        top = loop_stack[-1]
                        if top["type"] == "for":
                            current_val = self.variables[top["var"]] + top["step"]
                            if (top["step"] > 0 and current_val <= top["end"]) or (
                                top["step"] < 0 and current_val >= top["end"]
                            ):
                                self.variables[top["var"]] = current_val
                                self.pc = top["start_pc"]
                            else:
                                loop_stack.pop()
                        elif top["type"] == "while":
                            res = self.evaluate_expression(top["cond"])
                            if res:
                                self.pc = top["start_pc"] + 1
                            else:
                                loop_stack.pop()
                        elif top["type"] == "foreach":
                            top["index"] += 1
                            if top["index"] < len(top["items"]):
                                self.variables[top["var"]] = top["items"][top["index"]]
                                self.pc = top["start_pc"]
                            else:
                                loop_stack.pop()
                elif stmt.startswith("SUBPOENA "):
                    target = int(stmt[9:].strip())
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
                    sec = float(self.evaluate_expression(stmt[14:].strip()))
                    print(f"⛳ Executive on Golf Vacation for {sec} seconds...")
                    time.sleep(min(sec, 2.0))
                elif stmt.startswith("CLIMATE_EMERGENCY "):
                    msg = self.evaluate_expression(stmt[18:].strip())
                    raise LakeOntarioInterpreterError(
                        f"Line {self.current_line_number}: CLIMATE EMERGENCY RAISED: {msg}"
                    )
                elif stmt == "IMPEACH":
                    print("🏛️ IMPEACHMENT EFFECTIVE: Program terminated cleanly.")
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
                if in_healthcare:
                    while self.pc < len(self.lines):
                        _, sub_stmt = self.lines[self.pc]
                        if sub_stmt == "EXECUTIVE_ORDER_BLOCKED":
                            self.pc += 1
                            break
                        self.pc += 1
                else:
                    line_tag = (
                        f"Line {self.current_line_number}: "
                        if self.current_line_number is not None
                        else ""
                    )
                    print(f"🚨 UNHANDLED DISASTER: {line_tag}{e}")
                    sys.exit(1)


def validate_script(code):
    errors = []
    for raw_line in code.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("EXCUSE_ME"):
            continue

        match = re.match(r"^(\d+)\s+(.*)$", stripped)
        if match:
            line_number = int(match.group(1))
            stmt = match.group(2).strip()
        else:
            line_number = None
            stmt = stripped

        if stmt.startswith("FACT_CHECK"):
            if "=" not in stmt:
                label = f"Line {line_number}" if line_number is not None else "Line ?"
                errors.append(f"{label}: FACT_CHECK statement must include '='")
            else:
                _, rhs = stmt.split("=", 1)
                if not rhs.strip():
                    label = f"Line {line_number}" if line_number is not None else "Line ?"
                    errors.append(
                        f"{label}: FACT_CHECK assignment is missing a value"
                    )
        elif stmt.startswith("COAST_TO_COAST") and " UP_TO " not in stmt:
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(
                f"{label}: COAST_TO_COAST statement must include 'UP_TO'"
            )
        elif stmt.startswith("PUBLISH_RESEARCH_FILE") and "," not in stmt:
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(
                f"{label}: PUBLISH_RESEARCH_FILE must separate path and content with a comma"
            )
        elif stmt.startswith("SUBPOENA"):
            target_text = stmt[9:].strip()
            if not target_text.isdigit():
                label = f"Line {line_number}" if line_number is not None else "Line ?"
                errors.append(f"{label}: SUBPOENA must target a numbered line")
        elif stmt.startswith("GOLF_VACATION"):
            value = stmt[14:].strip()
            try:
                float(value)
            except ValueError:
                label = f"Line {line_number}" if line_number is not None else "Line ?"
                errors.append(f"{label}: GOLF_VACATION requires a numeric value")
        elif stmt.startswith("CLIMATE_EMERGENCY"):
            if not stmt[18:].strip():
                label = f"Line {line_number}" if line_number is not None else "Line ?"
                errors.append(f"{label}: CLIMATE_EMERGENCY requires a message")
        elif stmt.startswith("TOWN_HALL") and not stmt[10:].strip():
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(f"{label}: TOWN_HALL requires a variable name")
        elif stmt.startswith("INPUT_BOX") and not stmt[10:].strip():
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(f"{label}: INPUT_BOX requires a variable name")
        elif stmt.startswith("FOR_EACH ") and " IN " not in stmt:
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(f"{label}: FOR_EACH statement must include 'IN'")
        elif stmt.startswith("PERHAPS_ALSO") and not stmt[13:].strip():
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(f"{label}: PERHAPS_ALSO requires a condition")
        elif stmt.startswith("REMOVE_FROM") and "," not in stmt:
            label = f"Line {line_number}" if line_number is not None else "Line ?"
            errors.append(f"{label}: REMOVE_FROM must separate variable and value with a comma")

    return errors


def run_repl():
    interpreter = LakeOntarioInterpreter()
    print("Lake Ontario BASIC REPL")
    print("Type a statement and press Enter. Type IMPEACH or EXIT to quit.\n")
    while True:
        try:
            statement = input("lo> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\nGoodbye from Lake Ontario BASIC.")
            break

        statement = statement.strip()
        if not statement:
            continue
        if statement.upper() in {"IMPEACH", "EXIT", "QUIT"}:
            print("Goodbye from Lake Ontario BASIC.")
            break

        try:
            interpreter.load_script(statement)
            interpreter.run()
        except SystemExit as exc:
            if exc.code == 0:
                break
            # Runtime error already printed by run(); preserve variables across reset
            saved_vars = interpreter.variables.copy()
            interpreter = LakeOntarioInterpreter()
            interpreter.variables = saved_vars
        except (LakeOntarioInterpreterError, OSError, ValueError, TypeError,
                ZeroDivisionError, SyntaxError, NameError) as exc:
            print(f"🚨 REPL ERROR: {exc}")


def list_example_scripts():
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
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


def run_example_script(example_name):
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    candidate = example_name
    if not candidate.endswith(".lo"):
        candidate = f"{candidate}.lo"
    script_path = os.path.join(examples_dir, candidate)

    if not os.path.isfile(script_path):
        print(f"Example script not found: {example_name}")
        sys.exit(1)

    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    errors = validate_script(code)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    interpreter = LakeOntarioInterpreter()
    interpreter.load_script(code)
    interpreter.run()


def print_usage():
    print("Usage: python3 interpreter.py [--repl | -i] [--check script.lo] [--list-examples] [--run-example example.lo] [--doctor] [--version] [script.lo]")
    print()
    print("Examples:")
    print("  python3 interpreter.py examples/hello.lo")
    print("  python3 interpreter.py --repl")
    print("  python3 interpreter.py --check examples/hello.lo")
    print("  python3 interpreter.py --list-examples")
    print("  python3 interpreter.py --run-example hello")
    print("  python3 interpreter.py --doctor")
    print("  python3 interpreter.py --version")
    print("  python3 interpreter.py -i")
    print()
    print("The interpreter reads Lake Ontario BASIC scripts and supports an")
    print("interactive REPL for quick experimentation.")


def run_environment_doctor():
    python_version = sys.version.split()[0]
    venv_mode = "yes" if sys.prefix != sys.base_prefix or "VIRTUAL_ENV" in os.environ else "no"
    tkinter_status = "ok" if tkinter is not None else "missing"
    project_root = os.path.dirname(os.path.abspath(__file__))

    example_count = 0
    examples_dir = os.path.join(project_root, "examples")
    try:
        example_count = len(
            [
                name for name in os.listdir(examples_dir)
                if name.endswith(".lo")
            ]
        )
    except OSError:
        example_count = 0

    print(f"Python: {python_version}")
    print(f"Virtual environment: {venv_mode}")
    print(f"Tkinter: {tkinter_status}")
    print(f"Example scripts: {example_count}")

    if tkinter is None:
        print("Environment check failed: tkinter is missing. Install python3-tk or use the project venv.")
        sys.exit(1)

    print("Environment OK")


def main():
    if len(sys.argv) == 1:
        run_repl()
        return

    if sys.argv[1] in {"-h", "--help", "help"}:
        print_usage()
        return

    if sys.argv[1] in {"--version", "-V"}:
        print(f"Lake Ontario BASIC {__version__}")
        return

    if sys.argv[1] == "--doctor":
        run_environment_doctor()
        return

    if sys.argv[1] == "--list-examples":
        if len(sys.argv) != 2:
            print_usage()
            sys.exit(1)
        list_example_scripts()
        return

    if sys.argv[1] == "--run-example":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        run_example_script(sys.argv[2])
        return

    if sys.argv[1] in {"--repl", "-i"}:
        run_repl()
        return

    if sys.argv[1] == "--check":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        script_path = sys.argv[2]
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
        errors = validate_script(code)
        if errors:
            for error in errors:
                print(error)
            sys.exit(1)
        print(f"Validation passed for {script_path}")
        return

    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    script_path = sys.argv[1]
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    errors = validate_script(code)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    interpreter = LakeOntarioInterpreter()
    interpreter.load_script(code)
    interpreter.run()


if __name__ == "__main__":
    main()
