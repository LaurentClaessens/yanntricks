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

# copyright(c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu

from sage.all import sin, cos, prod, var
from sage.all import pi, PolynomialRing, QQ, symbolic_expression

from yanntricks.src.Utilities import distance
from yanntricks.src.degree_unit import degree
from yanntricks.src.point import Point
from yanntricks.src.AxesGraph import Axes
from yanntricks.src.Utilities import Intersection
from yanntricks.src.segment import Segment
from yanntricks.src.GridGraph import GridGraph
from yanntricks.src.MathStructures import AxesUnit
from yanntricks.src.MarkGraph import MarkGraph
from yanntricks.src.BoundingBox import BoundingBox
from yanntricks.src.AngleGraph import AngleGraph
from yanntricks.src.CircleGraph import CircleGraph
from yanntricks.src.affine_vector import AffineVector
from yanntricks.src.PerspectiveGraphs import CuboidGraph
from yanntricks.src.Utilities import EnsureParametricCurve
from yanntricks.src.MiscGraph import FractionPieDiagramGraph
from yanntricks.src.phyFunctionGraph import phyFunctionGraph
from yanntricks.src.ParametricCurveGraph import ParametricCurveGraph
from yanntricks.src.interpolation_curve import InterpolationCurve
from yanntricks.src.NonAnalytic import NonAnalyticPointParametricCurveGraph


def PolarPoint(r, theta):
    """
    return the point at polar coordinates (r,theta).

    INPUT:

    - ``r`` - the distance from origine
    - ``theta`` - the angle

    EXAMPLES::

        sage: from yanntricks import *
        sage: print PolarPoint(2,45)
        <Point(sqrt(2),sqrt(2))>
    """
    from yanntricks.src.point import Point
    from yanntricks.src.radian_unit import radian
    return Point(r*cos(radian(theta)), r*sin(radian(theta)))


def PolarSegment(P, r, theta):
    """
    return a segment on the base point P (class Point) of 
    length r and angle theta (degree)
    """
    from yanntricks.src.point import Point
    from yanntricks.src.radian_unit import radian
    alpha = radian(theta)
    return Segment(P, Point(P.x+r*cos(alpha), P.y+r*sin(alpha)))


def Circle(center, radius, angleI=0, angleF=360, visual=False, pspict=None):
    """
    Return a circle of given radius and center.

    INPUT:

    - ``center`` - the center of the circle.

    - ``radius`` - the radius of the circle.

    - ``angleI`` - (default=0) If you want an arc of circle, this is the beginning angle.
    - ``angleF`` - (default=0) If you want an arc of circle, this is the ending angle.
    - ``visual`` - (default=False) if 'True', the radius is taken as a 'visual' length. This option only affects the underlying parametric curve and then the graph. It is probably buggy to attempt to get normal and tangent vectors when a dilatation is performed when 'visual' is True.

    OUTPUT:

    A circle ready to be drawn

    EXAMPLES:

    The following describes the usual trigonometric circle::

            sage: from yanntricks import *
            sage: circle=Circle(Point(0,0),1)
            sage: print circle.angleI
            AngleMeasure, degree=0.000000000000000,radian=0
            sage: print circle.angleF
            AngleMeasure, degree=360.000000000000,radian=0

    """
    # TODO: in the last example, the radian value should be 2*pi.
    if visual and not pspict:
        print("You cannot try to use 'visual' not giving a pspicture")
        raise ValueError
    return CircleGraph(center, radius, angleI=angleI, angleF=angleF, visual=visual, pspict=pspict)


def CircleOA(O, A):
    """
    From the centrer O and a point A, return the circle.

    INPUT:

    - ``O`` - a point that will be the center of the circle.

    - ``A`` - a point on the circle.

    OUTPUT:

    A circle ready to be drawn of type :class:`CircleGraph`.

    EXAMPLES::

        sage: from yanntricks import *
        sage: A=Point(2,1)
        sage: O=Point(0,0)
        sage: circle=CircleOA(O,A)
        sage: circle.radius
        sqrt(5)

    """
    from yanntricks.src.Utilities import distance
    radius = distance(O, A)
    return Circle(O, radius)


def CircleAB(A, B):
    """
    return a circle with diameter [AB]
    """
    from yanntricks.src.segment import Segment
    center = Segment(A, B).midpoint()
    return CircleOA(center, A)


def CircularSector(center, radius, a, b):
    from yanntricks.src.segment import Segment
    circle = Circle(center, radius)
    P = circle.get_point(a)
    Q = circle.get_point(b)
    l1 = Segment(circle.center, P)
    l2 = circle.graph(a, b)
    l3 = Segment(Q, circle.center)
    return CustomSurface(l1, l2, l3)


def FractionPieDiagram(center, radius, a, b):
    return FractionPieDiagramGraph(center, radius, a, b)


