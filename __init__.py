# -*- coding: utf8 -*-

###########################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2009-2011
# email: moky.math@gmail.com

"""
A collection of tools for building LaTeX-pstricks figures with python.

COMMAND LINE ARGUMENTS:

    - ``--pdf`` - the picture arrives as an \includegraphics of a pdf. It also creates the `pdf` file.

    - ``--eps`` - the picture arrives as an \includegraphics of a eps. It also creates the `eps` file.

    - ``--png`` - the picture arrives as an \includegraphics of a png. It also creates the `png` file.

    - ``--create-png`` - create the png file, but does not change the `.pstricks`
                         file. Thus the LaTeX output will not be modified.
                         
                         See :class:`TestPspictLaTeXCode` and the function :func:`create_png_file`
                         in :class:`PspictureToOtherOutputs`

    NOTES:

        - Here we are really speaking about pspicture. There will be one file of one 
          \includegraphics for each pspicture. This is not figure-wise.

        - Using `--pdf`, `--create-png`, etc. create the picture from an auxiliary
          LaTeX file that will we compiled and converted on the fly. As a consequence,
          customizations (e.g. fonts) will not be taken into account. 
          See `pspict.specific_needs`

    - ``--create_tests`` - create a `tmp` file in which the pspicture is written.

    - ``--tests`` - compares the produced pspicture with the corresponding `tmp` file and
                    raises a ValueError if it does not correspond.
                    If this option is set, nothing is written on the disk.

                    See :class:`TestPspictLaTeXCode`
"""

# __init__.py contains constructors, classes and functions to be used directly by the end-user
# SmallComputations.py contains functions that does not requires phystricks.
#                       these are string or number manipulations
# main.py contains the LaTeX aspects
# BasicGeometricObjects.py contains the code the geometry.
#
# Ideally, __init__.py should only contain functions that return instances of classes from BasicGeometricObjects.py

#from __future__ import division
from sage.all import *
import codecs
import math, sys, os

from BasicGeometricObjects import GraphOfASegment


def PolarSegment(P,r,theta):
    """
    returns a segment on the base point P (class Point) of length r angle theta (degree)
    """
    alpha = radian(theta)
    return Segment(P, Point(P.x+r*math.cos(alpha),P.y+r*math.sin(alpha)) )

