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

# copyright (c) Laurent Claessens, 2010-2015
# email: moky.math@gmai.com

"""
Each of them have the methods for basic geometric manipulations: rotations, dilatations, tangent vector, etc.

The end-user should not use the functions whose name begin with ``GraphOf`` or ``Geometric``. 
Rather he has to use the constructors like :func:`Point`, :func:`AffineVector` and so on.
"""

from __future__ import division
from __future__ import unicode_literals

import math
from sage.all import *

from phystricks import *
var=WrapperStr(var)

def SubstitutionMathPsTricks(fx):
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

def SubstitutionMathTikz(fx):
    """
    - fx : string that gives a function with 'x'

    We return the same function, but in terms of tikz.
    """
    # One of the big deal is that tikz works with degree instead of radian

    listeSubst = []
    listeSubst.append(["x","(\\x)"])        # Notice the parenthesis because \x^2=-1 when \x=-1
    #listeSubst.append(["sin","radsin"])
    #listeSubst.append(["cos","radcos"])
    listeSubst.append(["<++>","<++>"])
    listeSubst.append(["<++>","<++>"])
    a = fx
    for s in listeSubst :
        a = a.replace(s[0],s[1])
    return a

def PointsNameList():
    """
    Furnish a list of points name.

    This is the generator of the sequence of strings 
    "aaaa", "aaab", ..., "aaaz","aaaA", ..., "aaaZ","aaba" etc.

    EXAMPLES::
    
        sage: from phystricks.BasicGeometricObjects import *
        sage: x=PointsNameList()
        sage: x.next()
        u'aaaa'
        sage: x.next()
        u'aaab'
    """
    # The fact that this function return 4 character strings is hard-coded here 
    #   and that 4 is hard-coded in the function unify_point_name
    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for i in alphabet:
        for j in alphabet:
            for k in alphabet:
                for l in alphabet:
                    yield i+j+k+l

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
        a = segment.I.create_PSpoint() + segment.F.create_PSpoint()
        a = a + "\\ncline["+params+"]{->}{"+segment.I.psName+"}{"+segment.F.psName+"}"
    if language=="tikz":
        params=params+",->,>=latex"
        a = "\draw [{0}] {1} -- {2};".format(params,segment.I.coordinates(numerical=True,pspict=pspict),segment.F.coordinates(numerical=True,pspict=pspict))
    if segment.marque :
        P = segment.F
        P.parameters.symbol = ""
        mark=segment.mark       # This -1 is quite arbitrary, but there are very pictures with more than one mark.
        P.put_mark(mark.dist,mark.angle,mark.text,automatic_place=(pspict,''))
        a = a + P.latex_code(language,pspict)
    return a


def Distance_sq(P,Q):
    """ return the squared distance between P and Q """
    return (P.x-Q.x)**2+(P.y-Q.y)**2

def Distance(P,Q):
    """ return the distance between P and Q """
    return sqrt(Distance_sq(P,Q))

def inner_product(v,w):
    """
    Return the inner product of vectors v and w

    INPUT:
    - ``v,w`` - two vectors or points

    OUTPUT:
    a number

    If the vectors are not based at (0,0), make first 
    the translation and return the inner product.

    If a point is passed, it is considered as the vector
    from (0,0).

    EXAMPLES::

    sage: from phystricks import *
    sage: from phystricks.BasicGeometricObjects import *
    sage: v=Vector(1,3)
    sage: w=Vector(-5,7)
    sage: inner_product(v,w)
    16

    sage: v=AffineVector(Point(1,1),Point(2,2))
    sage: w=AffineVector(Point(-2,5),Point(-1,4))
    sage: inner_product(v,w)
    0
    """
    try:
        a=v.Point()
    except AttributeError:
        a=v
    try:
        b=w.Point()
    except AttributeError:
        b=w
    return a.x*b.x+a.y*b.y

class Options(object):
    """
    Describe the drawing options of pstricks objects.

    ATTRIBUTES :
        self.DicoOptions : dictionnary which contains the options
    METHODS :
        self.merge_options(opt) : opt is an other object of the class Options. The method merges the two in the sense that opt is not
                        changed, but 
                        1. if opt contains a key more, it is added to self
                        2. if a key of opt is different of the one of self, self is changed
    """
    def __init__(self):
        self.DicoOptions = {}
    # On ajoute une des options en donnant genre
    # LineColor=blue,LineStyle=dashed
    # Ou alors en donnant un dictionnaire genre
    # {"Dx":1,"Dy":3}
    def add_option(self,opt):
        if opt :            # If the argument is empty.
            try:
                for op in opt.split(","):
                    s = op.split("=")
                    self.DicoOptions[s[0]] = s[1]
            except AttributeError :
                for op in opt.keys():
                    self.DicoOptions[op] = opt[op]

    def remove_option(self,opt):
        del(self.DicoOptions[opt])
    def merge_options(self,opt):
        for op in opt.DicoOptions.keys():
            self.add_option({op:opt[op]})
    def extend_options(self,Opt):
        for opt in Opt.DicoOptions.keys():
            self.add_option(opt+"="+Opt.DicoOptions[opt])
    # Afiter est une liste de noms d'options, et cette méthode retourne une instance de Options qui a juste ces options-là, 
    # avec les valeurs de self.
    def sousOptions(self,AFiter):
        O = Options()
        for op in self.DicoOptions.keys() :
            if op in AFiter : O.add_option(op+"="+self.DicoOptions[op])
        return O
    def style_ligne(self):
        return self.sousOptions(OptionsStyleLigne())
    def code(self,language=None):
        a = []
        if language=="pstricks":
            for op in self.DicoOptions.keys():
                a.append(op+"="+self.DicoOptions[op])
                a.append(",")
            del a[-1:]
            return "".join(a)
        if language=="tikz":
            a=[]
            for at in ["linecolor","linestyle"]:
                k=self.DicoOptions[at]
                if k and k!="none" :
                    a.append(k)
            return ",".join(a)
    def __getitem__(self,opt):
        return self.DicoOptions[opt]

class GraphOfAnObject(object):
    """ This class is supposed to be used to create other "GraphOfA..." by inheritance. It is a superclass. """
    # self.record_add_to_bb is a list of points to be added to the bounding box.
    # Typically, when a point has a mark, one can only know the size of the box at the end of the picture 
    #(because of xunit, yunit that change when using dilatation)
    # Thus if one wants to draw the bounding box, it has to be done at the end.
    def __init__(self,obj):
        self.obj = obj
        self.parameters = Parameters()
        self.wavy = False
        self.waviness = None
        self.options = Options()
        self.marque = False
        self.draw_bounding_box=False
        self.add_option("linecolor=black")
        self.add_option("linestyle=solid")
        self.record_add_to_bb=[]         
        self.separator_name="DEFAULT"
        self.in_math_bounding_box=True
        self.in_bounding_box=True
        self._draw_edges=False
        self.added_objects=[]
    def draw_edges(self):
        self._draw_edges=True
    def wave(self,dx,dy):                   # dx is the wave length and dy is the amplitude
        self.wavy = True
        self.waviness = Waviness(self,dx,dy)
    def get_mark(self,dist,angle,text,mark_point=None,automatic_place=False,added_angle=None):

        """
        If you want to put a mark on an object
        P.put_mark(0.1,-90,"text",automatic_place=(pspict,"N"))

        mark_point is a function which returns the position of the mark point.

        If you give no position (i.e. no "S","N", etc.) the position will be automatic regarding the angle.
        """
        if automatic_place==False:
            raise "You have to pass a pspicture"
        if self.marque:
            print("This is a second (or more) mark on the same point")
        self.marque = True
        autom=automatic_place
        third=None
        if not isinstance(autom,tuple):
            print("You should not use 'automatic_place' like that")
            pspict=autom
            position=""
        else :
            pspict=automatic_place[0]
            position=automatic_place[1]
            if position=="for axes":
                third=automatic_place[2]

        if angle is None :
            try :
                angle=self.advised_mark_angle(pspict=pspict)
            except AttributeError :
                angle=self.angle().degree+90

        if added_angle:
            angle=angle+added_angle
        if position=="" :
            position="corner"
            if isinstance(self,GraphOfAnAngle):
                position="center"
            alpha=AngleMeasure(value_degree=angle).positive()
            deg=alpha.degree
            if deg==0:
                position="W"
            if deg==90:
                position="S"
            if deg==180:
                position="E"
            if deg==180+90:
                position="N"
        mark=Mark(self,dist,angle,text,automatic_place=(pspict,position,third),mark_point=mark_point)

        # We need to immediately add the LaTeX lines about box sizes, no waiting fig.conclude. This is to allow several pictures
        # to use the same points and marks.
        # By the way, one cannot compute the self.mark.central_point() here because the axes are not yet computed.

        if not isinstance(pspict,list):
            pspict=[pspict]
        if automatic_place :
            for psp in pspict:
                dimx,dimy = psp.get_box_size(text)
        return mark

        # No more like that   (September, 21, 2014)
        #self.mark._central_point=self.mark.central_point()
        #if not self.mark._central_point :
        #    print(self)
        #    raise
    def put_mark(self,dist,angle,text,mark_point=None,automatic_place=False,added_angle=None):
        mark=self.get_mark(dist,angle,text,mark_point=None,automatic_place=automatic_place,added_angle=added_angle)
        self.added_objects.append(mark)
        self.mark=mark
    def add_option(self,opt):
        self.options.add_option(opt)
    def get_option(opt):
        return self.options.DicoOptions[opt]
    def remove_option(opt):
        self.options.remove_option(opt)
    def merge_options(self,graph):
        """
        takes an other object GraphOfA... and merges the options as explained in the documentation
        of the class Options. That merge takes into account the attributes "color", "style", wavy
        """
        self.parameters = graph.parameters
        self.options.merge_options(graph.options)
        self.wavy = graph.wavy
        self.waviness = graph.waviness
    def conclude_params(self):
        """
        However the better way to add something like
        linewidth=1mm
        to a graph object `seg` is to use
        seg.add_option("linewidth=1mm")
        """
        oo=self.parameters.other_options
        for opt in oo.keys():
            self.add_option(opt+"="+oo[opt])
        self.parameters.add_to_options(self.options)
    def params(self,language,refute=[]):
        self.conclude_params()
        l=[]
        for attr in [x for x in self.parameters.interesting_attributes if x not in refute]:
            value=self.parameters.__getattribute__(attr)
            if value != None:
                l.append(attr+"="+str(value))
        code=",".join(l)
        if language=="tikz":
            code=code.replace("plotpoints","samples")
        return code
        #return self.options.code(language=language)
    def action_on_pspict(self,pspict):
        for obj in self.added_objects :
            pspict.DrawGraphs(obj)
        # One cannot make try ... except AttributeError since it should silently pass a real AttributeError in the implementation if specific_action_on_pspict
        if "specific_action_on_pspict" in dir(self):
            self.specific_action_on_pspict(pspict)
    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def latex_code(self,pspict,language=None):
        return ""

def visual_length(v,l,xunit=None,yunit=None,pspict=None):
    """
    Return a vector in the direction of v that has *visual* length l taking xunit and yunit into accout.

    In the following example, the cyan vectors are deformed the the X-dilatation while the
    brown vectors are of length 2.

    .. literalinclude:: phystrickstestVisualLength.py
    .. image:: Picture_FIGLabelFigtestVisualLengthPICTtestVisualLength-for_eps.png

    """
    if pspict:
        xunit=pspict.xunit
        yunit=pspict.yunit
    Dx=v.Dx
    Dy=v.Dy
    if not v.vertical :
        slope=v.slope
        x=l/sqrt(xunit**2+slope**2*yunit**2)
        if Dx<0:
            x=-x
        y=slope*x
    else:
        x=0
        y=l/yunit
        if Dy<0:
            y=-l/yunit
    if hasattr(v,"I"):
        from phystricks import AffineVector
        from phystricks import Vector
        return AffineVector(v.I,v.I+Vector(x,y))
    else:
        from phystricks import Vector
        return Vector(x,y)

def visual_polar(P,r,theta,pspict=None):
    """
    Return a point at VISUAL coordinates (r,theta) from the point P.

    theta is given in degree.
    """
    xunit=pspict.xunit
    yunit=pspict.yunit
    alpha=pi*theta/180
    v=Vector( cos(alpha)/xunit,sin(alpha)/yunit  )
    w=visual_length(v,r,pspict=pspict)
    return P+w

def visual_polar_coordinates(P,pspict=None):
    """
    return the visual polar coordinates of 'P'
    """
    if isinstance(pspict,list):
        xu=pspict[0].xunit
        yu=pspict[0].xunit
        xunits=[ psp.xunit==xu for psp in pspict ]
        yunits=[ psp.yunit==yu for psp in pspict ]
        if sum(xunits)==len(xunits) and sum(yunits)==len(yunits):
            xunit=xu
            yunit=yu
        else :
            print("Probably more than one picture with different dilatations ...")
            raise ValueError
    else :
        xunit=pspict.xunit
        yunit=pspict.yunit
    Q=Point(xunit*P.x,yunit*P.y)
    return Q.polar_coordinates()

class GraphOfASingleAxe(GraphOfAnObject):
    def __init__(self,C,base,mx,Mx,pspict=None):
        GraphOfAnObject.__init__(self,self)
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
        return "<GraphOfASingleAxe: C={0} base={1} mx={2} Mx={3}>".format(self.C,self.base,self.mx,self.Mx)

# TODO : to fill portion of circle should be as easy as:
#    CerB=Cer.graph(alpha,alpha+90)
#    CerB.parameters.filled()
#    CerB.parameters.fill.color="blue"
# See the picture RouletteACaVVA

