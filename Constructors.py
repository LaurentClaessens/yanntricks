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

def Point(a,b):
    """
    return a point.

    INPUT:

    - ``x,y`` - the coordinates of the point. These are numbers.


    EXAMPLES::

        sage: from phystricks import *
        sage: print Point(1,1)
        <Point(1,1)>
        sage: print Point(pi,sqrt(2))
        <Point(pi,sqrt(2))>
    
    You can pass variables::

        sage: x=var('x')
        sage: P=Point(x**2,1)   
        sage: print P
        <Point(x^2,1)>

    Notice that the coordinates of the point have to be numerical in order to be passed to tikz (and then LaTeX) at the end::

    """
    import GraphOfAPoint
    return GraphOfAPoint.GraphOfAPoint(a,b)

def PolarPoint(r,theta):
    """
    return the point at polar coordinates (r,theta).

    INPUT:

    - ``r`` - the distance from origine
    - ``theta`` - the angle

    EXAMPLES::

        sage: from phystricks import *
        sage: print PolarPoint(2,45)
        <Point(sqrt(2),sqrt(2))>


    """
    return Point(r*cos(radian(theta)),r*sin(radian(theta)))

def Segment(A,B=None,vector=None):
    """
    Creates a segment.

    The typical use is to give two points.
    An alternative is to provide a point and a vector.

    EXAMPLES::

        sage: from phystricks import *
        sage: seg=Segment(  Point(0,0),Point(2,10) )
        sage: print seg.I            
        <Point(0,0)>
        sage: print seg.F
        <Point(2,10)>
        sage: seg2=Segment(  Point(-3,4),vector=Vector(1,2) )
        sage: print seg2.I            
        <Point(-3,4)>
        sage: print seg2.F
        <Point(-2,6)>
        sage: v=AffineVector(  Point(1,2),Point(-2,5) )
        sage: seg3=Segment(  Point(-3,4),vector=v )
        sage: print seg3.I            
        <Point(-3,4)>
        sage: print seg3.F
        <Point(-6,7)>
    """
    if vector:
        B=A+vector
    import GraphOfASegment
    return GraphOfASegment.GraphOfASegment(A,B)


def PolarSegment(P,r,theta):
    """
    returns a segment on the base point P (class Point) of length r angle theta (degree)
    """
    alpha = radian(theta)
    import GraphOfASegment
    return Segment(P, Point(P.x+r*cos(alpha),P.y+r*sin(alpha)) )


def AffineVector(A=None,B=None):
    """
    return an affine vector.

    An affine vector is a vector whose origin is not specifically (0,0).

    EXAMPLES:
        
    An affine vector can be given by two points::

        sage: from phystricks import *
        sage: print AffineVector(Point(1,1),Point(pi,sqrt(2)))
        <vector I=<Point(1,1)> F=<Point(pi,sqrt(2))>>

    It can be simply derived from a segment::

        sage: segment=Segment( Point(1,1),Point(2,2)  )
        sage: av=AffineVector(segment)
        sage: print av
        <vector I=<Point(1,1)> F=<Point(2,2)>>

    If you pass an object which has a method `segment`, the
    :func:`AffineVector` will provide the corresponding affine vector::

        sage: from phystricks.BasicGeometricObjects import SingleAxe
        sage: axe=SingleAxe(  Point(-2,2),Vector(1,1),-3,3  )
        sage: print AffineVector(axe)
        <vector I=<Point(-5,-1)> F=<Point(1,5)>>

    NOTE:

    The main difference between a :func:`Segment` an :func:`AffineVector` is that
    the latter will be draw with an arrow. There are also some difference in their
    behaviour under rotation, dilatation and operations like that.

    """
    if B :      # If B is given, I suppose that we gave two points
        vect=Segment(A,B)
    else :
        try :
            vect=A.segment()
        except AttributeError :
            vect=A
    vect.arrow_type="vector"
    return vect