class ParametricCurve(object):
    """
    This class describes a parametric curve.

    INPUT:

    - ``f1,f2`` - functions.

    OUTPUT:
    an object ready to be drawn.

    EXAMPLES::

        sage: x=var('x')
        sage: f1=phyFunction(x)
        sage: f2=phyFunction(x**2)
        sage: F=ParametricCurve(f1,f2).graph(-2,3)
        sage: print F.pstricks_code()
        \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{-2.00000000000000}{3.00000000000000}{t | t^2 }

    Notice that due to several `@lazy_attribute`, changing the components after creation could be buggy.


    .. literalinclude:: phystricksCycloide.py

    .. image:: Picture_FIGLabelFigCycloidePICTCycloide-for_eps.png

    """
    # The derivatives of the parametric curves are stored in the
    # dictionary attribute self._derivative_dict
    def __init__(self,f1,f2):
        self.f1=EnsurephyFunction(f1)
        self.f2=EnsurephyFunction(f2)
        self._derivative_dict={0:self}
    def pstricks(self,pspict=None):
        # The difficult point with pstrics is that the syntax is "f1(t) | f2(t)" with the variable t.
        #   In order to produce that, we use the Sage's function repr and the syntax f(x=t)
        var('t')
        return "%s | %s "%(SubstitutionMathPsTricks(repr(self.f1.sage(x=t)).replace("pi","3.1415")),  SubstitutionMathPsTricks(repr(self.f2.sage(x=t)).replace("pi","3.1415")) )

    @lazy_attribute
    def speed(self):
        r"""
        return the norm of the speed function.

        That is the function

        EXAMPLES::

            sage: curve=ParametricCurve(cos(x),sin(2*x))
            sage: print curve.speed
            x |--> sqrt(sin(x)^2 + 4*cos(2*x)^2)
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
        
            sage: var('x')
            x
            sage: f1=phyFunction(cos(2*x))
            sage: f2=phyFunction(x*exp(2*x))
            sage: F=ParametricCurve(f1,f2)
            sage: print F.derivative()
            The parametric curve given by
            x(t)=-2*sin(2*t)
            y(t)=2*t*e^(2*t) + e^(2*t)
            sage: print F.derivative(3)
            The parametric curve given by
            x(t)=8*sin(2*t)
            y(t)=8*t*e^(2*t) + 12*e^(2*t)
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
                P.advised_mark_angle=self.get_normal_vector(llam).angle()
            except TypeError :
                print "It seems that something got wrong somewhere in the computation of the advised mark angle. Return 0 as angle."
                P.advised_mark_angle=0
        return P
    def get_tangent_vector(self,llam,advised=False):
        """
        returns the tangent vector to the curve for the value of the parameter given by llam.
           The vector is normed to 1.

        INPUT:
        - ``llam`` - the value of the parameter on which we want the tangent
        - ``advised`` - (default = False) if True, the initial point is returned with its
                                            advised_mark_angle. This takes quite a long time
                                            of computation (and creates infinite loops if used
                                            in some circumstances)

        EXAMPLES:
        sage: F=ParametricCurve(x,x**2)
        sage: print F.get_tangent_vector(0)
        vector I=Point(0,0) F=Point(1,0)
        sage: print F.get_tangent_vector(1)
        vector I=Point(1,1) F=Point(1/5*sqrt(5) + 1,2/5*sqrt(5) + 1)
        """
        initial = self.get_point(llam,advised)     
        return AffineVector( initial,Point(initial.x+self.derivative().f1(llam),initial.y+self.derivative().f2(llam)) ).normalize()
    def get_normal_vector(self,llam,advised=False,normalize=True):
        """
        Return the outside normal vector to the curve for the value llam of the parameter.
           The vector is normed to 1.

        An other way to produce normal vector is to use
        self.get_tangent_vector(llam).orthogonal()
        However the latter does not guarantee to produce an outside pointing vector.

        If you want the second derivative vector, use self.get_derivative(2). This will not produce a normal vector in general.

        EXAMPLES:
        sage: F=ParametricCurve(sin(x),x**2)
        sage: print F.get_normal_vector(0)
        vector I=Point(0,0) F=Point(0,-1)
        """
        anchor=self.get_point(llam,advised=False)
        tangent=self.get_tangent_vector(llam)
        N = AffineVector(tangent.orthogonal())
        # The delicate part is to decide if we want to return N or -N. We select the angle which is on the same side of the curve
        #                                           than the second derivative.
        # If v is the second derivative, either N or -N has positive inner product with v. We select the one with
        # negative inner product since the second derivative vector is inner.
        try :
            second=self.get_second_derivative_vector(llam)
        except :
            print "Something got wrong with the computation of the second derivative. I return the default normal vector"
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

            sage: F=ParametricCurve(x,x**3)

        Normalizing a null vector produces a warning::

            sage: print F.get_second_derivative_vector(0,normalize=True)
            vector I=Point(0,0) F=Point(0,0)

        ::

            sage: print F.get_second_derivative_vector(0,normalize=False)
            vector I=Point(0,0) F=Point(0,0)
            sage: print F.get_second_derivative_vector(1)
            vector I=Point(1,1) F=Point(1,2)

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
    def get_minmax_data(self,deb,fin):
        """
        The difference between this and the get_minmax_data from Sage
        if that here we cut to 3 digits. This is due to
        the fact that we need the result to be reproducible
        for tests.

        WARNING: this is no more the case. See the example bellow.

        EXAMPLES::
            
            sage: from phystricks import *
            sage: f=1.5*(1+cos(x))
            sage: cardioid=PolarCurve(f)
            sage: cardioid.get_minmax_data(0,2*pi)
            {'xmin': -0.37499998976719928, 'ymin': -1.9484987597486128, 'ymax': 1.9482356168366479, 'xmax': 3.0}

        """
        dico_sage = MyMinMax(parametric_plot( (self.f1,self.f2), (deb,fin) ).get_minmax_data())
        return MyMinMax(dico_sage)
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
    def arc_length(self,mll,Mll):
        """
        numerically returns the arc length on the curve between two bounds of the parameters
        
        INPUT:

        - ``mll,Mll`` - the minimal and maximal values of the parameters

        OUTPUT:
        a number.

        EXAMPLES:

        The length of the circle of radius `sqrt(2)` in the first quadrant. We check that we 
        get the correct result up to 0.01::

            sage: curve=ParametricCurve(x,sqrt(2-x**2))
            sage: bool( abs(pi*sqrt(2)/2) - curve.arc_length(0,sqrt(2)) <0.01) 
            True
        
        """
        return numerical_integral(self.speed,mll,Mll)[0]
    def get_regular_parameter(self,mll,Mll,dl):
        """ 
        returns a list of values of the parameter such that the corresponding points are equally spaced by dl.
        Here, we compute the distance using the method arc_length.
        """
        prop_precision = float(dl)/100      # precision of the interval
        fp = self.derivative()
        minDll = abs(Mll-mll)/1000
        ll = mll
        PIs = []
        while ll < Mll :
            v = math.sqrt( (fp.f1(ll))**2+(fp.f2(ll))**2 )
            if v == 0 :
                print "v=0"
                Dll = minDll
            Zoom = 1
            Dll = dl/v
            grand = Mll
            petit = ll
            if abs(self.arc_length(ll,ll+Dll)) > dl :
                grand = ll+Dll
                while abs(self.arc_length(ll,petit)) > dl :
                    petit = (grand+petit)/2
            else :
                petit = ll+Dll
                while abs(self.arc_length(ll,grand)) < dl :
                    grand = 2*grand - ll
            ell = (petit+grand)/2
            while abs(self.arc_length( ll, ell )-dl) > prop_precision:
                if prop_precision == 0:
                    raise ValueError,"prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. dl=%s"%str(dl)
                ell = (grand+petit)/2
                if self.arc_length(ll,ell) > dl :
                    grand = ell
                else :
                    petit = ell
            ll = (petit+grand)/2
            if ll < Mll :
                PIs.append( ll )
        return PIs
    def get_regular_points_old(self,mll,Mll,dl):
        return [self.get_point(ll) for ll in self.get_regular_parameter_old(mll,Mll,dl)]
    def get_regular_points(self,mll,Mll,dl):
        """
        Return a list of points regularly spaced (with respect to the arc length) by dl. 

        mll is the inital value of the parameter and Mll is the end value of the parameter.

        In some applications, you prefer to use ParametricCurve.get_regular_parameter. The latter method returns the list of
        values of the parameter instead of the list of points. This is what you need if you want to draw tangent vectors for example.
        """
        return [self.get_point(ll) for ll in self.get_regular_parameter(mll,Mll,dl)]
    def get_wavy_points(self,mll,Mll,dl,dy):
        """
        Return a list of points which do a wave around the parametric curve.
        """
        PAs = self.get_regular_parameter(mll,Mll,dl)
        PTs = []
        for i in range(0,len(PAs)) :
            llam = float(PAs[i])
            PTs.append( self.get_point(llam)+self.get_normal_vector(llam).fix_size(dy)*(-1)**i )
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
        #return phystricks.GraphOfAParametricCurve(self,mx,Mx)      # I do not remember why I did so (March, 2, 2011)
        return GraphOfAParametricCurve(self,mx,Mx)
    def __call__(self,llam,approx=False):
        return self.get_point(llam,approx)
    def __str__(self):
        var('t')
        a=[]
        a.append("The parametric curve given by")
        a.append("x(t)=%s"%repr(self.f1.sage(x=t)))
        a.append("y(t)=%s"%repr(self.f2.sage(x=t)))
        return "\n".join(a)
def PolarCurve(fr,ftheta=None):
    """
    return the parametric curve (class ParametricCurve) corresponding to the 
    curve of equation r=f(theta) in polar coordinates.

    If ftheta is not given, return the curve
    x(t)=fr(t)cos(t)
    y(t)=fr(t)sin(t)

    If ftheta is given, return the curve
    x(t)=fr(t)cos( ftheta(t) )
    y(t)=fr(t)sin( ftheta(t) )

    EXAMPLES:
    
    .. literalinclude:: phystricksCardioid.py
    .. image:: Picture_FIGLabelFigCardioidPICTCardioid-for_eps.png

    """
    x=var('x')
    if ftheta==None :
        f1=fr*cos(x)
        f2=fr*sin(x)
    else:
        f1=fr(x=x)*cos(ftheta(x=x))
        f2=fr(x=x)*sin(ftheta(x=x))
    return ParametricCurve(f1,f2)

def phyFunction(fun,mx=None,Mx=None):
    """
    Represent a function
    """
    if isinstance(fun,BasicGeometricObjects.GraphOfAphyFunction):
        return GraphOfAphyFunction(fun.phyFunction,mx,Mx)
    return GraphOfAphyFunction(fun,mx,Mx)

class MeasureLength(BasicGeometricObjects.GraphOfASegment):
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

    .. literalinclude:: phystricksIntervalleUn.py
    .. image:: Picture_FIGLabelFigIntervallePICTIntervalle-for_eps.png
    
    In order to check the position of the arrow line,
    we check the position of the mark_point::

        sage: O=Point(0,0)
        sage: A=Point(1,0)

    Horizontal line directed from right to left; the
    arrow line has to be bellow::

        sage: measureOA=MeasureLength(Segment(O,A),0.1)
        sage: print measureOA.mark_point()
        Point(0.500000000000000,-0.100000000000000)

    Horizontal line directed from left to right::

        sage: measureAO=MeasureLength(Segment(A,O),0.1)
        sage: print measureAO.mark_point()
        Point(0.5,0.100000000000000)

    Vertical line::

        sage: B=Point(0,2)
        sage: measureOB=MeasureLength(Segment(O,B),0.1)
        sage: print measureOB.mark_point()
        Point(0.100000000000000,1.0)

        

    USEFUL ATTRIBUTE:

    - ``self.advised_mark_angle`` - the angle at which we advise you to put the mark.
                                    It indicates the direction orthogonal to the segment,
                                    with the orientation given in the discussion about the
                                    sign of <dist>.

    ::

        sage: m=MeasureLength(Segment( Point(1,1) ,Point(2,2) ),0.1)
        sage: print m.advised_mark_angle
        AngleMeasure, degree=315.000000000000,radian=-1/4*pi

    You are invited to use advised_mark_angle. If not the position of the mark
    could be unpredictable.
    """
    def __init__(self,seg,dist=0.1):
        try :
            self.segment=seg.segment
        except AttributeError :
            self.segment=seg
        self.dist=dist
        self.delta=seg.rotation(-90).fix_size(self.dist)
        self.mseg=seg.translate(self.delta)
        GraphOfASegment.__init__(self,self.mseg)
        self.advised_mark_angle=self.delta.angle()
        self.mI=self.mseg.I
        self.mF=self.mseg.F
    def math_bounding_box(self,pspict=None):
        return GraphOfASegment(self.mseg).math_bounding_box(pspict)
    def bounding_box(self,pspict=None):
        bb=self.mseg.bounding_box(pspict)
        if self.marque:
            C=self.mseg.center()
            C.marque=self.marque
            C.mark=self.mark
            C.mark.graph=C
            bb.AddBB(C.bounding_box(pspict))
        return bb
    def mark_point(self):
        return self.mseg.center()
    def pstricks_code(self,pspict=None):
        a=[]
        C=self.mseg.center()
        vI=AffineVector(C,self.mI)
        vF=AffineVector(C,self.mF)
        vI.parameters=self.parameters
        vF.parameters=self.parameters
        a.append(vI.pstricks_code())
        a.append(vF.pstricks_code())
        #if self.marque :
        #    a.append(self.mark.pstricks_code(pspict))
        return "\n".join(a)
