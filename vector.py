import numpy as np
import numbers
from math import sin, cos, radians
from copy import deepcopy
import turtle



class Vector():
    """A simple vector class to wrap the numpy vector functions"""
    def __init__(self, x, y, z=0):
        
        self.x = x
        self.y = y
        self.z = z


    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    def __radd__(self, other):
        if other in [0, Vector(0,0)]:
            return Vector(self.x, self.y, self.z)
        else:
            return other.__add__(self)


    def __sub__(self, other): 
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

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

    def move(self, move):
        # Move vector like add
        self.x += move.x
        self.y += move.y
        self.z += move.z
        return Vector(self.x+move.x, self.y+move.y, self.z+move.z)

    def rotate(self, rotation):
        # angle in degree
        alpha = rotation.x
        beta = rotation.y
        gamma = rotation.z

        if alpha == 0 and beta == 0 and gamma == 0:
            # print('no changes, need an angle to rotate!')
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
            # self.x = result[0]
            # self.y = result[1]
            # self.z = result[2]
            return Vector(round(result[0], 2), round(result[1], 2), round(result[2], 2))
            # return self

    
class Rotation(Vector):
    """A rotation class, same as vector but with values in degree"""
    def __init__(self, alpha=0, beta=0, gamma=0):
        super().__init__(x=alpha, y=beta, z=gamma)

    # def __add__(self, other):
    #     self.alpha += other.alpha
    #     self.beta += other.beta
    #     self.gamma += other.gamma
    #     return self

    # def __radd__(self, other):
    #     if other in [0, Rotation(0,0,0)]:
    #         return self
    #     else:
    #         return other.__add__(self)

    def rotate(self, alpha=0, beta=0, gamma=0):
        print('this is a rotation vector, cant be rotated, simply add angles to it')
        return self
        

def cross_prod(vector1, vector2):
    vector1 = [vector1.x, vector1.y, vector1.z]
    vector2 = [vector2.x, vector2.y, vector2.z]

    result = np.cross(vector1, vector2)
    return Vector(result[0], result[1], result[2])

    

class Load():
    """A position vector and charge vector combined to define a load."""
    def __init__(self, position, charge, _type='force'):
        self.position = position
        self.charge = charge
        self._type = _type

    def __repr__(self):
        return f'{self.position, self.charge, self._type}'

    def rotate(self, rotation=Rotation(0)):
        self.position.rotate(rotation)
        if self._type in ['force']: #moments and gravity does not rotate with displacement. 
            self.charge.rotate(rotation)
        return Load(self.position, self.charge, self._type)

    def move(self, x, y, z=0):
        # self.position.x += x
        # self.position.y += y
        # self.position.z += z
        return Load(self.position+x, self.charge+y, self._type+z)

    def reactions(self, gravity=None, parent_move=None, parent_rotation=None, offset=None): 
        # Calculate reaction forces and moment at origin of load.
        # if the load is part of an element, the load must be moved to proper position in element upon inserting it. 
        # print(self)
        # Need to apply rotation and then moves for the load to properly calculate it.
        final_charge = deepcopy(self.charge)
        final_position = deepcopy(self.position)

        # print('fp, pm', final_position, parent_move)
        # print('offset', offset)


        if parent_rotation not in [None, Rotation(0,0)]:
            # print('final_position before', final_position)
            final_position = final_position.rotate(parent_rotation)
            # print('final_position after', final_position)
            if self._type == 'force':
                final_charge = final_charge.rotate(parent_rotation)
                # print(final_charge)

        if parent_move not in [None, Vector(0,0)]:
            final_position += parent_move.rotate(parent_rotation)
        
        # print('calculating force result:', final_position,  final_charge)

        if offset not in [None, Vector(0,0)]:
            final_position += deepcopy(offset)

        if self._type == 'force':
            
            moments = cross_prod(final_position, final_charge)
            forces = final_charge

        elif self._type == 'moment':
            moments = final_charge
            forces = Vector(0,0)

        elif self._type == 'mass':
            moments = cross_prod(final_position, final_charge * gravity)
            forces = final_charge * gravity

        return forces, moments, final_position

