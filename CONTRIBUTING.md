# Contributing to Lake Ontario BASIC

Thanks for being interested in improving Lake Ontario BASIC. The project exists to make a weird, playful, truth-seeking language that is also useful, teachable, and technically solid.

Whether you are fixing a bug, improving the docs, adding a language feature, polishing the examples, or just helping the interpreter behave more politely, contributions are welcome.

## Ways to contribute

You can help by:

- fixing interpreter bugs or edge cases
- improving docs and learning materials
- adding or refining language examples
- improving CLI, IDE, or output behavior
- suggesting features that fit the project’s tone and goals
- reviewing pull requests and helping triage issues

## Project values

Lake Ontario BASIC should remain:

- evidence-aware rather than performatively deceptive
- respectful without being bland
- satirical without becoming hostile or cruel
- practical enough to run real examples and teach real concepts
- open to experimentation, as long as it remains understandable and maintainable

If a feature idea turns the project into a generic parody or introduces chaos without clarity, it may need revision before merge.

## Before you start

1. Read the project overview in [README.md](README.md).
2. Check the issue tracker to see whether a bug or feature already exists.
3. Keep changes focused and easy to review.
4. Prefer small, well-explained pull requests over broad rewrites.

## Local setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

You can then run the interpreter and examples with:

```bash
python3 interpreter.py --help
python3 interpreter.py examples/hello.lo
python3 run_ide.py
```

## Development workflow

### 1. Create a branch

Use a focused branch name that reflects the change, such as:

- `fix-boolean-evaluation`
- `doc-language-reference`
- `feature-new-stdlib-call`

### 2. Make a clear change

Keep the scope tight. A good contribution usually includes:

- a small, explainable code change
- tests or validation when relevant
- updated docs if behavior or syntax changed
- a clear summary in the pull request description

### 3. Validate before opening a PR

Run the relevant checks for your change. At minimum, try:

```bash
python3 -m compileall .
python3 interpreter.py --doctor
python3 interpreter.py examples/hello.lo
```

If you are changing parser or runtime behavior, also run the project test suite if present:

```bash
python3 tests.py
```

### 4. Open a pull request

Your pull request should explain:

- what changed
- why the change matters
- how it was validated
- any risk or follow-up work

Please keep the tone respectful and professional. This project is intentionally playful, but the review process should remain calm and constructive.

## Coding expectations

- Prefer readable, maintainable Python.
- Keep naming and structure consistent with the rest of the codebase.
- Write docs for behavior changes when they affect users.
- Avoid introducing unnecessary dependencies.
- Preserve the project’s tone and syntax conventions where possible.

## Pull request etiquette

- Be respectful with review feedback.
- Don’t take criticism personally; treat review comments as part of building a better interpreter.
- If you disagree with a suggestion, explain your reasoning clearly and calmly.
- If a change is too broad, shrink it down and re-submit a tighter version.

## Reporting issues

When opening an issue, include:

- a short description of the bug or idea
- the exact command or input that triggered it
- expected behavior vs actual behavior
- relevant environment details (Python version, OS, command output)

This makes the issue easier to reproduce and fix.

## Community expectations

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing. We are building a project with humor, integrity, and mutual respect, and the community is expected to uphold that standard.

## Final note

The best contributions are the ones that make the language more fun, clearer, and more useful without compromising trust, quality, or community health. We’re here to strengthen the weird little democratic interpreter, not to turn it into a dumpster fire.
