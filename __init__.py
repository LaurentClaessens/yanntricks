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

#from __future__ import division
from sage.all import *
import codecs
import math, sys, os

from phystricks.SmallComputations import *

def GenericFigure(nom):
    """
    This function returns a figure with some default values. It creates coherent label, file name and prints the lines to be appended in the LaTeX file to include the figure.
    """
    caption = "\CaptionFig"+nom     # This is also hard-coded in the function main.figure.LaTeX_lines
    label = "LabelFig"+nom          # The string "LabelFig" is hard-coded in the function main.figure.LaTeX_lines
    nFich = "Fig_"+nom+".pstricks"

    fig=main.figure(caption,label,nFich)
    print fig.LaTeX_lines()
    return fig

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
        picture.figure_mother=fig
        pspict.append(picture)
    return pspict,fig

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

def EnsurephyFunction(f):
    if "sage" in dir(f):        # This tests in the same time if the type if phyFunction or GraphOfAphyFunction
        return phyFunction(f.sage)
    if "phyFunction" in dir(f):
        return f.phyFunction()
    else :
        return phyFunction(f)

def EnsureParametricCurve(curve):
    if "parametric_curve" in dir(curve):
        return curve.parametric_curve()
    else :
        return curve

def PolarSegment(P,r,theta):
    """
    returns a segment on the base point P (class Point) of length r angle theta (degree)
    """
    alpha = radian(theta)
    return Segment(P, Point(P.x+r*cos(alpha),P.y+r*sin(alpha)) )

def ParametricCurve(*args,**opt):
    """
    This class describes a parametric curve.

    INPUT:

    - ``f1,f2`` - functions that are the components of the parametric curve.
    - ``mx,Mx`` - (optionals) Initial and final value of the parameter.

    Alternatively you can give a parametric curve as only argument.

    If `mx` and `Mx` are given, a graph object is returned.

    OUTPUT:
    an object ready to be drawn.

    EXAMPLES::

        sage: x=var('x')
        sage: f1=phyFunction(x)
        sage: f2=phyFunction(x**2)
        sage: F=ParametricCurve(f1,f2).graph(-2,3)
        sage: G=ParametricCurve(f1,f2,mx=-2,Mx=3)
        sage: print F.pstricks_code()
        \parametricplot[plotstyle=curve,linestyle=solid,plotpoints=1000,linecolor=blue]{-2.00000000000000}{3.00000000000000}{t | t^2 }
        sage: F.pstricks_code()==G.pstricks_code()
        True

    Notice that due to several `@lazy_attribute`, changing the components after creation could produce funny results.

    .. literalinclude:: phystricksCycloide.py

    .. image:: Picture_FIGLabelFigCycloidePICTCycloide-for_eps.png

    """
    # First, we consider the case in which two functions are given
    llamI=None
    llamF=None
    if "f2" not in dir(args[0]):
        f1=args[0]
        f2=args[1]
        if len(args)>2:
            llamI=args[2]
            llamF=args[3]
        f1=EnsurephyFunction(f1)
        f2=EnsurephyFunction(f2)

    # Then we consider the case in which the first argument is a parametric curve
    else :
        f1=EnsurephyFunction(args[0].f1)
        f2=EnsurephyFunction(args[0].f2)
        if len(args)>1:
            llamI=args[1]
            llamF=args[2]
    if "mx" in opt.keys() and "Mx" in opt.keys() :
        llamI=opt["mx"]
        llamF=opt["Mx"]
    return BasicGeometricObjects.GraphOfAParametricCurve(f1,f2,llamI,llamF)

def PolarCurve(fr,ftheta=None):
    """
    return the parametric curve (:class:`ParametricCurve`) corresponding to the 
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
    Represent a function.

    INPUT:

    - ``fun`` - a function.
    - ``mx,Mx`` - initial and final value of the argument.

    EXAMPLES::
    
        sage: f=phyFunction(cos(x))
        sage: f(pi/2)
        0

        sage: g=phyFunction(2*f,0,pi)
        sage: g(pi)
        -2
    """
    # The first try is that the given expression is already a phyFunction.
    try:
        return fun.graph(mx,Mx)     
    except AttributeError:
        pass
    # The second try is that `fun` is something that Sage knows.
    #fun=SR(fun)         # This manage the case of constant functions. I think that symbolic_expression is sufficient (May, 1, 2011)
    x=var('x')
    sy=symbolic_expression(fun).function(x)
    return BasicGeometricObjects.GraphOfAphyFunction(sy,mx,Mx)

def CustomSurface(*args):
    if len(args)==1:
        args=args[0]
    graphList=list(args)
    return BasicGeometricObjects.GraphOfACustomSurface(graphList)

def MeasureLength(seg,dist=0.1):
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
        Point(0.5,-0.100000000000000)

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
    return BasicGeometricObjects.GraphOfAMeasureLength(seg,dist)

