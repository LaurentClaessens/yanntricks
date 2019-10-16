#! /usr/bin/sage -python


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

# copyright (c) Laurent Claessens, 2016-2017, 2019
# email: laurent@claessens-donadello.eu

from yanntricks import *

from Testing import assert_true
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test


def testFGetMinMaxData():
    echo_function("testFGetMinMaxData")
    x, y = var('x,y')
    F = ImplicitCurve(x**2+y**2 == sqrt(2), (x, -5, 5),
                      (y, -4, 4), plot_points=300)
    F.plot_points = 10
    d = F.get_minmax_data()
    ans_d = {'xmax': 1.1885897706607917, 'xmin': -1.1885897706608,
             'ymax': 1.188452472892108, 'ymin': -1.1884524728921004}
    assert_true(d == ans_d, failure_message="get_min_max data badly computed.")


def testEnsureUnicode():
    echo_function("testEnsureUnicode")
    from yanntricks.src.NoMathUtilities import ensure_unicode
    from yanntricks.src.NoMathUtilities import ensure_str

    u1 = u"éà"
    s1 = "éà"

    uni_u1 = ensure_unicode(u1)
    str_u1 = ensure_str(u1)

    assert_equal(uni_u1, u1)
    assert_equal(str_u1, s1)

    s2 = "éàù"
    double_s2 = ensure_str(ensure_unicode(s2))
    assert_equal(double_s2, s2)

    u2 = u"éàù"
    double_u2 = ensure_unicode(ensure_str(u2))
    assert_equal(double_u2, u2)


from testNumericalOperations import testNumericalOperations
print("testNumericalOperations")
testNumericalOperations()

from testRecall import testRecall
print("testRecall")
testRecall()

from testSegment import testSegment
print("testSegment")
testSegment()

from testAngleMark import testAngleMark
print("testAngleMark")
testAngleMark()

from testOverloading import testOverloading
print("testOverloading")
testOverloading()

from testAffineVector import testAffineVector
print("testAffineVector")
testAffineVector()

from testIntersection import testIntersection
print("testIntersection")
testIntersection()

from testParametricCurve import testParametricCurve
print("testParametricCurve")
testParametricCurve()

from testPointCoordinates import testPointCoordinates
print("testPointCoordinates")
testPointCoordinates()


from testAngleMeasure import testAngleMeasure
print("testAngleMeasure")
testAngleMeasure()

print("testSegment")
testSegment()

print("testEnsureUnicode")
testEnsureUnicode()
print("testFGetMinMaxData")
testFGetMinMaxData()

from testAffineVector import testAffineVector
print("testAffineVector")
testAffineVector()
