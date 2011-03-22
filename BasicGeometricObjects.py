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

# copyright (c) Laurent Claessens, 2010-2011
# email: moky.math@gmai.com

"""
This module contains the basic graphics elements like points, segments and vectors. 
Each of them have the methods for basic geometric manipulations: rotations, dilatations, tangent vector, etc.

The end-user should not use the functions whose name begin with ``GraphOf`` or ``Geometric``. 
Rather he has to use the constructors like :func:`Point`, :func:`AffineVector` and so on.
"""

import math
import types
from sage.all import *
from phystricks import *
from phystricks.SmallComputations import *
import doctest


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

#class ListeNomsPoints(object):
#    """
#    This class serves to give a psname to my points. 
#
#    TODO: use a real iterator.
#    """
#    def __init__(self):
#        self.donne = 1000
#    def suivant(self):
#        self.donne = self.donne + 1
#        s = str(self.donne)
#        return "".join( [chr(int(c)+97) for c in s] )

def PointsNameList():
    """
    Furnish a list of points name.

    This is the generator of the sequence of strings 
    "aaaa", "aaab", ..., "aaaz","aaaA", ..., "aaaZ","aaba" etc.

    EXAMPLES::
    
        sage: x=PointsNameList()
        sage: x.next()
        'aaaa'
        sage: x.next()
        'aaab'
    """
    # The fact that this function return 4 character strings is hard-coded here 
    #   and that 4 is hard-coded in the function unify_point_name
    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for i in alphabet:
        for j in alphabet:
            for k in alphabet:
                for l in alphabet:
                    yield i+j+k+l

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

    """
    if xvalues is None and yvalues is None and draw_points is None :
        return GeometricVectorField(fx,fy)
    return GeometricVectorField(fx,fy).graph(xvalues,yvalues,draw_points)

def _vector_pstricks_code(segment,pspict=None):
    """
    Return the pstricks's code of a Segment when is is seen as a vector.
    """
    a = segment.I.create_PSpoint() + segment.F.create_PSpoint()
    a = a + "\\ncline["+segment.params()+"]{->}{"+segment.I.psName+"}{"+segment.F.psName+"}"
    if segment.marque :
        P = segment.F
        P.parameters.symbol = "none"
        P.put_mark(segment.mark.dist,segment.mark.angle,segment.mark.text)
        a = a + P.pstricks_code(pspict)
    return a

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
    # the following is thanks to the python's french usenet group
    #https://groups.google.com/group/fr.comp.lang.python/browse_thread/thread/5b19cfac661df251?hl=fr#
    #http://users.rcn.com/python/download/Descriptor.htm
    #vect.pstricks_code = types.MethodType(_vector_pstricks_code, vect, Segment)
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
    def wave(self,dx,dy):                   # dx is the wave length and dy is the amplitude
        self.wavy = True
        self.waviness = Waviness(self,dx,dy)
    def put_mark(self,dist,angle,text,automatic_place=False):
        self.marque = True
        self.mark = Mark(self,dist,angle,text,automatic_place)
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
        self.parameters.add_to_options(self.options)
    def params(self):
        self.conclude_params()
        return self.options.code()

class GeometricPoint(object):
    """
    This is a point. It is defined by its Cartesian coordinates.

    EXAMPLES:

        sage: print Point(1,1)
        Point(1,1)
        sage: print Point(pi,sqrt(2))
        Point(pi,sqrt(2))
    """
    NomPointLibre = PointsNameList()
    
    def __init__(self,x,y):
        self.x=SR(x)
        self.y=SR(y)
    
    @lazy_attribute
    def psName(self):
        return GeometricPoint.NomPointLibre.next()

    def projection(self,seg):
        """
        Return the projection of the point on the given segment.

        INPUT:

        - ``seg`` - a segment

        OUTPUT:

        a point.

        EXAMPLES:

        Return a point even if the projections happens to lies outside the segment::

            sage: s1=Segment( Point(0,0),Point(2,1) )
            sage: print Point(3,-1).projection(s1)
            Point(2,1)
            sage: print Point(5,0).projection(s1) 
            Point(4,2)

        You con project on a vector::

            sage: print Point(5,0).projection(Vector(2,1))
            Point(4,2)

        Computations are exact::

            sage: v=Vector(2,1)
            sage: print Point(sqrt(2),pi).projection(v)
            Point(2/5*pi + 4/5*sqrt(2),1/5*pi + 2/5*sqrt(2))

        """
        try :
            seg=seg.segment()       # allows to project onto an axe
        except AttributeError :
            pass
        if seg.vertical :
            return Point(seg.I.x,self.y)
        if seg.horizontal :
            return Point(self.x,seg.I.y)
        else :
            Rx = (self.y*seg.slope - seg.slope*seg.independent + self.x)/(seg.slope**2 + 1)
            Ry = (self.y*seg.slope**2 + self.x*seg.slope + seg.independent)/(seg.slope**2 + 1)
            return Point(Rx,Ry)
    def get_polar_point(self,r,theta,pspict=None):
        """
        Return the point located at distance r and angle theta from point self.

        INPUT:

        - ``r`` - A number.

        - ``theta`` - the angle (degree or :class:`AngleMeasure`).

        - ``pspict`` - the pspicture in which the point is supposed to live. If `pspict` is given, we compute the deformation due to the dilatation.  Be careful: in that case `r` is given as absolute value and the visual effect will not be affected by dilatations.

        OUTPUT: A point.

        EXAMPLES::

            sage: P=Point(1,2)
            sage: print P.get_polar_point(sqrt(2),45)
            Point(2,3)

        """
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

        EXAMPLES:

        You can translate by a :func:`Vector`::

            sage: v=Vector(2,1)                        
            sage: P=Point(-1,-1)
            sage: print P.translate(v)
            Point(1,0)

        An :func:`AffineVector` is accepted::

            sage: w=AffineVector( Point(1,1),Point(2,3) )
            sage: print P.translate(w)
            Point(0,1)

        You can also directly provide the coordinates::

            sage: print P.translate(10,-9)
            Point(9,-10)

        Or the :func:`Point` corresponding to the translation vector::

            sage: print P.translate( Point(3,4)  )
            Point(2,3)

        Translation by minus itself produces zero::

            sage: x,y=var('x,y')
            sage: P=Point(x,y)
            sage: print P.translate(-P)
            Point(0,0)

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

        EXAMPLES:
        sage: Point(1,1).norm()
        sqrt(2)
        sage: Point(-pi,sqrt(2)).norm()
        sqrt(pi^2 + 2)
        """
        return Segment(Point(0,0),self).length()
    def length(self):
        """
        The same as self.norm()

        EXAMPLES:
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
        P.parameters.symbol="none"
        return P.pstricks_code(None)+"\n"
    def polar_coordinates(self):
        """
        Return the polar coordinates of the point as a tuple (r,angle) where angle is given in degree.
        """
        r=self.norm()
        if self.x==0:
            radian=pi/2
        else :
            radian=arctan(self.y/self.x)
        if self.x<0:
            if self.y>0:
                radian=pi/2-radian
            if self.y<=0:
                radian=pi+radian
        angle=AngleMeasure(value_radian=radian)
        return r,angle
    def angle(self):
        """
        Return the angle of the segment from (0,0) and self

        Return the result in degree
        """
        return self.polar_coordinates()[1]
    def coordinates(self,numerical=False):
        """
        Return the coordinates of the point as a string.

        When one coordinate if very small (lower than 0.0001), it is rounded to zero in order to avoid string like "0.2335e-6" in the pstricks code.

        Example : 
        sage: P=Point(1,3)
        sage: print P.coordinates()
        (1,3)
        """
        if numerical :
            x=numerical_approx(self.x)
            y=numerical_approx(self.y)
        else :
            x = self.x
            y = self.y
        # This precaution in order to avoid something like 0.125547e-6 because pstricks doesn't like that notation.
        if abs(x) < 0.0001 :
            x=0
        if abs(y) < 0.0001 :
            y=0
        return "("+str(x)+","+str(y)+")"
    def coordinatesBr(self):
        return self.coordinates.replace("(","{").replace(")","}")
    def Affiche(self):
        return self.coordinates()
    def graph_object(self):
        return GraphOfAPoint(self)
    def copy(self):
        return Point(self.x,self.y)
    def __eq__(self,other):
        """
        return True if the coordinates of `self` and `other` are the same.

        INPUT:
        
        - ``other`` - an other point

        OUTPUT:

        boolean

        EXAMPLES:

        The fact to change the properties of a point don't change the equality::

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
        """
        try :
            dx = v.Dx
            dy = v.Dy
        except AttributeError :
            try :
                dx = v.x
                dy = v.y
            except AttributeError :
                raise TypeError, "You seem to add myself with something which is not a Point neither a Vector. Sorry, but I'm going to crash."
        return Point(self.x+dx,self.y+dy)
    def __sub__(self,v):
        return self+(-v)
    def __neg__(self):
        return Point(-self.x,-self.y)
    def __mul__(self,r):
        return Point(r*self.x,r*self.y)
    def __rmul__(self,r):
        return self.__mul__(r)
    def __str__(self):
        return "Point(%s,%s)"%(str(self.x),str(self.y))

class GeometricSegment(object):
    def __init__(self,A,B,arrow_type="segment"):
        self.I = A
        self.F = B
        self.arrow_type=arrow_type

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

        EXAMPLES:
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

        EXAMPLES:
        sage: s = Segment(Point(0,3),Point(6,-1))
        sage: s.independent
        3

        sage: Segment(Point(1,2),Point(-1,1)).independent
        3/2
        """
        return self.I.y-self.I.x*(self.slope)

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

        EXAMPLES:
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
        var('x,y')
        return self.coefs[0]*x+self.coefs[1]*y+self.coefs[2] == 0
 
    @lazy_attribute
    def length(self):
        """
        return the length of the segment

        EXAMPLES:
        sage: Segment(Point(1,1),Point(2,2)).length
        sqrt(2)

        """
        return Distance(self.I,self.F)

    @lazy_attribute
    def advised_mark_angle(self):
        x = self.angle()+AngleMeasure(value_degree=90)
        return x

    def copy(self):
        v=Segment(self.I,self.F)
        v.arrow_type=self.arrow_type
        return v

    def phyFunction(self):
        if self.horizontal:
            # The trick to define a constant function is explained here:
            # http://groups.google.fr/group/sage-support/browse_thread/thread/e5e8775dd79459e8?hl=fr?hl=fr
            var('x')
            fi = SR(A.y).function(x)
            return phyFunction(fi)
        if not (self.vertical or self.horizontal) :
            parms = [self.slope,(A.y*B.x-A.x*B.y)/(A.x-B.x)]
            var('x')
            return phyFunction( self.slope*x+self.independent )

    def get_regular_points(self,dx):
        """
        Notice that it does not return the last point of the segment, unless the length is a multiple of dx.
           this is why we add by hand the last point in GetWavyPoint
        """
        n = floor(self.length/dx)
        return [self.proportion(float(i)/n) for i in range(0,n)]
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
    def proportion(self,p):
        """
        returns a point on the segment which is at the position
        (p-1)*I+p*F
        if I and F denote the initial and final point of the segment.
        """
        return self.I*(1-p) + self.F*p
    def Point(self):
        """
        Return the point X such that as free vector, 0->X == self

        More precisely, if self is the segment A->B, return the point B-A
        """
        return self.F-self.I

    def center(self):
        P = self.proportion(0.5)
        P.advised_mark_angle=self.angle().degree+90
        return P

    def AffineVector(self):
        return AffineVector(self.I,self.F)
    def get_normal_vector(self):
        """
        returns a normalized normal vector at the center of the segment

        OUTPUT:
        A vector

        EXAMPLES:
        sage: v= Segment(Point(0,0),Point(2,0)).get_normal_vector()
        sage: print v
        vector I=Point(1.0,0) F=Point(1.0,-1)
        sage: v.length()
        1
        """
        if self.vertical :
            return Point(-1,0).Vector().origin(self.center())
        else :
            P = Point(self.slope,-1)
            return P.Vector().normalize().origin(self.center())
    def polaires(self):
        return PointToPolaire(self.Point())
    def angle(self):
        """
        return the angle of the segment.

        This is the angle between the segment and the horizontal axe.

        EXAMPLES:
        sage: S=Segment(Point(1,1),Point(2,2))
        sage: type(S.angle())
        <class 'phystricks.SmallComputations.AngleMeasure'>
        sage: S.angle().degree
        45
        sage: S.angle().radian
        1/4*pi

        sage: v=AffineVector(Point(2,3),Point(2-4/sqrt(3),-1))
        sage: v.angle().radian.simplify_trig()
        4/3*pi
        """
        return self.polaires().measure
    def origin(self,P):
        """
        return a vector (in affine space) whose origin is P.
        """
        return AffineVector(P,Point(P.x+self.Dx,P.y+self.Dy))
    def direction(self):
        d=self.F-self.I
        return d
    def return_deformations(self,segment):
        segment.arrow_type=self.arrow_type
        return segment
    def projection(self,segment):
        """
        Return the projection of self on the given segment

        It also works with vectors

        INPUT:
        - ``segment`` - the line on which we want to project

        EXAMPLES:
        sage: l = Segment(Point(0,0),Point(0,1))
        sage: v = AffineVector(Point(-1,1),Point(-2,3))
        sage: print v.equation
        x + 1/2*y + 1/2 == 0
        sage: print v.projection(l)
        vector I=Point(0,1) F=Point(0,3)
        sage: print l.projection(v)
        segment I=Point(-2/5,-1/5) F=Point(-4/5,3/5)

        
        sage: l = Segment(Point(0,0),Point(1,2))
        sage: s = Segment(Point(-2,1),Point(-3,4))
        sage: print s.projection(l)
        segment I=Point(0,0) F=Point(1,2)
        """
        v = Segment(self.I.projection(segment),self.F.projection(segment))
        return self.return_deformations(v)
    def orthogonal(self):
        """
        return the segment with a rotation of 90 degree. The new segment is still attached to the same point.

        Not to be confused with self.get_normal_vector
        """
        new_Dx=-self.Dy
        new_Dy=self.Dx
        v=Segment(self.I,Point(self.I.x+new_Dx,self.I.y+new_Dy))
        return self.return_deformations(v)
    def translate(self,vecteur):
        v = Segment(self.I.translate(vecteur),self.F.translate(vecteur))
        return self.return_deformations(v)
    def fix_origin(self,a,b=None):
        """
        Return the segment fixed at `P`. This is the translation of `self`  by `P-self`.

        Typically it is used in the framework of affine vector..

        INPUT:

        - ``P`` - The point on which we want to "attach" the new segment.

        OUTPUT:

        A new segment (or vector) with initial point at `P`

        EXAMPLES:
    
        We can fix the orignin by giving the coordinates of the new origin::

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
        v = PolarSegment(self.I,self.polaires().r,self.polaires().degree+angle)
        return self.return_deformations(v)
    def add_size_extemity(self,l):
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
    def add_size(self,lI,lF):
        """
        Return a new Segment with extra length lI at the initial side and lF at the final side. 
        """
        F=self.add_size_extemity(lF).F
        I=self.inverse().add_size_extemity(lI).F
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

        EXAMPLES:
        sage: S=Segment(Point(-2,-2),Point(2,2))
        sage: print S.dilatation(0.5)           
        segment I=Point(-1.00000000000000,-1.00000000000000) F=Point(1.00000000000000,1.00000000000000)

        But
        sage: v=AffineVector(Point(-2,-2),Point(2,2))
        sage: print v.dilatation(0.5)                
        vector I=Point(-2,-2) F=Point(0.000000000000000,0.000000000000000)
        """
        if self.arrow_type=="segment":
            d=0.5*self.length()*(coef-1)
            return self.add_size(d,d)
        if self.arrow_type=="vector":
            l=self.length*coef
            return self.normalize(l)
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

        EXAMPLES:
        sage: s=Segment(Point(0,0),Point(1,0))
        sage: print s.normalize(2)
        segment I=Point(-0.5,0) F=Point(1.5,0)
        sage: print s.normalize(-1)
        segment I=Point(0,0) F=Point(1,0)

        sage: v=AffineVector(Point(1,1),Point(3,1))
        sage: print v.normalize(2)
        vector I=Point(1,1) F=Point(3,1)
        sage: print v.normalize(-1)
        vector I=Point(1,1) F=Point(0,1)
        """
        if self.arrow_type=="segment":
            if l<0 : 
                l=-l
            v = self.fix_size(l)
        if self.arrow_type=="vector":
            L=self.length()
            if L==0:
                return self.copy()
            v = l*self/L
            v.arrow_type="vector"
        return self.return_deformations(v)
    def graph(self):
        return GraphOfASegment(self)
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return GraphOfASegment
    def Affiche(self):
        raise DeprecationWarning,"use print instead"
        return str(self.equation[0])+" x + "+str(self.equation[1])+" y + "+str(self.equation[2])
    def __mul__(self,coef):
        """
        multiply the segment by a coefficient.

        INPUT:
        - ``coef`` - the multiplying coefficient

        OUTPUT:
        A new segment or vector.

        EXAMPLES:
        sage: v=Vector(1,1)
        sage: print 2*v
        vector I=Point(0,0) F=Point(2,2)
        sage: print -2*v
        vector I=Point(0,0) F=Point(-2,-2)

        sage: s=Segment(Point(1,1),Point(2,2))
        sage: print 3*s
        segment I=Point(1,1) F=Point(4,4)

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

        INPUT:
        - ``other`` - an other segment

        OUTPUT:
        A new vector

        EXAMPLES:
        sage: a=Vector(1,1)
        sage: b=Vector(2,3)
        sage: print a+b
        vector I=Point(0,0) F=Point(3,4)

        sage: a=Segment(Point(1,1),Point(3,4))
        sage: b=AffineVector(Point(1,1),Point(-1,3))
        sage: print a+b
        segment I=Point(1,1) F=Point(1,6)
        """
        if isinstance(other,GeometricSegment):
            if self.I == other.I:
                v=Vector(self.F.x-self.I.x+other.F.x-other.I.x, self.F.y-self.I.y+other.F.y-other.I.y,)
                return self.return_deformations(v.origin(self.I))
            else:
                raise TypeError,"These two segments don't have the same origin. I cannot sum them."
        else:
            raise TypeError,"I do not know how to sum %s with %s"%(self,other)
    def __rmul__(self,coef):
        return self*coef
    def __neg__(self):
        return self*(-1)
    def __div__(self,coef):
        return self * (1/coef)
    def __str__(self):
        if self.arrow_type=="segment":
            return "segment I=%s F=%s"%(str(self.I),str(self.F))
        if self.arrow_type=="vector":
            return "vector I=%s F=%s"%(str(self.I),str(self.F))


class GraphOfACircle(GraphOfAnObject):
    """
    This is a circle, or an arc of circle.

    INPUT:

    - ``center`` - a point, the center of the circle.

    - ``radius`` - a number, the radius of the circle.

    - ``self.angleI`` - (default=0) the beginning angle of the arc (degree).

    - ``self.angleF`` - (default=360) the ending angle of the arc (degree).


    OUTPUT:

    A circle ready to be drawn.

    EXAMPLES::

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
    def __init__(self,center,radius,angleI=0,angleF=360):
        self.center = center
        self.radius = radius
        GraphOfAnObject.__init__(self,self)
        self.diameter = 2*self.radius
        self._parametric_curve=None
        self.angleI = AngleMeasure(value_degree=angleI)
        self.angleF = AngleMeasure(value_degree=angleF)

    @lazy_attribute
    def equation(self):
        """
        Return the equation of `self`.

        OUTPUT:

        an equation.

        EXAMPLES::

            sage: circle=Circle(Point(0,0),1)
            sage: circle.equation()
            x^2 + y^2 - 1 == 0

        ::

            sage: circle=CircleOA(Point(-1,-1),Point(0,0))
            sage: circle.equation()
            (y + 1)^2 + (x + 1)^2 - 2 == 0
        """
        var('x,y')
        return (x-self.center.x)**2+(y-self.center.y)**2-self.radius**2==0
    
    def parametric_curve(self,a=None,b=None):
        """
        Return the parametric curve associated to the circle.

        If optional arguments <a> and <b> are given, return the corresponding graph between the values a and b of the angle.

        The parameter of the curve is the angle in radian.
        """
        if self._parametric_curve is None :
            var('x')
            f1 = phyFunction(self.center.x+self.radius*cos(x))
            f2 = phyFunction(self.center.y+self.radius*sin(x))
            self._parametric_curve = ParametricCurve(f1,f2)
        curve=self._parametric_curve
        if a == None :
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

            sage: C=Circle(Point(0,0),2)
            sage: pts=C.get_regular_points(0,90,1)
            sage: [str(p) for p in pts]
            ['Point(2,0)', 'Point(2*cos(1/2),2*sin(1/2))', 'Point(2*cos(1),2*sin(1))', 'Point(2*cos(3/2),2*sin(3/2))']

        """
        Dtheta=(180/pi)*(l/self.radius)
        if Dtheta==0:
            raise ValueError,"Dtheta is zero"
        pts=[]
        import numpy
        theta=numpy.arange(mx,Mx,step=Dtheta)
        return [self.get_point(t,advised) for t in theta]

    def get_tangent_vector(self,theta):
        return PolarPoint(1,theta+90).origin(self.get_point(theta,advised=False))
    def get_normal_vector(self,theta):
        """
        Return a normal vector at the given angle 
        
        INPUT:

        - ``theta`` - an angle in degree or :class:`AngleMeasure`.

        OUTPUT:

        An affine vector

        EXAMPLES::

            sage: C=Circle(Point(0,0),2)
            sage: print C.get_normal_vector(45)
            vector I=Point(sqrt(2),sqrt(2)) F=Point(3/2*sqrt(2),3/2*sqrt(2))

        """
        v = PolarPoint(1,theta).origin(self.get_point(theta,advised=False))
        v.arrow_type="vector"
        return v
    # Here, angleI and angleF are given in degree while parametric_plot uses radian.
    def get_minmax_data(self,angleI,angleF):
        deb = radian(angleI)
        fin = radian(angleF)
        return MyMinMax(self.parametric_curve().get_minmax_data(deb,fin))
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
        return GraphOfACircle(self.center,self.radius,angleI,angleF)
    def __str__(self):
        return "Circle, center=%s, radius=%s"%(self.center.__str__(),str(self.radius))
    def copy(self):
        """
        Return a copy of the object as geometrical object.
        
        It only copies the center and the radius. In particular
        the following are not copied:

        - style of drawing.

        - initial and final angle if `self` is an arc.

        EXAMPLES:

        Python copies by assignation::

            sage: c1=Circle( Point(1,1),2 )
            sage: c2=c1
            sage: c2.center=Point(3,3)
            sage: print c1.center
            Point(3,3)

        The method :func:`copy` pass through::

            sage: c1=Circle( Point(1,1),3 )
            sage: c2=c1.copy()
            sage: c2.center=Point(3,3)
            sage: print c1.center
            Point(1,1)

        NOTE:

        Due to use of `lazy_attribute`, it is not recommended to change the center of
        a circle after having defined it.

        """
        return Circle(self.center,self.radius)
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        a=simplify_degree(self.angleI,keep_max=True,number=True)
        b=simplify_degree(self.angleF,keep_max=True,number=True)
        angleI=min(a,b)
        angleF=max(a,b)
        pI=self.get_point(angleI)
        pF=self.get_point(angleF)
        bb = BoundingBox(self.center,self.center)
        bb.append(pI,pspict)
        bb.append(pF,pspict)
        if angleI==0:
            bb.AddX(self.center.x+self.radius)
        if angleI<90 and angleF>90 :
            bb.AddY(self.center.y+self.radius)
        if angleI<180 and angleF>180 :
            bb.AddX(self.center.x-self.radius)
        if angleI<270 and angleF>270 :
            bb.AddY(self.center.y-self.radius)
        return bb
    def pstricks_code(self,pspict=None):
        if self.wavy:
            waviness = self.waviness
            alphaI = radian(self.angleI,number=True,keep_max=True)
            alphaF = radian(self.angleF,number=True,keep_max=True)
            if self.angleF.degree==360:        # Because the function radian simplifies modulo 2pi.
                alphaF=2*pi
            curve = self.parametric_curve()
            G = GraphOfAParametricCurve(curve,alphaI,alphaF)
            G.add_option(self.params())
            # The two following lines are a pity. If I add some properties, I have to change by hand...
            G.parameters.style = self.parameters.style
            G.parameters.color = self.color
            G.wave(waviness.dx,waviness.dy)
            return G.pstricks_code()
        else:
            angleI=degree(self.angleI,number=True,converting=False,keep_max=True)
            angleF=degree(self.angleF,number=True,converting=False,keep_max=True)
            if angleI == 0 and angleF == 360 :
                PsA = Point(self.center.x-self.radius,self.center.y)        
                a = PsA.create_PSpoint()
                a = a + self.center.create_PSpoint()
                a = a + "\pstCircleOA["+self.params()+"]{"+self.center.psName+"}{"+PsA.psName+"}"
                return a
                # Some remarks :
                # Besoin d'un point sur le cercle pour le tracer avec \pstCircleOA,"")
                # La commande pscircle ne tient pas compte des xunit et yunit => inutilisable.
                #self.add_latex_line("\pscircle["+params+"]("+Cer.center.psName+"){"+str(Cer.radius)+"}")
            else :
                PsA = self.get_point(angleI)
                PsB = self.get_point(angleF)
                a = PsA.create_PSpoint() + PsB.create_PSpoint() + self.center.create_PSpoint()
                a = a+"\pstArcOAB[%s]{%s}{%s}{%s}"%(self.params(),self.center.psName,PsA.psName,PsB.psName)
                return a

class GeometricRectangle(object):
    """
    The four points of the square are designated by NW,NE,SW and SE.
    """
    def __init__(self,NW,SE):
        self.NW = NW
        self.SE = SE
        self.SW = Point(self.NW.x,self.SE.y)
        self.NE = Point(self.SE.x,self.NW.y)
    def first_diagonal(self):
        return Segment(self.NW,self.SE)
    def second_diagonal(self):
        return Segment(self.SW,self.NE)
    def segment_N(self):
        return Segment(self.NW,self.NE)
    def segment_S(self):
        return Segment(self.SW,self.SE)
    def segment_E(self):
        return Segment(self.NE,self.SE)
    def segment_W(self):
        return Segment(self.NW,self.SW)
    def center(self):
        return self.first_diagonal().center()
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return GraphOfARectangle

def OptionsStyleLigne():
    return ["linecolor","linestyle"]

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
    def code(self):
        a = []
        for op in self.DicoOptions.keys():
            a.append(op+"="+self.DicoOptions[op])
            a.append(",")
        del a[-1:]
        return "".join(a)
    def __getitem__(self,opt):
        return self.DicoOptions[opt]

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
        if type(self.obj) == phyFunction :
            self.Mx = self.graph.Mx
            self.mx = self.graph.mx
    def get_wavy_points(self):
        if type(self.obj) == phyFunction :
            return self.obj.get_wavy_points(self.mx,self.Mx,self.dx,self.dy)
        if type(self.obj) == Segment :
            return self.obj.get_wavy_points(self.dx,self.dy)

class Mark(object):
    def __init__(self,graph,dist,angle,text,automatic_place=False):
        """
        Describe a mark (essentially a P on a point for example)
        angle is given in degree or AngleMeasure

        If automatic_place is True, then place the corner of the box at the point instead of the "central point" of the mark.
        automatic_place is intended to be a tuple of (pspict,anchor)
        where pspict is the pspicture in which we are working and <anchor> is one of "corner","N","S","W","E". By default, "corner" is taken.

        This class should not be used by the end-user.
        """
        self.graph = graph
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
        Thus an object that want to accept a mark has to have a method mark_point that returns the point on which the mark will be put.
        """
        default=self.graph.mark_point().get_polar_point(self.dist,self.angle,pspict)
        if self.automatic_place :
            try :
                position=self.automatic_place[1]
                pspict=self.automatic_place[0]
            except TypeError :
                pspict=self.automatic_place
                position="corner"
            dimx,dimy=pspict.get_box_size(self.text)
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
        else :
            return default
    def math_bounding_box(self,pspict=None):
        """
        Return the mathematics bounding box of its base object.

        A mark has non own math_bounding_box because we do not want the axes to fit even the marques.
        """
        return self.graph.math_bounding_box(pspict)
    def bounding_box(self,pspict=None):
        central_point=self.central_point(pspict)
        bb=BoundingBox(central_point,central_point)
        dimx,dimy=pspict.get_box_size(self.text)
        try :
            dimx=float(dimx)/pspict.xunit
            dimy=float(dimy)/pspict.yunit
        except AttributeError:
            print "Try to pass a pspicture when computing the bounding box of",type(self)
        pt1=Point(central_point.x-dimx/2,central_point.y-dimy/2) 
        pt2=Point(central_point.x+dimx/2,central_point.y+dimy/2)
        bb.AddPoint(pt1)
        bb.AddPoint(pt2)
        return bb
    def pstricks_code(self,pspict=None):
        l=[]
        central_point=self.central_point(pspict)
        #TODO : Use create_PSpoint instead of \pstGeonode.
        l.append("\pstGeonode[]"+central_point.coordinates(numerical=True)+"{"+central_point.psName+"}")
        l.append(r"\rput(%s){\rput(%s;%s){%s}}"%(central_point.psName,"0",0,str(self.text)))
        return "\n".join(l)

