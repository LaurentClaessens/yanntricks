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

# copyright (c) Laurent Claessens, 2009-2016
# email: laurent@claessens-donadello.eu

# The documentation is compiled by
# sage -sh
# make html

from __future__ import division
from __future__ import unicode_literals

from sage.all import *

from Constructors import *
from Utilities import radian
from Utilities import degree
from MathStructures import AxesUnit
from Utilities import Intersection
from phystricks.ObjectGraph import Options

"""
A collection of tools for building LaTeX pictures with python.
"""

"""
TEST :

    The following piece of code testes my WrapperStr

    sage: x=var('x')
    sage: f(x)=x**2
    sage: f(3)
    9
    sage: f(x=3)
    9
"""

class WrapperStr(object):
    def __init__(self,fun):
        self.fun=fun
    def __call__(self,arg):
        return self.fun(str(arg))

var=WrapperStr(var)

import codecs
import math, sys, os

from phystricks.SmallComputations import *

# TODO : f=phyFunction(x**2+3*x-10), then  g=f/3 does not work.
# TODO : In figureHYeBZVj, the grid begins at negative numbers. Why ? (see smath available on  https://github.com/LaurentClaessens/smath)
# TODO : waving functions behaves badly when X and Y dilatations are different. See figureHYeBZVj

def no_symbol(*arg):
    for l in arg:
        try:
            for P in l:
                no_symbol(P)
        except TypeError:
            l.parameters.symbol=""

