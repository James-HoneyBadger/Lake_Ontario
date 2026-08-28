#!/usr/bin/env python3
"""
Lake Ontario BASIC Interpreter
A fully featured, practical programming language interpreter inspired by classic BASIC,
infused with Canadian politeness & Honey Badger attitude, pro-science, pro-health care, pro-diversity,
pro-socialism, and anti-MAGA.
"""

import sys
import re
import math
import time

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
    except Exception:
        return 0

def tax_the_billionaire(val):
    try:
        num = float(val)
        if num > 1000000:
            excess = num - 1000000
            res = 1000000 + (excess * 0.1)  # 90% marginal rate
        else:
            res = num
        return LOString(f"{res:.2f}")
    except Exception:
        return LOString("0.00")

def defund_oligarchy(val):
    try:
        num = float(val)
        res = max(0.0, num * 0.05)  # Redistribute 95% to social housing
        return LOString(f"{res:.2f}")
    except Exception:
        return LOString("0.00")

def living_wage(hours, base_rate=25.0):
    try:
        res = float(hours) * float(base_rate)
        return LOString(f"{res:.2f}")
    except Exception:
        return LOString("0.00")

def universal_basic_income(population, grant=2000.0):
    try:
        res = float(population) * float(grant)
        return LOString(f"{res:.2f}")
    except Exception:
        return LOString("0.00")

def carbon_offset(emissions_tons):
    try:
        res = float(emissions_tons) * 65.0  # $65/ton rebate fund
        return LOString(f"{res:.2f}")
    except Exception:
        return LOString("0.00")

def format_currency(val):
    try:
        num = float(val)
        return LOString(f"{num:.2f}")
    except Exception:
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
        "climate": "Peer-Reviewed Consensus: Anthropogenic climate change is real and requires immediate renewable transition.",
        "vaccines": "Peer-Reviewed Consensus: Vaccines are safe, effective, and save millions of lives globally.",
        "evolution": "Peer-Reviewed Consensus: Biological evolution by natural selection is the foundational principle of biology.",
        "diversity": "Peer-Reviewed Consensus: Diverse and inclusive communities show higher resilience, innovation, and well-being."
    }
    for k, v in facts.items():
        if k in topic_str:
            return v
    return f"Peer-Reviewed Science: Empirical analysis confirms {topic} is backed by scientific evidence."

def peer_reviewed_sqrt(val):
    return math.sqrt(float(val))

def science_round(val, decimals=2):
    return round(float(val), int(decimals))