def Mark(graph=None, dist=None, angle=None, central_point=None, text="", mark_point=None, position=None, pspict=None):
    """
    Describe a mark on a point.

    The provided distance and angle are visual. That is
    P.put_mark(0.3,45, ... )
    will place a mark at distance 0.3 and angle 45 from the point P *on the picture*. This is why a pspicture is needed.

    INPUT:

    - ``graph`` - the graph that it marked. This is usually a point but it can be anything that has a `mark_point` method.
    - ``dist`` - the distance between `graph.mark_point()` and the mark.
    - ``angle`` - the angle given in degree or `AngleMeasure`.
    - ``text`` - the text to be printed on the mark. This is typically a LaTeX stuff like "$P$".
    - ``position`` - is one of "corner","N","S","W","E" or special cases (see below).

            - "corner" will put the mark at the distance such that the corner of the bounding box is at the (relative) position (dist;angle) instead of the center of the mark.
            - "N" will put the mark in such a way that the center of the north side of the bounding box is at the position (dist;angle).

            - "for axes". In this case we expect to have a 3-tuple `(pspict,"for axes",segment)` where `segment` is a segment (typically the segment of an axe).  In this case, we suppose `self.angle` to be orthogonal to the segment.  The mark will be put sufficiently far for the bounding box not to cross the segment.

         What is done is that the closest corner of the bounding box is at position (dist;angle) from the point.
    - ``pspict`` - the pspict in which the mark has to be computed and drawn.
    """
    return MarkGraph(graph, dist, angle, text, central_point=central_point, mark_point=mark_point, position=position, pspict=pspict)


def AngleAOB(A, O, B, r=None):
    """
    Return the angle AOB.

    It represent the angle formed at the point O with the lines
    OA and OB (in that order).

    INPUT:

    - ``A,O,A`` - points.

    - ``r`` - (default, see below) the radius of the arc circle marking the angle.

    OUTPUT:

    An object ready to be drawn of type :class:`AngleGraph`.

    If `r` is not given, a default value of 0.2 times the length OA is taken.

    EXAMPLES:

    Notice the difference between AOB and BOA::

        sage: from yanntricks import *
        sage: A=Point(1,1)
        sage: O=Point(0,0)
        sage: B=Point(1,0)
        sage: print Angle(A,O,B).measure()
        AngleMeasure, degree=-45.0000000000000,radian=-1/4*pi
        sage: print Angle(B,O,A).measure()
        AngleMeasure, degree=45.0000000000000,radian=1/4*pi


    .. literalinclude:: yanntricksTriangleRectangle.py
    .. image:: Picture_FIGLabelFigTriangleRectanglePICTTriangleRectangle-for_eps.png

    """
    return AngleGraph(A, O, B, r)


def phyFunction(fun, mx=None, Mx=None):
    """
    Represent a function.

    INPUT:

    - ``fun`` - a function.
    - ``mx,Mx`` - initial and final value of the argument.

    EXAMPLES::

        sage: from yanntricks import *
        sage: f=phyFunction(cos(x))
        sage: f(pi/2)
        0

        sage: g=phyFunction(2*f,0,pi)
        sage: g(pi)
        -2

        One can deal with probability distributions :
        sage: C=RealDistribution('chisquared',10).distribution_function
        sage: f=phyFunction(C)
        sage: f(4)
        0.0451117610789

    EXAMPLES with function for which one don't know analytic form

    .. literalinclude:: yanntricksChiSquared.py
    .. image:: Picture_FIGLabelFigChiSquaredPICTChiSquared-for_eps.png

    OTHER EXAMPLE

    .. literalinclude:: yanntricksNonAnalyticOne.py
    .. image:: Picture_FIGLabelFigNonAnalyticOnePICTNonAnalyticOne-for_eps.png

    """

    # The first try is that the given expression is already a phyFunction.
    try:
        return fun.graph(mx, Mx)
    except (AttributeError, TypeError):
        pass

    # The second try is that `fun` is something that Sage knows.
    try:
        sy = symbolic_expression(fun)
    except TypeError:   # Happens with probability distributions.
        return phyFunctionGraph(fun, mx, Mx)

    x = var('x')
    return phyFunctionGraph(sy.function(x), mx, Mx)


def ParametricCurve(f1, f2, interval=(None, None)):
    """
    Construct a parametric curve from its two Cartesian coordinates functions.

    INPUT:

    - ``f1,f2`` - functions that are the components of the parametric curve.
    - 'interval' - the interval on which the curve is considered.

    If 'f1' has mx and Mx and interval is not given, they are used.

    OUTPUT:
    an object ready to be drawn.

    EXAMPLES::

        sage: from yanntricks import *
        sage: x=var('x')
        sage: f1=phyFunction(x)
        sage: f2=phyFunction(x**2)
        sage: F=ParametricCurve(f1,f2).graph(-2,3)
        sage: G=ParametricCurve(f1,f2,mx=-2,Mx=3)

    Notice that due to several `@lazy_attribute`, changing the components after creation could produce unattended results.

    .. literalinclude:: yanntricksCycloide.py

    .. image:: Picture_FIGLabelFigCycloidePICTCycloide-for_eps.png

    """
    from yanntricks.src.Utilities import EnsurephyFunction
    from yanntricks.src.AngleMeasure import AngleMeasure
    llamI = interval[0]
    llamF = interval[1]
    if "mx" in dir(f1):
        if f1.mx != None:
            llamI = f1.mx
            llamF = f1.Mx
    f1 = EnsurephyFunction(f1)
    f2 = EnsurephyFunction(f2)
    if isinstance(llamI, AngleMeasure):
        raise
    return ParametricCurveGraph(f1, f2, llamI, llamF)


