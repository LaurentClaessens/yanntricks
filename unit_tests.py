from phystricks import *

"""
This file contains only doctests with output too long or not sufficiently interesting to be included in the code itself.

sage: v = Segment(Point(0,0),Point(2,0)).get_normal_vector()
sage: print v.arrow_type
vector
sage: s= Segment(Point(1,1),Point(2,2))
sage: v=s.get_normal_vector()
sage: print v.I
Point(1.5,1.5)
sage: print v.F
Point(1/2*sqrt(2) + 1.5,-1/2*sqrt(2) + 1.5)
sage: print v.length()
1


sage: l = Segment(Point(0,0),Point(0,1))
sage: v = AffineVector(Point(-1,1),Point(-2,3))
sage: print v.equation
x + 1/2*y + 1/2 == 0
"""