class InterpolationCurve(GraphOfAnObject):
    """
    determine an interpolation curve from a list of points.

    INPUT:
    - ``points_list`` - a list of points that have to be joined.

    OPTIONAL INPUT:

    - ``context_object`` -  the object that is going to use the InterpolationCurve's pstricks_code.
                            ImplicitCurve and wavy curves are using InterpolationCurve as "backend"
                            for the pstricks_code.
                            Here we use the context_object in order to take this one into account
                            when determining the parameters (color, ...).
                            See :func:`self.pstricks_code()`.

    EXAMPLES:

    This example is valid, but will not plot the expected line (this is a feature of `\pscurve`)::

        sage: F=InterpolationCurve([Point(0,0),Point(1,1)])

    If you want to plot the small segment, you have to add a point in the center::

        sage: F=InterpolationCurve([Point(0,0),Point(0.5,0.5),Point(1,1)])

    The following draws a circle::
    
        sage: C=Circle(Point(0,0),1)
        sage: G=InterpolationCurve([C.get_point(2*pi/i,advised=False) for i in range(1,100)])

    Notice in the lase example the use of advised=False in order to speed up the computation.

    NOTE:

    InterpolationCurve is used in order to produce implicit plot and wavy functions.

    """

    def __init__(self,points_list,context_object=None):
        GraphOfAnObject.__init__(self,self)
        self.parameters.color="brown"
        self.points_list=points_list
        self.context_object=context_object
        if self.context_object is None:
            self.contex_object=self
    def get_minmax_data(self):
        """
        Return a dictionary whose keys give the xmin, xmax, ymin, and ymax
        data for this graphic.

        EXAMPLES:
        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).get_minmax_data()
        {'xmin': -1, 'ymin': -1, 'ymax': 1, 'xmax': 1}
        """
        xmin=min([P.x for P in self.points_list])
        xmax=max([P.x for P in self.points_list])
        ymin=min([P.y for P in self.points_list])
        ymax=max([P.y for P in self.points_list])
        if dict:
            return MyMinMax({'xmin':xmin, 'xmax':xmax,'ymin':ymin, 'ymax':ymax})
        else:
            return xmin,xmax,ymin,ymax
    def xmin(self):
        return self.get_minmax_data()['xmin']
    def xmax(self):
        return self.get_minmax_data()['xmax']
    def ymin(self):
        return self.get_minmax_data()['ymin']
    def ymax(self):
        return self.get_minmax_data()['ymax']
    def bounding_box(self,pspict=None):
        """
        Return the bounding box of the interpolation curve

        EXAMPLES:    
        sage: print InterpolationCurve([Point(0,0),Point(1,1)]).bounding_box()
        (0,0),(1,1)
        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: print InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).bounding_box()
        (-1,-1),(1,1)

        NOTE:
        Since the bounding box is computed from the give points while the curve is an interpolation,
        this bounding box is incorrect to the extend that \pscurve does not remains in the convex hull
        of the given points.

        EXAMPLE:
        sage: F=InterpolationCurve([Point(-1,1),Point(1,1),Point(1,-1),Point(-1,-1)])
        sage: print F.bounding_box()
        (-1,-1),(1,1)
        """
        bb = BoundingBox( Point(self.xmin(),self.ymin()),Point(self.xmax(),self.ymax())  )
        return bb
    def math_bounding_box(self,pspict=None):
        """
        return the bounding box corresponding to the curve without decorations.

        See InterpolationCurve.bounding_box()
        """
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        """
        return the pstricks code of the interpolation curve trough the given points

        EXAMPLES:

        sage: C=Circle(Point(0,0),1)
        sage: F=InterpolationCurve([Point(0,0),Point(1,1)])
        sage: print F.pstricks_code()
        \pscurve[linestyle=solid,linecolor=brown](0,0)(1.00000000000000,1.00000000000000)
        sage: H=InterpolationCurve([Point(-1,1),Point(1,1),Point(1,-1),Point(-1,-1)])
        sage: print H.pstricks_code()
        \pscurve[linestyle=solid,linecolor=brown](-1.00000000000000,1.00000000000000)(1.00000000000000,1.00000000000000)(1.00000000000000,-1.00000000000000)(-1.00000000000000,-1.00000000000000)
        """
        l = []
        try:
            params=self.context_object.params()
        except AttributeError :
            params=self.params()
        l.append("\pscurve["+params+"]")
        for p in self.points_list:
            l.append(p.coordinates(numerical=True))
        return "".join(l)
        
    def __str__(self):
        """
        Return a string representation

        EXAMPLES:
        sage: print InterpolationCurve([Point(0,0),Point(1,1)])
        InterpolationCurve with points ['Point(0,0)', 'Point(1,1)']
        """
        return "InterpolationCurve with points %s"%(str([str(P) for P in self.points_list]))

def ImplicitCurve(f,xrange,yrange,plot_points=100):
    """
    return the implicit curve given by equation f on the range xrange x yrange

    This is a constructor for the class GraphOfAnImplicitCurve
    INPUT:
    - ``f`` -- a function of two variables or equation in two variables

    - ``xrange,yrange`` - the range on which we want to compute the implicit curve.
    
    OPTIONAL INPUT:
    - ``plot_points`` - (defautl : 100) the number of points that will be calculated in each direction. 

    The resulting bounding box will not be in general xrange x yrange. 
    EXAMPLES:
    We know that the curve x^2+y^2=2 is a circle of radius sqrt(2). Thus even if you ask a range of size 5, 
    you will only get the bounding box of size sqrt(2)
    sage: var('x,y')
    (x, y)
    sage: f(x,y)=x**2+y**2
    sage: F=ImplicitCurve(f==2,(x,-5,5),(y,-5,5))
    sage: print F.bounding_box()
    (-1.41342281879,-1.41342281879),(1.41342281879,1.41342281879)

    But the following will be empty :
    sage: G=ImplicitCurve(f==2,(x,-1,1),(y,-1,1))
    sage: print G.paths
    []

    If you give very low value of plot_points, you get incorrect results :
    sage: H=ImplicitCurve(f==2,(x,-2,2),(y,-2,2),plot_points=3)
    sage: print H.bounding_box()
    (-1.41411295429,-1.41411295429),(1.41411295429,1.41411295429)

    Using Sage's implicit_curve and matplotlib, a list of points "contained" in the curve is created. The bounding_box is 
    calculated from that list. The pstricsk code generated will be an interpolation curve passing trough all these points.
    """
    return GeometricImplicitCurve(f).graph(xrange,yrange,plot_points=100)
