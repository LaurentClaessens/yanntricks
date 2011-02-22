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

# copyright (c) Laurent Claessens, 2010
# email: moky.math@gmai.com

"""
This submodule contains functions that perform small computations for phystricks. 
The return values of the functions here are instances of classical classes, not from phystricks classes.
"""

import math
from sage.all import *


def MultipleLower(x,m):
    """ return the biggest multiple of m which is lower or equal to x"""
    return floor(x/m)*m

def MultipleBigger(x,m):
    """ return the lower multiple of m which is bigger or equal to x"""
    return ceil(x/m)*m

def enlarge_a_little_up(x,m,epsilon):
    """
    see the description of the function enlarge_a_little of the class BoundingBox.
    This function makes the job for one number.
    """
    if int(x/m) == x/m:
        return x+epsilon
    else : 
        return MultipleBigger(x,m)+epsilon
        
def enlarge_a_little_low(x,m,epsilon):
    """
    see the description of the function enlarge_a_little of the class BoundingBox.
    This function makes the job for one number.
    """
    if int(x/m) == x/m:
        return x-epsilon
    else : 
        return MultipleLower(x,m)-epsilon

def DegreeAngleMeasure(x):
    return AngleMeasure(value_degree=x)
def RadianAngleMeasure(x):
    return AngleMeasure(value_radian=x)

class AngleMeasure(object):
    """
    sage: x=AngleMeasure(value_radian=pi/2)
    sage: x()
    90

    Conversions are exact:
    sage: a=AngleMeasure(value_degree=30)
    sage: cos(a.radian)
    1/2*sqrt(3)

    You can create a new angle from an old one:
    sage: a=AngleMeasure(value_degree=180)
    sage: b=AngleMeasure(a)
    sage: b.degree
    180

    """
    # TODO : take into account the following thread:
    # http://ask.sagemath.org/question/332/add-a-personnal-coercion-rule
    def __init__(self,value_degree=None,value_radian=None):
        if isinstance(value_degree,AngleMeasure):
            value_degree=value_degree.degree
        if value_degree == None :
            value_degree=degree(value_radian)
        if value_radian == None :
            value_radian=radian(value_degree)
        self.degree=value_degree
        self.radian=value_radian
        if self.degree==None or self.radian==None:
            raise ValueError,"Something wrong"
    def __mul__(self,coef):
        return AngleMeasure(value_radian=coef*self.radian)
    def __rmul__(self,coef):
        return self*coef
    def __sub__(self,other):
        return AngleMeasure(value_radian=self.radian-other.radian)
    def __add__(self,other):
        """
        return the sum of two angles

        EXAMPLES:
        sage: a=AngleMeasure(value_degree=45)
        sage: b=AngleMeasure(value_radian=pi/3)
        sage: a.degree,a.radian
        (45, 1/4*pi)
        sage: b.degree,b.radian
        (60, 1/3*pi)
        sage: (a+b).degree,(a+b).radian
        (105, 7/12*pi)
        """
        return AngleMeasure(value_radian=self.radian+other.radian)
    def __call__(self):
        return self.degree
    def __div__(self,coef):
        return AngleMeasure(value_radian=self.radian/coef)
    def __cmp__(self,other):
        if isinstance(other,AngleMeasure):
            if self.degree > other.degree :
                return 1
            if self.degree < other.degree :
                return 1
            if self.degree == other.degree :
                return 0
    def __str__(self):
        return "AngleMeasure, degree=%s,radian=%s"%(str(numerical_approx(self.degree)),str(self.radian))

class PolarCoordinates(object):
    def __init__(self,r,value_degree=None,value_radian=None):
        self.r = r
        self.measure=AngleMeasure(value_degree,value_radian)
        self.degree=self.measure.degree
        self.radian=self.measure.radian
    def __str__(self):
        return "PolarCoordinates, r=%s,degree=%s,radian=%s"%(str(self.r),str(self.degree),str(self.radian))

