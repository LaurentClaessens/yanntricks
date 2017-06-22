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

from sage.all import cos,sin
from phystricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test
from Testing import SilentOutput

def test_non_equalities():
    echo_function("test_non_equalities")
    A=Point(0,0)
    B=Point(4.00000000000000*cos(0.111111111111111*pi),0)

    echo_single_test("difficult not 'almost equal'")
    assert_false(A.is_almost_equal(B))
    echo_single_test("difficult not 'really equal'")
    assert_false(A==B)

    v=AffineVector(A,B)
    u=AffineVector(B,A)
    w=AffineVector(A,-B)

    echo_single_test("difficult not 'almost equal' for affine vector")
    assert_false(v.is_almost_equal(w))

    echo_single_test("difficult 'almost equal' for affine vector")
    assert_true(w.is_almost_equal(-v))

def test_equalities():
    echo_function("test_equalities")
    a=3.00000000000000*cos(0.111111111111111*pi)
    b=3.00000000000000*cos(0.111111111111111*pi)

    P=Point(a,0)
    A=Point(0,0)
    B=Point(1,1)

    v1=AffineVector(P,A)
    v2=AffineVector(P,B)

    on=True
    try :
        d=v1+v2
    except OverflowError:
        on=False
    assert_false(on)

    

def test_add_bounding_box():
    echo_function("test_add_bounding_box")

    with SilentOutput():
        pspict,fig = SinglePicture("YDTGooZGkkei")

    A=Point(4.00000000000000*cos(0.111111111111111*pi),0)
    B=Point(0,0)

    pspict.DrawGraphs(A,B)
    fig.conclude()

def test_vertical_horizontal():
    echo_function("test_vertical_horizontal")

    A=Point(1.50000000000000*cos(0.111111111111111*pi),
            -1.50000000000000*sin(0.111111111111111*pi))
    B=Point(3.00000000000000*cos(0.111111111111111*pi),
            -3.00000000000000*sin(0.111111111111111*pi))
    seg=Segment(A,B)
    assert_equal(seg.is_vertical,False)
    assert_equal(seg.is_horizontal,False)

def test_right_angle():
    echo_function("test_right_angle")
    with SilentOutput():
        pspict,fig = SinglePicture("HYVFooTHaDDQ")

    A=Point(2.96406976477346*cos(-1/9*pi + 1.09432432510594),
            2.96406976477346*sin(-1/9*pi + 1.09432432510594))
    B=Point(1.50000000000000*cos(0.111111111111111*pi),
            -1.50000000000000*sin(0.111111111111111*pi))
    C=Point(3.00000000000000*cos(0.111111111111111*pi),
            -3.00000000000000*sin(0.111111111111111*pi))

    rh=RightAngleAOB(A,B,C)
    pspict.DrawGraphs(rh)

def testPointCoordinates():
    test_right_angle()
    test_vertical_horizontal()
    test_add_bounding_box()
    test_non_equalities()
    test_equalities()