def InterpolationCurve(points_list,context_object=None):
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
    return BasicGeometricObjects.GraphOfAnInterpolationCurve(points_list,context_object)


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
    (-1.413,-1.413),(1.413,1.413)

    But the following will be empty :
    sage: G=ImplicitCurve(f==2,(x,-1,1),(y,-1,1))
    sage: print G.paths
    []

    If you give very low value of plot_points, you get incorrect results :
    sage: H=ImplicitCurve(f==2,(x,-2,2),(y,-2,2),plot_points=3)
    sage: print H.bounding_box()
    (-1.414,-1.414),(1.414,1.414)


    Using Sage's implicit_curve and matplotlib, a list of points "contained" in the curve is created. The bounding_box is 
    calculated from that list. The pstricsk code generated will be an interpolation curve passing trough all these points.
    """
    return BasicGeometricObjects.GeometricImplicitCurve(f).graph(xrange,yrange,plot_points=100)


def SurfaceBetweenParametricCurves(curve1,curve2,interval=None,reverse1=False,reverse2=True):
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
    An object ready to be draw.

    EXAMPLES::

        sage: curve1=ParametricCurve(x,x**2).graph(2,3)
        sage: curve2=ParametricCurve(x,x**3).graph(2,5)
        sage: region=SurfaceBetweenParametricCurves(curve1,curve2)

    The segment "closing" the domain are available by the attributes `Isegment and Fsegment`::

        sage: print region.Isegment
        segment I=Point(2,8) F=Point(2,4)
        sage: print region.Fsegment
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
    return BasicGeometricObjects.GraphOfASurfaceBetweenParametricCurves(curve1,curve2,interval,reverse1,reverse2)

def SurfaceUnderFunction(f,mx,Mx):
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
    f2=0
    return SurfaceBetweenFunctions(f,f2,mx=mx,Mx=Mx)


def Polygon(*args):
    """
    represent a polygon.

    .. literalinclude:: phystricksExPolygone.py
    .. image:: Picture_FIGLabelFigExPolygonePICTExPolygone-for_eps.png
    """
    return BasicGeometricObjects.GraphOfAPolygon(args)

def CustomSurface(*args):
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
    if len(args)==1:        # This is in the case in which we give a tuple or a list directly
        a=args[0]
    else :
        a=args
    return BasicGeometricObjects.GraphOfACustomSurface(list(a))

def SurfaceBetweenFunctions(f1,f2,mx=None,Mx=None):
    r"""
    Represents a surface between two functions.

    INPUT:

    - ``f1,f2`` - functions (sage or phyFunction). ``f1`` is considered to be the upper function while ``f2`` is the lower function.

    - ``mx,Mx`` - (optional) initial and end values of x. If these are not given, we suppose that `f1` and `f2` are graphs.
                            If `f1` is a graph while `mx` is given, the value of `f1.mx` is forgotten and the given `mx`
                            is taken into account.

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
    mx1=mx
    mx2=mx
    Mx1=Mx
    Mx2=Mx
    if "mx" in dir(f1) and mx==None:
        mx1=f1.mx
        Mx1=f1.Mx
    if "mx" in dir(f2) and mx==None:
        mx2=f2.mx
        Mx2=f2.Mx
    # The following is a precaution because it happens that
    # f1 has a "mx" attribute which is set to None while
    # a mx is given here.
    if mx1 is None:
        mx1=mx
    if Mx1 is None:
        Mx1=Mx
    if mx2 is None:
        mx2=mx
    if Mx2 is None:
        Mx2=Mx
    x=var('x')
    curve1=ParametricCurve(x,f1,mx1,Mx1)
    curve2=ParametricCurve(x,f2,mx2,Mx2)
    return SurfaceBetweenParametricCurves(curve1,curve2)

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
    return BasicGeometricObjects.GraphOfACircle(center,radius)

