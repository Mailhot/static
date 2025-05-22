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
        self.xr = x
        self.yr = y 
        self.zr = z 


    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

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
            self.x = round(result[0], 2)
            self.y = round(result[1], 2)
            self.z = round(result[2], 2)
            return self
            

    
class Rotation(Vector):
    """A rotation class, same as vector but with values in degree"""
    def __init__(self, alpha=0, beta=0, gamma=0):
        super().__init__(x=alpha, y=beta, z=gamma)
    
    def __repr__(self):
        return f"Rotation({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"Rotation({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Rotation(self.x+other.x, self.y+other.y, self.z+other.z)

    def __radd__(self, other):
        if other in [0, Rotation(0,0)]:
            return Rotation(self.x, self.y, self.z)
        else:
            return other.__add__(self)
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
        return f'Load{self.position, self.charge, self._type}'

    def rotate(self, rotation=Rotation(0)):
        self.position.rotate(rotation)
        if self._type in ['force']: #moments and gravity does not rotate with displacement. 
            self.charge.rotate(rotation)
        return Load(self.position, self.charge, self._type)

    def move(self, x, y, z=0):
        # self.position.x += x
        # self.position.y += y
        # self.position.z += z
        return Load(self.position+Vector(x, y, z), self.charge, self._type)

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
            final_position += parent_move #.rotate(parent_rotation)
        
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
    def __init__(self, length=0, width=0, height=0, loads=None, name=None, elements=None, offset=None, rotations=None, moves=None):
        """
        Basic element class for calculation various thing on an element assembly
        offset: a vector to offset the origin of a group without affecting the rotations
        """
        self.length = length
        self.width = width
        self.height = height
        self.name = name
        if loads is None:
            loads = []
        self.loads = loads
        if moves is None:
            moves = []
        self.moves = []
        if rotations is None:
            rotations = []
        self.rotations = rotations
        if elements is None:
            elements = []
        self.elements = elements
        self.ops = []

        if offset is None:
            offset = Vector(0, 0)
        self.offset = offset

    def __repr__(self):

        return f"Element(length={self.length}, width={self.width}, height={self.height}, loads={self.loads}, name={self.name}, elements={self.elements}, offset={self.offset}, rotations={self.rotations}, moves={self.moves})"

    def rotate(self, rotation):
        # Rotate the element from it's origin
        # rotation = Rotation(alpha, beta, gamma)
        if isinstance(rotation, Rotation):
            self.ops.append(rotation)
            self.rotations.append(rotation)
        else:
            print(f'ERROR: need to have a Rotation() type to make a rotation got {type(rotation)}')
        return self

    def move(self, move):
        # move = Vector(x=x, y=y, z=z)
        self.ops.append(move)
        self.moves.append(move)
        return self

    def reactions(self, gravity=None, parent_move=None, parent_rotation=None, offset=None):
        
        forces = Vector(0,0,0)
        moments = Vector(0,0,0)
        positions = Vector(0,0,0)
        # move = Vector(0,0)
        # rotation = Rotation(0,0)
        print('-', self.name)
        print('parent move and rotation', parent_move, parent_rotation)
        print('element moves and rotations:', self.name, self.moves, self.rotations)

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

        # TODO: The moves will be affected by parent rotations. 
        if parent_move != None:

            move += parent_move

        if parent_rotation != None:
            # rotate the move based on parent rotation
            
            rotation += parent_rotation
            move.rotate(rotation)
            # print('rotated move', move)

        # print()
        # print('parent move and rotation:', parent_move, parent_rotation)
        if self.loads:
            for load in self.loads:
                
                force, moment, position = load.reactions(gravity=gravity, parent_move=move, parent_rotation=rotation, offset=offset_)
                forces += force
                moments += moment

        if self.elements: # TODO: ?An element has either child elements or loads not both.
            for number, element in enumerate(self.elements):
                
                force, moment, position = element.reactions(gravity=gravity, parent_move=move, parent_rotation=rotation,offset=offset_)
                print(number, element.name, force, moment, position)
                forces += force
                moments += moment

        return [forces, moments, position]


    def draw(self, parent_operation=None, parent_move=None, parent_rotation=None, offset=None):

        if parent_move == None:
            parent_move = Vector(0, 0)
        if parent_rotation == None:
            parent_rotation = Rotation(0, 0, 0)
        if offset == None:
            offset = Vector(0, 0)
        if parent_operation == None: 
            total_parent_ops = self.ops
        elif parent_operation != None:
            total_parent_ops = self.ops + parent_operation

        # if len(self.moves) >=1:
        #     parent_moves += sum(self.moves)
        # else:
        #     parent_moves = Vector(0, 0)
        # if len(self.rotations) >=1:
        #     parent_rotations += sum(self.rotations)
        # else:
        #     parent_rotations = Rotation(0,0,0)



        total_elements = self.elements

        # if the current element has a load, draw it.
        if len(self.loads) > 0:
            total_elements.append(self)

        print('drawing:', self.name)
        outputs = []

        for element in total_elements: #this is the second layer, group element
            load_position = None
            print(element.name)

            if len(element.loads) > 0:
                for load in element.loads:
                    if load._type == 'mass':
                        load_position = load.position
                        print('load_position', load.position)
                    else:
                        continue
                if len(element.elements) > 0 and element != self:
                    output = element.draw(parent_move=parent_move, parent_operation=total_parent_ops, parent_rotation=parent_rotation, offset=self.offset+offset)
                else:
                    output = draw(element, load_position, parent_operation=total_parent_ops, parent_move=parent_move, parent_rotation=parent_rotation, offset=self.offset+offset)
                
                if type(output) == list:
                    outputs += output
                else: 
                    outputs.append(output)

            # We only draw the element with mass load, the shape is based on the cg position
            else:
                print('skipped element, no mass found')
                continue

        return outputs




class Machine():
    """A machine class that can contain multiple elements (that moves relatives to each other), a gravity member
    elements: element class that apply to the machine
    gravity: a gravity load instance default to y=-1
    **parameters: a keyword arguments of variables parameters for the machine ex: mast angle
    add items to elements starting from the fartherst to the ground, in a chain. This way partial section will work.
    TODO: what about partial section I.E. A crane, or 2 mast.
    """

    def __init__(self, elements=None, gravity=None):

        if not elements:
            elements = []
        if not gravity:
            gravity = Gravity()
        self.elements = elements
        self.gravity = gravity

    def get_results(self, vector):
        # get a resulting force at a desired place of the model. 
        # will calculate the element resulting forces and moment starting from the last one
        pass

    def reactions(self):
        forces = Vector(0, 0, 0)
        moments = Vector(0, 0, 0)
        positions = Vector(0, 0)


        # #remove close,minimaze,maximaze buttons:
        # canvas = screen1.getcanvas()
        # root = canvas.winfo_toplevel()
        # root.overrideredirect(1)
        # print(self.elements[0].name)
        for number, element in enumerate(self.elements):
            force = Vector(0,0)
            moment = Vector(0,0)
            # shape1 = turtle.Turtle()
            # shape1.color = ("black")

            
            force, moment, mass_positions = element.reactions(gravity=Gravity(), offset=None)
            # if load._type == "mass":
            #     turtle_2d_draw(shape2, self, position=position, rotation=rotation)
            
            print(number, element.name, force, moment)
            forces += force
            # positions += mass_positions
            moments += moment

        return {'forces': forces, "moments": moments}

    def draw(self, offset=None, screen=None):

        
        elements_out = []
        for element in self.elements:
        
            output = element.draw(parent_move=None, parent_rotation=None, offset=offset)
            elements_out += output


        print('machine printed')
        return elements_out


    


def draw(element, load_position, parent_operation=None, parent_move=None, parent_rotation=None, offset=None):

    # if parent_move == None:
    #     parent_move = Vector(0, 0)
    # if parent_rotation == None:
    #     parent_rotation = Rotation(0, 0, 0)
    if offset == None:
        offset = Vector(0, 0)

    if parent_operation == None:
        tot_operations = element.ops 
    elif parent_operation != None:
        tot_operations = element.ops + parent_operation

    


    # Add self moves and rotation as parent moves and rotation.
    element_move = Vector(0, 0)
    element_rotation = Rotation(0, 0)
    # if len(element.moves) >= 1:
    #     element_move = sum(element.moves)

    # if len(element.rotations) >=  1:
    #     element_rotation = sum(element.rotations)
    element_move_rotated = load_position
    total_rotation = Rotation(0, 0)
    if tot_operations != None:
        for operation in tot_operations:
            print(operation)
            if isinstance(operation, Rotation):
                total_rotation += operation 
                element_move_rotated.rotate(operation)
            elif isinstance(operation, Vector):
                element_move_rotated += operation



    # element_move_rotated = ((load_position + element_move).rotate(element_rotation) + parent_move).rotate(parent_rotation)
    # print('a', element_rotation, 'b', parent_rotation)
    total_rotation = total_rotation + parent_rotation
    print('draw', element.length, element.height, element_move_rotated.x, element_move_rotated.y, total_rotation)
    final_position = (element_move_rotated.x+offset.x, element_move_rotated.y+offset.y)
    print('rotation', total_rotation)

    output = {'length': element.length, 'height': element.height, 'angle': total_rotation.z, 'color': 'RED', 'center': (element_move_rotated.x, -element_move_rotated.y)}
    print('output:', output)
    return output







# 3 - Pivot
# bl03 = Vector(-1, 7)
# bl3 = Vector(7, 7)
# bl3.rotate(gamma=mast_angle)
# # print(bl3)
# mg3 = Vector(0, -12) # no rotation gravity is absolute
# result += cross_prod((bl03+bl3), mg3)
# print('with pivot:', result)
    

        
    
        
