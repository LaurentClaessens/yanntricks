# -*- coding: utf8 -*-

###########################################################################
#   This is part of the module yanntricks
#
#   yanntricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   yanntricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with yanntricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2016-2017
# email: laurent@claessens-donadello.eu

from __future__ import division

from yanntricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test

def test_decorator():
    echo_function("test_decorator")
    v=AffineVector( Point(1,1),Point(2,2) )

    echo_single_test("initial value : None")
    assert_true(v.parameters.color==None)
    assert_true(v.parameters.style==None)

    v.parameters.color="foo"
    v.parameters.style="bar"

    echo_single_test("after fix_origin")
    w=v.fix_origin(Point(3,4))
    assert_true(w.parameters.color=="foo")
    assert_true(w.parameters.style=="bar")

def testOverloading():
    test_decorator()
