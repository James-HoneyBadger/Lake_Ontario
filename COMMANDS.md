# Lake Ontario BASIC Commands and Functions

## Statement Keywords

- `LAND_ACKNOWLEDGEMENT "territory"`
  - Mandatory respectful header for scripts.
- `HONEY_BADGER_MODE`
  - Activates fearless execution mode.
- `HONEY_BADGER_DONT_CARE "target"`
  - Declares bad-faith targets to ignore.
- `BADGER_BITE expression`
  - Prints a fierce truth statement.
- `FACT_CHECK name = expression`
  - Assigns a value to a variable.
- `BROADCAST_CBC expression`
  - Outputs text or values to standard output. Comma-separated values print
    space-separated, e.g. `BROADCAST_CBC "Fact", 7` prints `Fact 7`.
- `TOWN_HALL variable_name`
  - Prompts the user and stores the input.
- `PERHAPS condition FACT_ESTABLISHED`
  - Starts a conditional block.
- `STILL_IN_DENIAL`
  - Starts the `else` branch of a conditional block.
- `END_PERHAPS`
  - Ends a conditional block.
- `COALITION expression`
  - Examines a value once and runs the first matching `PLANK` branch.
- `PLANK value`
  - A branch of the enclosing `COALITION`, matched by equality.
- `PLANK >= value` (also `<=`, `==`, `!=`, `>`, `<`)
  - A branch matched by comparison, for banded decisions.
- `MINORITY_REPORT`
  - Default branch of a `COALITION` when no `PLANK` matches.
- `END_COALITION`
  - Closes a `COALITION` block.
- `WHILE_CLASS_CONSCIOUS condition`
  - Starts a while loop.
- `CONTINUE_ORGANIZING`
  - Ends a while loop.
- `COAST_TO_COAST var = start UP_TO end [STEP step]`
  - Starts a for-style loop.
- `THANK_YOU_EH`
  - Ends a for-style loop.
- `UNIVERSAL_HEALTHCARE`
  - Begins an exception-safe block.
- `EXECUTIVE_ORDER_BLOCKED`
  - Ends an exception-safe block.
- `SUBPOENA line_number`
  - Jumps to a numbered line as a subroutine.
- `RETURN_TO_OTTAWA`
  - Returns from a subroutine call.
- `GOLF_VACATION seconds`
  - Pauses execution for a short time.
- `CLIMATE_EMERGENCY message`
  - Raises an exception inside the script.
- `IMPEACH`
  - Terminates program execution.
- `PUBLISH_RESEARCH_FILE path, content`
  - Writes content to disk as a report.
- `HEAR_HEAR point`
  - Records a point the chamber reluctantly agrees with.
- `CITIZEN_PETITION text`
  - Files a petition and sends it to a very serious committee.
- `VOTE_RECORDED voter, election, choice`
  - Records a ballot in the civic registry.
- `PETITION_SIGNATURE_COLLECTED name, petition`
  - Adds a signature to a petition's supporting documents.
- `TESTIMONY_ADDED witness, statement`
  - Files testimony and opens a fresh binder.
- `MOTION_PASSED`
  - Confirms that the public interest defeated administrative fog.
- `SHOW_EVIDENCE_LOG`
  - Prints the evidence journal: every `FACT_CHECK`, with amendments flagged.
- `PUBLISH_EVIDENCE_LOG "path"`
  - Writes the evidence journal to a file as an auditable record.

### Farcical Policy Statements
- `FAT_CATS_TAX amount`
  - Issues a farcical wealth redistribution order.
- `DONUT_DIVIDEND amount`
  - Sends pastries to the people.
- `NATIONAL_STOOGE statement`
  - Publishes a theatrical political spin.
- `GREEN_NEW_DEAL goal`
  - Starts a high-minded climate policy declaration.
- `RHETORICAL_QUESTION question`
  - Poses an obviously evidence-based question.
- `LOONIE_LOOP count`
  - Iterates a cartoonish loop of loonies.
- `SOCIAL_LICENSE name`
  - Grants approval from unionized beavers and poets.
- `ELECTORATE_PULSE value`
  - Reports mock public enthusiasm as a percentage.
- `NATIONAL_HEALTHCARE`
  - Alias for `UNIVERSAL_HEALTHCARE` with extra pomp.
- `INPUT_BOX variable_name`
  - Prompts the user with a GUI input dialog and stores the response.
- `SET_PEN_COLOR "color"`
  - Sets the drawing pen color for future shapes and lines.
- `SET_FILL_COLOR "color"`
  - Sets the fill color for filled shapes.
- `SET_CANVAS_BG "color"`
  - Sets the graphics canvas background color.
