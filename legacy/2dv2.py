from vector import Vector, cross_prod, Element, Load, Machine


# current position
mast_angle = 90 #mast angle taken from horizontal
holdback = 8000 #lbs
feed_position = 20 # [0-158 inches]a  distance value in inches for the feed positoin
mast_slide_position = 20 # [0-40 inches] distance value for the mast slide position

## Components
max150 = Machine() # Set a machine with default gravity

base = Element()

track_pos = Vector(30, 5) #position of the element load in it's own referential xy
track = Load(track_pos, 10, _type='mass') #load details (this one is mass only)
base.loads.append(track) # add the load to the base referential loads

platform_pos = Vector(33, 5)
platform = Load(platform_pos, 20, _type='mass')
base.loads.append(platform.move(-3, 10)) # move platform in base referential and move it in place.

mast_base_pos = Vector(5, 5)
mast_base = Load(mast_base_pos, 10, _type='mass')
base.loads.append(mast_base.move(-3 - mast_slide_position, 15)) # the mast base is positioned at -3, 15 in the base element

engine_base_pos = Vector(22.5, 20)
engine_base = Load(engine_base_pos, 450, _type='mass')
base.loads.append(engine_base.move(30, 35))

pump_base_pos = Vector(8, 5) # #7 - Pumps (2x tandem K3VL60)
pump_base = Load(pump_base_pos, 110, _type='mass')
base.loads.append(pump_base.move(10, 35))

jack_base_pos = Vector(60, 25) # #8 - Jacks (4x of them)
jack_base = Load(jack_base_pos, 800, _type='mass') 
base.loads.append(jack_base.move(0, 30))





mast = Element()
# We add the mast loads laying down and will rotate it once all components are added (instead of rotating each components)

pivot_mast_pos = Vector(7, 7)
pivot_mast = Load(pivot_mast_pos, 12, _type='mass')
base.loads.append(pivot_mast)

mast_mast_pos = Vector(60, 8)
mast_mast = Load(mast_mast_pos, 40, _type='mass')
mast.loads.append(mast_mast.move(-20, 10))

head_mast_pos = Vector(15, 10)
head_mast = Load(head_mast_pos, 20, _type='mass')
mast.loads.append(head_mast.move(-20+feed_position, 34))

feed_force_mast_pos = Vector(0, 12) # # 21 - drilling force
feed_force_mast = Load(feed_force_mast_pos, Vector(-holdback, 0), _type='force')
mast.loads.append(feed_force_mast.move(-20+feed_position, 34))


max150.elements.append(base)
max150.elements.append(mast)

mast.move(-1, 7) # the origin of the mast element is the pivot hinge
mast.rotate(gamma=mast_angle)


# reactions = max150.reactions()
# if reactions == []
print(max150.reactions())




