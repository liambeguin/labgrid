from time import sleep

from labgrid import step, steps
from pytest import approx


@step("a")
def step_a(*, step):
    assert steps.get_current() is not None
    return step.level

@step("outer")
def step_outer(*, step):
    assert step.level == 1
    return step_a()

def test_single():
    assert steps.get_current() is None
    step_a()
    assert steps.get_current() is None

def test_nested():
    assert steps.get_current() is None
    inner_level = step_outer()
    assert steps.get_current() is None
    assert inner_level == 2

@step("timing")
def step_sleep(*, step):
    sleep(0.25)
    return step

def test_timing():
    step = step_sleep()
    assert step.duration == approx(0.25, abs=1e-2)