def NonAnalyticPointParametricCurve(f, mx, Mx):
    """
    Describe a parametric curve when we have a function 'f' that associates a Point from a value of the parameter.

    - f : a function (in the Python sense) that takes a number as argument and which returns a Point.
    - mx,Mx  : the minimal and maximal values of the parameters.
    """
    return NonAnalyticPointParametricCurveGraph(f, mx, Mx)


def MeasureLength(seg, dist=0.1):
    """
    When a segment exists, one wants sometimes to denote its length drawing a double-arrow parallel to the segment. This is what this class is intended to.

    The segment (and then the graph associated with the mark) is the parallel one,
    not the segment given in argument.

    INPUT:

    - ``seg`` - the segment to be measured.

    - ``dist`` - the distance between the segment and the measure.

    The sign of <dist> is an issue. If you give 0.3 you get one result, if you give
    -0.3, you get the segment on the other side.
    The algorithm is the following. If v is the vector seg.I --> seg.F and w is the vector from
    <seg> to the arrow line to be drawn, then (v,w) has the same orientation as (Y,X) where X=(1,0) 
    and Y=(0,1).
    The rational is that if the segment is vertical, we want the measure to appear
    on the right.

    EXAMPLES:

    .. literalinclude:: yanntricksIntervalleUn.py
    .. image:: Picture_FIGLabelFigIntervallePICTIntervalle-for_eps.png

    In order to check the position of the arrow line,
    we check the position of the mark_point::

        sage: from yanntricks import *
        sage: O=Point(0,0)
        sage: A=Point(1,0)

    Horizontal line directed from right to left; the
    arrow line has to be bellow::

        sage: measureOA=MeasureLength(Segment(O,A),0.1)
        sage: print measureOA.mark_point()
        <Point(0.5,-0.100000000000000)>

    Horizontal line directed from left to right::

        sage: measureAO=MeasureLength(Segment(A,O),0.1)
        sage: print measureAO.mark_point()
        <Point(0.5,0.100000000000000)>

    Vertical line::

        sage: B=Point(0,2)
        sage: measureOB=MeasureLength(Segment(O,B),0.1)
        sage: print measureOB.mark_point()
        <Point(0.100000000000000,1.0)>



    USEFUL ATTRIBUTE:

    - ``self.advised_mark_angle`` - the angle at which we advise you to put the mark.
                                    It indicates the direction orthogonal to the segment,
                                    with the orientation given in the discussion about the
                                    sign of <dist>.

    ::

        sage: m=MeasureLength(Segment( Point(1,1) ,Point(2,2) ),0.1)
        sage: print m.advised_mark_angle
        AngleMeasure, degree=315.000000000000,radian=7/4*pi

    You are invited to use advised_mark_angle. If not the position of the mark
    could be unpredictable.
    """
    from yanntricks.src.MeasureLengthGraph import MeasureLengthGraph
    return MeasureLengthGraph(seg, dist)


def CustomSurface(*args):
    r"""
    Represent the surface contained between some lines and (parametric) curves.

    INPUT:
    - ``*args`` - la tuple of lines like segments, functions, parametric curves.

    EXAMPLE:

    The following describes the surface between the circle of radius 1 and 
    the square of length 1::

        sage: from yanntricks import *
        sage: C=Circle(Point(0,0),1)
        sage: arc=C.parametric_curve(0,pi/2)
        sage: h=Segment(Point(0,1),Point(1,1))
        sage: v=Segment(Point(1,1),Point(1,0))
        sage: surf=CustomSurface(arc,h,v)

    The border is not drawn.

    This is somewhat the more general use of the pstricks's macro \pscustom
    """
    if len(args) == 1:        # This is in the case in which we give a tuple or a list directly
        a = args[0]
    else:
        a = args
    from yanntricks.src.CustomSurfaceGraph import CustomSurfaceGraph
    return CustomSurfaceGraph(list(a))


def RightAngle(d1, d2, n1=0, n2=1, r=0.3):
    """
    'd1' and 'd2' are the two lines.
    'r' is the size of the "edge"
    'n1' and 'n2' are 0 ot 1 and are determining which of the 4 angles has to be marked (two lines -> 4 angles)
    """
    from yanntricks.src.AngleGraph import RightAngleGraph
    return RightAngleGraph(d1, d2, r, n1, n2)


def RightAngleAOB(A, O, B, n1=0, n2=1, r=0.3):
    """
    return the right angle between Segment(A,O) and Segment(O,B)
    """
    from yanntricks.src.segment import Segment
    return RightAngle(Segment(A, O), Segment(O, B), n1, n2, r)


