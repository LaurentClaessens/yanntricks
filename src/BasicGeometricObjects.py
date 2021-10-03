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

from sage.all import symbolic_expression
from sage.all import lazy_attribute, numerical_approx, var

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.parameters.Parameters import Parameters
from yanntricks.src.point import Point
from yanntricks.src.Utilities import EnsurephyFunction
from yanntricks.src.NoMathUtilities import first_bracket


def genericBracketAttributeToLanguage(attr, language):
    if language == "tikz":
        if attr == "plotpoints":
            return "samples"
        if attr == "linewidth":
            return "line width"
    return attr

# TODO : filling a portion of circle should be as easy as:
#    CerB=Cer.graph(alpha,alpha+90)
#    CerB.parameters.filled()
#    CerB.parameters.fill.color="blue"
# See the picture RouletteACaVVA


def OptionsStyleLigne():
    return ["linecolor", "linestyle"]


class TextGraph(ObjectGraph):
    """
    You can customize the background via the object `self.rectangle`
    """

    def __init__(self, P, text, hide=True):
        from yanntricks.src.Constructors import Mark
        from yanntricks.src.Constructors import Rectangle
        ObjectGraph.__init__(self, self)
        self.P = P
        self.text = text
        self.mark = Mark(self, 0, 0, self.text)
        self.hide = hide

        # This is fake; just to have an object to act on.
        self.rectangle = Rectangle(Point(0, 0), Point(1, 1))
        self.rectangle.parameters.filled()
        self.rectangle.parameters.fill.color = "white"
        self.rectangle.parameters.style = "none"

    def mark_point(self, pspict=None):
        return self.P

    def _math_bounding_box(self, pspict=None):
        # a text has no math_bounding_box because the axes do not want to fit them.
        # return self.mark.math_bounding_box(pspict)         # June 1, 2015
        from yanntricks.src.BoundingBox import BoundingBox
        return BoundingBox()

    def _bounding_box(self, pspict=None):
        return self.mark.bounding_box(pspict)

    def latex_code(self, language=None, pspict=None):
        from yanntricks.src.Constructors import Rectangle
        a = []
        rect = Rectangle(self.mark.bounding_box(pspict))
        rect.parameters = self.rectangle.parameters
        if self.hide:
            a.append(rect.latex_code(language=language, pspict=pspict))
        a.append(self.mark.latex_code(language=language, pspict=pspict))
        return "\n".join(a)


class GeometricVectorField(object):
    """
    Describe a vector field

    INPUT:

    - ``f`` - a tupe of function

    EXAMPLES::


        sage: from yanntricks.BasicGeometricObjects import *
        sage: x,y=var('x,y')
        sage: f1=phyFunction(x**2)
        sage: F = GeometricVectorField( f1,cos(x*y) )
        sage: print F(3,pi/3)
        <vector I=<Point(3,1/3*pi)> F=<Point(12,1/3*pi - 1)>>

    """

    def __init__(self, fx, fy):
        x, y = var('x,y')
        fx = EnsurephyFunction(fx)
        fy = EnsurephyFunction(fy)
        self.fx = symbolic_expression(fx.sage).function(x, y)
        self.fy = symbolic_expression(fy.sage).function(x, y)
        # g=[fx,fy]
        # for i in [0,1]:
        #    if isinstance(g[i],phyFunction):
        #        g[i]=g[i].sage
        # self.fx=g[0]
        # self.fy=g[1]
        self.vector_field = self

    def divergence(self):
        """
        return the divergence of the vector field.

        OUTPUT:

        a two-variable function

        EXAMPLES::

            sage: from yanntricks.BasicGeometricObjects import *
            sage: x,y=var('x,y')
            sage: F = GeometricVectorField( x , y )
            sage: F.divergence()
            (x, y) |--> 2

        The divergence of the gravitational field vanishes::

            sage: G=GeometricVectorField(x/(x**2+y**2),y/(x**2+y**2))
            sage: G.divergence().simplify_full()
            0

        The divergence is a function::

            sage: a,b=var('a,b')
            sage: H=GeometricVectorField( x**2,y**3 )
            sage: H.divergence()(a,b)
            3*b^2 + 2*a

        """
        x, y = var('x,y')
        formula = self.fx.diff(x)+self.fy.diff(y)
        divergence = symbolic_expression(formula).function(x, y)
        return divergence

    def graph(self, xvalues=None, yvalues=None, draw_points=None):
        """
        return a graph of self with the given points

        INPUT:

        - ``xvalues`` - tuple (x,mx,My,n) interval and number of points with respect to X.

        - ``yvalues`` - tuple (y,my,My,n) interval and number of points with respect to Y.

        - ``draw_points`` - (defaulf : empty list) a list of points.

        If xvalues is given, then yvalues has to be given.

        OUTPUT:

        object VectorFieldGraph.

        EXAMPLES::

            sage: from yanntricks.BasicGeometricObjects import *
            sage: x,y=var('x,y')
            sage: F=VectorField(x,y).graph(xvalues=(x,-2,2,3),yvalues=(y,-10,10,3),draw_points=[Point(100,100)])
            sage: print F.draw_points[0]
            <Point(100,100)>
            sage: print len(F.draw_points)
            10
        """
        if draw_points is None:
            draw_points = []
        if xvalues is not None:
            mx = xvalues[1]
            Mx = xvalues[2]
            nx = xvalues[3]
            my = yvalues[1]
            My = yvalues[2]
            ny = yvalues[3]
            from numpy import linspace
            pos_x = linspace(mx, Mx, nx)
            pos_y = linspace(my, numerical_approx(My), ny)
            for xx in pos_x:
                for yy in pos_y:
                    draw_points.append(Point(xx, yy))
        return VectorFieldGraph(self, draw_points=draw_points)

    def __call__(self, a, b=None):
        """
        return the affine vector at point (a,b).

        INPUT:

        - ``a,b`` - numbers.

        OUTPUT:
        an affine vector based on (a,b).

        EXAMPLES::

            sage: from yanntricks import *
            sage: x,y=var('x,y')
            sage: F=VectorField(x**2,y**3)
            sage: print F(1,2)
            <vector I=<Point(1,2)> F=<Point(2,10)>>

            sage: P=Point(3,4)
            sage: print F(P)
            <vector I=<Point(3,4)> F=<Point(12,68)>>

        """
        from yanntricks.src.affine_vector import AffineVector
        if b is not None:
            P = Point(a, b)
        else:
            P = a
        vx = self.fx(x=P.x, y=P.y)
        vy = self.fy(x=P.x, y=P.y)
        return AffineVector(P, Point(P.x+vx, P.y+vy))