class FillParameters(object):
    """
    Represent the parameters of filling a surface.
    """
    def __init__(self):
        self.color= None
        self.style= "solid"
    def add_to_options(self,opt):
        """
        add `self` to a set of options.

    
        INPUT:

        - ``opt`` - an instance of :class:`Options`.

        OUTPUT:

        Return `opt` with added properties.

        EXAMPLES::

            sage: opt=Options()
            sage: fill=FillParameters()
            sage: fill.color="blue"
            sage: fill.add_to_options(opt)
            sage: opt.code()
            'fillcolor=blue,fillstyle=solid'

        ::

            sage: fill.style="MyStyle"
            sage: fill.add_to_options(opt)
            sage: opt.code()
            'fillcolor=blue,fillstyle=MyStyle'

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
        self.color = None
        self.symbol = None
        self.style = None
        self.fill=FillParameters()
        self.hatch=HatchParameters()
        self._filled=False
        self._hatched=False
    def filled(self):
        self._filled=True
    def hatched(self):
        self._hatched=True
    def add_to_options(self,opt):
        """
        Add to the object <opt> (type Option) the different options that correspond to the parameters.

        In an imaged way, this method adds self to the object <opt>.
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


def EnsurephyFunction(f):
    if "sage" in dir(f):        # This tests in the same time if the type if phyFunction or GraphOfAphyFunction
        return phyFunction(f.sage)
    else :
        return phyFunction(f)

