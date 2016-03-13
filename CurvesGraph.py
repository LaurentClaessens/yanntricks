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

# copyright (c) Laurent Claessens, 2010-2016
# email: moky.math@gmai.com

from __future__ import division

from ObjectGraph import ObjectGraph
from Constructors import *
from Utilities import *
from SmallComputations import MyMinMax as MyMinMax
from Exceptions import ShouldNotHappenException

class phyFunctionGraph(ObjectGraph):
    """
    INPUT:

    - ``fun`` - sage symbolic expression that is to be interpreted as
                a function of `x`.

    - ``mx,Mx`` - the initial and end values of the variable.

    NOTE :

    The end-used has to use :func:`phyFunction` instead. The latter accepts more
    types of arguments.
    """
    def __init__(self,fun,mx,Mx):
        ObjectGraph.__init__(self,fun)
        self.sage=fun
        x,y=var('x,y')
        self.sage=fun
        try :
            self.sageFast = self.sage._fast_float_(x)
        except (NotImplementedError,TypeError,ValueError,AttributeError) : 
            # Happens when the derivative of the function is not implemented in Sage
            # Also happens when there is a free variable,
            # as an example
            # F=VectorFieldGraph(x,y)
            # Also when something non analytic is given like a distribution.
            self.sageFast = self.sage
        self.string = repr(self.sage)
        self.fx = self.string.replace("x |--> ","")
        #self.pstricks = SubstitutionMathPsTricks(self.fx)
        self.tikz = SubstitutionMathTikz(self.fx)
        self.ListeSurface = []
        self.listeTests = []
        self.TesteDX = 0
        self.listeExtrema = []
        self.listeExtrema_analytique = []
        self._derivative = None
        self.equation=y==self.sage

        self.f = self.obj
        self.mx = mx
        self.Mx = Mx
        self.do_cut_y=False
        self.cut_ymin=None
        self.cut_ymax=None
        self.parameters.plotpoints = 100                   # We draw 100 points as default.
        self.pieces=[]      
        self.parameters.color = "blue"              # Modification with respect to the attribute in ObjectGraph
        self.nul_function=None
    @lazy_attribute
    def I(self):
        if not self.do_cut_y:
            mx=self.mx
        else :
            mx=self.pieces[0].mx
        P=Point(mx,self(mx))
        return P
    @lazy_attribute
    def F(self):
        if not self.do_cut_y:
            Mx=self.Mx
        else :
            Mx=self.pieces[0].Mx
        P = Point(Mx,self(Mx))
        return P
    def parametric_curve(self):
        """
        return a parametric curve with the same graph as `self`.
        """
        x=var('x')
        curve = ParametricCurve(phyFunction(x),self,(self.mx,self.Mx))
        curve.parameters=self.parameters.copy()
        return curve
    def inverse(self,y):
        """ returns a list of values x such that f(x)=y """
        listeInverse = []
        x=var('x')
        eq = self.sage(x) == y
        from SmallComputations import CalculSage
        return CalculSage().solve_one_var([eq],x)
    def PointsNiveau(self,y):
        return [ Point(x,y) for x in self.inverse(y) ]
    def roots(self):
        """ return roots of the function as a list of Points. Some can miss ! """
        return self.PointsNiveau(0)
    def derivative(self,n=1):
        """
        return the derivative of the function. 

        INPUT:

        - ``n`` - an interger (default = 1) the order of derivative. If n=0, return self.

        EXAMPLES::

            sage: from phystricks import *
            sage: f=phyFunction(x**2)
            sage: print f.derivative()
            x |--> 2*x
            sage: print f.derivative()(3)
            6
            sage: g(x)=cos(x)
            sage: print [g.derivative(i) for i in range(0,5)]
            [x |--> cos(x), x |--> -sin(x), x |--> -cos(x), x |--> sin(x), x |--> cos(x)]
        """
        x=var('x')
        if n==0 :
            try :
                return self.f
            except AttributeError :     # Happens when self is a phyFunction instead of phyFunctionGraph
                return self
        if n==1:
            if self._derivative == None :
                self._derivative = phyFunction(self.sage.derivative(x))
            return self._derivative
        else:
            return self.derivative(n-1).derivative()
    def get_point(self,x,advised=True):        
        return general_function_get_point(self,x,advised)
    def get_normal_vector(self,xx):
        """ 
        return a normalized normal vector to the graph of the function at xx

        The direction of the vector is outside

        INPUT:
        - ``x`` - a number, the position at which we want the normal vector

        OUTPUT:
        a vector

        EXAMPLES:
        sage: from phystricks import *
        sage: x=var('x')
        sage: f=phyFunction(x**2)
        sage: print f.get_normal_vector(0)
        <vector I=<Point(0,0)> F=<Point(0,-1)>>
        """
        x=var('x')
        F=ParametricCurve(x,self)
        return F.get_normal_vector(xx)
    def get_tangent_vector(self,x,advised=False,numerical=False):
        """
        return a tangent vector at the point (x,f(x))
        """
        ca = self.derivative()(x,numerical=numerical)
        v = Point(1,ca).normalize().origin(self.get_point(x,advised))
        v.in_math_bounding_box = False
        return v
    def get_tangent_segment(self,x):
        """
        Return a tangent segment at point (x,f(x)).
        
        The difference with self.get_tangent_vector is that self.get_tangent_segment returns a segment that will
        be symmetric. The point (x,f(x)) is the center of self.get_tangent_segment.
        """
        v=self.get_tangent_vector(x)
        mv=-v
        return Segment(mv.F,v.F)
    def tangent_phyFunction(self,x0):
        """
        Return the tangent at the given point as a :class:`phyFunction`.

        INPUT:

        - ``x0`` - a number

        OUTPUT:

        A :class:`phyFunction` that represents the tangent. This is an affine function.

        EXAMPLE::

            sage: from phystricks import *
            sage: g=phyFunction(cos(x))
            sage: print g.tangent_phyFunction(pi/2)
            x |--> 1/2*pi - x
            sage: g.tangent_phyFunction(pi/2)(1)
            1/2*pi - 1
        """
        x=var('x')
        ca=self.derivative()(x0)
        h0=self.get_point(x0).y
        return phyFunction(h0+ca*(x-x0))
    def get_normal_point(self,x,dy):
        """ return a point at distance `dy` in the normal direction of the point `(x,f(x))` """
        vecteurNormal =  self.get_normal_vector(x)
        return self.get_point(x).translate(vecteurNormal.fix_size(dy))
    def get_regular_points(self,mx,Mx,dx):
        """
        return a list of points regularly spaced (with respect to the arc length) on the graph of `self`.

        INPUT:

        - ``mx,Mx`` - the minimal and maximal values of `x` between we will search for points. 
        - ``dx`` - the arc length between two points

        OUTPUT:
        A list of points
            
        EXAMPLES::
        
            sage: from phystricks import *
            sage: f=phyFunction(x+1)
            sage: print [P.coordinates() for P in f.get_regular_points(-2,2,sqrt(2))]  # random

        These are almost the points (-1,0),(0,1), and (1,2).

        """
        curve = self.parametric_curve()
        return curve.get_regular_points(mx,Mx,dx)
    def length(self):
        curve = self.parametric_curve()
        return curve.length()
    def representative_points(self):
        dx=self.length()/self.parameters.plotpoints
        return self.get_regular_points(self.mx,self.Mx,dx)
    def get_wavy_points(self,mx,Mx,dx,dy):
        print("SKBooMaOvCE")
        curve=self.parametric_curve()
        return curve.get_wavy_points(mx,Mx,dx,dy)

    def get_minmax_data(self,mx,Mx):
        """
        return numerical approximations of min and max of the function on the interval

        INPUT:
        - ``mx,Mx`` - the interval on which we look at the extrema

        OUTPUT:

        dictionary conaining `xmax`, `ymax`, `xmin` and `ymin`

        Notice that we are only interested in ymax and ymin.

        EXAMPLES::
        
            sage: from phystricks import *
            sage: f=phyFunction(x)
            sage: f.get_minmax_data(-3,pi)      # random


        In the case of the sine function, the min and max are almost -1 and 1::

            sage: from phystricks import *
            sage: f=phyFunction(sin(x))
            sage: f.get_minmax_data(0,2*pi)     # random

        NOTE:

        This function is victim of the `Trac 10246 <http://trac.sagemath.org/sage_trac/ticket/10246>` The try/except
        block is a workaround.

        """
        minmax={}
        minmax['xmin']=mx
        minmax['xmax']=Mx
        ymin=1000
        ymax=-1000
        for x in self.plotpoints_list(xmin=mx,xmax=Mx,plotpoints=self.parameters.plotpoints):
            valid=True
            try :
                y=self(x)
            except ZeroDivisionError :
                valid=False
            try :
                if y.is_infinity():
                    valid=False
            except AttributeError :
                pass            # When drawing non-analytic function, y is numpy.float64
            if valid :
                ymax=max(ymax,y)
                ymin=min(ymin,y)
        minmax['ymax']=ymax
        minmax['ymin']=ymin
        return minmax
    def xmax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmax']
    def xmin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmin']
    def ymax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymax']
    def ymin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymin']
    def graph(self,mx,Mx):
        gr = phyFunctionGraph(self.sage,mx,Mx)
        gr.parameters=self.parameters.copy()
        return gr
    def fit_inside(self,xmin,xmax,ymin,ymax):
        k=self.graph(xmin,xmax)
        k.cut_y(ymin,ymax)
        return k
    def surface_under(self,mx=None,Mx=None):
        """
        Return the graph of a surface under the function.

        If mx and Mx are not given, try to use self.mx and self.Mx, assuming that the method is used on
        an instance of phyFunctionGraph that inherits from here.
        """
        if not mx :
            mx=self.mx
        if not Mx :
            Mx=self.Mx
        return SurfaceUnderFunction(self,mx,Mx)
    def add_plotpoint(self,x):
        """
        This point will be added to the list of points to be computed.
        """
        self.parameters.added_plotpoints.append(x)
    def plotpoints_list(self,xmin=None,xmax=None,plotpoints=None):
        import numpy
        if not plotpoints:
            plotpoints=self.parameters.plotpoints
        if xmin==None:
            xmin=self.mx
        if xmax==None:
            xmax=self.Mx
        # Sometimes, xmin and xmax have some Sage's types that numpy does not
        # understand
        xmin=numerical_approx(xmin)
        xmax=numerical_approx(xmax)
        X=list(numpy.linspace(xmin,xmax,plotpoints))
        X.extend(self.parameters.added_plotpoints)
        X.sort()
        return X
    def cut_y(self,ymin,ymax,plotpoints=None):
        """
        Will not draw the function bellow 'ymin' and over 'ymax'. Will neither join the pieces.

        This is useful when drawing functions like 1/x.

        It is wise to use a value of plotpoints that is not a multiple of the difference Mx-mx. The default behaviour is most of time like that.

        If an other cut_y is already imposed, the most restrictive is used.
        """
        from SmallComputations import split_list
        if self.do_cut_y:
            self.pieces=[]
            ymin=max(ymin,self.cut_ymin)
            ymax=min(ymax,self.cut_ymax)
        if not plotpoints:
            plotpoints=2.347*self.parameters.plotpoints             # Avoid being a multiple of Mx-mx, while being more or less twice the old plotpoints
        self.do_cut_y=True
        self.cut_ymin=ymin
        self.cut_ymax=ymax
        X=self.plotpoints_list(plotpoints=plotpoints)
        s=split_list(X,self.sage,self.cut_ymin,self.cut_ymax)
        for k in s:
            mx=k[0]
            Mx=k[1]
            f=self.graph(mx,Mx)
            self.pieces.append(f)
    def bounding_box(self,pspict=None):
        bb = BoundingBox()
        if self.do_cut_y and len(self.pieces)>0:
            # In this case, we will in any case look for the bounding boxes of the pieces.
            # Notice that it can happen that self.do_cut_y=True but that only one piece is found.
            return bb
        bb.addY(self.ymin(self.mx,self.Mx))
        bb.addY(self.ymax(self.mx,self.Mx))
        bb.addX(self.mx)
        bb.addX(self.Mx)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def mark_point(self,pspict=None):
        if not self.pieces:
            return self.get_point(self.Mx)
        return self.pieces[-1].mark_point()
    def angle(self):
        """ For put_mark.  """
        return AngleMeasure(value_degree=0)
    def representative_graph_object(self):
        """
        Return is the object that will be drawn. It serves to control the chain function --> parametric_curve --> interpolation curve
        """
        deb = numerical_approx(self.mx) 
        fin = numerical_approx(self.Mx)
        curve=self.parametric_curve().graph(deb,fin)
        curve.parameters=self.parameters.copy()
        return curve
    def action_on_pspict(self,pspict):
        still_have_to_draw=True
        if self.marque :
            P = self.mark_point()
            P.parameters.symbol=""
            P.marque = True
            P.mark = self.mark
            pspict.DrawGraph(P)
        if self.wavy :          
            waviness = self.waviness
            curve=self.parametric_curve()
            curve.parameters=self.parameters.copy()
            curve.wave(self.waviness.dx,self.waviness.dy)
            pspict.DrawGraph(curve)
            still_have_to_draw=False
        if self.cut_ymin:
            pspict.DrawGraphs( self.pieces  )
            still_have_to_draw=False
        if still_have_to_draw :
            gr=self.representative_graph_object()
            pspict.DrawGraph(gr)
            #TODO : we have to implement y_cut to InterpolationCurve
    def pstricks_code(self,pspict=None):
        raise DeprecationWarning   # June 24 2014
        if not self.wavy and not self.do_cut_y:
            # The use of numerical_approx is intended to avoid strings like "2*pi" in the final pstricks code.
            deb = numerical_approx(self.mx) 
            fin = numerical_approx(self.Mx)
            return "\psplot["+self.params()+"]{"+str(deb)+"}{"+str(fin)+"}{"+self.pstricks+"}"
        return ""
    def latex_code(self,language=None,pspict=None):
        if not self.wavy and not self.do_cut_y:
            return self.representative_graph_object().latex_code(language=language,pspict=pspict)
        return ""
    def __call__(self,xe,numerical=False):
        """
        return the value of the function at given point

        INPUT:
        - ``xe`` - a number. The point at which we want to evaluate the function
        - ``numerical`` (boolean, default=False) If True, return a numerical_approximation

        EXAMPLES::

            sage: from phystricks import *
            sage: x=var('x')
            sage: f=phyFunction(cos(x))
            sage: f(1)
            cos(1)
            sage: f(1,numerical=True)
            0.540302305868140
        """
        if numerical :
            return numerical_approx(self.sageFast(xe))
        else :
            try :
                return self.sage(x=xe)
            except TypeError:       # Happens when one has a distribution function
                return self.sage(xe)
    def __pow__(self,n):
        return phyFunction(self.sage**n)
    def __mul__(self,other):
        try :
            f=phyFunction(self.sage*other)
        except TypeError :
            f=phyFunction(self.sage * other.sage)
        return f
    def __rmul__(self,other):
        return self*other
    def __add__(self,other):
        try :
            g=other.sage
        except AttributeError:
            g=other
        return phyFunction(self.sage+g)
    def __sub__(self,other):
        return self+(-other)
    def __neg__(self):
        return phyFunction(-self.sage).graph(self.mx,self.Mx)
    def __str__(self):
        return str(self.sage)

