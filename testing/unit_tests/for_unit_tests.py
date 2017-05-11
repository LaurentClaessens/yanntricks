#! /usr/bin/sage -python
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

from phystricks import *

from Testing import assert_true
from Testing import assert_equal
from Testing import assert_almost_equal
from Testing import echo_function
from Testing import echo_single_test

def testFGetMinMaxData():
    echo_function("testFGetMinMaxData")
    x,y=var('x,y')
    F=ImplicitCurve(x**2+y**2==sqrt(2),(x,-5,5),(y,-4,4),plot_points=300)
    F.plot_points=10
    d=F.get_minmax_data()       
    ans_d={'xmax': 1.1885897706607917, 'xmin': -1.1885897706608, 'ymax': 1.188452472892108, 'ymin': -1.1884524728921004}
    assert_true(d==ans_d,failure_message="get_min_max data badly computed.")

def testSegment():
    echo_function("testSegment")
    s= Segment(Point(1,1),Point(2,2))
    v=s.get_normal_vector()
    assert_equal(v.I,Point(1.5,1.5))
    assert_almost_equal(v.length,1,epsilon=0.001)
    assert_almost_equal(v.F,Point(1/2*sqrt(2) + 1.5,-1/2*sqrt(2) + 1.5),epsilon=0.001)

def testEnsureUnicode():
    echo_function("testEnsureUnicode")
    from phystricks.src.NoMathUtilities import ensure_unicode
    from phystricks.src.NoMathUtilities import ensure_str

    u1=u"éà"
    s1="éà"

    uni_u1=ensure_unicode(u1)
    str_u1=ensure_str(u1)

    assert_equal(uni_u1,u1)
    assert_equal(str_u1,s1)

    s2="éàù"
    double_s2=ensure_str( ensure_unicode(s2)  )
    assert_equal(double_s2,s2)

    u2=u"éàù"
    double_u2=ensure_unicode( ensure_str(u2) )
    assert_equal(double_u2,u2)

def testVectorConstructor():
    """
    Test different ways of building a vector.
    """
    echo_function("testVectorConstructor")
    P=Point(4,2)
    O=Point(0,0)
    t=(4,2)
    v1=Vector(P)
    v2=Vector(t)
    v3=Vector(4,2)

    assert_equal(v1.F.x,4)
    assert_equal(v2.F.x,4)
    assert_equal(v3.F.x,4)
    assert_equal(v1.F.y,2)
    assert_equal(v2.F.y,2)
    assert_equal(v3.F.y,2)
    assert_equal(v1.I,O)
    assert_equal(v2.I,O)
    assert_equal(v3.I,O)

def testIntersection():
    """
    Test the intersection function
    """
    echo_function("testIntersection")
    
    x=var('x')
    fun=phyFunction(x**2-5*x+6)
    droite=phyFunction(2)
    pts = Intersection(fun,droite)

    echo_single_test("Function against horizontal line")
    assert_equal(pts[0],Point(1,2))
    assert_equal(pts[1],Point(4,2))

    echo_single_test("Two functions (sine and cosine)")
    f=phyFunction(sin(x))
    g=phyFunction(cos(x))
    pts=Intersection(f,g,-2*pi,2*pi,numerical=True)

    # due to the default epsilon in `assert_almost_equal`,
    # in fact we do not test these points with the whole given precision.
    ans=[]
    ans.append(Point(-5.497787143782138,0.707106781186548))
    ans.append(Point(-2.3561944901923466,-0.707106781186546))
    ans.append(Point(0.7853981633974484,0.707106781186548))
    ans.append(Point(3.926990816987241,-0.707106781186547))
    
    for t in zip(pts,ans):
        assert_almost_equal( t[0],t[1] )

def testAngleMeasure():
        echo_function("testAngleMeasure")

        alpha=AngleMeasure(value_degree=360)
        assert_equal(alpha.__repr__(),"AngleMeasure, degree=360.000000000000,radian=2*pi")

        alpha=AngleMeasure(value_degree=30)
        assert_equal(cos(a.radian),1/2*sqrt(3))


        alpha=AngleMeasure(value_degree=180)
        beta=AngleMeasure(a)
        assert_equal(b.degree,180)

        alpha=AngleMeasure(value_degree=-(3.47548077273962e-14)/pi + 360)
        assert_equal(a.degree,360)
        assert_equal(a.radian,2*pi)

testAngleMeasure()
testIntersection()
testEnsureUnicode()
testFGetMinMaxData()
testSegment()
testVectorConstructor()
