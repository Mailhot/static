import math

class Point():
    """Point instance """
    def __init__(self, x, y, z=0, name=None):
        self.x = x
        self.y = y
        self.z = z
        self.name = name

    def __repr__(self):
        if self.name == None:
            return f'P({self.x},{self.y})'
        
        elif self.name != None:
            return f'{self.name}({self.x},{self.y})'

    def move(self, angle=0, point=None):

        # Rotation
        if angle != 0:
            # Find the initial point angle
            theta0 = math.atan2(self.y, self.x)
            # print(theta0)
            length_init = math.sqrt(self.x ** 2 + self.y ** 2)
            self.x = length_init * math.cos(theta0 + math.radians(angle))
            self.y = length_init * math.sin(theta0 + math.radians(angle))

        # Translation
        # TODO: Ambigus does the translation happen before or after?
        if point != None:
            # translate a point 
            self.x += point.x
            self.y += point.y

        return self

        

class Element():
    """Basic structural element, pivots and mass"""
    def __init__(self, mass, pivots=[], angle=0):
        self.mass = mass
        self.pivots = pivots
        self.angle = angle
        self.connections = []

    def pivot(self, no):
        return self.pivots[no]

class Pivot():
    """ class to contain an element and a point index for this element """
    def __init__(self, element, point_index):
        self.element = element
        self.point_index = point_index

class Connection():
    """Connection class to connect elements through pivots"""
    def __init__(self, elements=[], motion=None):
        self.elements = elements
        self.motion = motion
        print(elements)
        
        # add connections to their respectives elements
        self.elements[0].element.connections.append(self.elements[1])
        self.elements[1].element.connections.append(self.elements[0])

class Cylinder():
    """Cylinder connection, same as a connection but with a distance attached"""
    def __init__(self, closed_length=None, open_length=None, stroke=None):
        super(Cylinder, self).__init__()
        if closed_length is None and open_length is not None and stroke is not None:
            closed_length = open_length - stroke
        elif closed_length is not None and open_length is None and stroke is not None:
            open_length = closed_length + stroke
        elif closed_length is not None and open_length is not None and stroke is None:
            stroke = open_length - closed_length

        else: 
            return 'error, you need at least 2 value to make a cylinder'


        self.closed_length = closed_length
        self.open_length = open_length
        self.stroke = stroke
        self.current_length = closed_length
        self.pivots = [Point(0,0, name='A0'), Point(self.current_length, 0, name='A1')]

class World():
    """Space class with gravity, contains elements, and other things"""
    def __init__(self, gravity, elements=[], connections=[]):
        self.gravity = gravity
        self.elements = elements
        self.connections = connections

    def calculate(self):
        # Order the components properly
        for element in self.elements:
            element.pivots
            


##############################
# force.py
##############################

class Load():
    """Load elelement, contains module, angle, Fx and Fy"""
    def __init__(self, module=None, angle=None, Fx=None, Fy=None, moment=0):

        self.module = module
        self.angle = angle
        self.Fx = Fx
        self.Fy = Fy
        self.moment = moment

        if self.module != None and self.angle != None:
            self.Fx = self.module * math.cos(math.radians(angle))
            self.Fy = self.module * math.cos(math.radians(angle))

        elif self.Fx != None and self.Fy != None:
            self.module = math.sqrt(Fx ** 2 + Fy ** 2)
            self.angle = math.degrees(math.atan2(Fy, Fx))

    def update(self, module=None, angle=None, Fx=None, Fy=None):
        if self.module != None and self.angle != None:
            self.Fx = self.module * math.cos(math.radians(self.angle))
            self.Fy = self.module * math.sin(math.radians(self.angle))

        elif Fx != None and Fy != None:
            self.module = math.sqrt(self.Fx ** 2 + self.Fy ** 2)
            self.angle = math.degrees(math.atan2(self.Fy, self.Fx))


class Gravity(Load):
    """Gravity load instance"""
    def __init__(self, module=None, angle=-90, Fx=None, Fy=None, moment=0):
        super().__init__(module, angle, Fx, Fy, moment)
        self.angle = -90
        self.update()
    
    def update(self, module=None, angle=None, Fx=None, Fy=None):
        if self.module != None and self.angle != None:
            self.Fx = self.module * math.cos(math.radians(self.angle))
            self.Fy = self.module * math.sin(math.radians(self.angle))

        elif Fx != None and Fy != None:
            self.module = math.sqrt(self.Fx ** 2 + self.Fy ** 2)
            self.angle = math.degrees(math.atan2(self.Fy, self.Fx))


