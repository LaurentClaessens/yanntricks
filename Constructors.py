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

# copyright(c) Laurent Claessens, 2010-2016
# email: moky.math@gmai.com


def Point(a,b):
    """
    return a point.

    INPUT:

    - ``x,y`` - the coordinates of the point. These are numbers.


    EXAMPLES::

        sage: from phystricks import *
        sage: print Point(1,1)
        <Point(1,1)>
        sage: print Point(pi,sqrt(2))
        <Point(pi,sqrt(2))>
    
    You can pass variables::

        sage: x=var('x')
        sage: P=Point(x**2,1)   
        sage: print P
        <Point(x^2,1)>

    Notice that the coordinates of the point have to be numerical in order to be passed to tikz (and then LaTeX) at the end::

    """
    import GraphOfAPoint
    return GraphOfAPoint.GraphOfAPoint(a,b)

def PolarPoint(r,theta):
    """
    return the point at polar coordinates (r,theta).

    INPUT:

    - ``r`` - the distance from origine
    - ``theta`` - the angle

    EXAMPLES::

        sage: from phystricks import *
        sage: print PolarPoint(2,45)
        <Point(sqrt(2),sqrt(2))>


    """
    return Point(r*cos(radian(theta)),r*sin(radian(theta)))

def Segment(A,B=None,vector=None):
    """
    Creates a segment.

    The typical use is to give two points.
    An alternative is to provide a point and a vector.

    EXAMPLES::

        sage: from phystricks import *
        sage: seg=Segment(  Point(0,0),Point(2,10) )
        sage: print seg.I            
        <Point(0,0)>
        sage: print seg.F
        <Point(2,10)>
        sage: seg2=Segment(  Point(-3,4),vector=Vector(1,2) )
        sage: print seg2.I            
        <Point(-3,4)>
        sage: print seg2.F
        <Point(-2,6)>
        sage: v=AffineVector(  Point(1,2),Point(-2,5) )
        sage: seg3=Segment(  Point(-3,4),vector=v )
        sage: print seg3.I            
        <Point(-3,4)>
        sage: print seg3.F
        <Point(-6,7)>
    """
    if vector:
        B=A+vector
    import GraphOfASegment
    return GraphOfASegment.GraphOfASegment(A,B)

def PolarSegment(P,r,theta):
    """
    returns a segment on the base point P (class Point) of length r angle theta (degree)
    """
    alpha = radian(theta)
    import GraphOfASegment
    return Segment(P, Point(P.x+r*cos(alpha),P.y+r*sin(alpha)) )

def AffineVector(A=None,B=None):
    """
    return an affine vector.

    An affine vector is a vector whose origin is not specifically (0,0).

    EXAMPLES:
        
    An affine vector can be given by two points::

        sage: from phystricks import *
        sage: print AffineVector(Point(1,1),Point(pi,sqrt(2)))
        <vector I=<Point(1,1)> F=<Point(pi,sqrt(2))>>

    It can be simply derived from a segment::

        sage: segment=Segment( Point(1,1),Point(2,2)  )
        sage: av=AffineVector(segment)
        sage: print av
        <vector I=<Point(1,1)> F=<Point(2,2)>>

    If you pass an object which has a method `segment`, the
    :func:`AffineVector` will provide the corresponding affine vector::

        sage: from phystricks.BasicGeometricObjects import SingleAxe
        sage: axe=SingleAxe(  Point(-2,2),Vector(1,1),-3,3  )
        sage: print AffineVector(axe)
        <vector I=<Point(-5,-1)> F=<Point(1,5)>>

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
    from Constructors import AffineVector
    return AffineVector(Point(0,0),Point(x,y))

def Circle(center,radius,angleI=0,angleF=360,visual=False,pspict=None):
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

            sage: from phystricks import *
            sage: circle=Circle(Point(0,0),1)
            sage: print circle.angleI
            AngleMeasure, degree=0.000000000000000,radian=0
            sage: print circle.angleF
            AngleMeasure, degree=360.000000000000,radian=0

    """
    # TODO: in the last example, the radian value should be 2*pi.
    if visual and not pspict :
        print("You cannot try to use 'visual' not giving a pspicture")
        raise ValueError
    import GraphOfACircle
    return GraphOfACircle.GraphOfACircle(center,radius,angleI=angleI,angleF=angleF,visual=visual,pspict=pspict)

def CircleOA(O,A):
    """
    return a circle with center 'O' and passing through the point 'A'
    """
    radius=distance(O,A)
    return Circle(O,radius)

def CircleAB(A,B):
    """
    return a circle with diameter [AB]
    """
    center=Segment(A,B).midpoint()
    return CircleOA(center,A)