class SurfaceBetweenFunctions(GraphOfAnObject):
    r"""
    Represents a surface between two functions.

    INPUT:

    - ``f1,f2`` - functions (sage or phyFunction). ``f1`` is considered to be the upper function while ``f2`` is the lower function.

    - ``mx,Mx`` - initial and end values of x.

    EXAMPLES:

    If you want the surface and the functions to be blue ::

        sage: surf=SurfaceBetweenFunctions(sin(x)+3,cos(x),0,2*pi)
        sage: surf.parameters.color="blue"

    If the style of the functions is not set, the functions are not drawn at all.
    In the following example you see that the function ``f1`` is not drawn. In particular, the color red is nowhere::

        sage: surf.f1.parameters.color="red"
        sage: surf.pstricks_code()
        '\\pscustom[hatchcolor=blue,linestyle=none,fillcolor=blue,linecolor=blue,fillstyle=vlines]{\n\\psplot[linestyle=none]{0.000000000000000}{6.28318530717959}{sin(x) + 3}\n\\psplot[linestyle=none]{6.28318530717959}{0.000000000000000}{cos(x)}\n}'

    If you want the function ``f1`` to be red without changing the color of the surface, you have to change
    the color AND the style::

        sage: surf.f1.parameters.color="red"
        sage: surf.f1.parameters.style="solid"
        sage: surf.pstricks_code()
        '\\pscustom[hatchcolor=blue,linestyle=none,fillcolor=blue,linecolor=blue,fillstyle=vlines]{\n\\psplot[linestyle=none]{0.000000000000000}{6.28318530717959}{sin(x) + 3}\n\\psplot[linestyle=none]{6.28318530717959}{0.000000000000000}{cos(x)}\n}\n\\psplot[linestyle=solid,plotpoints=100,linecolor=red]{0.000000000000000}{6.28318530717959}{sin(x) + 3}'

    You can also try to control the option linestyle (use add_option).
    """

    #TODO: change this class into a function which returns a SurfaceBetweenParametricCurves instead.

    # linestyle=none in self.add_option corresponds to the fact that we do not want to draw the curve.
    # No default color are given; the reason is  that we want to be able  to control the color of each element separately. 
    def __init__(self,f1,f2,mx,Mx):
        GraphOfAnObject.__init__(self,self)
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
        bb.append(self.f1,pspict=None)
        bb.append(self.f2,pspict=None)
        bb.AddY(0)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        if self.parameters.color :      # Here we give a default color
            self.add_option("fillcolor="+self.parameters.color+",linecolor="+self.parameters.color+",hatchcolor="+self.parameters.color)
        a=[]
        deb = numerical_approx(self.mx)     # Avoid "pi" in the pstricks code
        fin = numerical_approx(self.Mx)
        a.append("\pscustom["+self.params()+"]{")
        a.append("\psplot[linestyle=none]{"+str(deb)+"}{"+str(fin)+"}{"+self.f1.pstricks+"}")
        a.append("\psplot[linestyle=none]{"+str(fin)+"}{"+str(deb)+"}{"+self.f2.pstricks+"}")
        a.append("}")
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


