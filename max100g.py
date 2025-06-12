import display
from vector import Vector, cross_prod, Element, Load, Machine, Rotation, Gravity




# First thig, configure the system.

holdback = 11000 # Lbs [11000 to -6000] feed up force) Plus is force directed toward base 
rotation_max_torque = 4000 # [lbs-ft] max torque for T3500
mast_angle = -90 # [0-95] degree
feed_position = 157.5 # range [0-157.5] inch 0 is at bottom of mast
mast_slide_position = 48 # [0-48] inch 0 is the mast slide raised up all the way

X1 = 0 # [0-12] casing extension cylinder extended / retracted

max100 = Machine(gravity=Gravity()) # Set a machine with default gravity
head_group = Element(name='head_group Group')
max100.elements.append(head_group)


## Sliding Table
sliding_table = Element(name="sliding_table", length=52.25, width=28, height=5.375)
sliding_table_head_pos = Vector(-28.2385, 0.9192, 1.2987)
sliding_table_cg = Load(sliding_table_head_pos, 537, _type='mass')
sliding_table.loads.append(sliding_table_cg)
head_group.elements.append(sliding_table)

## Casing extension
casing_extension = Element(name="casing_extension", length=20.25, width=13.25, height=10.5)
casing_extension_cg_pos = Vector(-9.4189+X1, 6.6808, 0.0059)
casing_extension_cg = Load(casing_extension_cg_pos, 59, _type='mass')
casing_extension.loads.append(casing_extension_cg)
head_group.elements.append(casing_extension)

## Casing Bonnet
casing_bonnet = Element(name="casing bonnet", length=23, width=18.5, height=12)
casing_bonnet_cg_pos = Vector(6.4998+X1, 9.4631, 0)
casing_bonnet_cg = Load(casing_bonnet_cg_pos, 172.54, _type="mass")
casing_bonnet.loads.append(casing_bonnet_cg)
head_group.elements.append(casing_bonnet)

## Head
head = Element(name="head", length=14.84, width=18.5, height=15.625)
head_cg_pos = Vector(-25.9307, 8.9466, 2.0638)
head_cg = Load(head_cg_pos, 524, _type="mass")
head.loads.append(head_cg)
head_group.elements.append(head)

### Torque
head_torque = Load(Vector(-25.9307, 8.9466, 2.0638), Vector(rotation_max_torque, 0, 0), _type="force")
head.loads.append(head_torque)

### Feed force
feed_force = Load(Vector(-13.254, 9.125, 0), Vector(holdback, 0, 0), _type="moment")
head.loads.append(feed_force)

mast_group = Element(name='mast_group Group')
max100.elements.append(mast_group)

## mast
mast = Element(name="mast", length=245, width=10, height=12)
mast_cg_pos = Vector(-121.1904, 6.6961, 0.0381)
mast_cg = Load(mast_cg_pos, 1816, _type="mass")
mast.loads.append(mast_cg)
mast_group.elements.append(mast)

## Break-out
break_out = Element(name="Break-Out", length=17, width=18, height=31)
break_out_cg_pos = Vector(-1.4334, 14.7466, 5.4025)
break_out_cg = Load(break_out_cg_pos, 593, _type="mass")
break_out.loads.append(break_out_cg)
mast_group.elements.append(break_out)


pivot_group = Element(name='pivot_group Group')
max100.elements.append(pivot_group)

## pivot
pivot = Element(name="pivot", length=83, width=17.5, height=17.5)
pivot_cg_pos = Vector(-20.6742, 8.7457, 0.0162)
pivot_cg = Load(pivot_cg_pos, 570, _type="mass")
pivot.loads.append(pivot_cg)
pivot_group.elements.append(pivot)


## Base (only for mast lift cyl placement)
base = Element(name="base", length=126, width=60, height=48)
base_cg_pos = Vector(-36.54, -1.628, -5.03)
base_cg = Load(pivot_base_cg_pos, 0, _type="mass")
base.loads.append(base_cg)
max100.elements.append(base)

# Vector between coordinates

R23 = Vector(-18-feed_position, 14, 0)
R12 = Vector(16.5+mast_slide_position, 12.5, 0)

## Diplacement relative to each other
head_group.move(R23).move(R12).rotate(Rotation(gamma=mast_angle))
mast_group.move(R12).rotate(Rotation(gamma=mast_angle))
pivot_group.rotate(Rotation(gamma=mast_angle))

print('##############################')
print()
print('reactions:', max100.reactions())
print()

items = max100.draw()

color_key = list(display.App().colors.keys())

# randomise color for each components.
for i, item in enumerate(items):
    item['color'] = color_key[i]

theApp = display.App()
theApp.items = items
theApp.on_execute()