class VectorFieldGraph(ObjectGraph, GeometricVectorField):
    """
    the graph object of a vector field

    INPUT:
    - ``F`` - a vector field
    - ``draw_point`` - the list of points on which it has to be drawn

    Typically, in order to construct such an object we use the function
    VectorField
    and then the method
    GeometricVectorField.graph

    See the function VectorField and GeometricVectorField.graph for documentation.
    """

    def __init__(self, F, draw_points):
        ObjectGraph.__init__(self, F)
        GeometricVectorField.__init__(self, F.fx, F.fy)
        self.vector_field = F
        self.F = self.vector_field
        self.draw_points = draw_points

    @lazy_attribute
    def draw_vectors(self):
        """
        the list of vectors to be drawn
        """
        l = []
        return [self(P) for P in self.draw_points]

    @lazy_attribute
    def pos_x(self):
        """
        return the list of x positions on which there is a drawn vector

        The list is sorted

        NOTE:

        If `self` was created using the optional argument `draw_points`,
        then the set of points on which there is a vector
        is not equal to the Cartesian product `self.pos_x` times `self.pos_y`

        EXAMPLES:

        The two lists created in the following example are the same::

            sage: from yanntricks import *
            sage: x,y=var('x,y')
            sage: F=VectorField(x,y).graph(xvalues=(x,1,2,3),yvalues=(y,-2,2,3))
            sage: [ P.coordinates() for P in F.draw_points ]
            ['(1.0,-2.0)', '(1.0,0)', '(1.0,2.0)', '(1.5,-2.0)', '(1.5,0)', '(1.5,2.0)', '(2.0,-2.0)', '(2.0,0)', '(2.0,2.0)']

        and ::

            sage: x,y=var('x,y')
            sage: [ (x,y) for x in F.pos_x for y in F.pos_y ]
            [(1.0, -2.0), (1.0, 0.0), (1.0, 2.0), (1.5, -2.0), (1.5, 0.0), (1.5, 2.0), (2.0, -2.0), (2.0, 0.0), (2.0, 2.0)]


        But in the following, the list is not the list of points::

            sage: x,y=var('x,y')
            sage: G=VectorField(x,y).graph(draw_points=[Point(1,2),Point(3,4)])
            sage: [ (x,y) for x in G.pos_x for y in G.pos_y ]
            [(1, 2), (1, 4), (3, 2), (3, 4)]

        """
        l = []
        for P in self.draw_points:
            if P.x not in l:
                l.append(P.x)
        l.sort()
        return l

    @lazy_attribute
    def pos_y(self):
        """
        return the list of y positions on which there is a drawn vector

        See pos_x
        """
        l = []
        for P in self.draw_points:
            if P.y not in l:
                l.append(P.y)
        l.sort()
        return l

    def _math_bounding_box(self, pspict):
        return self.bounding_box(pspict)

    def _bounding_box(self, pspict=None):
        from yanntricks.src.BoundingBox import BoundingBox
        bb = BoundingBox()
        for v in self.draw_vectors:
            bb.append(v, pspict)
        return bb

    def latex_code(self, language=None, pspict=None):
        code = []
        for v in self.draw_vectors:
            v.parameters = self.parameters.copy()
            code.append(v.latex_code(language=language, pspict=pspict))
        return "\n".join(code)


def draw_to_fill(text):
    r"""
    The tikz code of objects are of the form
     \draw [...] something (...) ;
    Here we have to convert that into
      something [...] (...)
    ex :
    \draw[domain=2:3] plot ( {\x},{\x} );
         -->
     plot [domain=2:3] ( {\x},{\x} )

     There are also interpolations curves whose come like that :
       \draw [...] plot [smooth,tension=1] coordinates {(x1,y2)(x2,y2)}
    """
    t1 = text.replace("\\draw", "").replace(";", "")
    bracket = first_bracket(t1)
    t2 = t1.replace(bracket, "")
    t3 = t2.strip()
    if "coordinates" in t3:
        return t3
    else:
        answer = t3.replace("plot", "plot "+bracket)
    return answer