def SubstitutionMathTikz(fx):
    """
    - fx : string that gives a function with 'x'

    We return the same function, but in terms of tikz.
    """
    # One of the big deal is that tikz works with degree instead of radian

    listeSubst = []
    listeSubst.append(["x","(\\x)"])        # Notice the parenthesis because \x^2=-1 when \x=-1
    a = fx
    for s in listeSubst :
        a = a.replace(s[0],s[1])
    return a


class ParametricCurveGraph(ObjectGraph):
    def __init__(self,f1,f2,llamI,llamF):
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
        if isinstance(f1,ParametricCurveGraph):
            print("You cannot creare a parametric curve by giving a parametric curve")
            raise TypeError
        ObjectGraph.__init__(self,self)
        self._derivative_dict={0:self}
        self.f1=f1
        self.f2=f2
        self.curve = self.obj
        self.llamI = llamI
        self.llamF = llamF
        self.mx = llamI
        self.Mx = llamF
        self.parameters.color = "blue"
        self.plotstyle = "curve"
        self.parameters.plotpoints = None
        self.record_arrows=[]
        self.parameters.force_smoothing=False       # plot with regularly spaced points. In this case self.parameters.plotpoints will not be exact.
        #TODO: if I remove the protection "if self.llamI", sometimes it 
        # tries to make self.get_point(self.llamI) with self.llamI==None
        # In that case the crash is interesting since it is a segfault instead of an exception.
        if self.llamI != None:
            self.I=self.get_point(self.llamI,advised=False)   
            self.F=self.get_point(self.llamF,advised=False)
    def pstricks(self,pspict=None):
        # One difficult point with pstrics is that the syntax is "f1(t) | f2(t)" with the variable t.
        #   In order to produce that, we use the Sage's function repr and the syntax f(x=t)
        raise DeprecationWarning
        t=var('t')
        return "%s | %s "%(SubstitutionMathPsTricks(repr(self.f1.sage(x=t)).replace("pi","3.1415")),  SubstitutionMathPsTricks(repr(self.f2.sage(x=t)).replace("pi","3.1415")) )
    @lazy_attribute
    def speed(self):
        r"""
        return the norm of the speed function.

        That is the function

        EXAMPLES::

            sage: from phystricks import *
            sage: curve=ParametricCurve(cos(x),sin(2*x))
            sage: print curve.speed
            x |--> sqrt(4*cos(2*x)^2 + sin(x)^2)
        """
        return sqrt( self.f1.derivative().sage**2+self.f2.derivative().sage**2 )
    def tangent_angle(self,llam):
        """"Return the angle of the tangent (radian)"""
        dx=self.f1.derivative()(llam)
        dy=self.f2.derivative()(llam)
        ca=dy/dx
        return atan(ca)
    def derivative(self,n=1):
        """
        Return the parametric curve given by the derivative. (f1,f2) -> (f1',f2').

        INPUT:
        - ``n`` - an integer (default=1).  If the optional parameter `n` is given, give higher order derivatives. If n=0, return self.

        EXAMPLES::
        
            sage: from phystricks import *
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
        try :
            return self._derivative_dict[n]
        except KeyError :
            pass
        if n==1:
            self._derivative_dict[1] = ParametricCurve(self.f1.derivative(),self.f2.derivative())
        else:
            self._derivative_dict[n] = self.derivative(n-1).derivative()
        return self._derivative_dict[n]
    def put_arrow(self,*args):
        # TODO : one should be able to give the size as optional argument, as done with
        #       put_arrow on SegmentGraph. 
        """
        Add a small arrow at the given positions.

        The arrow is a vector of size (by default 0.01). The set of vectors
        is stored in `self.record_arrows`. Thus they can be customized
        as any vectors.

        EXAMPLES:

        In the following example, notice the way one of the arrow is
        red and backward.

        .. literalinclude:: phystricksContourGreen.py
        .. image:: Picture_FIGLabelFigContourGreenPICTContourGreen-for_eps.png
        """
        # TODO: in the previous example, if I first change the color
        # and then change the orientation of the arrow, it does not work.
        ll=[]
        for a in args:
            try:
                ll.extend(a)
            except TypeError:
                ll.append(a)
        for llam in ll:
            v=self.get_tangent_vector(llam).fix_size(0.01)
            self.record_arrows.append(v)
    def middle_point(self):
        """
        return the middle point of the curve (respect to the arc length)
        """
        l=self.arc_length()
    def get_point(self,llam,advised=True):
        """
        Return the point on the curve for the value llam of the parameter.
        
        Add the attribute advised_mark_angle which gives the normal exterior angle at the given point.
        If you want to put a mark on the point P (obtained by get_point), you should consider to write
        P.put_mark(r,P.advised_mark_angle,text)
        The so build angle is somewhat "optimal" for a visual point of view. The attribute self.get_point(llam).advised_mark_angle is given in degree.

        The advised angle is given in degree.

        The optional boolean argument <advised> serves to avoid infinite loops because we use get_point in get_normal_vector.
        """
        if isinstance(llam,AngleMeasure):
            llam=llam.radian
        P = Point(self.f1(llam),self.f2(llam))
        if advised :
            try :
                P._advised_mark_angle=self.get_normal_vector(llam).angle()
            except TypeError :
                print "It seems that something got wrong somewhere in the computation of the advised mark angle. Return 0 as angle."
                P._advised_mark_angle=0
        return P
    def get_tangent_vector(self,llam,advised=False):
        """
        returns the tangent vector to the curve for the value of the parameter given by llam.
           The vector is normed to 1.

        INPUT::

        - ``llam`` - the value of the parameter on which we want the tangent.

        - ``advised`` - (default = False) if True, the initial point is returned with its
                        advised_mark_angle. This takes quite a long time of computation
                        (and creates infinite loops in some circumstances)

        EXAMPLES::

            sage: from phystricks import *
            sage: F=ParametricCurve(x,x**2)
            sage: print F.get_tangent_vector(0)
            <vector I=<Point(0,0)> F=<Point(1,0)>>
            sage: print F.get_tangent_vector(1)
            <vector I=<Point(1,1)> F=<Point(1/5*sqrt(5) + 1,2/5*sqrt(5) + 1)>>
        """
        initial = self.get_point(llam,advised)     
        return AffineVector( initial,Point(initial.x+self.derivative().f1(llam),initial.y+self.derivative().f2(llam)) ).normalize()
    def get_normal_vector(self,llam,advised=False,normalize=True,Green_convention=False):
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

            sage: from phystricks import *
            sage: F=ParametricCurve(sin(x),x**2)
            sage: print F.get_normal_vector(0)
            <vector I=<Point(0,0)> F=<Point(0,-1)>>

        Tangent and outward normal vector fields to a closed path ::

        .. literalinclude:: phystricksContourTgNDivergence.py
        .. image:: Picture_FIGLabelFigContourTgNDivergencePICTContourTgNDivergence-for_eps.png
        """

        # TODO: give a picture of the same contour, but taking the "local" outward normal vector.

        anchor=self.get_point(llam,advised=False)
        tangent=self.get_tangent_vector(llam)
        N = AffineVector(tangent.orthogonal())
        if Green_convention :
            return N
        # The delicate part is to decide if we want to return N or -N. We select the angle which is on the same side of the curve than the second derivative.  If v is the second derivative, either N or -N has positive inner product with v. We select the one with negative inner product since the second derivative vector is inner.
        try :
            second=self.get_second_derivative_vector(llam)
        except :
            print "Something got wrong with the computation of the second derivative. I return the default normal vector. The latter could not be outwards."
            return N
        if inner_product(N,second) >= 0:
            v=-N
        else :
            v=N
        return AffineVector(v.origin(anchor))
    def get_second_derivative_vector(self,llam,advised=False,normalize=True):
        r"""
        return the second derivative vector normalised to 1.

        INPUT:

        - ``llam`` - the value of the parameter on which we want the second derivative.

        - ``advised`` - (default=False) If True, the initial point is given with
                                            an advised_mark_angle.

        - ``normalize`` - (defautl=True) If True, provides a vector normalized to 1.
                                            if False, the norm is not guaranteed and depend on the 
                                            parametrization..

        EXAMPLES::

            sage: from phystricks import *
            sage: F=ParametricCurve(x,x**3)

        Normalizing a null vector produces a warning::

            sage: print F.get_second_derivative_vector(0,normalize=True)
            <vector I=<Point(0,0)> F=<Point(0,0)>>

        ::

            sage: print F.get_second_derivative_vector(0,normalize=False)
            <vector I=<Point(0,0)> F=<Point(0,0)>>
            sage: print F.get_second_derivative_vector(1)
            <vector I=<Point(1,1)> F=<Point(1,2)>>

        Note : if the parametrization is not normal, this is not orthogonal to the tangent.
        If you want a normal vector, use self.get_normal_vector
        """
        initial=self.get_point(llam,advised)
        c=self.get_derivative(llam,2)
        if normalize :
            try:
                return c.Vector().origin(initial).normalize()
            except ZeroDivisionError :
                print "I cannot normalize a vector of size zero"
                return c.Vector().origin(initial)
        else :
            return c.Vector().origin(initial)
    def get_derivative(self,llam,order=1):
        """
        Return the derivative of the curve. If the curve is f(t), return f'(t) or f''(t) or higher derivatives.

        Return a Point, not a vector. This is not normalised.
        """
        return self.derivative(order).get_point(llam,False)
    def get_tangent_segment(self,llam):
        """
        Return a tangent segment of length 2 centred at the given point. It is essentially two times get_tangent_vector.
        """
        v=self.get_tangent_vector(llam)
        mv=-v
        return Segment(mv.F,v.F)
    def get_osculating_circle(self,llam):
        """
        Return the osculating circle to the parametric curve.
        """
        P=self.get_point(llam)
        first=self.get_derivative(llam,1)
        second=self.get_derivative(llam,2)
        coefficient = (first.x**2+first.y**2)/(first.x*second.y-second.x*first.y)
        Ox=P.x-first.y*coefficient
        Oy=P.y+first.x*coefficient
        center=Point(Ox,Oy)
        return CircleOA(center,P)
    def get_minmax_data(self,deb,fin,decimals=3):
        """
        Return the get_minmax_data from Sage.

        INPUT:

        - ``deb,fin`` - interval on which we are considering the function.
        - ``decimals`` - (default=3) the number of decimals

        OUTPUT:

        A dictionary

        EXAMPLES::

            sage: from phystricks import *
            sage: f=1.5*(1+cos(x))
            sage: cardioid=PolarCurve(f)
            sage: cardioid.get_minmax_data(0,2*pi)
            {'xmax': 3.0, 'xmin': -0.375, 'ymax': 1.948, 'ymin': -1.948}

        NOTE:

        Cutting to 3 decimals is a way to get more reproducible results. 
        It turns out the Sage's get_minmax_data produce unpredictable figures.

        """
        if deb==None:
            raise
        d = MyMinMax(parametric_plot( (self.f1.sage,self.f2.sage), (deb,fin) ).get_minmax_data(),decimals=decimals)
        # for the curve (x,0), Sage gives a bounding box ymin=-1,ymax=1.
        # In order to avoid that problem, when the surface under a function is created, the second curve (the one of y=0) is given the attribute nul_function to True
        # See 2252914222
        if self.f2.nul_function:
            d["ymin"]=0
            d["ymax"]=0
        return d
    def xmax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmax']
    def xmin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmin']
    def ymax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymax']
    def ymin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymin']
    def get_normal_point(self,x,dy):
        vecteurNormal =  self.get_normal_vector(x)
        return self.get_point(x).translate(self.get_normal_vector.fix_size(dy))
    def length(self,mll=None,Mll=None):
        """
        numerically returns the arc length on the curve between two bounds of the parameters.

        If no parameters are given, return the total length.
        
        INPUT:

        - ``mll,Mll`` - the minimal and maximal values of the parameters

        OUTPUT:
        a number.

        EXAMPLES:

        The length of the circle of radius `sqrt(2)` in the first quadrant. We check that we 
        get the correct result up to 0.01::

            sage: from phystricks import *
            sage: curve=ParametricCurve(x,sqrt(2-x**2))
            sage: bool( abs(pi*sqrt(2)/2) - curve.length(0,sqrt(2)) <0.01) 
            True
        
        """
        if mll==None :
            mll=self.llamI
        if Mll==None :
            Mll=self.llamF
        return numerical_integral(self.speed,mll,Mll)[0]
    def arc_length(self,mll=None,Mll=None):
        print("You should use 'length' instead.")
        return self.length(mll=mll,Mll=Mll)
    def get_parameter_at_length(self,l):
        """
        return the value of the parameter corresponding to the given arc length.
        """
        # TODO : create this function
        pass 
    def getFunctionIntegral( self,fun,  lmin=None,lmax=None ):
        """
        Return the integral of 'fun' from 'lmin' to 'lmax'.
        """
        if lmin==None:
            lmin=self.llamI
        if lmax==None:
            lmax=self.llamF
        return numerical_integral(fun,lmin,lmax)[0]
    def getNextRegularFunctionParameters( self, lmin,lmax,fun,df,xunit=1,yunit=1 ):
        """
        Return a value 'nl' of the parameter such that the integral of 'fun' from 'lmin' to 'nl' is 'df'.

        `lmax` - is the maximal value of the parameter. If the interval [lmin,lmax]  reveals to be too small, return 'None'

        """
        # Vcurve is the curve as visually seen taking the dilatation into account.
        Vf1=phyFunction(self.f1(xunit*x))
        Vf2=phyFunction(self.f2(yunit*x))
        Vcurve=ParametricCurve(Vf1,Vf2)

        prop_precision = float(df)/100      # precision of the interval
        if prop_precision == 0:
            raise ValueError,"prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. dl=%s"%str(dl)

        # We'll perform a dichotomy method.
        # 'too_large' is a value of the parameter we know to be too large
        # 'too_small' is a value of the parameter we know to be too small
        # 'ell' is the median value on which the condition is tested. 
        # The dichotomy method consist to make 'too_large' or 'too_small' become 'ell' and to recalculate a new 'ell'

        too_small=lmin
        too_large=lmax
        if Vcurve.getFunctionIntegral(fun,too_small,too_large) < df:
            return None

        max_iter=100
        done_iter=0
        while done_iter<max_iter :
            ell=(too_large+too_small)/2
            done_iter+=1
            integral=Vcurve.getFunctionIntegral(fun,lmin,ell)
            if abs(integral-df)<prop_precision :
                return ell
            if integral>df:
                too_large=ell
            if integral<df:
                too_small=ell
        raise ShouldNotHappenException("I give up with this dichotomy")

    def getRegularFunctionParameters( self, lmin,lmax,fun,df,initial_point=False,final_point=False,xunit=1,yunit=1 ):
        """
        `fun` - is a function on the curve, expressed by the parameter.

        We return a list of points  x_i on the curve such that the integral of 'fun' from x_i to x_{i+1} is df.

        This is a visual function in the sense that the curve is first transformed in order to take the dilatation into account.

        EXAMPLE :

        Taking as 'fun' the norm of the tangent vector, one consider the arc length
        """
        prop_precision = float(df)/100      # precision of the interval
        if prop_precision == 0:
            raise ValueError,"prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. dl=%s"%str(dl)

        x=var('x')
        # Vcurve is the curve as visually seen taking the dilatation into account.
        Vf1=phyFunction(self.f1(xunit*x))
        Vf2=phyFunction(self.f2(yunit*x))
        Vcurve=ParametricCurve(Vf1,Vf2)

        PIs = []            # The list of selected values of the parameter
        if initial_point:
            PIs.append(mll)
        if final_point:
            PIs.append(Mll)
        ll=lmin
        while ll is not None :
            ll=Vcurve.getNextRegularFunctionParameters(ll,lmax,fun,df,xunit=1,yunit=1)
            if ll is not None:
                PIs.append(ll)
        return PIs

    def getRegularLengthParameter(self,mll,Mll,dl,initial_point=False,final_point=False,xunit=1,yunit=1):
        """ 
        return a list of values of the parameter such that the corresponding points are equally spaced by dl.
        Here, we compute the distance using the method arc_length.

        INPUT:

        - ``mll,Mll`` - the initial and final values of the parameters.

        - ``dl`` - the arc length distance between the points corresponding
                    to the returned values.

        - ``initial_point`` - (default=False) it True, return also the initial parameters (i.e. mll).

        - ``final_point`` - (default=False) it True, return also the final parameter (i.e. Mll)

        """
        return self.getRegularFunctionParameters(mll,Mll,self.speed,dl,initial_point=initial_point,final_point=final_point,xunit=xunit,yunit=yunit)

    def get_regular_points(self,mll,Mll,dl):
        """
        Return a list of points regularly spaced (with respect to the arc length) by dl. 

        mll is the inital value of the parameter and Mll is the end value of the parameter.

        In some applications, you prefer to use ParametricCurve.getRegularLengthParameter. The latter method returns the list of
        values of the parameter instead of the list of points. This is what you need if you want to draw tangent vectors for example.
        """
        return [self.get_point(ll) for ll in self.getRegularLengthParameter(mll,Mll,dl)]
    def get_wavy_points(self,mll,Mll,dl,dy,xunit=1,yunit=1):
        """
        Return a list of points which do a wave around the parametric curve.
        """
        PAs = self.getRegularLengthParameter(mll,Mll,dl,xunit=xunit,yunit=yunit)
        PTs = [self.get_point(mll)]
        for i in range(0,len(PAs)) :
            llam = float(PAs[i])
            v=self.get_normal_vector(llam)
            vp=v.F-v.I
            w=Vector(vp.x*yunit/xunit,vp.y*xunit/yunit).fix_visual_size(dy,xunit,yunit)
            PTs.append( self.get_point(llam)+w*(-1)**i )
        PTs.append(self.get_point(Mll))
        return PTs
    def rotate(self,theta):
        """
        Return a new ParametricCurve which graph is rotated by <theta> with respect to self.

        theta is given in degree.
        """
        alpha=radian(theta)
        g1=cos(alpha)*self.f1+sin(alpha)*self.f2
        g2=-sin(alpha)*self.f1+cos(alpha)*self.f2
        return ParametricCurve(g1,g2)
    def graph(self,mx,Mx):
        gr = ParametricCurve(self.f1,self.f2,(mx,Mx))
        gr.parameters=self.parameters.copy()
        return gr
    def __call__(self,llam,approx=False):
        return self.get_point(llam,approx)
    def __str__(self):
        t=var('t')
        a=[]
        a.append("<The parametric curve given by")
        a.append("x(t)=%s"%repr(self.f1.sage(x=t)))
        a.append("y(t)=%s"%repr(self.f2.sage(x=t)))
        a.append("between {} and {}>".format(self.mx,self.Mx))
        return "\n".join(a)

    def reverse(self):
        """
        return the curve in the inverse sense but on the same interval

        EXAMPLE::

        sage: from phystricks import *
        sage: x=var('x')
        sage: curve=ParametricCurve(cos(x),sin(x)).graph(0,2*pi).reverse()
        sage: print curve
        <The parametric curve given by
        x(t)=cos(2*pi - t)
        y(t)=sin(2*pi - t)
        between 0 and 2*pi>
        """
        x=var('x')
        a=self.llamI
        b=self.llamF
        f1=self.f1.sage(x=b-(x-a))
        f2=self.f2.sage(x=b-(x-a))
        return ParametricCurve(f1,f2).graph(a,b)
    def bounding_box(self,pspict=None):
        xmin=self.xmin(self.llamI,self.llamF)
        xmax=self.xmax(self.llamI,self.llamF)
        ymin=self.ymin(self.llamI,self.llamF)
        ymax=self.ymax(self.llamI,self.llamF)
        bb = BoundingBox( Point(xmin,ymin),Point(xmax,ymax)  )
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def representative_points(self):
        initial = numerical_approx(self.llamI)      # Avoid the string "pi" in the latex code.
        final = numerical_approx(self.llamF)
        plotpoints=self.parameters.plotpoints
        if plotpoints==None :
            plotpoints=50
        if self.parameters.force_smoothing :
            Llam=self.getRegularLengthParameter(initial,final,self.length()/plotpoints,initial_point=True,final_point=False)
        else :
            import numpy
            # If not RR, the elements of Llam are type numpy.float64. In this case, computing the sqrt of negative return NaN instead of complex.
            # Then we cannot remove the probably fake imaginary part. It happens for the function sqrt(cos(x)) with x=3*pi/2. 
            Llam=[ RR(s) for s in  numpy.linspace(initial,final,plotpoints)]
        pts = [ self.get_point(x,advised=False) for x in Llam ]

        pl=[]
        for P in pts:
            isreal,Q=test_imaginary_part_point(P)
            if not isreal:
                print("There is a not so small imaginary part ... prepare to crash or something")
            pl.append(Q)
        return pl

    def action_on_pspict(self,pspict):
        if self.wavy :
            waviness = self.waviness
            curve=InterpolationCurve(self.curve.get_wavy_points(self.llamI,self.llamF,waviness.dx,waviness.dy,xunit=pspict.xunit,yunit=pspict.yunit),context_object=self)
            curve.parameters=self.parameters.copy()

            pspict.DrawGraph(curve)
        else:
            points_list=self.representative_points()
            curve=InterpolationCurve(points_list)
            curve.parameters=self.parameters.copy()
            curve.mode="trivial"
            pspict.DrawGraph(curve)
        for v in self.record_arrows:
            pspict.DrawGraph(v)
    def latex_code(self,language=None,pspict=None):
        return ""


