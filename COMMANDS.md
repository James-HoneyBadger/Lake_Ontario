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
  - Outputs text or values to standard output.
- `TOWN_HALL variable_name`
  - Prompts the user and stores the input.
- `PERHAPS condition FACT_ESTABLISHED`
  - Starts a conditional block.
- `STILL_IN_DENIAL`
  - Starts the `else` branch of a conditional block.
- `END_PERHAPS`
  - Ends a conditional block.
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
- `CLEAR_GRAPHICS`
  - Clears the GUI graphics canvas while running in the GUI IDE.
- `DRAW_LINE x1, y1, x2, y2`
  - Draws a line on the GUI canvas.
- `DRAW_RECTANGLE x, y, width, height`
  - Draws a rectangle on the GUI canvas.
- `FILL_RECTANGLE x, y, width, height`
  - Draws a filled rectangle on the GUI canvas.
- `DRAW_CIRCLE x, y, radius`
  - Draws a circle on the GUI canvas.
- `FILL_CIRCLE x, y, radius`
  - Draws a filled circle on the GUI canvas.
- `DRAW_TEXT x, y, text`
  - Draws text on the GUI canvas.
- `WAIT milliseconds`
  - Pauses execution for the given number of milliseconds.

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
  - Reads a public resource file.
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
- `SORT_CITIZENS variable`
  - Sorts a list-like variable in ascending order.
- `AVERAGE_CITIZENS variable`
  - Computes the numeric average of a list-like variable and stores it in `variable_average`.
- `SHOW_VARS`
  - Prints the active variable registry for debugging and live inspection.
- `RESET_CITIZENS`
  - Clears all stored variables and resets the live state.
- `APPEND_TO variable, value`
  - Appends a value to a list-like variable.

## Operator Aliases

- `WEALTH_TAX` -> `-`
- `EQUAL_PAY` -> `+`
- `PROPORTIONAL_SHARE` -> `/`
- `FAIR_MULTIPLIER` -> `*`
- `POWER_TO_THE_PEOPLE` -> `**`
- `MAPLE_SYRUP` -> `%`
- `MOONSHOT` -> `**`

## Literals

- `EVIDENCE_BASED` -> `True`
- `ALTERNATIVE_FACT` -> `False`
- `CLASSIFIED_MAR_A_LAGO` -> `None`

## IDE

Run the interactive development environment with:

```bash
python3 ide.py
```

Use the IDE to edit scripts, run examples, and consult the command reference.
