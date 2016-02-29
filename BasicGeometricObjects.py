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

"""
Each of them have the methods for basic geometric manipulations: rotations, dilatations, tangent vector, etc.
"""

from __future__ import division
from __future__ import unicode_literals

from sage.all import *
from phystricks import *
from phystricks.Constructors import *


var=WrapperStr(var)

def SubstitutionMathPsTricks(fx):
    DeprecationWarning
    listeSubst = []
    listeSubst.append(["**","^"])
    listeSubst.append(["math.exp","2.718281828459045^"])
    listeSubst.append(["e^","2.718281828459045^"])
    for i in range(1,10):   
        listeSubst.append(["math.log"+str(i),str(0.43429448190325*math.log(i))+"*log"])
    listeSubst.append(["math.log","2.302585092994046*log"])     # because \psplot[]{1}{5}{log(x)} draws the logarithm in basis 10.
    listeSubst.append(["log","2.302585092994046*log"])  
    # Pour rappel, la formule est log_b(x)=log_a(x)/log_a(b)
    listeSubst.append(["math.pi","3.141592653589793"])
    listeSubst.append(["pi","3.141516"])
    listeSubst.append(["math.cosh","COSH"])
    listeSubst.append(["math.tan","TAN"])
    listeSubst.append(["math.sinh","SINH"])
    listeSubst.append(["math.sinc","SINC"])
    listeSubst.append(["arccos","acos"])        # See the documentation of pst-math package
    listeSubst.append(["arcsin","asin"])
    listeSubst.append(["arctan","atan"])
    listeSubst.append(["math.",""])
    a = fx
    for s in listeSubst :
        a = a.replace(s[0],s[1])
    return a

from phystricks.ObjectGraph import Options

class Axes(object):
    """
    Describe a system of axes (two axes).

    By default they are orthogonal.
    """
    def __init__(self,C,bb,pspict=None):
        # if a pspicture is passed, these axes will be considered as the default axes system of `pspict`.
        # This has an influence in the computation of the bounding box.
        self.C = C                      
        self.BB = bb.copy()
        self.pspict=pspict
        self.options = Options()
        self.Dx = 1
        self.Dy = 1
        self.arrows = "->"
        self.separator_name="AXES"
        self.graduation=True
        self.numbering=True
        # Since the size of the axe is given in multiple of self.base,
        # one cannot give mx=-1000 as "minimal value".
        self.single_axeX=SingleAxe(self.C,Vector(1,0),0,0,pspict=self.pspict)
        self.single_axeX.mark_origin=False
        self.single_axeX.axes_unit=AxesUnit(1,"")
        self.draw_single_axeX=True
        self.single_axeY=SingleAxe(self.C,Vector(0,1),0,0,pspict=self.pspict)
        self.single_axeY.mark_origin=False
        self.single_axeY.axes_unit=AxesUnit(1,"")
        self.single_axeY.mark_angle=180
        self.draw_single_axeY=True
        self.single_axeX.Dx=self.Dx
        self.single_axeY.Dx=self.Dy
        self.already_enlarged=False
        self.enlarge_size=0.5
        self.do_enlarge=True
        self.do_mx_enlarge=True
        self.do_my_enlarge=True
        self.do_Mx_enlarge=True
        self.do_My_enlarge=True
    def enlarge_a_little(self,l,pspict):
        if self.already_enlarged :
            raise ValueError,"I'm already enlarged"
        self.already_enlarged=True
        mx,Mx=self.single_axeX.enlarge_a_little(l,pspict=pspict)
        if self.do_mx_enlarge:
            self.single_axeX.mx=mx
        if self.do_Mx_enlarge :
            self.single_axeX.Mx=Mx
        my,My=self.single_axeY.enlarge_a_little(l,pspict=pspict)
        if self.do_my_enlarge :
            self.single_axeY.mx=my
        if self.do_My_enlarge :
            self.single_axeY.Mx=My

    def add_bounding_box(self,BB,pspict):
        """
        Modify the mx and Mx of each single axes X and Y in order to fit the given BB.

        This is only supposed to work with automatic axes because if assumes that these are
        vertical and horizontal.
        """
        axeX=self.single_axeX
        axeY=self.single_axeY
        axeX.mx=min((BB.xmin-axeX.C.x)/axeX.base.F.x,axeX.mx)
        axeX.Mx=max((BB.xmax-axeX.C.x)/axeX.base.F.x,axeX.Mx)

        axeY.mx=min((BB.ymin-axeY.C.y)/axeY.base.F.y,axeY.mx)
        axeY.Mx=max((BB.ymax-axeY.C.y)/axeY.base.F.y,axeY.Mx)
    def add_option(self,opt):
        self.options.add_option(opt)
    def no_graduation(self):
        self.single_axeX.no_graduation()
        self.single_axeY.no_graduation()
    def no_numbering(self):
        self.single_axeX.no_numbering()
        self.single_axeY.no_numbering()
    def bounding_box(self,pspict=None):
        """
        return the bounding box of the axes.

        If `self` is a default axe, it take into account the content of the pspicture
        and update the mx,my of the single axes X and Y.
        """
        if pspict == None :
            print "pgPIYd"
            raise TypeError,"No pspict given"
        BB=BoundingBox()
        BB.append(self.single_axeX.bounding_box(pspict),pspict)
        BB.append(self.single_axeY.bounding_box(pspict),pspict)

        if self.pspict :
            BB.append(self.pspict.math_bounding_box(),pspict)
        self.add_bounding_box(BB,pspict)                       # This line updates the single axes taking the content of pspict into account.
        BB.check_too_large()
        return BB
    def math_bounding_box(self,pspict=None):
        BB=BoundingBox()
        BB.append(self.single_axeX.math_bounding_box(pspict))
        BB.append(self.single_axeY.math_bounding_box(pspict))
        return BB
    def latex_code(self,language=None,pspict=None):
        if pspict == None :
            raise TypeError,"No pspict given"
        sDx=RemoveLastZeros(self.Dx,10)
        sDy=RemoveLastZeros(self.Dy,10)
        self.add_option("Dx="+sDx)
        self.add_option("Dy="+sDy)
        c=[]
        if self.draw_single_axeX :
            c.append(self.single_axeX.latex_code(language=language,pspict=pspict))
        if self.draw_single_axeY :
            c.append(self.single_axeY.latex_code(language=language,pspict=pspict))
        return "\n".join(c)

