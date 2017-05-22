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

# copyright (c) Laurent Claessens, 2016-2017
# email: laurent@claessens-donadello.eu

from __future__ import division

from phystricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test

from phystricks.src.Debug import dprint

def vector_constructor():
    """
    Test different ways of building a vector.
    """
    echo_function("vector_constructor")
    P=Point(4,2)
    O=Point(0,0)
    t=(4,2)
    v1=Vector(P)
    v2=Vector(t)
    v3=Vector(4,2)

    assert_equal(v1.F.x,4)
    assert_equal(v2.F.x,4)
    assert_equal(v3.F.x,4)
    assert_equal(v1.F.y,2)
    assert_equal(v2.F.y,2)
    assert_equal(v3.F.y,2)
    assert_equal(v1.I,O)
    assert_equal(v2.I,O)
    assert_equal(v3.I,O)

def orthogonal_decompostion():
    echo_function("orthogonal_decomposition")
    v=Vector(2,3)
    perp,parall = v.decomposition(Segment(Point(0,0),Point(0,1)))

    echo_single_test("In the Y direction")

    ans_parall=AffineVector( Point(0,0),Point(0,3) )
    ans_perp=AffineVector( Point(0,0),Point(2,0) )

    assert_true( parall+perp==v )
    assert_equal(parall,ans_parall)
    assert_equal(perp,ans_perp)

    P=Point(0,2)
    seg = Segment(P,P.get_polar_point(2,-130))


    Q=seg.get_point_proportion(0.5)
    v=AffineVector( Q, Point(Q.x-1,Q.y) )
    perp,paral = v.decomposition(seg)

    echo_single_test("130 degree : sum")
    assert_equal(perp+paral,v)

    echo_single_test("130 degree : orthogonal")
    assert_true(perp.segment.is_almost_orthogonal(seg,epsilon=0.0001))

    ip=perp.inner_product(paral)
    echo_single_test("130 degree : inner product 1")
    assert_equal(perp.inner_product(paral),0)
    echo_single_test("130 degree : inner product 2")
    assert_equal(paral.inner_product(perp),0)

def translation():
    echo_function("translation")
    v=Vector(2,1)                        
    P=Point(-1,-1)
    assert_equal(P.translate(v),Point(1,0))

    w=AffineVector( Point(1,1),Point(2,3) )
    assert_equal(P.translate(w),Point(0,1))

    assert_equal(P.translate(10,-9),Point(9,-10))

    x,y=var('x,y')
    P=Point(x,y)
    assert_equal(P.translate(Vector(-P)),Point(0,0))

def projection():
    echo_function("projection")
    s1=Segment( Point(0,0),Point(2,1) )
    assert_equal(Point(3,-1).projection(s1),Point(2,1))
    assert_equal(Point(5,0).projection(s1),Point(4,2))
    assert_equal(Point(5,0).projection(Vector(2,1)),Point(4,2))

def testAffineVector():
    orthogonal_decompostion()
    projection()
    translation()
    vector_constructor()
