from vector import Vector, cross_prod, Element, Load, Machine, Rotation, Gravity
import pygame


machine1 = Machine(gravity=Gravity())

cube1 = Element(name='Cube1')
machine1.elements.append(cube1)

machine1.turtle_2d_draw()