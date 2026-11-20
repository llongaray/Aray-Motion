import pytest
from core.gestures import Point, distance, interpret_hand
from core.safety import GestureGate


def make_hand(pinch=False):
    points = [Point(0.5, 0.5) for _ in range(21)]
    points[0] = Point(0.5, 0.8)
    points[9] = Point(0.5, 0.4)
    points[8] = Point(0.5, 0.2)
    points[4] = Point(0.53, 0.21) if pinch else Point(0.8, 0.7)
    return points


def test_distance():
    assert distance(Point(0, 0), Point(3, 4)) == 5


def test_pinch():
    g = interpret_hand(make_hand(pinch=True))
    assert g.name == "pinch"
    assert g.cursor == Point(0.5, 0.2)


def test_point():
    assert interpret_hand(make_hand()).name == "point"


def test_bad_landmarks():
    with pytest.raises(ValueError):
        interpret_hand([Point(0, 0)])


def test_confirmation_gate():
    gate = GestureGate(hold_seconds=0.3, cooldown_seconds=0.5)
    assert not gate.update("pinch", 1.0, enabled=False)
    assert not gate.update("pinch", 2.0, enabled=True)
    assert not gate.update("pinch", 2.2, enabled=True)
    assert gate.update("pinch", 2.4, enabled=True)
    assert not gate.update("pinch", 2.5, enabled=True)
    assert gate.update("pinch", 3.0, enabled=True)


def test_reset_gate():
    gate = GestureGate(hold_seconds=0.1)
    assert not gate.update("pinch", 1.0, True)
    gate.reset()
    assert not gate.update("pinch", 1.2, True)