def CircularSector(center,radius,a,b):
    circle=Circle(center,radius)
    P=circle.get_point(a)
    Q=circle.get_point(b)
    l1=Segment( circle.center,P  )
    l2=circle.graph(a,b)
    l3=Segment(Q,circle.center)
    return CustomSurface(l1,l2,l3)

def FractionPieDiagram(center,radius,a,b):
    return BasicGeometricObjects.GraphOfAFractionPieDiagram(center,radius,a,b)

class BoundingBox(object):
    r"""
    Represent the bounding box of something.

    INPUT:

    - ``xmin`` the coordinate of the left border (same for xmax,ymin and ymax)

    - ``mother`` - the object of which this is the bounding box.

    By default, the bounding box has `mx=1000`, `Mx=-1000` and the same for `y`.

    The attribute `parent` is used for drawing the bounding boxes that can vary with
    the dilatation. The usual way for drawing the bounding bow of the mark of an object is to put
    `P.mark.bounding_box(pspict)` in `pspict.DrawGraph`.

    The problem arises when one dilates the figure after the call to `DrawGraph`.
    Indeed the bounding box of the mark will be the LaTeX's size of the box
    containing the text. In order to be correct one has to take into account the 
    parameters `xunit`/`yunit` that are not yet fixed at the time of `DrawGraph`.

    If 'math' is True, it always tries to include 'math_bounding_box' instead of 'bounding_box'
    """
    def __init__(self,P1=None,P2=None,xmin=1000,xmax=-1000,ymin=1000,ymax=-1000,parent=None,mother=None,math=False):
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.mother=mother
        self.math=math
        if P1 :
            self.add_math_object(P1,check_too_large=False)
            self.add_math_object(P2,check_too_large=False)
        if parent :
            raise DeprecationWarning,"Use mother instead"   # 2014
    def add_object(self,obj,pspict=None,fun="bounding_box",check_too_large=True):
        if self.math:
            fun="math_bounding_box"
        try :
            bb=obj.__getattribute__(fun)(pspict=pspict)
        except AttributeError,message :
            if obj:     # If obj is None, we are not surprised.
                print "The attribute {1} of the object {0} seems to have problems".format(obj,fun)
                print "The message was :"
                print message
                raise main.NoMathBoundingBox(obj,fun)
        else :
            if check_too_large :
                bb.check_too_large(pspict)
            self.AddBB(bb)
    def add_math_object(self,obj,pspict=None,check_too_large=True):
        try :
            self.add_object(obj,pspict=pspict,fun="math_bounding_box",check_too_large=check_too_large)
        except TypeError :
            print obj,type(obj)
            raise
    def check_too_large(self,pspict=None):
        """
        Raise a ValueError if the bounding box is too large.
        """
        check_too_large(self,pspict=pspict)
    def N(self):
        return Segment(self.NW(),self.NE()).center()
    def S(self):
        return Segment(self.SW(),self.SE()).center()
    def NE(self):
        return Point(self.xmax,self.ymax)
    def NW(self):
        return Point(self.xmin,self.ymax)
    def SE(self):
        return Point(self.xmax,self.ymin)
    def SW(self):
        return Point(self.xmin,self.ymin)
    def north_segment(self):
        return Segment( self.NW(),self.NE() )
    def south_segment(self):
        return Segment( self.SW(),self.SE() )
    def east_segment(self):
        return Segment( self.NE(),self.SE() )
    def west_segment(self):
        return Segment( self.NW(),self.SW() )
    def coordinates(self,pspict=None):
        return self.SW().coordinates(pspict=pspict)+self.NE().coordinates(pspict=pspict)
    def xsize(self):
        return self.xmax-self.xmin
    def ysize(self):
        return self.ymax-self.ymin
    def extraX_left(self,l):
        """Enlarge the bounding box of a length l on the left"""
        self.xmin=self.xmin-l
    def extraX_right(self,l):
        """Enlarge the bounding box of a length l on the right"""
        self.xmax=self.xmax+l
    def extraX(self,l):
        """Enlarge the bounding box of a length l on both sides"""
        self.extraX_left(l)
        self.extraX_right(l)
    def addX(self,x):
        self.xmin=min(self.xmin,x)
        self.xmax=max(self.xmax,x)
    def AddX(self,x):
        raise DeprecationWarning   # Use addX instead. Augustus, 24, 2014
        self.xmin=min(self.xmin,x)
        self.xmax=max(self.xmax,x)
    def addY(self,y):
        self.ymin=min(self.ymin,y)
        self.ymax=max(self.ymax,y)
    def AddY(self,y):
        raise DeprecationWarning   # Use addY instead. Augustus, 24, 2014
        self.ymin=min(self.ymin,y)
        self.ymax=max(self.ymax,y)
    def AddBB(self,bb):
        self.xmin = min(self.xmin,bb.xmin)
        self.ymin = min(self.ymin,bb.ymin)
        self.xmax = max(self.xmax,bb.xmax)
        self.ymax = max(self.ymax,bb.ymax)
    def append(self,graph,pspict=None):
        if isinstance(graph,list):
            raise KeyError,"%s is a list"%graph
        if not pspict :
            print "You should provide a pspict in order to add",graph
        on=False
        if self.math:
            try :
                bb=graph.math_bounding_box(pspict=pspict)
            except AttributeError :
                on=True
        if not self.math or on :
            try :
                bb=graph.bounding_box(pspict=pspict)
            except (ValueError,AttributeError),msg :
                print "Something got wrong with %s"%str(graph)
                print msg
                print "If you want to debug me, you should add a raise here."
                print("HURVooBiLyiI",graph,type(graph))
                print("MRLWooXAmSHT",self.math,on)
                raise
        self.AddBB(bb)
    def add_math_graph(self,graphe,pspict=None):
        try :
            self.addBB(graphe.math_bounding_box(pspict))
        except NoMathBoundingBox,message :
            print message
            self.addBB(graphe.bounding_box(pspict))
    def AddCircleBB(self,Cer,xunit,yunit):
        """
        Add a deformed circle to the bounding box.

        INPUT:

        - ``Cer`` - a circle. 
        - ``xunit,yunit`` - the `x` and `y` deformation coefficients.

        The given circle will be deformed by the coefficient xunit and yunid and the be added to `self`.
        """
        raise DeprecationWarning,"use 'append' instead"     # February 21, 2015
        self.AddPoint( Point( Cer.center.x-Cer.radius/xunit,Cer.center.y-Cer.radius/yunit ) )
        self.AddPoint( Point( Cer.center.x+Cer.radius/xunit,Cer.center.y+Cer.radius/yunit ) )
    def AddAxes(self,axes):
        self.AddPoint( axes.BB.SW() )
        self.AddPoint( axes.BB.NE() )
    def latex_code(self,language=None,pspict=None):
        rect=Rectangle(self.SW(),self.NE())
        rect.parameters.color="cyan"
        return rect.latex_code(language=language,pspict=pspict)
    def action_on_pspict(self,pspict=None):
        pass
    def bounding_box(self,pspict=None):
        return self
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def copy(self):
        return BoundingBox(xmin=self.xmin,ymin=self.ymin,xmax=self.xmax,ymax=self.ymax)
    def __str__(self):
        return "<BoundingBox xmin={0},xmax={1}; ymin={2},ymax={3}>".format(self.xmin,self.xmax,self.ymin,self.ymax)
    def __contains__(self,P):
        """
        Return True if the point P belongs to self and False otherwise.

        Allow to write
        if P in bb :
        http://www.rafekettler.com/magicmethods.html
        """
        if P.x <= self.xmax and P.x>=self.xmin and P.y<=self.ymax and P.y>=self.ymin:
            return True
        return False