def PointToPolaire(P=None,x=None,y=None):
    """
    Return the polar coordinates of a point.

    If you give a point as argument, numerical approximations are returned (because the coordinated of a point is automatically numerically approximed)
    If you explicitelly provides x and y, exact values are returned.

    sage: from phystricks import *     
    sage: print PointToPolaire(x=1,y=1)
    PolarCoordinates, r=sqrt(2),degree=45,radian=1/4*pi
    sage: print PointToPolaire(Point(1,1))
    PolarCoordinates, r=sqrt(2),degree=45,radian=1/4*pi
    """
    if P:
        x=P.x
        y=P.y
    r = sqrt(x**2+y**2)
    if x == 0:
        if y > 0:
            alpha = pi/2
        if y < 0:
            alpha = 3*pi/2
        if y == 0 :             # Convention : the angle for point (0,0) is 0.
            print "phystricks Warning. You are trying to convert into polar coordinates the point (0,0). I'm returning 0 as angle."
            alpha = 0
    else :
        alpha = atan(y/x)
    if not P :
        alpha=alpha.simplify_trig()
    if (x < 0) and (y == 0) :
        alpha = pi
    if (x < 0) and (y > 0) :
        alpha = alpha + pi
    if (x < 0) and (y < 0 ) :
        alpha = alpha +pi
    return PolarCoordinates(r,value_radian=alpha)

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

        If what is given is a number, return a number. If what is given is a AngleMeasure, return a new AngleMeasure
    
        INPUT:
        - ``angle`` - an angle that can be an instance of AngleMeasure or a number.
                        if it is a number, the simplify modulo self.max_value
                        if it is a AngleMeasure, then first extract the value of the angle
                            using self.exit_attribute
        - ``keep_max`` - (defautl=False) If True, does not simplify the angle with max value.
                                            Typically, keeps 2*pi as 2*pi. 
                                            This is used in order to keep track of the difference
                                            between 0 and 2*pi in the context of drawing an full circle.
        - ``number`` - (default=False) If True, return a number even is a AngleMeasure is given.
        - ``numerical`` - (default=False) If True, return numerical_approx of the result

        NOTE:
        number=True allow exit like pi/2 while numerical will return 1.57079632679490.


        EXAMPLE:
        sage: simplify_degree=ConversionAngles(180/pi,360).simplify
        sage: simplify_degree(400)
        40

        If <keep_max> is True, maximal values are kept:
        sage: simplify_degree(500,keep_max=True)
        140
        sage: simplify_degree(360,keep_max=True)
        360

        """
        if numerical:
            number=True
        if isinstance(angle,AngleMeasure) :
            x=angle.__getattribute__(self.exit_attribute)
            gotMeasure=True
        else :
            x=angle
            gotMeasure=False
        if keep_max and x == self.max_value:
            if gotMeasure and number==False:
                return angle
            else :
                if numerical:
                    return numerical_approx(self.max_value)
                else:
                    return self.max_value
        while x >= self.max_value :
            x=x-self.max_value
        while x < 0 :
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
        - ``theta`` - the angle to be converted
        - ``number`` - (default =False) If true, return a number. Not to be confused with <numerical>
        - ``keep_max`` - (defaut False) If true, does not convert the max value into the minimal value. 
                                        Typically, leaves 2*pi as 2*pi instead of returning 0.
        - ``converting`` - (defaut = True) If False, make no conversion.
        - ``numerical`` - (default = False) boolean. If True, return a numerical approximation. 
                                            If <numerical>=True, then <number> is automatically
                                            switched to True.

        EXAMPLES:

        For converting 7 radian into degree, make the following.
        sage: degree=ConversionAngles(180/pi,360).conversion
        sage: degree(7)     
        1260/pi - 360

        Notice that the result is an exact value. If you want a numerical approximation,

        sage: degree(7,numerical=True)
        41.0704565915763
        sage: numerical_approx(degree(7))
        41.0704565915763
        sage: degree(120,converting=False)
        120

        Using converting=False,number=True is a way to ensure something to be a number instead of a AngleMeasure
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

simplify_degree=DegreeConversions.simplify
simplify_radian=RadianConversions.simplify
degree=DegreeConversions.conversion
radian=RadianConversions.conversion

def Distance_sq(P,Q):
    """ return the squared distance between P and Q """
    return (P.x-Q.x)**2+(P.y-Q.y)**2

def Distance(P,Q):
    """ return the distance between P and Q """
    return sqrt(Distance_sq(P,Q))

# Convention : theta is in degree while alpha is in gradient.
#def radian(theta,number=False,converting=True,keep_max=False):
    #"""
    #Convert from degree to radian. Return a value between 0 and 2pi (not 2pi itself)
    #"""
    #if isinstance(theta,AngleMeasure):
        #return simplify_radian(theta,number=number,keep_max=keep_max)
    #else :
        #if converting :
            #return simplify_radian(theta*math.pi/180,keep_max=keep_max)
        #else :
            #return simplify_radian(theta,keep_max=keep_max)
#def degree(alpha,number=False,converting=True,keep_max=False):
    #"""Convert from radian to degree. Return a value between 0 and 360 (not 360 itself)"""
    #if isinstance(alpha,AngleMeasure):
        #return simplify_degree(alpha,numbre=number,keep_max=keep_max)
    #else :
        #return simplify_degree(180*alpha/math.pi)

