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

def test_equalities():
    echo_function("test_equalities")
    A=Point(4.00000000000000*cos(0.111111111111111*pi),0)
    B=Point(0,0)

    echo_single_test("almost_equal")
    b=0
    if A.is_almost_equal(B):    # an == here raises an 'OverflowError'
        b=1
    assert_equal(b,0)

    echo_single_test("overflowError")
    b=0
    try :
        if A==B:
            pass
    except OverflowError :
        b=2
    assert_equal(b,2)

def test_add_bounding_box():
    echo_function("test_add_bounding_box")

    with SilentOutput():
        pspict,fig = SinglePicture("YDTGooZGkkei")

    A=Point(4.00000000000000*cos(0.111111111111111*pi),0)
    B=Point(0,0)

    pspict.DrawGraphs(A,B)
    fig.conclude()

def testPointCoordinates():
    test_add_bounding_box()
    test_equalities()
