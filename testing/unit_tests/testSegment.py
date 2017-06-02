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

def test_constructors():
    seg=Segment(  Point(0,0),Point(2,10) )
    assert_equal(seg.I,Point(0,0))
    assert_equal(seg.F,Point(2,10))

    seg2=Segment(  Point(-3,4),vector=Vector(1,2) )
    assert_equal(seg.I,Point(-3,4))
    assert_equal(seg.F,Point(-2,6))

    v=AffineVector(  Point(1,2),Point(-2,5) )
    seg3=Segment(  Point(-3,4),vector=v )
    assert_equal(seg.I,Point(-3,4))
    assert_equal(seg.F,Point(-6,7))

def testSegment():
    test_constructors()

