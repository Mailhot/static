# This is a test the result should be: 
# [(-9.797174393178826e-13, -18944.0, 0.0), (0.0, 0.0, 1019376.0)]

from vector import Vector, cross_prod, Element, Load, Machine, Rotation




## Components
max150 = Machine() # Set a machine with default gravity

base = Element(name='base')


track_pos = Vector(60, 10) #position of the element load in it's own referential xy
track = Load(track_pos, 8000, _type='mass') #load details (this one is mass only)
base.loads.append(track) # add the load to the base referential loads

platform_pos = Vector(60, 8)
platform = Load(platform_pos, 4000, _type='mass')
base.loads.append(platform.move(-16, 20)) # move platform in base referential and move it in place.

mast_base_pos = Vector(10, -16)
mast_base = Load(mast_base_pos, 1200, _type='mass')
base.loads.append(mast_base.move(-10, 36)) # the mast base is positioned at -3, 15 in the base element

max150.elements.append(base)



mast = Element(name='mast')

# We add the mast loads laying down and will rotate it once all components are added (instead of rotating each components)

pivot_mast_pos = Vector(20, 20)
pivot_mast = Load(pivot_mast_pos, 800, _type='mass')
mast.loads.append(pivot_mast)

mast_mast_pos = Vector(90, 8)
mast_mast = Load(mast_mast_pos, 6000, _type='mass')
mast.loads.append(mast_mast.move(-10, 26))

head_mast_pos = Vector(15, 10)
head_mast = Load(head_mast_pos, 600, _type='mass')
mast.loads.append(head_mast.move(8, 42))


max150.elements.append(mast)


mast.move(-10, 36) # the origin of the mast element is the pivot hinge

mast.rotate(Rotation(gamma=90)) # It's important to rotate before moving as you are rotating around the moved origin


print(max150.reactions())