def read_resource(filepath):
    try:
        with open(str(filepath).strip('"\''), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ALTERNATIVE_FACT (Cannot read resource: {e})"

def publish_research(filepath, content):
    try:
        with open(str(filepath).strip('"\''), 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except Exception:
        return False

def honey_badger_debunk(val):
    text = str(val)
    return LOString(f"🦡 HONEY BADGER DEBUNK: Shredded lie '{text}' into peer-reviewed dust! Takes no shit!")

def honey_badger_bite(target):
    text = str(target)
    return LOString(f"🦡 HONEY BADGER BITES BACK: Relentlessly tearing apart '{text}' with zero fear and 100% truth!")

def honey_badger_strike(action):
    text = str(action)
    return LOString(f"🦡 UNYIELDING BADGER STRIKE: Taking no shit on '{text}'! Standing firm!")

def say_sorry(message):
    text = str(message)
    return LOString(f"Sorry, eh? {text} — delivered with extra maple syrup and contrition.")

def make_it_rain(amount):
    try:
        num = float(amount)
        redistributed = num * 0.95
        return LOString(f"🍁 MAKE IT RAIN: Redistributing ${redistributed:.2f} to healthcare, transit, and doughnuts.")
    except Exception:
        return LOString("🍁 MAKE IT RAIN: Alternative facts cannot be redistributed.")

def public_transit_fare(distance, base_fare=3.50):
    try:
        miles = float(distance)
        fare = max(1.0, base_fare + miles * 0.25)
        return LOString(f"🚊 Transit fare for {miles:.1f} km: ${fare:.2f} (inclusive of polite service fees)")
    except Exception:
        return LOString("🚊 Transit fare unavailable: Invalid route.")

def toque_warmth(temp_celsius):
    try:
        temp = float(temp_celsius)
        if temp < -20:
            return LOString("🧣 Toque warmth: Full Canada Goose thermal emergency activated.")
        if temp < 0:
            return LOString("🧣 Toque warmth: Cozy enough for poutine and parliament protests.")
        return LOString("🧣 Toque warmth: Too warm for a toque, but wear it anyway for civic pride.")
    except Exception:
        return LOString("🧣 Toque warmth: Invalid weather, eh?")

def truth_meter(claim):
    text = str(claim)
    rating = 100 if "EVIDENCE_BASED" in text or "True" in text else 0
    return LOString(f"📏 Truth Meter: {rating}% sincerity, with a side of maple humour.")

def make_it_snow(forecast, flakes=100):
    try:
        count = int(flakes)
        return LOString(f"❄️ Snow forecast: {count} flake-level protests expected when {forecast}.")
    except Exception:
        return LOString("❄️ Snow forecast: Confused, like a polar vortex in July.")


def fat_cats_tax(amount):
    try:
        num = float(amount)
        taxed = max(0.0, num * 0.95)
        return LOString(f"💼 FAT CATS TAX: Extracted ${taxed:.2f} from the one-percenters and sent it to universal crumbs.")
    except Exception:
        return LOString("💼 FAT CATS TAX: Alternative facts cannot be taxed.")


def donut_dividend(amount):
    try:
        num = float(amount)
        return LOString(f"🍩 DONUT DIVIDEND: Distributing ${num:.2f} worth of pastries to every rally-goer.")
    except Exception:
        return LOString("🍩 DONUT DIVIDEND: Invalid pastry budget.")


def national_stooge(statement):
    text = str(statement)
    return LOString(f"🎩 NATIONAL STOOGE: '{text}' — delivered with maximum spin and minimum accountability.")


def green_new_deal(goal):
    return LOString(f"🌿 GREEN NEW DEAL: Targeting '{goal}' with electric buses, solar subsidies, and polite protest marches.")


def rhetorical_question(question):
    return LOString(f"❓ RHETORICAL QUESTION: {question} — and yes, the answer is obviously 'EVIDENCE_BASED'.")


def loonie_loop(count):
    try:
        num = int(count)
        return [f"Loonie #{i+1}" for i in range(max(0, num))]
    except Exception:
        return ["Loonie loop failed: invalid flake count."]


def social_license(license_name):
    return LOString(f"✅ SOCIAL LICENSE: '{license_name}' has 100% approval from unionized beavers and open-source poets.")


def electorate_pulse(value):
    try:
        pct = float(value)
        return LOString(f"📊 ELECTORATE PULSE: {min(max(pct, 0.0), 100.0):.1f}% enthusiasm for the public mandate.")
    except Exception:
        return LOString("📊 ELECTORATE PULSE: Polling data is unavailable, eh.")


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

    def set_input_callback(self, callback):
        self.input_callback = callback

    def set_graphics_callbacks(self, callbacks):
        self.graphics_callbacks = callbacks or {}

    def load_script(self, code_str):
        raw_lines = code_str.splitlines()
        self.lines = []
        self.line_map = {}

        for line in raw_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("EXCUSE_ME"):
                continue
            
            # Line number parsing
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
        
        # Replace keywords, literals and custom operators
        expr = re.sub(r'\bEVIDENCE_BASED\b', 'True', expr)
        expr = re.sub(r'\bALTERNATIVE_FACT\b', 'False', expr)
        expr = re.sub(r'\bCLASSIFIED_MAR_A_LAGO\b', 'None', expr)

        # Custom operators mapped to Python operators
        expr = re.sub(r'\bWEALTH_TAX\b', '-', expr)
        expr = re.sub(r'\bEQUAL_PAY\b', '+', expr)
        expr = re.sub(r'\bPROPORTIONAL_SHARE\b', '/', expr)
        expr = re.sub(r'\bFAIR_MULTIPLIER\b', '*', expr)
        expr = re.sub(r'\bPOWER_TO_THE_PEOPLE\b', '**', expr)
        expr = re.sub(r'\bMAPLE_SYRUP\b', '%', expr)
        expr = re.sub(r'\bMOONSHOT\b', '**', expr)

        # Preserve string literals during variable replacement
        literals = []
        def save_literal(m):
            literals.append(m.group(0))
            return f"__STR_{len(literals)-1}__"

        processed = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', save_literal, expr)

        # Built-in symbol whitelist
        builtins = {
            "True": True, "False": False, "None": None, "LOString": LOString,
            "and": lambda a, b: a and b, "or": lambda a, b: a or b, "not": lambda a: not a,
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
            "COLLECTIVE_LIST": lambda *args: list(args),
            "MUTUAL_AID_REGISTRY": lambda **kwargs: dict(kwargs)
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

        eval_safe = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', var_replacer, processed)

        # Restore string literals wrapped as LOString objects for overloaded + operator
        for idx, lit in enumerate(literals):
            clean_str = repr(lit[1:-1])
            eval_safe = eval_safe.replace(f"__STR_{idx}__", f"LOString({clean_str})")

        try:
            return eval(eval_safe, builtins)
        except Exception:
            return f"ALTERNATIVE_FACT ({expr})"

    def run(self):
        self.pc = 0
        in_healthcare = False
        loop_stack = []

        while self.pc < len(self.lines):
            line_num, stmt = self.lines[self.pc]
            self.pc += 1

            if stmt.startswith("EXCUSE_ME"):
                continue

            try:
                # LAND_ACKNOWLEDGEMENT header
                if stmt.startswith("LAND_ACKNOWLEDGEMENT "):
                    land_name = self.evaluate_expression(stmt[21:].strip())
                    print(f"🍁 LAND ACKNOWLEDGEMENT: Respectfully acknowledging traditional territory of {land_name}. 🍁")

                # HONEY_BADGER_MODE statement
                elif stmt == "HONEY_BADGER_MODE":
                    print("🦡 HONEY BADGER MODE ENGAGED: Fearless execution activated! Taking zero shit from MAGA spin, censorship, or intimidation! 🦡")

                # HONEY_BADGER_DONT_CARE statement
                elif stmt.startswith("HONEY_BADGER_DONT_CARE "):
                    target = self.evaluate_expression(stmt[23:].strip())
                    print(f"🦡 HONEY BADGER DOESN'T GIVE A SHIT ABOUT: '{target}'! Moving forward with 100% fearlessness! ⚡")

                # BADGER_BITE statement
                elif stmt.startswith("BADGER_BITE "):
                    target = self.evaluate_expression(stmt[12:].strip())
                    print(f"💥 BADGER BITE: {target} 💥")

                # FAT_CATS_TAX statement
                elif stmt.startswith("FAT_CATS_TAX "):
                    amount = self.evaluate_expression(stmt[13:].strip())
                    print(fat_cats_tax(amount))

                # DONUT_DIVIDEND statement
                elif stmt.startswith("DONUT_DIVIDEND "):
                    amount = self.evaluate_expression(stmt[15:].strip())
                    print(donut_dividend(amount))

                # NATIONAL_STOOGE statement
                elif stmt.startswith("NATIONAL_STOOGE "):
                    msg = self.evaluate_expression(stmt[14:].strip())
                    print(national_stooge(msg))

                # GREEN_NEW_DEAL statement
                elif stmt.startswith("GREEN_NEW_DEAL "):
                    goal = self.evaluate_expression(stmt[15:].strip())
                    print(green_new_deal(goal))

                # RHETORICAL_QUESTION statement
                elif stmt.startswith("RHETORICAL_QUESTION "):
                    question = self.evaluate_expression(stmt[19:].strip())
                    print(rhetorical_question(question))

                # LOONIE_LOOP statement
                elif stmt.startswith("LOONIE_LOOP "):
                    count = self.evaluate_expression(stmt[12:].strip())
                    result = loonie_loop(count)
                    print(result)

                # SOCIAL_LICENSE statement
                elif stmt.startswith("SOCIAL_LICENSE "):
                    license_name = self.evaluate_expression(stmt[15:].strip())
                    print(social_license(license_name))

                # ELECTORATE_PULSE statement
                elif stmt.startswith("ELECTORATE_PULSE "):
                    pulse = self.evaluate_expression(stmt[16:].strip())
                    print(electorate_pulse(pulse))

                # NATIONAL_HEALTHCARE alias for UNIVERSAL_HEALTHCARE
                elif stmt == "NATIONAL_HEALTHCARE":
                    in_healthcare = True
                    print("🏥 NATIONAL HEALTHCARE ENGAGED: Public safety net activated with honour and apologies.")

                # FACT_CHECK variable assignment
                elif stmt.startswith("FACT_CHECK "):
                    body = stmt[11:].strip()
                    if "=" in body:
                        var_name, val_expr = body.split("=", 1)
                        self.variables[var_name.strip()] = self.evaluate_expression(val_expr)

                # BROADCAST_CBC print statement
                elif stmt.startswith("BROADCAST_CBC "):
                    val_expr = stmt[14:].strip()
                    val = self.evaluate_expression(val_expr)
                    print(val)

                # TOWN_HALL input statement
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

                # INPUT_BOX statement for GUI text input dialogs
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

                # SET_PEN_COLOR and SET_FILL_COLOR statements
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

                # FILL_RECTANGLE statement
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

                # FILL_CIRCLE statement
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

                # PUBLISH_RESEARCH_FILE statement
                elif stmt.startswith("PUBLISH_RESEARCH_FILE "):
                    body = stmt[22:].strip()
                    path_expr, content_expr = body.split(",", 1)
                    path = self.evaluate_expression(path_expr)
                    content = self.evaluate_expression(content_expr)
                    publish_research(path, content)
                    print(f"📄 Published research document to {path}")

                # Graphics and GUI drawing statements
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

                # PERHAPS ... FACT_ESTABLISHED conditional
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
                            elif sub_stmt == "STILL_IN_DENIAL" and depth == 1:
                                self.pc += 1
                                break
                            self.pc += 1

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

                # WHILE_CLASS_CONSCIOUS loop
                elif stmt.startswith("WHILE_CLASS_CONSCIOUS "):
                    cond_expr = stmt[22:].strip()
                    start_pc = self.pc - 1
                    res = self.evaluate_expression(cond_expr)
                    if res:
                        loop_stack.append({
                            "type": "while",
                            "cond": cond_expr,
                            "start_pc": start_pc
                        })
                    else:
                        # Skip to CONTINUE_ORGANIZING
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

                # UNIVERSAL_HEALTHCARE exception safety block
                elif stmt == "UNIVERSAL_HEALTHCARE":
                    in_healthcare = True

                elif stmt == "EXECUTIVE_ORDER_BLOCKED":
                    in_healthcare = False

                # COAST_TO_COAST for loop (COAST_TO_COAST i = start UP_TO end [STEP step])
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
                        "start_pc": self.pc
                    })

                elif stmt == "THANK_YOU_EH":
                    if loop_stack and loop_stack[-1]["type"] == "for":
                        top = loop_stack[-1]
                        current_val = self.variables[top["var"]] + top["step"]
                        if (top["step"] > 0 and current_val <= top["end"]) or (top["step"] < 0 and current_val >= top["end"]):
                            self.variables[top["var"]] = current_val
                            self.pc = top["start_pc"]
                        else:
                            loop_stack.pop()

                # SUBPOENA subroutine call
                elif stmt.startswith("SUBPOENA "):
                    target = int(stmt[9:].strip())
                    if target in self.line_map:
                        self.call_stack.append(self.pc)
                        self.pc = self.line_map[target]
                    else:
                        print(f"Subpoena Error: Line {target} ignored subpoena!")

                # RETURN_TO_OTTAWA return from subroutine
                elif stmt == "RETURN_TO_OTTAWA":
                    if self.call_stack:
                        self.pc = self.call_stack.pop()
                    else:
                        print("Error: RETURN_TO_OTTAWA with empty call stack, eh!")

                # GOLF_VACATION pause execution
                elif stmt.startswith("GOLF_VACATION "):
                    sec = float(self.evaluate_expression(stmt[14:].strip()))
                    print(f"⛳ Executive on Golf Vacation for {sec} seconds...")
                    import time
                    time.sleep(min(sec, 2.0))

                # CLIMATE_EMERGENCY exception raise
                elif stmt.startswith("CLIMATE_EMERGENCY "):
                    msg = self.evaluate_expression(stmt[18:].strip())
                    raise Exception(f"CLIMATE EMERGENCY RAISED: {msg}")

                # IMPEACH terminate program
                elif stmt == "IMPEACH":
                    print("🏛️ IMPEACHMENT EFFECTIVE: Program terminated cleanly.")
                    break

            except Exception as e:
                if in_healthcare:
                    while self.pc < len(self.lines):
                        _, sub_stmt = self.lines[self.pc]
                        if sub_stmt == "EXECUTIVE_ORDER_BLOCKED":
                            self.pc += 1
                            break
                        self.pc += 1
                else:
                    print(f"🚨 UNHANDLED DISASTER: {e}")
                    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 interpreter.py <script.lo>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    interpreter = LakeOntarioInterpreter()
    interpreter.load_script(code)
    interpreter.run()

if __name__ == "__main__":
    main()