- `SET_PEN_WIDTH width`
  - Sets the stroke width used for lines and shape outlines.
- `CLEAR_GRAPHICS`
  - Clears the GUI graphics canvas while running in the GUI IDE.
- `DRAW_LINE x1, y1, x2, y2`
  - Draws a line on the GUI canvas.
- `DRAW_POINT x, y`
  - Draws a single point (dot) on the GUI canvas.
- `DRAW_RECTANGLE x, y, width, height`
  - Draws a rectangle on the GUI canvas.
- `FILL_RECTANGLE x, y, width, height`
  - Draws a filled rectangle on the GUI canvas.
- `DRAW_CIRCLE x, y, radius`
  - Draws a circle on the GUI canvas.
- `FILL_CIRCLE x, y, radius`
  - Draws a filled circle on the GUI canvas.
- `DRAW_OVAL x1, y1, x2, y2`
  - Draws an oval within the given bounding box.
- `FILL_OVAL x1, y1, x2, y2`
  - Draws a filled oval within the given bounding box.
- `DRAW_ARC x, y, radius, start_angle, extent_angle`
  - Draws an arc centered at `x, y` from `start_angle` for `extent_angle` degrees.
- `DRAW_POLYGON x1, y1, x2, y2, ...`
  - Draws an outlined polygon from a flat list of point coordinates (3+ points).
- `FILL_POLYGON x1, y1, x2, y2, ...`
  - Draws a filled polygon from a flat list of point coordinates (3+ points).
- `DRAW_TRIANGLE x1, y1, x2, y2, x3, y3`
  - Draws an outlined triangle from three points.
- `FILL_TRIANGLE x1, y1, x2, y2, x3, y3`
  - Draws a filled triangle from three points.
- `DRAW_TEXT x, y, text`
  - Draws text on the GUI canvas.
- `PLAY_TONE frequency, duration_ms`
  - Plays a tone at `frequency` Hz for `duration_ms` milliseconds.
- `PLAY_SOUND_FILE path`
  - Plays an audio file (e.g. `.wav`) from disk.
- `STOP_SOUND`
  - Stops any sound currently playing.
- `HONEY_BADGER_GROWL`
  - Plays a short, gruff low tone — the Honey Badger doesn't care.
- `TOWN_HALL_BELL`
  - Rings a bell tone to call the room to order.
- `STANDING_OVATION`
  - Plays a celebratory rising flourish of tones, fit for a passed motion.
- `WAIT milliseconds`
  - Pauses execution for the given number of milliseconds.
- `FOR_EACH item IN collection`
  - Iterates over each item in a list, assigning it to `item` each pass.
- `END_EACH`
  - Ends a `FOR_EACH` loop.
- `PERHAPS_ALSO condition [FACT_ESTABLISHED]`
  - Acts as an `else if` branch inside a `PERHAPS` block.
- `BREAK_FROM_CAUCUS`
  - Exits the innermost active loop immediately.
- `NEXT_MOTION`
  - Skips to the next iteration of the innermost active loop.
- `SHOW_VARS`
  - Prints the active variable registry for debugging and live inspection.
- `RESET_CITIZENS`
  - Clears all stored variables and resets the live state.
- `APPEND_TO variable, value`
  - Appends a value to a list-like variable.
- `REMOVE_FROM variable, value`
  - Removes the first matching value from a list variable.
- `SORT_CITIZENS variable`
  - Sorts a list-like variable in ascending order.
- `AVERAGE_CITIZENS variable`
  - Computes the numeric average of a list-like variable and stores it in `variable_average`.

## Built-in Functions

- `DEBUNK(text)`
  - Normalizes MAGA-style text into lowercase fact-checked output.
- `FACT_CHECK_CROWD(value)`
  - Reduces an exaggerated crowd claim by a factor of 10.
- `TAX_THE_BILLIONAIRE(amount)`
  - Applies a 90% marginal tax above $1M.
- `DEFUND_OLIGARCHY(amount)`
  - Keeps 5% and redistributes the rest.
- `LIVING_WAGE(hours, base_rate=25.0)`
  - Calculates income for a fair living wage.
- `UNIVERSAL_BASIC_INCOME(population, grant=2000.0)`
  - Calculates a universal payment pool.
- `CARBON_OFFSET(emissions_tons)`
  - Calculates renewable rebate funds.
- `CELEBRATE_DIVERSITY(*items)`
  - Formats an inclusive community list.
- `UNIONIZE(*workers)`
  - Creates a union member list.
- `SCIENCE_FACT(topic)`
  - Returns peer-reviewed consensus statements.