def get_equal_lengths_code(s1,s2,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
    from ObjectGraph import AddedObjects
    added1=AddedObjects()
    added2=AddedObjects()
    pspicts=make_psp_list(pspict,pspicts)
    for psp in pspicts :
        c1=s1.get_code(n=n,d=d,l=l,pspict=psp)
        c2=s2.get_code(n=n,d=d,l=l,pspict=psp)
        added1.append(psp,c1)
        added2.append(psp,c2)
    return added1,added2

def put_equal_lengths_code(s1,s2,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
    """
    Add the code for equal length between segments s1 and s2
    """
    pspicts=make_psp_list(pspict,pspicts)
    for psp in pspicts :
        added=get_equal_lengths_code(s1,s2,n,d,l,angle,pspict)
        c1=added[0]
        c2=added[1]
        s1.added_objects.fusion( c1 )
        s2.added_objects.fusion( c2 )

def GenericFigure(nom,script_filename=None):
    """
    This function returns a figure with some default values. It creates coherent label, file name and prints the lines to be appended in the LaTeX file to include the figure.
    """
    if not script_filename:
        script_filename=nom
    caption = "\CaptionFig"+nom     # This is also hard-coded in the function main.figure.LaTeX_lines
    label = "LabelFig"+nom          # The string "LabelFig" is hard-coded in the function main.figure.LaTeX_lines
    filename = "Fig_"+nom+".pstricks"

    from Figure import Figure
    fig=Figure(caption,label,filename,script_filename)
    fig.figure_mother=fig   # I'm not sure that this line is useful.
    print fig.LaTeX_lines()
    return fig

def SinglePicture(name,script_filename=None):
    """ Return the tuple of pspicture and figure that one needs in 90% of the cases. """
    fig = GenericFigure(name,script_filename)
    pspict=fig.new_pspicture(name)
    fig.child_pspictures.append(pspict)
    return pspict,fig

def MultiplePictures(name,n=None,pspicts=None,script_filename=None):
    r"""
    Return a figure with multiple subfigures. 

    INPUT:

    - `name` - the name of the figure.

    - `n` (optional)  - the number of subfigures.

    -  `pspicts` (optional) : a list of pspictures to be appended.

    You can either give `n` or `pspicts`. In the first case, `n` new pspictures are created;
    in the second case, the given pspictures are attached to the multiple pictures.

    You have to think about naming the subfigures.

    EXAMPLE::

        sage: from phystricks import *
        sage: pspicts,fig = MultiplePictures("MyName",3)
        The result is on figure \ref{LabelFigMyName}.
        \newcommand{\CaptionFigMyName}{<+Type your caption here+>}
        \input{Fig_MyName.pstricks}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName0}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName1}
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName2}
        sage: pspicts[0].mother.caption="My first subfigure"
        sage: pspicts[1].mother.caption="My second subfigure"
        sage: pspicts[2].mother.caption="My third subfigure"

    Notice that a caption is related to a figure or a subfigure, not to a pspicture.

    See also :class:`subfigure`
    """
    if not script_filename:
        script_filename=name
    fig = GenericFigure(name,script_filename)


    if n is not None :
        pspictures_list=[]
        for i in range(n):
            subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
            picture=subfigure.new_pspicture(name+"pspict"+str(i))
            picture.figure_mother=fig
            fig.child_pspictures.append(picture)
            pspictures_list.append(picture)

    if pspicts is not None :
        pspictures_list=[]
        n=len(pspicts)
        for i,psp in enumerate(pspicts) :
            subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
            subfigure.new_pspicture(pspict=psp)
            psp.figure_mother=fig
            fig.child_pspictures.append(psp)
            pspictures_list.append(psp)

    return pspictures_list,fig

def IndependentPictures(name,n):
    """
    Return a tuple of a list of 'n' pspictures and 'n' figures.
    """
    pspicts=[]
    figs=[]
    from Utilities import latinize
    for i in range(0,n):
        # One has to latinize to be in grade of making subfigures :
        # if not one gets things like \newcommand{\CaptionFigFoo1}{blahblah}  which does not work in LaTeX because of the "1"
        pspict,fig = SinglePicture(name+"oo"+Utilities.latinize(str(i)))
        pspicts.append(pspict)
        figs.append(fig)
    return pspicts,figs

def SubsetFigures(old_pspicts,old_fig,l):
    r"""
    Return a subset of a figure with subfigures.

    If you've prepared a figure with 10 subfigure but at the end of the day,
    you change your mind and decide to remove the subfigure 3 and 8
    
    EXAMPLE::

    
    .. literalinclude:: phystricksSubSetMultiple.py

    .. image:: Picture_FIGLabelFigSubSetMultiplessLabelSubFigSubSetMultiple2PICTSubSetMultiplepspict2-for_eps.png
    .. image:: Picture_FIGLabelFigSubSetMultiplessLabelSubFigSubSetMultiple3PICTSubSetMultiplepspict3-for_eps.png
    .. image:: Picture_FIGLabelFigSubSetMultiplessLabelSubFigSubSetMultiple5PICTSubSetMultiplepspict5-for_eps.png

    I'm not sure that it is still possible to use the old fig.
    """
    name=old_fig.name
    script_filename=old_fig.script_filename
    fig = GenericFigure(name,script_filename)
    pspict=[]
    for i in l:
        subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
        subfigure._add_pspicture(old_pspicts[i])
        old_pspicts[i].figure_mother=fig
        pspict.append(old_pspicts[i])
    return pspict,fig

def ImplicitCurve(f,xrange,yrange,plot_points=100):
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

    sage: from phystricks import *
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
    return BasicGeometricObjects.GeometricImplicitCurve(f).graph(xrange,yrange,plot_points=100)

class ObliqueProjection(object):
    def __init__(self,alpha,k):
        """
        This is the oblique projection of angle `alpha` and scale factor `k`.

        `alpha` is given in degree. It is immediately converted in order to have positive number. If you give -45, it will be converted to 315
        """
        from MathStructures import AngleMeasure
        self.k=k
        if self.k>=1 :
            print "Are you sure that you want such a scale factor : ",float(self.k)
        self.alpha=alpha
        a=AngleMeasure(value_degree=self.alpha).positive()
        self.alpha=a.degree
        self.theta=radian(self.alpha)
        self.kc=self.k*cos(self.theta)
        self.ks=self.k*sin(self.theta)
    def point(self,x,y,z):
        return Point(x+z*self.kc,y+z*self.ks)
    def cuboid(self,P,a,b,c):
        """
        `P` -- a tupe (x,y) that gives the lower left point.

        `a,b,c` the size
        """
        return Cuboid(self,P,a,b,c)

def Text(P,text,hide=True):

    """
    A text.

    INPUT:

    - ``P`` - the point at which the center of the bounding box will lie.

    - ``text`` - the text.

    - ``hide`` - (default=True) When `True`, the background of the text is hidden by
                    a rectangle. The color and style of that rectangle can be customized,
                    see :class:`BasicGeometricObjects.TextGraph`

    """
    return BasicGeometricObjects.TextGraph(P,text,hide=hide)

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

        sage: from phystricks import *
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
    Interpret `s` as the pstricks code of something and return a chain with
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

        sage: from phystricks import *
        sage: P=Point(3,4)
        sage: S = Segment(Point(1,1),Point(2,2))

    However, using the function unify_point_name, the returned string begins with "Xaaaa" ::

    Notice that the presence of "X" is necessary in order to avoid
    conflicts when one of the points original name is one of the new points name as in the following example ::

        sage: s="{xxxx}{aaaa}{yyyy}"
        sage: print unify_point_name(s)
        {Xaaaa}{Xaaab}{Xaaac}

    Without the additional X,

    1. The first "xxxx" would be changed to "aaaa".
    2. When changing "aaaa" into "aaab", the first one would be changed too.

    """
    import re

    point_pattern=re.compile("({[a-zA-Z]{4,4}})")
    match = point_pattern.findall(s)

    rematch=[]
    for m in match:
        n=m[1:-1]       # I transform "{abcd}" into "abcd"
        if n not in rematch:
            rematch.append(n)

    from PointGraph import PointsNameList
    names=PointGraph.PointsNameList()
    for m in rematch:
        name=names.next()
        s=s.replace("{%s}"%m,"{X%s}"%name).replace("(%s)"%m,"(X%s)"%name)
    return s

import GlobalVariables
import phystricks.BasicGeometricObjects as BasicGeometricObjects
import phystricks.main as main