def PolarCurve(fr, ftheta=None):
    """
    return the parametric curve (:class:`ParametricCurve`) corresponding to the 
    curve of equation r=f(theta) in polar coordinates.

    If ftheta is not given, return the curve
    x(t)=fr(t)cos(t)
    y(t)=fr(t)sin(t)

    If ftheta is given, return the curve
    x(t)=fr(t)cos( ftheta(t) )
    y(t)=fr(t)sin( ftheta(t) )

    EXAMPLES::

    .. literalinclude:: yanntricksCardioid.py
    .. image:: Picture_FIGLabelFigCardioidPICTCardioid-for_eps.png

    """
    x = var('x')
    if ftheta is None:
        f1 = fr*cos(x)
        f2 = fr*sin(x)
    else:
        f1 = fr(x=x)*cos(ftheta(x=x))
        f2 = fr(x=x)*sin(ftheta(x=x))
    return ParametricCurve(f1, f2)


def LagrangePolynomial(*args):
    """
    return as `phyFunction` the Lagrange polynomial passing
    trough the given points

    You can either provide a list of points or some points.
    """
    # http://ask.sagemath.org/question/1815/polynomialring-and-from-__future__-import
    points_list = []
    for arg in args:
        try:
            for P in arg:
                points_list.append(P)
        except TypeError:
            points_list.append(arg)
    R = PolynomialRing(QQ, str('x'))
    f = R.lagrange_polynomial([(float(P.x), float(P.y)) for P in points_list])
    return phyFunction(f)


def HermiteInterpolation(points_list):
    """
    return a polynomial that pass trough the given points with the given derivatives.

    Each element of points_list is a triple
    (x,y,d)
    and the given polynomial satisfies P(x)=y and P'(x)=d

    EXAMPLES :

    sage : P=HermiteInterpolation( [  (1,14,7),(3,64,51),(-2,-16,31)    ] )
    sage: P.simplify_full()
    2*x^3 - x^2 + 3*x + 10

    """
    x = var('x')
    n = len(points_list)
    xx = {i: points_list[i][0] for i in range(0, n)}
    y = {i: points_list[i][1] for i in range(0, n)}
    d = {i: points_list[i][2] for i in range(0, n)}

    b = {i: (x-xx[i])**2 for i in range(0, n)}

    Q = {}
    for j in range(0, n):
        Q[j] = prod([b[i] for i in range(0, n) if i != j])
    P = {}
    for j in range(0, n):
        parenthese = 1-(x-xx[j])*Q[j].diff(x)(xx[j])/Q[j](xx[j])
        P[j] = (Q[j](x)/Q[j](xx[j]))*(parenthese*y[j]+(x-xx[j])*d[j])
    f = sum(P.values())
    return phyFunction(f.expand())


def Polygon(*args):
    """
    represent a polygon.

    You can give either a list of point or a list containing the points :

    .. literalinclude:: yanntricksExPolygone.py
    .. image:: Picture_FIGLabelFigExPolygonePICTExPolygone-for_eps.png
    """
    from yanntricks.src.PolygonGraph import PolygonGraph
    if len(args) == 1:     # In this case, we suppose that this is a list
        # args is a tupe containing the arguments. If you call
        # Polygon([P,Q]) then args[0] is [P,Q]
        return PolygonGraph(args[0])
    return PolygonGraph(list(args))


def Rectangle(*args, **arg):
    """
    INPUT:

    - ``NW,SE`` - the North-West corner and South-East corner

    Alternatively, you can pass a bounding box as unique argument.

    Still alternatively, you can pass xmin,ymin,xmax,ymax
    """
    from yanntricks.src.BoundingBox import BoundingBox
    if len(args) == 2:
        NW = args[0]
        SE = args[1]
    if len(args) == 1:
        NW = args[0].NW()
        SE = args[0].SE()
    if "xmin" in arg:
        bb = BoundingBox(xmin=arg["xmin"], ymin=arg["ymin"],
                         xmax=arg["xmax"], ymax=arg["ymax"])
        # TODO : I should be able to pass directly the dictionary to BoundingBox
        NW = bb.getVertex("NW")
        SE = bb.getVertex("SE")
    if "mx" in arg:
        bb = BoundingBox(xmin=arg["mx"], ymin=arg["my"],
                         xmax=arg["Mx"], ymax=arg["My"])
        # TODO : I should be able to pass directly the dictionary to BoundingBox
        NW = bb.getVertex("NW")
        SE = bb.getVertex("SE")
    from yanntricks.src.RectangleGraph import RectangleGraph
    return RectangleGraph(NW, SE)


def Circle3D(op, O, A, B, angleI=0, angleF=2*pi):
    from yanntricks.src.PerspectiveGraphs import Circle3DGraph
    return Circle3DGraph(op, O, A, B, angleI, angleF)


