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


from sage.all import lazy_attribute, var

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.Exceptions import ShouldNotHappenException
from yanntricks.src.GenericCurve import GenericCurve


class phyFunctionGraph(GenericCurve, ObjectGraph):
    """
    INPUT:

    - ``fun`` - sage symbolic expression that is to be interpreted as
                a function of `x`.

    - ``mx,Mx`` - the initial and end values of the variable.

    NOTE :

    The end-used has to use :func:`phyFunction` instead. The latter accepts more
    types of arguments.
    """

    def __init__(self, fun, mx, Mx):
        ObjectGraph.__init__(self, fun)
        GenericCurve.__init__(self, mx, Mx)
        self.sage = fun
        x, y = var('x,y')
        self.sage = fun
        try:
            self.sageFast = self.sage._fast_float_(x)
        except (NotImplementedError, TypeError, ValueError, AttributeError):
            # Happens when the derivative of the function is
            # not implemented in Sage
            # Also happens when there is a free variable,
            # as an example
            # F=VectorFieldGraph(x,y)
            # Also when something non analytic is given like a distribution.
            self.sageFast = self.sage
        self.string = repr(self.sage)
        self.fx = self.string.replace("x |--> ", "")
        # self.pstricks = SubstitutionMathPsTricks(self.fx)
        # self.tikz is suppressed on October 16, 2019
        # self.tikz = SubstitutionMathTikz(self.fx)
        self.ListeSurface = []
        self.listeTests = []
        self.TesteDX = 0
        self.listeExtrema = []
        self.listeExtrema_analytique = []
        self.equation = y == self.sage

        self.f = self.obj
        self.mx = mx
        self.Mx = Mx
        self.do_cut_y = False
        self.cut_ymin = None
        self.cut_ymax = None
        self.pieces = []
        # Modification with respect to the attribute in ObjectGraph
        self.parameters.color = "blue"
        self.nul_function = None

        self._derivative = None
        self._parametric_curve = None

    @lazy_attribute
    def I(self):
        if not self.do_cut_y:
            mx = self.mx
        else:
            mx = self.pieces[0].mx
        P = Point(mx, self(mx))
        return P

    @lazy_attribute
    def F(self):
        if not self.do_cut_y:
            Mx = self.Mx
        else:
            Mx = self.pieces[0].Mx
        P = Point(Mx, self(Mx))
        return P

    def parametric_curve(self):
        """
        return a parametric curve with the same graph as `self`.
        """
        from yanntricks.src.Constructors import phyFunction
        if self._parametric_curve:
            return self._parametric_curve
        x = var('x')
        curve = ParametricCurve(phyFunction(x), self, (self.mx, self.Mx))
        curve.parameters = self.parameters.copy()

        curve.linear_plotpoints = self.linear_plotpoints
        curve.curvature_plotpoints = self.curvature_plotpoints
        curve.added_plotpoints = self.added_plotpoints

        curve._representativeParameters = self._representativeParameters
        self._parametric_curve = curve

        return curve

    def visualParametricCurve(self, xunit, yunit):
        return self.parametric_curve().visualParametricCurve(xunit, yunit)

    def inverse(self, y):
        """ returns a list of values x such that f(x)=y """
        from SmallComputations import CalculSage
        listeInverse = []
        x = var('x')
        eq = self.sage(x) == y
        return CalculSage().solve_one_var([eq], x)

    def PointsNiveau(self, y):
        return [Point(x, y) for x in self.inverse(y)]

    def roots(self):
        """ return roots of the function as a list of Points. Some can miss ! """
        return self.PointsNiveau(0)

    def derivative(self, n=1):
        """
        return the derivative of the function. 

        INPUT:

        - ``n`` - an interger (default = 1) the order of derivative. If n=0, return self.

        EXAMPLES::

            sage: from yanntricks import *
            sage: f=phyFunction(x**2)
            sage: print f.derivative()
            x |--> 2*x
            sage: print f.derivative()(3)
            6
            sage: g(x)=cos(x)
            sage: print [g.derivative(i) for i in range(0,5)]
            [x |--> cos(x), x |--> -sin(x), x |--> -cos(x), x |--> sin(x), x |--> cos(x)]
        """
        from yanntricks.src.Constructors import phyFunction
        x = var('x')
        if n == 0:
            try:
                return self.f
            except AttributeError:     # Happens when self is a phyFunction instead of phyFunctionGraph
                return self
        if n == 1:
            if self._derivative == None:
                self._derivative = phyFunction(self.sage.derivative(x))
            return self._derivative
        else:
            return self.derivative(n-1).derivative()

    def get_point(self, x, advised=True):
        return general_function_get_point(self, x, advised)

    def get_normal_vector(self, xx):
        """ 
        return a normalized normal vector to the graph of the function at xx

        The direction of the vector is outside

        INPUT:
        - ``x`` - a number, the position at which we want the normal vector

        OUTPUT:
        a vector

        EXAMPLES:
        sage: from yanntricks import *
        sage: x=var('x')
        sage: f=phyFunction(x**2)
        sage: print f.get_normal_vector(0)
        <vector I=<Point(0,0)> F=<Point(0,-1)>>
        """
        x = var('x')
        F = ParametricCurve(x, self)
        return F.get_normal_vector(xx)

    def get_tangent_vector(self, x, advised=False, numerical=False):
        """
        return a tangent vector at the point (x,f(x))
        """
        ca = self.derivative()(x, numerical=numerical)
        v = Point(1, ca).normalize().origin(self.get_point(x, advised))
        v.in_math_bounding_box = False
        return v

    def get_tangent_segment(self, x):
        """
        Return a tangent segment at point (x,f(x)).

        The difference with self.get_tangent_vector is that self.get_tangent_segment returns a segment that will
        be symmetric. The point (x,f(x)) is the center of self.get_tangent_segment.
        """
        v = self.get_tangent_vector(x)
        mv = -v
        return Segment(mv.F, v.F)

    def tangent_phyFunction(self, x0):
        """
        Return the tangent at the given point as a :class:`phyFunction`.

        INPUT:

        - ``x0`` - a number

        OUTPUT:

        A :class:`phyFunction` that represents the tangent. This is an affine function.

        EXAMPLE::

            sage: from yanntricks import *
            sage: g=phyFunction(cos(x))
            sage: print g.tangent_phyFunction(pi/2)
            x |--> 1/2*pi - x
            sage: g.tangent_phyFunction(pi/2)(1)
            1/2*pi - 1
        """
        from yanntricks.src.Constructors import phyFunction
        x = var('x')
        ca = self.derivative()(x0)
        h0 = self.get_point(x0).y
        return phyFunction(h0+ca*(x-x0))

    def get_normal_point(self, x, dy):
        """ return a point at distance `dy` in the normal direction of the point `(x,f(x))` """
        vecteurNormal = self.get_normal_vector(x)
        return self.get_point(x).translate(vecteurNormal.fix_size(dy))

    def get_regular_points(self, mx, Mx, dx):
        print("Use 'getRegularLengthPoints' instead")
        return self.getRegularLengthPoints(mx, Mx, dx)

    def getRegularLengthPoints(self, mx, Mx, dx):
        """
        return a list of points regularly spaced (with respect to the arc length) on the graph of `self`.

        INPUT:

        - ``mx,Mx`` - the minimal and maximal values of `x` between we will search for points. 
        - ``dx`` - the arc length between two points

        OUTPUT:
        A list of points

        EXAMPLES::

            sage: from yanntricks import *
            sage: f=phyFunction(x+1)
            sage: print [P.coordinates() for P in f.get_regular_points(-2,2,sqrt(2))]  # random

        These are almost the points (-1,0),(0,1), and (1,2).
        """
        Llams = self.getRegularLengthParameters(mx, Mx, dx)
        return [self.get_point(x) for x in Llams]

    @lazy_attribute
    def speed(self):
        return sqrt(1+self.derivative().sage**2)

    def length(self):
        curve = self.parametric_curve()
        return curve.length()

    @lazy_attribute
    def curvature(self):
        return self.parametric_curve().curvature()

    def get_wavy_points(self, mx, Mx, dx, dy):
        curve = self.parametric_curve()
        return curve.get_wavy_points(mx, Mx, dx, dy)

    def get_minmax_data(self, mx, Mx):
        """
        return numerical approximations of min and max of the function on the interval

        INPUT:
        - ``mx,Mx`` - the interval on which we look at the extrema

        OUTPUT:

        dictionary conaining `xmax`, `ymax`, `xmin` and `ymin`

        Notice that we are only interested in ymax and ymin.

        EXAMPLES::

            sage: from yanntricks import *
            sage: f=phyFunction(x)
            sage: f.get_minmax_data(-3,pi)      # random


        In the case of the sine function, the min and max are almost -1 and 1::

            sage: from yanntricks import *
            sage: f=phyFunction(sin(x))
            sage: f.get_minmax_data(0,2*pi)     # random

        NOTE:

        This function is victim of the `Trac 10246 <http://trac.sagemath.org/sage_trac/ticket/10246>` The try/except block is a workaround.

        """

        # If this test never crashes, we could memoize a lot.
        if mx != self.mx or Mx != self.Mx:
            from Exceptions import ShouldNotHappenException
            raise ShouldNotHappenException(
                "I really need to know the minmax on that interval ?")

        minmax = {}
        minmax['xmin'] = mx
        minmax['xmax'] = Mx
        ymin = 1000
        ymax = -1000
        for x in self.representativeParameters():
            valid = True
            try:
                y = self(x)
            except ZeroDivisionError:
                valid = False
            if y.is_infinity():
                valid = False
            if valid:
                ymax = max(ymax, y)
                ymin = min(ymin, y)
        minmax['ymax'] = ymax
        minmax['ymin'] = ymin
        return minmax

    def xmax(self, deb, fin):
        return self.get_minmax_data(deb, fin)['xmax']

    def xmin(self, deb, fin):
        return self.get_minmax_data(deb, fin)['xmin']

    def ymax(self, deb, fin):
        return self.get_minmax_data(deb, fin)['ymax']

    def ymin(self, deb, fin):
        return self.get_minmax_data(deb, fin)['ymin']

    def graph(self, mx, Mx):
        from yanntricks.src.Constructors import phyFunction
        gr = phyFunctionGraph(self.sage, mx, Mx)
        gr.parameters = self.parameters.copy()
        return gr

    def fit_inside(self, xmin, xmax, ymin, ymax):
        k = self.graph(xmin, xmax)
        k.cut_y(ymin, ymax)
        return k

    def surface_under(self, mx=None, Mx=None):
        """
        Return the graph of a surface under the function.

        If mx and Mx are not given, try to use self.mx and self.Mx, assuming that the method is used on
        an instance of phyFunctionGraph that inherits from here.
        """
        if not mx:
            mx = self.mx
        if not Mx:
            Mx = self.Mx
        return SurfaceUnderFunction(self, mx, Mx)

    def cut_y(self, ymin, ymax, plotpoints=None):
        """
        Will not draw the function bellow 'ymin' and over 'ymax'. Will neither join the pieces.

        This is useful when drawing functions like 1/x.

        It is wise to use a value of plotpoints that is not a multiple of the difference Mx-mx. The default behaviour is most of time like that.

        If an other cut_y is already imposed, the most restrictive is used.
        """
        from SmallComputations import split_list
        if self.do_cut_y:
            self.pieces = []
            ymin = max(ymin, self.cut_ymin)
            ymax = min(ymax, self.cut_ymax)
        # Avoid being a multiple of Mx-mx, while being more or less twice the old plotpoints
        self.linear_plotpoints = 2.347*self.linear_plotpoints
        self.do_cut_y = True
        self.cut_ymin = ymin
        self.cut_ymax = ymax
        X = self.representativeParameters()
        s = split_list(X, self.sage, self.cut_ymin, self.cut_ymax)
        for k in s:
            mx = k[0]
            Mx = k[1]
            f = self.graph(mx, Mx)
            self.pieces.append(f)

    def _bounding_box(self, pspict=None):
        if self.do_cut_y and len(self.pieces) > 0:
            # In this case, we will in any case look for the bounding boxes
            # of the pieces.
            # Notice that it can happen that self.do_cut_y=True but
            # that only one piece is found.
            return BoundingBox()
        return self.parametric_curve().bounding_box()

    def mark_point(self, pspict=None):
        if not self.pieces:
            return self.get_point(self.Mx)
        return self.pieces[-1].mark_point()

    def angle(self):
        """ For put_mark.  """
        return AngleMeasure(value_degree=0)

    def representative_graph_object(self):
        """
        Return is the object that will be drawn. It serves to control the chain 
        function --> parametric_curve --> interpolation curve
        """
        return self.parametric_curve()

    def action_on_pspict(self, pspict):
        still_have_to_draw = True
        if self.wavy:
            waviness = self.waviness
            curve = self.parametric_curve()
            curve.parameters = self.parameters.copy()
            curve.wave(self.waviness.dx, self.waviness.dy)
            pspict.DrawGraphs(curve)
            still_have_to_draw = False
        if self.cut_ymin:
            pspict.DrawGraphs(self.pieces)
            still_have_to_draw = False
        if still_have_to_draw:
            gr = self.representative_graph_object()
            pspict.DrawGraphs(gr)
            # TODO : we have to implement y_cut to InterpolationCurve

    def latex_code(self, language=None, pspict=None):
        if not self.wavy and not self.do_cut_y:
            return self.representative_graph_object().latex_code(language=language, pspict=pspict)
        return ""

    def __call__(self, xe, numerical=False):
        """
        return the value of the function at given point

        INPUT:
        - ``xe`` - a number. The point at which we want to evaluate the function
        - ``numerical`` (boolean, default=False) If True, return a numerical_approximation

        EXAMPLES::

            sage: from yanntricks import *
            sage: x=var('x')
            sage: f=phyFunction(cos(x))
            sage: f(1)
            cos(1)
            sage: f(1,numerical=True)
            0.540302305868140
        """
        if numerical:
            return numerical_approx(self.sageFast(xe))
        else:
            try:
                return self.sage(x=xe)
            except TypeError:       # Happens when one has a distribution function
                try:
                    return self.sage(xe)
                except TypeError:
                    print("ooMHAQooMbDokI")
                    print(self, type(self))
                    print(xe, type(xe))
                    raise

    def __pow__(self, n):
        from yanntricks.src.Constructors import phyFunction
        return phyFunction(self.sage**n)

    def __mul__(self, other):
        from yanntricks.src.Constructors import phyFunction
        try:
            f = phyFunction(self.sage*other)
        except TypeError:
            f = phyFunction(self.sage * other.sage)
        return f

    def __rmul__(self, other):
        return self*other

    def __add__(self, other):
        from yanntricks.src.Constructors import phyFunction
        try:
            g = other.sage
        except AttributeError:
            g = other
        return phyFunction(self.sage+g)

    def __sub__(self, other):
        return self+(-other)

    def __neg__(self):
        from yanntricks.src.Constructors import phyFunction
        return phyFunction(-self.sage).graph(self.mx, self.Mx)

    def __str__(self):
        return str(self.sage)


def SubstitutionMathTikz(fx):
    """
    - fx : string that gives a function with 'x'

    We return the same function, but in terms of tikz.
    """
    # One of the big deal is that tikz works with degree instead of radian

    listeSubst = []
    # Notice the parenthesis because \x^2=-1 when \x=-1
    listeSubst.append(["x", "(\\x)"])
    a = fx
    for s in listeSubst:
        a = a.replace(s[0], s[1])
    return a
