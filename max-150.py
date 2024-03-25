from vector import Vector, cross_prod, Element, Load, Machine, Rotation, Gravity
import copy


# Notes
# All units are in inches and pounds


# Variables
feed_pos = 0 # range [0-160] inch 0 is at bottom of mast
mast_angle = 90 # range [95 - 0] degree, 0 degree is laying flat

# track_304 = element.track(length=87.2, width=13.8, height=19.1, mass=922, cg=(0,0,0), load_capacity=8200, tractive_effort=8025)
# track_306 = element.track(length=102, width=15.8, height=21.4, mass=2260, cg=(0,0,0), load_capacity=15000, tractive_effort=12246)
# track_305e2 = element.track(length=101.8, width=15.8, height=21.4, mass=1961, cg=(0,0,0), load_capacity=12000, tractive_effort=13278)
# track_308 = element.track(length=104.3, width=17.7, height=26.1, mass=2000, cg=(0,0,0), load_capacity=20940, tractive_effort=116850)

# carbody = element.Element(length=56, width=36.6, height=10, mass=2000, cg=(0,0,0))



## Components
max150 = Machine() # Set a machine with default gravity

base = Element(name='base')


# Track 308 (this is for the 2 tracks)
track_cg_pos = Vector(44.85, 14) #position of the element load in it's own referential xy
track_cg = Load(track_cg_pos, 4000, _type='mass') #load details (this one is mass only)
base.loads.append(track_cg) # add the load to the base referential loads

platform_pos = Vector(60, 3)
platform = Load(platform_pos, 2000, _type='mass')
base.loads.append(platform.move(-15.15, 30)) # move platform in base referential and move it in place.

mast_base_pos = Vector(16, 16)
mast_base = Load(mast_base_pos, 2000, _type='mass')
base.loads.append(mast_base.move(-15.15, 36)) # the mast base is positioned at -3, 15 in the base element

max150.elements.append(base)
print('base reactions:', base.reactions(gravity=Gravity()))



mast = Element(name='mast')

# We add the mast loads laying down and will rotate it once all components are added (instead of rotating each components)

pivot_mast_pos = Vector(16, -10)
pivot_mast = Load(pivot_mast_pos, 800, _type='mass')
mast.loads.append(pivot_mast)

mast_mast_pos = Vector(80, 8)
mast_mast = Load(mast_mast_pos, 4000, _type='mass')
mast.loads.append(mast_mast.move(-10, 8))

head_mast_pos = Vector(12, 12)
head_mast = Load(head_mast_pos, 400, _type='mass')
mast.loads.append(head_mast.move(feed_pos, 16))


max150.elements.append(mast)

mast.move(Vector(-8, 12)) # move the mast element to center it's origin at pivot point on mast-pivot hinge
mast.rotate(Rotation(gamma=90)) # It's important to rotate before moving as you are rotating around the moved origin

mast_alone = copy.deepcopy(mast) # Take a snapshot of the mast to make calculation on solely this portion.
mast.move(Vector(-7.15, 60)) # move the mast element to the base-pivot point in the machine referential

reactions = max150.reactions()



# mast_alone.move(Vector(-7.15, 60))
# mast_alone.move(Vector(7.15, -60)) # move back the mast alone to it's origin at pivot.
print(reactions)
print()
print('mast_alone', mast_alone.reactions(gravity=Gravity()))