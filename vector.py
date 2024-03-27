import numpy as np
import numbers
from math import sin, cos, radians
from copy import deepcopy

class Vector():
    """A simple vector class to wrap the numpy vector functions"""
    def __init__(self, x, y, z=0):
        
        self.x = x
        self.y = y
        self.z = z


    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other): 
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

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

    def __eq__(self, other):
        if other == None:
            return False
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False


    def rotate(self, rotation):
        # angle in degree
        alpha = rotation.x
        beta = rotation.y
        gamma = rotation.z

        if alpha == 0 and beta == 0 and gamma == 0:
            print('no changes, need an angle to rotate!')
            return self
        else:
            # print('rotating', rotation)
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

    
class Rotation(Vector):
    """A rotation class, same as vector but with values in degree"""
    def __init__(self, alpha=0, beta=0, gamma=0):
        super().__init__(x=alpha, y=beta, z=gamma)

    def rotate(self, alpha=0, beta=0, gamma=0):
        print('this is a rotation vector, cant be rotated, simply add angles to it')
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

    def rotate(self, rotation=Rotation(0)):
        self.position.rotate(rotation)
        if self._type in ['force']: #moments and gravity does not rotate with displacement. 
            self.charge.rotate(rotation)
        return self

    def move(self, x, y, z=0):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        return self

    def reactions(self, gravity=None, parent_move=None, parent_rotation=None): # Calculate reaction forces and moment at origin of load.
        # if the load is part of an element, the load must be moved to proper position in element upon inserting it. 

        # Need to apply rotation and then moves for the load to properly calculate it.
        final_charge = self.charge
        final_position = self.position
        # print(final_position)


        if parent_rotation not in [None, Rotation(0,0)]:
            # print('final_position before', final_position)
            final_position.rotate(parent_rotation)
            # print('final_position after', final_position)
            if self._type == 'force':
                final_charge.rotate(parent_rotation)
                # print(final_charge)

        if parent_move not in [None, Vector(0,0)]:
            final_position += parent_move
        
        

        if self._type == 'force':

            moments = cross_prod(final_position, final_charge)
            forces = final_charge

        elif self._type == 'moment':
            moments = final_charge
            forces = Vector(0,0)

        elif self._type == 'mass':
            moments = cross_prod(final_position, final_charge * gravity)
            forces = final_charge * gravity

        return forces, moments

class Gravity(Vector):
    """A gravity class"""
    def __init__(self, x=0, y=-1, z=0): # Unit vector into the direction of the gravity
        super().__init__(x=x, y=y, z=z)
        
    #TODO: normalize, take the random vector values and set them to unit vector.
        

class Element():
    def __init__(self, length=0, width=0, height=0, loads=None, name=None):
        """Basic element class for calculation various thing on an element assembly"""
        self.length = length
        self.width = width
        self.height = height
        self.name = name

        if loads == None:
            self.loads = list()
        else:
            self.loads = loads
        self.moves = list()
        self.rotations = list()

    def rotate(self, rotation):
        # Rotate the element from it's origin
        # rotation = Rotation(alpha, beta, gamma)
        self.rotations.append(rotation)
        return self

    def move(self, move):
        # move = Vector(x=x, y=y, z=z)
        self.moves.append(move)
        return self

    def reactions(self, gravity=None, parent_move=None, parent_rotation=None):
        forces = Vector(0,0,0)
        moments = Vector(0,0,0)

        # print('element rotation and moves:', self.rotations, self.moves)
        
        if len(self.moves) > 1:
            # print('self.moves', self.moves)
            move = sum(self.moves) # sum all moves of the element
        elif len(self.moves) == 1:
            move = self.moves[0]
        else:
            move = Vector(0,0)

        if len(self.rotations) > 1:
            rotation = sum(self.rotations) #sum all rotation of the element
            # print('self.rotations', self.rotations)
        elif len(self.rotations) == 1:
            rotation = self.rotations[0]

        else:
            rotation = Rotation(0, 0)

        if parent_move != None:
            move += parent_move
        if parent_rotation != None:
            rotation += parent_rotation

        # print()
        # print('parent move and rotation:', move, rotation)
        for load in self.loads:
            # print('load_before:', load.position, load.charge)
            force, moment = load.reactions(gravity=gravity, parent_move=move, parent_rotation=rotation)
            forces += force
            moments += moment
            # print('load_after:', force, moment)
            # print()

        return [forces, moments]





class Machine():
    """A machine class that can contain multiple elements (that moves relatives to each other), a gravity member
    elements: element class that apply to the machine
    gravity: a gravity load instance default to y=-1
    **parameters: a keyword arguments of variables parameters for the machine ex: mast angle
    add items to elements starting from the fartherst to the ground, in a chain. This way partial section will work.
    TODO: what about partial section I.E. A crane, or 2 mast.
    """

    def __init__(self, elements=None, gravity=None):
        if elements == None:
            self.elements = list()
        else:
            self.elements = elements
        if gravity == None:
            self.gravity = Gravity()
        else:
            self.gravity = gravity

    def get_results(self, vector):
        # get a resulting force at a desired place of the model. 
        # will calculate the element resulting forces and moment starting from the last one
        pass

    def reactions(self):
        forces = Vector(0, 0, 0)
        moments = Vector(0, 0, 0)
        for number, element in enumerate(self.elements):
            force = Vector(0,0)
            moment = Vector(0,0)
            force, moment = element.reactions(gravity=self.gravity)

            
            print(number, element.name, force, moment)
            forces += force
            moments += moment
        # print()
        # print('-------------------------------')
        # print('[(force vector), (moment vector)]')
        return [forces, moments]




        # 3 - Pivot
# bl03 = Vector(-1, 7)
# bl3 = Vector(7, 7)
# bl3.rotate(gamma=mast_angle)
# # print(bl3)
# mg3 = Vector(0, -12) # no rotation gravity is absolute
# result += cross_prod((bl03+bl3), mg3)
# print('with pivot:', result)
    

        
    
        
