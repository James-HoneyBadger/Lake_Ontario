"""pytest bridge for the Lake Ontario BASIC regression harness.

``tests.py`` stays the single source of truth so ``python3 tests.py`` keeps
working exactly as described in the README. This module simply lets
``python -m pytest`` collect the same checks, one test per harness function.
"""

import inspect

import pytest

import tests as harness

CHECKS = [
    check
    for name, check in vars(harness).items()
    if name.startswith("run_") and callable(check) and not inspect.signature(check).parameters
]


@pytest.mark.parametrize("check", CHECKS, ids=[check.__name__ for check in CHECKS])
def test_harness_check(check):
    assert check() is True
