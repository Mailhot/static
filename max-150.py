import element
import config


track_304 = element.track(length=87.2, width=13.8, height=19.1, mass=922, cg=(0,0,0), load_capacity=8200, tractive_effort=8025)
track_306 = element.track(length=102, width=15.8, height=21.4, mass=2260, cg=(0,0,0), load_capacity=15000, tractive_effort=12246)
track_305e2 = element.track(length=101.8, width=15.8, height=21.4, mass=1961, cg=(0,0,0), load_capacity=12000, tractive_effort=13278)
track_308 = element.track(length=104.3, width=17.7, height=26.1, mass=2000, cg=(0,0,0), load_capacity=20940, tractive_effort=116850)

carbody = element.Element(length=56, width=36.6, height=10, mass=2000, cg=(0,0,0))

track_left_carbody = element.Connection(member1=carbody, member1_anchor_position=(-18.3,12,0), member_2=track_308, member2_anchor_position=(8.85,0,0), anchor_rotation=(0,0,0))
track_right_carbody = element.Connection(member1=carbody, member1_anchor_position=(18.3,12,0), member_2=track_308, member2_anchor_position=(-8.85,0,0), anchor_rotation=(0,0,0))


machine1 = element.Machine()
machine.connections.append(track_left_carbody)
machine.connections.append(track_right_carbody)