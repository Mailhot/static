from vector import Vector, Element, Load, Machine, Rotation, Gravity, Point


def build_max250(holdback, rotation_max_torque, mast_angle,
                  feed_position, mast_slide_position, mast_weight,
                  head_weight, pivot_weight, head_pos, mast_pos):
    """Assemble the max250 Machine for a given set of configuration parameters.

    Hardab 12k4, relying on 7K4 drawing DDA0105, each center of mass is based on its own assy ref.
    Returns a Machine ready to call .reactions() on.
    """

    max250 = Machine(gravity=Gravity()) # Set a machine with default gravity

    head_group = Element(name='head_group')
    max250.elements.append(head_group)

    ## Head
    head = Element(name="head", length=14.84, width=18.5, height=15.625)
    head_cg_pos = Vector(*head_pos)
    head_cg = Load(head_cg_pos, head_weight, _type="mass")
    head.loads.append(head_cg)
    head_group.elements.append(head)

    ### Torque
    head_torque = Load(Vector(-13.10, 10.25, 0), Vector(rotation_max_torque, 0, 0), _type="moment")
    head.loads.append(head_torque)

    ### Feed force
    feed_force = Load(Vector(-13.254, 10.25, 0), Vector(holdback, 0, 0), _type="force")
    head.loads.append(feed_force)

    mast_group = Element(name='mast_group')
    max250.elements.append(mast_group)

    ## mast
    mast = Element(name="mast", length=245, width=10, height=12)
    mast_cg_pos = Vector(*mast_pos)
    mast_cg = Load(mast_cg_pos, mast_weight, _type="mass")
    mast.loads.append(mast_cg)
    mast_group.elements.append(mast)

    pivot_group = Element(name='pivot_group')
    max250.elements.append(pivot_group)

    ## pivot
    pivot = Element(name="pivot", length=83, width=17.5, height=17.5)
    pivot_cg_pos = Vector(-23.75, 6.19, 0.68)
    pivot_cg = Load(pivot_cg_pos, pivot_weight, _type="mass")
    pivot.loads.append(pivot_cg)
    pivot_group.elements.append(pivot)
    point1 = Point(-38.81, 3.35, 4.02, name='mast_lift_rod')
    pivot.points.append(point1)

    ## Base (only for mast lift cyl placement)
    base = Element(name="base", length=126, width=60, height=48)
    base_cg_pos = Vector(-36.54, -1.628, -5.03)
    base_cg = Load(base_cg_pos, 0, _type="mass")
    base.loads.append(base_cg)
    max250.elements.append(base)
    point2 = Point(-91.79, -21.44, -7.48, name='mast_lift_piston')
    base.points.append(point2)

    # Vector between coordinates
    R23 = Vector(-3.05-feed_position, 10.04, -10.22) #mast to table
    R12 = Vector(22.54+mast_slide_position, 7.28, 0.02) #pivot to mast
    # R01 is zero, other than the rotation the 2 coordinate between base and pivot are the same

    ## Displacement relative to each other
    head_group.move(R23).move(R12).rotate(Rotation(gamma=mast_angle))
    mast_group.move(R12).rotate(Rotation(gamma=mast_angle))
    pivot_group.rotate(Rotation(gamma=mast_angle))

    return max250