class SurfaceBetweenParametricCurves(GraphOfAnObject):
    """
    Represents a surface between two parametric curves.

    INPUT:

    - ``curve1,curve2`` - two parametric curves.

    OPTIONAL ARGUMENTS :
    - ``mx1,Mx1`` - initial and final values of the parameter for the first curve.

    - ``mx2,Mx2`` - initial and final values of the parameter for the first curve.
        If these parameters are not given, consider the values of mx and Mx of curve1 and curve2
        (if the latter are graphs).

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

    NOTE:
    If the two curves make intersections, the result could be messy.
    """
    def __init__(self,curve1,curve2,mx1=None,Mx1=None,mx2=None,Mx2=None,reverse1=False,reverse2=True):
        GraphOfAnObject.__init__(self,self)
        self.mx1=mx1
        self.mx2=mx2
        self.Mx1=Mx1
        self.Mx2=Mx2
        self.reverse1=reverse1
        self.reverse2=reverse2

        if mx1 is None :
            self.mx1=curve1.llamI
            self.Mx1=curve1.llamF
        if mx2 is None :
            self.mx2=curve2.llamI
            self.Mx2=curve2.llamF

        self.curve1=curve1
        self.curve2=curve2
        self.low_segment=Segment(self.curve2.get_point(self.mx2,advised=False),self.curve1.get_point(self.mx1,advised=False))
        self.up_segment=Segment(self.curve1.get_point(self.Mx1,advised=False),self.curve2.get_point(self.Mx2,advised=False))

        self.add_option("fillstyle=vlines,linestyle=none")  
        self.parameters.color=None              
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        bb.append(self.curve1,pspict=None)
        bb.append(self.curve2,pspict=None)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        if self.parameters.color :      # Here we give a default color
            self.add_option("fillcolor="+self.parameters.color+",linecolor="+self.parameters.color+",hatchcolor="+self.parameters.color)
        a=[]
        
        c1=self.curve1.graph(self.mx1,self.Mx1)
        c2=self.curve2.graph(self.mx2,self.Mx2)
        if self.reverse1:
            c1=c1.reverse()
        if self.reverse2:
            c2=c2.reverse()

        custom=CustomSurface(c1,self.up_segment,c2,self.low_segment)
        a.append(custom.pstricks_code())

        if self.curve1.parameters.style != "none":
            a.append(self.curve1.pstricks_code())
        if self.curve2.parameters.style != "none":
            a.append(self.curve2.pstricks_code())
        if self.low_segment.parameters.style != "none" :
            a.append(self.low_segment.pstricks_code())
        if self.up_segment.parameters.style != "none" :
            a.append(self.up_segment.pstricks_code())
        return "\n".join(a)



