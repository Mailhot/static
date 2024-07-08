from vector import Vector, cross_prod, Element, Load, Machine, Rotation, Gravity
import copy
import sys


# Notes
# All units are in inches and pounds

# Variables
# Head

# # Case 1 - 90 deg, mast slide up, feed up, torque max clockwise, feed up max
# rotation_max_torque = 42000 # 42000 lb-in (Positive is counterclockwise)
# mast_angle = 90 # range [95 - 0] degree, 0 degree is laying flat
# holdback = -11000 # Lbs [-11000 to 6000] feed up force) Minus is force directed toward bast foot

# Case 2 - 0 deg, mast slide up, feed up
rotation_max_torque = 0 # 42000 lb-in (Positive is counterclockwise)
mast_angle = 0 # range [95 - 0] degree, 0 degree is laying flat
holdback = 0 # Lbs [-11000 to 6000] feed up force) Minus is force directed toward bast foot

feed_position = 0 # range [0-160] inch 0 is at bottom of mast
mast_slide_position = 0 # [0-40] inch 0 is the mast slide raised up all the way

machine_width = 72 # overall width of the mahine (preliminary guess)

# Track cat 308
track_width = 26.1 # 308
track_length = 114.3
track_height = 26.1
track_ground_length = 89.7
track_mass = 4415 # [lbs] TODO: check with cat if mass is really for the 2 or per side

rod_rack_angle = 85 # [between 30 and 85 degree] 90 is vertical


# track_304 = element.track(length=87.2, width=13.8, height=19.1, mass=922, cg=(0,0,0), load_capacity=8200, tractive_effort=8025)
# track_306 = element.track(length=102, width=15.8 , height=21.4, mass=2260, cg=(0,0,0), load_capacity=15000, tractive_effort=12246)
# track_305e2 = element.track(length=101.8, width=15.8, height=21.4, mass=1961, cg=(0,0,0), load_capacity=12000, tractive_effort=13278)
# track_308 = element.track(length=104.3, width=17.7, height=26.1, mass=2000, cg=(0,0,0), load_capacity=20940, tractive_effort=116850)

# carbody = element.Element(length=56, width=36.6, height=10, mass=2000, cg=(0,0,0))



## Components
max150 = Machine(gravity=Gravity()) # Set a machine with default gravity

mast = Element(name='Mast Group')
max150.elements.append(mast)

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


# # 2-3 Mast-Pivot
# mast_pivot = Element(name='Mast Pivot', length=40, width=22, height=16)
# pivot_mast_pos = Vector(16, -10)
# pivot_mast = Load(pivot_mast_pos, 800, _type='mass')
# mast_pivot.loads.append(pivot_mast)
# mast.elements.append(mast_pivot)

# mast.move(Vector(-8, 12)) # Center at pivot point
# mast.rotate(Rotation(gamma=mast_angle))

print('-----mast', mast)
# print('equivalent loads:', mast.reactions(gravity=Gravity()))



# # We add the mast loads laying down and will rotate it once all components are added (instead of rotating each components)


# ## Swivel



# mast.move(Vector(-7.15, 60)) # move the mast element to the base-pivot point in the machine referential




#### base = Element(name='Base Group')
#### max150.elements.append(base)
###
#### # 1-3
#### pivot_base = Element(name='Base Pivot', length=36, width=24, height=36)
#### pivot_base_cg_pos = Vector(16, 16)
#### pivot_base_cg = Load(pivot_base_cg_pos, 2000, _type='mass')
#### pivot_base.loads.append(pivot_base_cg)
#### base.elements.append(pivot_base)
#### mast.offset.move(Vector(8, 24)) # Move the mast assy to center at the base-pivot point
#### # base.elements.append(pivot_base.move(Vector(-15.15, 36, 0))) # the mast base is positioned at -3, 15 in the base element
###
#### # 1-2
#### platform = Element(name='Platform', length=120, width=72, height=6)
#### platform_pos = Vector(60, 3)
#### platform_cg = Load(platform_pos, 2000, _type='mass')
#### platform.loads.append(platform_cg)
#### base.elements.append(platform)
#### pivot_base.move(Vector(0, 6))
#### mast.offset.move(Vector(0, 6))


