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

# copyright (c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu

from numpy import arange
from sage.all import sin, cos, RR

from yanntricks.src.GenericCurve import GenericCurve
from yanntricks.src.Decorators import copy_parameters
from yanntricks.src.ObjectGraph import ObjectGraph

import yanntricks.src.Defaults


class CircleGraph(GenericCurve, ObjectGraph):
    """
    This is a circle, or an arc of circle.

    INPUT:

    - ``center`` - a point, the center of the circle.

    - ``radius`` - a number, the radius of the circle.

    - ``self.angleI`` - (default=0) the beginning angle of the arc (degree).

    - ``self.angleF`` - (default=360) the ending angle of the arc (degree).
    - ``visual`` - (default=False) if 'True', the radius is taken as a 'visual' length.


    OUTPUT:

    A circle ready to be drawn.

    EXAMPLES::

        sage: from yanntricks import *
        sage: circle=Circle(Point(-1,1),3)

    If you want the same circle but between the angles 45 and 78::

        sage: other_circle=circle.graph(45,78)
    """

    def __init__(self, center, radius, angleI=0, angleF=360, visual=False, pspict=None):
        GenericCurve.__init__(self, pI=angleI, pF=angleF)
        self.linear_plotpoints = Defaults.CIRCLE_LINEAR_PLOTPOINTS
        self.center = center
        self.radius = radius
        ObjectGraph.__init__(self, self)
        self.diameter = 2*self.radius
        self._parametric_curve = None
        self.angleI = AngleMeasure(value_degree=angleI, keep_negative=True)
        self.angleF = AngleMeasure(value_degree=angleF, keep_negative=True)
        a = numerical_approx(self.angleI.degree)
        b = numerical_approx(self.angleF.degree)
        self.visual = visual
        self.pspict = pspict
        self._equation = None
        self._numerical_equation = None

    def equation(self, numerical=False):
        """
        Return the equation of `self`.

        OUTPUT:

        an equation.

        EXAMPLES::

            sage: from yanntricks import *
            sage: circle=Circle(Point(0,0),1)
            sage: circle.equation()
            x^2 + y^2 - 1 == 0

        ::

            sage: circle=CircleOA(Point(-1,-1),Point(0,0))
            sage: circle.equation()
            (x + 1)^2 + (y + 1)^2 - 2 == 0

        If 'numerical' is True, return numerical approximations of the coefficients.
        """
        if numerical == True and self._numerical_equation is not None:
            return self._numerical_equation
        if numerical == False and self._equation is not None:
            return self._equation

        x, y = var('x,y')
        if not self.visual:
            cx = self.center.x
            cy = self.center.y
            cr = self.radius
            self._equation = (x-cx)**2+(y-cy)**2-cr**2 == 0
            if not numerical:
                return self._equation
            if numerical:
                cx = numerical_approx(cx)
                cy = numerical_approx(cy)
                cr = numerical_approx(cr)
                self._numerical_equation = (x-cx)**2+(y-cy)**2-cr**2 == 0
                return self._numerical_equation

        Rx = self.radius/self.pspict.xunit
        Ry = self.radius/self.pspict.yunit

        if numerical == False:
            self._equation = (x-self.center.x)**2/Rx**2 + \
                (y-self.center.y)**2/Ry**2-1 == 0
            return self._equation
        if numerical == True:
            Rx = numerical_approximation(Rx)
            Ry = numerical_approximation(Ry)
            cx = numerical_approximation(self.center.x)
            cy = numerical_approximation(self.center.y)
            self._numerical_equation = (x-cx)**2/Rx**2+(y-cy)**2/Ry**2-1 == 0
            return self._numerical_equation

    @copy_parameters
    def parametric_curve(self, a=None, b=None):
        """
        Return the parametric curve associated to the circle.

        If optional arguments <a> and <b> are given, return the corresponding graph between the values a and b of the angle.

        The parameter of the curve is the angle in radian.
        """
        if self._parametric_curve is None:
            x = var('x')
            if self.visual is True:
                if self.pspict is None:
                    from Exceptions import MissingPictureException
                    raise MissingPictureException(
                        "You are trying to draw something with 'visual==True' when not giving a pspict.")
                f1 = phyFunction(self.center.x+self.radius *
                                 cos(x)/self.pspict.xunit)
                f2 = phyFunction(self.center.y+self.radius *
                                 sin(x)/self.pspict.yunit)
            else:
                f1 = phyFunction(self.center.x+self.radius*cos(x))
                f2 = phyFunction(self.center.y+self.radius*sin(x))
            try:
                ai = self.angleI.radian
                af = self.angleF.radian
            except AttributeError:
                ai = self.angleI
                af = self.angleF
            self._parametric_curve = ParametricCurve(f1, f2, (ai, af))
        curve = self._parametric_curve
        # The following is the typical line that is replaced by the decorator
        # 'copy_parameters'
        # curve.parameters=self.parameters.copy()
        if a == None:
            return curve
        else:
            return curve.graph(a, b)

    def put_arrow(self, *arg, **pw):
        self.parametric_curve().put_arrow(*arg, **pw)

    def getPoint(self, theta, advised=True, numerical=False):
        """
        Return a point at angle <theta> (degree) on the circle. 

        INPUT:
        - ``theta`` - the angle given in degree.
        """
        return self.parametric_curve().get_point(radian(theta, numerical=numerical), advised=advised)

    def get_point(self, theta, advised=True, numerical=False):
        return self.getPoint(theta, advised, numerical)

    def get_regular_points(self, mx, Mx, l=None, n=None, advised=True):
        """
        return regularly spaced points on the circle

        INPUT:

        - ``mx`` - initial angle (degree).
        - ``Mx`` - final angle (degree).
        - ``l`` - distance between two points (arc length).
        - ``n`` - number of points
        - ``advised`` - (default=True) if True, compute an advised mark angle for each point
                                        this is CPU-intensive.

        OUTPUT:
        a list of points

        EXAMPLES::

            sage: from yanntricks import *
            sage: C=Circle(Point(0,0),2)
            sage: pts=C.get_regular_points(0,90,1)
            sage: len(pts)
            4

        The points in the previous examples are approximatively :
        ['<Point(2,0)>', '<Point(2*cos(1/2),2*sin(1/2))>', '<Point(2*cos(1),2*sin(1))>', '<Point(2*cos(3/2),2*sin(3/2))>']

        """
        if mx == Mx:
            return [self.get_point(mx)]
        if l is not None:
            Dtheta = (180/pi)*(l/self.radius)
        if n is not None:
            Dtheta = (Mx-mx)/n
        if Dtheta == 0:
            raise ValueError("Dtheta is zero")
        pts = []
        # arange return 'numpy.int32' that cannot be passed into a cosine.
        theta = [RR(x) for x in arange(mx, Mx, step=Dtheta)]
        return [self.get_point(t, advised) for t in theta]

    def get_tangent_vector(self, theta):
        return PolarPoint(1, theta+90).origin(self.get_point(theta, advised=False))

    def get_tangent_segment(self, theta):
        """
        Return a tangent segment at point (x,f(x)).

        The difference with self.get_tangent_vector is that self.get_tangent_segment returns a segment that will
        be symmetric. The point (x,f(x)) is the center of self.get_tangent_segment.
        """
        v = self.get_tangent_vector(theta)
        mv = -v
        return Segment(mv.F, v.F)

    def get_normal_vector(self, theta):
        """
        Return a normal vector at the given angle 

        INPUT:

        - ``theta`` - an angle in degree or :class:`AngleMeasure`.

        OUTPUT:

        An affine vector

        EXAMPLES::

            sage: from yanntricks import *
            sage: C=Circle(Point(0,0),2)
            sage: print C.get_normal_vector(45)
            <vector I=<Point(sqrt(2),sqrt(2))> F=<Point(3/2*sqrt(2),3/2*sqrt(2))>>

        """
        v = PolarPoint(1, theta).origin(self.get_point(theta, advised=False))
        v.arrow_type = "vector"
        return v

    def xmax(self, angleI, angleF):
        return self.get_minmax_data(angleI, angleF)['xmax']

    def xmin(self, angleI, angleF):
        return self.get_minmax_data(angleI, angleF)['xmin']

    def ymax(self, angleI, angleF):
        return self.get_minmax_data(angleI, angleF)['ymax']

    def ymin(self, angleI, angleF):
        return self.get_minmax_data(angleI, angleF)['ymin']

    def graph(self, angleI, angleF):
        """
        Return a graph of the circle between the two angles given in degree
        """
        C = CircleGraph(self.center, self.radius, angleI=angleI,
                        angleF=angleF, visual=self.visual, pspict=self.pspict)
        C.parameters = self.parameters.copy()
        return C

    def __str__(self):
        return "<Circle, center=%s, radius=%s>" % (self.center.__str__(), str(self.radius))

    def copy(self):
        """
        Return a copy of the object as geometrical object.

        It only copies the center and the radius. In particular
        the following are not copied:

        - style of drawing.

        - initial and final angle if `self` is an arc.

        EXAMPLES:

        Python copies by assignation::

            sage: from yanntricks import *
            sage: c1=Circle( Point(1,1),2 )
            sage: c2=c1
            sage: c2.center=Point(3,3)
            sage: print c1.center
            <Point(3,3)>

        The method :func:`copy` pass through::

            sage: c1=Circle( Point(1,1),3 )
            sage: c2=c1.copy()
            sage: c2.center=Point(3,3)
            sage: print c1.center
            <Point(1,1)>

        NOTE:

        Due to use of `lazy_attribute`, it is not recommended to change the center of
        a circle after having defined it.

        """
        return Circle(self.center, self.radius)

    def _math_bounding_box(self, pspict=None):
        return self.bounding_box(pspict)

    def _bounding_box(self, pspict):
        a = simplify_degree(self.angleI, keep_max=True, number=True)
        b = simplify_degree(self.angleF, keep_max=True, number=True)
        if self.angleI < self.angleF:
            angleI = min(a, b)
            angleF = max(a, b)
        else:
            angleI = max(a, b)
            angleF = min(a, b)+360
        pI = self.get_point(angleI)
        pF = self.get_point(angleF)
        bb = BoundingBox(self.center, self.center)
        bb.append(pI, pspict)
        bb.append(pF, pspict)
        if angleI == 0:
            bb.addX(self.center.x+self.radius)
        if angleI < 90 and angleF > 90:
            bb.addY(self.center.y+self.radius)
        if angleI < 180 and angleF > 180:
            bb.addX(self.center.x-self.radius)
        if angleI < 270 and angleF > 270:
            bb.addY(self.center.y-self.radius)
        return bb

    def representative_points(self):
        pp = self.linear_plotpoints
        return self.get_regular_points(mx=degree(self.angleI), Mx=degree(self.angleF), n=pp, advised=False)

    def action_on_pspict(self, pspict):
        alphaI = radian(self.angleI, number=True,
                        keep_max=True, keep_large=True)
        alphaF = radian(self.angleF, number=True,
                        keep_max=True, keep_large=True)

        # self.angleI and self.angleF should be AngleMeasure, but sometimes the user
        #    writes something like
        #   C.angleI=20

        if isinstance(self.angleF, AngleMeasure):
            f = self.angleF.degree
        else:
            f = self.angleF
        if f == 360:        # Because the function radian simplifies modulo 2pi.
            alphaF = 2*pi
        G = self.parametric_curve(alphaI, alphaF)
        G.parameters = self.parameters.copy()
        if self.parameters._filled or self.parameters._hatched:
            custom = CustomSurface([self.parametric_curve(alphaI, alphaF)])
            custom.parameters = self.parameters.copy()
            pspict.DrawGraphs(custom)

        if self.wavy:
            waviness = self.waviness
            G.wave(waviness.dx, waviness.dy)
            pspict.DrawGraphs(G)
        else:
            pspict.DrawGraphs(G)
    # No need of that empty latex_code since it is now default in ObjectGraph (May 14, 2016)
    # def latex_code(self,language=None,pspict=None):
    #    return ""