def Vector3D(x, y, z):
    from yanntricks.src.PerspectiveGraphs import Vector3DGraph
    return Vector3DGraph(x, y, z)


def Cuboid(op, P, a, b, c):
    """
    - `op` -- the projection method.
    - `P` -- tuple (x,y) giving the lower left point
    - `a,b,c` -- lengths of the edges.

          +--------------------------+
        0/ |                       1/|
        /  |         0             / |
        0-------------------------1  |
        |  |                      |  |
        |  |                     1|  | 
       3|  |______________________|__|
        |3/                       |2/
        |/           2            |/
        3-------------------------2

    """
    return CuboidGraph(op, P, a, b, c)


def Grid(bb):
    return GridGraph(bb)


def intervals(curve1, curve2, interval, interval1, interval2):
    if interval:
        mx1 = interval[0]
        Mx1 = interval[1]
        mx2 = interval[0]
        Mx2 = interval[1]
        return mx1, Mx1, mx2, Mx2
    if interval1:
        mx1 = interval1[0]
        Mx1 = interval1[1]
    else:
        mx1, Mx1 = extract_interval_information(curve1)
    if interval2:
        mx2 = interval2[0]
        Mx2 = interval2[1]
    else:
        mx2, Mx2 = extract_interval_information(curve2)
    return mx1, Mx1, mx2, Mx2


def SurfaceBetweenParametricCurves(curve1, curve2, interval=None, interval1=None, interval2=None, reverse1=False, reverse2=True):
    """
    Represents a surface between two parametric curves.

    'curve1' and 'curve2' are parametric curves or objects that have
    a method 'parametric_curve'

        FOR THE INTERVALS :

        - interval=(pI,PF)    where pI and pF are the initial and final
        value of this parameter

        If you want to choose these parameters separately, use
        - interval1=(pI1,pF1),interval2=(pI2,pF2)

        You have to give either 'interval' or both 'interval1' and 'interval2'

        - If "interval" is given, it erases all other choices.
        - If neither 'interval' and 'interval1' are given,
        search in 'curve1' if there is something to eat.

    OPTIONAL ARGUMENTS :

    - ``reverse1`` - (default=False) if True, reverse the sense of curve1.

    - ``reverse2`` - (default=True) if True, reverse the sense of curve1.

    Let us suppose that curve1 goes from A1 to B1 and curve2 from A2 to B2
    If we do not reverse the sense of anything, the result will be
    the surface delimited by

    curve1:        A1 -> B1
    Fsegment:    B1 -> B2
    curve2:        A2 -> B2
    Isegment:   A2 -> A1

    This is wrong since the last point of each line is not the first
    point of the next line.

    For that reason, the second curve is, by default, reversed in order to get
    curve1:             A1 -> B1
    Fsegment:         B1 -> B2
    curve2 (reversed):  B2 -> A2
    Isegment:        A2 -> A1

    OUTPUT:
    An object ready to be drawn.

    EXAMPLES::

        sage: from yanntricks import *
        sage: curve1=ParametricCurve(x,x**2).graph(2,3)
        sage: curve2=ParametricCurve(x,x**3).graph(2,5)
        sage: region=SurfaceBetweenParametricCurves(curve1,curve2)

    The segment "closing" the domain are available by
    the attributes `Isegment and Fsegment`::

        sage: print region.Isegment
        <segment I=<Point(2,8)> F=<Point(2,4)>>
        sage: print region.Fsegment
        <segment I=<Point(3,9)> F=<Point(5,125)>>

    The initial and final values of the parameters can be given
    in different ways.
    The "normal" way is to provide the curves by triples `(curve,mx,Mx)`::

        sage: f1=phyFunction(x**2)
        sage: f2=phyFunction(x)
        sage: curve=SurfaceBetweenParametricCurves((f1,1,2),(f2,3,4))
        sage: print curve.mx1,curve.Mx1,curve.mx2,curve.Mx2
        1 2 3 4

    If one of the curve is provided without interval, the latter will
    be deduced::

        sage: f1=phyFunction(x**2).graph(1,2)
        sage: f2=phyFunction(x)
        sage: curve=SurfaceBetweenParametricCurves(f1,(f2,3,4))
        sage: print curve.mx1,curve.Mx1,curve.mx2,curve.Mx2
        1 2 3 4

    If the optional argument `interval` is provided, it erases
    the other intervals::

        sage: f1=phyFunction(x**2).graph(1,2)
        sage: f2=phyFunction(x)
        sage: curve=SurfaceBetweenParametricCurves(f1,(f2,3,4),interval=(7,8))
        sage: print curve.mx1,curve.Mx1,curve.mx2,curve.Mx2
        7 8 7 8

    NOTE:
    If the two curves make intersections, the result could be messy.

    .. literalinclude:: yanntricksBetweenParametric.py
    .. image:: Picture_FIGLabelFigBetweenParametricPICTBetweenParametric-for_eps.png

    """
    from yanntricks.src.segment import Segment
    exceptions = [CircleGraph, Segment]

    on = True
    for ex in exceptions:
        if isinstance(curve1, ex):
            on = False
    if on:
        iz11 = curve1.f1.nul_function
        iz21 = curve2.f1.nul_function

    on = True
    for ex in exceptions:
        if isinstance(curve2, ex):
            on = False
    if on:
        iz22 = curve2.f2.nul_function
        iz12 = curve1.f2.nul_function

    mx = [None, None]
    Mx = [None, None]
    mx[0], Mx[0], mx[1], Mx[1] = intervals(
        curve1, curve2, interval, interval1, interval2)

    curve = [curve1, curve2]

    for i in [0, 1]:
        curve[i] = EnsureParametricCurve(curve[i]).graph(mx[i], Mx[i])

    c1 = curve[0]
    c2 = curve[1]
    mx1 = mx[0]
    mx2 = mx[1]
    Mx1 = Mx[0]
    Mx2 = Mx[1]

    try:
        c1.f1.nul_function = iz11
        c1.f2.nul_function = iz12
        c2.f1.nul_function = iz21
        c2.f2.nul_function = iz22
    except UnboundLocalError:
        pass

    from yanntricks.src.SurfacesGraph import SurfaceBetweenParametricCurvesGraph
    surf = SurfaceBetweenParametricCurvesGraph(
        c1, c2, (mx1, mx2), (Mx1, Mx2), reverse1, reverse2)

    surf.add_option("fillstyle=vlines,linestyle=none")
    return surf


