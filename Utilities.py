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

from sage.all import *
from Constructors import *
from phystricks.MathStructures import *

def is_real(z):
    if type(z) in [int,sage.rings.real_mpfr.RealNumber]:
        return True
    return z.is_real()

def test_imaginary_part(z,epsilon=0.0001):
    """
    Return a tuple '(isreal,w)' where 'isreal' is a boolean saying if 'z' is real (in the sense that it is real and does not contain 'I' in its string representation) and 'w' is 'z' when the imaginary part is larger than epsilon and an 'numerical_approx' of 'z' when its imaginary part is smaller than 'epsilon'

    With the collateral effect that it returns a numerical approximation.
    """
    if is_real(z) and "I" not in str(z):
        return True,z
    k=numerical_approx(z)
    if is_real(k):
        return True,k
    if abs( k.imag_part() )<epsilon:
        #print("I am removing a (probably fake) imaginary part")
        return True,numerical_approx( z.real_part() )
    print("It seems that an imaginary part is not so small.")
    return False,z

def test_imaginary_part_point(P,epsilon=0.0001):
    """
    return the tuple '(isreal,P)' whit the same description of 'test_imaginary_part'
    """
    realx,x=test_imaginary_part(P.x)
    realy,y=test_imaginary_part(P.y)
    on=False
    if realx and realy:
        on=True
    return on,Point(x,y)

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

def Intersection(f,g,a=None,b=None,numerical=False,only_real=True):
    """
    When f and g are objects with an attribute equation, return the list of points of intersections.

    The list of point is sorted by order of `x` coordinates.

    If 'only_real' is True, return only the real solutions.

    Only numerical approximations are returned as there are some errors otherwise. As an example the following 
    solving return points that are not even near from the circle x**2+y**2=9
    solve(    [   -1/3*sqrt(3)*y + 1/3*sqrt(3)*(-0.19245008972987399*sqrt(3) - 3) + x == 0,x^2 + y^2 - 9 == 0    ],[x,y]   )
    Position : 313628350

    EXAMPLES::

        sage: from phystricks import *
        sage: fun=phyFunction(x**2-5*x+6)
        sage: droite=phyFunction(2)
        sage: pts = Intersection(fun,droite)
        sage: for P in pts:print P
        <Point(1,2)>
        <Point(4,2)>

        sage: f=phyFunction(sin(x))
        sage: g=phyFunction(cos(x))
        sage: pts=Intersection(f,g,-2*pi,2*pi,numerical=True)
        sage: for P in pts:print P
        <Point(-5.497787143782138,0.707106781186548)>
        <Point(-2.3561944901923466,-0.707106781186546)>
        <Point(0.7853981633974484,0.707106781186548)>
        <Point(3.926990816987241,-0.707106781186547)>

    If 'numerical' is True, it search for the intersection points of the functions 'f' and 'g' (it only work with functions). In this case an interval is required.
    """

    if numerical and "sage" in dir(f) :
        k=f-g
        xx=SmallComputations.find_roots_recursive(k.sage,a,b)
        pts=[  Point(x,f(x)) for x in xx ]
        for P in pts:
            if "I" in P.coordinates():
                print("There should not be imaginary part")
                raise
        return pts

    x,y=var('x,y')
    pts=[]
    if numerical :
        soluce=solve([f.equation(numerical=True),g.equation(numerical=True)],[x,y])
    else :
        soluce=solve([f.equation(),g.equation()],[x,y])
    for s in soluce:
        a=s[0].rhs()
        b=s[1].rhs()
        z=a**2+b**2
        ok1,a=test_imaginary_part(a)
        ok2,b=test_imaginary_part(b)
        if ok1 and ok2 :
            pts.append(Point(a,b))
    pts.sort(lambda P,Q:cmp(P.x,Q.x))
    for P in pts:
        if "I" in P.coordinates():
            print("There should not be imaginary part")
            print(f.equation,g.equation)
            raise
    return pts

def PointToPolaire(P=None,x=None,y=None,origin=None):
    """
    Return the polar coordinates of a point.

    INPUT:
    - ``P`` - (default=None) a point
    - ``x,y`` - (defautl=None) the coordinates of the points

    EXAMPLES:

    You can provide a point::

        sage: from phystricks import Point
        sage: from phystricks.SmallComputations import *
        sage: print PointToPolaire(Point(1,1))
        PolarCoordinates, r=sqrt(2),degree=45,radian=1/4*pi

    or directly the coordinates ::

        sage: print PointToPolaire(x=1,y=1)
        PolarCoordinates, r=sqrt(2),degree=45,radian=1/4*pi
    """
    if origin:
        Ox=origin.x
        Oy=origin.y
    if not origin:
        Ox=0
        Oy=0
    if P:
        Px=P.x
        Py=P.y
    else :
        Px=x
        Py=y
    Qx=Px-Ox
    Qy=Py-Oy
    r=sqrt(  Qx**2+Qy**2 )
    if Qx==0:
        if Qy>0:
            radian=pi/2
        else :
            radian=3*pi/2
    else :
        radian=arctan(Qy/Qx)
    if Qx<0:
        if Qy>0:
            radian=radian+pi
        if Qy<=0:
            radian=pi+radian
    # Only positive values (February 11, 2015)
    if radian < 0 :
        radian=radian+2*pi
    return PolarCoordinates(r,value_radian=radian)

