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
# email: laurent@claessens-donadello.eu

from __future__ import division
from __future__ import unicode_literals

from sage.all import *
from phystricks import *
from phystricks.Constructors import *

from phystricks.ObjectGraph import ObjectGraph

var=WrapperStr(var)

def genericBracketAttributeToLanguage(attr,language):
    if language=="tikz":
        if attr=="plotpoints":
            return "samples"
        if attr=="linewidth":
            return "line width"
    return attr

# TODO : to fill portion of circle should be as easy as:
#    CerB=Cer.graph(alpha,alpha+90)
#    CerB.parameters.filled()
#    CerB.parameters.fill.color="blue"
# See the picture RouletteACaVVA

def OptionsStyleLigne():
    return ["linecolor","linestyle"]

from phystricks.Parameters import Parameters
from phystricks.PointGraph import PointGraph

class GeometricImplicitCurve(object):
    """
    Describe a curve given by an implicit equation.

    INPUT:

    - ``f`` -- a function of two variables or equation in two variables

    End users should not use this class but use the constrcutor :func:`ImplicitCurve`.

    EXAMPLES::

        sage: from phystricks.BasicGeometricObjects import *
        sage: x,y=var('x,y')
        sage: f(x,y)=x**2+1/x
        sage: F=GeometricImplicitCurve(f(x,y)==2)
        sage: G=GeometricImplicitCurve(x+y==2)   

    """
    def __init__(self,f):
        self.f=f
        self.parameters=Parameters()
        from sage.symbolic.expression import is_SymbolicEquation
        if is_SymbolicEquation(f):
            if f.operator() != operator.eq:
                raise ValueError, "input to implicit plot must be function or equation"
            self.f = f.lhs() - f.rhs()          # At this point self.f is the expression to be equated to zero.
    def graph(self,xrange,yrange,plot_points=100):
        """
        Return the graph corresponding to the implicit curve.

        INPUT:

        - ``xrange`` - the X-range on which the curve will be plotted.

        - ``yrange`` - the Y-range on which the curve will be plotted.

        EXAMPLE ::
    
            sage: from phystricks.BasicGeometricObjects import *
            sage: x,y=var('x,y')
            sage: F=GeometricImplicitCurve(x-y==3)
            sage: graph=F.graph((x,-3,3),(y,-2,2))
            sage: print graph.bounding_box()
            <BoundingBox xmin=1.0,xmax=3.0; ymin=-2.0,ymax=0.0>

        """
        gr = ImplicitCurveGraph(self,xrange,yrange,plot_points)
        gr.parameters=self.parameters.copy()
        return gr
    def __str__(self):
        """
        Return string representation of this implicit curve

        EXAMPLE::

            sage: from phystricks.BasicGeometricObjects import *
            sage: x,y=var('x,y')
            sage: f(x,y)=x**2+1/x
            sage: print GeometricImplicitCurve(f(x,y)==2)
            <Implicit curve of equation x^2 + 1/x - 2 == 0>
            sage: print GeometricImplicitCurve(x+y==7)   
            <Implicit curve of equation x + y - 7 == 0>
        """
        return "<Implicit curve of equation %s == 0>"%repr(self.f)

