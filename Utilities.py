# -*- coding: utf8 -*-

###########################################################################
#   This is part of the module phystricks
#
#   phystricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   phystricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with phystricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2010-2016
# email: moky.math@gmai.com

def Distance_sq(P,Q):
    """ return the squared distance between P and Q """
    return (P.x-Q.x)**2+(P.y-Q.y)**2

def Distance(P,Q):
    """ return the distance between P and Q """
    return sqrt(Distance_sq(P,Q))

def inner_product(v,w):
    """
    Return the inner product of vectors v and w

    INPUT:
    - ``v,w`` - two vectors or points

    OUTPUT:
    a number

    If the vectors are not based at (0,0), make first 
    the translation and return the inner product.

    If a point is passed, it is considered as the vector
    from (0,0).

    EXAMPLES::

    sage: from phystricks import *
    sage: from phystricks.BasicGeometricObjects import *
    sage: v=Vector(1,3)
    sage: w=Vector(-5,7)
    sage: inner_product(v,w)
    16

    sage: v=AffineVector(Point(1,1),Point(2,2))
    sage: w=AffineVector(Point(-2,5),Point(-1,4))
    sage: inner_product(v,w)
    0
    """
    try:
        a=v.Point()
    except AttributeError:
        a=v
    try:
        b=w.Point()
    except AttributeError:
        b=w
    return a.x*b.x+a.y*b.y

def Intersection(f,g,a=None,b=None,numerical=False,only_real=True):
    """
    When f and g are objects with an attribute equation, return the list of points of intersections.

    The list of point is sorted by order of `x` coordinates.

    If 'only_real' is True, return only the real solutions.

    Only numerical approximations are returned as there are some errors otherwise. As an example the following 
    solving return points that are not even near from the circle x**2+y**2=9
    solve(    [   -1/3*sqrt(3)*y + 1/3*sqrt(3)*(-0.19245008972987399*sqrt(3) - 3) + x == 0,x^2 + y^2 - 9 == 0    ],[x,y]   )
    Position : 313628350

    EXAMPLES::

        sage: from phystricks import *
        sage: fun=phyFunction(x**2-5*x+6)
        sage: droite=phyFunction(2)
        sage: pts = Intersection(fun,droite)
        sage: for P in pts:print P
        <Point(1,2)>
        <Point(4,2)>

        sage: f=phyFunction(sin(x))
        sage: g=phyFunction(cos(x))
        sage: pts=Intersection(f,g,-2*pi,2*pi,numerical=True)
        sage: for P in pts:print P
        <Point(-5.497787143782138,0.707106781186548)>
        <Point(-2.3561944901923466,-0.707106781186546)>
        <Point(0.7853981633974484,0.707106781186548)>
        <Point(3.926990816987241,-0.707106781186547)>

    If 'numerical' is True, it search for the intersection points of the functions 'f' and 'g' (it only work with functions). In this case an interval is required.
    """

    if numerical and "sage" in dir(f) :
        k=f-g
        xx=SmallComputations.find_roots_recursive(k.sage,a,b)
        pts=[  Point(x,f(x)) for x in xx ]
        for P in pts:
            if "I" in P.coordinates():
                print("There should not be imaginary part")
                raise
        return pts

    x,y=var('x,y')
    pts=[]
    if numerical :
        soluce=solve([f.equation(numerical=True),g.equation(numerical=True)],[x,y])
    else :
        soluce=solve([f.equation(),g.equation()],[x,y])
    for s in soluce:
        a=s[0].rhs()
        b=s[1].rhs()
        z=a**2+b**2
        ok1,a=test_imaginary_part(a)
        ok2,b=test_imaginary_part(b)
        if ok1 and ok2 :
            pts.append(Point(a,b))
    pts.sort(lambda P,Q:cmp(P.x,Q.x))
    for P in pts:
        if "I" in P.coordinates():
            print("There should not be imaginary part")
            print(f.equation,g.equation)
            raise
    return pts