def _vector_latex_code(segment,language=None,pspict=None):
    """
    Return the LaTeX's code of a Segment when is is seen as a vector.
    """
    params=segment.params(language=language)
    if language=="pstricks":
        raise DeprecationWarning
        a = segment.I.create_PSpoint() + segment.F.create_PSpoint()
        a = a + "\\ncline["+params+"]{->}{"+segment.I.psName+"}{"+segment.F.psName+"}"
    if language=="tikz":
        params=params+",->,>=latex"
        a = "\draw [{0}] {1} -- {2};".format(params,segment.I.coordinates(numerical=True,pspict=pspict),segment.F.coordinates(numerical=True,pspict=pspict))
    if segment.marque :
        P = segment.F
        P.parameters.symbol = ""
        mark=segment.mark       # This -1 is quite arbitrary, but there are many pictures with more than one mark.
        P.put_mark(mark.dist,mark.angle,mark.text,automatic_place=(pspict,''))
        a = a + P.latex_code(language,pspict)
    return a

from phystricks.ObjectGraph import ObjectGraph

class SingleAxeGraph(ObjectGraph):
    def __init__(self,C,base,mx,Mx,pspict=None):
        ObjectGraph.__init__(self,self)
        self.C=C
        self.base=base
        self.mx=mx
        self.Mx=Mx
        self.pspict=pspict
        self.options=Options()
        self.IsLabel=False
        self.axes_unit=AxesUnit(self.base.length(),"")
        self.Dx=1
        self.arrows="->"
        self.graduation=True
        self.numbering=True
        self.imposed_graduation=[]
        self.mark_origin=True
        self.mark=None
        self.mark_angle=degree(base.angle().radian-pi/2)
        #self.already_enlarged=False
        self.enlarge_size=0.5
    
    # SingleAxe.segment cannot be a lazy attribute because we use it for some projections before
    # to compute the bounding box.
    def segment(self,projection=False,pspict=None):
        if self.mx == 0 and self.Mx == 0 :
            # I think that we only pass here in order either to do a projection either to create an initial bounding box.
            # If xunit or yunit are very low, then returning something like
            #   Segment(self.C-self.base.visual_length(1,pspict=pspict),self.C+self.base.visual_length(1,pspict=pspict))      
            # causes bounding box to be too large.
            # This is why I return a small segment.
            if projection :
                return Segment(self.C,self.C+self.base)
            else :
                return Segment(self.C-self.base.fix_size(1),self.C+self.base.fix_size(1))      

                # raising an error here makes impossible to draw pictures with only vertical stuff. As an example, the following 
                # was crashing :

                #P=Point(0,0)
                #pspict.DrawGraphs(P)
                #pspict.DrawDefaultAxes()
                #pspict.dilatation(1)
                #fig.conclude()

                #raise ValueError,"The size of {0} is not yet defined.".format(self) # this message is hard-checked at position 27319 in main.py
                                                                                    # do not change it.
        #if isinstance(self.C,function):
        #    print("If it crashes here it is most probably because you are using 'O' as base point while 'O' is a function in Sage. You have to define 'O=Point(0,0)' for example")
        return Segment(self.C+self.mx*self.base,self.C+self.Mx*self.base)
    def add_option(self,opt):
        self.options.add_option(opt)
    def mark_point(self,pspict=None):
        return self.segment().F
    def no_numbering(self):
        self.numbering=False
    def no_graduation(self):
        self.graduation=False
    def enlarge_a_little(self,l,xunit=None,yunit=None,pspict=None):
        """
        return the tuple (mx,Mx) that correspond to axes of length `l` more than self
        (in both directions)
        """
        if pspict:
            xunit=pspict.xunit
            yunit=pspict.yunit
        seg=self.segment(pspict=pspict)
        # The aim is to find the multiple of the base vector that has length `l`.
        vx=self.base.F.x
        vy=self.base.F.y
        k=l/sqrt(  (vx*xunit)**2+(vy*yunit)**2  )
        mx=self.mx-k
        Mx=self.Mx+k
        return mx,Mx
    def graduation_bars(self,pspict):
        """
        Return the list of bars that makes the graduation of the axes

        By default, it is one at each multiple of self.base. If an user-defined axes_unit is given, then self.base is modified.

        This function also enlarges the axe by half a *visual* centimeter.
        """
        
        # bars_list contains in the same time marks (for the numbering) and segments (for the bars itself)

        # It seems that this 'imposed_graduation' does not work because
        # the so-created points do not appear in the auxiliary file.
        if self.imposed_graduation :
            raise DeprecationWarning  # June 24 2014
            return self.imposed_graduation
        if not self.graduation:
            return []
        bars_list=[]
        bar_angle=SR(self.mark_angle).n(digits=7)    # pstricks does not accept too large numbers
        for x,symbol in self.axes_unit.place_list(self.mx,self.Mx,self.Dx,self.mark_origin):
            P=(x*self.base).F
            P.psName="ForTheBar"   # Since this point is not supposed to
                                       # be used, all of them have the same ps name.

            if self.numbering :
                # The 0.2 here is hard coded in Histogram, see 71011299
                r,theta=polar_with_dilatation(0.2,radian(self.mark_angle),pspict.xunit,pspict.yunit)
                theta=degree(theta)
                P.put_mark(r,theta,symbol,automatic_place=(pspict,"for axes",self.segment()))
                bars_list.append(P.mark)

            # The following was not taking (xunit,yunit) into account. June 30, 2014
            #circle=Circle(P,0.1)    # 0.1 will be the (half)length of the bar
            #a=circle.get_point(bar_angle,numerical=True)
            #b=circle.get_point(bar_angle+180,numerical=True)

            a=visual_polar(P,0.1,bar_angle,pspict)
            b=visual_polar(P,0.1,bar_angle+180,pspict)

            seg=Segment(a,b)
            bars_list.append(seg)
        return bars_list
    def bounding_box(self,pspict):
        # One cannot take into account the small enlarging here because
        # we do not know if this is the vertical or horizontal axe,
        # so we cannot make the fit of the drawn objects.
        BB=self.math_bounding_box(pspict)
        for graph in self.graduation_bars(pspict):
            BB.append(graph,pspict)
        return BB
    def math_bounding_box(self,pspict):
        # The math_bounding box does not take into account the things that are inside the picture
        # (not even if this are default axes)
        bb=BoundingBox()
        for x,symbol in self.axes_unit.place_list(self.mx,self.Mx,self.Dx,self.mark_origin):
            P=(x*self.base).F
            bb.addX(P.x)
            bb.addY(P.y)
        return bb
    def latex_code(self,language,pspict):
        """
        Return the pstricks code of the axe.
        """
        sDx=RemoveLastZeros(self.Dx,10)
        self.add_option("Dx="+sDx)
        c=[]
        if self.mark :
            c.append(self.mark.latex_code(language,pspict))
        if self.graduation :
            for graph in self.graduation_bars(pspict):
                c.append(graph.latex_code(language=language,pspict=pspict))
        h=AffineVector(self.segment(pspict))
        c.append(h.latex_code(language,pspict))
        return "\n".join(c)
    def __str__(self):
        return "<SingleAxeGraph: C={0} base={1} mx={2} Mx={3}>".format(self.C,self.base,self.mx,self.Mx)