def Mark(graph,dist,angle,text,mark_point=None,automatic_place=False):
    """
    Describe a mark (essentially a P on a point for example) angle is given in degree or AngleMeasure

    INPUT:

    - ``graph`` - the graph that it marked. This is usually a point but it can be anything that has a `mark_point` method.
    - ``dist`` - the distance between `graph.mark_point()` and the mark.
    - ``angle`` - the angle given in degree or `AngleMeasure`.
    - ``text`` - the text to be printed on the mark. This is typically a LaTeX stuff like "$P$".
    - ``automatic_place`` - this is a tuple (pspict,anchor) where pspict is the pspicture in which we are working and ̣`anchor` is one of "corner","N","S","W","E" or special cases (see below).

            - "corner" will put the mark at the distance such that the corner of the bounding box is at the (relative) position (dist;angle) instead of the center of the mark.

            - "N" will put the mark in such a way that the center of the north side of the bounding box is at the position (dist;angle).

            - "for axes". In this case we expect to have a 3-tuple `(pspict,"for axes",segment)` where `segment` is a segment (typically the segment of an axe).  In this case, we suppose `self.angle` to be orthogonal to the segment.  The mark will be put sufficiently far for the bounding box not to cross the segment.

         What is done is that the closest corner of the bounding box is at position (dist;angle) from the point.
    """
    import GraphOfAMark
    return GraphOfAMark.GraphOfAMark(graph,dist,angle,text,mark_point=None,automatic_place=False)

