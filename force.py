from math import sin, cos, tan, sqrt, radians, atan2, degrees
from app import Load, Force, Point, Solid, Gravity

def find_net_force(forces):
    # Sum forces at point in 2d (x and y) from a list of set(force, angle[deg])

    horizontal_total = 0
    vertical_total = 0
    for i in forces:
        horizontal = i[0] * cos(radians(i[1]))
        vertical = i[0] * sin(radians(i[1]))
        horizontal_total += horizontal
        vertical_total += vertical

    total_magnitude = sqrt(horizontal_total ** 2 + vertical_total ** 2)
    total_angle = atan2(vertical_total, horizontal_total)
    total_angle = degrees(total_angle)
    total_magnitude = round(total_magnitude, 1)
    total_angle = round(total_angle, 1)
    force = (total_magnitude, total_angle)
    return force

# forces = [(10, 90), (10, -45)]#, (100, 45), (20, 180)]

#print(find_net_force(forces))



# Force and point: [(force, angle), (x, y)]
forces2 = [[(10, 90), (5, -2)], [(10, -45), (10, 0)]]

def find_net_force_moment(forces):

    horizontal_total = 0
    vertical_total = 0
    moment_total = 0

    


    for i in forces:
        # add moment
        if i.load.moment != 0:
            moment_total += i.load.moment

        horizontal = i.load.module * cos(radians(i.load.angle))
        vertical = i.load.module * sin(radians(i.load.angle))
        moment = horizontal * i.point.y + vertical * i.point.x
        print(moment)
        horizontal_total += horizontal
        vertical_total += vertical
        moment_total += i.load.moment


    total_magnitude = sqrt(horizontal_total ** 2 + vertical_total ** 2)
    total_angle = atan2(vertical_total, horizontal_total)
    total_angle = degrees(total_angle)
    total_magnitude = round(total_magnitude, 1)
    total_angle = round(total_angle, 1)
    force = (total_magnitude, total_angle)
    return Force(Load(Fx=horizontal_total, Fy=vertical_total, moment=moment_total), Point(0,0))


points1 = [(0,0), (12,6), (12,12)]

def rotation(points, angle):
    # Rotate an element by an angle, angle is to move the component in referenctial. (positive is counterclockwise)
    output = []
    for point in points:
        # Find the initial point angle
        theta0 = atan2(point.y, point.x)
        # print(theta0)
        length_init = sqrt(point.x ** 2 + point.y ** 2)
        x_prim = length_init * cos(theta0 + radians(angle))
        y_prim = length_init * sin(theta0 + radians(angle))
        output.append(Point(x_prim, y_prim))

    return output

def translation(forces, point):
    # translate a series of point from forces
    output = []
    for force in forces:
        force.point.x += point.x
        force.point.y += point.y
        # Moments
        force.load.moment += point.x * force.load.Fy 
        force.load.moment += point.y * force.load.Fx
        output.append(force)

    return output


#print(find_net_force_moment(forces2))

#point forces: (Fx, Fy, Mz)
point_forces = (7.071067811865476, 2.9289321881345254, -70.71067811865474)
reactions = [(None, 90), (3, -2)]


def find_reactions(point_forces, reactions):
    # Take a sum of force and moment value and convert it to a reaction at a point
    horizontal_total = point_forces[0]
    vertical_total = point_forces[1]
    moment_total = point_forces[2]


    Rx = -moment_total / (vertical_total + tan(radians(reactions[0][1]))*reactions[1][0])
    Ry = Rx * tan(radians(reactions[0][1]))

    horizontal_total += Rx 
    vertical_total += Ry 

    reaction_angle = degrees(atan2(Ry, Rx))
    reaction_force = sqrt(Ry ** 2 + Rx ** 2)


    return (horizontal_total, vertical_total, reaction_force, reaction_angle)

reactions = find_reactions(point_forces, reactions)
# print(f'fx={reactions[0]}, fy={reactions[1]}, R={reactions[2]}, Theta={reactions[3]}')



print('problem solving...')

print('sliding table')

forces2 = [Force(Load(2500, -90), Point(30, 12)),]
print(find_net_force_moment(forces2))

force_table = (0, -2500.0, -75000.0)

print('mast')

forces3 = [Force(Load(6600, -90), Point(120, 8)), 
            Force(Load(2500, -90, moment=-75000), Point(140, 12)),
            ]
moments3 = [-75000]
print(find_net_force_moment(forces3))

force_mast = (0, -9100.0, -1217000.0)

print('pivot')

print('rotating module')

points = [Point(0,0, name='P0'), Point(12,12, name='P1')]
gravity1 = Force(Gravity(2000, -90), Point(12, 6))
print(gravity1)
solid_pivot = Solid(forces=[gravity1], points=points).move(angle=90)
print(solid_pivot)

print('adding other module forces directly')
solid_pivot.forces.append(Force(Gravity(6600, -90), Point(120, 8)).move(0, Point(-100,18)))
solid_pivot.forces.append(Force(Gravity(2500, -90), Point(30, 12)).move(0, Point(-100,18)).move(0, Point(+100,12)))
solid_pivot.forces.append(Force(Load(40000, 0), Point(36, 18)).move(0, Point(-100,18)).move(0, Point(+100,12)))
print('after adding all to pivot')
print(solid_pivot)
points4 = rotation(points, 90)
print(points4)

forces4 = [Force(Load(6600, -90, moment=-1142000), Point(120, 8)).move(angle=15, point=Point(-120, 0)), 
            Force(Load(2500, -90, moment=-75000), Point(140, 12)).move(angle=15, point=Point(-120, 0)),
            ]

# translate forces4 into Pivot module
# forces4 = translation(forces4, Point(-120,0)) #TODO: this implies changing the moments...
# print(forces4)

forces5 = [Force(Load(6600, -90, moment=-1142000), Point(120, 8)).move(angle=15, point=Point(-120, 0)), 
            Force(Load(2500, -90, moment=-75000), Point(140, 12)).move(angle=15, point=Point(-120, 0)), 
            Force(Load(2000, -90), Point(-6.0, 12.0)), 
            ]

print(find_net_force_moment(forces5))

forces6 = (6.79678973526781e-13, -11100.0, -2347000.0)