class GraphOfACircle(GraphOfAnObject):
    """
    This is a circle, or an arc of circle.

    INPUT:

    - ``center`` - a point, the center of the circle.

    - ``radius`` - a number, the radius of the circle.

    - ``self.angleI`` - (default=0) the beginning angle of the arc (degree).

    - ``self.angleF`` - (default=360) the ending angle of the arc (degree).
    - ``visual`` - (default=False) if 'True', the radius is taken as a 'visual' length.


    OUTPUT:

    A circle ready to be drawn.

    EXAMPLES::

        sage: from phystricks import *
        sage: circle=Circle(Point(-1,1),3)
        sage: print unify_point_name(circle.pstricks_code())
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-4.00000000000000,1.00000000000000){Xaaaa}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-1.00000000000000,1.00000000000000){Xaaab}
        \pstCircleOA[linestyle=solid,linecolor=black]{Xaaab}{Xaaaa}
    
    If you want the same circle but between the angles 45 and 78::
        
        sage: other_circle=circle.graph(45,78)
        sage: print unify_point_name(other_circle.pstricks_code())
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.12132034355964,3.12132034355964){Xaaaa}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-0.376264927546722,3.93444280220142){Xaaab}
        \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](-1.00000000000000,1.00000000000000){Xaaac}
        \pstArcOAB[linestyle=solid,linecolor=black]{Xaaac}{Xaaaa}{Xaaab}

    """
    def __init__(self,center,radius,angleI=0,angleF=360,visual=False,pspict=None):
        self.center = center
        self.radius = radius
        GraphOfAnObject.__init__(self,self)
        self.diameter = 2*self.radius
        self._parametric_curve=None
        self.angleI = AngleMeasure(value_degree=angleI,keep_negative=True)
        self.angleF = AngleMeasure(value_degree=angleF,keep_negative=True)
        a=numerical_approx(self.angleI.degree)
        b=numerical_approx(self.angleF.degree)
        self.visual=visual
        self.pspict=pspict
    @lazy_attribute
    def equation(self):
        """
        Return the equation of `self`.

        OUTPUT:

        an equation.

        EXAMPLES::

            sage: from phystricks import *
            sage: circle=Circle(Point(0,0),1)
            sage: circle.equation()
            x^2 + y^2 - 1 == 0

        ::

            sage: circle=CircleOA(Point(-1,-1),Point(0,0))
            sage: circle.equation()
            (y + 1)^2 + (x + 1)^2 - 2 == 0
        """
        x,y=var('x,y')
        if not self.visual :
            return (x-self.center.x)**2+(y-self.center.y)**2-self.radius**2==0
        Rx=self.radius/self.pspict.xunit
        Ry=self.radius/self.pspict.yunit
        return (x-self.center.x)**2/Rx**2+(y-self.center.y)**2/Ry**2==1
    def phyFunction(self):
        """
        return the function corresponding to
        the graph of the *upper* part of the circle
        """
    def parametric_curve(self,a=None,b=None):
        """
        Return the parametric curve associated to the circle.

        If optional arguments <a> and <b> are given, return the corresponding graph between the values a and b of the angle.

        The parameter of the curve is the angle in radian.
        """
        if self._parametric_curve is None :
            x=var('x')
            if self.visual is True:
                if self.pspict is None :
                    print("You are trying to draw something with 'visual==True' when not giving a pspict")
                    raise ValueError
                f1 = phyFunction(self.center.x+self.radius*cos(x)/self.pspict.xunit)
                f2 = phyFunction(self.center.y+self.radius*sin(x)/self.pspict.yunit)
            else :
                f1 = phyFunction(self.center.x+self.radius*cos(x))
                f2 = phyFunction(self.center.y+self.radius*sin(x))
            try :
                ai=self.angleI.radian
                af=self.angleF.radian
            except AttributeError:
                ai=self.angleI
                af=self.angleF
            self._parametric_curve = ParametricCurve(f1,f2,(ai,af))
        curve=self._parametric_curve
        curve.parameters=self.parameters.copy()
        if a==None :
            return curve
        else :
            return curve.graph(a,b)
    def get_point(self,theta,advised=True,numerical=False):
        """
        Return a point at angle <theta> (degree) on the circle. 
        
        INPUT:
        - ``theta`` - the angle given in degree.
        """
        return self.parametric_curve().get_point(radian(theta,numerical=numerical),advised=advised)
    def get_regular_points(self,mx,Mx,l,advised=True):
        """
        return regularly spaced points on the circle

        INPUT:

        - ``mx`` - initial angle (degree).
        - ``Mx`` - final angle (degree).
        - ``l`` - distance between two points (arc length).
        - ``advised`` - (default=True) if True, compute an advised mark angle for each point
                                        this is CPU-intensive.

        OUTPUT:
        a list of points

        EXAMPLES::

            sage: from phystricks import *
            sage: C=Circle(Point(0,0),2)
            sage: pts=C.get_regular_points(0,90,1)
            sage: [str(p) for p in pts]
            ['<Point(2,0)>', '<Point(2*cos(1/2),2*sin(1/2))>', '<Point(2*cos(1),2*sin(1))>', '<Point(2*cos(3/2),2*sin(3/2))>']

        """
        Dtheta=(180/pi)*(l/self.radius)
        if Dtheta==0:
            raise ValueError,"Dtheta is zero"
        pts=[]
        from numpy import arange
        theta=arange(mx,Mx,step=Dtheta)
        return [self.get_point(t,advised) for t in theta]
    def get_tangent_vector(self,theta):
        return PolarPoint(1,theta+90).origin(self.get_point(theta,advised=False))
    def get_tangent_segment(self,theta):
        """
        Return a tangent segment at point (x,f(x)).
        
        The difference with self.get_tangent_vector is that self.get_tangent_segment returns a segment that will
        be symmetric. The point (x,f(x)) is the center of self.get_tangent_segment.
        """
        v=self.get_tangent_vector(theta)
        mv=-v
        return Segment(mv.F,v.F)
    def get_normal_vector(self,theta):
        """
        Return a normal vector at the given angle 
        
        INPUT:

        - ``theta`` - an angle in degree or :class:`AngleMeasure`.

        OUTPUT:

        An affine vector

        EXAMPLES::

            sage: from phystricks import *
            sage: C=Circle(Point(0,0),2)
            sage: print C.get_normal_vector(45)
            <vector I=<Point(sqrt(2),sqrt(2))> F=<Point(3/2*sqrt(2),3/2*sqrt(2))>>

        """
        v = PolarPoint(1,theta).origin(self.get_point(theta,advised=False))
        v.arrow_type="vector"
        return v
    # Here, angleI and angleF are given in degree while parametric_plot uses radian.
    def get_minmax_data(self,angleI,angleF,n=3):
        deb = radian(angleI)
        fin = radian(angleF)
        return MyMinMax(self.parametric_curve().get_minmax_data(deb,fin),n)
    def xmax(self,angleI,angleF):
        return self.get_minmax_data(angleI,angleF)['xmax']
    def xmin(self,angleI,angleF):
        return self.get_minmax_data(angleI,angleF)['xmin']
    def ymax(self,angleI,angleF):
        return self.get_minmax_data(angleI,angleF)['ymax']
    def ymin(self,angleI,angleF):
        return self.get_minmax_data(angleI,angleF)['ymin']
    def graph(self,angleI,angleF):
        """
        Return a graph of the circle between the two angles given in degree
        """
        C = GraphOfACircle(self.center,self.radius,angleI=angleI,angleF=angleF,visual=self.visual,pspict=self.pspict)
        C.parameters=self.parameters.copy()
        return C
    def __str__(self):
        return "<Circle, center=%s, radius=%s>"%(self.center.__str__(),str(self.radius))
    def copy(self):
        """
        Return a copy of the object as geometrical object.
        
        It only copies the center and the radius. In particular
        the following are not copied:

        - style of drawing.

        - initial and final angle if `self` is an arc.

        EXAMPLES:

        Python copies by assignation::

            sage: from phystricks import *
            sage: c1=Circle( Point(1,1),2 )
            sage: c2=c1
            sage: c2.center=Point(3,3)
            sage: print c1.center
            <Point(3,3)>

        The method :func:`copy` pass through::

            sage: c1=Circle( Point(1,1),3 )
            sage: c2=c1.copy()
            sage: c2.center=Point(3,3)
            sage: print c1.center
            <Point(1,1)>

        NOTE:

        Due to use of `lazy_attribute`, it is not recommended to change the center of
        a circle after having defined it.

        """
        return Circle(self.center,self.radius)
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        if not pspict:
            raise TypeError,"You have to pass a pspict in order to compute the bounding box"
        a=simplify_degree(self.angleI,keep_max=True,number=True)
        b=simplify_degree(self.angleF,keep_max=True,number=True)
        if self.angleI<self.angleF:
            angleI=min(a,b)
            angleF=max(a,b)   
        else :
            angleI=max(a,b)
            angleF=min(a,b)+360
        pI=self.get_point(angleI)
        pF=self.get_point(angleF)
        bb = BoundingBox(self.center,self.center)
        bb.append(pI,pspict)
        bb.append(pF,pspict)
        if angleI==0:
            bb.addX(self.center.x+self.radius)
        if angleI<90 and angleF>90 :
            bb.addY(self.center.y+self.radius)
        if angleI<180 and angleF>180 :
            bb.addX(self.center.x-self.radius)
        if angleI<270 and angleF>270 :
            bb.addY(self.center.y-self.radius)
        return bb
    def latex_code(self,language=None,pspict=None):
        alphaI = radian(self.angleI,number=True,keep_max=True)
        alphaF = radian(self.angleF,number=True,keep_max=True)

        # self.angleI and self.angleF should be AngleMeasure, but sometimes the user
        #    writes something like 
        #   C.angleI=20

        if isinstance(self.angleF,AngleMeasure):
            f=self.angleF.degree
        else :
            f=self.angleF
        if f==360:        # Because the function radian simplifies modulo 2pi.
            alphaF=2*pi
        G = self.parametric_curve(alphaI,alphaF)
        G.parameters=self.parameters.copy()
        G.parameters.plotpoints=500

        a=[]
        if self.parameters._filled or self.parameters._hatched:
            custom=CustomSurface( [self.parametric_curve(alphaI,alphaF)] )
            custom.parameters=self.parameters.copy()
            a.append(custom.latex_code(language=language,pspict=pspict))

        if self.wavy:
            waviness = self.waviness
            G.wave(waviness.dx,waviness.dy)
            a.append( G.latex_code(language=language,pspict=pspict))
        else :
            a.append( G.latex_code(language=language,pspict=pspict))
        return "\n".join(a)

def OptionsStyleLigne():
    return ["linecolor","linestyle"]

class Waviness(object):
    """
    This class contains the informations about the waviness of a curve. It takes as argument a GraphOfAphyFunction and the parameters dx, dy of the wave.
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

class Mark(object):
    def __init__(self,graph,dist,angle,text,mark_point=None,automatic_place=False):
        """
        Describe a mark (essentially a P on a point for example)
        angle is given in degree or AngleMeasure


        This class should not be used by the end-user.

        INPUT:

        - ``graph`` - the graph that it marked. This is usually a point but it can be
                        anything that has a `mark_point` method.
        - ``dist`` - the distance between `graph.mark_point()` and the mark.
        - ``angle`` - the angle
        - ``text`` - the text to be printed on the mark. This is typically a LaTeX stuff like "$P$".
        - ``automatic_place`` - this is a tuple (pspict,anchor) where pspict is the pspicture
                                in which we are working and ̣`anchor` is one of "corner","N","S","W","E" 
                                or special cases (see below).

                        - "corner" will put the mark at the distance such that the corner of the 
                          bounding box is at the (relative) position (dist;angle) instead
                          of the center of the mark.

                        - "N" will put the mark in such a way that the center of the north
                          side of the bounding box is at the position (dist;angle).

                        - "for axes". In this case we expect to have a 3-tuple `(pspict,"for axes",segment)`
                          where `segment` is a segment (typically the segment of an axe).
                          In this case, we suppose `self.angle` to be orthogonal to the segment.
                          The mark will be put sufficiently far for the bounding box not to cross the segment.

                          What is done is that the closest corner of the bounding box is at
                          position (dist;angle) from the point.

        """
        self._central_point=None
        self.mark_point=mark_point
        self.graph = graph
        self.parent = graph
        self.angle = angle
        self.dist = dist
        self.text = text
        self.angle = angle
        self.automatic_place=automatic_place
        alpha=radian(angle)
        if isinstance(alpha,AngleMeasure):
            self.x=self.dist*cos(alpha.radian)
            self.y=self.dist*sin(alpha.radian)
        else :
            self.x=self.dist*cos(alpha)
            self.y=self.dist*sin(alpha)
    def central_point(self,pspict=None):
        """
        return the central point of the mark, that is the point where the mark arrives.

        The central point of the mark is computed from self.graph.mark_point()
        Thus an object that wants to accept a mark needs a method mark_point that returns the point on which the mark will be put.
        """
        if self._central_point:
            return self._central_point
        if self.mark_point :
            graph_mark_point=self.mark_point
        else :
            try :
                graph_mark_point=self.graph.mark_point(pspict=pspict)
            except TypeError :          # Happens when mark_point is redefined as a 'lambda' function
                                        #  or when an other TypeError is raised ...
                graph_mark_point=self.graph.mark_point()
   
        default=graph_mark_point.get_polar_point(self.dist,self.angle,pspict)

        if self.automatic_place :
            pspict=self.automatic_place[0]
            position=self.automatic_place[1]

            # Suppressed on September, 10, 2014
            #except TypeError :
            #    pspict=self.automatic_place
            #    position="corner"

            # The idea here is to allow to use the same point in several pictures and to ask
            # each figure to remember the box size.
            if not isinstance(pspict,list):
                pspict=[pspict]

            for psp in pspict:
                dimx,dimy = psp.get_box_size(self.text)
                dimx=float(dimx)/psp.xunit
                dimy=float(dimy)/psp.yunit

            if position=="for axes":
                seg=self.automatic_place[2]
                alpha=seg.angle().radian
                d=self.dist+0.5*max(dimx*sin(alpha),dimy*cos(alpha))
                beta=degree(-pi/2+alpha)
                beta=self.angle
                return graph_mark_point.get_polar_point(d,beta)

            if position=="center":
                return default

            if position=="corner":
                if self.x>=0:
                    lx=dimx*0.5
                if self.x<0:
                    lx=-dimx*0.5
                if self.y>=0:
                    ly=dimy*0.5
                if self.y<0:
                    ly=-dimy*0.5
                return default.translate(lx,ly)
            if position=="N":
                return default.translate(0,-dimy*0.5)
            if position=="S":
                return default.translate(0,dimy*0.5)
            if position=="W":
                return default.translate(dimx*0.5,0)
            if position=="E":
                return default.translate(-dimx*0.5,0)
            print("Something wrong. I think the 'position' argument is not good :",position)
            raise ValueError
        else :
            return default
    def math_bounding_box(self,pspict=None):
        """
        Return the mathematics bounding box of its base object.

        A mark has non own math_bounding_box because we do not want the axes to fit the marks.
        This is the deep difference between math_bounding_box and bounding_box. We want the
        marks to be fit in the bounding_box since if not the mark risks to be cut
        in the pdf/png version.
        """
        return self.graph.math_bounding_box(pspict)
    def bounding_box(self,pspict=None):
        central_point=self.central_point(pspict)
        if not central_point:
            print(self.parent)
            raise
        bb=BoundingBox(central_point,central_point)
        dimx,dimy=pspict.get_box_size(self.text)
        try :
            dimx=float(dimx)/pspict.xunit
            dimy=float(dimy)/pspict.yunit
        except AttributeError:
            print "Try to pass a pspicture when computing the bounding box of",type(self)
        pt1=Point(central_point.x-dimx/2,central_point.y-dimy/2) 
        pt2=Point(central_point.x+dimx/2,central_point.y+dimy/2)
        #bb.AddPoint(pt1)
        #bb.AddPoint(pt2)
        bb.add_object(pt1,pspict)
        bb.add_object(pt2,pspict)
        bb.parent=self
        return bb
    def action_on_pspict(self,pspict=None):
        pass
    def pstricks_code(self,pspict=None):
        l=[]
        central_point=self.central_point(pspict)
        #TODO : Use create_PSpoint instead of \pstGeonode.
        l.append("\pstGeonode[]"+central_point.coordinates(numerical=True,pspict=pspict)+"{"+central_point.psName+"}")
        l.append(r"\rput({0}){{\rput({1};{2}){{{3}}}}}".format(central_point.psName,"0",0,self.text))
        return "\n".join(l)
    def tikz_code(self,pspict=None):
        central_point=self.central_point(pspict)
        code="\draw "+central_point.coordinates(numerical=True,pspict=pspict)+" node {"+self.text+"};"
        return code
    def latex_code(self,language=None,pspict=None):
        if language=="pstricks":
            return self.pstricks_code(pspict=pspict)
        if language=="tikz":
            return self.tikz_code(pspict=pspict)

class FillParameters(object):
    """
    Represent the parameters of filling a surface.
    """
    def __init__(self):
        self.color = "lightgray"
        self.style = "solid"
    def add_to_options(self,opt):
        """
        add `self` to a set of options.

    
        INPUT:

        - ``opt`` - an instance of :class:`Options`.

        OUTPUT:

        Return `opt` with added properties.

        EXAMPLES::

            sage: from phystricks.BasicGeometricObjects import *
            sage: opt=Options()
            sage: fill=FillParameters()
            sage: fill.color="blue"
            sage: fill.add_to_options(opt)
            sage: opt.code()
            u'fillcolor=blue,fillstyle=solid'

        ::

            sage: fill.style="MyStyle"
            sage: fill.add_to_options(opt)
            sage: opt.code()
            u'fillcolor=blue,fillstyle=MyStyle'

        """
        if self.color :
            opt.add_option("fillcolor=%s"%str(self.color))
        if self.style :
            opt.add_option("fillstyle=%s"%str(self.style))

class HatchParameters(object):
    """Same as FillParameters, but when one speaks about hatching"""
    def __init__(self):
        self.color = None
        self._crossed = False
        self.angle = -45
    def crossed(self):
        self._crossed=True
    def add_to_options(self,opt):
        opt.add_option("hatchangle=%s"%str(self.angle))
        if self._crossed:
            opt.add_option("fillstyle=crosshatch")
        else:
            opt.add_option("fillstyle=vlines")
        if self.color :
            opt.add_option("hatchcolor=%s"%str(self.color))

class Parameters(object):
    def __init__(self):
        self.color = None           # I take into account in SurfaceBetweenParametricCurves that the default values are None
        self.symbol = None
        self.style = None
        self.plotpoints=None
        self.dotangle=None
        self.fill=FillParameters()
        self.hatch=HatchParameters()
        self.other_options={}
        self._filled=False
        self._hatched=False
        self.visual=None        # If True, it means that one wants the object to be non deformed by xunit,yunit
        self.interesting_attributes=["color","symbol","style","plotpoints","dotangle"]
    def copy(self):
        cop=Parameters()
        cop.visual=self.visual
        cop._hatched=self._hatched
        cop._filled=self._filled
        cop.hatch=self.hatch
        cop.fill=self.fill
        cop.plotpoints=self.plotpoints
        cop.style=self.style
        cop.symbol=self.symbol
        cop.color=self.color
        cop.dotangle=self.dotangle
        return cop
    def filled(self):
        self._filled=True
    def hatched(self):
        self._hatched=True
    def add_option(self,key,value):
        # TODO : This method should be used as the other "add_option" methods in other classes.
        """
        Add options that will be added to to code.

            sage: from phystricks.BasicGeometricObjects import *
            sage: seg=Segment(Point(0,0),Point(1,1))
            sage: seg.parameters.add_option("linewidth","1mm")
            sage: seg.pstricks_code()
            klmklm

        However the better way to add something like
        linewidth=1mm
        to a graph object `seg` is to use
        seg.add_option("linewidth=1mm")
        """
        self.other_options[key]=value
    def add_to_options(self,opt):
        """
        Add to the object `opt` (type Option) the different options that correspond to the parameters.

        In an imaged way, this method adds `self` to the object `opt`.
        """
        if self.color :
            opt.add_option("linecolor=%s"%str(self.color))
        if self.style :
            opt.add_option("linestyle=%s"%str(self.style))
        if self.symbol :
            opt.add_option("PointSymbol=%s"%str(self.symbol))
        if self._filled:
            self.fill.add_to_options(opt)
        if self._hatched:
            self.hatch.add_to_options(opt)
    def add_to(self,parameters,force=False):
        """
        Add `self` to `parameters`.

        Where `self` has non-trivial or non-default values, put these values to `parameters`

        EXAMPLES ::

            sage: from phystricks.BasicGeometricObjects import *
            sage: p1=Parameters()
            sage: p1.color="red"
            sage: p1.symbol="A"

            sage: p2=Parameters()
            sage: p2.style="solid"
            sage: p2.symbol="B"
            sage: p2.filled()
            sage: p2.fill.color="cyan"

            sage: p2.add_to(p1)
            sage: print p1.color,p1.style,p1.symbol,p1._filled,p1.fill.color
            red solid A True cyan

        By default, it only fills the "empty" slots (None and False). 
        If `force` is True, it fills all.
        """
        for attr in parameters.interesting_attributes:
            if (parameters.__getattribute__(attr) in [None,False]) or force :
                parameters.__dict__[attr]=self.__getattribute__(attr)
        parameters.fill=self.fill
        parameters.hatch=self.hatch
    def replace_to(self,parameters):
        """
        The same as :func:`add_to`, but replace also non-trivial parameters

        EXAMPLES::

            sage: from phystricks.BasicGeometricObjects import *
            sage: p1=Parameters()
            sage: p1.color="red"
            sage: p1.symbol="A"

            sage: p2=Parameters()
            sage: p2.style="solid"
            sage: p2.symbol="B"
            sage: p2.filled()
            sage: p2.fill.color="cyan"

            sage: p2.replace_to(p1)
            sage: print p1.color,p1.style,p1.symbol,p1._filled,p1.fill.color
            red solid B True cyan

        Notice that here `p1.style` is replace while it was not replaced by the function 
        :func:`add_to`.
        """
        for attr in parameters.__dict__.keys():
            candidate=self.__getattribute__(attr)
            if candidate is not None :
                parameters.__dict__[attr]=candidate
        parameters.fill=self.fill
        parameters.hatch=self.hatch

def extract_interval_information(curve):
    """
    return the interval of the curve.

    That is the initial and final value of the parameter
    of `curve` if that is a :class:`ParametricCurve` and
    the initial and final values of `x` if this the the graph
    of a function.

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
        # we are thus returning 'curve.angleI.radian' instead of 'curve.angleI' (November 29, 2014)
        return curve.angleI.radian,curve.angleF.radian
    return None,None