class Gravity(Vector):
    """A gravity class"""
    def __init__(self, x=0, y=-1, z=0): # Unit vector into the direction of the gravity
        super().__init__(x=x, y=y, z=z)
        
    #TODO: normalize, take the random vector values and set them to unit vector.
        

class Element():
    def __init__(self, length=0, width=0, height=0, loads=None, name=None, elements=None, offset=None):
        """
        Basic element class for calculation various thing on an element assembly
        offset: a vector to offset the origin of a group without affecting the rotations
        """
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
        if elements == None:
            self.elements = list()
        else:
            self.elements = elements

        self.offset = Vector(0, 0)

    def rotate(self, rotation):
        # Rotate the element from it's origin
        # rotation = Rotation(alpha, beta, gamma)
        self.rotations.append(rotation)
        return self

    def move(self, move):
        # move = Vector(x=x, y=y, z=z)
        self.moves.append(move)
        return self

    def reactions(self, gravity=None, parent_move=None, parent_rotation=None, offset=None):
        forces = Vector(0,0,0)
        moments = Vector(0,0,0)
        positions = Vector(0,0,0)
        move = Vector(0,0)
        rotation = Rotation(0,0)
        # print('-', self.name)
        # print(parent_move, parent_rotation)

        # print('element rotation and moves:', self.name, self.rotations, self.moves)

        if offset not in [None, Vector(0, 0)]:
            offset_ = deepcopy(self.offset + offset)

        else:
            offset_ = deepcopy(self.offset)
        
        if len(self.moves) > 1:
            # print('self.moves', self.moves)
            move = sum(self.moves) # sum all moves of the element

        elif len(self.moves) == 1:
            move = deepcopy(self.moves[0])

        else:
            move = Vector(0,0)

        if len(self.rotations) > 1:
            rotation = sum(self.rotations) # sum all rotation of the element
            # print('self.rotations', self.rotations)
        elif len(self.rotations) == 1:
            rotation = deepcopy(self.rotations[0])

        else:
            rotation = Rotation(0, 0)

        if parent_move != None:
            move += parent_move
        if parent_rotation != None:
            rotation += parent_rotation

        # print()
        # print('parent move and rotation:', move, rotation)
        if self.loads:
            for load in self.loads:
                
                # shape2.color = ("blue")
                force = Vector(0,0,0)
                moment = Vector(0,0,0)
                # print('load_before:', load.position, load.charge)
                # print(move, rotation)
                force, moment, position = load.reactions(gravity=gravity, parent_move=move, parent_rotation=rotation,offset=offset_)
                # if load._type == "mass":
                #     turtle_2d_draw(shape2, self, position=position, rotation=rotation)
                forces += force
                moments += moment
                # print('load_after:', forces, moments)
                # print()

        if self.elements: # TODO: ?An element has either child elements or loads not both.
            for number, element in enumerate(self.elements):
                
                force = Vector(0,0,0)
                moment = Vector(0,0,0)
                # print(element.moves)

                

                force, moment, position = element.reactions(gravity=gravity, parent_move=move, parent_rotation=rotation,offset=offset_)
                
                print(number, element.name, force, moment)
                forces += force
                moments += moment
                # positions += position
                # print('total load: ', forces, moments)


        return [forces, moments, position]

    def turtle_2d_draw(self, screen, parent_move=None, parent_rotation=None, offset=None):
        
        if parent_move == None:
            parent_move = Vector(0, 0)
        if parent_rotation == None:
            parent_rotation = Rotation(0, 0, 0)
        if offset == None:
            offset = Vector(0, 0)

        print(self.name)
        for element in self.elements: #this is the second layer, groupe element
            load_position = None
            print(element.name)


            if len(element.loads) > 0:
                for load in element.loads:
                    if load._type == 'mass':
                        load_position = load.position
                        print('load_position', load.position)
                    else:
                        continue

            # We only draw the element with mass load, the shape is based on the cg position
            else:
                print('skipped element, no mass found')
                continue
            move_rot = {0: {'move': parent_move, 'rotation': parent_rotation},
                        1: {'move': sum(self.moves), 'rotation': sum(self.rotations)},}

            turtle_draw(screen, element, load_position, parent_move=parent_move, parent_rotation=parent_rotation, offset=self.offset+offset)
        
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


        # #remove close,minimaze,maximaze buttons:
        # canvas = screen1.getcanvas()
        # root = canvas.winfo_toplevel()
        # root.overrideredirect(1)

        for number, element in enumerate(self.elements):
            # force = Vector(0,0)
            # moment = Vector(0,0)
            # shape1 = turtle.Turtle()
            # shape1.color = ("black")

            
            force, moment, mass_positions = element.reactions(gravity=Gravity(), offset=None)
            # if load._type == "mass":
            #     turtle_2d_draw(shape2, self, position=position, rotation=rotation)
            
            print(number, element.name, force, moment)
            forces += force
            moments += moment

        return [forces, moments]


    def turtle_2d_draw(self, offset=None):

        screen1, shape1 = init_turtle()


        for element in self.elements:
            if len(element.moves) >=1:
                parent_moves = sum(element.moves)
            else:
                parent_moves = Vector(0, 0)

            if len(element.rotations) >=1:
                parent_rotations = sum(element.rotations)
            else:
                parent_rotations = Rotation(0,0,0)

            element.turtle_2d_draw(screen=screen1, parent_move=parent_moves, parent_rotation=parent_rotations)

        print('machine printed')
        turtle.exitonclick()