class SurfaceBetweenParametricCurves(GraphOfAnObject):
    """
    Represents a surface between two parametric curves.

    INPUT:

    - ``curve1,curve2`` - two parametric curves.

    OPTIONAL ARGUMENTS :
    - ``(mx1,Mx1)`` - a tuple. Initial and final values of the parameter for the first curve.

    - ``reverse1`` - (default=False) if True, reverse the sense of curve1.

    - ``reverse2`` - (default=True) if True, reverse the sense of curve1.

    Let us suppose that curve1 goes from A1 to B1 and curve2 from A2 to B2
    If we do not reverse the sense of anything, the result will be
    the surface delimited by

    curve1:        A1 -> B1
    up_segment:    B1 -> B2
    curve2:        A2 -> B2
    low_segment:   A2 -> A1
        
    This is wrong since the last point of each line is not the first
    point of the next line.

    For that reason, the second curve is, by default, reversed in order to get
    curve1:             A1 -> B1
    up_segment:         B1 -> B2
    curve2 (reversed):  B2 -> A2
    low_segment:        A2 -> A1

    OUTPUT:
    An object ready to be draw.

    EXAMPLES::

        sage: curve1=ParametricCurve(x,x**2).graph(2,3)
        sage: curve2=ParametricCurve(x,x**3).graph(2,5)
        sage: region=SurfaceBetweenParametricCurves(curve1,curve2)

    The segment "closing" the domain are available by the attributes `low_segment and up_segment`::

        sage: print region.low_segment
        segment I=Point(2,8) F=Point(2,4)
        sage: print region.up_segment
        segment I=Point(3,9) F=Point(5,125)

    The initial and final values of the parameters can be given in different ways.
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

    If the optional argument `interval` is provided, it erases the other intervals::

        sage: f1=phyFunction(x**2).graph(1,2)
        sage: f2=phyFunction(x)
        sage: curve=SurfaceBetweenParametricCurves(f1,(f2,3,4),interval=(7,8))
        sage: print curve.mx1,curve.Mx1,curve.mx2,curve.Mx2
        7 8 7 8

    NOTE:
    If the two curves make intersections, the result could be messy.
    
    .. literalinclude:: phystricksBetweenParametric.py
    .. image:: Picture_FIGLabelFigBetweenParametricPICTBetweenParametric-for_eps.png

    """
    def __init__(self,curve1,curve2,interval=None,reverse1=False,reverse2=True):
        GraphOfAnObject.__init__(self,self)

        curve=[curve1,curve2]
        self.curve=[None,None]
        self.mx=[None,None]
        self.Mx=[None,None]

        self.reverse1=reverse1
        self.reverse2=reverse2

        for i in [0,1]:
            if isinstance(curve[i],tuple) :
                self.mx[i]=curve[i][1]
                self.Mx[i]=curve[i][2]
                self.curve[i]=EnsureParametricCurve(curve[i][0]).graph(self.mx[i],self.Mx[i])
            else :
                self.mx[i],self.Mx[i]=extract_interval_information(curve[i])
                self.curve[i]=EnsureParametricCurve(curve[i]).graph(self.mx[i],self.Mx[i])

            if self.mx[i] == None :
                raise ValueError, "Cannot determine the initial or final value of the parameter for %s"%str(curve[i])

            if "parameters" in dir(curve[i]):
                curve[i].parameters.replace_to(self.curve[i].parameters)

            if interval:
                self.mx[i]=interval[0]
                self.Mx[i]=interval[1]

        self.curve1=self.curve[0]
        self.curve2=self.curve[1]
        self.mx1=self.mx[0]
        self.mx2=self.mx[1]
        self.Mx1=self.Mx[0]
        self.Mx2=self.Mx[1]

        self.low_segment=Segment(self.curve2.get_point(self.mx2,advised=False),self.curve1.get_point(self.mx1,advised=False))
        self.up_segment=Segment(self.curve1.get_point(self.Mx1,advised=False),self.curve2.get_point(self.Mx2,advised=False))

        self.add_option("fillstyle=vlines") 
        self.parameters.color=None       

    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        bb.append(self.curve1,pspict=None)
        bb.append(self.curve2,pspict=None)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        a=[]
       
        c1=self.curve1.graph(self.mx1,self.Mx1)
        c2=self.curve2.graph(self.mx2,self.Mx2)
        if self.reverse1:
            c1=c1.reverse()
        if self.reverse2:
            c2=c2.reverse()

        custom=CustomSurface(c1,self.up_segment,c2,self.low_segment)
        self.parameters.add_to(custom.parameters)     # This line is essentially dedicated to the colors
        a.append(custom.pstricks_code())

        a.append(self.curve1.pstricks_code(pspict))
        a.append(self.curve2.pstricks_code(pspict))
        a.append(self.low_segment.pstricks_code(pspict))
        a.append(self.up_segment.pstricks_code(pspict))
        return "\n".join(a)

class SurfaceUnderFunction(SurfaceBetweenFunctions):
    """
    Represent a surface under a function.

    This is a particular case of SurfaceBetweenFunctions when the second function is the y=0 axis.

    The function `f` becomes `self.f1` while self.f2 will be the function 0 (this is a consequence of inheritance).
    The function f will also be recorded as self.f.

    INPUT:

    - ``f`` - a function
    - ``mx,Mx`` - initial and final values 

    EXAMPLES:

    .. literalinclude:: phystricksSurfaceFunction.py
    .. image:: Picture_FIGLabelFigSurfaceFunctionPICTSurfaceFunction-for_eps.png

    """

    def __init__(self,f,mx,Mx):
        self.f=EnsurephyFunction(f)
        var('x')
        f2=0
        SurfaceBetweenFunctions.__init__(self,self.f,f2,mx,Mx)
    def __str__(self):
        return "SurfaceUnderFunction %s x:%s->%s"%(self.f,str(self.mx),str(self.Mx))

class Polygon(GraphOfAnObject):
    """
    represent a polygon.

    .. literalinclude:: phystricksExPolygone.py
    .. image:: Picture_FIGLabelFigExPolygonePICTExPolygone-for_eps.png
    """
    def __init__(self,*args):
        GraphOfAnObject.__init__(self,self)
        self.points_list=list(args)
        self.edges_list=[]
        self.edge=Segment(Point(0,0),Point(1,1))    # This is an arbitrary segment that only serves to have a
                                                    # "model" for the parameters.
        for i in range(len(self.points_list)-1):
            segment=Segment(self.points_list[i],self.points_list[i+1])
            self.edges_list.append(segment)
        final_segment=Segment(self.points_list[-1],self.points_list[0])
        self.edges_list.append(final_segment)
        for edge in self.edges_list:
            edge.parameters=self.edge.parameters
    def math_bounding_box(self,pspict=None):
        bb=BoundingBox()
        for P in self.points_list:
            bb.append(P,pspict)
        return bb
    def bounding_box(self,pspict=None):
        return self.math_bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        a=[]
        custom=CustomSurface(tuple(self.edges_list))
        custom.parameters=self.parameters
        a.append(custom.pstricks_code(pspict))

        for edge in self.edges_list:
            a.append(edge.pstricks_code(pspict))
        return "\n".join(a)