class Force():
    """Force class, holds a load and a point"""
    def __init__(self, load, point=Point(0, 0)):
        
        self.load = load
        self.point = point

    def __repr__(self):
        point_str = str(self.point)
        return f'{point_str} f={self.load.module}, theta={self.load.angle}, moment={self.load.moment}, Fx={self.load.Fx}, Fy={self.load.Fy}'
        
    def move(self, angle=0, point=Point(0,0)):
        self.point.move(angle, point)

        # Moments
        # self.load.moment += (point.x) * self.load.Fy
        # self.load.moment += (point.y) * self.load.Fx
        
        if isinstance(self.load, Gravity):
            pass

        else:
            self.load.angle += angle
        self.load.update()
            
        return self

    def find_reaction_between_points(self, point1, point2):
        # If a pivot is at origin and given the load at this origin, 
        # this will find the angle of resulting force and calculate the force at this point1 (with angle) based on point2
        cyl_x = point1.x - point2.x
        cyl_y = point1.y - point2.y

        angle_rad = math.atan2(cyl_y, cyl_x)

        # We now have a point and angle to find the resulting force
        # Take a sum of force and moment value and convert it to a reaction at a point

        R1x = -self.load.moment / (cyl_y + math.atan(angle_rad))
        R1y = R1x * math.atan(angle_rad)

        reaction_angle = math.degrees(angle_rad)
        reaction_force = math.sqrt(R1y ** 2 + R1x ** 2)
        return Force(Load(reaction_force, reaction_angle), point1)



class Solid():
    """Solid class that contain forces and points"""
    def __init__(self, forces, points):
        
        self.forces = forces
        self.points = points

    def __repr__(self,):
        
        returned_string = '\nForces:\n'

        for element in self.forces:
            returned_string += str(element) + '\n'

        returned_string += 'Points:\n'
        
        for element in self.points:
            returned_string += str(element) + '\n'

        return returned_string


    def move(self, angle=0, point=Point(0,0)):
        
        for element in self.forces:
            element.move(angle, point)

        for element in self.points:
            element.move(angle, point)

        return self

    def find_net_force_at_origin(self):
        # calculated at (0,0)
        horizontal_total = 0
        vertical_total = 0
        moment_total = 0

        for i in self.forces:
            # add moment
            if i.load.moment != 0:
                moment_total += i.load.moment

            horizontal = i.load.module * math.cos(math.radians(i.load.angle))
            vertical = i.load.module * math.sin(math.radians(i.load.angle))
            moment = horizontal * i.point.y + vertical * i.point.x
            print(moment)
            horizontal_total += horizontal
            vertical_total += vertical
            moment_total += moment


        total_magnitude = math.sqrt(horizontal_total ** 2 + vertical_total ** 2)
        total_angle = math.atan2(vertical_total, horizontal_total)
        total_angle = math.degrees(total_angle)
        total_magnitude = round(total_magnitude, 1)
        total_angle = round(total_angle, 1)
        
        return Force(Load(Fx=horizontal_total, Fy=vertical_total, moment=moment_total), Point(0,0))

    
if __name__ == '__main__':

    base0 = Element(mass=20000)
    pivot01 = Point(0, 0, ' ', name='P0')
    pivot02 = Point(10, -10, name='P1')
    base0.pivots = [pivot01, pivot02]
    print(base0.pivots)


    boom1 = Element(mass=5000,)
    pivot11 = Point(0, 0, name='P0')
    pivot12 = Point(10, 3, name='P1')
    pivot13 = Point(5, 1, name='A0')
    pivot14 = Point(5, 3, name='A1')
    boom1.pivots = [pivot11, pivot12, pivot13, pivot14]

    connection0 = Connection(elements=[Pivot(base0, 0), Pivot(boom1, 0)])

    cylinder0 = Cylinder(closed_length=13, open_length=14)

    connection1 = Connection(elements=[Pivot(base0, 1), Pivot(boom1, 3)], motion=cylinder0)

    world0 = World(gravity='-y', elements=[base0, boom1, cylinder0,], connections=[connections0, connection1])

    world0.calculate()