class GraphOfAPoint(GraphOfAnObject):
    NomPointLibre = PointsNameList()

    def __init__(self,a,b):
        self.x=SR(a)
        self.y=SR(b)
        GraphOfAnObject.__init__(self,self)
        #self.psName = point.psName      # The psName of the point is erased when running Point.__init__
                                         # This line is no more useful (April 29 2011)
        self.point = self.obj
        self.add_option("PointSymbol=*")
        self._advised_mark_angle=None
        self.psName=GraphOfAPoint.NomPointLibre.next()
        
        # The following is a good test, but one cannot use it because
        # sometimes we need the projection of a point on an axe before to compute the bounding box.
        # In that case, the points defining the axe could still have coordinates like 1000 because it is the "default"
        # size of a bounding box.
        #if max(abs(self.x),abs(self.y))>500:
        #    raise ValueError,"I don't believe you want a point with coordinates {0},{1}".format(self.x,self.y)

        ax=abs(numerical_approx(self.x))
        if ax<0.00001 and ax>0 :
            self.x=0
        ay=abs(numerical_approx(self.y))
        if ay<0.00001 and ay>0 :
            self.y=0
    def advised_mark_angle(self,pspict):
        if self._advised_mark_angle:
            return self._advised_mark_angle
        else :
            print("No advised mark angle for this point")
            raise AttributeError
    def numerical_approx(self):
        return Point(numerical_approx(self.x),numerical_approx(self.y))
    def projection(self,seg,direction=None,advised=False):
        """
        Return the projection of the point on the given segment.

        INPUT:

        - ``seg`` - a segment
        - ``direction`` - (default=None) a vector. If given, we use a projection parallel to
                            `vector` instead of the orthogonal projection.

        OUTPUT:

        a point.

        EXAMPLES:

        Return a point even if the projections happens to lies outside the segment::

            sage: from phystricks import *
            sage: s1=Segment( Point(0,0),Point(2,1) )
            sage: print Point(3,-1).projection(s1)
            <Point(2,1)>
            sage: print Point(5,0).projection(s1) 
            <Point(4,2)>

        You can project on a vector::

            sage: print Point(5,0).projection(Vector(2,1))
            <Point(4,2)>

        Computations are exact::

            sage: v=Vector(2,1)
            sage: print Point(sqrt(2),pi).projection(v)
            <Point(2/5*pi + 4/5*sqrt(2),1/5*pi + 2/5*sqrt(2))>

        """
        try :
            seg=seg.segment(projection=True)
        except AttributeError :
            pass

        if direction is None:
            direction=seg.get_normal_vector()

        seg2=direction.fix_origin(self)
        P=main.Intersection(seg,seg2)[0]
        if advised :
            P._advised_mark_angle=seg.angle().degree+90
        return P
    def symmetric_by(self,Q):
        """
        return the central symmetry  with respect to 'Q'
        """
        v=Q-self
        return Q+v
    def get_polar_point(self,r,theta,pspict=None):
        """
        Return the point located at distance r and angle theta from point self.

        INPUT:

        - ``r`` - A number.

        - ``theta`` - the angle (degree or :class:`AngleMeasure`).

        - ``pspict`` - the pspicture in which the point is supposed to live. If `pspict` is given, we compute the deformation due to the dilatation.  Be careful: in that case `r` is given as absolute value and the visual effect will not be affected by dilatations.

        OUTPUT: A point.

        EXAMPLES::

            sage: from phystricks import *
            sage: P=Point(1,2)
            sage: print P.get_polar_point(sqrt(2),45)
            <Point(2,3)>

        """
        if isinstance(r,SmallComputations.AngleMeasure):
            raise TypeError, "This should not happen"
        alpha=radian(theta,number=True)
        if pspict:
            A=pspict.xunit
            B=pspict.yunit
            xP=r*cos(alpha)/A
            yP=r*sin(alpha)/B
            return self.translate(Vector(xP,yP))
        return Point(self.x+r*cos(alpha),self.y+r*sin(alpha))
    def value_on_line(self,line):
        """
        Return the value of the equation of a line on `self`.

        If $f(x,y)=0$ is the equation of `line`, return the number f(self.x,self.y).

        NOTE:

        The object `line` has to have an attribute line.equation

        EXAMPLE::

            sage: from phystricks import *
            sage: s=Segment(Point(0,1),Point(1,0))
            sage: s.equation()
            x + y - 1 == 0
            sage: P=Point(-1,3)
            sage: P.value_on_line(s)
            1   

        It allows to know if a point is inside or outside a circle::

            sage: circle=Circle(Point(-1,2),4)
            sage: Point(1,1).value_on_line(circle)
            -11

        ::

            sage: Point(1,sqrt(2)).value_on_line(circle)
            (sqrt(2) - 2)^2 - 12

        """
        x,y=var('x,y')
        return line.equation.lhs()(x=self.x,y=self.y)
    def translate(self,a,b=None):
        """
        translate `self`.

        EXAMPLES::

        You can translate by a :func:`Vector`::

            sage: from phystricks import *
            sage: v=Vector(2,1)                        
            sage: P=Point(-1,-1)
            sage: print P.translate(v)
            <Point(1,0)>

        An :func:`AffineVector` is accepted::

            sage: w=AffineVector( Point(1,1),Point(2,3) )
            sage: print P.translate(w)
            <Point(0,1)>

        You can also directly provide the coordinates::

            sage: print P.translate(10,-9)
            <Point(9,-10)>

        Or the :func:`Point` corresponding to the translation vector::

            sage: print P.translate( Point(3,4)  )
            <Point(2,3)>

        Translation by minus itself produces zero::

            sage: x,y=var('x,y')
            sage: P=Point(x,y)
            sage: print P.translate(-P)
            <Point(0,0)>

        """
        if b==None :
            v=a
        else :
            v=Vector(a,b)
        return self+v
    def origin(self,p):
        return AffineVector(p,Point(p.x+self.x,p.y+self.y))
    def Vector(self):
        return AffineVector(Point(0,0),self)
    def norm(self):
        """
        Return the norm of the segment between (0,0) and self.

        This is the radial component in polar coordinates.

        EXAMPLES::

        sage: from phystricks import *
        sage: Point(1,1).norm()
        sqrt(2)
        sage: Point(-pi,sqrt(2)).norm()
        sqrt(pi^2 + 2)
        """
        return Segment(Point(0,0),self).length()
    def length(self):
        """
        The same as self.norm()

        EXAMPLES::

            sage: from phystricks import *
            sage: P=Point(1,1)
            sage: P.length()
            sqrt(2)
        """
        return self.norm()
    # La méthode normalize voit le point comme un vecteur partant de zéro, et en donne le vecteur de taille 1
    def normalize(self,l=None):
        """
        Return a vector of norm <l>. If <l> is not given, take 1.
        """
        unit = self*(1/self.norm())
        if l :
            return unit*l
        return unit
    def default_graph(self,opt):
        """
        Return a default Graph
        
        <opt> is a tuple. The first is the symbol to the point (like "*" or "none").
        The second is a string to be passed to pstricks, like "linecolor=blue,linestyle=dashed".
        """
        P=self.default_associated_graph_class()(self)
        P.parameters.symbol=opt[0]
        P.add_option(opt[1])
        return P
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return GraphOfAPoint             # Graph is also a method of Sage
    def create_PSpoint(self):
        """Return the code of creating a pstgeonode. The argument is a Point of GraphOfAPoint"""
        P = Point(self.x,self.y)
        P.psName = self.psName
        P.parameters.symbol=""
        return P.pstricks_code(None)+"\n"
    def polar_coordinates(self,origin=None):
        """
        Return the polar coordinates of the point as a tuple (r,angle) where angle is AngleMeasure

        EXAMPLES::

            sage: from phystricks import *
            sage: Point(1,1).polar_coordinates()
            (sqrt(2), AngleMeasure, degree=45.0000000000000,radian=1/4*pi)
            sage: Point(-1,1).polar_coordinates()
            (sqrt(2), AngleMeasure, degree=135.000000000000,radian=3/4*pi)
            sage: Point(0,2).polar_coordinates()
            (2, AngleMeasure, degree=90.0000000000000,radian=1/2*pi)
            sage: Point(-1,0).polar_coordinates()
            (1, AngleMeasure, degree=180.000000000000,radian=pi)
            sage: alpha=-pi*(arctan(2)/pi - 2)
            sage: Point(cos(alpha),sin(alpha)).polar_coordinates()
            (1, AngleMeasure, degree=180.000000000000,radian=pi)

        If 'origin' is given, it is taken as origin of the polar coordinates.

        Only return positive angles (between 0 and 2*pi)
        """
        return SmallComputations.PointToPolaire(self,origin=origin)
    def angle(self,origin=None):
        """
        Return the angle of the segment from (0,0) and self.
        """
        return self.polar_coordinates(origin=origin)            # No more degree. February 11, 2015
    def coordinates(self,numerical=False,digits=10,pspict=None):
        """
        Return the coordinates of the point as a string.

        When one coordinate if very small (lower than 0.0001), it is rounded to zero in order to avoid string like "0.2335e-6" in the pstricks code.

        EXAMPLE::

            sage: from phystricks import *
            sage: P=Point(1,3)
            sage: print P.coordinates()
            (1,3)

        If a pspicture is given, we divide by xunit and yunit to normalize.
        """
        if numerical :
            x=numerical_approx(self.x,digits=digits)
            y=numerical_approx(self.y,digits=digits)
        else :
            x = self.x
            y = self.y
        # This precaution in order to avoid something like 0.125547e-6 because pstricks doesn't like that notation.
        if abs(x) < 0.0001 :
            x=0
        if abs(y) < 0.0001 :
            y=0
        if pspict :
            x=x*pspict.xunit
            y=y*pspict.yunit
        return str("("+str(x)+","+str(y)+")")
    def coordinatesBr(self):
        raise DeprecationWarning  # June 23, 2014
        return self.coordinates.replace("(","{").replace(")","}")
    def Affiche(self):
        raise DeprecationWarning  # June 24, 2014
        return self.coordinates()
    def graph_object(self):
        return GraphOfAPoint(self)
    def copy(self):
        return Point(self.x,self.y)
    def mark_point(self,pspict=None):
        return self
    def bounding_box(self,pspict=None):
        """
        return the bounding box of the point including its mark

        A small box of radius 0.1 (modulo xunit,yunit[1]) is given in any case.
        You need to provide a pspict in order to compute the size since it can vary from the place in your document you place the figure.

        [1] If you dont't know what is the "bounding box", or if you don't want to fine tune it, you don't care.
        """
        if pspict==None:
            print("You should consider to give a pspict as argument. Otherwise the boundig box of %s could be bad"%str(self))
            xunit=1
            yunit=1
        else :
            xunit=pspict.xunit
            yunit=pspict.yunit
        Xradius=0.1/xunit
        Yradius=0.1/yunit
        bb = BoundingBox(Point(self.x-Xradius,self.y-Yradius),Point(self.x+Xradius,self.y+Yradius))
        for P in self.record_add_to_bb:
            bb.AddPoint(P)
        return bb
    def math_bounding_box(self,pspict=None):
        """Return a bounding box which include itself and that's it."""
        # Here one cannot use BoundingBox(self.point,self.point) because
        # it creates infinite loop.
        bb=BoundingBox(xmin=self.point.x,xmax=self.point.x,ymin=self.point.y,ymax=self.point.y)
        return bb
    def pstricks_code(self,pspict=None,with_mark=False):
        r"""
        Return the pstricks code of the point

        INPUT:
        - ``with_mark`` - (default : False) if it is true, return the pstrick code
                                of the mark in the same time. This is only used by the axes.
        OUTPUT:
        string

        This function is not supposed to be used by the end-user.

        When the point has a mark, the code of the mark is not included here because 
        :func:`DrawGraph` automatically adds the mark to the list of objects
        to be drawn.
        However, some constructions want to include the pstricks code of points in its own
        pstricks code. In that case we want the code of the mark to be part of the code
        of the point.
        This is the case of the axes. The pstricks code of the axes have to be in one block
        including the markes. For that usage, we use with_mark=True
        
        EXAMPLE::

            sage: from phystricks import *
            sage: P=Point(1,1)
            sage: P.put_mark(0.3,45,"$P$")

        By default the code of the mark does not appears in the code of the point:
        sage: unify_point_name(P.pstricks_code())
        u'\\pstGeonode[PointSymbol=*,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaaa}'

        If we specify with_mark=True, then we see the code of the mark:
        sage: unify_point_name(P.pstricks_code(with_mark=True))
        u'\\pstGeonode[](1.21213203435596,1.21213203435596){Xaaaa}\n\\rput(Xaaaa){\\rput(0;0){$P$}}\n\\pstGeonode[PointSymbol=*,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaab}'
        """
        return "\pstGeonode["+self.params(language="pstricks")+"]"+self.coordinates(numerical=True,pspict=pspict)+"{"+self.psName+"}"
    def tikz_code(self,pspict=None):
        symbol_dict={}
        symbol_dict[None]="$\\bullet$"
        symbol_dict[None]="$\\times$"       # This change of default is from November 24, 2014
        symbol_dict["*"]="$\\bullet$"
        symbol_dict["|"]="$|$"
        symbol_dict["x"]="$\\times$"
        symbol_dict["o"]="$o$"
        symbol_dict["diamond"]="$\diamondsuit$"
        try :
            effective_symbol=symbol_dict[self.parameters.symbol]
        except KeyError:
            effective_symbol=self.parameters.symbol
        if self.parameters.symbol=='none' :
            print("You should use '' instead of 'none'")
        if self.parameters.symbol not in ["none",""]:
            s = "\draw [{2}]  {0} node [rotate={3}] {{{1}}};".format(self.coordinates(numerical=True,pspict=pspict),effective_symbol,self.params(language="tikz",refute=["symbol","dotangle"]),"DOTANGLE")
            if self.parameters.dotangle != None :
                s=s.replace("DOTANGLE",str(self.parameters.dotangle))
            else :
                s=s.replace("DOTANGLE","0")
            return s
        return ""
    def latex_code(self,language=None,pspict=None,with_mark=False):
        l=[]
        if self.marque and with_mark:
            for mark in self.marks_list:
                l.append(self.mark.latex_code(language=language,pspict=pspict))
        if language=="pstricks":
            l.append(self.pstricks_code(pspict=pspict))
        if language=="tikz":
            l.append(self.tikz_code(pspict=pspict))
        return "\n".join(l)
    def __eq__(self,other):
        """
        return True if the coordinates of `self` and `other` are the same.

        INPUT:
        
        - ``other`` - an other point

        OUTPUT:

        boolean

        EXAMPLES:

        The fact to change the properties of a point don't change the equality::

            sage: from phystricks import *
            sage: a=Point(1,1)
            sage: b=Point(1,1)
            sage: b.put_mark(1,1,"$P$")
            sage: a==b
            True
            sage: c=Point(0,0)
            sage: c==a
            False
        """
        if self.x == other.x and self.y==other.y :
            return True
        return False
    def __add__(self,v):
        """
        Addition of a point with a vector is the parallel translation, while addition of a point with an other point is simply
        the addition of coordinates.

        INPUT:

        - ``v`` - a vector or a tuple of size 2

        OUTPUT:

        a new point
        """
        if isinstance(v,tuple) :
            if len(v)==2:
                return Point(self.x+v[0],self.y+v[1])
            else :
                raise TypeError, "Cannot sum %s with %s."%(self,v)
        try :
            dx = v.Dx
            dy = v.Dy
        except AttributeError :
            try :
                dx = v.x
                dy = v.y
            except AttributeError :
                print("VSWooXmhSzY")
                print(v.Dx())
                print(v.Dx)
                raise TypeError, "You seem to add myself with something which is not a Point neither a Vector. Sorry, but I'm going to crash : {},{}".format(v,type(v))
        return Point(self.x+dx,self.y+dy)
    def __sub__(self,v):
        if isinstance(v,tuple):
            if len(v)==2:
                return self+(-v[0],-v[1])
            else :
                raise TypeError, "Cannot sum %s with %s."%(self,v)
        return self+(-v)
    def __neg__(self):
        return Point(-self.x,-self.y)
    def __mul__(self,r):
        return Point(r*self.x,r*self.y)
    def __div__(self,r):
        return Point(self.x/r,self.y/r)
    def __rmul__(self,r):
        return self.__mul__(r)
    def __str__(self):
        return "<Point(%s,%s)>"%(str(self.x),str(self.y))


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
        gr = GraphOfAnImplicitCurve(self,xrange,yrange,plot_points)
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

