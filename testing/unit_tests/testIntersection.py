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

# copyright (c) Laurent Claessens, 2017
# email: laurent@claessens-donadello.eu

from __future__ import division

from phystricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test
from Testing import SilentOutput

def with_lagrange():
    ## This function tests the fact that non real solutions are discarded.

    echo_function("with_lagrange")

    x=var('x')
    mx=-6
    Mx=2.7
    intersections=[  Point(-5.5,1.5),Point(-3.5,1),Point(-1,1),Point(1.5,-1) ]
    pts1=intersections[:]
    pts1.extend([Point(-4.5,-1),Point(-2,3),Point(1,-1),Point(2.5,0)])
    lag1=LagrangePolynomial(pts1)

    pts2=intersections[:]
    pts2.extend([Point(-4.5,2.5),Point(-2,0),Point(0,1.5),Point(2,-2)])
    lag2=LagrangePolynomial(pts2)

    ans=[]
    ans.append(Point(-6.381638163816381,-1.821966693100714))
    ans.append(Point(-11/2,3/2))
    ans.append(Point(-7/2,1))
    ans.append(Point(-1,1))
    ans.append(Point(3/2,-1))

    pts=Intersection(lag1,lag2)

    for PP in zip(ans,pts):
        assert_equal(PP[0],PP[1])

def lines_and_functions():
    """
    Test the intersection function
    """
    echo_function("lines_and_functions")
    
    x=var('x')
    fun=phyFunction(x**2-5*x+6)
    droite=phyFunction(2)
    pts = Intersection(fun,droite)

    echo_single_test("Function against horizontal line")
    assert_equal(pts[0],Point(1,2))
    assert_equal(pts[1],Point(4,2))

    echo_single_test("Two functions (sine and cosine)")
    f=phyFunction(sin(x))
    g=phyFunction(cos(x))
    pts=Intersection(f,g,-2*pi,2*pi,numerical=True)

    # due to the default epsilon in `assert_almost_equal`,
    # in fact we do not test these points with the whole given precision.
    ans=[]
    ans.append(Point(-5.497787143782138,0.707106781186548))
    ans.append(Point(-2.3561944901923466,-0.707106781186546))
    ans.append(Point(0.7853981633974484,0.707106781186548))
    ans.append(Point(3.926990816987241,-0.707106781186547))
    
    for t in zip(pts,ans):
        assert_almost_equal( t[0],t[1] )

def with_box():
    echo_function("with_box")
    P=Point(2,2)
    box=BoundingBox(xmin=2,ymin=3,xmax=6,ymax,4)
    for Q in point_to_box_intersection(P,box):
        print(Q)
    assert_true(False)
    

def testIntersection():
    with_box()
    with_lagrange()
    lines_and_functions()