- `PEER_REVIEWED_SQRT(value)`
  - Computes the square root.
- `SCIENCE_ROUND(value, decimals=2)`
  - Rounds numbers with scientific precision.
- `READ_RESOURCE(path)`
  - Reads a public resource file. Raises an error (which
    `UNIVERSAL_HEALTHCARE` can catch) when the file cannot be opened.
- `PUBLISH_RESEARCH(path, content)`
  - Writes a research file, returning True/False.
- `FORMAT_CURRENCY(value)`
  - Formats numeric values as currency.
- `CAD_CURRENCY(value)`
  - Alias for `FORMAT_CURRENCY`.
- `HONEY_BADGER_DEBUNK(claim)`
  - Produces a satirical debunk message.
- `HONEY_BADGER_BITE(target)`
  - Produces a fierce rebuttal.
- `HONEY_BADGER_STRIKE(action)`
  - Produces a strike declaration.
- `SAY_SORRY(message)`
  - Delivers contrition with maple syrup sincerity.
- `MAKE_IT_RAIN(amount)`
  - Redistributes wealth into healthcare, transit, and doughnuts.
- `PUBLIC_TRANSIT_FARE(distance, base_fare=3.50)`
  - Calculates a polite transit fare, inclusive of civic service fees.
- `TOQUE_WARMTH(temp_celsius)`
  - Converts temperature into a toque-warmth alert.
- `TRUTH_METER(claim)`
  - Scores sincerity with a Canadian humour rating.
- `MAKE_IT_SNOW(forecast, flakes=100)`
  - Predicts a satirical protest snowstorm.
- `FAT_CATS_TAX(amount)`
  - Tells the wealthy it’s time to lose a few zeros.
- `DONUT_DIVIDEND(amount)`
  - Spreads pastry payouts across the solidarity front.
- `NATIONAL_STOOGE(statement)`
  - Emits a spin-heavy public statement with extra nonsense.
- `GREEN_NEW_DEAL(goal)`
  - Declares an electrified visionary public policy agenda.
- `RHETORICAL_QUESTION(question)`
  - Asks a question where the answer is obviously evidence-based.
- `LOONIE_LOOP(count)`
  - Generates a whimsical set of symbolic loonies.
- `SOCIAL_LICENSE(name)`
  - Confirms approval from unionized beavers and open-source poets.
- `ELECTORATE_PULSE(value)`
  - Reports a fun mock-stat poll percentage.
- `COLLECTIVE_LIST value1, value2, ...`
  - Creates a list of values, including the shorthand BASIC-style call form used in scripts.
- `MUTUAL_AID_REGISTRY key = value, ...`
  - Creates a dictionary of named values.
- `CITIZEN_COUNT(...)`
  - Returns the number of items in a collection or argument list.
- `CITIZEN_AT(list, index)`
  - Returns the item at the given zero-based index in a list.
- `FIRST_CITIZEN(list)`
  - Returns the first item in a list.
- `LAST_CITIZEN(list)`
  - Returns the last item in a list.
- `JOIN_COLLECTIVE(list, separator)`
  - Joins list items into a single string using the separator.
- `MATH_ABS(value)`
  - Returns the absolute value.
- `MATH_FLOOR(value)`
  - Rounds down to the nearest integer.
- `MATH_CEIL(value)`
  - Rounds up to the nearest integer.
- `MATH_MIN(a, b, ...)`
  - Returns the smallest of the given values.
- `MATH_MAX(a, b, ...)`
  - Returns the largest of the given values.
- `RANDOM_DEMOCRACY(lo, hi)`
  - Returns a random integer between `lo` and `hi` inclusive.
- `STR_UPPER(text)`
  - Converts text to uppercase.
- `STR_LOWER(text)`
  - Converts text to lowercase.
- `STR_LEN(text)`
  - Returns the character length of text.
- `STR_TRIM(text)`
  - Strips leading and trailing whitespace from text.
- `STR_CONTAINS(text, substring)`
  - Returns `EVIDENCE_BASED` if substring is found in text.
- `STR_REPLACE(text, old, new)`
  - Replaces all occurrences of old with new in text.
- `STR_SPLIT(text, delimiter)`
  - Splits text into a list on the given delimiter.
- `TO_NUMBER(text)`
  - Converts a text value to an integer or float.
- `TO_TEXT(value)`
  - Converts any value to its text representation.
- `SORT_CITIZENS(list)`
  - Returns a sorted copy of list values.
- `AVERAGE_CITIZENS(list)`
  - Returns the numeric average of list values.
- `COLLECTIVE_APPEND(target, item)`
  - Returns a list with item appended to target.