class SurfaceUnderFunction(SurfaceBetweenFunctions):
    """
    Represent a surface under a function.

    This is a particular case of SurfaceBetweenFunctions when the second function is the y=0 axis.

    Arguments :
    f : a function
    mx : initial x value
    Mx : end x value

    The function f becomes self.f1 while self.f2 will be the function 0 (this is a consequence of inheritance).
    The function f will also be recorded as self.f.
    """

    def __init__(self,f,mx,Mx):
        self.f=EnsurephyFunction(f)
        var('x')
        f2=0
        SurfaceBetweenFunctions.__init__(self,self.f,f2,mx,Mx)
    def __str__(self):
        return "SurfaceUnderFunction %s x:%s->%s"%(self.f,str(self.mx),str(self.Mx))

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
        a.append("\pscustom["+self.params()+"]{")
        a.append(inside)
        a.append("}")
        return "\n".join(a)

class GraphOfAPoint(GraphOfAnObject,GeometricPoint):
    def __init__(self,point):
        GraphOfAnObject.__init__(self,point)
        GeometricPoint.__init__(self,point.x,point.y)
        self.psName = point.psName      # The psName of the point is erased when running Point.__init__
        self.point = self.obj
        self.add_option("PointSymbol=*")
        self._advised_mark_angle=None
    def mark_point(self):
        return self
    def bounding_box(self,pspict=None):
        """
        return the bounding box of the point including its mark

        A small box of radius 0.1 (modulo xunit,yunit[1]) is given in any case.
        You need to provide a pspict in order to compute the size since it can vary from the place in your document you place the figure.

        [1] If you dont't know what is the "bounding box", or if you don't want to fine tune it, you don't care.
        """
        Xradius=0.1
        Yradius=0.1
        try :
            Xradius=0.1/pspict.xunit
            Yradius=0.1/pspict.yunit
        except :
            print "You should consider to give a pspict as argument. Otherwise the boundig box of %s could be bad"%str(self)
            raise TypeError
        bb = BoundingBox(Point(self.x-Xradius,self.y-Yradius),Point(self.x+Xradius,self.y+Yradius))
        for P in self.record_add_to_bb:
            bb.AddPoint(P)
        return bb
    def math_bounding_box(self,pspict=None):
        """Return a bounding box which include itself and that's it."""
        return BoundingBox(self.point,self.point)
    def pstricks_code(self,pspict=None,with_mark=False):
        r"""
        Return the pstricks code of the point

        INPUT:
        - ``with_mark`` - (default : False) if it is true, return the pstrick code
                                of the mark in the same time. This is only used by the axes.
        OUTPUT:
        string

        This function is not supposed to be used by the end-user.

        When the point has a mark, the code of the mark is not included here because the
        function pspicture.DrawGraph automatically adds the mark to the list of objects
        to be drawn.
        However, some constructions want to include the pstricks code of points in its own
        pstricks code. In that case we want the code of the mark to be part of the code
        of the point.
        This is the case of the axes. The pstricks code of the axes have to be in one block
        including the markes. For that usage, we use with_mark=True
        
        EXAMPLE:
        sage: P=Point(1,1)
        sage: P.put_mark(0.3,45,"$P$")

        By default the code of the mark does not appears in the code of the point:
        sage: unify_point_name(P.pstricks_code())
        '\\pstGeonode[PointSymbol=*,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaaa}'

        If we specify with_mark=True, then we see the code of the mark:
        sage: unify_point_name(P.pstricks_code(with_mark=True))
        '\\pstGeonode[](1.21213203435596,1.21213203435596){Xaaaa}\n\\rput(Xaaaa){\\rput(0;0){$P$}}\n\\pstGeonode[PointSymbol=*,linestyle=solid,linecolor=black](1.00000000000000,1.00000000000000){Xaaab}'
        """
        l=[]
        if self.marque and with_mark:
            l.append(self.mark.pstricks_code(pspict))
        l.append("\pstGeonode["+self.params()+"]"+self.coordinates(numerical=True)+"{"+self.psName+"}")
        return "\n".join(l)

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

class GeometricImplicitCurve(object):
    """
    Describe a curve given by an implicit equation.

    INPUT:

    - ``f`` -- a function of two variables or equation in two variables

    End users should not use this class but use the constrcutor :func:`ImplicitCurve`.

    EXAMPLES::

        sage: f(x,y)=x**2+1/x
        sage: F=GeometricImplicitCurve(f(x,y)==2)
        sage: G=GeometricImplicitCurve(x+y==2)   

    """
    def __init__(self,f):
        self.f=f
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
    
            sage: x,y=var('x,y')
            sage: F=GeometricImplicitCurve(x-y==3)
            sage: graph=F.graph((x,-3,3),(y,-2,2))
            sage: print graph.bounding_box()
            (1.0,-2.0),(3.0,1.88737914186e-15)

        """
        return GraphOfAnImplicitCurve(self,xrange,yrange,plot_points)
    def __str__(self):
        """
        Return string representation of this implicit curve

        EXAMPLE::

            sage: f(x,y)=x**2+1/x
            sage: print GeometricImplicitCurve(f(x,y)==2)
            Implicit curve of equation x^2 + 1/x - 2 == 0
            sage: print GeometricImplicitCurve(x+y==7)   
            Implicit curve of equation x + y - 7 == 0
        """
        return "Implicit curve of equation %s == 0"%repr(self.f)

class GraphOfAnImplicitCurve(GraphOfAnObject,GeometricImplicitCurve):
    r"""
    Describe the graph of an implicit curve.

    INPUT:
    - ``implicit_curve`` - the implicit curve to be considered
    - ``xrange``,``yrange`` - the range on which we want to plot
    

    OPTIONAL INPUT:
    - ``plot_points``  -- integer (default: 100); number of points to plot
    in each direction of the grid.  

    ATTRIBUTES:
    - ``self.path`` this is a list of lists of points. Each list correspond to a path
                    in the sense of matplotlib. Notice that here the points are given as
                    instances of Point; not as list [x,y] as matplotlib does.
    
    EXAMPLES:
    sage: var('x,y')
    (x, y)
    sage: implicit_curve=GeometricImplicitCurve(x**2+x==3)
    sage: F=GraphOfAnImplicitCurve(implicit_curve,(x,-1,1),(y,-3,2)).pstricks_code()

    NOTES:
    the get_minmax_data is contributed by the Sage's community here :
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
    def get_minmax_data(self,dict=True):
        """
        Return a dictionary whose keys give the xmin, xmax, ymin, and ymax
        data for this graphic.

        Since the results come from the lazy_attribute function _get_minmax_data, changing the number of points
        between two call will not change the result.

        EXAMPLES
        sage: var('x,y')
        (x, y)
        sage: F=ImplicitCurve(x**2+y**2==sqrt(2),(x,-5,5),(y,-4,4),plot_points=300)
        sage: F.get_minmax_data()
        {'xmin': -1.18858977066, 'ymin': -1.18845247289, 'ymax': 1.18845247289, 'xmax': 1.18858977066}
        sage: F.plot_points=10
        sage: F.get_minmax_data()
        {'xmin': -1.18858977066, 'ymin': -1.18845247289, 'ymax': 1.18845247289, 'xmax': 1.18858977066}
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
        Return the bounding box of the implicit curve.

        This is NOT the bounding box got that one could expect
        using Sage's plotting system
        implicit_plot(f,xrange,yrange).get_minmax_data()

        Instead the bounding box returned here only contains the points that
        are actually plotted. In the following example, we know that the ymax
        has to be half the sqrt of the radius (and not the 5 given in yrange).

        EXAMPLES:    
        sage: var('x,y')
        (x, y)
        sage: f=x**2+2*y**2
        sage: G=ImplicitCurve(f==sqrt(2),(x,-5,5),(y,-5,5),plot_points=200)
        sage: print G.bounding_box()
        (-1.18795591533,-0.840500197448),(1.18795591533,0.840500197448)
        """
        bb = BoundingBox( Point(self.xmin(),self.ymin()),Point(self.xmax(),self.ymax())  )
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        r"""
        Return the pstrick code of the implicit curve.
        """
        code=[]
        for path in self.paths:
            curve=InterpolationCurve(path,context_object=self)
            code.append(curve.pstricks_code(pspict))
        return "\n".join(code)