class CustomSurface(GraphOfAnObject):
    """
    Represent the surface contained between some lines and (parametric) curves.

    INPUT:
    - ``*args`` - la tuple of lines like segments, functions, parametric curves.

    EXAMPLE:
  
    The following describes the surface between the circle of radius 1 and 
    the square of length 1::
    
        sage: C=Circle(Point(0,0),1)
        sage: arc=C.parametric_curve(0,pi/2)
        sage: h=Segment(Point(0,1),Point(1,1))
        sage: v=Segment(Point(1,1),Point(1,0))
        sage: surf=CustomSurface(arc,h,v)
        sage: print unify_point_name(surf.pstricks_code())
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,1.00000000000000){Xaaaa}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaab}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaac}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,0){Xaaad}
        \pscustom[linestyle=none,linecolor=black,fillstyle=vlines]{
        \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{0.000000000000000}{1.57079632679490}{cos(t) | sin(t) }
        <BLANKLINE>
        \pstLineAB[linestyle=solid,linecolor=black]{Xaaaa}{Xaaab}
        <BLANKLINE>
        \pstLineAB[linestyle=solid,linecolor=black]{Xaaac}{Xaaad}
        }

    The border is not drawn.

    This is somewhat the more general use of the pstricks's macro \pscustom
    """
    def __init__(self,*args):
        GraphOfAnObject.__init__(self,self)
        # len(args)==1 when doing CustomSurface(list) where `list` is  a list.
        if len(args)==1:
            args=args[0]
        self.graphList=list(args)
        self.add_option("fillstyle=vlines,linestyle=none")  
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        for obj in self.graphList :
            bb.AddBB(obj.bounding_box(pspict))
        return bb
    def math_bounding_box(self,pspict=None):
        bb=BoundingBox()
        for obj in self.graphList :
            bb.AddBB(obj.math_bounding_box(pspict))
        return bb
    def pstricks_code(self,pspict=None):
        # I cannot add all the obj.pstricks_code() inside the \pscustom because we cannot have \pstGeonode inside \pscustom
        # Thus I have to hack the code in order to bring all the \pstGeonode before the opening of \pscustom
        a=[]
        for obj in self.graphList :
            a.append(obj.pstricks_code(pspict))
        insideBefore="\n".join(a)
        insideBeforeList=insideBefore.split("\n")
        outsideList=[]
        insideList=[]
        for line in insideBeforeList:
            if "pstGeonode" in line :
                outsideList.append(line)
            else:
                insideList.append(line)
        outside="\n".join(outsideList)
        inside="\n".join(insideList)
        # Now we create the pscustom
        a=[]
        a.append(outside)
        if self.parameters.color :
            self.add_option("fillcolor="+self.parameters.color+",linecolor="+self.parameters.color+",hatchcolor="+self.parameters.color)
        a.append("\pscustom["+self.params()+"]{")
        a.append(inside)
        a.append("}")
        return "\n".join(a)



class SurfaceBetweenFunctions(GraphOfAnObject):
    r"""
    Represents a surface between two functions.

    INPUT:

    - ``f1,f2`` - functions (sage or phyFunction). ``f1`` is considered to be the upper function while ``f2`` is the lower function.

    - ``mx,Mx`` - (optional) initial and end values of x. If these are not given, we suppose that `f1` and `f2` are graphs.

    EXAMPLES:

    If you want the surface to be blue ::

        sage: surf=SurfaceBetweenFunctions(sin(x)+3,cos(x),0,2*pi)
        sage: surf.parameters.color="blue"

    If you want the function ``f1`` to be red without changing the color of the surface, you have to change
    the color AND the style::

        sage: surf.f1.parameters.color="red"
        sage: print "red" in surf.pstricks_code(),"solid" in surf.pstricks_code()
        True True

    Notice that the output of `surf.pstricks_code()` is too long to be written here.

    You can also try to control the option linestyle (use add_option).

    .. literalinclude:: phystricksexSurfaceBetweenFunction.py

    .. image:: Picture_FIGLabelFigexSurfaceBetweenFunctionPICTexSurfaceBetweenFunction-for_eps.png

    """

    #TODO: change this class into a function which returns a SurfaceBetweenParametricCurves instead.

    # linestyle=none in self.add_option corresponds to the fact that we do not want to draw the curve.
    # No default color are given; the reason is that we want to be able  to control the color of each element separately. 
    def __init__(self,f1,f2,mx=None,Mx=None):
        GraphOfAnObject.__init__(self,self)
        if mx==None :
            try:
                if f1.mx != f2.mx :
                    raise ValueError,"The initial values of %s and %s does not fit"%(str(f1),str(f2))
                mx=f1.mx
            except AttributeError :
                print "If you do not provide `mx` and/or `Mx`, you should pass graphs and not %s and %s"%(type(f1),type(f2))
        if Mx==None :
            try :
                if f1.Mx != f2.Mx :
                    raise ValueError,"The final values of %s and %s does not fit"%(str(f1),str(f2))
                Mx=f1.Mx
            except AttributeError :
                print "If you do not provide `mx` and/or `Mx`, you should pass graphs and not %s and %s"%(type(f1),type(f2))
        self.f1=EnsurephyFunction(f1).graph(mx,Mx)
        self.f2=EnsurephyFunction(f2).graph(mx,Mx)
        self.vertical_left=Segment(self.f1.get_point(mx,advised=False),self.f2.get_point(mx,advised=False))
        self.vertical_right=Segment(self.f1.get_point(Mx,advised=False),self.f2.get_point(Mx,advised=False))
        self.f1.parameters.style="none"
        self.f2.parameters.style="none"
        self.vertical_left.parameters.style="none"
        self.vertical_right.parameters.style="none"
        self.mx=mx
        self.Mx=Mx
        self.add_option("fillstyle=vlines,linestyle=none")  
        self.parameters.color=None              
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        bb.append(self.f1,pspict)
        bb.append(self.f2,pspict)
        #bb.AddY(0)      # Really, what was that line for ??
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        a=[]
        mx = numerical_approx(self.mx)     # Avoid "pi" in the pstricks code
        Mx = numerical_approx(self.Mx)

        surface=SurfaceBetweenParametricCurves(self.f1,self.f2,interval=(mx,Mx))
        self.parameters.add_to(surface.parameters)     # This line is essentially dedicated to the colors

        surface.low_segment=self.vertical_left
        surface.up_segment=self.vertical_right

        a.append(surface.pstricks_code(pspict))

        #a.append("\pscustom["+self.params()+"]{")
        #a.append("\psplot[linestyle=none]{"+str(deb)+"}{"+str(fin)+"}{"+self.f1.pstricks+"}")
        #a.append("\psplot[linestyle=none]{"+str(fin)+"}{"+str(deb)+"}{"+self.f2.pstricks+"}")
        #a.append("}")

        # This was before a change in GraphOfAphyFunction.pstricks_code (13005)
        #if self.f1.parameters.style != "none":
        #   a.append("\n".join(self.f1.pstricks_code()))
        #if self.f2.parameters.style != "none":
        #   a.append("\n".join(self.f2.pstricks_code()))
        if self.f1.parameters.style != "none":
            a.append(self.f1.pstricks_code())
        if self.f2.parameters.style != "none":
            a.append(self.f2.pstricks_code())
        if self.vertical_left.parameters.style != "none" :
            a.append(self.vertical_left.pstricks_code())
        if self.vertical_right.parameters.style != "none" :
            a.append(self.vertical_right.pstricks_code())
        return "\n".join(a)
