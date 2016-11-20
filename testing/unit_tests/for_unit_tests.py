#! /usr/bin/sage -python
# -*- coding: utf8 -*-

from __future__ import division

from phystricks import *

from Testing import roundingForTest
from Testing import assert_true
from Testing import assert_equal
from Testing import assert_almost_equal

"""
This file contains only doctests with output too long or not sufficiently interesting to be included in the code itself.
"""

def testFGetMinMaxData():
    x,y=var('x,y')
    F=ImplicitCurve(x**2+y**2==sqrt(2),(x,-5,5),(y,-4,4),plot_points=300)
    d=F.get_minmax_data()
    F.plot_points=10
    d=F.get_minmax_data()       
    assert_true(roundingForTest(d)=={'xmin': -1.189, 'ymin': -1.188, 'ymax': 1.188, 'xmax': 1.189},failure_message="get_min_max data badly computed or rounding failure.")
    assert_true(roundingForTest(d)==roundingForTest({'xmin': -1.1890000000000001, 'ymin': -1.1879999999999999, 'ymax': 1.1879999999999999, 'xmax': 1.1890000000000001}),failure_message="get_min_max data badly computed or rounding failure.")

def testSegment():
    s= Segment(Point(1,1),Point(2,2))
    v=s.get_normal_vector()
    assert_equal(v.I,Point(1.5,1.5))
    assert_almost_equal(v.length,1,epsilon=0.001)
    assert_almost_equal(v.F,Point(1/2*sqrt(2) + 1.5,-1/2*sqrt(2) + 1.5),epsilon=0.001)

testFGetMinMaxData()
testSegment()