class ConversionAngles(object):
    """
    Simplify and convert angle units.

    This class serves to factorise conversion degree -> radian and radian -> degree
    INPUT:
    - ``conversion_factor`` - the conversion factor from the considered unit to the other (radian->degree or the contrary)
    - ``max_value`` - the maximal value (360 or 2*pi)
    """
    def __init__(self,conversion_factor,max_value,exit_attribute=None,create_function=None):
        self.conversion_factor=conversion_factor
        self.max_value=max_value
        self.exit_attribute=exit_attribute
        self.create_function=create_function
    def simplify(self,angle,keep_max=False,number=False,numerical=False):
        """
        Simplify the angles modulo the maximum. 

        If what is given is a number, return a number. If what is given is a AngleMeasure, return a new AngleMeasure.

        Keep the negative numbers to negative numbers. The return interval is
        [-2 pi,2pi]
        which could be open or closed following the `keep_max` boolean.
    
        INPUT:

        - ``angle`` - an angle that can be an instance of AngleMeasure or a number.
                        if it is a number, the simplify modulo self.max_value
                        if it is a AngleMeasure, then first extract the value of the angle
                            using self.exit_attribute .

        - ``keep_max`` - (defautl=False) If True, does not simplify the angle with max value.
                                            Typically, keeps 2*pi as 2*pi. 
                                            This is used in order to keep track of the difference
                                            between 0 and 2*pi in the context of drawing an full circle.

        - ``number`` - (default=False) If True, return a number even is a AngleMeasure is given.

        - ``numerical`` - (default=False) If True, return numerical_approx of the result

        NOTE:
        `number=True` allows exit like pi/2 while numerical will return 1.57079632679490.


        EXAMPLES::

            sage: from phystricks.SmallComputations import *
            sage: simplify_degree=ConversionAngles(180/pi,360).simplify
            sage: simplify_degree(400)
            40

        If <keep_max> is True, maximal values are kept::

            sage: simplify_degree(500,keep_max=True)
            140
            sage: simplify_degree(360,keep_max=True)
            360

        Negative numbers are kept negative::

            sage: simplify_degree(-10)
            -10
            sage: simplify_degree(-380)
            -20
            sage: simplify_degree(-360)
            0
            sage: simplify_degree(-360,keep_max=True)
            -360

        """
        if numerical:
            number=True
        if isinstance(angle,AngleMeasure) :
            x=angle.__getattribute__(self.exit_attribute)
            gotMeasure=True
        else :
            x=angle
            gotMeasure=False
        if keep_max and (x == self.max_value or x == -self.max_value):
            if gotMeasure and number==False:
                return angle
            else :
                if numerical:
                    return numerical_approx(x)
                else:
                    return x

        while x >= self.max_value :
            x=x-self.max_value
        while x <= -self.max_value :
            x=x+self.max_value

        if gotMeasure and number==False :
            return self.create_function(x)
        else :
            if numerical:
                return numerical_approx(x)
            else:
                return x

    def conversion(self,theta,number=False,keep_max=False,converting=True,numerical=False):
        """
        Makes the conversion and simplify.

        INPUT:

        - ``theta`` - the angle to be converted.
        - ``number`` - (default =False) If true, return a number. Not to be confused with <numerical>.
        - ``keep_max`` - (defaut False) If true, does not convert the max value into the minimal value. 
                                        Typically, leaves 2*pi as 2*pi instead of returning 0.
        - ``converting`` - (defaut = True) If False, make no conversion.
        - ``numerical`` - (default = False) boolean. If True, return a numerical approximation. 
                                            If <numerical>=True, then <number> is automatically
                                            switched to True.

        EXAMPLES:

        For converting 7 radian into degree, make the following::

            sage: from phystricks.SmallComputations import *
            sage: degree=ConversionAngles(180/pi,360).conversion
            sage: degree(7)     
            1260/pi - 360

        Notice that the result is an exact value. If you want a numerical approximation::

            sage: degree(7,numerical=True)
            41.0704565915763
            sage: numerical_approx(degree(7))
            41.0704565915763
            sage: degree(120,converting=False)
            120

        Using `converting=False,number=True` is a way to ensure something to be a number instead of a AngleMeasure. For that, we need to precise
        what unit we want to produce. This is done by `self.exit_attribute`.
        A realistic way to define a function that converts to degree is::

            sage: DegreeConversions=ConversionAngles(SR(180)/pi,360,exit_attribute="degree",create_function=DegreeAngleMeasure)
            sage: degree=DegreeConversions.conversion
            sage: a=45 
            sage: b=AngleMeasure(value_radian=pi/4)
            sage: degree(a,number=True,converting=False)
            45
            sage: degree(b,number=True,converting=False)
            45

        """
        if numerical:
            number=True
        if isinstance(theta,AngleMeasure):
            angle = self.simplify(theta,keep_max=keep_max)
            if number:
                 x = angle.__getattribute__(self.exit_attribute)
                 if numerical:
                     return numerical_approx(x)
                 else:
                     return x
            else :
                return angle
        else :
            if converting :
                return self.simplify(self.conversion_factor*theta,keep_max=keep_max,numerical=numerical)
            else :
                return self.simplify(theta,keep_max=keep_max,numerical=numerical)