def AngleAOB(A,O,B,r=None):
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

        sage: from phystricks import *
        sage: A=Point(1,1)
        sage: O=Point(0,0)
        sage: B=Point(1,0)
        sage: print Angle(A,O,B).measure()
        AngleMeasure, degree=-45.0000000000000,radian=-1/4*pi
        sage: print Angle(B,O,A).measure()
        AngleMeasure, degree=45.0000000000000,radian=1/4*pi


    .. literalinclude:: phystricksTriangleRectangle.py
    .. image:: Picture_FIGLabelFigTriangleRectanglePICTTriangleRectangle-for_eps.png

    """
    from GraphOfAnAngle import GraphOfAnAngle
    return GraphOfAnAngle(A,O,B,r)

def Angle(A,O,B,r=None):
    print("Warning : You should use 'AngleAOB' instead of 'Angle'")
    return AngleAOB(A,O,B,r=r)

def phyFunction(fun,mx=None,Mx=None):
    """
    Represent a function.

    INPUT:

    - ``fun`` - a function.
    - ``mx,Mx`` - initial and final value of the argument.

    EXAMPLES::
    
        sage: from phystricks import *
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

    .. literalinclude:: phystricksChiSquared.py
    .. image:: Picture_FIGLabelFigChiSquaredPICTChiSquared-for_eps.png

    OTHER EXAMPLE

    .. literalinclude:: phystricksNonAnalyticOne.py
    .. image:: Picture_FIGLabelFigNonAnalyticOnePICTNonAnalyticOne-for_eps.png

    """
    # The first try is that the given expression is already a phyFunction.
    try:
        return fun.graph(mx,Mx)     
    except (AttributeError,TypeError):
        pass

    # The second try is that `fun` is something that Sage knows.
    try:
        sy=symbolic_expression(fun)
    except TypeError:       # This deals with probability distributions for example.
        return BasicGeometricObjects.GraphOfAphyFunction(fun,mx,Mx)

        # I'm trying not to use NonAnalytic anymore, July 1, 2014
        #return BasicGeometricObjects.NonAnalyticFunction(fun,mx,Mx)
    x=var('x')
    import GraphOfAphyFunction
    return GraphOfAphyFunction.GraphOfAphyFunction(sy.function(x),mx,Mx)

def ParametricCurve(f1,f2,interval=(None,None)):
    """
    This class describes a parametric curve.

    INPUT:

    - ``f1,f2`` - functions that are the components of the parametric curve.
    - 'interval' - the interval on which the curve is considered.

    If 'f1' has mx and Mx and interval is not given, they are used.

    OUTPUT:
    an object ready to be drawn.

    EXAMPLES::

        sage: from phystricks import *
        sage: x=var('x')
        sage: f1=phyFunction(x)
        sage: f2=phyFunction(x**2)
        sage: F=ParametricCurve(f1,f2).graph(-2,3)
        sage: G=ParametricCurve(f1,f2,mx=-2,Mx=3)

    Notice that due to several `@lazy_attribute`, changing the components after creation could produce unattended results.

    .. literalinclude:: phystricksCycloide.py

    .. image:: Picture_FIGLabelFigCycloidePICTCycloide-for_eps.png

    """
    llamI=interval[0]
    llamF=interval[1]
    if "mx" in dir(f1) :
        if f1.mx != None:
            llamI=f1.mx
            llamF=f1.Mx
    f1=EnsurephyFunction(f1)
    f2=EnsurephyFunction(f2)
    if isinstance(llamI,AngleMeasure):
        raise
    import GraphOfAParametricCurve
    return GraphOfAParametricCurve.GraphOfAParametricCurve(f1,f2,llamI,llamF)

def InterpolationCurve(points_list,context_object=None,mode=None):
    """
    determine an interpolation curve from a list of points.

    INPUT:
    - ``points_list`` - a list of points that have to be joined.

    OPTIONAL INPUT:

    - ``context_object`` -  the object that is going to use the InterpolationCurve's latex code.
                            ImplicitCurve and wavy curves are using InterpolationCurve as "backend"
                            for the latex code.
                            Here we use the context_object in order to take this one into account
                            when determining the parameters (color, ...).

    EXAMPLES:

    This example is valid, but will not plot the expected line (this is a feature of `\pscurve`)::

        sage: from phystricks import *
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
    import InterpolationCurveGraph
    return InterpolationCurveGraph.InterpolationCurveGraph(points_list,context_object,mode=mode)

from Utilities import *