- `MEDIAN_CITIZENS(values)`
  - Returns the median of a collection of numbers.
- `CITIZEN_SUM(values)`
  - Returns the numeric total of a collection.
- `CITIZEN_ANY(values)`
  - Returns `EVIDENCE_BASED` when any value is truthy.
- `CITIZEN_ALL(values)`
  - Returns `EVIDENCE_BASED` when every value is truthy.
- `GROUP_BY_CITIZENS(values, categories)`
  - Builds a registry grouping values by matching category.
- `COUNT_BY_CITIZENS(values, target)`
  - Counts how many values equal target.
- `REGISTRY_GET(registry, key, default)`
  - Reads a key from a registry, falling back to default.
- `REGISTRY_KEYS(registry)`
  - Returns a list of registry keys.
- `REGISTRY_VALUES(registry)`
  - Returns a list of registry values.
- `EVIDENCE_SCORE(claim, evidence)`
  - Scores a claim 0–100 based on how much evidence it cites.
- `POLICY_SCORE(policy, criteria)`
  - Scores a policy 0–100 against its review criteria.
- `PARLIAMENT_GAZETTE(title, content)`
  - Records an official parliamentary notice.
- `POLL_THE_PEOPLE(question, agreement)`
  - Reports a clamped (0–100%) public agreement figure.
- `CIVIC_COMPROMISE(proposal_a, proposal_b)`
  - Merges two proposals and refers the result to three committees.
- `RIGGED_ELECTION_METER(claim)`
  - Reviews election claims and asks for evidence first.
- `VOTER_SUPPRESSION_ALERT(tactic)`
  - Flags a suppression tactic and calls for expanded access.
- `CORPORATE_FINE(company, violation, amount)`
  - Assesses a fine and asks shareholders to read the receipt.
- `WORKPLACE_SAFETY_AUDIT(workplace)`
  - Requires hazard checks, paid training, and safe reporting.
- `INDIGENOUS_LAND_RETURN(territory, people)`
  - Records a land-return commitment requiring consultation and consent.
- `INDIGENOUS_CONSULTATION_REQUIRED(project)`
  - Requires early, meaningful consultation and consent.
- `TREATY_OBLIGATION_TRACKER(treaty)`
  - Tracks ongoing treaty review, accountability, and action.
- `RENEWABLE_ENERGY_TARGET(percent, year)`
  - States a clean-energy target as a percentage and year.
- `WAGE_THEFT_RECOVERY(amount)`
  - Returns recovered wages to workers.
- `AFFORDABLE_HOUSING_BUILT(units, location)`
  - Announces affordable homes, key ceremony included.
- `ACCESSIBILITY_AUDIT(building)`
  - Lists the access features a building still owes the public.
- `ACCOMMODATION_APPROVED(request)`
  - Approves an accommodation; dignity is not optional.
- `PUBLIC_SERVICE_WAIT(service, minutes)`
  - Publishes a service queue wait time.
- `EMISSIONS_REDUCED(baseline, current)`
  - Computes the percentage reduction against a baseline.
- `CLIMATE_RISK_SCORE(place, score)`
  - Reports a clamped 0–100 climate risk score.
- `SCIENCE_CONSENSUS(topic)`
  - Returns the peer-reviewed consensus for a known topic.
- `COMMUNITY_CARE_PLAN(need, response)`
  - Pairs a community need with a funded care response.

## Operator Aliases

- `WEALTH_TAX` -> `-`
- `EQUAL_PAY` -> `+`
- `PROPORTIONAL_SHARE` -> `/`
- `FAIR_MULTIPLIER` -> `*`
- `POWER_TO_THE_PEOPLE` -> `**`
- `MAPLE_SYRUP` -> `%`
- `MOONSHOT` -> `**`
- `AND` / `OR` / `NOT` -> `and` / `or` / `not` (lowercase forms also work)

## Literals

- `EVIDENCE_BASED` -> `True`
- `ALTERNATIVE_FACT` -> `False`
- `CLASSIFIED_MAR_A_LAGO` -> `None`

## Package entry points and launchers

The project exposes the following installed entry points after installation:

```bash
python3 -m pip install -e .
lake-ontario-ide
lake-ontario-basic --help
lake-ontario-cli
```

The bundled launcher also bootstraps a local `.venv` and then starts the GUI:

```bash
python3 run_ide.py
```

The classic interpreter entry point from the repository root is:

```bash
python3 interpreter.py examples/hello.lo
python3 interpreter.py --repl
```

## IDE

Run the interactive development environment with:

```bash
python3 ide.py
```

Use the IDE to edit scripts, run examples, and consult the command reference.
