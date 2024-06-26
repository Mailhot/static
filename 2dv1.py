from vector import Vector, cross_prod


# current position
mast_angle = 90 #mast angle taken from horizontal
holdback = 8000 #lbs

## Components
# 0 - track
bl00 = Vector(0, 0) # the base referential is at the same place as the origin
bl0 = Vector(30, 5)
mg0 = Vector(0, -10)
result = cross_prod(bl0, mg0)
print('track moment: ', result)

# 1 - Platform
bl01 = Vector(-3, 10)
bl1 = Vector(33, 5)
mg1 = Vector(0, -20)
result += cross_prod((bl01+bl1), mg1)
print('with platform added:', result)

# 2 - Base
bl02 = Vector(-3, 15)
bl2 = Vector(5, 5)
mg2 = Vector(0, -10)
result += cross_prod((bl02+bl2), mg2)
print('with base:', result)

# 3 - Pivot
bl03 = Vector(-1, 7)
bl3 = Vector(7, 7)
bl3.rotate(gamma=mast_angle)
# print(bl3)
mg3 = Vector(0, -12) # no rotation gravity is absolute
result += cross_prod((bl03+bl3), mg3)
print('with pivot:', result)

# 4 - Mast
bl04 = bl03 + Vector(-20, 10).rotate(gamma=mast_angle) #we refer position of mast from the pivot point so that the angle will define everything. Otherwise we would have to re-position this point based on the angle.
bl4 = Vector(60, 8).rotate(gamma=mast_angle)
mg4 = Vector(0, -40)
result += cross_prod((bl04+bl4), mg4)
print('with mast:', result)

# 5 - Head
bl05 = bl04 + Vector(20, 10).rotate(gamma=mast_angle)
bl5 = Vector(15, 10).rotate(gamma=mast_angle)
mg5 = Vector(0, -20)
result += cross_prod((bl05+bl5), mg5)
print('with head:', result)

# 6 - Engine
bl06 = Vector(30, 35)
bl6 = Vector(22.5, 20)
mg6 = Vector(0, -450) # around 450 lbs
result += cross_prod((bl06+bl6), mg6)
print('with engine:', result)

#7 - Pumps (2x tandem K3VL60)
bl07 = Vector(10, 35)
bl7 = Vector(8, 5)
mg7 = Vector(0, -110) # 110 lbs for the 2 of them
result += cross_prod((bl07+bl7), mg7)
print('with pump:', result)

#8 - Jacks (4x of them)
bl08 = Vector(0, 30)
bl8 = Vector(60, 25)
mg8 = Vector(0, -800)
result += cross_prod((bl08+bl8), mg8)
print('with jacks:', result)


## Forces
# 21 - drilling force
bl0_21 = bl05 # We use the head referential
bl21 = Vector(0, 12).rotate(gamma=mast_angle)
f21 = Vector(-holdback, 0).rotate(gamma=mast_angle) #holdback is negative it goes in minus x direction.
result_f21 = cross_prod((bl0_21+bl21), f21)
print('moment for holdback force:', result_f21)
result += result_f21

result = -result
print('Reaction at point:', result)
