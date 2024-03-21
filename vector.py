import numpy as np
import numbers
from math import sin, cos, radians

class Vector():
    """A simple vector class to wrap the numpy vector functions"""
    def __init__(self, x, y, z=0):
        
        self.x = x
        self.y = y
        self.z = z


    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other): 
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        if not isinstance(other, numbers.Real):
            raise NotImplemented
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if not isinstance(other, numbers.Real):
            raise NotImplemented
        return Vector(self.x * other, self.y * other, self.z * other)


    def rotate(self, alpha=0, beta=0, gamma=0):
        # angle in degree

        if alpha == 0 and beta == 0 and gamma == 0:
            print('no changes, need an angle to rotate!')
            return self
        else:
            alpha = radians(alpha)
            beta = radians(beta)
            gamma = radians(gamma)
            rotation_matrix = np.array([[cos(beta)*cos(gamma), sin(alpha)*sin(beta)*cos(gamma)-cos(alpha)*sin(gamma), cos(alpha)*sin(beta)*cos(gamma)+sin(alpha)*sin(gamma)], 
                                        [cos(beta)*sin(gamma), sin(alpha)*sin(beta)*sin(gamma)+cos(alpha)*cos(gamma), cos(alpha)*sin(beta)*sin(gamma)-sin(alpha)*cos(gamma)], 
                                        [-sin(beta), sin(alpha)*cos(beta), cos(alpha)*cos(beta)]
                                        ])
            vector = np.array([self.x, self.y, self.z])
            result = rotation_matrix.dot(vector)
            # print(result)
            self.x = result[0]
            self.y = result[1]
            self.z = result[2]
            return self

    


def cross_prod(vector1, vector2):
    vector1 = [vector1.x, vector1.y, vector1.z]
    vector2 = [vector2.x, vector2.y, vector2.z]

    result = np.cross(vector1, vector2)
    # print(result)
    return Vector(result[0], result[1], result[2])

    

class Load():
    """A position vector and charge vector combined to define a load."""
    def __init__(self, position, charge, _type='force'):
        self.position = position
        self.charge = charge
        self._type = _type
        #TODO: check if _type is in [force, moment, mass] return error if not

    def rotate(self, alpha=0, beta=0, gamma=0):
        self.position.rotate(alpha=alpha, beta=beta, gamma=gamma)
        if self._type in ['force']: #moments and gravity does not rotate with displacement. 
            self.charge.rotate(alpha=alpha, beta=beta, gamma=gamma)
        return self

    def move(self, x, y, z=0):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        return self

    def reactions(self, gravity=None): # Calculate reaction forces and moment at origin of load.
        # if the load is part of an element, the load must be moved to proper position in element upon inserting it. 
        if self._type == 'force':
            moments = cross_prod(self.position, self.charge)
            forces = self.charge
        elif self._type == 'moment':
            moments = self.charge
            forces = Vector(0,0)

        elif self._type == 'mass':
            moments = cross_prod(self.position, self.charge * gravity)
            forces = self.charge * gravity

        return [forces, moments]

class Gravity(Vector):
    """A gravity class"""
    def __init__(self, x=0, y=-1, z=0): # Unit vector into the direction of the gravity
        super().__init__(x=x, y=y, z=z)
        
    #TODO: normalize, take the random vector values and set them to unit vector.
        

class Element():
    """Basic element class for calculation various thing on an element assembly"""
    def __init__(self, length=0, width=0, height=0, loads=[]):

        self.length = length
        self.width = width
        self.height = height
        self.loads = loads

    def rotate(self, alpha=0, beta=0, gamma=0):
        # Rotate the element from it's origin
        for load in self.loads:
            load.rotate(alpha=alpha, beta=beta, gamma=gamma)
        return self

    def move(self, x, y, z=0):
        for load in self.loads:
            load.move(x=x, y=y, z=z)
        return self

    def reactions(self, gravity=None):
        forces = Vector(0,0,0)
        moments = Vector(0,0,0)
        for load in self.loads:
            force, moment = load.reactions(gravity=gravity)
            forces += force
            moments += moment

        return [forces, moments]





class Machine():
    """A machine class that can contain multiple elements (that moves relatives to each other), a gravity member
    elements: element class that apply to the machine
    gravity: a gravity load instance default to y=-1
    **parameters: a keyword arguments of variables parameters for the machine ex: mast angle
    add items to elements starting from the fartherst to the ground, in a chain. This way partial section will work.
    TODO: what about partial section I.E. A crane, or 2 mast.
    """

    def __init__(self, elements=[], gravity=Gravity(), **parameters):
        self.elements = elements
        self.gravity = gravity

    def get_results(self, vector):
        # get a resulting force at a desired place of the model. 
        # will calculate the element resulting forces and moment starting from the last one
        pass

    def reactions(self):
        forces = Vector(0, 0, 0)
        moments = Vector(0, 0, 0)
        for element in self.elements:
            force, moment = element.reactions(gravity=self.gravity)
            forces += force
            moments += moment
        print('[(force vector), (moment vector)]')
        return [forces, moments]




        # 3 - Pivot
# bl03 = Vector(-1, 7)
# bl3 = Vector(7, 7)
# bl3.rotate(gamma=mast_angle)
# # print(bl3)
# mg3 = Vector(0, -12) # no rotation gravity is absolute
# result += cross_prod((bl03+bl3), mg3)
# print('with pivot:', result)
    

        
    
        
