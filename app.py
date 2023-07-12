import math

class Point():
    """Point instance """
    def __init__(self, x, y, z=0, name=None):
        self.x = x
        self.y = y
        self.z = z
        self.name = name

    def __repr__(self):
        return f'P({self.x},{self.y})'        



        

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
            self.Fy = self.module * math.cos(math.radians(self.angle))

        elif Fx != None and Fy != None:
            self.module = math.sqrt(self.Fx ** 2 + self.Fy ** 2)
            self.angle = math.degrees(math.atan2(self.Fy, self.Fx))


class Force():
    """Force class, holds a load and a point"""
    def __init__(self, load, point=(0, 0)):
        
        self.load = load
        self.point = point

    def __repr__(self):
        return f'f={self.load.module}, theta={self.load.angle}, Fx={self.load.Fx}, Fy={self.load.Fy}, M={self.load.moment}, x={self.point.x}, y={self.point.y}'
        
    def move(self, angle=0, point=Point(0,0)):

        if point.x != 0 and point.y !=0:
            # translate a series of point from forces
            output = []
            self.point.x += point.x
            self.point.y += point.y

            # Moments
            self.load.moment += point.x * self.load.Fy 
            self.load.moment += point.y * self.load.Fx

        # Rotation
        if angle != 0:
            # Find the initial point angle
            theta0 = math.atan2(self.point.y, self.point.x)
            # print(theta0)
            length_init = math.sqrt(point.x ** 2 + point.y ** 2)
            self.point.x = length_init * math.cos(theta0 + math.radians(angle))
            self.point.y = length_init * math.sin(theta0 + math.radians(angle))
            self.load.angle += angle
        return self

        

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