def init_turtle():
    screen1 = turtle.Screen()
    screen1.setup(width = 0.25, height = 0.5, startx=0, starty=0)
    shape = turtle.Turtle()
    shape.color = ("blue")
    shape.goto(0, 100)
    shape.penup()
    shape.goto(0, 0)
    shape.pendown()
    shape.goto(100, 0)
    shape.penup()
    shape.goto(0, 0)
    return screen1, shape



def turtle_draw(screen, element, load_position, parent_move=None, parent_rotation=None, offset=None):

    if parent_move == None:
        parent_move = Vector(0, 0)
    if parent_rotation == None:
        parent_rotation = Rotation(0, 0, 0)
    if offset == None:
        offset = Vector(0, 0)

    # # Do the parent changes (move first)
    # load_position += parent_move
    # total_rotation = parent_rotation 
    # pos_rotated = load_position.rotate(parent_rotation+sum(self.rotations))

    # Add self moves and rotation as parent moves and rotation.
    element_move = Vector(0, 0)
    element_rotation = Rotation(0, 0)
    if len(element.moves) >= 1:
        element_move = sum(element.moves)

    if len(element.rotations) >=  1:
        element_rotation = sum(element.rotations)


    element_move_rotated = ((load_position + element_move).rotate(element_rotation) + parent_move).rotate(parent_rotation)

    total_rotation = element_rotation + parent_rotation
    print('turtle_draw', element.length, element.height, element_move_rotated.x, element_move_rotated.y, total_rotation)
    # angle = rotation.gamma
    # shape.penup()
    # shape.goto(x, y)
    # shape.pendown()

    # These are the displacement that will be rotated later
    pts = [Vector(-element.length/2, -element.height/2), Vector(0, element.height), Vector(element.length, 0), Vector(0, -element.height), Vector(-element.length, 0)]
    
    shape = turtle.Turtle()
    shape.color = ("blue")

    # rotated_pts = 

    shape.penup()
    current_position = element_move_rotated
    for point in pts:
        current_position += point
        current_position_rotated = current_position.rotate(element_rotation)
        current_position_rotated = current_position_rotated.rotate(parent_rotation)
        
        shape.goto(current_position_rotated.x + offset.x, current_position_rotated.y + offset.y)
        shape.pendown()






# 3 - Pivot
# bl03 = Vector(-1, 7)
# bl3 = Vector(7, 7)
# bl3.rotate(gamma=mast_angle)
# # print(bl3)
# mg3 = Vector(0, -12) # no rotation gravity is absolute
# result += cross_prod((bl03+bl3), mg3)
# print('with pivot:', result)
    

        
    
        