class GraphOfASegment(GraphOfAnObject,GeometricSegment):
    def __init__(self,seg):
        GraphOfAnObject.__init__(self,seg)
        GeometricSegment.__init__(self,seg.I,seg.F)
        self.seg = self.obj
        self.I = self.seg.I
        self.F = self.seg.F
    def mark_point(self):
        """
        return the point on which a mark has to be placed if we use the method put_mark.

        If we have a segment, the mark is at center while if it is a vector the mark
        has to be placed on the extremity.
        EXAMPLES:
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
            P=self.F.copy()
        else :
            P=self.center().copy()
        return P
    def bounding_box(self,pspict=None):
        return BoundingBox(self.I,self.F)       # If you change this, maybe you have to adapt math_bounding_box
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        """
        Return the pstricks's code of a Segment when is is seen as a segment
        """
        if self.arrow_type=="vector":
            return _vector_pstricks_code(self,pspict)
        if self.arrow_type=="segment":
            if self.wavy:
                waviness = self.waviness
                curve=InterpolationCurve(self.get_wavy_points(waviness.dx,waviness.dy),context_object=self)
                return curve.pstricks_code()
            else:
                a =  self.I.create_PSpoint() + self.F.create_PSpoint()
                a=a+"\n\pstLineAB[%s]{%s}{%s}"%(self.params(),self.I.psName,self.F.psName)
                return a

class GeometricVectorField(object):
    """
    Describe a vector field

    INPUT:
    
    - ``f`` - a tupe of function

    EXAMPLES::

        sage: x,y=var('x,y')
        sage: f1=phyFunction(x**2)
        sage: F = GeometricVectorField( f1,cos(x*y) )
        sage: print F(3,pi/3)
        vector I=Point(3,1/3*pi) F=Point(12,1/3*pi - 1)

    """
    def __init__(self,fx,fy):
        g=[fx,fy]
        for i in [0,1]:
            if isinstance(g[i],phyFunction):
                g[i]=g[i].sage
        self.fx=g[0]
        self.fy=g[1]
        self.vector_field=self
    def divergence(self):
        """
        return the divergence of the vector field.

        OUTPUT:

        a two-variable function

        EXAMPLES::

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

            sage: x,y=var('x,y')
            sage: F=VectorField(x,y).graph(xvalues=(x,-2,2,3),yvalues=(y,-10,10,3),draw_points=[Point(100,100)])
            sage: print F.draw_points[0]
            Point(100,100)
            sage: print len(F.draw_points)
            10
        """
        if draw_points is None:
            draw_points=[]
        if xvalues is not None:
            import numpy
            mx=xvalues[1]
            Mx=xvalues[2]
            nx=xvalues[3]
            my=yvalues[1]
            My=yvalues[2]
            ny=yvalues[3]
            pos_x=numpy.linspace(mx,Mx,nx)
            pos_y=numpy.linspace(my,My,ny)
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

            sage: x,y=var('x,y')
            sage: F=VectorField(x**2,y**3)
            sage: print F(1,2)
            vector I=Point(1,2) F=Point(2,10)

            sage: P=Point(3,4)
            sage: print F(P)
            vector I=Point(3,4) F=Point(12,68)

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
        If self was created using the optional argument draw_points,
        then the set of points on which there is a vector
        is not equal to the product
        self.pos_x times self.pos_y
        
        EXAMPLES:
        The two lists created in the following example are the same :
        sage: x,y=var('x,y')
        sage: F=VectorField(x,y).graph(xvalues=(x,1,2,3),yvalues=(y,-2,2,3))
        sage: [ P.coordinates() for P in F.draw_points ]
        ['(1.0,-2.0)', '(1.0,0)', '(1.0,2.0)', '(1.5,-2.0)', '(1.5,0)', '(1.5,2.0)', '(2.0,-2.0)', '(2.0,0)', '(2.0,2.0)']
        sage: [ (x,y) for x in F.pos_x for y in F.pos_y ]
        [(1.0, -2.0), (1.0, 0.0), (1.0, 2.0), (1.5, -2.0), (1.5, 0.0), (1.5, 2.0), (2.0, -2.0), (2.0, 0.0), (2.0, 2.0)]


        But in the following, the list is not the list of points :
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
    def pstricks_code(self,pspict=None):
        code=[]
        for v in self.draw_vectors:
            v.parameters=self.parameters
            code.append(v.pstricks_code(pspict))
        return "\n".join(code)

class MeasureLength(GraphOfASegment):
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

class GraphOfARectangle(GraphOfAnObject,GeometricRectangle):
    """
    The parameters of the four lines are by default the same, but they can be adapted separately.

    graph_N returns the north side as a phystricks.Segment object
    The parameters of the four sides have to be set independently.

    The drawing is done by \psframe, so that, in principle, all the options are available.
    """
    def __init__(self,rect):
        GraphOfAnObject.__init__(self,rect)
        GeometricRectangle.__init__(self,rect.NW,rect.SE)
        self.rectangle = self.obj
    def _segment(self,side):
        bare_name = "graph_"+side
        if not bare_name in self.__dict__.keys():
            line = self.__getattribute__("segment_"+side)()
            #line.parameters=self.parameters
            self.__dict__[bare_name]=line
        return  self.__dict__[bare_name]
    def __getattr__(self,attrname):
        if "graph_" in attrname:
            return self._segment(attrname[6])
    def bounding_box(self,pspicture=1):
        return BoundingBox(self.NW,self.SE)
    def math_bounding_box(self,pspicture=1):
        return self.bounding_box(pspicture)
    def pstricks_code(self,pspict=None):
        return "\psframe["+self.params()+"]"+self.rectangle.SW.coordinates(numerical=True)+self.rectangle.NE.coordinates(numerical=True)


class GeometricAngle(object):
    def __init__(self,A,O,B,r=None):
        self.A=A
        self.O=O
        self.B=B
        if r==None:
            r=0.2*Segment(A,O).length()
        self.r=r
        self.angleA=AffineVector(O,A).angle()
        self.angleB=AffineVector(O,B).angle()
        self.angleI=min(self.angleA,self.angleB)
        self.angleF=max(self.angleA,self.angleB)
        self.media=self.angleF-0.5*self.measure()
    def circle(self):
        return Circle(self.O,self.r).graph(self.angleI,self.angleF)
    def measure(self):
        return AngleMeasure(value_degree=self.angleF.degree-self.angleI.degree)
    def graph(self):
        return GraphOfAnAngle(self)

class GraphOfAnAngle(GraphOfAnObject,GeometricAngle):
    """
    self.mark_angle is the angle at which self.mark_point will be placed. By default it is at the middle. 
        If you want to change it, use
        self.set_mark_angle(x).
        It will set the mark_angle to x AND the advised_mark angle too.
    """
    def __init__(self,angle):
        GraphOfAnObject.__init__(self,angle)
        GeometricAngle.__init__(self,angle.A,angle.O,angle.B,angle.r)
        self.advised_mark_angle=self.media.degree
        self.mark_angle=self.media
    def set_mark_angle(self,theta):
        """
        theta is degree or AngleMeasure
        """
        self.mark_angle=AngleMeasure(theta)
        self.advised_mark_angle=degree(theta,number=True,converting=False)
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        return self.circle().bounding_box(pspict)
    def mark_point(self):
        return self.circle().get_point(self.mark_angle)
    def pstricks_code(self,pspict=None):
        circle=self.circle()
        circle.parameters=self.parameters
        l=[]
        #if self.marque:
        #    l.append(self.mark.pstricks_code(pspict))
        l.append(circle.pstricks_code(pspict))
        return "\n".join(l)

class phyFunction(object):
    """
    Represent a function.
    """
    def __init__(self,fun):
        if isinstance(fun,phyFunction) :        # It allows fun to be a graph of a function.
            phyFunction.__init__(self,fun.sage)
        else :
            var('x,y')
            try:
                # The technique to assure to have a function is taken from the
                # answer by kcrisman in
                # http://ask.sagemath.org/question/368/python-equivalent-of-txyxyxy
                # Be careful : this induce the bug
                # http://trac.sagemath.org/sage_trac/ticket/10246
                # See the implementation of get_minmax_data
                self.sage=symbolic_expression(fun).function(x)
                try :
                    self.sageFast = self.sage._fast_float_(x)

                except (NotImplementedError,TypeError,ValueError) :    
                    # Happens when the derivative of the function is not implemented in Sage
                    # Also happens when there is a free variable,
                    # as an example
                    # F=GraphOfAVectorField(x,y)
                    self.sageFast = self.sage(x)

            except AttributeError,text:          # Happens when the function is given by a number like f=0  F=phyFunction(f)
                raise AttributeError,text        # It is no more supposed to do that since I use self.sage=symbolic_expression(fun).function(x)
                self.sage = SR(fun)
                self.sageFast = self.sage._fast_float_(x)
            self.string = repr(self.sage)
            self.fx = self.string.replace("^","**").replace("x |--> ","")
            self.pstricks = SubstitutionMathPsTricks(self.fx)
            self.ListeSurface = []
            self.listeTests = []
            self.TesteDX = 0
            self.listeExtrema = []
            self.listeExtrema_analytique = []
            self._derivative = None
            self.equation=y==self.sage
    def eval(self,xe):
        raise AttributeError,"Use the syntax f(x) instead of f.eval(x)"
        return numerical_approx(self.sageFast(xe))
    def inverse(self,y):
        """ returns a list of values x such that f(x)=y """
        listeInverse = []
        var('x')
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

            sage: f=phyFunction(x**2)
            sage: print f.derivative()
            x |--> 2*x
            sage: print f.derivative()(3)
            6
            sage: g(x)=cos(x)
            sage: print [g.derivative(i) for i in range(0,5)]
            [x |--> cos(x), x |--> -sin(x), x |--> -cos(x), x |--> sin(x), x |--> cos(x)]
        """
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
    #def diff(self,v):
    #    """
    #    make the same as Sage's diff.
    #
    #    The aim is to be able to differentiate with respect to x and y a function of two variables.

    #    EXAMPLES:
    #    sage: x,y=var('x,y')
    #    sage: f=phyFunction(x*y)
    #    sage: print f.diff(x)
    #    y
    #    sage: print f.diff(y)
    #    x
    #    """
    #    return phyFunction(self.sage.diff(v))
    def get_point(self,x,advised=True):        
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
        P = Point(float(x),self(x))
        if advised :
            try :
                ca = self.derivative()(x) 
                angle_n=degree(atan(ca)+pi/2)
                if self.derivative(2)(x) > 0:
                    angle_n=angle_n+180
                P.advised_mark_angle=angle_n
            except TypeError :      # Happens when Sage has no derivative of the function.
                pass
        return P
    def get_normal_vector(self,xx):
        """ 
        return a normalized normal vector to the graph of the function at xx

        The direction of the vector is outside

        INPUT:
        - ``x`` - a number, the position at which we want the normal vector

        OUTPUT:
        a vector

        EXAMPLES:
        sage: var('x')
        x
        sage: f=phyFunction(x**2)
        sage: print f.get_normal_vector(0)
        vector I=Point(0,0) F=Point(0,-1)
        """
        #ca = self.derivative()(x) 
        #return Point(-ca,1).normalize().origin(self.get_point(x))       
        F=ParametricCurve(x,self)
        return F.get_normal_vector(xx)
    def get_tangent_vector(self,x,advised=False,numerical=False):
        """
        return a tangent vector at the point (x,f(x))
        """
        ca = self.derivative()(x,numerical=numerical)
        return Point(1,ca).normalize().origin(self.get_point(x,advised))
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

            sage: g=phyFunction(cos(x))
            sage: print g.tangent_phyFunction(pi/2)
            x |--> 1/2*pi - x
            sage: g.tangent_phyFunction(pi/2)(1)
            1/2*pi - 1
        """
        var('x')
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
        
            sage: f=phyFunction(x+1)
            sage: print [P.coordinates() for P in f.get_regular_points(-2,2,sqrt(2))]
            ['(0.70434464532253749*sqrt(2) - 2,0.70434464532253749*sqrt(2) - 1)', '(1.408689290645075*sqrt(2) - 2,1.408689290645075*sqrt(2) - 1)', '(2.1130339359676125*sqrt(2) - 2,2.1130339359676125*sqrt(2) - 1)', '(2.81737858129015*sqrt(2) - 2,2.81737858129015*sqrt(2) - 1)']

        Even if it is not clear from these expressions, these are almos the points (-1,0),(0,1), and (1,2).

        """
        var('x')
        f1 = phyFunction(x)
        try :
            f2 = self.f     # Here, self can be of type «GraphOfAphyFunction»
        except AttributeError :
            f2 = self
        curve = ParametricCurve(f1,f2)
        return curve.get_regular_points(mx,Mx,dx)
    def get_wavy_points(self,mx,Mx,dx,dy):
        PIs = self.get_regular_points(mx,Mx,dx)
        Ps = [self.get_point(mx)]
        for i in range(0,len(PIs)) :
            Ps.append( self.get_normal_point(PIs[i].x, ((-1)**i)*dy ) )
        Ps.append(self.get_point(Mx))   
        return Ps
    def liste_extrema(self):
        if self.listeExtrema == []:
            self.extrema_analytique()
        return self.listeExtrema
    def ToutExtrema(self,mx,Mx,dx):
        min = self.get_point(mx)
        max = self.get_point(mx)
        for ex in list(xsrange(mx,Mx,dx,include_endpoint=true)):
            ey = self(ex)
            if ey > max.y : max = Point(ex,ey)
            if ey < min.y : min = Point(ex,ey)
        self.listeExtrema.extend([min,max])
    # La méthode phyFunction.extrema_analytique() ajoute les solutions de f'(x)=0 à self.listeExtrema
    def extrema_analytique(self):
        print "Analytique"
        var('x')
        a = []
        listeSymbolicEquation = solve( [self.sage.diff(x)==0],[x] )
        for sol in listeSymbolicEquation :
            #s = sol[2]
            s = sol.right_hand_side()
            if "x" not in repr(s) :             # En attendant de trouver comment demander des solutions non implicites
                a.append(self.get_point(numerical_approx(s)))
        self.listeExtrema.extend(a)
    # Donne les extrema connus entre mx et Mx
    def extrema(self,mx,Mx):
        a = []
        for p in self.liste_extrema() :
            if p.x >= mx and p.x <= Mx :
                a.append(p)
        return a
    def get_minmax_data(self,mx,Mx):
        """
        return numerical approximations of min and max of the function on the interval

        INPUT:
        - ``mx,Mx`` - the interval on which we look at the extrema

        OUTPUT:

        dictionary conaining `xmax`, `ymax`, `xmin` and `ymin`

        Notice that we are only interested in ymax and ymin.

        EXAMPLES::
        
            sage: f=phyFunction(x)
            sage: f.get_minmax_data(-3,pi)
            {'xmin': -3.0, 'ymin': -3.0, 'ymax': 3.1415926535897931, 'xmax': 3.1415926535897931}

        In the case of the sine function, the min and max are almost -1 and 1::

            sage: f=phyFunction(sin(x))
            sage: f.get_minmax_data(0,2*pi)
            {'xmin': 0.0, 'ymin': -0.99996566005741139, 'ymax': 0.99999992589514664, 'xmax': 6.2831853071795862}

        NOTE:

        This function is victim of the `Trac 10246 <http://trac.sagemath.org/sage_trac/ticket/10246>` The try ... except
        block is a workaround.

        """
        try :
            return MyMinMax(plot(self.sage,(mx,Mx)).get_minmax_data())
        except ValueError :
            if self.sage==x:
                return MyMinMax(plot(x,mx,Mx).get_minmax_data())
            else :
                raise ValueError,"This is a strange case. Maybe to be reported to ticker 10246"
    def xmax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmax']
    def xmin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['xmin']
    def ymax(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymax']
    def ymin(self,deb,fin):
        return self.get_minmax_data(deb,fin)['ymin']
    def maximum_global(self,mx,Mx):
        max = self.liste_extrema()[0]
        for p in self.liste_extrema() :
            if p.y > max.y : max = p
        return max
    # Donne le minimum de la fonction entre mx et Mx. 
    def minimum_global(self,mx,Mx):
        min = self.get_point(mx)
        for p in self.liste_extrema() :
            print "candidat : %s" %p.Affiche()
            if p.y < min.y : min = p
        print min.Affiche()
        return min
    def tangente(self,x):
        """
        This should no more be used.
        """
        raise
        ca = self.derivative()(x)
        A = self.get_point(x)
        Ad = Point( A.x+1,A.y+ca )
        Ag = Point( A.x-1,A.y-ca )
        return ( Segment(Ag,Ad) )
    def graph(self,mx,Mx):
        return GraphOfAphyFunction(self,mx,Mx)
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
    def __call__(self,xe,numerical=False):
        """
        return the value of the function at given point

        INPUT:
        - ``xe`` - a number. The point at which we want to evaluate the function
        - ``numerical`` (boolean, default=False) If True, return a numerical_approximation

        EXAMPLES:
        sage: var('x')
        x
        sage: f=phyFunction(cos(x))
        sage: f(1)
        cos(1)
        sage: f(1,numerical=True)
        0.540302305868140
        """
        if numerical :
            return numerical_approx(self.sageFast(xe))
        else :
            return self.sage(x=xe)
    def __pow__(self,n):
        return phyFunction(self.sage**n)
    def __mul__(self,other):
        try :
            f=phyFunction(self.sage*other)
        except TypeError :
            f=phyFunction(self.sage * other.sage)
        return f
    def __add__(self,other):
        return phyFunction(self.sage+other.sage)
    def __str__(self):
        return str(self.sage)

class GraphOfAphyFunction(GraphOfAnObject,phyFunction):
    def __init__(self,f,mx,Mx):
        GraphOfAnObject.__init__(self,f)
        phyFunction.__init__(self,f.sage)
        self.f = self.obj
        self.mx = mx
        self.Mx = Mx
        self.plotpoints = 100                   # We draw 100 points as default.
        self.parameters.color = "blue"              # Modification with respect to the attribute in GraphOfAnObject
    def params(self):
        self.conclude_params()
        self.add_option("plotpoints=%s"%str(self.plotpoints))
        return self.options.code()
    def bounding_box(self,pspict=None):
        bb = BoundingBox()
        bb.AddY(self.f.ymin(self.mx,self.Mx))
        bb.AddY(self.f.ymax(self.mx,self.Mx))
        bb.AddX(self.mx)
        bb.AddX(self.Mx)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        """
        return the pstricks code of the function

        EXAMPLES::

            sage: f=phyFunction(x*sin(1/x)).graph(-5,5)
            sage: f.pstricks_code()      
            '\\psplot[linestyle=solid,plotpoints=100,linecolor=blue]{-5.00000000000000}{5.00000000000000}{x*sin(1/x)}'
        """
        a = []
        if self.marque :
            P = self.get_point(self.Mx)
            P.parameters.symbol="none"
            P.marque = True
            P.mark = self.mark
            a.append(P.pstricks_code())
        if self.wavy :          
            waviness = self.waviness
            #self.TracephyFunctionOndule(self.f,waviness.mx,waviness.Mx,waviness.dx,waviness.dy,self.params())
            curve=InterpolationCurve( self.get_wavy_points(waviness.mx,waviness.Mx,waviness.dx,waviness.dy),context_object=self)
            a.append(curve.pstricks_code())
        else :
            # The use of numerical_approx is intended to avoid strings like "2*pi" in the final pstricks code.
            deb = numerical_approx(self.mx) 
            fin = numerical_approx(self.Mx)
            a.append("\psplot["+self.params()+"]{"+str(deb)+"}{"+str(fin)+"}{"+self.f.pstricks+"}")
        #return a               # I do not remember why it was like that. See also the change in SurfaceBetweenFunctions.pstricks_code (13005)
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
    
    We create a cardioid::

        sage: f=1.5*(1+cos(x))
        sage: cardioid=PolarCurve(f).graph(0,2*pi)

    """
    x=var('x')
    if ftheta==None :
        f1=fr*cos(x)
        f2=fr*sin(x)
    else:
        f1=fr(x=x)*cos(ftheta(x=x))
        f2=fr(x=x)*sin(ftheta(x=x))
    return ParametricCurve(f1,f2)

def get_paths_from_plot(p):
    """
    return the paths (in the sense of matplotlib) contained in the plot object p.

    The paths here are paths in the sense of matplotlib; the elements are vertices.
    Not to be confused with get_paths_from_implicit_plot in which the basic elements
    are points.

    INPUT:
    - ``p`` - a plot object

    EXAMPLES:
    sage: var('x,y')
    (x, y)
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
        <class 'BasicGeometricObjects.GraphOfAPoint'>
        sage: print paths[1][3]
        Point(4.87405534614,-4.6644295302)
    """
    l=[]
    for path in get_paths_from_plot(p):
        pp=[]
        for vertice in path.vertices:
            pp.append(Point(vertice[0],vertice[1]))
        l.append(pp)
    return l


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
        if type(f1) is phyFunction : 
            self.f1 = f1
        else : 
            self.f1 = phyFunction(f1)
        if type(f2) is phyFunction :
            self.f2 = f2
        else : 
            self.f2 = phyFunction(f2)
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

class GraphOfAParametricCurve(GraphOfAnObject,ParametricCurve):
    def __init__(self,curve,llamI,llamF):
        GraphOfAnObject.__init__(self,curve)
        ParametricCurve.__init__(self,curve.f1,curve.f2)
        self.curve = self.obj           # It is strange that this line does not raise a crash.
        self.llamI = llamI
        self.llamF = llamF
        self.parameters.color = "blue"
        self.plotstyle = "curve"
        self.plotpoints = "1000"
    def params(self):
        self.conclude_params()
        self.add_option("plotpoints=%s"%str(self.plotpoints))
        self.add_option("plotstyle=%s"%str(self.plotstyle))
        return self.options.code()
    def reverse(self):
        """
        return the curve in the inverse sense but on the same interval

        EXAMPLE:
        sage: x=var('x')
        sage: curve=ParametricCurve(cos(x),sin(x)).graph(0,2*pi).reverse()
        sage: print curve
        The parametric curve given by
        x(t)=cos(2*pi - t)
        y(t)=sin(2*pi - t)
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
    def pstricks_code(self,pspict=None):
        if self.wavy :
            waviness = self.waviness
            curve=InterpolationCurve(self.curve.get_wavy_points(self.llamI,self.llamF,waviness.dx,waviness.dy),context_object=self)
            return curve.pstricks_code()
        else:
            initial = numerical_approx(self.llamI)      # Avoid the string "pi" in the pstricks code.
            final = numerical_approx(self.llamF)
            return "\parametricplot[%s]{%s}{%s}{%s}" %(self.params(),str(initial),str(final),self.curve.pstricks())



#class Nuage_de_Points(object):
#   def __init__(self):
#       self.listePoints = []
#   def ajoute_point(self,p):
#       self.listePoints.append(p)

def PolarSegment(P,r,theta):
    """
    returns a segment on the base point P (class Point) of length r angle theta (degree)
    """
    alpha = radian(theta)
    return Segment(P, Point(P.x+r*math.cos(alpha),P.y+r*math.sin(alpha)) )

class BoundingBox(object):
    def __init__(self,dSW=GeometricPoint(0,0),dNE=GeometricPoint(0,0)):
        self.mx=dSW.x
        self.Mx=dNE.x
        self.my=dSW.y
        self.My=dNE.y
    def N(self):
        return Segment(self.NW(),self.NE()).center()
    def S(self):
        return Segment(self.SW(),self.SE()).center()
    def NE(self):
        return Point(self.Mx,self.My)
    def NW(self):
        return Point(self.mx,self.My)
    def SE(self):
        return Point(self.Mx,self.My)
    def SW(self):
        return Point(self.mx,self.my)
    def north_segment(self):
        return Segment( self.NW(),self.NE() )
    def south_segment(self):
        return Segment( self.SW(),self.SE() )
    def east_segment(self):
        return Segment( self.NE(),self.SE() )
    def west_segment(self):
        return Segment( self.NW(),self.SW() )
    def coordinates(self):
        return self.SW().coordinates()+self.NE().coordinates()
    def Affiche(self):
        raise DeprecationWarning
        return self.coordinates()
    def tailleX(self):
        return self.Mx-self.mx
    def tailleY(self):
        return self.My-self.my
    def extraX_left(self,l):
        """Enlarge the bounding box of a length l on the left"""
        self.mx=self.mx-l
    def extraX_right(self,l):
        """Enlarge the bounding box of a length l on the right"""
        self.Mx=self.Mx+l
    def extraX(self,l):
        """Enlarge the bounding box of a length l on both sides"""
        self.extraX_left(l)
        self.extraX_right(l)
    def AddX(self,x):
        self.Mx=max(self.Mx,x)
        self.mx=min(self.mx,x)
    def AddY(self,y):
        self.My=max(self.My,y)
        self.my=min(self.my,y)
    def AddPoint(self,P):
        self.AddX(P.x)
        self.AddY(P.y)
    def AddSegment(self,seg):
        self.AddPoint(seg.I)
        self.AddPoint(seg.F)
    def AddArcCircle(self,Cer,deb,fin):
        self.AddX(Cer.xmin(deb,fin))
        self.AddY(Cer.ymin(deb,fin))
        self.AddX(Cer.xmax(deb,fin))
        self.AddY(Cer.ymax(deb,fin))
    def AddBB(self,bb):
        self.AddX(bb.mx)
        self.AddX(bb.Mx)
        self.AddY(bb.my)
        self.AddY(bb.My)
    def add_graph(self,graphe,pspict=None):
        raise DeprecationWarning,"Use self.append instead"
        self.AddBB(graphe.bounding_box(pspict))
    def append(self,graphe,pspict=None):        # It seems to me that the method name "append" is more intuitive that "add_graph"
        try :
            self.AddBB(graphe.bounding_box(pspict))
        except (ValueError,AttributeError),msg :
            print "Something got wrong with %s"%graphe
            print msg
    def add_math_graph(self,graphe,pspict=None):
        try :
            self.addBB(graphe.math_bounding_box(pspict))
        except AttributeError :
            print "%s seems not to have a method math_bounding_box. I add its bounding_box instead"%str(graphe)
            self.addBB(graphe.bounding_box(pspict))
    def AddCircleBB(self,Cer,xunit,yunit):
        """
        Add a deformed circle to the bounding box.

        INPUT:

        - ``Cer`` - a circle. 
        - ``xunit,yunit`` - the `x` and `y` deformation coefficients.

        The given circle will be deformed by the coefficient xunit and yunid and the be added to `self`.
        """
        self.AddPoint( Point( Cer.center.x-Cer.radius/xunit,Cer.center.y-Cer.radius/yunit ) )
        self.AddPoint( Point( Cer.center.x+Cer.radius/xunit,Cer.center.y+Cer.radius/yunit ) )
    def AddAxes(self,axes):
        self.AddPoint( axes.BB.SW() )
        self.AddPoint( axes.BB.NE() )
    def enlarge_a_little(self,Dx,Dy,epsilonX,epsilonY):
        """
        Essentially intended to the bounding box of a axis coordinate. 
        The aim is to make the axis slightly larger than the picture in such a way that all the numbers are written
        1. If a coordinate is integer multiple of epsilon, (say n), we enlarge to n+epsilon, so that the number n appears on the axis
        2. If a coordinate is non integer multiple, we enlarge to the next integer multiple (plus epsilon) so that the axis still has a number written
            further than the limit of the picture.
        The aim is to make the axes slightly bigger than their (Dx,Dy) in order the last graduation to be visible.
        """
        self.mx = enlarge_a_little_low(self.mx,Dx,epsilonX)
        self.my = enlarge_a_little_low(self.my,Dy,epsilonY)
        self.Mx = enlarge_a_little_up(self.Mx,Dx,epsilonX)
        self.My = enlarge_a_little_up(self.My,Dy,epsilonY)
    def pstricks_code(self,pspict=None):
        rect=Rectangle(self.SW(),self.NE())
        rect.parameters.color="cyan"
        return rect.pstricks_code(pspict)
    def bounding_box(self,pspict=None):
        return self
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def copy(self):
        return BoundingBox(self.SW(),self.NE())
    def __str__(self):
        return "(%s,%s),(%s,%s)"%tuple(str(x) for x in(self.mx,self.my,self.Mx,self.My))
