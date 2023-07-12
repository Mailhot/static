from sympy.physics.mechanics import *
from sympy import symbols
mechanics_printing(pretty_print=False)
f = symbols('f')
q, p, u, v = dynamicsymbols('q, p, u, v')
base = Body('base')
boom = Body('boom')
pivot = Body('Pivot')

joint1 = PinJoint(
    'hinge', base, boom, coordinates=q, speeds=u,
    parent_point=3 * base.frame.x,
    child_point=-3 * boom.frame.x,
    joint_axis=base.frame.z)

joint2 = PinJoint(
    'hinge', boom, pivot, coordinates=p, speeds=v,
    parent_point=3 * boom.frame.x,
    child_point=-3 * pivot.frame.x,
    joint_axis=boom.frame.z)

force1 = f*pivot.y
point1 = Point('A')
pivot.apply_force(force1, point1) 

print(pivot.loads)
print(boom.loads)

method = JointsMethod(base, )

# print(joint1.kdes)
# print(joint1.parent_point.pos_from(base.masscenter))
# print(joint1.parent_interframe)
# print(joint1.joint_axis.express(boom.frame))
# print(boom.masscenter.pos_from(base.masscenter))
# print(boom.masscenter.vel(base.frame))
