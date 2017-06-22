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
from sage.all import cos

from phystricks import *

from Testing import assert_true
from Testing import assert_false
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test

def comparison():
    echo_function("comparison")
    alpha=AngleMeasure(value_degree=30)
    beta=AngleMeasure(value_radian=pi/2)

    assert_true(alpha<beta)
    assert_true(alpha<=alpha)
    assert_true(alpha==alpha)
    assert_false(alpha==beta)
    assert_true(alpha>=alpha)


def testAngleMeasure():
    echo_function("testAngleMeasure")

    comparison()

    alpha=AngleMeasure(value_degree=360)
    assert_equal(alpha.__repr__(),
                    "AngleMeasure, degree=360.000000000000,radian=2*pi")

    alpha=AngleMeasure(value_degree=30)
    assert_equal(cos(alpha.radian),1/2*sqrt(3))


    alpha=AngleMeasure(value_degree=180)
    beta=AngleMeasure(alpha)
    assert_equal(beta.degree,180)

    alpha=AngleMeasure(value_degree=-(3.47548077273962e-14)/pi + 360)
    assert_equal(alpha.degree,360)
    assert_equal(alpha.radian,2*pi)

    alpha=AngleMeasure(value_degree=-30)
    assert_equal(alpha.positive().degree,330)


    alpha=AngleMeasure(value_degree=45)
    beta=AngleMeasure(value_radian=pi/3)
    assert_equal(alpha.degree,45)
    assert_equal(alpha.radian,1/4*pi)
    assert_equal(beta.degree,60)
    assert_equal(beta.radian,1/3*pi)

    a_sum_b = alpha+beta
    assert_equal(a_sum_b.degree,105)
    assert_equal(a_sum_b.radian,7/12*pi)

