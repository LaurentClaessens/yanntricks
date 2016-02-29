from phystricks import *

"""
this is essentially to test the import.
"""

k=pi*radian
k=30*degree
l = Segment(Point(0,0),Point(1,2))
s = Segment(Point(-2,1),Point(-3,4))
l1=l.fix_origin(   Point(2,3*sqrt(5))  )

print("Seem ok")
