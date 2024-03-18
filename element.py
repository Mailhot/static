
class Element():
	"""Basic element class for calculation various thing on an element assembly"""
	def __init__(self, length, width, height, mass, cg=(0,0,0)):
		super(element, self).__init__()
		self.length = length
		self.width = width
		self.height = height
		self.mass = mass
		self.cg = cg


class Connection():
	"""A connection class to connect multiple Element
	The connection is composed by 2 members and their relative position.
	The first member referential serves as the main referential here.
	member1: Element class of a component
	member1_anchor_position: vector in the member1 referencial to locate the anchor position of member2
	member2: second Element class to be connected
	member2_anchor_position: Vector in the member2 referencial to locate connection location in the member2 referential.
	anchor_rotation: rotation vector to identify the rotation of member2 into member1 referential

	each connection has got an anchor vector relative to their member referential, and a rotation vector relative
	each connection has got a rotation theta_x theta_y theta_z to define it's orientation
	"""
	def __init__(self, member1, member1_anchor_position, member_2, member2_anchor_position, anchor_rotation):
		self.member1 = member1
		self.member1_anchor_position = member1_anchor_position
		self.member2 = member2
		self.member2_anchor_position = member2_anchor_position
		self.anchor_rotation = anchor_rotation
		


		

class Track(Element):
	"""An instance of a track (single), with it's own parameters"""
	def __init__(self, load_capacity, tractive_effort):
		super(Track, self).__init__()
		self.load_capacity = load_capacity
		self.tractive_effort = tractive_effort
		
		
class Machine():
	"""A machine class that englobe multiple elements and connections to form a group of components"""
	def __init__(self, connections=[]):
		self.connections = connections


	# Find the maximum overall width of a machine
	def find_width(self):
		for connection in connections:
			pass