class ImplicitCurveGraph(ObjectGraph,GeometricImplicitCurve):
    r"""
    Describe the graph of an implicit curve.

    INPUT:

    - ``implicit_curve`` - the implicit curve to be considered.

    - ``xrange``,``yrange`` - the range on which we want to plot.
    

    OPTIONAL INPUT:

    - ``plot_points``  -- integer (default: 100); number of points to plot in each direction of the grid.

    ATTRIBUTES:

    - ``self.path`` this is a list of lists of points. Each list correspond to a path
                    in the sense of matplotlib. Notice that here the points are given as
                    instances of Point; not as list [x,y] as matplotlib does.
    
    EXAMPLES::

            sage: from phystricks.BasicGeometricObjects import *
            sage: x,y=var('x,y')
            sage: implicit_curve=GeometricImplicitCurve(x**2+x==3)
            sage: F=ImplicitCurveGraph(implicit_curve,(x,-1,1),(y,-3,2))

    NOTES:

    The get_minmax_data is contributed by the Sage's community here :
    """
    def __init__(self,implicit_curve,xrange,yrange,plot_points=300):
        ObjectGraph.__init__(self,implicit_curve)
        GeometricImplicitCurve.__init__(self,implicit_curve.f)
        self.implicit_curve=implicit_curve
        self.implicit_plot=implicit_plot(self.f,xrange,yrange)
        self.xrange=xrange
        self.yrange=yrange
        self.plot_points=plot_points
        self.paths=get_paths_from_implicit_plot(self.implicit_plot)
        self.parameters.color="blue"
    def get_minmax_data(self,decimals=3,dict=True):
        """
        Return a dictionary whose keys give the xmin, xmax, ymin, and ymax
        data for this graphic.

        Since the results come from the lazy_attribute function _get_minmax_data, changing the number of points
        between two call will not change the result.

        EXAMPLES::

            sage: from phystricks import *
            sage: x,y=var('x,y')
            sage: F=ImplicitCurve(x**2+y**2==sqrt(2),(x,-5,5),(y,-4,4),plot_points=300)
            sage: F.get_minmax_data()   # random
            {'xmin': -1.1890000000000001, 'ymin': -1.1879999999999999, 'ymax': 1.1879999999999999, 'xmax': 1.1890000000000001}
            sage: F.plot_points=10
            sage: F.get_minmax_data()       # random
            {'xmin': -1.189, 'ymin': -1.188, 'ymax': 1.188, 'xmax': 1.189}

        """
        tot_points=[]
        for path in self.paths :
            tot_points.extend(path)
        xx=[P.x for P in tot_points]
        yy=[P.y for P in tot_points]
        xmin=min(xx)
        xmax=max(xx)
        ymin=min(yy)
        ymax=max(yy)
        if dict:
            return MyMinMax({str('xmin'):xmin, str('xmax'):xmax,str('ymin'):ymin, str('ymax'):ymax},decimals=decimals)
        else:
            return around(xmin,decimals),around(xmax,decimals),around(ymin,decimals),around(ymas,decimals)
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
        Return the bounding box of the implicit curve.

        This is NOT the bounding box got that one could expect
        using Sage's plotting system
        implicit_plot(f,xrange,yrange).get_minmax_data()

        Instead the bounding box returned here only contains the points that
        are actually plotted. In the following example, we know that the ymax
        has to be half the sqrt of the radius (and not the 5 given in yrange).

        EXAMPLES::

            sage: from phystricks import *
            sage: x,y=var('x,y')
            sage: f=x**2+2*y**2
            sage: G=ImplicitCurve(f==sqrt(2),(x,-5,5),(y,-5,5),plot_points=200)
            sage: print G.bounding_box()
            <BoundingBox xmin=-1.188,xmax=1.188; ymin=-0.841,ymax=0.841>
        """
        bb = BoundingBox( Point(self.xmin(),self.ymin()),Point(self.xmax(),self.ymax())  )
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        """
        Return the pstrick code of the implicit curve.
        """
        code=[]
        for path in self.paths:
            curve=InterpolationCurve(path,context_object=self)
            curve.parameters=self.parameters.copy()
            code.append(curve.latex_code(language=language,pspict=pspict))
        return "\n".join(code)

class TextGraph(ObjectGraph):
    """
    You can customize the background via the object `self.rectangle`
    """
    def __init__(self,P,text,hide=True):
        ObjectGraph.__init__(self,self)
        self.P=P
        self.text=text
        self.mark=Mark(self,0,0,self.text)
        self.hide=hide

        self.rectangle=Rectangle(Point(0,0),Point(1,1))     # This is fake; just to have an object to act on.
        self.rectangle.parameters.filled()
        self.rectangle.parameters.fill.color="white"
        self.rectangle.parameters.style="none"
    def mark_point(self,pspict=None):
        return self.P
    def math_bounding_box(self,pspict=None):
        # a text has no math_bounding_box because the axes do not want to fit them.
        #return self.mark.math_bounding_box(pspict)         # June 1, 2015
        return BoundingBox()
    def bounding_box(self,pspict=None):
        return self.mark.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        a=[]
        rect=Rectangle(self.mark.bounding_box(pspict))
        rect.parameters=self.rectangle.parameters
        if self.hide:
            a.append(rect.latex_code(language=language,pspict=pspict))
        a.append(self.mark.latex_code(language=language,pspict=pspict))
        return "\n".join(a)

class GeometricVectorField(object):
    """
    Describe a vector field

    INPUT:
    
    - ``f`` - a tupe of function

    EXAMPLES::


        sage: from phystricks.BasicGeometricObjects import *
        sage: x,y=var('x,y')
        sage: f1=phyFunction(x**2)
        sage: F = GeometricVectorField( f1,cos(x*y) )
        sage: print F(3,pi/3)
        <vector I=<Point(3,1/3*pi)> F=<Point(12,1/3*pi - 1)>>

    """
    def __init__(self,fx,fy):
        x,y=var('x,y')
        fx = EnsurephyFunction(fx)
        fy = EnsurephyFunction(fy)
        self.fx=symbolic_expression(fx.sage).function(x,y)
        self.fy=symbolic_expression(fy.sage).function(x,y)
        #g=[fx,fy]
        #for i in [0,1]:
        #    if isinstance(g[i],phyFunction):
        #        g[i]=g[i].sage
        #self.fx=g[0]
        #self.fy=g[1]
        self.vector_field=self
    def divergence(self):
        """
        return the divergence of the vector field.

        OUTPUT:

        a two-variable function

        EXAMPLES::

            sage: from phystricks.BasicGeometricObjects import *
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
        x,y=var('x,y')
        formula = self.fx.diff(x)+self.fy.diff(y)
        divergence=symbolic_expression(formula).function(x,y)
        return divergence
    def graph(self,xvalues=None,yvalues=None,draw_points=None):
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

            sage: from phystricks.BasicGeometricObjects import *
            sage: x,y=var('x,y')
            sage: F=VectorField(x,y).graph(xvalues=(x,-2,2,3),yvalues=(y,-10,10,3),draw_points=[Point(100,100)])
            sage: print F.draw_points[0]
            <Point(100,100)>
            sage: print len(F.draw_points)
            10
        """
        if draw_points is None:
            draw_points=[]
        if xvalues is not None:
            mx=xvalues[1]
            Mx=xvalues[2]
            nx=xvalues[3]
            my=yvalues[1]
            My=yvalues[2]
            ny=yvalues[3]
            from numpy import linspace
            pos_x=linspace(mx,Mx,nx)
            pos_y=linspace(my,numerical_approx(My),ny)
            for xx in pos_x:
                for yy in pos_y:
                    draw_points.append(Point(xx,yy))
        return VectorFieldGraph(self,draw_points=draw_points)
    def __call__(self,a,b=None):
        """
        return the affine vector at point (a,b).

        INPUT:

        - ``a,b`` - numbers.

        OUTPUT:
        an affine vector based on (a,b).

        EXAMPLES::

            sage: from phystricks import *
            sage: x,y=var('x,y')
            sage: F=VectorField(x**2,y**3)
            sage: print F(1,2)
            <vector I=<Point(1,2)> F=<Point(2,10)>>

            sage: P=Point(3,4)
            sage: print F(P)
            <vector I=<Point(3,4)> F=<Point(12,68)>>

        """
        if b is not None :
            P=Point(a,b)
        else :
            P=a
        vx=self.fx(x=P.x,y=P.y)
        vy=self.fy(x=P.x,y=P.y)
        return AffineVector(P,Point(P.x+vx,P.y+vy))

class VectorFieldGraph(ObjectGraph,GeometricVectorField):
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
    def __init__(self,F,draw_points):
        ObjectGraph.__init__(self,F)
        GeometricVectorField.__init__(self,F.fx,F.fy)
        self.vector_field=F
        self.F=self.vector_field
        self.draw_points=draw_points

    @lazy_attribute
    def draw_vectors(self):
        """
        the list of vectors to be drawn
        """
        l=[]
        return  [self(P) for P in self.draw_points] 

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

            sage: from phystricks import *
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
        for P in self.draw_points :
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
        for P in self.draw_points :
            if P.y not in l:
                l.append(P.y)
        l.sort()
        return l

    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        bb = BoundingBox()
        for v in self.draw_vectors:
            bb.append(v,pspict)
        return bb
    def latex_code(self,language=None,pspict=None):
        code=[]
        for v in self.draw_vectors:
            v.parameters=self.parameters.copy()
            code.append(v.latex_code(language=language,pspict=pspict))
        return "\n".join(code)

def get_paths_from_plot(p):
    """
    return the paths (in the sense of matplotlib) contained in the plot object p.

    The paths here are paths in the sense of matplotlib; the elements are vertices.
    Not to be confused with get_paths_from_implicit_plot in which the basic elements
    are points.

    INPUT:
    - ``p`` - a plot object

    EXAMPLES:
    sage: from phystricks import *
    sage: from phystricks.BasicGeometricObjects import *
    sage: x,y=var('x,y')
    sage: F=implicit_plot(x**2+y**2==2,(x,-5,5),(y,-5,5))
    sage: g=get_paths_from_plot(F)
    sage: print type(g[0])
    <class 'matplotlib.path.Path'>

    NOTE:
    The first version of the function is due to the DSM here:
    http://ask.sagemath.org/question/359/get_minmax_data-on-implicit_plot
    """
    import matplotlib.path
    m = p.matplotlib()
    sp = m.get_children()[1]
    ll=[]
    for c in sp.get_children():
        # not sure if I need to test for both or not? don't understand
        # matplotlib internals well enough to know if every Line2D
        # will be in some LineCollection and so this is pure duplication (probably)
        if isinstance(c, matplotlib.lines.Line2D):
            ll.append(c.get_path())
        elif isinstance(c, matplotlib.collections.LineCollection):
            for path in c.get_paths():
                ll.append(path)
    return ll

def get_paths_from_implicit_plot(p):
    """
    Return a list of list of points from an implicit plot.

    Each list correspond to a path.

    INPUT:

    - ``p`` an implicit plot.

    OUTPUT:

    A list of lists of points. Each list corresponds to a path (see matplotlib), but the components are converted into points in the sens of phystricks (instead of matplotlib's vertices).

    EXAMPLES:

    The length of the list can be quite long::

        sage: from phystricks import *
        sage: from phystricks.BasicGeometricObjects import *
        sage: x,y=var('x,y')
        sage: F=implicit_plot(x**2+y**2==2,(x,-5,5),(y,-5,5))
        sage: len(get_paths_from_implicit_plot(F)[0])
        169

    When you have more than one connected component, you see it ::

        sage: F=implicit_plot(x**2-y**2==2,(x,-5,5),(y,-5,5))
        sage: paths=get_paths_from_implicit_plot(F)
        sage: len(paths)
        4
        sage: type(paths[0][1])
        <class 'phystricks.BasicGeometricObjects.PointGraph'>
        sage: print paths[0][3]
        <Point(4.87405534614323,-4.6644295302013425)>
        sage: print paths[1][3]
        <Point(4.87405534614323,-4.6644295302013425)>
        sage: print paths[2][3]
        <Point(4.87405534614323,-4.6644295302013425)>
        sage: print paths[3][3]
        <Point(4.87405534614323,-4.6644295302013425)>
    """
    l=[]
    for path in get_paths_from_plot(p):
        pp=[]
        for vertice in path.vertices:
            pp.append(Point(vertice[0],vertice[1]))
        l.append(pp)
    return l

def first_bracket(text):
    """
    return the first bracket in the string 'text'  
    """
    if "[" not in text:
        return ""
    a=text.find("[")
    b=text[a:].find("]")+1+a
    bracket=text[a:b]
    return bracket

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
    t1=text.replace("\draw","").replace(";","")
    bracket=first_bracket(t1)
    t2=t1.replace(bracket,"")
    t3=t2.strip()
    if "coordinates" in t3 :
        return t3
    else :
        answer=t3.replace("plot","plot "+bracket)
    return answer

class HistogramBox(ObjectGraph):
    """
    describes a box in an histogram.
    """
    def __init__(self,a,b,n,histo):
        """
        It is given by the initial value, the final value and the "surrounding" histogram
        """
        ObjectGraph.__init__(self,self)
        self.d_xmin=a
        self.d_xmax=b
        self.n=n
        self.histo=histo
        self.size=self.d_xmax-self.d_xmin
        self.th_height=self.n/self.size
        self.length=None
        self.height=None
    @lazy_attribute
    def rectangle(self):
        xmin=self.histo.xscale*self.d_xmin
        xmax=self.histo.xscale*self.d_xmax
        ymin=0
        ymax=self.histo.yscale*self.th_height
        rect=Rectangle(mx=xmin,Mx=xmax,my=ymin,My=ymax)
        rect.parameters=self.parameters.copy()
        return rect
    def bounding_box(self,pspict=None):
        return self.rectangle.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        # The put_mark can only be done here (and not in self.rectangle()) because one needs the pspict.
        return self.rectangle.latex_code(language=language,pspict=pspict)

class HistographGraph(ObjectGraph):
    """
    An histogram is given by a list of tuple '(a,b,n)' where 'a' and 'b' are the extremal values of the box and 'n' is the number of elements in the box.
    """
    def __init__(self,tuple_box_list):
        ObjectGraph.__init__(self,self)
        self.tuple_box_list=tuple_box_list
        self.box_list=[]
        for t in self.tuple_box_list:
            self.box_list.append(HistogramBox(t[0],t[1],t[2],self))
        self.n=sum( [b.n for b in self.box_list] )
        self.length=12  # Visual length (in centimeter) of the histogram
        self.height=6  # Visual height (in centimeter) of the histogram
        self.d_xmin=min([b.d_xmin for b in self.box_list])       # min and max of the data
        self.d_xmax=max([b.d_xmax for b in self.box_list])
        self.d_ymax=max([b.n for b in self.box_list])       # max of the data ordinate.
        self.xsize=self.d_xmax-self.d_xmin
        self.ysize=self.d_ymax              # d_ymin is zero (implicitly)
        self.legende=None
        # TODO : For sure one can sort it easier.
        # The problem is that if several differences x.th_height-y.th_height are small, 
        # int(...) always returns 1 (or -1), so that the sorting gets wrong.
        self.xscale=self.length/self.xsize
        classement = self.box_list[:]
        facteur=10
        for x in classement :
            for y in classement :
                try :
                    facteur=max(facteur,10/(x.th_height-y.th_height))
                except ZeroDivisionError :
                    pass
        classement.sort(lambda x,y:int((x.th_height-y.th_height)*facteur))
        self.yscale=self.height/classement[-1].th_height
        self.height/self.ysize
    def IF_x(self):
        """
        return the list of I and F points without repetitions.

        This is the list of "physical values" (i.e. the ones of the histogram), not the ones
        of the pspict coordinates.
        """
        x_list=[]
        for b in self.box_list:
            if b.d_xmin not in x_list :
                x_list.append(b.d_xmin)
            if b.d_xmax not in x_list :
                x_list.append(b.d_xmax)
        return x_list
    def specific_action_on_pspict(self,pspict):
        pspict.axes.no_graduation()
        pspict.axes.do_mx_enlarge=False
        pspict.axes.do_my_enlarge=False
        if self.legende :
            pspict.axes.single_axeX.put_mark(0.5,-90,self.legende,pspict=pspict,position="N")
        else :
            print "Are you sure that you don't want a legend on your histogram ?"
        # The construction of the list 'values' is created in such a way not to have '1.0' instead of '1'.
        # By the way, you have to know that the values in numpy.arange are type numpy.float64
        import numpy
        un=numpy.arange(self.d_xmin,self.d_xmax+0.1,step=int(self.xsize/10))
        values=[]
        for xx in un :
            if int(xx)==xx:
                values.append(int(xx))
            else :
                values.append(xx)
        for xx in values:
            P=Point(xx*self.xscale,0)
            P.parameters.symbol="|"
            P.put_mark(0.2,-90,str(xx),pspict=pspict,position="N")    # see 71011299 before to change this 0.2
            pspict.DrawGraphs(P)
        for box in self.box_list :
            P=box.rectangle.segment_N.mark_point()
            P.put_mark(0.2,90,"$"+str(box.n)+"$",pspict=pspict,position="S")
            P.parameters.symbol=""
            pspict.DrawGraphs(P)
    def bounding_box(self,pspict):
        bb=BoundingBox()
        for b in self.box_list:
            bb.append(b,pspict)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict=pspict)
    def latex_code(self,language=None,pspict=None):
        a=["% Histogram"]
        a.extend([x.latex_code(language=language,pspict=pspict) for x in self.box_list])
        return "\n".join(a)

class MoustacheGraph(ObjectGraph):
    def __init__(self,minimum,Q1,M,Q3,maximum,h,delta_y=0):
        ObjectGraph.__init__(self,self)
        self.Q1=Q1
        self.Q3=Q3
        self.M=M
        self.h=h
        self.delta_y=delta_y
        self.minimum=minimum
        self.maximum=maximum
    def specific_action_on_pspict(self,pspict):
        my=self.delta_y-self.h/2
        My=self.delta_y+self.h/2
        h1=Segment(Point(self.minimum,my),Point(self.minimum,My))
        s1=Segment(Point(self.minimum,self.delta_y),Point(self.Q1,self.delta_y))
        box=Polygon( Point(self.Q1,my),Point(self.Q3,my),Point(self.Q3,My),Point(self.Q1,My) )
        med=Segment(Point(self.M,my),Point(self.M,My))
        med.parameters.color="red"
        s2=Segment(Point(self.Q3,self.delta_y),Point(self.maximum,self.delta_y))
        h2=Segment(Point(self.maximum,my),Point(self.maximum,My))
        pspict.DrawGraphs(h1,h2,s1,box,med,s2)
    def mark_point(self,pspict=None):
        return Point(self.maximum,self.delta_y)
    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict):
        bb=BoundingBox()
        bb.addX(self.minimum)
        bb.addX(self.maximum)
        bb.addY(self.delta_y-self.h/2)
        bb.addY(self.delta_y+self.h/2)
        return bb
    def latex_code(self,language=None,pspict=None):
        return ""

class BoxDiagramGraph(ObjectGraph):
    def __init__(self,values,h,delta_y=0):
        ObjectGraph.__init__(self,self)

        import numpy
        from scipy.stats.mstats import mquantiles

        ms=mquantiles(values)
        self.average=numpy.mean(values)
        self.q1=ms[0]
        self.median=ms[1]
        self.q3=ms[2]
        self.minimum=min(values)
        self.maximum=max(values)
        self.h=h
        self.delta_y=delta_y
    def specific_action_on_pspict(self,pspict):
        my=self.delta_y-self.h/2
        My=self.delta_y+self.h/2
        h1=Segment(Point(self.minimum,my),Point(self.minimum,My))
        s1=Segment(Point(self.minimum,self.delta_y),Point(self.q1,self.delta_y))
        box=Polygon( Point(self.q1,my),Point(self.q3,my),Point(self.q3,My),Point(self.q1,My) )
        med=Segment(Point(self.median,my),Point(self.median,My))
        med.parameters.color="red"

        #average=Segment(Point(self.average,my),Point(self.average,My))
        ave=Point( self.average,(my+My)/2 )
        ave.parameters.color="blue"

        s2=Segment(Point(self.q3,self.delta_y),Point(self.maximum,self.delta_y))
        h2=Segment(Point(self.maximum,my),Point(self.maximum,My))
        pspict.DrawGraphs(h1,h2,s1,box,med,s2,ave)
    def mark_point(self,pspict=None):
        return Point(self.maximum,self.delta_y)
    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict):
        bb=BoundingBox()
        bb.addX(self.minimum)
        bb.addX(self.maximum)
        bb.addY(self.delta_y-self.h/2)
        bb.addY(self.delta_y+self.h/2)
        return bb
    def latex_code(self,language=None,pspict=None):
        return ""

class BarDiagramGraph(object):
    def __init__(self,X,Y):
        self.X=X
        self.Y=Y
        self.linewidth=1    # width of the lines (in centimetrs)
        self.numbering=True
        self.numbering_decimals=2

        # Definition of the default bars to be drawn.
        self.lines_list=[]
        for i,x in enumerate(self.X):
            y=self.Y[i]
            l=Segment(Point(x,0),Point(x,y)  )
            l.parameters.color="blue"
            l.parameters.add_option("linewidth","{}cm".format(self.linewidth))
            self.lines_list.append(l)
    def numbering_marks(self,pspict):
        nb=[]
        if self.numbering:
            for i,h in enumerate(self.Y):
                P=Point(self.X[i],h)
                P.parameters.symbol=""
                P.put_mark(0.2,90,"\({{:.{}f}}\)".format(self.numbering_decimals).format(h),pspict=pspict,position="S")
                nb.append(P)
        return nb
    def action_on_pspict(self,pspict):
        for P in self.numbering_marks(pspict):
            pspict.DrawGraphs(P)
        for l in self.lines_list:
            l.parameters.other_options["linewidth"]="{}cm".format(self.linewidth)
            pspict.DrawGraphs(l)
        for P in self.numbering_marks(pspict):
            pspict.DrawGraphs(P)
    def math_bounding_box(self,pspict):
        bb=BoundingBox()
        for l in self.lines_list:
            bb.append(l,pspict)
        return bb
    def bounding_box(self,pspict):
        bb=self.math_bounding_box(pspict)
        for P in self.numbering_marks(pspict):
            bb.append(P.mark,pspict)
        return bb
    def latex_code(self,language=None,pspict=None):
        return ""

import phystricks.main as main
import phystricks.SmallComputations as SmallComputations
