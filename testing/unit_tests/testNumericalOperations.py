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

# copyright (c) Laurent Claessens, 2017, 2019
# email: laurent@claessens-donadello.eu

from sage.all import sin, cos

from yanntricks import *

from yanntricks.src.point import Point
from yanntricks.src.affine_vector import AffineVector
from yanntricks.src.Visual import visual_length
from yanntricks.src.Numerical import numerical_is_negative
from yanntricks.src.Utilities import number_to_string

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test
from Testing import SilentOutput


def test_visual_length():
    echo_function("test_visual_length")

    with SilentOutput():
        pspict, fig = SinglePicture("ZZTHooTeGyMT")

    v = AffineVector(Point(0, 0), Point(0, sin(0.5*pi)))
    w = visual_length(v, 0.1, pspict=pspict)
    ans = AffineVector(Point(0, 0), Point(0, 0.1))

    echo_single_test("positive")
    assert_equal(w, ans)

    echo_single_test("negative")
    v = AffineVector(Point(0, 0), Point(0, -sin(0.5*pi)))
    w = visual_length(v, 0.1, pspict=pspict)
    ans = AffineVector(Point(0, 0), Point(0, -0.1))
    assert_equal(w, ans)


def test_vector_equality():
    echo_function("test_vector_equality")

    A = Point(1, 1)
    B = Point(2, -3)

    vv = AffineVector(A, B)
    ww = AffineVector(A, B)

    echo_single_test("Two trivial equalities")
    assert_equal(vv, vv)
    assert_equal(ww, ww)

    echo_single_test("One less trivial equalities")
    assert_equal(vv, ww)


def test_is_negative():
    echo_function("test_is_negative")

    echo_single_test("some values")
    a = -sin(0.5*pi)
    assert_true(numerical_is_negative(a))
    a = -pi
    assert_true(numerical_is_negative(a))
    a = pi
    assert_false(numerical_is_negative(a))

    echo_single_test("zero is not negative")
    assert_false(numerical_is_negative(0))


def test_number_to_string():
    echo_function("test_number_to_string")

    a = 7.73542889062775*cos(11/9*pi + 1.30951587282752) - \
        7.55775391156456*cos(5/18*pi) + 2.5*cos(2/9*pi)
    assert_equal(number_to_string(a, digits=7), "0.329851")

    assert_equal(number_to_string(0, digits=15), "0.00000000000000")
    assert_equal(number_to_string(120, digits=3), "120")
    assert_equal(number_to_string(120, digits=5), "120.00")
    assert_equal(number_to_string(120.67, digits=3), "120")
    assert_equal(number_to_string(120.67, digits=4), "120.6")
    assert_equal(number_to_string(120.67, digits=14), "120.67000000000")
    assert_equal(number_to_string(-1, digits=3), "-1.00")
    assert_equal(number_to_string(-12, digits=2), "-12")
    assert_equal(number_to_string(-0.1234, digits=6), "-0.12340")
    assert_equal(number_to_string(-0.12, digits=3), "-0.12")


def testNumericalOperations():
    test_vector_equality()
    test_visual_length()
    test_is_negative()
    test_number_to_string()
