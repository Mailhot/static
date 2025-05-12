import vector


def test_machine_reaction():

    ## Components
    machine1 = Machine(gravity=Gravity()) # Set a machine with default gravity

    group1 = Element(name='Group')
    machine1.elements.append(element1)

    # 2-1 Head (Sliding table)
    head = Element(name="Head", length=30, width=20, height=16)
    head_mast_pos = Vector(10, 12)
    head_mast = Load(head_mast_pos, 600, _type='mass')
    head.loads.append(head_mast)

    mast.elements.append(head)


    feed_force_mast_pos = Vector(0, 12) # # 21 - drilling force
    feed_force_mast = Load(feed_force_mast_pos, Vector(holdback, 0), _type='force')
    head.loads.append(feed_force_mast)

    torque_mast_pos = Vector(0, 12)
    torque_mast_load = Load(torque_mast_pos, Vector(rotation_max_torque, 0, 0), _type='moment')
    head.loads.append(torque_mast_load)

    # 2-2 Mast 
    mast_mast = Element(name='Mast', length=160, width=16, height=16)
    mast_mast_cg_pos = Vector(80, 8)
    mast_mast_cg = Load(mast_mast_cg_pos, 6000, _type='mass')
    mast_mast.loads.append(mast_mast_cg)
    mast.elements.append(mast_mast.move(Vector(-10-mast_slide_position, 0))) # Move the mast 10 inch from bottom (where the pivot will likely be)

    head.move(Vector(feed_position, 16))


    # 2-3 Mast-Pivot
    mast_pivot = Element(name='Mast Pivot', length=40, width=22, height=16)
    pivot_mast_pos = Vector(16, -10)
    pivot_mast = Load(pivot_mast_pos, 800, _type='mass')
    mast_pivot.loads.append(pivot_mast)
    mast.elements.append(mast_pivot)

    mast.offset = Vector(-8, 12) # Center at pivot point
    mast.rotate(Rotation(gamma=mast_angle))

    print('-----mast', mast)
    # print('equivalent loads:', mast.reactions(gravity=Gravity()))



    # # We add the mast loads laying down and will rotate it once all components are added (instead of rotating each components)


    # ## Swivel



    # mast.move(Vector(-7.15, 60)) # move the mast element to the base-pivot point in the machine referential




    base = Element(name='Base Group')
    max150.elements.append(base)
    # 1-3
    pivot_base = Element(name='Base Pivot', length=36, width=24, height=36)
    pivot_base_cg_pos = Vector(16, 16)
    pivot_base_cg = Load(pivot_base_cg_pos, 2000, _type='mass')
    pivot_base.loads.append(pivot_base_cg)
    base.elements.append(pivot_base)
    mast.offset.move(Vector(8, 24)) # Move the mast assy to center at the base-pivot point
    # base.elements.append(pivot_base.move(Vector(-15.15, 36, 0))) # the mast base is positioned at -3, 15 in the base element
    # 1-2
    platform = Element(name='Platform', length=120, width=72, height=6)
    platform_pos = Vector(60, 3)
    platform_cg = Load(platform_pos, 2000, _type='mass')
    platform.loads.append(platform_cg)
    base.elements.append(platform)
    pivot_base.move(Vector(0, 6))
    mast.offset.move(Vector(0, 6))