# TODO : to fill portion of circle should be as easy as:
#    CerB=Cer.graph(alpha,alpha+90)
#    CerB.parameters.filled()
#    CerB.parameters.fill.color="blue"
# See the picture RouletteACaVVA

def OptionsStyleLigne():
    return ["linecolor","linestyle"]

class Waviness(object):
    """
    This class contains the informations about the waviness of a curve. It takes as argument a phyFunctionGraph and the parameters dx, dy of the wave.
    Waviness.get_wavy_points        returns a list of points which are disposed around the graph of the curve. These are the points to be linked
                       by a bezier or something in order to get the wavy graph of the function.
    """
    def __init__(self,graph,dx,dy):
        self.graph = graph
        self.dx = dx
        self.dy = dy
        self.obj = self.graph.obj
        try:
            self.Mx = self.graph.Mx
            self.mx = self.graph.mx
        except AttributeError :
            pass
    def get_wavy_points(self):
        if type(self.obj) == phyFunction :
            return self.obj.get_wavy_points(self.mx,self.Mx,self.dx,self.dy)
        if type(self.obj) == Segment :
            return self.obj.get_wavy_points(self.dx,self.dy)

from phystricks.Parameters import Parameters

def extract_interval_information(curve):
    """
    return the interval of the curve.

    That is the initial and final value of the parameter
    of `curve` if that is a :class:`ParametricCurve` and
    the initial and final values of `x` if this the graph of a function.

    INPUT:

    - ``curve`` - graph of a function or a parametric curve

    OUTPUT:

    a tuple of numbers. If nothing is found, return (None,None).

    EXAMPLES::

        sage: from phystricks import *
        sage: from phystricks.BasicGeometricObjects import *
        sage: f=phyFunction(x**2).graph(1,pi)
        sage: extract_interval_information(f)
        (1, pi)
         
        sage: from phystricks.BasicGeometricObjects import *
        sage: a=var('a')
        sage: curve=ParametricCurve(x,sin(x)).graph(sqrt(2),a)
        sage: extract_interval_information(curve)
        (sqrt(2), a)

        sage: f=phyFunction(x**3)
        sage: extract_interval_information(f)
        (None, None)

    """
    # For parametric curves
    if "llamI" in dir(curve):
        return curve.llamI,curve.llamF
    # for functions
    if "mx" in dir(curve):
        return curve.mx,curve.Mx
    # for segments
    if "I" in dir(curve) and "F" in dir(curve):
        return 0,curve.length()
    # for circles
    if "angleI" in dir(curve):
        # We know that circles are AngleI and AngleF that are of type 'AngleMeasure'
        # we are thus returning 'curve.angleI.radian' instead of 'curve.angleI'
        return curve.angleI.radian,curve.angleF.radian
    return None,None

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
    http://ask.sagemath.org/question/359/get_minmax_data-on-implicit_plot
    (thanks to DSM)
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

def general_funtion_get_point(fun,x,advised=True):
        """
        Return a point on the graph of the function with the given x, i.e. it return the point (x,f(x)).

        Also set an attribute advised_mark_angle to the point. This angle is the normal exterior to the graph; 
        visually this is usually the best place to put a mark. Typically you use this as
        P=f.get_point(3)
        P.mark(radius,P.advised_mark_angle,"$P$")

        NOTE:
        If you don't plan to put a mark on the point, you are invited to use advised=False
        in order to speed up the computations.
        """
        P = Point(float(x),fun(x))
        if advised :
            try :
                ca = fun.derivative()(x) 
            except TypeError:       # Happens when Sage has no derivative of the function.
                print "I'm not able to compute derivative of {0}. You should pass advised=False".format(fun)
            else :
                angle_n=degree(atan(ca)+pi/2)
                if fun.derivative(2)(x) > 0:
                    angle_n=angle_n+180
                P._advised_mark_angle=angle_n
        return P

class NonAnalyticParametricCurve(ObjectGraph):
    def __init__(self,f1,f2,mx,Mx):
        ObjectGraph.__init__(self,self)
        self.f1=f1
        self.f2=f2
        self.mx=mx
        self.Mx=Mx
        self.I=self.get_point(mx)
        self.F=self.get_point(Mx)

        self.parameters.plotpoints=100

        from numpy import linspace
        if self.mx is not None and self.Mx is not None:
            self.drawpoints=linspace(self.mx,self.Mx,self.parameters.plotpoints,endpoint=True)
    def curve(self):
        interpolation = InterpolationCurve([self.get_point(x) for x in self.drawpoints])
        self.parameters.add_to(interpolation.parameters,force=True)     # This curve is essentially dedicated to the colors
        return interpolation
    def get_point(self,x,advised=False):
        return Point(self.f1(x),self.f2(x))
    def reverse(self):
        """
        Return the curve [mx,Mx] -> R^2 that makes
        the inverse path.
        """
        f1=lambda x:self.f1(self.mx+self.Mx-x)
        f2=lambda x:self.f2(self.mx+self.Mx-x)
        return NonAnalyticParametricCurve(f1,f2,self.mx,self.Mx)
    def math_bounding_box(self,pspict=None):
        return self.curve().math_bounding_box(pspict)
    def bounding_box(self,pspict=None):
        return self.curve().bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        return self.curve().latex_code(language=language,pspict=pspict)
    def __call__(self,x):
        return self.get_point(x)