def Vector(*args):
    """
    From the coordinates x,y, return the corresponding vector, i.e. the affine vector from (0,0) to (x,y).

    You can also only give a Point
    """
    try :
        x=args[0]
        y=args[1]
    except IndexError :
        x=args[0].x
        y=args[0].y
    return AffineVector(Point(0,0),Point(x,y))

def Circle(center,radius,angleI=0,angleF=360):
    """
    Return a circle of given radius and center.

    INPUT:

    - ``center`` - the center of the circle.

    - ``radius`` - the radius of the circle.
    
    - ``angleI`` - (default=0) If you want an arc of circle, this is the beginning angle.
    - ``angleF`` - (default=0) If you want an arc of circle, this is the ending angle.

    OUTPUT:

    A circle ready to be drawn

    EXAMPLES:

    The following describes the usual trigonometric circle::

            sage: circle=Circle(Point(0,0),1)
            sage: print circle.angleI
            AngleMeasure, degree=0.000000000000000,radian=0
            sage: print circle.angleF
            AngleMeasure, degree=360.000000000000,radian=0

    """
    # TODO: in the last example, the radian value should be 2*pi.
    return GraphOfACircle(center,radius)

def Rectangle(NW,SE):
    return GraphOfARectangle(GeometricRectangle(NW,SE))

def AffineVector(A=None,B=None):
    """
    return an affine vector.

    An affine vector is a vector whose origin is not specifically (0,0).

    EXAMPLES:
        
    An affine vector can be given by two points::

        sage: print AffineVector(Point(1,1),Point(pi,sqrt(2)))
        vector I=Point(1,1) F=Point(pi,sqrt(2))

    It can be simply derived from a segment::

        sage: segment=Segment( Point(1,1),Point(2,2)  )
        sage: av=AffineVector(segment)
        sage: print av
        vector I=Point(1,1) F=Point(2,2)

    If you pass an object which has a method `segment`, the
    :func:`AffineVector` will provide the corresponding affine vector::

        sage: axe=SingleAxe(  Point(-2,2),Vector(1,1),-3,3  )
        sage: print AffineVector(axe)
        vector I=Point(-5,-1) F=Point(1,5)

    NOTE:

    The main difference between a :func:`Segment` an :func:`AffineVector` is that
    the latter will be draw with an arrow. There are also some difference in their
    behaviour under rotation, dilatation and operations like that.

    """
    if B :      # If B is given, I suppose that we gave two points
        vect=Segment(A,B)
    else :
        try :
            vect=A.segment()
        except AttributeError :
            vect=A
    vect.arrow_type="vector"
    return vect
# the following is thanks to the python's french usenet group
#https://groups.google.com/group/fr.comp.lang.python/browse_thread/thread/5b19cfac661df251?hl=fr#
#http://users.rcn.com/python/download/Descriptor.htm
#vect.pstricks_code = types.MethodType(_vector_pstricks_code, vect, Segment)

class Grid(object):
    """
    A grid. This is main lines to appear at regular interval on the picture.


    ATTRIBUTES:

    - ``self.BB`` - the bounding box of the grid : its size.

    - ``self.Dx,self.Dy`` - the step of main subdivision along `X` and `Y` directions (have to be integers).

    - ``self.num_subX,self.num_subY`` - number of subdivision within each main subdivision of length Dx or Dy. When it is zero, there are no subdivisions.

    It draws lines on the integer multiples of `Dx`. It begins at the closest integer multiple of `Dx` from the lower left corner.
    It finishes before to reach the upper right corner if `Dx` the size.
    Subdivisions are drawn following the same rule.

    - ``self.draw_border`` - (default=False) If True, the border is drawn even if it does not  arrives on an integer multiple of Dx.
                                        It turns out that for aestetical reasons, this is a bad idea to turn it True.


    - ``self.main_horizontal`` : an objet of type :class:`GraphOfASegment`. This is the archetype of the horizontal lines
                                 of the main grid will be drawn.

    As an example, in order to have red main horizontal lines::

        sage: grid=Grid( BoundingBox() )
        sage: grid.main_horizontal.parameters.color = "red"

    """
    def __init__(self,bb):
        self.BB = bb
        self.options = Options()
        self.separator_name="GRID"
        self.add_option({"Dx":1,"Dy":1})        # Default values, have to be integer.
        self.Dx = self.options.DicoOptions["Dx"]
        self.Dy = self.options.DicoOptions["Dy"]
        self.num_subX = 2
        self.num_subY = 2
        self.draw_border = False
        self.main_horizontal = GraphOfASegment(Segment(Point(0,1),Point(1,1)))  # Ce segment est bidon, c'est juste pour les options de tracé.
        self.main_horizontal.parameters.color="gray"
        self.main_horizontal.parameters.style = "solid"
        self.main_vertical = GraphOfASegment(Segment(Point(0,1),Point(1,1)))
        self.main_vertical.parameters.color="gray"
        self.main_vertical.parameters.style = "solid"
        self.sub_vertical = GraphOfASegment(Segment(Point(0,1),Point(1,1))) 
        self.sub_vertical.parameters.color="gray"
        self.sub_vertical.parameters.style = "dotted"
        self.sub_horizontal = GraphOfASegment(Segment(Point(0,1),Point(1,1)))   
        self.sub_horizontal.parameters.color="gray"
        self.sub_horizontal.parameters.style = "dotted"
        self.border = GraphOfASegment(Segment(Point(0,1),Point(1,1)))   
        self.border.parameters.color = "gray"
        self.border.parameters.style = "dotted"
    def bounding_box(self,pspict=None):     # This method is for the sake of "Special cases aren't special enough to break the rules."
        return self.BB
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def add_option(self,opt):
        self.options.add_option(opt)
    def optionsTrace(self):
        return self.options.sousOptions(OptionsStyleLigne())
    def optionsParams(self):
        return self.options.sousOptions(["Dx","Dy"])
    def drawing(self):
        a = []
        # ++++++++++++ Border ++++++++ 
        #self.draw_border = False        # 16 oct 2010 : no more border  # commented this line on 14 March 2011
        if self.draw_border :
            # Right border
            if self.BB.Mx <> int(self.BB.Mx):
                S = self.BB.east_segment()
                S.merge_options(self.border)
                a.append(S)
            # Left border
            if self.BB.mx <> int(self.BB.mx):
                S = self.BB.west_segment()
                S.merge_options(self.border)
                a.append(S)
            # Upper border
            if self.BB.My <> int(self.BB.My):
                S = self.BB.north_segment()
                S.merge_options(self.border)
                a.append(S)
            # Lower border
            if self.BB.my <> int(self.BB.my):
                S = self.BB.south_segment()
                S.merge_options(self.border)
                a.append(S)
        # ++++++++++++ The vertical sub grid ++++++++ 
        if self.num_subX <> 0 :
            for x in  SubGridArray(self.BB.mx,self.BB.Mx,self.Dx,self.num_subX) :
                    S = Segment( Point(x,self.BB.my),Point(x,self.BB.My) )
                    S.merge_options(self.sub_vertical)
                    a.append(S)
        # ++++++++++++ The horizontal sub grid ++++++++ 
        if self.num_subY <> 0 :
            for y in  SubGridArray(self.BB.my,self.BB.My,self.Dy,self.num_subY) :
                    S = Segment( Point(self.BB.mx,y),Point(self.BB.Mx,y) )
                    S.merge_options(self.sub_horizontal)
                    a.append(S)
        # ++++++++++++ Principal horizontal lines ++++++++ 
        for y in MainGridArray(self.BB.my,self.BB.My,self.Dy) :
            S = Segment( Point(self.BB.mx,y),Point(self.BB.Mx,y) )
            S.merge_options(self.main_vertical)
            a.append(S)
        # ++++++++++++ Principal vertical lines ++++++++
        for x in MainGridArray(self.BB.mx,self.BB.Mx,self.Dx) :
            S = Segment( Point(x,self.BB.my),Point(x,self.BB.My) )
            S.merge_options(self.main_vertical)
            a.append(S)
        return a
    def pstricks_code(self,pspict=None):
        a=[]
        for element in self.drawing():
            a.append(element.pstricks_code(pspict))
        return "\n".join(a)

