import pytest

from vector import Vector, Element, Load, Machine, Rotation, Gravity


def build_two_arm_machine():
    """Two mass loads on a shared sub-assembly, one of them moved off-origin."""
    machine = Machine(gravity=Gravity())
    load1 = Load(Vector(10, 10), 10, _type='mass')
    load2 = Load(Vector(10, 0), 20, _type='mass')
    element2 = Element(loads=[load2], name='ele load2').move(Vector(20, 20))
    element1 = Element(loads=[load1], name='ele load1')
    element3 = Element(elements=[element1, element2], name='combined arms')
    machine.elements = [element3]
    return machine, element3, load2


def test_basic_reactions():
    machine, _element3, _load2 = build_two_arm_machine()
    reactions = machine.reactions()
    assert reactions['forces'] == Vector(0, -30, 0)
    assert reactions['moments'] == Vector(0, 0, -700)


def test_rotation_sequence_accumulates():
    # Rotating the combined-arms element by repeated 90deg steps rotates the
    # resulting moment through this expected sequence.
    machine, element3, _load2 = build_two_arm_machine()

    element3.rotate(Rotation(0, 0, 90))
    reactions = machine.reactions()
    assert reactions['forces'] == Vector(0, -30, 0)
    assert reactions['moments'] == Vector(0.0, 0.0, 500.0)

    element3.rotate(Rotation(0, 0, 90))
    reactions = machine.reactions()
    assert reactions['forces'] == Vector(0, -30, 0)
    assert reactions['moments'] == Vector(0.0, 0.0, 700.0)

    element3.rotate(Rotation(0, 0, 90))
    reactions = machine.reactions()
    assert reactions['forces'] == Vector(0, -30, 0)
    assert reactions['moments'] == Vector(0.0, 0.0, -500.0)


@pytest.mark.xfail(strict=True, reason=(
    "Element.rotate()/.move() append to both self.rotations/self.moves AND "
    "self.ops. Clearing only element.rotations (bypassing reset_transform()) "
    "leaves self.ops still carrying the old rotations down to child elements, "
    "so this does not actually undo the rotation. Use reset_transform() "
    "instead - see test_reset_transform_clears_everything below."
))
def test_resetting_only_rotations_list_does_not_clear_ops():
    machine, element3, load2 = build_two_arm_machine()
    element3.rotate(Rotation(0, 0, 90))
    element3.rotate(Rotation(0, 0, 90))
    element3.rotate(Rotation(0, 0, 90))

    element3.rotations = []  # intent: undo element3's rotation
    load2.rotate(Rotation(0, 0, -90))
    reactions = machine.reactions()
    assert reactions['forces'] == Vector(0, -30, 0)
    assert reactions['moments'] == Vector(0.0, 0.0, -500.0)


def test_reset_transform_clears_everything():
    machine, element3, load2 = build_two_arm_machine()
    element3.rotate(Rotation(0, 0, 90))
    element3.rotate(Rotation(0, 0, 90))
    element3.rotate(Rotation(0, 0, 90))

    element3.reset_transform()
    load2.rotate(Rotation(0, 0, -90))
    reactions = machine.reactions()
    assert reactions['forces'] == Vector(0, -30, 0)
    assert reactions['moments'] == Vector(0.0, 0.0, -500.0)
