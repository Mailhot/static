import numpy as np
from math import sin, cos, radians

class Vector():
	"""A simple vector class to wrap the numpy vector functions"""
	def __init__(self, x, y, z=0, alpha=0, beta=0, gamma=0):
		
		self.x = x
		self.y = y
		self.z = z
		self.alpha = alpha
		self.beta = beta
		self.gamma = gamma

	def __repr__(self):
		return f"({self.x}, {self.y}, {self.z})"

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other): 
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def __neg__(self):
		return Vector(-self.x, -self.y, -self.z)

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

		