DegreeConversions=ConversionAngles(SR(180)/pi,360,exit_attribute="degree",create_function=DegreeAngleMeasure)
RadianConversions=ConversionAngles(pi/180,2*pi,exit_attribute="radian",create_function=RadianAngleMeasure)

class degreeUnit(object):
    def __call__(self,x,number=False,keep_max=None,converting=True,numerical=False):
        if isinstance(x,PolarCoordinates) or isinstance(x,AngleMeasure):
            return x.degree
        return DegreeConversions.conversion(x,number=number,keep_max=keep_max,converting=converting,numerical=numerical)
    def __rmul__(self,x):
        return AngleMeasure(value_degree=x)

class radianUnit(object):
    def __call__(self,x,number=False,keep_max=None,converting=True,numerical=False):
        if isinstance(x,PolarCoordinates) or isinstance(x,AngleMeasure):
            return x.radian
        return RadianConversions.conversion(x,number=number,keep_max=keep_max,converting=converting,numerical=numerical)
    def __rmul__(self,x):
        return AngleMeasure(value_radian=x)

degree=degreeUnit()
radian=radianUnit()

simplify_degree=DegreeConversions.simplify
simplify_radian=RadianConversions.simplify

def visual_length(v,l,xunit=None,yunit=None,pspict=None):
    """
    Return a vector in the direction of v that has *visual* length l taking xunit and yunit into account.

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

def EnsurephyFunction(f):
    try :
        k= phyFunction(f.sage)
    except AttributeError :
        pass
    try :
        k = f.phyFunction()
    except AttributeError :
        pass
    k = phyFunction(f)
    try :
        k.nul_function = f.nul_function
    except AttributeError:
        pass
    return k

def EnsureParametricCurve(curve):
    if "parametric_curve" in dir(curve):
        return curve.parametric_curve()
    else :
        return curve

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
        import Exceptions
        try :
            if mx<pspict.mx_acceptable_BB :
                print("mx=",mx,"when pspict.mx_acceptable_BB=",pspict.mx_acceptable_BB)
                raise Exceptions.PhystricksCheckBBError()
            if my<pspict.my_acceptable_BB :
                print("my=",my,"when pspict.my_acceptable_BB=",pspict.my_acceptable_BB)
                raise Exceptions.PhystricksCheckBBError()
            if Mx>pspict.Mx_acceptable_BB :
                print("Mx=",Mx,"when pspict.Mx_acceptable_BB=",pspict.Mx_acceptable_BB)
                raise Exceptions.PhystricksCheckBBError()
            if My>pspict.My_acceptable_BB:
                print("My=",My,"when pspict.My_acceptable_BB=",pspict.My_acceptable_BB)
                raise Exceptions.PhystricksCheckBBError()
        except Exceptions.PhystricksCheckBBError :
            print "I don't believe that object {1} has a bounding box as large as {0}".format(bb,obj)
            try :
                print "The mother of {0} is {1}".format(obj,obj.mother)
            except AttributeError :
                pass
            print("""The easiest way to debug this is to make the picture compile adding something like 
                        pspict.Mx_acceptable_BB=1000
                        pspict.mx_acceptable_BB=-1000
                        pspict.My_acceptable_BB=1000
                        pspict.my_acceptable_BB=-1000
        and then see de visu what is the faulty object.
                    """)
            raise ValueError

def general_function_get_point(fun,x,advised=True):
        """
        Return a point on the graph of the function with the given x, i.e. it return the point (x,f(x)).

        Also set an attribute advised_mark_angle to the point. This angle is the normal exterior to the graph; visually this is usually the best place to put a mark. Typically you use this as
        P=f.get_point(3)
        P.mark(radius,P.advised_mark_angle,"$P$")

        NOTE:
        If you don't plan to put a mark on the point, you are invited to use advised=False in order to speed up the computations.
        """
        P = Point(float(x),fun(x))
        if advised :
            try :
                ca = fun.derivative()(x) 
            except TypeError:    # Sage cannot derivate the function
                print "I'm not able to compute derivative of {0}. You should pass advised=False".format(fun)
            else :
                angle_n=degree(atan(ca)+pi/2)
                if fun.derivative(2)(x) > 0:
                    angle_n=angle_n+180
                P._advised_mark_angle=angle_n
        return P