class AxesUnit(object):
    def __init__(self,numerical_value,latex_symbol=""):
        try :
            numerical_value=sage.rings.rational.Rational(numerical_value)
        except TypeError :
            pass
        self.numerical_value=numerical_value
        self.latex_symbol=latex_symbol
    def symbol(self,x):
        return latex(x)+self.latex_symbol
    def place_list(self,mx,Mx,frac=1,mark_origin=True):
        """
        return a tuple of 
        1. values that are all the integer multiple of <frac>*self.numerical_value between mx and Mx
        2. the multiple of the basis unit.

        Please give <frac> as literal real. Recall that python evaluates 1/2 to 0. If you pass 0.5, it will be converted to 1/2 for a nice display.
        """
        try :
            frac=sage.rings.rational.Rational(frac)     # If the user enters "0.5", it is converted to 1/2
        except TypeError :
            pass
        if frac==0:
            raise ValueError,"frac is zero in AxesUnit.place_list(). Maybe you ignore that python evaluates 1/2 to 0 ? (writes literal 0.5 instead) \n Or are you trying to push me in an infinite loop ?"
        l=[]
        k=var("TheTag")
        for x in MultipleBetween(frac*self.numerical_value,mx,Mx,mark_origin):
            if self.latex_symbol == "":
                l.append((x,"$"+latex(x)+"$"))
            else :
                pos=(x/self.numerical_value)*k
                text="$"+latex(pos).replace("\mbox{TheTag}",self.latex_symbol)+"$"  # This risks to be Sage-version dependent.
                l.append((x,text))
        return l

class SingleAxe(object):
    """
    Describe an axe.
    
    INPUT:

    - ``C`` - the center of the axe. This is the point corresponding to the "zero" coordinate
    - ``base`` - the unit of the axe. This indicates

                1. the direction
                2. the size of "1"

                A mark will be added at each integer multiple of that vector (but zero) including negative.
    - ``mx`` - the multiple of ``base`` at which the axe begins. This is typically negative
    - ``Mx`` -  the multiple of ``base`` at which the axe ends. This is typically positive
                    The axe goes from ``C+mx*base`` to ``C-Mx*base``. 

    OTHER CONTROLS :

    The default behaviour can be modified by the following attributes.

    - ``self.Dx`` - (default=1) A mark is written each multiple of ``self.Dx*base``.
    - ``self.mark_angle`` - the angle in degree under which the mark are written. By default this is orthogonal
                        to the direction given by ``self.base``.

    If an user-defined axes_unit is given, the length of ``base`` is "forgotten"

    EXAMPLES::
    
        sage: axe = SingleAxe(Point(1,1),Vector(0,1),-2,2)
    """
    def __init__(self,C,base,mx,Mx):
        self.C=C
        self.base=base
        self.mx=mx
        self.Mx=Mx
        self.options=Options()
        self.IsLabel=False
        self.axes_unit=AxesUnit(self.base.length(),"")
        self.Dx=1
        self.arrows="->"
        self.graduation=True
        self.numbering=True
        self.mark_origin=True
        self.mark_angle=degree(base.angle().radian-pi/2)
        #self.vertical=base.vertical
        #self.horizontal=base.horizontal
    
    # SingleAxe.segment cannot be a lazy attribute because we use it for some projections before
    # to compute the bounding box.
    def segment(self):
        return Segment(self.C+self.mx*self.base,self.C+self.Mx*self.base)
    def add_option(self,opt):
        self.options.add_option(opt)
    def add_label(self,dist,angle,marque):
        self.IsLabel = True
        self.Label = marque
        self.DistLabel = dist
        self.AngleLabel = angle
    def no_numbering(self):
        self.numbering=False
    def no_graduation(self):
        self.graduation=False
    def graduation_points(self,pspict):
        """
        Return the list of points that makes the graduation of the axes

        By defaut, it is one at each multiple of self.base. If an user-defined axes_unit is given, then self.base is modified.
        """
        if not self.graduation:
            return []
        points_list=[]
        bar_angle=SR(self.mark_angle+90).n(digits=7)    # pstricks does not accept too large numbers
        for x,symbol in self.axes_unit.place_list(self.mx,self.Mx,self.Dx,self.mark_origin):
            P=(x*self.base).F
            P.parameters.symbol="|"
            P.add_option("dotangle=%s"%str(bar_angle))
            #P.psName=P.psName+pspict.name+latinize(str(numerical_approx(x)))   # Make the point name unique.
            P.psName="ForTheBar"   # Since this point is not supposed to
                                       # be used, all of them have the same ps name.
            if self.numbering :
                P.put_mark(0.2,self.mark_angle,symbol,automatic_place=(pspict,"for axes",self.segment()))
                                            # I do not understand why I don't have to multiply 0.4 by xunit or yunit
            points_list.append(P)
        return points_list
    def bounding_box(self,pspict):
        BB=self.math_bounding_box(pspict)
        for P in self.graduation_points(pspict):
            BB.append(P,pspict)
            if P.marque :
                BB.append(P.mark,pspict)
        return BB
    def math_bounding_box(self,pspict):
        return self.segment().bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        """
        Return the pstricks code of the axe.
        """
        sDx=RemoveLastZeros(self.Dx,10)
        self.add_option("Dx="+sDx)
        #bgx = self.BB.mx
        #if self.BB.mx == int(self.BB.mx):      # Avoid having end of axes on an integer coordinate for aesthetic reasons.
        #   bgx = self.BB.mx + 0.01
        #self.BB.mx = bgx
        c=[]
        if self.IsLabel :
            P = self.segment().F
            P.parameters.symbol="none"
            P.put_mark(self.DistLabel,self.AngleLabel,self.Label)
            c.append(P.pstricks_code())
        if self.graduation :
            for P in self.graduation_points(pspict):
                c.append(P.pstricks_code(pspict,with_mark=True))
        h=AffineVector(self.segment())
        c.append(h.pstricks_code(pspicture))
        return "\n".join(c)

def Intersection(f,g):
    """
    When f and g are objects with an attribute equation, return the list of points of intersections.

    EXAMPLES::

        sage: fun=phyFunction(x**2-5*x+6)
        sage: droite=phyFunction(2)
        sage: pts = Intersection(fun,droite)
        sage: for P in pts:print P
        Point(4,2)
        Point(1,2)
    """
    var('x,y')
    pts=[]
    soluce=solve([f.equation,g.equation],[x,y])
    for s in soluce:
        a=s[0].rhs()
        b=s[1].rhs()
        pts.append(Point(a,b))
    return pts

def SinglePicture(name):
    """ Return the tuple of pspicture and figure that one needs in 90% of the cases. """
    fig = GenericFigure(name)
    pspict=fig.new_pspicture(name)
    return pspict,fig

