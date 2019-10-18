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

from sage.all import cos, sin
from yanntricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test
from Testing import SilentOutput

from yanntricks.src.Debug import testtype


def test_reverse():
    echo_function("test_reverse")
    x = var('x')
    curve = ParametricCurve(cos(x), sin(x)).graph(0, 2*pi).reverse()

    f1 = cos(-x)
    f2 = sin(-x)

    assert_true(curve.f1.sage == f1)
    assert_true(curve.f2.sage == f2)


def test_second_derivative_vector():
    echo_function("test_second_derivative_vector")

    F = ParametricCurve(x, x**3)

    echo_single_test("normalize=true")
    v = F.get_second_derivative_vector(0, normalize=True)
    ans = AffineVector(Point(0, 0), Point(0, 0))
    assert_equal(v, ans)

    echo_single_test("normalize=false")
    v = F.get_second_derivative_vector(0, normalize=False)
    ans = AffineVector(Point(0, 0), Point(0, 0))
    assert_equal(v, ans)

    echo_single_test("On an other point")
    v = F.get_second_derivative_vector(1)
    ans = AffineVector(Point(1, 1), Point(1, 2))
    assert_equal(v, ans)


def testParametricCurve():
    test_reverse()
    test_second_derivative_vector()
