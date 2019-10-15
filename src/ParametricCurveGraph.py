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

"""
    ParametricCurveGraph describe a parametric curve of which we know an analytic expression of the components.
"""

from sage.all import lazy_attribute

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.Exceptions import ShouldNotHappenException
from yanntricks.src.GenericCurve import GenericCurve


class ParametricCurveGraph(GenericCurve, ObjectGraph):
    def __init__(self, f1, f2, llamI, llamF):
        """
        Use the constructor :func:`ParametricCurve`.

        INPUT:

        - ``f1,f2`` - two functions.

        - ``llamI,llamF`` - initial and final values of the parameter.

        ATTRIBUTES:

        - ``plotpoints`` - (default=50)  number of points to be computed.
                           If the function seems wrong, increase that number.
                           It can happen with functions like sin(1/x) close to zero:
                            such a function have too fast oscillations.

        """
        if isinstance(f1, ParametricCurveGraph):
            print("You cannot creare a parametric curve by giving a parametric curve")
            raise TypeError
        ObjectGraph.__init__(self, self)
        GenericCurve.__init__(self, llamI, llamF)
        self._derivative_dict = {0: self}
        self.f1 = f1
        self.f2 = f2
        self.curve = self.obj
        self.llamI = llamI
        self.llamF = llamF
        self.mx = llamI
        self.Mx = llamF
        self.parameters.color = "blue"
        self.plotstyle = "curve"
        self.record_arrows = []
        # TODO: if I remove the protection "if self.llamI", sometimes it
        # tries to make self.get_point(self.llamI) with self.llamI==None
        # In that case the crash is interesting since it is a segfault instead of an exception.
        if self.llamI != None:
            self.I = self.get_point(self.llamI, advised=False)
            self.F = self.get_point(self.llamF, advised=False)

    @lazy_attribute
    def speed(self):
        r"""
        return the norm of the speed function.

        That is the function

        EXAMPLES::

            sage: from yanntricks import *
            sage: curve=ParametricCurve(cos(x),sin(2*x))
            sage: print curve.speed
            x |--> sqrt(4*cos(2*x)^2 + sin(x)^2)
        """
        return sqrt(self.f1.derivative().sage**2+self.f2.derivative().sage**2)

    @lazy_attribute
    def curvature(self):
        """
        return the curvature function.
        """
        gp = self.derivative()
        gpp = self.derivative(n=2)

        fp1 = gp.f1.sage
        fp2 = gp.f2.sage

        fpp1 = gpp.f1.sage
        fpp2 = gpp.f2.sage

        mixed = fpp1*fp1+fpp2*fp2
        mixed = mixed.simplify_full()

        num1 = fpp1*self.speed-2*fp1*mixed
        num2 = fpp2*self.speed-2*fp2*mixed
        num1 = num1.simplify_full()
        num2 = num2.simplify_full()

        tau1 = num1/(self.speed**2)
        tau2 = num2/(self.speed**2)
        tau1 = tau1.simplify_full()
        tau2 = tau2.simplify_full()

        c = sqrt(tau1**2+tau2**2)
        return c.full_simplify()

    def visualParametricCurve(self, xunit, yunit):
        Vf1 = phyFunction(self.f1(xunit*x))
        Vf2 = phyFunction(self.f2(yunit*x))
        return ParametricCurve(Vf1, Vf2)

    def tangent_angle(self, llam):
        """"Return the angle of the tangent (radian)"""
        dx = self.f1.derivative()(llam)
        dy = self.f2.derivative()(llam)
        ca = dy/dx
        return atan(ca)

    def derivative(self, n=1):
        """
        Return the parametric curve given by the derivative. (f1,f2) -> (f1',f2').

        INPUT:
        - ``n`` - an integer (default=1).  If the optional parameter `n` is given, give higher order derivatives. If n=0, return self.

        EXAMPLES::

            sage: from yanntricks import *
            sage: x=var('x')
            sage: f1=phyFunction(cos(2*x))
            sage: f2=phyFunction(x*exp(2*x))
            sage: F=ParametricCurve(f1,f2)
            sage: print F.derivative()
            <The parametric curve given by
            x(t)=-2*sin(2*t)
            y(t)=2*t*e^(2*t) + e^(2*t)
            between None and None>
            sage: print F.derivative(3)
            <The parametric curve given by
            x(t)=8*sin(2*t)
            y(t)=8*t*e^(2*t) + 12*e^(2*t)
            between None and None>
        """
        try:
            return self._derivative_dict[n]
        except KeyError:
            pass
        if n == 1:
            self._derivative_dict[1] = ParametricCurve(
                self.f1.derivative(), self.f2.derivative())
        else:
            self._derivative_dict[n] = self.derivative(n-1).derivative()
        return self._derivative_dict[n]

    def put_arrow(self, *args):
        # TODO : one should be able to give the size as optional argument, as done with
        #       put_arrow on SegmentGraph.
        """
        Add a small arrow at the given positions.

        The arrow is a vector of size (by default) 0.01. The set of vectors
        is stored in `self.record_arrows`. Thus they can be customized
        as any vectors.

        EXAMPLES:

        In the following example, notice the way one of the arrow is
        red and backward.

        .. literalinclude:: yanntricksContourGreen.py
        .. image:: Picture_FIGLabelFigContourGreenPICTContourGreen-for_eps.png
        """
        # TODO: in the previous example, if I first change the color
        # and then change the orientation of the arrow, it does not work.
        ll = []
        for a in args:
            try:
                ll.extend(a)
            except TypeError:
                ll.append(a)
        for llam in ll:
            v = self.get_arrow(llam)
            self.record_arrows.append(v)

    def middle_point(self):
        """
        return the middle point of the curve (respect to the arc length)
        """
        l = self.arc_length()

    def get_point(self, llam, advised=True):
        """
        Return the point on the curve for the value llam of the parameter.

        Add the attribute advised_mark_angle which gives the normal
        exterior angle at the given point.
        If you want to put a mark on the point P (obtained by get_point),
        you should consider to write
            P.put_mark(r,P.advised_mark_angle,text)
        The so build angle is somewhat "optimal" for a visual point 
        of view. The attribute self.get_point(llam).advised_mark_angle 
        is given in degree.

        The advised angle is given in degree.

        The optional boolean argument <advised> serves to avoid infinite
        loops because we use get_point in get_normal_vector.
        """
        if isinstance(llam, AngleMeasure):
            llam = llam.radian
        P = Point(self.f1(llam), self.f2(llam))
        if advised:
            P._advised_mark_angle = self.get_normal_vector(llam).angle()
        return P

    def get_tangent_vector(self, llam, advised=False):
        """
        returns the tangent vector to the curve for the value of the parameter given by llam.
           The vector is normed to 1.

        INPUT::

        - ``llam`` - the value of the parameter on which we want the tangent.

        - ``advised`` - (default = False) if True, the initial point is returned with its
                        advised_mark_angle. This takes quite a long time of computation
                        (and creates infinite loops in some circumstances)

        EXAMPLES::

            sage: from yanntricks import *
            sage: F=ParametricCurve(x,x**2)
            sage: print F.get_tangent_vector(0)
            <vector I=<Point(0,0)> F=<Point(1,0)>>
            sage: print F.get_tangent_vector(1)
            <vector I=<Point(1,1)> F=<Point(1/5*sqrt(5) + 1,2/5*sqrt(5) + 1)>>
        """
        initial = self.get_point(llam, advised)
        return AffineVector(initial, Point(initial.x+self.derivative().f1(llam), initial.y+self.derivative().f2(llam))).normalize()

    def get_normal_vector(self, llam, advised=False, normalize=True, Green_convention=False):
        """
        Return the outside normal vector to the curve for the value llam of the parameter.
           The vector is normed to 1.

        An other way to produce normal vector is to use
        self.get_tangent_vector(llam).orthogonal()
        However the latter does not guarantee to produce an outside pointing vector.

        If you want the second derivative vector, use self.get_derivative(2). This will not produce a normal vector in general.

        NOTE:

        The normal vector will be outwards with respect to the *local* curvature only.

        If you have a contour and you need a outward normal vector, you should pass the 
        optional argument `Green_convention=True`. In that case you'll get a vector
        that is a rotation by pi/2 of the tangent vector. In that case, you still have
        to choose by hand if you take N or -N. But this choice is the same for all
        normal vectors of your curve.

        I do not know how could a program guess if N or -N is *globally* outwards. 
        Let me know if you have a trick :)

        EXAMPLES::

            sage: from yanntricks import *
            sage: F=ParametricCurve(sin(x),x**2)
            sage: print F.get_normal_vector(0)
            <vector I=<Point(0,0)> F=<Point(0,-1)>>

        Tangent and outward normal vector fields to a closed path ::

        .. literalinclude:: yanntricksContourTgNDivergence.py
        .. image:: Picture_FIGLabelFigContourTgNDivergencePICTContourTgNDivergence-for_eps.png
        """

        # TODO: give a picture of the same contour, but taking the "local" outward normal vector.

        anchor = self.get_point(llam, advised=False)
        tangent = self.get_tangent_vector(llam)
        N = tangent.orthogonal()
        if Green_convention:
            return N
        # The delicate part is to decide if we want to return N or -N. We select the angle which is on the same side of the curve than the second derivative.  If v is the second derivative, either N or -N has positive inner product with v. We select the one with negative inner product since the second derivative vector is inner.
        second = self.get_second_derivative_vector(llam)
        # If there is an error here, we were returning N before.

        if inner_product(N, second, numerical=True) >= 0:
            v = -N
        else:
            v = N
        return v.fix_origin(anchor)

    # \brief  return the second derivative vector normalised to 1.
    #
    #        \param llam - the value of the parameter on which we want
    #        the second derivative.
    #
    #         \param advised - (default=False) If True,
    #            the initial point is given with
    #                an advised_mark_angle.
    #
    #        \param normalize - (defautl=True) If True, provides a vector
    #                            normalized to 1.
    #                           if False, the norm is not guaranteed
    # and depends on the parametrization.
    #
    # Note : if the parametrization is not normal,
    # this is not orthogonal to the tangent.
    # If you want a normal vector, use `get_normal_vector`.
    def get_second_derivative_vector(self, llam, advised=False, normalize=True):
        initial = self.get_point(llam, advised)
        c = self.get_derivative(llam, 2)
        if normalize:
            try:
                return c.Vector().fix_origin(initial).normalize()
            except ZeroDivisionError:
                print("I cannot normalize a vector of size zero")
                return c.Vector().fix_origin(initial)
        else:
            return c.Vector().fix_origin(initial)

    def get_derivative(self, llam, order=1):
        """
        Return the derivative of the curve. If the curve is f(t),
        return f'(t) or f''(t) or higher derivatives.

        Return a Point, not a vector. This is not normalised.
        """
        return self.derivative(order).get_point(llam, False)

    def get_tangent_segment(self, llam):
        """
        Return a tangent segment of length 2 centred at the given point.
        It is essentially two times get_tangent_vector.
        """
        v = self.get_tangent_vector(llam)
        mv = -v
        return Segment(mv.F, v.F)

    def get_osculating_circle(self, llam):
        """
        Return the osculating circle to the parametric curve.
        """
        P = self.get_point(llam)
        first = self.get_derivative(llam, 1)
        second = self.get_derivative(llam, 2)
        coefficient = (first.x**2+first.y**2) / \
            (first.x*second.y-second.x*first.y)
        Ox = P.x-first.y*coefficient
        Oy = P.y+first.x*coefficient
        center = Point(Ox, Oy)
        return CircleOA(center, P)

    def get_normal_point(self, x, dy):
        vecteurNormal = self.get_normal_vector(x)
        return self.get_point(x).translate(self.get_normal_vector.normalize(dy))

    def length(self, mll=None, Mll=None):
        """
        numerically returns the arc length on the curve between
        two bounds of the parameters.

        If no parameters are given, return the total length.

        INPUT:

        - ``mll,Mll`` - the minimal and maximal values of the parameters

        OUTPUT:
        a number.

        EXAMPLES:

        The length of the circle of radius `sqrt(2)` in the first quadrant.
        We check that we get the correct result up to 0.01::

            sage: from yanntricks import *
            sage: curve=ParametricCurve(x,sqrt(2-x**2))
            sage: bool( abs(pi*sqrt(2)/2) - curve.length(0,sqrt(2)) <0.01) 
            True

        """
        if mll == None:
            mll = self.llamI
        if Mll == None:
            Mll = self.llamF
        return numerical_integral(self.speed, mll, Mll)[0]

    def arc_length(self, mll=None, Mll=None):
        print("You should use 'length' instead.")
        return self.length(mll=mll, Mll=Mll)

    def get_regular_points(self, mll, Mll, dl):
        """
        Return a list of points regularly spaced (with respect to the arc length)
        by dl. 

        - 'mll' is the initial value of the parameter  
        - 'Mll' is the end value of the parameter.

        In some applications, you prefer to use 
        ParametricCurve.getRegularLengthParameter. 
        The latter method returns the list of values of the parameter instead
        of the list of points. This is what you need if you want to draw 
        tangent vectors for example.
        """
        return [self.get_point(ll) for ll in self.getRegularLengthParameters(mll, Mll, dl)]

    def get_wavy_points(self, mll, Mll, dl, dy, xunit=1, yunit=1):
        """
        Return a list of points which do a wave around the parametric curve.
        """
        PAs = self.getRegularLengthParameters(
            mll, Mll, dl, xunit=xunit, yunit=yunit)
        PTs = [self.get_point(mll)]
        for i in range(0, len(PAs)):
            llam = float(PAs[i])
            v = self.get_normal_vector(llam)
            vp = v.F-v.I
            w = Vector(vp.x*yunit/xunit, vp.y*xunit /
                       yunit).fix_visual_size(dy, xunit, yunit)
            PTs.append(self.get_point(llam).translate(w*(-1)**i))
        PTs.append(self.get_point(Mll))
        return PTs

    def rotate(self, theta):
        """
        Return a new ParametricCurve which graph is rotated by <theta> with respect to self.

        theta is given in degree.
        """
        alpha = radian(theta)
        g1 = cos(alpha)*self.f1+sin(alpha)*self.f2
        g2 = -sin(alpha)*self.f1+cos(alpha)*self.f2
        return ParametricCurve(g1, g2)

    def graph(self, mx, Mx):
        gr = ParametricCurve(self.f1, self.f2, (mx, Mx))
        gr.parameters = self.parameters.copy()
        return gr

    def __call__(self, llam, approx=False):
        return self.get_point(llam, approx)

    def __str__(self):
        t = var('t')
        a = []
        a.append("<The parametric curve given by")
        a.append("x(t)=%s" % repr(self.f1.sage(x=t)))
        a.append("y(t)=%s" % repr(self.f2.sage(x=t)))
        a.append("between {} and {}>".format(self.mx, self.Mx))
        return "\n".join(a)

    def reverse(self):
        """
        return the curve in the inverse sense but on the same interval

        EXAMPLE::

        sage: from yanntricks import *
        sage: x=var('x')
        sage: curve=ParametricCurve(cos(x),sin(x)).graph(0,2*pi).reverse()
        sage: print curve
        <The parametric curve given by
        x(t)=cos(2*pi - t)
        y(t)=sin(2*pi - t)
        between 0 and 2*pi>
        """
        x = var('x')
        a = self.llamI
        b = self.llamF
        f1 = self.f1.sage(x=b-(x-a))
        f2 = self.f2.sage(x=b-(x-a))
        curve = ParametricCurve(f1, f2).graph(a, b)
        curve.f1.nul_function = self.f1.nul_function
        curve.f2.nul_function = self.f2.nul_function

        return curve

    def _bounding_box(self, pspict=None):
        xmin = self.xmin(self.llamI, self.llamF)
        xmax = self.xmax(self.llamI, self.llamF)
        ymin = self.ymin(self.llamI, self.llamF)
        ymax = self.ymax(self.llamI, self.llamF)
        bb = BoundingBox(Point(xmin, ymin), Point(xmax, ymax))
        return bb

    def action_on_pspict(self, pspict):
        if self.wavy:
            waviness = self.waviness
            interpolation = InterpolationCurve(self.curve.get_wavy_points(
                self.llamI, self.llamF, waviness.dx, waviness.dy, xunit=pspict.xunit, yunit=pspict.yunit), context_object=self)
            interpolation.parameters = self.parameters.copy()

            pspict.DrawGraphs(interpolation)
        else:
            points_list = self.representative_points()
            curve = InterpolationCurve(points_list)
            curve.parameters = self.parameters.copy()
            curve.mode = "trivial"
            pspict.DrawGraphs(curve)
        for v in self.record_arrows:
            pspict.DrawGraphs(v)