def SurfaceUnderFunction(f, mx, Mx):
    """
    Represent a surface under a function.

    This is a particular case of SurfaceBetweenFunctions when
    the second function is the y=0 axis.

    The function `f` becomes `self.f1` while self.f2 will be the
    function 0 (this is a consequence of inheritance).
    The function f will also be recorded as self.f.

    INPUT:

    - ``f`` - a function
    - ``mx,Mx`` - initial and final values 

    EXAMPLES:

    .. literalinclude:: yanntricksSurfaceFunction.py
    .. image:: Picture_FIGLabelFigSurfaceFunctionPICTSurfaceFunction-for_eps.png


    .. literalinclude:: yanntricksChiSquaresQuantile.py
    .. image:: Picture_FIGLabelFigChiSquaresQuantilePICTChiSquaresQuantile-for_eps.png

    """
    from yanntricks.src.NonAnalytic import NonAnalyticFunctionGraph
    from yanntricks.src.point import Point
    from yanntricks.src.segment import Segment
    from yanntricks.src.SurfacesGraph import SurfaceBetweenLines
    if isinstance(f, NonAnalyticFunctionGraph):
        line1 = Segment(Point(mx, 0), Point(Mx, 0))
        line2 = f.parametric_curve(mx, Mx)
        surf = SurfaceBetweenLines(line1, line2)
        return surf
    f2 = phyFunction(0)
    f2.nul_function = True  # See 2252914222
    return SurfaceBetweenFunctions(f, f2, mx=mx, Mx=Mx)


def SurfaceBetweenFunctions(f1, f2, mx=None, Mx=None):
    r"""
    Represents a surface between two functions.

    INPUT:

    - ``f1,f2`` - functions (sage or phyFunction). ``f1`` is considered
    to be the upper function while ``f2`` is the lower function.

    - ``mx,Mx`` - (optional) initial and end values of x.
    If these are not given, we suppose that `f1` and `f2` are graphs.
        If `f1` is a graph while `mx` is given, t
        he value of `f1.mx` is forgotten and the given `mx`
        is taken into account.

    EXAMPLES:

    If you want the surface to be blue ::

        sage: from yanntricks import *
        sage: surf=SurfaceBetweenFunctions(sin(x)+3,cos(x),0,2*pi)
        sage: surf.parameters.color="blue"

    If you want the function ``f1`` to be red without changing
    the color of the surface, you have to change the color AND the style::

        sage: surf.f1.parameters.color="red"

    You can also try to control the option linestyle (use add_option).

    .. literalinclude:: yanntricksexSurfaceBetweenFunction.py

    .. image:: Picture_FIGLabelFigexSurfaceBetweenFunctionPICTexSurfaceBetweenFunction-for_eps.png

    """
    mx1 = mx
    mx2 = mx
    Mx1 = Mx
    Mx2 = Mx
    if "mx" in dir(f1) and mx is None:
        mx1 = f1.mx
        Mx1 = f1.Mx
    if "mx" in dir(f2) and mx is None:
        mx2 = f2.mx
        Mx2 = f2.Mx
    # The following is a precaution because it can happen that
    # f1 has a "mx" attribute which is set to None while
    # a mx is given here.
    if mx1 is None:
        mx1 = mx
    if Mx1 is None:
        Mx1 = Mx
    if mx2 is None:
        mx2 = mx
    if Mx2 is None:
        Mx2 = Mx
    x = var('x')
    curve1 = ParametricCurve(x, f1, (mx1, Mx1))
    curve2 = ParametricCurve(x, f2, (mx2, Mx2))
    return SurfaceBetweenParametricCurves(curve1, curve2, (mx1, Mx1), (mx, Mx2))


