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

def test_almost_equal():
    echo_function("test_almost_equal")
    s= Segment(Point(1,1),Point(2,2))
    v=s.get_normal_vector()
    assert_equal(v.I,Point(1.5,1.5))
    assert_almost_equal(v.length,1,epsilon=0.001)
    assert_almost_equal(v.F,Point(1/2*sqrt(2) + 1.5,-1/2*sqrt(2) + 1.5),epsilon=0.001)

def test_constructors():

    echo_single_test("Usual constructor")
    seg=Segment(  Point(0,0),Point(2,10) )
    assert_equal(seg.I,Point(0,0))
    assert_equal(seg.F,Point(2,10))

    echo_single_test("Construct with a vector")
    seg=Segment(  Point(-3,4),vector=Vector(1,2) )
    assert_equal(seg.I,Point(-3,4))
    assert_equal(seg.F,Point(-2,6))

    echo_single_test("Construct with an affine vector")
    v=AffineVector(  Point(1,2),Point(-2,5) )
    seg=Segment(  Point(-3,4),vector=v )
    assert_equal(seg.I,Point(-3,4))
    assert_equal(seg.F,Point(-6,7))

def testSegment():
    test_constructors()
    test_almost_equal()

