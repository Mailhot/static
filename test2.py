from vector import Vector, cross_prod, Element, Load, Machine, Rotation, Gravity

machine1 = Machine(gravity=Gravity())

load1 = Load(Vector(10, 10), 10, _type='mass')
load2 = Load(Vector(10,  0), 20, _type='mass')
element2 = Element(loads=[load2], name='ele load2').move(Vector(20, 20))
# print('element2 reactions', element2.reactions(Gravity()))
element1 = Element(loads=[load1], name='ele load1')
element3 = Element(elements=[element1, element2], name='combined arms')

machine1.elements = [element3]
reactions = machine1.reactions()

print('reactions', reactions)
expected_reactions = {'forces': Vector(0, -30, 0), "moments": Vector(0, 0, -700)}

for key in expected_reactions.keys():
	assert expected_reactions[key] == reactions[key], f'test1 failed for {key}, expected:{expected_reactions[key]}, got {reactions[key]}'
print('test1, all passed!')

print()
print('test2')
element3.rotate(Rotation(0, 0, 90))
# print(element3.rotations)
reactions = machine1.reactions()
# print(reactions)
expected_reactions = {'forces': Vector(0, -30, 0), "moments": Vector(0.0, 0.0, 500.0)}
for key in expected_reactions.keys():
	assert expected_reactions[key] == reactions[key], f'test2 failed for {key}, expected:{expected_reactions[key]}, got {reactions[key]}'
print('test2, all passed!')


print()
print('3rd test')
element3.rotate(Rotation(0, 0, 90))
reactions = machine1.reactions()
# print(reactions)
expected_reactions = {'forces': Vector(0, -30, 0), "moments": Vector(0.0, 0.0, 700.0)}
for key in expected_reactions.keys():
	assert expected_reactions[key] == reactions[key], f'test3 failed for {key}, expected:{expected_reactions[key]}, got {reactions[key]}'
print('test3, all passed!')


print()
print('4th test')
element3.rotate(Rotation(0, 0, 90))
reactions = machine1.reactions()
# print(reactions)
expected_reactions = {'forces': Vector(0, -30, 0), "moments": Vector(0.0, 0.0, -500.0)}
for key in expected_reactions.keys():
	assert expected_reactions[key] == reactions[key], f'test3 failed for {key}, expected:{expected_reactions[key]}, got {reactions[key]}'
print('test4, all passed!')

print()
print('5th test')
element3.rotations = [] #reset element3 rotations
load2.rotate(Rotation(0,0,-90))
reactions = machine1.reactions()
print(reactions)
# expected_reactions = {'forces': Vector(0, -30, 0), "moments": Vector(0.0, 0.0, -500.0)}
# for key in expected_reactions.keys():
# 	assert expected_reactions[key] == reactions[key], f'test3 failed for {key}, expected:{expected_reactions[key]}, got {reactions[key]}'
# print('test4, all passed!')