def Rectangle(*args):
    """
    INPUT:

    - ``NW,SE`` - the North-West corner and South-East corner

    Alternatively, you can pass a bounding box as unique argument.
    """
    if len(args)==2:
        NW=args[0]
        SE=args[1]
    if len(args)==1:
        NW=args[0].NW()
        SE=args[0].SE()
    return BasicGeometricObjects.GraphOfARectangle(NW,SE)

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

        sage: from phystricks.BasicGeometricObjects import SingleAxe
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

        sage: grid=Grid()
        sage: grid.main_horizontal.parameters.color = "red"

    """
    def __init__(self,bb=None):
        if bb is None:
            bb=BasicGeometricObjects.BoundingBox()
        self.BB = bb
        self.options = BasicGeometricObjects.Options()
        self.separator_name="GRID"
        self.add_option({"Dx":1,"Dy":1})        # Default values, have to be integer.
        self.Dx = self.options.DicoOptions["Dx"]
        self.Dy = self.options.DicoOptions["Dy"]
        self.num_subX = 2
        self.num_subY = 2
        self.draw_border = False
        self.main_horizontal = Segment(Point(0,1),Point(1,1))
        self.main_horizontal.parameters.color="gray"
        self.main_horizontal.parameters.style = "solid"
        self.main_vertical = Segment(Point(0,1),Point(1,1))
        self.main_vertical.parameters.color="gray"
        self.main_vertical.parameters.style = "solid"
        self.sub_vertical = Segment(Point(0,1),Point(1,1))
        self.sub_vertical.parameters.color="gray"
        self.sub_vertical.parameters.style = "dotted"
        self.sub_horizontal = Segment(Point(0,1),Point(1,1))
        self.sub_horizontal.parameters.color="gray"
        self.sub_horizontal.parameters.style = "dotted"
        self.border = Segment(Point(0,1),Point(1,1))
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
    return BasicGeometricObjects.GraphOfAnAngle(A,O,B,r)

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

        sage: print Point(1,1)
        Point(1,1)
        sage: print Point(pi,sqrt(2))
        Point(pi,sqrt(2))
    
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
    return BasicGeometricObjects.GraphOfAPoint(x,y)

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

def SingleAxe(C,base,mx,Mx):
    """
    Return an axe.
    
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
    return BasicGeometricObjects.GraphOfASingleAxe(C,base,mx,Mx)

def Segment(A,B):
    return BasicGeometricObjects.GraphOfASegment(A,B)

def Text(P,text,hide=True):
    """
    A text.

    INPUT:

    - ``P`` - the point at which the center of the bounding box will lie.

    - ``text`` - the text.

    - ``hide`` - (default=True) When `True`, the background of the text is hidden by
                    a rectangle. The color and style of that rectangle can be customized,
                    see :class:`BasicGeometricObjects.GraphOfAText`

    """
    return BasicGeometricObjects.GraphOfAText(P,text,hide=hide)

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
        return BasicGeometricObjects.GeometricVectorField(fx,fy)
    return BasicGeometricObjects.GeometricVectorField(fx,fy).graph(xvalues,yvalues,draw_points)

def unify_point_name(s):
    r"""
    Internet s as the pstricks code of something and return a chain with
    all the points names changed to "Xaaaa", "Xaaab" etc.

    Practically, it changes the strings like "{abcd}" to "{Xaaaa}".

    When "{abcd}" is found, it also replace the occurences of "(abcd)".
    This is because the marks of points are given by example as
    '\\rput(abcd){\\rput(0;0){$-2$}}'

    This serves to build more robust doctests by providing strings in which
    we are sure that the names of the points are the first in the list.

    INPUT:

    - ``s`` - a string

    OUTPUT:
    string

    EXAMPLES:
    
    In the following example, the points name in the segment do not begin
    by "aaaa" because of the definition of P, or even because of other doctests executed before.
    (due to complex implementation, the names of the points are
    more or less unpredictable and can change)

    ::

        sage: P=Point(3,4)
        sage: S = Segment(Point(1,1),Point(2,2))
        sage: print S.pstricks_code()       # random
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){aaad}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,2.00000000000000){aaae}
        <BLANKLINE>
        \pstLineAB[linestyle=solid,linecolor=black]{aaad}{aaae}


    However, using the function unify_point_name, the returned string begins with "Xaaaa" ::

        sage: print unify_point_name(S.pstricks_code())
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaaa}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,2.00000000000000){Xaaab}
        <BLANKLINE>
        \pstLineAB[linestyle=solid,linecolor=black]{Xaaaa}{Xaaab}

    Notice that the presence of "X" is necessary in order to avoid
    conflicts when one of the points original name is one of the new points name as in the following example ::

        sage: s="{xxxx}{aaaa}{yyyy}"
        sage: print unify_point_name(s)
        {Xaaaa}{Xaaab}{Xaaac}

    Without the additional X,

    1. The first "xxxx" would be changed to "aaaa".
    2. When changing "aaaa" into "aaab", the first one
            would be changed too.

    ::

        sage: P=Point(-1,1)
        sage: P.put_mark(0.3,90,"$A$")
        sage: unify_point_name(P.mark.pstricks_code())
        '\\pstGeonode[](-1.00000000000000,1.30000000000000){Xaaaa}\n\\rput(Xaaaa){\\rput(0;0){$A$}}'
    """
    import re

    point_pattern=re.compile("({[a-zA-Z]{4,4}})")
    match = point_pattern.findall(s)

    rematch=[]
    for m in match:
        n=m[1:-1]       # I transform "{abcd}" into "abcd"
        if n not in rematch:
            rematch.append(n)

    names=BasicGeometricObjects.PointsNameList()
    for m in rematch:
        name=names.next()
        s=s.replace("{%s}"%m,"{X%s}"%name).replace("(%s)"%m,"(X%s)"%name)
    return s

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


import phystricks.BasicGeometricObjects as BasicGeometricObjects
import phystricks.main as main