def extract_interval_information(curve):
    """
    return the interval of the curve.

    That is the initial and final value of the parameter
    of `curve` if that is a :class:`ParametricCurve` and
    the initial and final values of `x` if this the graph of a function.

    INPUT:

    - ``curve`` - graph of a function or a parametric curve

    OUTPUT:

    a tuple of numbers. If nothing is found, return (None,None).

    EXAMPLES::

        sage: from yanntricks import *
        sage: from yanntricks.BasicGeometricObjects import *
        sage: f=phyFunction(x**2).graph(1,pi)
        sage: extract_interval_information(f)
        (1, pi)

        sage: from yanntricks.BasicGeometricObjects import *
        sage: a=var('a')
        sage: curve=ParametricCurve(x,sin(x)).graph(sqrt(2),a)
        sage: extract_interval_information(curve)
        (sqrt(2), a)

        sage: f=phyFunction(x**3)
        sage: extract_interval_information(f)
        (None, None)

    """
    # For parametric curves
    if "llamI" in dir(curve):
        return curve.llamI, curve.llamF
    # for functions
    if "mx" in dir(curve):
        return curve.mx, curve.Mx
    # for segments
    if "I" in dir(curve) and "F" in dir(curve):
        return 0, curve.length()
    # for circles
    if "angleI" in dir(curve):
        # We know that circles are AngleI and AngleF that are of type 'AngleMeasure'
        # we are thus returning 'curve.angleI.radian' instead of 'curve.angleI'
        return curve.angleI.radian, curve.angleF.radian
    return None, None


def SudokuGrid(question, length=1):
    from yanntricks.src.SudokuGridGraph import SudokuGridGraph
    return SudokuGridGraph(question, length)


def phyMatrix(nlines, ncolumns):
    from yanntricks.src.MatrixGraph import MatrixGraph
    return MatrixGraph(nlines, ncolumns)


def EllipseOAB(O, A, B):
    """
    An ellipse of center O and such that OA and OB are the axis 
    (OA and OB are supposed to be orthogonal)
    """
    from yanntricks.src.EllipseGraph import EllipseGraph
    return EllipseGraph(O, A, B)


def BarDiagram(X, Y):
    if len(X) != len(Y):
        raise ValueError("X and Y must be of the same size.")
    from yanntricks.src.BarDiagramGraph import BarDiagramGraph
    return BarDiagramGraph(X, Y)


def Histogram(tuple_box_list, legende=None):
    """
    An histogram is given by a list of tuple '(a,b,n)' where 'a' and 'b' are the extremal values of the box and 'n' is the number of elements in the box.
    """
    from yanntricks.src.HistogramGraph import HistogramGraph
    return HistogramGraph(tuple_box_list, legende)


def BoxDiagram(values, h, delta_y=0):
    from yanntricks.src.BoxDiagramGraph import BoxDiagramGraph
    return BoxDiagramGraph(values, h, delta_y)


def Moustache(minimum, Q1, M, Q3, maximum, h, delta_y=0):
    """
    Q1 and Q3 are first and third quartiles; M is the median.
    h is the size of the box
    """
    from yanntricks.src.MoustacheGraph import MoustacheGraph
    return MoustacheGraph(minimum, Q1, M, Q3, maximum, h, delta_y)


def ImplicitCurve(f, xrange, yrange, plot_points=100):
    """
    return the implicit curve given by equation f on the range xrange x yrange

    This is a constructor for the class ImplicitCurveGraph
    INPUT:

    - ``f`` -- a function of two variables or equation in two variables

    - ``xrange,yrange`` - the range on which we want to compute the implicit curve.

    OPTIONAL INPUT:

    - ``plot_points`` - (defautl : 100) the number of points that will be calculated in each direction. 

    The resulting bounding box will not be in general xrange x yrange. 

    EXAMPLES:

    We know that the curve x^2+y^2=2 is a circle of radius sqrt(2). Thus even if you ask a range of size 5,  you will only get the bounding box of size sqrt(2).

    EXAMPLES::

    sage: from yanntricks import *
    sage: x,y=var('x,y')
    sage: f(x,y)=x**2+y**2
    sage: F=ImplicitCurve(f==2,(x,-5,5),(y,-5,5))
    sage: print F.bounding_box()
    <BoundingBox mx=-1.413,Mx=1.413; my=-1.413,My=1.413>

    But the following will be empty::

    sage: G=ImplicitCurve(f==2,(x,-1,1),(y,-1,1))
    sage: print G.paths
    []

    If you give very low value of plot_points, you get incorrect results::

    sage: H=ImplicitCurve(f==2,(x,-2,2),(y,-2,2),plot_points=3)
    sage: print H.bounding_box()
    <BoundingBox mx=-1.414,Mx=1.414; my=-1.414,My=1.414>


    Using Sage's implicit_curve and matplotlib, a list of points "contained" in the curve is created. The bounding_box is calculated from that list. The pstricsk code generated will be an interpolation curve passing trough all these points.
    """
    from yanntricks.src.ImplicitCurve import GeometricImplicitCurve
    return GeometricImplicitCurve(f).graph(xrange, yrange, plot_points=100)