# base.elements.append(platform.move(Vector(-15.15, 30, 0))) # move platform in base referential and move it in place.


# # Track 308 (this is for the 2 tracks)
# # 1-1
# track = Element(name='track pair', length=track_length, width=machine_width, height=track_height)
# track_z_position = (machine_width/2)-(track_width/2)
# track_l_cg_pos = Vector(57.15, 14, track_z_position) # position of the element load in it's own referential xy
# track_r_cg_pos = Vector(57.15, 14, -track_z_position) # position of the element load in it's own referential xy

# track_cg_l = Load(track_l_cg_pos, track_mass/2, _type='mass') # load details (this one is mass only)
# track_cg_r = Load(track_r_cg_pos, track_mass/2, _type='mass')
# track.loads.append(track_cg_l) # add the load to the base referential loads
# track.loads.append(track_cg_r) # add the load to the base referential loads

# # print(moved_track.moves)
# base.elements.append(track)
# platform.move(Vector(0, 30))
# pivot_base.move(Vector(0, 30))
# mast.offset.move(Vector(0, 30))

# # Move mast and base to the track origin
# mast.offset.move(Vector(-15, 0))
# base.offset.move(Vector(-15, 0))



###
#### 4- Engine
#### We plan on using CAT C3.6 74Hp for now (took a bigger engine to leave plase in case we need it)
###engine = Element(name='Engine', length=46.3, width=22.2, height=33.7)
###engine_base_pos = Vector(13.4, 16.85, 0)
###engine_base = Load(engine_base_pos, 1226, _type='mass')
###engine.loads.append(engine_base)
###base.elements.append(engine.move(Vector(30, 36, 0)))
###
###
#### 5 - Pumps (2x tandem K3VL60)
#### Approx dimensions
###hyd_pumps = Element(name='Hydraulic Pumps', length=16, width=10, height=10)
###hyd_pumps_base_pos = Vector(8, 5)
###hyd_pumps_base = Load(hyd_pumps_base_pos, 110, _type='mass')
###hyd_pumps.loads.append(hyd_pumps_base)
###base.elements.append(hyd_pumps.move(Vector(6, 36, 0)))
###
#### 6 - Jacks (4x of them)
###jacks = Element(name='Jacks', length=120, width=72, height=40)
###jacks_cg_pos = Vector(60, 25)
###jacks_cg = Load(jacks_cg_pos, 800, _type='mass')
###jacks.loads.append(jacks_cg)
###base.elements.append(jacks.move(Vector(0, 12, 0)))
###
#### 7 - Hydraulic Tank
###hydraulic_tank = Element(name='Hydraulic Tank', length=42, width=8, height=24)
###tank_cg_pos = Vector(21, 12)
###tank_cg = Load(tank_cg_pos, 375, _type='mass')
###hydraulic_tank.loads.append(tank_cg)
###base.elements.append(hydraulic_tank.move(Vector(60, 50, -16)))
###
#### 8 - rod rack 
###rod_rack = Element(name='Rod Rack', length=130, width=20, height=24)
###rack_base_pos = Vector(65, 12)
###rack_base = Load(rack_base_pos, 4300, _type='mass')
###rack_base.rotate(Rotation(gamma=rod_rack_angle))
###
###rod_rack.loads.append(rack_base)
###rod_rack.move(Vector(-40, 10, 15))
###base.elements.append(rod_rack)

# max150.elements.append(base)
# # print('base reactions:', base.reactions(gravity=Gravity()))






## mast_alone = copy.deepcopy(mast) # Take a snapshot of the mast to make calculation on solely this portion.
print('')
reactions = max150.reactions()
print('Equivalent Load:', reactions)


# mast_alone.move(Vector(-7.15, 60))
# mast_alone.move(Vector(7.15, -60)) # move back the mast alone to it's origin at pivot.

# print('mast_alone', mast_alone.reactions(gravity=Gravity()))