class NonAnalyticFunction(ObjectGraph):
    """
    Represent a function for which one has no analytic form.

    As long as one can evaluate it at points, one can draw an interpolation curve.
    """
    def __init__(self,fun,mx=None,Mx=None):
        ObjectGraph.__init__(self,fun)
        self.mx=mx
        self.Mx=Mx
        self.fun=fun
        self.parameters.plotpoints=100
        self.old_mx=None    # Will be used in order to simulate a lazy_attribute in self.get_minmax_data
        self.old_Mx=None
        self.minmax_result=None
        from numpy import linspace
        if self.mx is not None and self.Mx is not None:
            self.drawpoints=linspace(self.mx,self.Mx,self.parameters.plotpoints,endpoint=True)
        self.parameters.color="blue"
    def parametric_curve(self,mx=None,Mx=None):
        if mx == None:
            mx=self.mx
        if Mx == None:
            Mx=self.Mx
        x=var('x')
        return NonAnalyticParametricCurve(x,self,mx,Mx)
    def reverse(self):
        new = lambda x: self.fun(self.Mx+self.mx-x)
        return NonAnalyticFunction(new,self.mx,self.Mx)
    def curve(self,drawpoints):
        """
        Return the interpolation curve corresponding to self.

        Since it could be cpu-consuming, this is a lazy_attribute. For that reason it should not be
        called by the end-user but only during the computation of the bounding box and the pstricks code.
        """
        points_list=[self.get_point(x) for x in self.drawpoints]
        return InterpolationCurve(points_list,context_object=self)
    def get_point(self,x):
        return general_funtion_get_point(self,x,advised=False)
    def graph(self,mx,Mx):
        return NonAnalyticFunction(self.fun,mx,Mx)
    def get_minmax_data(self,mx,Mx):
        """
        return the xmin, xmax, ymin and ymax of the graph.
        """
        if self.old_mx!=mx or self.old_Mx!=Mx or not self.minmax_result:
            self.minmax_result = MyMinMax(plot(self.fun,(mx,Mx)).get_minmax_data())
        return self.minmax_result
    def math_bounding_box(self,pspict=None):
        xmin=self.get_minmax_data(self.mx,self.Mx)["xmin"]
        xmax=self.get_minmax_data(self.mx,self.Mx)["xmax"]
        ymin=self.get_minmax_data(self.mx,self.Mx)["ymin"]
        ymax=self.get_minmax_data(self.mx,self.Mx)["ymax"]
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    def bounding_box(self,pspict=None):
        return self.math_bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        return self.curve(self.drawpoints).latex_code(language=language,pspict=pspict)
    def __call__(self,x):
        return self.fun(x)

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

    A list of lists of points. Each list corresponds to a path (see matplotlib), but the components
    are converted into points in the sens of phystricks (instead of matplotlib's vertices).

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
        sage: print paths[1][3]
        <Point(4.87405534614323,-4.6644295302013425)>
    """
    l=[]
    for path in get_paths_from_plot(p):
        pp=[]
        for vertice in path.vertices:
            pp.append(Point(vertice[0],vertice[1]))
        l.append(pp)
    return l

class SurfaceBetweenLines(ObjectGraph):
    def __init__(self,curve1,curve2):
        """
        Give the graph of the surface between the two lines.

        The lines are needed to have a starting and ending point
        that will be joined by straight lines.
        """
        # By convention, the first line goes from left to right and the second one to right to left.

        ObjectGraph.__init__(self,self)

        if curve1.I.x > curve1.F.x:
            curve1=curve1.reverse()
        if curve2.I.x > curve2.F.x:
            curve2=curve2.reverse()

        self.curve1=curve1
        self.curve2=curve2

        self.I1=curve1.I
        self.I2=curve2.I

        self.F1=curve1.F
        self.F2=curve2.F

        self.Isegment=Segment(self.I1,self.I2)
        self.Fsegment=Segment(self.F1,self.F2)
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        bb.append(self.curve1,pspict)
        bb.append(self.curve2,pspict)
        return bb
    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        a=[]
       
        c1=self.curve1
        c2=self.curve2.reverse()

        custom=CustomSurface(c1,self.Fsegment,c2,self.Isegment)
        self.parameters.add_to(custom.parameters)     # This curve is essentially dedicated to the colors
        custom.options=self.options
        
        a.append("%--- begin of Surface between lines ---")
        a.append("% Custom surface")
        a.append(custom.latex_code(language=language,pspict=pspict))

        a.append("% Curve 1")
        a.append(self.curve1.latex_code(language=language,pspict=pspict))
        a.append("% Curve 2")
        a.append(self.curve2.latex_code(language=language,pspict=pspict))
        a.append("% Isegment")
        a.append(self.Isegment.latex_code(language=language,pspict=pspict))
        a.append("% Fsegment")
        a.append(self.Fsegment.latex_code(language=language,pspict=pspict))
        a.append("%--- end of Surface between lines ---")
        return "\n".join(a)

# Since all type of surfaces have to be specializations of SurfaceBetweenParametricCurves,
# we have to unify the names of the segments.
# x.Isegment is the segment joining the first point of the first curve
# c.Fsegment is the other one.
# May, 1, 2011

# For the same reason, all type of surfaces have to be functions instead of classes.
# These functions return an object SurfaceBetweenParametricCurvesGraph 
# with the right particularization.

class SurfaceBetweenParametricCurvesGraph(ObjectGraph):
    def __init__(self,curve1,curve2,interval1=(None,None),interval2=(None,None),reverse1=False,reverse2=True):
        # TODO: I think that the parameters reverse1 and reverse2 are no more useful
        #   since I enforce the condition curve1 : left -> right by hand.
        ObjectGraph.__init__(self,self)

        self.curve1=curve1
        self.curve2=curve2

        #self.f1=self.curve1       # TODO: Soon or later, one will have to fusion these two
        #self.f2=self.curve2        

        self.mx1=interval1[0]
        self.mx2=interval1[1]
        self.Mx1=interval2[0]
        self.Mx2=interval2[1]
        for attr in [self.mx1,self.mx2,self.Mx1,self.Mx2]:
            if attr == None:
                raise TypeError,"At this point, initial and final values have to be already chosen"
        self.curve1.llamI=self.mx1
        self.curve1.llamF=self.Mx1
        self.curve2.llamI=self.mx2
        self.curve2.llamF=self.Mx2

        self.draw_Isegment=True
        self.draw_Fsegment=True
        self.Isegment=Segment(self.curve2.get_point(self.mx2,advised=False),self.curve1.get_point(self.mx1,advised=False))
        self.Fsegment=Segment(self.curve1.get_point(self.Mx1,advised=False),self.curve2.get_point(self.Mx2,advised=False))

        self.add_option("fillstyle=vlines") 
        self.parameters.color=None       

    def bounding_box(self,pspict=None):
        if pspict==None:
            raise ValueError, "You have to provide a pspict"
        bb=BoundingBox()
        bb.append(self.curve1,pspict)
        bb.append(self.curve2,pspict)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        a=[]
       
        c1=self.curve1.graph(self.mx1,self.Mx1)
        c2=self.curve2.graph(self.mx2,self.Mx2)

        # By convention, the first line goes from left to right and the second one to right to left.
        # The same is followed in SurfaceBetweenLines

        if c1.I.x > c1.F.x:
            c1=c1.reverse()
        if c2.I.x < c2.F.x:
            c2=c2.reverse()

        reIsegment=Segment(c2.F,c1.I)
        reFsegment=Segment(c1.F,c2.I)
        reIsegment.parameters=self.Isegment.parameters
        reFsegment.parameters=self.Fsegment.parameters

        if self.parameters._filled or self.parameters._hatched :
            custom=CustomSurface(c1,reFsegment,c2,reIsegment)
            custom.parameters=self.parameters.copy()
            a.append(custom.latex_code(language=language,pspict=pspict))

        if self.parameters.color!=None :
            self.Isegment.parameters.color=self.parameters.color
            self.Fsegment.parameters.color=self.parameters.color
            self.curve1.parameters.color=self.parameters.color
            self.curve2.parameters.color=self.parameters.color
    
        a.append(self.curve1.latex_code(language=language,pspict=pspict))
        a.append(self.curve2.latex_code(language=language,pspict=pspict))
        if self.draw_Isegment :
            a.append(reIsegment.latex_code(language=language,pspict=pspict))
        if self.draw_Fsegment :
            a.append(reFsegment.latex_code(language=language,pspict=pspict))
        return "\n".join(a)

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
    #"""
    #The tikz code of objects are of the form
    # \draw [...] something (...) ;
    #Here we have to convert that into
    #  something [...] (...)
    #ex :
    #\draw[domain=2:3] plot ( {\x},{\x} );
    #     -->
    # plot [domain=2:3] ( {\x},{\x} )

    # There are also interpolations curves whose come like that :
    #   \draw [...] plot [smooth,tension=1] coordinates {(x1,y2)(x2,y2)} 

    t1=text.replace("\draw","").replace(";","")
    bracket=first_bracket(t1)
    t2=t1.replace(bracket,"")
    t3=t2.strip()
    if "coordinates" in t3 :
        return t3
    else :
        answer=t3.replace("plot","plot "+bracket)
    return answer

class CustomSurfaceGraph(ObjectGraph):
    """
    INPUT:

    - args - A list or a tuple of graphs that can compose a \pscustom
    """
    def __init__(self,args):
        ObjectGraph.__init__(self,self)
        #self.add_option("fillstyle=vlines,linestyle=none")  
        self.add_option("fillstyle=none,linestyle=none")
        self.graphList=args
        self.edges=Parameters()
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
        raise DeprecationWarning
        # I cannot add all the obj.pstricks_code() inside the \pscustom because we cannot have \pstGeonode inside \pscustom
        # Thus I have to hack the code in order to bring all the \pstGeonode before the opening of \pscustom
        a=[]
        for obj in self.graphList :
            a.append(obj.pstricks_code(pspict=pspict))
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
        if self.parameters.color :
            self.add_option("fillcolor="+self.parameters.color+",linecolor="+self.parameters.color+",hatchcolor="+self.parameters.color)
        a.append(outside)
        a.append("\pscustom["+self.params(language="pstricks")+"]{")
        a.append(inside)
        a.append("}")
        return "\n".join(a)
    def tikz_code(self,pspict=None):
        """
        If the CustomSurface has to be filled, we start by plotting the filling.

        Then we plot, separately, the lines forming the border. Thus we can have different colors and line style for the different edges.
        """
        # The color attribution priority is the following.
        # if self.parameters.color is given, then this will be the color
        # if an hatch or a fill color is given and no self.parameters.color, then this will be used
        a=[]
        color=None

        # It cannot be filled by default when a color is given because Rectangles and Polygon drop here
        #if self.parameters.color :
        #    if self.parameters._hatched==False:     # By default it will be filled if one give a color
        #        self.parameters._filled=True

        if self.parameters._filled and self.parameters.fill.color:
            color=self.parameters.fill.color
        if self.parameters._hatched and self.parameters.hatch.color:
            color=self.parameters.hatch.color
        if self.parameters._filled or self.parameters._hatched :
            l=[]
            for obj in self.graphList :
                try:
                    l.extend( [p.coordinates(numerical=True,digits=3,pspict=pspict) for p in obj.representative_points()] )
                except AttributeError :
                    print(obj)
                    raise
                    obj_code=obj.latex_code(language="tikz",pspict=pspict)
                    l.append( draw_to_fill(obj_code) )
            l.append(" cycle;")
            code=" -- ".join(l)
            if self.parameters._hatched :
                # This is from
                # http://www.techques.com/question/31-54358/custom-and-built-in-tikz-fill-patterns
                # position 170321508
                def_hatching=r"""
% declaring the keys in tikz
\tikzset{hatchspread/.code={\setlength{\hatchspread}{#1}},
         hatchthickness/.code={\setlength{\hatchthickness}{#1}}}
% setting the default values
\tikzset{hatchspread=3pt,
         hatchthickness=0.4pt}
"""
                a.append(def_hatching)
                if color==None:
                    color="lightgray"
                options="color="+color
                options=options+",  pattern=custom north west lines,hatchspread=10pt,hatchthickness=1pt "
            if self.parameters._filled:
                options="color="+color
            a.append("\\fill [{}] ".format(options)+code)
    
        return "\n".join(a)
    def latex_code(self,language=None,pspict=None):
        """
        There are two quite different ways to get here. The first is to ask a surface under a function and the second is to ask for a rectangle or a polygon.

        if self.parameters.color is given, this will be the color of the edges

        If one wants to give different colors to edges, one has to ask explicitly using
        self.Isegment
        self.Fsegment
        self.curve1
        self.curve2
        in the case of surface between curves.

        If one wants the surface to be filled or hatched, on has to ask explicitly.
        """
        a=[]
        if language=="pstricks":
            raise DeprecationWarning
            a.append(self.pstricks_code(pspict))
        if language=="tikz":
            a.append(self.tikz_code(pspict))
        if self._draw_edges :
            for obj in self.graphList :
                obj.parameters = self.edges.copy()
                a.append(obj.latex_code(language=language,pspict=pspict))
        return '\n'.join(a)

class PolygonGraph(ObjectGraph):
    """
    INPUT:

    - ``args`` - a tuple of points.

    NOTE:

    This class is not intended to be used by the end-user. The latter has to use :func:`Polygon`.
    """
    def __init__(self,points_list):
        ObjectGraph.__init__(self,self)
        self.edges=[]
        self.vertices=points_list
        self.points_list=self.vertices
        self.edge=Segment(Point(0,0),Point(1,1))    # This is an arbitrary segment that only serves to have a
                                                    # "model" for the parameters.
        for i in range(0,len(self.points_list)):
            segment=Segment(self.points_list[i],self.points_list[(i+1)%len(self.points_list)])
            self.edges.append(segment)
        self.draw_edges=True
        self.independent_edge=False
    def rotation(self,angle):
        pts=[  P.rotation(angle) for P in self.points_list  ]
        return Polygon(pts)
    def make_edges_independent(self):
        """
        make the edges customisation independent the one to the other.
        """
        for s in self.edges :
            s.parameters=self.edge.parameters.copy()
        self.independent_edge=True
    def no_edges(self):
        """
        When X.no_edges() is used, the edges of the polygon will not be drawn.
        """
        self.draw_edges=False
    def put_mark(self,dist,text_list=None,points_names=None,mark_point=None,pspict=None):
        n=len(self.points_list)
        if not text_list and not points_names:
            import string
            text_list=[   "\( {} \)".format(x) for x in  string.ascii_uppercase[0:n]  ]
        if points_names :
            text_list=[    "\( {} \)".format(x) for x in points_names   ]
        for i,P in enumerate(self.points_list):
            text=text_list[i]
            A=self.points_list[(i-1)%n]
            B=self.points_list[(i+1)%n]
            v1=AffineVector(A,P).fix_origin(P).fix_size(1)
            v2=AffineVector(B,P).fix_origin(P).fix_size(1)
            vect=(v1+v2).fix_size(dist)
            Q=P+vect
            angle=Segment(P,Q).angle()
            P.put_mark(dist,angle,text,automatic_place=(pspict,"center"))
            self.added_objects.append(P)
    def math_bounding_box(self,pspict=None):
        bb=BoundingBox()
        for P in self.points_list:
            bb.append(P,pspict)
        return bb
    def bounding_box(self,pspict=None):
        return self.math_bounding_box(pspict)
    def specific_action_on_pspict(self,pspict):
        """
        If self.parameters.color is not None, it will be the color of the edges.

        If one wants to fill or hatch, one has to ask explicitly.
        """
        if self.parameters._hatched or self.parameters._filled :
            custom=CustomSurface(self.edges)
            custom.parameters=self.parameters.copy()
            pspict.DrawGraph(custom)
        if self.parameters.color!=None:
            self.draw_edges=True
            for edge in self.edges:
                edge.parameters.color=self.parameters.color
        if self.draw_edges:
            for edge in self.edges:
                if not self.independent_edge :
                    edge.parameters=self.edge.parameters
                    if self.parameters.color!=None:
                        edge.parameters.color=self.parameters.color
                pspict.DrawGraph(edge)

# RectangleGraph once inherited from GeometricRectangle):   (June 26, 2014)
class RectangleGraph(PolygonGraph):
    """
    The parameters of the four lines are by default the same, but they can be adapted separately.

    graph_N returns the north side as a phystricks.Segment object
    The parameters of the four sides have to be set independently.

    The drawing is done by \psframe, so that, in principle, all the options are available.
    """
    def __init__(self,NW,SE):
        #ObjectGraph.__init__(self,self)
        self.NW = NW
        self.SE = SE
        self.SW = Point(self.NW.x,self.SE.y)
        self.NE = Point(self.SE.x,self.NW.y)
        PolygonGraph.__init__(self,[self.SW,self.SE,self.NE,self.NW])
        self.mx=self.NW.x
        self.Mx=self.SE.x
        self.my=self.SE.y
        self.My=self.NW.y
        self.rectangle = self.obj

        self.segment_N=Segment(self.NW,self.NE)
        self.segment_S=Segment(self.SW,self.SE)
        self.segment_E=Segment(self.NE,self.SE)
        self.segment_W=Segment(self.NW,self.SW)

        # Use self.edges instead of self.segments (September, 18, 2014)
        #self.segments=[self.segment_N,self.segment_S,self.segment_E,self.segment_W]

        # Putting the style of the edges to none makes the 
        # CustomSurface (and then filling and hatching) not work because the edges'LaTeX code is use to create the tikz path
        # defining the surface.
        #for s in self.edges:
        #    s.parameters.style="none"
    def polygon(self):
        polygon= Polygon(self.NW,self.NE,self.SE,self.SW)
        polygon.parameters=self.parameters.copy()
        return polygon
    def first_diagonal(self):
        return Segment(self.NW,self.SE)
    def second_diagonal(self):
        return Segment(self.SW,self.NE)
    def center(self):
        return self.first_diagonal().center()
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return RectangleGraph

    def _segment(self,side):
        bare_name = "graph_"+side
        if not bare_name in self.__dict__.keys():
            line = self.__getattribute__("segment_"+side)()
            #line.parameters=self.parameters.copy()
            self.__dict__[bare_name]=line
        return  self.__dict__[bare_name]
    def __getattr__(self,attrname):
        if "graph_" in attrname:
            return self._segment(attrname[6])
        raise AttributeError

    # Inherited from PolygonGraph

    #def bounding_box(self,pspict=None):
    #    return BoundingBox(self.NW,self.SE)
    #def math_bounding_box(self,pspict=None):
    #    return self.bounding_box(pspict)
    #def latex_code(self,language=None,pspict=None):
    #    """
    #    We are drawing the psframe AND the segments.
    #    The aim is to be able to use the frame for filling, being still able to customise separately the edges.
    #    """
    #    return self.polygon().latex_code(language=language,pspict=pspict)

        # Drawing of rectangle is now completely passed to Polygon.
        #    June 26, 2014
        #for s in self.segments:
        #    if s.parameters==None:
        #        s.parameters=self.parameters.copy()
        #a=[]
        #cNE=self.rectangle.NE.coordinates(numerical=True)
        #cSW=self.rectangle.SW.coordinates(numerical=True)
        #if language=="pstricks":
        #    a.append("\psframe["+self.params(language="pstricks")+"]"+cSW+cNE)
        #if language=="tikz":
        #    k=self.params(language="tikz")
        #    if "none" in k:
        #        print(self)
        #        print(self.parameters)
        #        raise TypeError
        #    a.append("\draw [{0}] {1} rectangle {2}; ".format(self.params(language="tikz"),cSW,cNE))
        #for s in self.segments :
        #    a.append(s.latex_code(language=language,pspict=pspict))
        #return "\n".join(a)

class Circle3DGraph(ObjectGraph):
    def __init__(self,op,O,A,B,angleI=0,angleF=0):
        """
        The circle passing trough A and B with center O.

        `A`, `B` and `O` are tuples of numbers
        """
        ObjectGraph.__init__(self,self)
        self.op=op
        self.O=O
        self.A=A
        self.B=B
        self.center=Vector3D(O[0],O[1],O[2])
        self.u=Vector3D( A[0]-O[0],A[1]-O[1],A[2]-O[2]  )
        self.v=Vector3D( B[0]-O[0],B[1]-O[1],B[2]-O[2]  )
        self.radius_u=sqrt( sum([k**2 for k in self.u])  )
        self.radius_v=sqrt( sum([k**2 for k in self.v])  )
        self.parameters.plotpoints=10*max(self.radius_u,self.radius_v)
        self.angleI=angleI
        self.angleF=angleF
        self.divide=False
    @lazy_attribute
    def points_list(self):
        l=[]
        import numpy
        angles=numpy.linspace(self.angleI,self.angleF,self.parameters.plotpoints)
        for a in angles:
            l.append( self.get_point(a) )
        return l
    @lazy_attribute
    def curve2d(self):
        proj_points_list=[]
        for P in self.points_list:
            t=self.op.point(P.x,P.y,P.z)
            proj_points_list.append(t)
        curve=InterpolationCurveGraph(proj_points_list)
        curve.parameters=self.parameters.copy()
        return curve
    def xmin(self):
        """
        return the visually --in the sense of the projection on the screen, not in the sense of xunit,yunit-- minimal x point of the circle
        """
        return min(  self.curve2d.points_list,key=lambda P:P.x  )
    def xmax(self):
        """
        return the visually --in the sense of the projection on the screen, not in the sense of xunit,yunit-- maximal x point of the circle
        """
        return max(  self.curve2d.points_list,key=lambda P:P.x  )
    def get_point(self,angle):
        return self.center+cos(angle)*self.u+sin(angle)*self.v  
    def get_point2d(self,angle):
        return self.op.point(self.get_point(angle))
    def graph(self,angleI,angleF):
        C = Circle3DGraph(self.op,self.O,self.A,self.B,angleI,angleF)
        C.parameters=self.parameters.copy()
        return C
    def bounding_box(self,pspict=None):
        return self.curve2d.bounding_box(pspict)
    def math_bounding_box(self,pspict=None):
        return self.curve2d.math_bounding_box(pspict)
    def specific_action_on_pspict(self,pspict):
        if not self.divide:
            pspict.DrawGraphs(self.curve2d)
        if self.divide:
            c1=self.graph(0,pi)
            c2=self.graph(pi,2*pi)
            c1.parameters.style="dashed"
            pspict.DrawGraphs(c1,c2)


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
            pspict.axes.single_axeX.put_mark(0.5,-90,self.legende,automatic_place=(pspict,"N"))
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
            P.put_mark(0.2,-90,str(xx),automatic_place=(pspict,"N"))    # see 71011299 before to change this 0.2
            pspict.DrawGraph(P)
        for box in self.box_list :
            P=box.rectangle.segment_N.mark_point()
            P.put_mark(0.2,90,"$"+str(box.n)+"$",automatic_place=(pspict,"S"))
            P.parameters.symbol=""
            pspict.DrawGraph(P)
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
                P.put_mark(0.2,90,"\({{:.{}f}}\)".format(self.numbering_decimals).format(h),automatic_place=(pspict,"S"))
                nb.append(P)
        return nb
    def action_on_pspict(self,pspict):
        for P in self.numbering_marks(pspict):
            pspict.DrawGraph(P)
        for l in self.lines_list:
            l.parameters.other_options["linewidth"]="{}cm".format(self.linewidth)
            pspict.DrawGraph(l)
        for P in self.numbering_marks(pspict):
            pspict.DrawGraph(P)
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

class RightAngleGraph(ObjectGraph):
    def __init__(self,d1,d2,r,n1,n2):
        """
        two lines and a distance.

        n1 and n2 are 0 or 1 and indicating which sector has to be marked.
        'n1' if for the intersection with d1. If 'n1=0' then we choose the intersection nearest to d1.I
        Similarly for n2
        """
        ObjectGraph.__init__(self,self)
        self.d1=d1
        self.d2=d2

        # If the intersection point is one of the initial or final point of d1 or d2, then the sorting
        # in 'specific_action_on_pspict' does not work.
        # This happens in RightAngle(  Segment(D,E),Segment(D,F),l=0.2, n1=1,n2=1 ) because the same point 'D' is given
        # for both d1 and d2.
        # We need d1.I, d1.F, d2.I and d2.F to be four distinct points.
        if self.d1.I==self.d2.I or self.d1.I==self.d2.F or self.d1.F==self.d2.I or self.d1.F==self.d2.F:
            self.d1=d1.dilatation(1.5)
            self.d2=d2.dilatation(1.5)

        self.r=r
        self.n1=n1
        self.n2=n2
        self.intersection=Intersection(d1,d2)[0]
    def inter_point(self,I,F,n,pspict):
        v1=AffineVector(I,F)
        v=visual_length(v1,l=1,pspict=pspict)
        if n==0:
            P1=I - self.r*v
        if n==1:
            P1=I + self.r*v
        
        rv=self.r*v
        return P1

    def specific_action_on_pspict(self,pspict):
    
        if False :          # No more used (April 23, 2015)
            circle=Circle(self.intersection,self.r)
            K=Intersection(circle,self.d1)
            K.sort(key=lambda P:Distance_sq(P,self.d1.I))
            L=Intersection(circle,self.d2)
            L.sort(key=lambda P:Distance_sq(P,self.d2.I))
            if self.n1==0:
                P1=K[0]
            if self.n1==1:
                P1=K[1]
            if self.n2==0:
                P2=L[0]
            if self.n2==1:
                P2=L[1]

        P1=self.inter_point(self.intersection,self.d1.F,self.n1,pspict)
        P2=self.inter_point(self.intersection,self.d2.F,self.n2,pspict)

        Q=P1+P2-self.intersection
        l1=Segment(Q,P1)
        l2=Segment(Q,P2)
        
        l1.parameters=self.parameters.copy()
        l2.parameters=self.parameters.copy()
        pspict.DrawGraphs(l1,l2)
    def bounding_box(self,pspict):
        return BoundingBox()
    def math_bounding_box(self,pspict):
        return BoundingBox()
    def latex_code(self,language=None,pspict=None):
        return ""

def check_too_large(obj,pspict=None):
    try:
        bb=obj.bounding_box(pspict)
        mx=bb.xmin
        my=bb.ymin
        Mx=bb.xmax
        My=bb.ymax
    except AttributeError:
        print "Object {0} has no method bounding_box.".format(obj)
        mx=obj.mx
        my=obj.my
        Mx=obj.Mx
        My=obj.My
    if pspict:
        try :
            if mx<pspict.mx_acceptable_BB :
                print("mx=",mx,"when pspict.mx_acceptable_BB=",pspict.mx_acceptable_BB)
                raise main.PhystricksCheckBBError()
            if my<pspict.my_acceptable_BB :
                print("my=",my,"when pspict.my_acceptable_BB=",pspict.my_acceptable_BB)
                raise main.PhystricksCheckBBError()
            if Mx>pspict.Mx_acceptable_BB :
                print("Mx=",Mx,"when pspict.Mx_acceptable_BB=",pspict.Mx_acceptable_BB)
                raise main.PhystricksCheckBBError()
            if My>pspict.My_acceptable_BB:
                print("My=",My,"when pspict.My_acceptable_BB=",pspict.My_acceptable_BB)
                raise main.PhystricksCheckBBError()
        except main.PhystricksCheckBBError :
            print "I don't believe that object {1} has a bounding box as large as {0}".format(bb,obj)
            try :
                print "The mother of {0} is {1}".format(obj,obj.mother)
            except AttributeError :
                pass
            raise ValueError

def sudoku_substitution(tableau,symbol_list=[  str(k) for k in range(-4,5) ]):
    """
    From a string representing a sudoku grid,
    1. remove empty lines
    2. remove spaces
    3. substitute 1..9 to the symbol_list
    """
    import string
    lines = tableau.split("\n")[1:]
    n_lines=[   l.replace(" ","") for l in lines if len(l)!=0  ]
    nn_lines=[]
    for l in n_lines :
        a=[]
        for c in l.split(","):
            if  c in string.digits:
                a.append(  symbol_list[int(c)-1])
            else :
                a.append(c)
        nn_lines.append(",".join(a))
    n_tableau="\n".join(nn_lines)
    return n_tableau

class SudokuGridGraph(object):
    def __init__(self,question,length=1):
        self.question=sudoku_substitution(question)
        self.length=length       # length of a cell

    def specific_action_on_pspict(self,pspict):
        import string

        vlines=[]
        hlines=[]
        content=[]
        numbering=[]
        for i in range(0,9):
            A=Point(  (i+1)*self.length-self.length/2,self.length/2  )
            A.parameters.symbol=""
            A.put_mark(0,0,string.uppercase[i])
            B=Point(-self.length/2,-i*self.length-self.length/2)
            B.parameters.symbol=""
            B.put_mark(0,0,string.digits[i+1])
            numbering.append(A)
            numbering.append(B)

        for i in range(0,10):
            v=Segment(Point(i*self.length,0),Point(i*self.length,-9*self.length))
            h=Segment(Point(0,-i*self.length),Point(9*self.length,-i*self.length))
            if i%3==0 :
                v.parameters.add_option("linewidth","0.07cm")
                h.parameters.add_option("linewidth","0.07cm")
            vlines.append(v)
            hlines.append(h)
    
        lines = self.question.split("\n")
        for i,li in enumerate(lines):
            for j,c in enumerate(li.split(",")):
                A=Point(   j*self.length+self.length/2, -i*self.length-self.length/2  )
                A.parameters.symbol=""
                if c=="i":
                    A.put_mark(3*self.length/9,-90,"\ldots",automatic_place=(pspict,"N"))
                if c in [  str(k) for k in range(-9,10)  ] :
                    A.put_mark(0,0,c)
                content.append(A)
        pspict.DrawGraphs(vlines,hlines,content,numbering)
    def action_on_pspict(self,pspict):
        pass
    # No need to give a precise bounding box. Since the elements will be inserted with pspict.DrawGraph,
    # their BB will be counted in the global BB.
    def math_bounding_box(self,pspict):
        return BoundingBox()
    def bounding_box(self,pspict):
        return BoundingBox()
    def latex_code(self,language=None,pspict=None):
        return ""

class FractionPieDiagramGraph(ObjectGraph):
    def __init__(self,center,radius,a,b):
        """
        The pie diagram for the fraction 'a/b' inside the circle of given center and radius.

        2/4 and 1/2 are not treated in the same way because 2/4 divides the pie into 4 parts (and fills 2) while 1/2 divides into 2 parts.
        """
        ObjectGraph.__init__(self,self)
        self.center=center
        self.radius=radius
        self.numerator=a
        self.denominator=b
        if a>b:
            raise ValueError,"Numerator is larger than denominator"
        self.circle=Circle(self.center,self.radius)
        self._circular_sector=None
    def circular_sector(self):
        if not self._circular_sector :
            FullAngle=AngleMeasure(value_degree=360)
            cs=CircularSector(self.center,self.radius,0,self.numerator*FullAngle//self.denominator)
            cs.parameters.filled()
            cs.parameters.fill.color="lightgray"
            self._circular_sector=cs
        return self._circular_sector
    def bounding_box(self,pspict):
        return self.circle.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        return ""
    def specific_action_on_pspict(self,pspict):
        if self.denominator==self.numerator:
            cs=Circle(self.center,self.radius)
            cs.parameters.filled()
            cs.parameters.fill.color="lightgray"
            l=[cs]
        else :
            import numpy
            l=[self.circular_sector()]
            for k in numpy.linspace(0,360,self.denominator,endpoint=False):
                s=Segment(  self.circle.get_point(k),self.center  )
                s.parameters.style="dashed"
                l.append(s)
            l.append(self.circle)
        pspict.DrawGraphs(l)

import phystricks.main as main
import phystricks.SmallComputations as SmallComputations