class ObliqueProjection(object):
    def __init__(self, alpha, k):
        """
        This is the oblique projection of angle `alpha` and scale factor `k`.

        `alpha` is given in degree. It is immediately converted in order to have positive number. If you give -45, it will be converted to 315
        """
        from yanntricks.src.AngleMeasure import AngleMeasure
        from yanntricks.src.radian_unit import radian
        self.k = k
        if self.k >= 1:
            print("Are you sure that you want such a scale factor : ",
                  float(self.k))
        self.alpha = alpha
        a = AngleMeasure(value_degree=self.alpha).positive()
        self.alpha = a.degree
        self.theta = radian(self.alpha)
        self.kc = self.k*cos(self.theta)
        self.ks = self.k*sin(self.theta)

    def point(self, x, y, z):
        from yanntricks.src.point import Point
        return Point(x+z*self.kc, y+z*self.ks)

    def cuboid(self, P, a, b, c):
        """
        `P` -- a tupe (x,y) that gives the lower left point.

        `a,b,c` the size
        """
        return Cuboid(self, P, a, b, c)


def Text(P, text, hide=True):
    """
    A text.

    INPUT:

    - ``P`` - the point at which the center of the bounding box will lie.

    - ``text`` - the text.

    - ``hide`` - (default=True) When `True`, the background of the text is hidden by
                    a rectangle. The color and style of that rectangle can be customized,
                    see :class:`BasicGeometricObjects.TextGraph`

    """
    from yanntricks.src.BasicGeometricObjects import TextGraph
    return TextGraph(P, text, hide=hide)


def VectorField(fx, fy, xvalues=None, yvalues=None, draw_points=None):
    """
    return a vector field that is drawn on the points given in the list.

    INPUT:

    - ``fx,fy`` - two functions

    OPTIONAL :

    - ``xvalues`` - a tuple `(x,mx,Mx,n)` where `mx` and `Mx` are the min and max values of x and
                    `n` is the number of values to be used on that interval.

    - ``draw_points`` - a list of points on which the vector field has to be drawn.
                        If draw_point is given, xvalues and yvalues are not taken into account.

    OUTPUT:
    the graphe vector field.

    EXAMPLES::

        sage: from yanntricks import *
        sage: x,y=var('x,y')
        sage: F=VectorField(x*y,cos(x)+y)
        sage: F.divergence()
        (x, y) |--> y + 1


    If you want an automatic Cartesian grid of points, use xvalues and yvalues::

        sage: F=VectorField(exp(x+y),x**2+y**2,xvalues=(x,-1,1,3),yvalues=(y,-5,5,6))
        sage: len(F.draw_points)
        18
        sage: print F.draw_points[5]
        <Point(-1.0,5.0)>

    The same can be obtained using the following syntax (see the function GeometricVectorField.graph)::

        sage: F=VectorField(exp(x+y),x**2+y**2).graph(xvalues=(x,-1,1,3),yvalues=(y,-5,5,6))
        sage: len(F.draw_points)
        18
        sage: print F.draw_points[5]
        <Point(-1.0,5.0)>

    If you want a personal list of points, use draw_points ::

        sage: F=VectorField(exp(x+y),x**2+y**2, draw_points=[Point(1,1),Point(5,-23)] )
        sage: print F.draw_points[0]
        <Point(1,1)>
        sage: print F.draw_points[1]
        <Point(5,-23)>

    A vector field with automatic management of the points to be drawn:

    .. literalinclude:: yanntricksChampVecteursDeux.py
    .. image:: Picture_FIGLabelFigChampVecteursDeuxPICTChampVecteursDeux-for_eps.png

    A vector field with given points to be drawn: 

    .. literalinclude:: yanntricksChampVecteur.py
    .. image:: Picture_FIGLabelFigChampVecteursPICTChampVecteurs-for_eps.png


    """
    from yanntricks.src.BasicGeometricObjects import GeometricVectorField
    if xvalues is None and yvalues is None and draw_points is None:
        return GeometricVectorField(fx, fy)
    return GeometricVectorField(fx, fy).graph(xvalues, yvalues, draw_points)


def Vector(A, B=None):
    """
    Return an affine vector from (0,0) to the given point.

    Vector(3,4)
    Vector(P)  # If 'P' is a point
    Vector(t)  # if 't' is a tuple of two numbers
    """
    from yanntricks.src.affine_vector import AffineVector
    from yanntricks.src.point import Point
    O = Point(0, 0)
    if isinstance(A, Point):
        return AffineVector(O, A)
    if isinstance(A, tuple):
        if len(A) != 2:
            raise TypeError(f"You can define a vector from a tuple "
                            f"of length 2, not {len(A)}")
        return AffineVector(O, Point(A[0], A[1]))
    return AffineVector(Point(0, 0), Point(A, B))