class GraphOfAnImplicitCurve(GraphOfAnObject,GeometricImplicitCurve):
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
            sage: F=GraphOfAnImplicitCurve(implicit_curve,(x,-1,1),(y,-3,2)).pstricks_code()

    NOTES:

    The get_minmax_data is contributed by the Sage's community here :
    http://ask.sagemath.org/question/359/get_minmax_data-on-implicit_plot
    (thanks to DSM)
    """
    def __init__(self,implicit_curve,xrange,yrange,plot_points=300):
        GraphOfAnObject.__init__(self,implicit_curve)
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
            sage: F.get_minmax_data()
            {'xmin': -1.1890000000000001, 'ymin': -1.1879999999999999, 'ymax': 1.1879999999999999, 'xmax': 1.1890000000000001}
            sage: F.plot_points=10
            sage: F.get_minmax_data()
            {'xmin': -1.1890000000000001, 'ymin': -1.1879999999999999, 'ymax': 1.1879999999999999, 'xmax': 1.1890000000000001}

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

class GraphOfASegment(GraphOfAnObject):
    def __init__(self,A,B,arrow_type="segment"):
        self.I = A
        self.F = B
        self.arrow_type=arrow_type
        GraphOfAnObject.__init__(self,self)
        #self.arrow_list=[]
        self.measure=None
    @lazy_attribute
    def Dx(self):
        return self.F.x-self.I.x
    @lazy_attribute
    def Dy(self):
        return self.F.y-self.I.y
    @lazy_attribute
    def slope(self):        # It was before names "coefficient"
        """
        return the angular coefficient of line.

        This is the coefficient a in the equation
        y = ax + b

        Notice that the result does not depend on the order

        This is not the same as the coefficient a in self.equation
        ax + by + c == 0
        
        of the points.

        OUTPUT:
        a number

        EXAMPLES::

            sage: from phystricks import *
            sage: Segment(Point(0,0),Point(1,1)).slope
            1
            sage: Segment(Point(1,1),Point(0,0)).slope
            1
            sage: Segment(Point(1,2),Point(-1,8)).slope
            -3

        NOTE:

        If the line is vertical, raise a ZeroDivisionError
        """
        return SR(self.Dy)/self.Dx
    @lazy_attribute
    def independent(self):
        """
        return the b in the equation
        y = ax + b

        If the line is vertical, raise an ZeroDivisionError

        EXAMPLES::

            sage: from phystricks import *
            sage: s = Segment(Point(0,3),Point(6,-1))
            sage: s.independent
            3

        sage: Segment(Point(1,2),Point(-1,1)).independent
        3/2
        """
        return self.I.y-self.I.x*(self.slope)
    def get_point(self,x):
        """
        Return the point of abscisses 'x' on the line.
        """
        return Point(x,self.slope*x+self.independent)
    @lazy_attribute
    def vertical(self):
        vert = False
        if self.I.x == self.F.x :
            vert = True
        return vert
    @lazy_attribute
    def horizontal(self):
        horiz = False
        if self.I.y == self.F.y :
            horiz = True
        return horiz
    @lazy_attribute
    def equation(self):
        """
        return the equation of the line under the form
        x + by + c = 0

        Coefficients 'b' and 'c' are numerical approximations. See position : 313628350 in __init__.py

        EXAMPLES::

            sage: from phystricks import *
            sage: Segment(Point(0,0),Point(1,1)).equation
            x - y == 0
            sage: Segment(Point(1,0),Point(0,1)).equation
            x + y - 1 == 0
        """
        if self.vertical :
            self.coefs = [1,0,-self.I.x]
        if self.horizontal :
            self.coefs = [0,1,-self.I.y]
        if not (self.vertical or self.horizontal) :
            self.coefs = [1,-1/self.slope,self.independent/self.slope]
        x,y=var('x,y')
        Ix=numerical_approx(self.I.x)
        Iy=numerical_approx(self.I.y)
        Fx=numerical_approx(self.F.x)
        Fy=numerical_approx(self.F.y)
        coefs=[ numerical_approx(s) for s in self.coefs  ]
        return coefs[0]*x+coefs[1]*y+coefs[2] == 0
    @lazy_attribute
    def length(self):
        """
        return the length of the segment

        EXAMPLES::

            sage: from phystricks import *
            sage: Segment(Point(1,1),Point(2,2)).length
            sqrt(2)

        """
        return Distance(self.I,self.F)
    def advised_mark_angle(self,pspict=None):
        return self.angle()+AngleMeasure(value_degree=90)
    def phyFunction(self):
        if self.horizontal:
            # The trick to define a constant function is explained here:
            # http://groups.google.fr/group/sage-support/browse_thread/thread/e5e8775dd79459e8?hl=fr?hl=fr
            x=var('x')
            fi = SR(A.y).function(x)
            return phyFunction(fi)
        if not (self.vertical or self.horizontal) :
            x=var('x')
            return phyFunction( self.slope*x+self.independent )
    def symmetric_by(self,O):
        """
        return a segment wich is symmetric to 'self' with respect to the point 'O'
        """
        A=self.I.symmetric_by(O)
        B=self.F.symmetric_by(O)
        return Segment(A,B)
    def inside_bounding_box(self,bb=None,xmin=None,xmax=None,ymin=None,ymax=None):
        """
        Return a segment that is the part of self contained inside the given bounding box.
        """
        if bb:
            xmin=bb.xmin
            xmax=bb.xmax
            ymin=bb.ymin
            ymax=bb.ymax
        if self.vertical:
            return Segment( Point(self.I.x,ymin),Point(self.I.y,ymax)  )
        if self.horizontal:
            return Segment( Point(xmin,self.I.y),Point(xmax,self.I.y)  )
        bxmin=Segment( Point(xmin,-1),Point(xmin,1) )
        bxmax=Segment( Point(xmax,-1),Point(xmax,1) )
        bymin=Segment( Point(-1,ymin),Point(1,ymin) )
        bymax=Segment( Point(-1,ymax),Point(1,ymax) )
        # We compute the intersections of self with the four lines describing the window.
        # Two of them will be the initial and final point of the searched segment.
        Ixmin=Intersection(self,bxmin)[0]
        Ixmax=Intersection(self,bxmax)[0]
        Iymin=Intersection(self,bymin)[0]
        Iymax=Intersection(self,bymax)[0]
        l=[]
        if Ixmin.y>= ymin and Ixmin.y <= ymax :
            l.append(Ixmin)
        if Ixmax.y>= ymin and Ixmax.y <= ymax :
            l.append(Ixmax)
        if Iymin.x>= xmin and Iymin.x <= xmax :
            l.append(Iymin)
        if Iymax.x >= xmin and Iymax.x <= xmax :
            l.append(Iymax)
        if len(l) == 0:     # this is the case in which the line does not cross the window.
            return None
        if len(l) != 2:
            if Ixmin==Iymax and Ixmin in l:
                l.remove(Ixmin)
            if Ixmax==Iymax and Ixmax in l:
                l.remove(Ixmax)
            if Ixmax==Iymin and Ixmax in l:
                l.remove(Ixmax)
            if Ixmin==Iymin and Ixmin in l:
                l.remove(Ixmin)
        if len(l) != 2:
            print("We found {} points".format(len(l)))
            for p in l :
                print(p)
            print("The segment is {}, with equation {} ".format(self,self.equation))
            print("and the intersection points are :")
            for P in [Ixmin,Ixmax,Iymin,Iymax]:
                print(   "({},{})".format(P.x,P.y)  )
            raise ValueError
        return Segment(  l[0],l[1]  )
    def segment(self,projection=False):
        """
        serves to transform a vector into a segment
        """
        return Segment(self.I,self.F)
    def fit_inside(self,xmin,xmax,ymin,ymax):
        """
        return the largest segment that fits into the given bounds
        """
        if self.horizontal:
            k=self.I.y
            return Segment(  Point(xmin,k),Point(xmax,k)  )
        if self.vertical:
            k=self.I.x
            return Segment(  Point(x,ymin),Point(x,ymax)  )

        x=var("x")
        f=self.phyFunction()
        x1=solve( [ f(x)==ymax ],x )[0].rhs()
        x2=solve( [ f(x)==ymin ],x )[0].rhs()
        x1=QQ(x1)
        x2=QQ(x2)
        X=[xmin,x1,x2,xmax]
        X.sort()
        A=Point(  X[1],f(X[1]) ) 
        B=Point(X[2],f(X[2]))
        return Segment(   Point(  X[1],f(X[1]) )  ,Point(X[2],f(X[2]))  )
    def parametric_curve(self):
        """
        Return the parametric curve corresponding to `self`.

        The starting point is `self.I` and the parameters is the arc length.
        The parameter is positive on the side of `self.B` and negative on the
        opposite side.

        EXAMPLES::

            sage: from phystricks import *
            sage: segment=Segment(Point(0,0),Point(1,1))
            sage: curve=segment.parametric_curve()
            sage: print curve(0)
            <Point(0,0)>
            sage: print curve(1)
            <Point(1/2*sqrt(2),1/2*sqrt(2))>
            sage: print curve(segment.length())
            <Point(1,1)>
        """
        x=var('x')
        l=self.length()
        f1=phyFunction(self.I.x+x*(self.F.x-self.I.x)/l)
        f2=phyFunction(self.I.y+x*(self.F.y-self.I.y)/l)
        return ParametricCurve(f1,f2,(0,l))
    def copy(self):
        v=Segment(self.I,self.F)
        v.arrow_type=self.arrow_type
        return v
    def get_regular_points(self,dx):
        """
        Notice that it does not return the last point of the segment, unless the length is a multiple of dx.
           this is why we add by hand the last point in GetWavyPoint
        """
        n = floor(self.length/dx)
        return [self.get_point_proportion(float(i)/n) for i in range(0,n)]
    def get_wavy_points(self,dx,dy):
        """
        Return a list of points that make a wave around the segment.
        The wavelength is dx and the amplitude is dy.
        The first and the last points are self.I and self.F and are then *on* the segment. Thus the wave begins and ends on the segment.
        """
        normal = self.get_normal_vector().fix_size(dy)
        PI = self.get_regular_points(dx)
        PIs = [self.I]
        PIs.extend( [  PI[i]+normal*(-1)**i for i in range(1,len(PI))  ] )
        PIs.append(self.F)
        return PIs
    def proportion(self,p,advised=True):
        print("You should use 'get_point_proportion' instead")
        raise DeprecationWarning
        return self.get_point_proportion(p,advised)
    def get_point_proportion(self,p,advised=True):
        """
        Return a point on the segment which is at the position
        (p-1)*I+p*F
        if I and F denote the initial and final point of the segment.
        """
        P = self.I*(1-p) + self.F*p
        if advised:
            P._advised_mark_angle=self.angle().degree+90
        return P
    def put_arrow(self,position=0.5,size=0.01):
        """
        Add a small arrow at the given position. `position` is a number between 0 and 1.

        The arrow is pointed from self.I to self.F and is by default put at the middle of the
        segment.

        The arrow is a vector of size (by default) 0.01. 
        """
        P=self.get_point_proportion(position,advised=False)
        v=AffineVector(P,self.F).fix_size(size)
        self.added_objects.append(v)
        #self.arrow_list.append(v)
    def put_measure(self,measure_distance,mark_distance,mark_angle,name,automatic_place):
        measure=self.get_measure(measure_distance,mark_distance,mark_angle,name,automatic_place)
        self.added_objects.append(measure)
    def get_measure(self,measure_distance,mark_distance,mark_angle,name,automatic_place):
        """
        The difference between 'put_measure' and 'get_measure' is that 'get_measure' return the measure graph while 'put_measure' add the measure graph to the segment.

        This allows constructions like
        mesL=Segment(F,D).get_measure(-0.2,0.1,90,"\( 10\)",automatic_place=(pspict,"S"))
        and then draw mesL. The Segment(F,D) object is not drawn.

        If 'mark_angle' is 'None', then the angle will be perpendicular to 'self'
        """
        if mark_angle==None:
            mark_angle=self.angle()+90*degree
        measure=MeasureLength(self,measure_distance)
        measure.put_mark(mark_distance,mark_angle,name,automatic_place=automatic_place)
        return measure
    def put_code(self,n=1,d=0.1,l=0.1,angle=45,pspict=None):
        """
        add small line at the center of the segment.

        'n' add 'n' small lines. Default is 1
        'd' is the distance between two of them
        'l' is the (visual) length of the segment
        'angle' is the angle with 'self'.
        """
        ao=self.get_code(n=n,d=d,l=l,angle=angle,pspict=pspict)
        self.added_objects.extend(ao)
    def get_code(self,n=1,d=0.1,l=0.1,angle=45,pspict=None):
        #TODO : the angle given here should be visual
        ao=[]
        vect=AffineVector(self.I,self.F).fix_visual_size(d,pspict)
        center=self.midpoint(advised=False)
        positions=[]
        if n%2==1:
            for k in range( int(-(n-1)/2),int((n-1)/2)+1 ):
                positions.append(center+k*vect)
        if n%2==0:
            import numpy
            for k in numpy.linspace(-n/2+0.5,n/2-0.5,n):
                positions.append(center+k*vect)
        mini1=self.rotation(angle).fix_visual_size(l)
        for P in positions:
            mini=mini1+AffineVector(mini1.midpoint(),P)
            ao.append(mini)
        return ao
    def get_divide_in_two(self,n=1,d=0.1,l=0.1,angle=45,pspict=None):
        M=self.midpoint()
        s1=Segment(self.I,M)
        s2=Segment(M,self.F)
        s1.put_code(n=n,d=d,l=l,pspict=pspict)
        s2.put_code(n=n,d=d,l=l,pspict=pspict)
        a=s1.added_objects
        a.extend(s2.added_objects)
        return a
    def divide_in_two(self,n=1,d=0.1,l=0.1,angle=45,pspict=None):
        a=self.get_divide_in_two(n=n,d=d,l=l,angle=angle,pspict=pspict)
        self.added_objects.extend( a )
    def Point(self):
        """
        Return the point X such that as free vector, 0->X == self

        More precisely, if self is the segment A->B, return the point B-A
        """
        return self.F-self.I
    def center(self,advised=True):
        return self.midpoint(advised=advised)
    def midpoint(self,advised=True):
        P = self.get_point_proportion(0.5,advised)
        return P
    def AffineVector(self):
        return AffineVector(self.I,self.F)
    def get_normal_vector(self):
        """
        returns a normalized normal vector at the center of the segment

        OUTPUT:
        A vector

        EXAMPLES::

            sage: from phystricks import *
            sage: v= Segment(Point(0,0),Point(2,0)).get_normal_vector()
            sage: print v
            <vector I=<Point(1.0,0)> F=<Point(1.0,-1)>>
            sage: v.length()
            1
        """
        if self.vertical :
            return Point(-1,0).Vector().origin(self.center())
        else :
            P = Point(self.slope,-1)
            return P.Vector().normalize().origin(self.center())
    def get_tangent_vector(self):
        """
        return a tangent vector at center of the segment
        """
        C=self.center()
        v=self.AffineVector()
        return v.origin(self.center()).fix_size(1)
    def polaires(self):
        return PointToPolaire(self.Point())
    def angle(self):
        """
        return the angle of the segment.

        This is the angle between the segment and the horizontal axe. 
        The returned angle is positive.

        EXAMPLES::

            sage: from phystricks import *
            sage: S=Segment(Point(1,1),Point(2,2))
            sage: type(S.angle())
            <class 'phystricks.SmallComputations.AngleMeasure'>
            sage: S.angle().degree
            45
            sage: S.angle().radian
            1/4*pi

            sage: S=Segment(Point(1,1),Point(2,0))
            sage: S.angle().degree
            315

            sage: v=AffineVector(Point(2,3),Point(2-4/sqrt(3),-1))
            sage: v.angle().radian.simplify_trig()
            4/3*pi
        """
        return self.polaires().measure.positive()
    def origin(self,P):
        """
        return a vector (in affine space) whose origin is P.
        """
        return AffineVector(P,Point(P.x+self.Dx,P.y+self.Dy))
    def direction(self):
        return self.F-self.I
    def return_deformations(self,segment):
        segment.arrow_type=self.arrow_type
        return segment
    def projection(self,segment,advised=False):
        """
        Return the projection of self on the given segment

        It also works with vectors

        INPUT:
        - ``segment`` - the line on which we want to project

        EXAMPLES::

            sage: from phystricks import *
            sage: l = Segment(Point(0,0),Point(0,1))
            sage: v = AffineVector(Point(-1,1),Point(-2,3))
            sage: print v.equation
            x + 1/2*y + 1/2 == 0
            sage: print v.projection(l)
            <vector I=<Point(0,1)> F=<Point(0,3)>>
            sage: print l.projection(v)
            <segment I=<Point(-2/5,-1/5)> F=<Point(-4/5,3/5)>>

        
            sage: l = Segment(Point(0,0),Point(1,2))
            sage: s = Segment(Point(-2,1),Point(-3,4))
            sage: print s.projection(l)
            <segment I=<Point(0,0)> F=<Point(1,2)>>
        """
        v = Segment(self.I.projection(segment),self.F.projection(segment))
        if advised:
            v._advised_mark_angle=self.angle().degree+90
        return self.return_deformations(v)
    def bisector(self,code=None):
        """
        return the segment which is orthogonal to the center of 'self'.
        """
        normal=self.get_normal_vector()
        M=self.center()
        P1=M+normal
        P2=M-normal
        seg=Segment(P1,P2)
        if code:
            s1=Segment(self.I,M)
            s2=Segment(M,self.F)
            s1.put_code(n=code[0],d=code[1],l=code[2],angle=code[3],pspict=code[4])
            s2.put_code(n=code[0],d=code[1],l=code[2],angle=code[3],pspict=code[4])
            seg.added_objects.append(s1)
            seg.added_objects.append(s2)
        return seg
    def orthogonal(self,point=None):
        """
        return the segment with a rotation of 90 degree. The new segment is, by default, still attached to the same point.

        If 'point' is given, the segment will be attached to that point

        Not to be confused with self.get_normal_vector
        """
        new_Dx=-self.Dy
        new_Dy=self.Dx
        v=Segment(self.I,Point(self.I.x+new_Dx,self.I.y+new_Dy))
        defo=self.return_deformations(v)
        if not point:
            return defo
        defo=defo.fix_origin(point)
    def orthogonal_trough(self,P):
        """
        return a segment orthogonal to self passing trough P.

        The starting point is 'P' and the final point is the intersection with 'self'

        If these two points are the same --when d^2(P,Q)<0.001 (happens when 'P' belongs to 'self'), the end point is not guaranteed.

        By the way, when you want
        Segment(A,B).orthogonal_trough(B)
        you can use
        seg=Segment(B,A).orthogonal()
        instead.
        """
        s=self.orthogonal().fix_origin(P)
        Q=Intersection(s,self)[0]
        if (P.x-Q.x)**2+(P.y-Q.y)**2 <0.001 :
            return s
        else :
            return Segment(P,Q)
    def parallel_trough(self,P):
        """ 
        return a segment parallel to self passing trough P
        """
        v=self.F-self.I
        Q=P+v
        return Segment(P,Q)
    def decomposition(self,v):
        """
        return the decomposition of `self` into a `v`-component and a normal component.

        INPUT:

        - ``v`` - a segment or a vector

        OUTPUT:

        a tuple of vectors that are the decomposition of `self` into `v` and `v-perp` directions

        NOTE:

        The result does not depend on `v`, but only on the *direction* of `v`.

        EXAMPLES::

            sage: from phystricks import *
            sage: v=Vector(2,3)
            sage: vx,vy = v.decomposition(Segment(Point(0,0),Point(0,1)))
            sage: print vx
            <vector I=<Point(0,0)> F=<Point(0,3)>>
            sage: print vy
            <vector I=<Point(0,0)> F=<Point(2,0)>>

        .. literalinclude:: phystricksExDecomposition.py
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition0PICTExDecompositionpspict0-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition1PICTExDecompositionpspict1-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition2PICTExDecompositionpspict2-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition3PICTExDecompositionpspict3-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition4PICTExDecompositionpspict4-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition5PICTExDecompositionpspict5-for_eps.png
        """
        v1=self.projection(v)
        v2=self-v1
        return v1,v2
    def translate(self,vecteur):
        v = Segment(self.I.translate(vecteur),self.F.translate(vecteur))
        return self.return_deformations(v)
    def fix_origin(self,a,b=None):
        """
        Return the segment fixed at `P`. This is the translation of `self`  by `P-self`.

        In other words, it returns the segment which is parallel to self trough the given point.

        Typically it is used in the framework of affine vector..

        INPUT:

        - ``P`` - The point on which we want to "attach" the new segment.

        OUTPUT:

        A new segment (or vector) with initial point at `P`

        EXAMPLES:
    
        We can fix the orignin by giving the coordinates of the new origin::

            sage: from phystricks import *
            sage: v=AffineVector( Point(1,1),Point(2,2) )
            sage: w=v.fix_origin(3,5)
            sage: w.I.coordinates(),w.F.coordinates()
            ('(3,5)', '(4,6)')
        
        We can also give a point::    

            sage: P=Point(-1,-pi)
            sage: u=w.fix_origin(P)
            sage: u.I.coordinates(),u.F.coordinates()
            ('(-1,-pi)', '(0,-pi + 1)')
        """
        if b:
            P=Point(a,b)
        else:
            P=a
        v=self.translate(P-self.I)
        return self.return_deformations(v)
    def inverse(self):
        """
        Return the segment BA instead of AB.

        Not to be confused with (-self). The latter is a rotation of 180 degree of self.
        """
        v = Segment(self.F,self.I)
        return self.return_deformations(v)
    def rotation(self,angle):
        """
        Return the segment attached to the same point but with a rotation of angle.

        INPUT:

        - ``angle`` - the value of the rotation angle (in radian).

        """
        a=angle
        if isinstance(angle,AngleMeasure):
            a=angle.degree
        v = PolarSegment(self.I,self.polaires().r,self.polaires().degree+a)
        return self.return_deformations(v)
    def get_visual_length(self,xunit=None,yunit=None,pspict=None):
        """
        Return the visual length of self. That is the length taking xunit and  yunit into account
        """
        if pspict:
            xunit=pspict.xunit
            yunit=pspict.yunit
        Dx=(self.F.x-self.I.x)*xunit
        Dy=(self.F.y-self.I.y)*yunit
        if self.vertical:
            return Dy
        else: 
            return sqrt(Dx**2+Dy**2)
    def fix_visual_size(self,l,xunit=None,yunit=None,pspict=None):
        """
        return a segment with the same initial point, but with visual length  `l`
        """
        if pspict:
            xunit=pspict.xunit
            yunit=pspict.yunit
        if xunit==None or yunit==None:
            return self.fix_size(l)
        return visual_length(self,l,xunit,yunit,pspict)
    def visual_length(self,l,xunit=None,yunit=None,pspict=None):
        raise DeprecationWarning,"Use 'fix_visual_size' instead" #2014
    def add_size_extremity(self,l):
        """
        Add a length <l> at the extremity of the segment. Return a new object.
        """
        L=self.length()
        coef=(l+L)/L
        v = coef*self
        return self.return_deformations(v)
    def fix_size(self,l):
        """
        return a new vector or segment with size l.

        This function has not to be used by the end user. Use self.normalize() instead.
        """
        L=self.length()
        if L == 0:
            print "fix_size problem: this vector has a norm equal to zero"
            return self.copy()
        if self.arrow_type=="segment":
            v = self.dilatation(l/self.length())
        if self.arrow_type=="vector":
            return self.normalize(l)
        return self.return_deformations(v)
    def add_size(self,lI=0,lF=0):
        """
        Return a new Segment with extra length lI at the initial side and lF at the final side. 
        """
        F=self.add_size_extremity(lF).F
        I=self.inverse().add_size_extremity(lI).F
        v = Segment(I,F)
        return self.return_deformations(v)
    def dilatation(self,coef):
        """
        Return a Segment which is dilated by the coefficient coef 

        If self is a segment:
            This adds the same length at both extremities.
            The segment A --> B dilated by 0.5 returns
            a segment C --> D where [CD] is the _central_ half of [AB].
            If you want to add some length to one
            of the extremities, use
            self.add_size
            or
            l*self
            with a scalar l.

        If self is a vector:
            This adds the length only at the end.
            The affine vector A --> B dilated by 0.5 returns
            an affine vector A --> D where D is the _central_ point of [AB].

        INPUT:
        - ``coef`` - a number. This is the dilatation coefficient

        OUTPUT:
        a new vector or segment

        EXAMPLES::

            sage: from phystricks import *
            sage: S=Segment(Point(-2,-2),Point(2,2))
            sage: print S.dilatation(0.5)           
            <segment I=<Point(-1.00000000000000,-1.00000000000000)> F=<Point(1.00000000000000,1.00000000000000)>>

        But ::

            sage: v=AffineVector(Point(-2,-2),Point(2,2))
            sage: print v.dilatation(0.5)                
            <vector I=<Point(-2,-2)> F=<Point(0.000000000000000,0.000000000000000)>>
        """
        if self.arrow_type=="segment":
            d=0.5*self.length()*(coef-1)
            return self.add_size(d,d)
        if self.arrow_type=="vector":
            l=self.length*coef
            return self.normalize(l)
    def dilatationI(self,coef):
        """
        return a dilated segment, but only enlarges at the initial extremity.
        """
        v=AffineVector(self)
        w=-v
        wp=w.dilatation(coef)
        return Segment(wp.F,v.F)
    def dilatationF(self,coef):
        """
        return a dilated segment, but only enlarges at the final extremity.
        """
        v=self.AffineVector()
        v=v.dilatation(coef)
        return Segment(v.I,v.F)
    def normalize(self,l=1):
        """
        If self.arrow_type is "segment", it normalize the segment to <l> by dilating in both extremities

        If self.arrow_type is "vector", it normalize the vector to <l> but keeps the origin.

        NOTES:
        * If self is of length zero, return a copy of self.
        * If not length is given, normalize to 1.
        * If the given new length is negative, 
            if self is a vector, change the sense
            if self is a segment, consider the absolute value

        INPUT:
        - ``l`` - (default=1) a number, the new length

        OUTPUT:
        A segment or a vector

        EXAMPLES::

            sage: from phystricks import *
            sage: s=Segment(Point(0,0),Point(1,0))
            sage: print s.normalize(2)
            <segment I=<Point(-0.5,0)> F=<Point(1.5,0)>>
            sage: print s.normalize(-1)
            <segment I=<Point(0,0)> F=<Point(1,0)>>

            sage: v=AffineVector(Point(1,1),Point(3,1))
            sage: print v.normalize(2)
            <vector I=<Point(1,1)> F=<Point(3,1)>>
            sage: print v.normalize(-1)
            <vector I=<Point(1,1)> F=<Point(0,1)>>
        """
        if self.arrow_type=="segment":
            if l<0 : 
                l=-l
            v = self.fix_size(l)
        if self.arrow_type=="vector":
            L=self.length()
            if L==0:
                return self.copy()
            v = (l*self).__div__(L)     
            v.arrow_type="vector"
        return self.return_deformations(v)
    def graph(self,mx=None,Mx=None):
        if not mx:
            C = GraphOfASegment(self.I,self.F)
        else :
            C = GraphOfASegment(self.get_point(mx),self.get_point(Mx))
        C.parameters=self.parameters.copy()
        return C
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return GraphOfASegment
    def __mul__(self,coef):
        """
        multiply the segment by a coefficient.

        INPUT:
        - ``coef`` - the multiplying coefficient

        OUTPUT:
        A new segment or vector.

        EXAMPLES::

            sage: from phystricks import *
            sage: v=Vector(1,1)
            sage: print 2*v
            <vector I=<Point(0,0)> F=<Point(2,2)>>
            sage: print -2*v
            <vector I=<Point(0,0)> F=<Point(-2,-2)>>

            sage: s=Segment(Point(1,1),Point(2,2))
            sage: print 3*s
            <segment I=<Point(1,1)> F=<Point(4,4)>>

        The initial point stays the same (this is not the same behaviour as in self.normalize !)
        If the coefficient is negative :
            if self is a vector : change the sense of the vector
            if self is a segment : don't care about the sign of coeff
        """
        if self.arrow_type=="segment":
            if coef<=0:
                coef=-coef
        v = Segment(self.I,Point(self.I.x+self.Dx*coef,self.I.y+self.Dy*coef))
        return self.return_deformations(v)
    def __add__(self,other):
        """
        In the case of addition of two segments with same origin, return a segment
        representing the vector sum.

        If the two segments have not the same origin, the `other` one is first translated.

        If the other is a vector, return the translated segment

        INPUT:
        - ``other`` - an other segment

        OUTPUT:
        A new vector or segment that has the same origin as `self`.

        EXAMPLES::

            sage: from phystricks import *
            sage: a=Vector(1,1)
            sage: b=Vector(2,3)
            sage: print a+b
            <vector I=<Point(0,0)> F=<Point(3,4)>>

            sage: a=Segment(Point(1,1),Point(3,4))
            sage: b=AffineVector(Point(1,1),Point(-1,3))
            sage: print a+b
            <segment I=<Point(1,1)> F=<Point(1,6)>>
        """
        if isinstance(other,GraphOfASegment):
            if self.arrow_type=="segment" and other.arrow_type=="vector":
                return Segment(   self.I+other,self.F+other  )
            if self.I != other.I:
                other=other.fix_origin(self.I)
            v=Vector(self.F.x-self.I.x+other.F.x-other.I.x, self.F.y-self.I.y+other.F.y-other.I.y,)
            return self.return_deformations(v.origin(self.I))
        elif isinstance(other,tuple):
            return self.return_deformations(  Segment(self.I+other,self.F+other)  )
        else:
            raise TypeError,"I do not know how to sum %s with %s"%(self,other)
    def __sub__(self,other):
        return self+(-other)
    def __rmul__(self,coef):
        return self*coef
    def __neg__(self):
        if self.arrow_type=="segment":
            return Segment(self.F,self.I)
        return self*(-1)
    def __div__(self,coef):
        return self * (1/coef)
    def __div__(self,coef):
        return self * (1/coef)
    def __str__(self):
        if self.arrow_type=="segment":
            return "<segment I=%s F=%s>"%(str(self.I),str(self.F))
        if self.arrow_type=="vector":
            return "<vector I=%s F=%s>"%(str(self.I),str(self.F))
    def mark_point(self,pspict=None):
        """
        return the point on which a mark has to be placed if we use the method put_mark.

        If we have a segment, the mark is at center while if it is a vector the mark
        has to be placed on the extremity.

        EXAMPLES::

            sage: from phystricks import *
            sage: v=Vector(1,1)
            sage: v.mark_point().coordinates()
            '(1,1)'
            sage: v.advised_mark_angle.radian
            3/4*pi

            sage: S=Segment(Point(1,2),Point(3,5))
            sage: S.mark_point().coordinates()
            '(2.0,3.5)'
            sage: S.advised_mark_angle.radian
            1/2*pi + arctan(3/2)
        """
        if self.arrow_type == "vector" :
            return self.F.copy()
        else :
            return self.center().copy()
    def bounding_box(self,pspict):
        if self.in_bounding_box:
            return BoundingBox(self.I,self.F)       # If you change this, maybe you have to adapt math_bounding_box
        else :
            return BoundingBox()
    def math_bounding_box(self,pspict=None):
        if self.in_math_bounding_box:
            return self.bounding_box(pspict)
        else :
            return BoundingBox()
    def latex_code(self,language=None,pspict=None):
        """
        Return the LaTeX's code (pstricks or tikz) of a Segment when is is seen as a segment
        """
        if self.parameters.style=="none":
            return ""
        if self.arrow_type=="vector":
                return _vector_latex_code(self,language=language,pspict=pspict)
        if self.arrow_type=="segment":
            if self.wavy:
                waviness = self.waviness
                curve=InterpolationCurve(self.get_wavy_points(waviness.dx,waviness.dy),context_object=self)
                curve.parameters=self.parameters.copy()
                return curve.latex_code(language=language,pspict=pspict)
            else:
                if language=="pstricks":
                    a =[self.I.create_PSpoint() + self.F.create_PSpoint()]
                    a.append("\pstLineAB[%s]{%s}{%s}"%(self.params(language="pstricks"),self.I.psName,self.F.psName))
                if language=="tikz":
                    a=[]
                    c1=self.I.coordinates(numerical=True,pspict=pspict)
                    c2=self.F.coordinates(numerical=True,pspict=pspict)
                    if 'I' in c1 or "I" in c2 :
                        print(self.I,self.F)
                        raise
                    a.append("\draw [{2}] {0} -- {1};".format(c1,c2,self.params(language="tikz")))
        #for v in self.arrow_list:
        #    a.append(v.latex_code(pspict=pspict,language=language))
        return "\n".join(a)
    def pstricks_code(self,pspict=None):
        return self.latex_code(language="pstricks",pspict=pspict)
    def tikz_code(self,pspict=None):
        return self.latex_code(language="tikz",pspict=pspict)

class GraphOfAMeasureLength(GraphOfASegment):
    def __init__(self,seg,dist=0.1):
        try :
            self.segment=seg.segment
        except AttributeError :
            self.segment=seg
        self.dist=dist
        self.delta=seg.rotation(-90).fix_size(self.dist)
        self.mseg=seg.translate(self.delta)
        GraphOfASegment.__init__(self,self.mseg.I,self.mseg.F)
        self.mI=self.mseg.I
        self.mF=self.mseg.F
    def advised_mark_angle(self,pspict=None):
        return self.delta.angle()
    def math_bounding_box(self,pspict=None):
        return BoundingBox()
        # I return a "empty" bounding box because I don't want to
        # take the measures in consideration when creating the axes.
        #return self.mseg.math_bounding_box(pspict)
        #return BoundingBox()
    def bounding_box(self,pspict=None):
        bb=self.mseg.bounding_box(pspict)
        if self.marque:
            C=self.mseg.center()
            C.marque=self.marque
            C.mark=self.mark
            C.mark.graph=C
            bb.AddBB(C.bounding_box(pspict))
        return bb
    def mark_point(self,pspict=None):
        return self.mseg.center()
    def latex_code(self,language=None,pspict=None):
        a=[]
        C=self.mseg.center()
        vI=AffineVector(C,self.mI)
        vF=AffineVector(C,self.mF)
        vI.parameters=self.parameters.copy()
        vF.parameters=self.parameters.copy()
        a.append(vI.latex_code(language=language,pspict=pspict))
        a.append(vF.latex_code(language=language,pspict=pspict))
        #if self.marque :
        #    a.append(self.mark.pstricks_code(pspict))
        return "\n".join(a)

class GraphOfAText(GraphOfAnObject):
    """
    You can customize the background via the object `self.rectangle`
    """
    def __init__(self,P,text,hide=True):
        GraphOfAnObject.__init__(self,self)
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
        return self.mark.math_bounding_box(pspict)
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
            (x, y) |--> 0

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

        object GraphOfAVectorField.
        
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
            pos_y=linspace(my,My,ny)
            for xx in pos_x:
                for yy in pos_y:
                    draw_points.append(Point(xx,yy))
        return GraphOfAVectorField(self,draw_points=draw_points)
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

class GraphOfAVectorField(GraphOfAnObject,GeometricVectorField):
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
        GraphOfAnObject.__init__(self,F)
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

class GraphOfAnAngle(GraphOfAnObject):
    """
    self.mark_angle is the angle at which self.mark_point will be placed. By default it is at the middle. 
        If you want to change it, use
        self.set_mark_angle(x).
        It will set both the mark_angle and the advised_mark_angle to to x in the same time.

        We have to make a choice between the two angles that can be deduced from 3 points. Here the choice is
        the angle from the first given point to the second one.

        EXAMPLES ::

            sage: from phystricks import *
            sage: R=2
            sage: theta=-10     # Notice the negative number
            sage: sigma=60
            sage: O=Point(0,0)
            sage: C=Circle(O,R)
    
            sage: P=C.get_point(theta)
            sage: Q=C.get_point(sigma)
            sage: angle=Angle(P,O,Q)
            sage: numerical_approx(angle.advised_mark_angle)
            25.0000000000000
    """
    def __init__(self,A,O,B,r=None):
        self.A=A
        self.O=O
        self.B=B
        if r==None:
            #r=0.2*Segment(A,O).length()
            r=0.5           # change of the default since we are now giving a 'visual' length (February 8, 2015)
        self.r=r
        self.angleA=AffineVector(O,A).angle()
        self.angleB=AffineVector(O,B).angle()

        # I think that one dos not have to check and fix what angle is first here
        # because the angles are re-computed in self.circle.

        self.angleI=self.angleA
        self.angleF=self.angleB

        GraphOfAnObject.__init__(self,self)
        #self.mark_angle=self.media
        self._mark_angle=None
    def visual_angleIF(self,pspict):
        aI1=visual_polar_coordinates(Point( cos(self.angleI.radian),sin(self.angleI.radian) ),pspict).measure
        aF1=visual_polar_coordinates(Point( cos(self.angleF.radian),sin(self.angleF.radian) ),pspict).measure

        a=numerical_approx(aI1.degree)
        b=numerical_approx(aF1.degree)
        if a > b:
            a=a-360
            aI2=AngleMeasure(value_degree=a)
        else :
            aI2=aI1
        aF2=aF1
        return aI2,aF2
    def circle(self,visual=False,pspict=None):
        visualI,visualF=self.visual_angleIF(pspict)
        return Circle(self.O,self.r,visual=visual,pspict=pspict).graph(visualI,visualF)
    def measure(self):
        return AngleMeasure(value_degree=self.angleF.degree-self.angleI.degree)
    def graph(self):
        return GraphOfAnAngle(self)
    def set_mark_angle(self,theta):
        """
        theta is degree or AngleMeasure
        """
        self._mark_angle=AngleMeasure(value_degree=theta)
        #self._advised_mark_angle=degree(theta,number=True,converting=False)
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        C= self.circle(visual=True,pspict=pspict)
        bb=C.bounding_box(pspict)
        return self.circle(visual=True,pspict=pspict).bounding_box(pspict)
    def advised_mark_angle(self,pspict):
        if self._mark_angle:
            return self._mark_angle
        visualI,visualF=self.visual_angleIF(pspict=pspict)
        return (visualI.degree+visualF.degree)/2
    def mark_point(self,pspict=None):
        ama=self.advised_mark_angle(pspict)
        return self.circle(visual=True,pspict=pspict).get_point(ama)
    def latex_code(self,language=None,pspict=None):
        circle=self.circle(visual=True,pspict=pspict)
        circle.parameters=self.parameters.copy()
        return circle.latex_code(language=language,pspict=pspict)

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

class NonAnalyticParametricCurve(GraphOfAnObject):
    def __init__(self,f1,f2,mx,Mx):
        GraphOfAnObject.__init__(self,self)
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

class NonAnalyticFunction(GraphOfAnObject):
    """
    Represent a function for which one has no analytic form.

    As long as one can evaluate it at points, one can draw an interpolation curve.
    """
    def __init__(self,fun,mx=None,Mx=None):
        GraphOfAnObject.__init__(self,fun)
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

class GraphOfAphyFunction(GraphOfAnObject):
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
        GraphOfAnObject.__init__(self,fun)
        self.sage=fun
        x,y=var('x,y')
        self.sage=fun
        try :
            self.sageFast = self.sage._fast_float_(x)
        except (NotImplementedError,TypeError,ValueError,AttributeError) : 
            # Happens when the derivative of the function is not implemented in Sage
            # Also happens when there is a free variable,
            # as an example
            # F=GraphOfAVectorField(x,y)
            # Also when something non analytic is given like a distribution.
            self.sageFast = self.sage
        self.string = repr(self.sage)
        self.fx = self.string.replace("x |--> ","")
        self.pstricks = SubstitutionMathPsTricks(self.fx)
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
        self.added_plotpoints=[]
        self.pieces=[]      
        self.parameters.color = "blue"              # Modification with respect to the attribute in GraphOfAnObject
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
            except AttributeError :     # Happens when self is a phyFunction instead of GraphOfAphyFunction
                return self
        if n==1:
            if self._derivative == None :
                self._derivative = phyFunction(self.sage.derivative(x))
            return self._derivative
        else:
            return self.derivative(n-1).derivative()
    def get_point(self,x,advised=True):        
        return general_funtion_get_point(self,x,advised)
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
            sage: print [P.coordinates() for P in f.get_regular_points(-2,2,sqrt(2))]
            ['(0.704344645322537*sqrt(2) - 2,0.704344645322537*sqrt(2) - 1)', '(1.40868929064507*sqrt(2) - 2,1.40868929064507*sqrt(2) - 1)', '(2.11303393596761*sqrt(2) - 2,2.11303393596761*sqrt(2) - 1)', '(2.81737858129015*sqrt(2) - 2,2.81737858129015*sqrt(2) - 1)']

        Even if it is not clear from these expressions, these are almost the points (-1,0),(0,1), and (1,2).

        """

        # Use self.parametric_curve instead of that stuff since June 25, 2014
        #x=var('x')
        #f1 = phyFunction(x)
        #try :
        #    f2 = self.f     # Here, self can be of type «GraphOfAphyFunction»
        #except AttributeError :
        #    f2 = self
        #curve = ParametricCurve(f1,f2)
        

        curve = self.parametric_curve()
        return curve.get_regular_points(mx,Mx,dx)
    def get_wavy_points(self,mx,Mx,dx,dy):
        print("SKBooMaOvCE")
        curve=self.parametric_curve()
        return curve.get_wavy_points(mx,Mx,dx,dy)

        # No more in use since June 25, 2014
        #PIs = self.get_regular_points(mx,Mx,dx)
        #Ps = [self.get_point(mx)]
        #for i in range(0,len(PIs)) :
        #    Ps.append( self.get_normal_point(PIs[i].x, ((-1)**i)*dy ) )
        #Ps.append(self.get_point(Mx))   
        #return Ps

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
            sage: f.get_minmax_data(-3,pi)
            {'xmin': -3.0, 'ymin': -3.0, 'ymax': 3.1419999999999999, 'xmax': 3.1419999999999999}


        In the case of the sine function, the min and max are almost -1 and 1::

            sage: from phystricks import *
            sage: f=phyFunction(sin(x))
            sage: f.get_minmax_data(0,2*pi)
            {'xmin': 0.0, 'ymin': -1.0, 'ymax': 1.0, 'xmax': 6.2830000000000004}

        NOTE:

        This function is victim of the `Trac 10246 <http://trac.sagemath.org/sage_trac/ticket/10246>` The try/except
        block is a workaround.

        """
        minmax={}
        minmax['xmin']=mx
        minmax['xmax']=Mx
        ymin=1000
        ymax=-1000
        for x in self.plotpoints_list():
            valid=True
            try :
                y=self(x)
            except ZeroDivisionError :
                valid=False
            if y.is_infinity():
                valid=False
            if valid :
                ymax=max(ymax,y)
                ymin=min(ymin,y)
        minmax['ymax']=ymax
        minmax['ymin']=ymin
        return minmax

        # This is no more based on the Sage's MinMax function of a plot.
        #try :
        #    return MyMinMax(plot(self.sage,(mx,Mx)).get_minmax_data())
        #except ValueError :
        #    try:
        #        if self.sage==x:
        #            return MyMinMax(plot(x,mx,Mx).get_minmax_data())
        #    except NameError:
        #        if repr(self.sage)=="x |--> x":
        #            x=var('x')
        #            return MyMinMax(plot(x,mx,Mx).get_minmax_data())
        #else :
        #    raise ValueError,"This is a strange case. Maybe related to ticket 10246"
    def xmax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmax']
    def xmin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmin']
    def ymax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymax']
    def ymin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymin']
    def graph(self,mx,Mx):
        gr = GraphOfAphyFunction(self.sage,mx,Mx)
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
        an instance of GraphOfAphyFunction that inherits from here.
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
        self.added_plotpoints.append(x)
    def plotpoints_list(self,plotpoints=None):
        import numpy
        if not plotpoints:
            plotpoints=self.parameters.plotpoints
        X=list(numpy.linspace(self.mx,self.Mx,plotpoints))
        X.extend(self.added_plotpoints)
        X.sort()
        return X
    def cut_y(self,ymin,ymax,plotpoints=None):
        """
        Will not draw the function bellow 'ymin' and over 'ymax'. Will neither join the pieces.

        This is useful when drawing functions like 1/x.

        It is wise to use a value of plotpoints that is not a multiple of the difference Mx-mx. The default behaviour is most of time like that.

        If an other cut_y is already imposed, the most restrictive is used.
        """
        if self.do_cut_y:
            self.pieces=[]
            ymin=max(ymin,self.cut_ymin)
            ymax=min(ymax,self.cut_ymax)
        if not plotpoints:
            plotpoints=2.347*self.parameters.plotpoints
        self.do_cut_y=True
        self.cut_ymin=ymin
        self.cut_ymax=ymax
        X=self.plotpoints_list(plotpoints=plotpoints)
        s=SmallComputations.split_list(X,self.sage,self.cut_ymin,self.cut_ymax)
        for k in s:
            mx=k[0]
            Mx=k[1]
            f=self.graph(mx,Mx)
            self.pieces.append(f)
    # I use the generic function 'params' from GraphOfAnObject, June 27, 2014
    #def params(self,language=None):
    #    self.conclude_params()
    #    self.add_option("plotpoints=%s"%str(self.parameters.plotpoints))
    #    return self.options.code()
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
    def specific_action_on_pspict(self,pspict):
        a = []
        if self.marque :
            P = self.mark_point()
            P.parameters.symbol=""
            P.marque = True
            P.mark = self.mark
            pspict.DrawGraph(P)
        if self.cut_ymin:
            pspict.DrawGraphs( self.pieces  )
        elif self.wavy :          
            waviness = self.waviness
            curve=self.parametric_curve()
            curve.parameters=self.parameters.copy()
            curve.wave(self.waviness.dx,self.waviness.dy)
            pspict.DrawGraph(curve)

            #All the wave stuff on phyFunction is now using parametric curve.
            #TODO : we have to implement y_cut to InterpolationCurve
            #curve=InterpolationCurve( self.get_wavy_points(waviness.mx,waviness.Mx,waviness.dx,waviness.dy),context_object=self)
            #pspict.DrawGraph(curve)
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
            deb = numerical_approx(self.mx) 
            fin = numerical_approx(self.Mx)
            curve=self.parametric_curve().graph(deb,fin)
            return curve.latex_code(language=language,pspict=pspict)
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

# TODO : the following should work
#    f=phyFunction(2*x**2-x-1).graph(-0.8,1.3)
#    a=f.coefficient(x,2)
#    b=f.coefficient(x,1)
#    c=f.coefficient(x,0)
# when an attribute is not found, GraphOfAphyFunction should try the attribute of self.sage

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
        <class 'phystricks.BasicGeometricObjects.GraphOfAPoint'>
        sage: print paths[1][3]
        <Point(4.87405534614,-4.6644295302)>
    """
    l=[]
    for path in get_paths_from_plot(p):
        pp=[]
        for vertice in path.vertices:
            pp.append(Point(vertice[0],vertice[1]))
        l.append(pp)
    return l

