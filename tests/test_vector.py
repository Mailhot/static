from vector import Vector, Rotation, Element, cross_prod


def test_vector_add_sub():
    assert Vector(1, 2, 3) + Vector(1, 1, 1) == Vector(2, 3, 4)
    assert Vector(1, 2, 3) - Vector(1, 1, 1) == Vector(0, 1, 2)


def test_vector_sum_supports_builtin_sum():
    # Vector.__radd__ makes sum([...]) work, relied on by Element.reactions().
    assert sum([Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)]) == Vector(1, 1, 1)


def test_vector_move_mutates_and_returns_self():
    # Regression: move() used to return self + move again (a double offset).
    v = Vector(1, 1, 0)
    result = v.move(Vector(2, 3, 0))
    assert v == Vector(3, 4, 0)
    assert result == Vector(3, 4, 0)
    assert result is v


def test_vector_rotate_90_about_z():
    v = Vector(1, 0, 0)
    v.rotate(Rotation(gamma=90))
    assert v == Vector(0, 1, 0)


def test_cross_prod():
    assert cross_prod(Vector(1, 0, 0), Vector(0, 1, 0)) == Vector(0, 0, 1)


def test_element_constructor_respects_moves_argument():
    # Regression: Element.__init__ used to discard the moves= argument.
    moves = [Vector(1, 0, 0)]
    element = Element(name='e', moves=moves)
    assert element.moves == moves