def MultiplePictures(name,n):
    r"""
    return a figure with multiple subfigures. This is the other 10% of cases.

    INPUT:

    - `name` - the name of the figure.

    - `n` - the number of subfigures.

    You have to think about naming the subfigures.

    EXAMPLE::

        sage: pspict,fig = MultiplePictures("MyName",3)
        The result is on figure \ref{LabelFigMyName}.
        \newcommand{\CaptionFigMyName}{<+Type your caption here+>}
        \input{Fig_MyName.pstricks}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName0}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName1}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName2}
        sage: pspict[0].mother.caption="My first subfigure"
        sage: pspict[1].mother.caption="My second subfigure"
        sage: pspict[2].mother.caption="My third subfigure"

    Notice that a caption is related to a figure or a subfigure, not to a pspicture.

    See also :class:`subfigure`
    """
    fig = GenericFigure(name)
    pspict=[]
    for i in range(n):
        subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
        picture=subfigure.new_pspicture(name+"pspict"+str(i))
        pspict.append(picture)
    return pspict,fig

class global_variables(object):
    """
    Some global variables

    - ``create_formats`` - dictionary which says the exit files we want to produce. These can be

                    * eps,pdf,pfd : I think that these names are self-explaining.

                    * test : outputs a `tmp` file

    - ``exit_format`` - the format one wants to use in the LaTeX file. By default it is pstricks.

    - ``perform_tests`` - (default=False) If True, perform the tests.

    The difference between `create_formats` and `exit_format` is that `create_format` says
    what files are going to be _produced_ while `exit_format` is the format that LaTeX will see.

    Notice that `create_formats` is a plural while `exit_format` is a singlular. This is
    not a joke ;)
    """
    def __init__(self):
        self.create_formats={"eps":False,"pdf":False,"png":False,"test":False}
        self.exit_format="pstricks"
        self.perform_tests = False
    def special_exit(self):
        for sortie in self.create_formats.values():
            if sortie:
                return True
        return False



def Angle(A,O,B,r=None):
    """
    Return the angle AOB.

    It represent the angle formed at the point O with the lines
    OA and OB (in that order).

    INPUT:

    - ``A,O,A`` - points.

    - ``r`` - (default, see below) the radius of the arc circle marking the angle.

    OUTPUT:

    An object ready to be drawn of type :class:`GraphOfAnAngle`.

    If `r` is not given, a default value of 0.2 times the length OA is taken.

    EXAMPLES:

    Notice the difference between AOB and BOA::

        sage: A=Point(1,1)
        sage: O=Point(0,0)
        sage: B=Point(1,0)
        sage: print Angle(A,O,B).measure()
        AngleMeasure, degree=-45.0000000000000,radian=7/4*pi
        sage: print Angle(B,O,A).measure()
        AngleMeasure, degree=45.0000000000000,radian=1/4*pi


    .. literalinclude:: phystricksTriangleRectangle.py
    .. image:: Picture_FIGLabelFigTriangleRectanglePICTTriangleRectangle-for_eps.png

    """
    return GraphOfAnAngle(GeometricAngle(A,O,B,r))

def CircleOA(O,A):
    """
    From the centrer O and a point A, return the circle.

    INPUT:

    - ``O`` - a point that will be the center of the circle.
    
    - ``A`` - a point on the circle.

    OUTPUT:

    A circle ready to be drawn of type :class:`GraphOfACircle`.

    EXAMPLES::

        sage: A=Point(2,1)
        sage: O=Point(0,0)
        sage: circle=CircleOA(O,A)
        sage: circle.radius
        sqrt(5)

    """
    center=O
    radius=sqrt( (O.x-A.x)**2+(O.y-A.y)**2 )
    return Circle(O,radius)

def Point(x,y):
    """
    return a point.

    INPUT:

    - ``x,y`` - the coordinates of the point. These are numbers.

    EXAMPLES::

        sage: P=Point(-1,sqrt(2))
        sage: print P
        Point(-1,sqrt(2))

    You can pass variables::

        sage: x=var('x')
        sage: P=Point(x**2,1)   
        sage: print P
        Point(x^2,1)

    Notice that the coordinates of the point have to be numerical in order to be passed to pstricks at the end::

        sage: print P.pstricks_code()
        Traceback (most recent call last):
        ...
        TypeError: cannot evaluate symbolic expression numerically

                
    """
    return GraphOfAPoint(GeometricPoint(x,y))
def PolarPoint(r,theta):
    """
    return the point at polar coordinates (r,theta).

    INPUT:

    - ``r`` - the distance from origine
    - ``theta`` - the angle

    EXAMPLES::

        sage: print PolarPoint(2,45)
        Point(sqrt(2),sqrt(2))


    """
    return Point(r*cos(radian(theta)),r*sin(radian(theta)))
def Segment(A,B):
    return GraphOfASegment(GeometricSegment(A,B))

def VectorField(fx,fy,xvalues=None,yvalues=None,draw_points=None):
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

        sage: x,y=var('x,y')
        sage: F=VectorField(x*y,cos(x)+y)
        sage: F.divergence()
        (x, y) |--> y + 1


    If you want an automatic Cartesian grid of points, use xvalues and yvalues::

        sage: F=VectorField(exp(x+y),x**2+y**2,xvalues=(x,-1,1,3),yvalues=(y,-5,5,6))
        sage: len(F.draw_points)
        18
        sage: print F.draw_points[5]
        Point(-1.0,5.0)

    The same can be obtained using the following syntax (see the function GeometricVectorField.graph)::

        sage: F=VectorField(exp(x+y),x**2+y**2).graph(xvalues=(x,-1,1,3),yvalues=(y,-5,5,6))
        sage: len(F.draw_points)
        18
        sage: print F.draw_points[5]
        Point(-1.0,5.0)

    If you want a personal list of points, use draw_points ::

        sage: F=VectorField(exp(x+y),x**2+y**2, draw_points=[Point(1,1),Point(5,-23)] )
        sage: print F.draw_points[0]
        Point(1,1)    
        sage: print F.draw_points[1]
        Point(5,-23)

    A vector field with automatic management of the points to be drawn:

    .. literalinclude:: phystricksChampVecteursDeux.py
    .. image:: Picture_FIGLabelFigChampVecteursDeuxPICTChampVecteursDeux-for_eps.png

    A vector field with given points to be drawn: 

    .. literalinclude:: phystricksChampVecteur.py
    .. image:: Picture_FIGLabelFigChampVecteursPICTChampVecteurs-for_eps.png


    """
    if xvalues is None and yvalues is None and draw_points is None :
        return GeometricVectorField(fx,fy)
    return GeometricVectorField(fx,fy).graph(xvalues,yvalues,draw_points)

global_vars = global_variables()
if "--eps" in sys.argv :
    global_vars.exit_format="eps"
    global_vars.create_formats["eps"] = True
if "--png" in sys.argv :
    global_vars.exit_format="png"
    global_vars.create_formats["png"] = True
if "--pdf" in sys.argv :
    global_vars.exit_format="pdf"
    global_vars.create_formats["pdf"] = True
if "--create-png" in sys.argv :
    global_vars.create_formats["png"] = True
if "--create-pdf" in sys.argv :
    global_vars.create_formats["pdf"] = True
if "--create-eps" in sys.argv :
    global_vars.create_formats["eps"] = True
if "--create-tests" in sys.argv :
    global_vars.create_formats["test"] = True
if "--tests" in sys.argv :
    global_vars.perform_tests = True