class SurfaceBetweenLines(GraphOfAnObject):
    def __init__(self,curve1,curve2):
        """
        Give the graph of the surface between the two lines.

        The lines are needed to have a starting and ending point
        that will be joined by straight lines.
        """
        # By convention, the first line goes from left to right and the second one to right to left.

        GraphOfAnObject.__init__(self,self)

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
# These functions return an object GraphOfASurfaceBetweenParametricCurves 
# with the right particularization.

class GraphOfASurfaceBetweenParametricCurves(GraphOfAnObject):
    def __init__(self,curve1,curve2,interval1=(None,None),interval2=(None,None),reverse1=False,reverse2=True):
        # TODO: I think that the parameters reverse1 and reverse2 are no more useful
        #   since I enforce the condition curve1 : left -> right by hand.
        GraphOfAnObject.__init__(self,self)

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

class GraphOfAnInterpolationCurve(GraphOfAnObject):
    def __init__(self,points_list,context_object=None):
        GraphOfAnObject.__init__(self,self)
        self.parameters.color="brown"
        self.points_list=points_list
        self.I=self.points_list[0]
        self.F=self.points_list[-1]
        self.context_object=context_object
        if self.context_object is None:
            self.contex_object=self
    def get_minmax_data(self):
        """
        Return a dictionary whose keys give the xmin, xmax, ymin, and ymax
        data for this graphic.

        EXAMPLES::

        sage: from phystricks import *
        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).get_minmax_data()
        {'xmin': -1.0, 'ymin': -1.0, 'ymax': 1.0, 'xmax': 1.0}

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
    def mark_point(self,pspict=None):
        return self.points_list[-1]
    def bounding_box(self,pspict=None):
        """
        Return the bounding box of the interpolation curve

        EXAMPLES::

        sage: from phystricks import *
        sage: print InterpolationCurve([Point(0,0),Point(1,1)]).bounding_box()
        <BoundingBox mx=0.0,Mx=1.0; my=0.0,My=1.0>

        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: print InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).bounding_box()
        <BoundingBox mx=-1.0,Mx=1.0; my=-1.0,My=1.0>

        NOTE::

        Since the bounding box is computed from the give points while the curve is an interpolation,
        this bounding box is incorrect to the extend that \pscurve does not remains in the convex hull
        of the given points.

        EXAMPLE:
        sage: F=InterpolationCurve([Point(-1,1),Point(1,1),Point(1,-1),Point(-1,-1)])
        sage: print F.bounding_box()
        <BoundingBox mx=-1.0,Mx=1.0; my=-1.0,My=1.0>

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

        EXAMPLES::

        sage: from phystricks import *
        sage: C=Circle(Point(0,0),1)
        sage: F=InterpolationCurve([Point(0,0),Point(1,1)])
        sage: print F.pstricks_code()
        \pscurve[linestyle=solid,linecolor=brown](0,0)(1.00000000000000,1.00000000000000)
        sage: H=InterpolationCurve([Point(-1,1),Point(1,1),Point(1,-1),Point(-1,-1)])
        sage: print H.pstricks_code()
        \pscurve[linestyle=solid,linecolor=brown](-1.00000000000000,1.00000000000000)(1.00000000000000,1.00000000000000)(1.00000000000000,-1.00000000000000)(-1.00000000000000,-1.00000000000000)
        """

        # Explanation of 295815047.
        # It seems to me that very large lines like the ones describing a curve cause 
        #  ! TeX capacity exceeded, sorry [pool size=6179214].

        l = []
        try:
            params=self.context_object.params(language="pstricks")
        except AttributeError :
            params=self.params()
        l.append("\pscurve["+params+"]")
        for p in self.points_list:
            l.append(p.coordinates(numerical=True,pspict=pspict))
        return "".join(l)
    def tikz_code(self,pspict=None):
        l = []
        #try:
        #    params=self.context_object.params(language="tikz")
        #except AttributeError :
        params=self.params(language="tikz")
        l.append("\draw [{0}] plot [smooth,tension=1] coordinates {{".format(params))
        for p in self.points_list:
            l.append(p.coordinates(numerical=True,digits=3,pspict=pspict))  # 295815047.
        l.append("};")
        return "".join(l)
    def latex_code(self,language,pspict=None):
        if language=="pstricks":
            return self.pstricks_code(pspict)
        if language=="tikz":
            return self.tikz_code(pspict)
    def __str__(self):
        """
        Return a string representation

        EXAMPLES::


        sage: from phystricks.BasicGeometricObjects import *
        sage: print InterpolationCurve([Point(0,0),Point(1,1)])
        <InterpolationCurve with points ['<Point(0,0)>', '<Point(1,1)>']>
        """
        return "<InterpolationCurve with points %s>"%(str([str(P) for P in self.points_list]))

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

class GraphOfACustomSurface(GraphOfAnObject):
    """
    INPUT:

    - args - A list or a tuple of graphs that can compose a \pscustom
    """
    def __init__(self,args):
        GraphOfAnObject.__init__(self,self)
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
                obj_code=obj.latex_code(language="tikz",pspict=pspict)
                l.append( draw_to_fill(obj_code) )

                #if isinstance(obj,GraphOfASegment):
                #    l.append( obj.I.coordinates(numerical=True)+" -- "+obj.F.coordinates(numerical=True) )
                #else :
                #    l.append(obj.latex_code(language="tikz",pspict=pspict).replace(";",""))
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
            a.append(self.pstricks_code(pspict))
        if language=="tikz":
            a.append(self.tikz_code(pspict))
        if self._draw_edges :
            for obj in self.graphList :
                obj.parameters = self.edges.copy()
                a.append(obj.latex_code(language=language,pspict=pspict))
        return '\n'.join(a)

class GraphOfAPolygon(GraphOfAnObject):
    """
    INPUT:

    - ``args`` - a tuple of points.

    NOTE:

    This class is not intended to be used by the end-user. The latter has to use :func:`Polygon`.
    """
    def __init__(self,points_list):
        GraphOfAnObject.__init__(self,self)
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
    def make_edges_independent(self):
        """
        make the edges customisation independent the one to the other.
        """
        for s in self.edges :
            s.parameters=Parameters()
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

# GraphOfARectangle once inherited from GeometricRectangle):   (June 26, 2014)
class GraphOfARectangle(GraphOfAPolygon):
    """
    The parameters of the four lines are by default the same, but they can be adapted separately.

    graph_N returns the north side as a phystricks.Segment object
    The parameters of the four sides have to be set independently.

    The drawing is done by \psframe, so that, in principle, all the options are available.
    """
    def __init__(self,NW,SE):
        #GraphOfAnObject.__init__(self,self)
        self.NW = NW
        self.SE = SE
        self.SW = Point(self.NW.x,self.SE.y)
        self.NE = Point(self.SE.x,self.NW.y)
        GraphOfAPolygon.__init__(self,[self.SW,self.SE,self.NE,self.NW])
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
        return GraphOfARectangle

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

    # Inherited from GraphOfAPolygon

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

class GraphOfAParametricCurve(GraphOfAnObject):
    def __init__(self,f1,f2,llamI,llamF):
        """
        Use the constructor :func:`ParametricCurve`.

        INPUT:

        - ``f1,f2`` - two functions.

        - ``llamI,llamF`` - initial and final values of the parameter.

        ATTRIBUTES:

        - ``plotpoints`` - (default=1000)  number of points to be computed.
                           If the function seems wrong, increase that number.
                           It can happen with functions like sin(1/x) close to zero:
                            such a function have too fast oscillations.

        """
        if isinstance(f1,GraphOfAParametricCurve):
            print("You cannot creare a parametric curve by giving a parametric curve")
            raise TypeError
        GraphOfAnObject.__init__(self,self)
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
        self.parameters.plotpoints = "1000"
        self.record_arrows=[]
        #TODO: if I remove the protection "if self.llamI", sometimes it 
        # tries to make self.get_point(self.llamI) with self.llamI==None
        # In that case the crash is interesting since it is a segfault instead of an exception.
        if self.llamI != None:
            self.I=self.get_point(self.llamI,advised=False)   
            self.F=self.get_point(self.llamF,advised=False)
    def pstricks(self,pspict=None):
        # One difficult point with pstrics is that the syntax is "f1(t) | f2(t)" with the variable t.
        #   In order to produce that, we use the Sage's function repr and the syntax f(x=t)
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
        
            sage: from phystricks import *
            sage: x=var('x')
            sage: f1=phyFunction(cos(2*x))
            sage: f2=phyFunction(x*exp(2*x))
            sage: F=ParametricCurve(f1,f2)
            sage: print F.derivative()
            <The parametric curve given by
            x(t)=-2*sin(2*t)
            y(t)=2*t*e^(2*t) + e^(2*t)>
            sage: print F.derivative(3)
            <The parametric curve given by
            x(t)=8*sin(2*t)
            y(t)=8*t*e^(2*t) + 12*e^(2*t)>
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
        #       put_arrow on GraphOfASegment. 
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
        # The delicate part is to decide if we want to return N or -N. We select the angle which is on the same side of the curve
        #                                           than the second derivative.
        # If v is the second derivative, either N or -N has positive inner product with v. We select the one with
        # negative inner product since the second derivative vector is inner.
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
            {'xmin': -0.375, 'ymin': -1.948, 'ymax': 1.948, 'xmax': 3.0}

        NOTE:

        Cutting to 3 decimals is a way to produce more reproducible results. 
        It turns out the Sage's get_minmax_data produce unpredictable figures.

        """
        if deb==None:
            raise
        d = MyMinMax(parametric_plot( (self.f1.sage,self.f2.sage), (deb,fin) ).get_minmax_data(),decimals=decimals)
        # for the curve (x,0), Sage gives a bounding box ymin=-1,ymax=1.
        # In order to avoid that problem, when the surface under a function is created, the second curve (the one of y=0)
        # is given the attribute nul_function to True
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
    def arc_length(self,mll=None,Mll=None):
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
            sage: bool( abs(pi*sqrt(2)/2) - curve.arc_length(0,sqrt(2)) <0.01) 
            True
        
        """
        if mll==None :
            mll=self.llamI
        if Mll==None :
            Mll=self.llamF
        return numerical_integral(self.speed,mll,Mll)[0]
    def get_parameter_at_length(self,l):
        """
        return the value of the parameter corresponding to the given arc length.
        """
        # TODO : create this function
        pass 
    def get_regular_parameter(self,mll,Mll,dl,initial_point=False,final_point=False,xunit=1,yunit=1):
        """ 
        returns a list of values of the parameter such that the corresponding points are equally spaced by dl.
        Here, we compute the distance using the method arc_length.

        INPUT:

        - ``mll,Mll`` - the initial and final values of the parameters.

        - ``dl`` - the arc length distance between the points corresponding
                    to the returned values.

        - ``initial_point`` - (default=False) it True, return also the initial parameters (i.e. mll).

        - ``final_point`` - (default=False) it True, return also the final parameter (i.e. Mll)

        """
        prop_precision = float(dl)/100      # precision of the interval

        x=var('x')
        Vf1=phyFunction(self.f1(xunit*x))
        Vf2=phyFunction(self.f2(yunit*x))
        Vcurve=ParametricCurve(Vf1,Vf2)

        fp = Vcurve.derivative()
        minDll = abs(Mll-mll)/1000
        ll = mll
        PIs = []
        if initial_point:
            PIs.append(mll)
        if final_point:
            PIs.append(Mll)
        while ll < Mll :
            # Here if one removes numerical=True, we got a segfault in some cases
            v = sqrt( (fp.f1(ll,numerical=True))**2+(fp.f2(ll,numerical=True))**2 )
            if v == 0 :
                Dll = minDll
            Zoom = 1
            Dll = dl/v
            grand = Mll
            petit = ll
            if abs(Vcurve.arc_length(ll,ll+Dll)) > dl :
                grand = ll+Dll
                while abs(Vcurve.arc_length(ll,petit)) > dl :
                    petit = (grand+petit)/2
            else :
                petit = ll+Dll
                while abs(Vcurve.arc_length(ll,grand)) < dl :
                    grand = 2*grand - ll
            ell = (petit+grand)/2
            while abs(Vcurve.arc_length( ll, ell )-dl) > prop_precision:
                if prop_precision == 0:
                    raise ValueError,"prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. dl=%s"%str(dl)
                ell = (grand+petit)/2
                if Vcurve.arc_length(ll,ell) > dl :
                    grand = ell
                else :
                    petit = ell
            ll = (petit+grand)/2
            if ll < Mll :
                PIs.append( ll )

        return PIs

    def get_regular_points(self,mll,Mll,dl):
        """
        Return a list of points regularly spaced (with respect to the arc length) by dl. 

        mll is the inital value of the parameter and Mll is the end value of the parameter.

        In some applications, you prefer to use ParametricCurve.get_regular_parameter. The latter method returns the list of
        values of the parameter instead of the list of points. This is what you need if you want to draw tangent vectors for example.
        """
        return [self.get_point(ll) for ll in self.get_regular_parameter(mll,Mll,dl)]
    def get_wavy_points(self,mll,Mll,dl,dy,xunit=1,yunit=1):
        """
        Return a list of points which do a wave around the parametric curve.
        """
        PAs = self.get_regular_parameter(mll,Mll,dl,xunit=xunit,yunit=yunit)
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
        a.append("y(t)=%s>"%repr(self.f2.sage(x=t)))
        return "\n".join(a)

    # Use the generic method 'params' from 'GraphOfAnObject'.  June 27, 2014
    #def params(self,language=None):
    #    self.conclude_params()
    #    if language=="pstricks":
    #        self.add_option("plotpoints=%s"%str(self.parameters.plotpoints))
    #        self.add_option("plotstyle=%s"%str(self.plotstyle))
    #    if language=="tikz":
    #        self.add_option("sample="+str(self.parameters.plotpoints))
    #        self.add_option("plotstyle=%s"%str(self.plotstyle))
    #    return self.options.code(language=language)
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
        y(t)=sin(2*pi - t)>
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
    def latex_code(self,language=None,pspict=None):
        a=[]
        if self.wavy :
            waviness = self.waviness
            curve=InterpolationCurve(self.curve.get_wavy_points(self.llamI,self.llamF,waviness.dx,waviness.dy,xunit=pspict.xunit,yunit=pspict.yunit),context_object=self)
            curve.parameters=self.parameters.copy()
            a.append(curve.latex_code(language=language,pspict=pspict))
        else:
            initial = numerical_approx(self.llamI)      # Avoid the string "pi" in the latex code.
            final = numerical_approx(self.llamF)
            params=self.params(language="tikz")
            plotpoints=self.parameters.plotpoints
            if plotpoints==None :
                plotpoints=100
            import numpy
            Llam=numpy.linspace(initial,final,plotpoints)
            points_list=[ self.get_point(x,advised=False) for x in Llam ]
            curve=InterpolationCurve(points_list)
            curve.parameters=self.parameters.copy()
            a.append( curve.latex_code(language=language,pspict=pspict))
                #Everything is InterpolationCurve. June 27, 2014
                #params=params+",smooth,domain={0}:{1}".format(str(initial),str(final))
                #x=var('x')
                #a.append("\draw[{0}] plot ({{{1}}},{{{2}}});".format(params,self.f1.tikz,self.f2.tikz))
                    #if language=="pstricks":
                    #    a.append("\parametricplot[%s]{%s}{%s}{%s}" %(self.params(),str(initial),str(final),self.curve.pstricks()))
        for v in self.record_arrows:
            a.append(v.latex_code(language=language,pspict=pspict))
        return "\n".join(a)

class GraphOfACircle3D(GraphOfAnObject):
    def __init__(self,op,O,A,B,angleI=0,angleF=0):
        """
        The circle passing trough A and B with center O.

        `A`, `B` and `O` are tuples of numbers
        """
        GraphOfAnObject.__init__(self,self)
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
        curve=GraphOfAnInterpolationCurve(proj_points_list)
        curve.parameters=self.parameters.copy()
        return curve
    def get_point(self,angle):
        return self.center+cos(angle)*self.u+sin(angle)*self.v  
    def get_point2d(self,angle):
        return self.op.point(self.get_point(angle))
    def graph(self,angleI,angleF):
        C = GraphOfACircle3D(self.op,self.O,self.A,self.B,angleI,angleF)
        C.parameters=self.parameters.copy()
        return C
    def bounding_box(self,pspict=None):
        return self.curve2d.bounding_box(pspict)
    def math_bounding_box(self,pspict=None):
        return self.curve2d.math_bounding_box(pspict)
    def specific_action_on_pspict(self,pspict):
        pspict.DrawGraphs(self.curve2d)

class HistogramBox(GraphOfAnObject):
    """
    describes a box in an histogram.
    """
    def __init__(self,a,b,n,histo):
        """
        It is given by the initial value, the final value and the "surrounding" histogram
        """
        GraphOfAnObject.__init__(self,self)
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

class GraphOfAnHistogram(GraphOfAnObject):
    """
    An histogram is given by a list of tuple '(a,b,n)' where 'a' and 'b' are the extremal values of the box and 'n' is the number of elements in the box.
    """
    def __init__(self,tuple_box_list):
        GraphOfAnObject.__init__(self,self)
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

class GraphOfAMoustache(GraphOfAnObject):
    def __init__(self,minimum,Q1,M,Q3,maximum,h,delta_y=0):
        GraphOfAnObject.__init__(self,self)
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

class GraphOfABarDiagram(object):
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

class GraphOfARightAngle(GraphOfAnObject):
    def __init__(self,d1,d2,l,n1,n2):
        """
        two lines and a distance.

        n1 and n2 are 0 or 1 and indicating which sector has to be marked.
        'n1' if for the intersection with d1. If 'n1=0' then we choose the intersection nearest to d1.I
        Similarly for n2
        """
        GraphOfAnObject.__init__(self,self)
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

        self.l=l
        self.n1=n1
        self.n2=n2
        self.intersection=Intersection(d1,d2)[0]
    def specific_action_on_pspict(self,pspict):
        circle=Circle(self.intersection,self.l)

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

        if "I" in P1.coordinates():
            print("RKXTooEGijdq","P1")
            raise
        if "I" in P2.coordinates():
            print("ZGRZooFXJBXE","P2")
            print(circle.equation,self.d2.equation)
            raise
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

class GraphOfASudokuGrid(object):
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
    # No need to give a precise bounding box. Since the elements will be inserted with pspict.DrawGraph,
    # their BB will be counted in the global BB.
    def math_bounding_box(self,pspict):
        return BoundingBox()
    def bounding_box(self,pspict):
        return BoundingBox()
    def latex_code(self,language=None,pspict=None):
        return ""

class GraphOfAFractionPieDiagram(GraphOfAnObject):
    def __init__(self,center,radius,a,b):
        """
        The pie diagram for the fraction 'a/b' inside the circle of given center and radius.

        2/4 and 1/2 are not treated in the same way becaise 2/4 divides the pie into 4 parts (and fills 2) while 1/2 divides into 2 parts.
        """
        GraphOfAnObject.__init__(self,self)
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
        
class BoundingBox(object):
    r"""
    Represent the bounding box of something.

    INPUT:

    - ``dSW`` - The point at the "South-West" corner of the bounding box.

    - ``dNE`` - The point at the "North-East" corner of the bounding box.

    - ``parent`` - the object of which this is the bounding box.

    By default, the bounding box has `mx=1000`, `Mx=-1000` and the same for `y`.

    The attribute `parent` is used for drawing the bounding boxes that can vary with
    the dilatation. The usual way for drawing the bounding bow of the mark of an object is to put
    `P.mark.bounding_box(pspict)` in `pspict.DrawGraph`.

    The problem arises when one dilates the figure after the call to `DrawGraph`.
    Indeed the bounding box of the mark will be the LaTeX's size of the box
    containing the text. In order to be correct one has to take into account the 
    parameters `xunit`/`yunit` that are not yet fixed at the time of `DrawGraph`.

    EXAMPLE::

        sage: from phystricks import *
        sage: pspict,fig = SinglePicture("DefinitionCartesiennes")  #random
        sage: P=Point(1,1)
        sage: P.put_mark(0.3,0,"$MMM$")
        sage: bb = P.mark.bounding_box(pspict)  #random
        sage: print bb
        <BoundingBox mx=1.20000000000000,Mx=1.40000000000000; my=0.90000000000000002,My=1.1000000000000001>
        sage: pspict.dilatation(2)
        sage: bb = P.mark.bounding_box(pspict) #random
        sage: print bb
        <BoundingBox mx=1.10000000000000,Mx=1.20000000000000; my=0.94999999999999996,My=1.05>

    In the first call, the bounding box is not the same as in the second call.

    If 'math' is True, it always try to include 'math_bounding_box' instead of 'bounding_box'

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

        #if pspict==None:
        #    raise ValueError
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

import phystricks.main as main
import phystricks.SmallComputations as SmallComputations
