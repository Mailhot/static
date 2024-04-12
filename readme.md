Todo: 
make a test case for 2d and probably 3d

Make a function in element to get the equivalent center of mass for the element.
We should be able to cut the model between 2 load and get a load moment value at a point?

TODO: add visualisation tool to show the different components
TODO: make the element englobable where we can englobe few components with another element, and move them as group.


Note: 
rotate always happens in the current origin, moving an element or load will affect 
it's own origin, so rotating after moving will happen around the new origin.


Elements holds multiple loads, loads are define into their own referentials and then moved into the element referential or rotated.

The moves on an element does not affect the loads position, they are added on calculating results like forces. They 
are stored into the element as list of moves and rotations. 


Test case #1
base reactions: [(0, -14035, 0), (105800.0, 0.0, -428429.1003577506)]
0 base (0, -14035, 0) (105800.0, 0.0, -428429.1003577506)
1 mast (-6.735557395310442e-13, -16200.0, 0.0) (0.0, 0.0, 818630.0)

reactions: [(-6.735557395310442e-13, -30235.0, 0.0), (105800.0, 0.0, 390200.8996422494)]