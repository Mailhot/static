from vector import Vector, axle, cylinder_force
from models.max250 import build_max250
from configs.prj175 import one


def test_build_max250_case_one_reactions():
    machine = build_max250(**one)
    reactions = machine.reactions()
    reactions = axle((0, 0, 1), **reactions)

    assert reactions['forces'] == Vector(0.0, 10120.0, 0.0)
    assert round(reactions['moments'].z, 2) == 329862.81

    force = cylinder_force(reactions)
    assert round(force, 2) == 45759.81
