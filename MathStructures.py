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

# copyright (c) Laurent Claessens, 2010,2011,2013-2016
# email: moky.math@gmai.com

from Utilities import *
from SmallComputations import MultipleBetween

class PolarCoordinates(object):
    def __init__(self,r,value_degree=None,value_radian=None):
        self.r = r
        self.measure=AngleMeasure(value_degree=value_degree,value_radian=value_radian)
        self.degree=self.measure.degree
        self.radian=self.measure.radian
    def __str__(self):
        return "PolarCoordinates, r=%s,degree=%s,radian=%s"%(str(self.r),str(self.degree),str(self.radian))

def DegreeAngleMeasure(x):
    return AngleMeasure(value_degree=x)
def RadianAngleMeasure(x):
    return AngleMeasure(value_radian=x)

class AngleMeasure(object):
    """
    Describe an angle.

    This class is an attempt to abstract the degree/radian problem.

    EXAMPLES::

        sage: from phystricks.SmallComputations import *
        sage: x=AngleMeasure(value_radian=pi/2)
        sage: x()
        90

        sage: from phystricks.SmallComputations import *
        sage: x=AngleMeasure(value_degree=360)
        sage: print x
        AngleMeasure, degree=360.000000000000,radian=2*pi

    Conversions are exact::

        sage: a=AngleMeasure(value_degree=30)
        sage: cos(a.radian)
        1/2*sqrt(3)

    You can create a new angle from an old one::

        sage: a=AngleMeasure(value_degree=180)
        sage: b=AngleMeasure(a)
        sage: b.degree
        180

    If the numerical approximation of an angle in degree is close to an integer to minus than 1e-10, we round it.
    The reason is that in some case I got as entry such a number : -(3.47548077273962e-14)/pi + 360
    Then the computation of radian gave 0 and we are left with degree around 359.9999 while the radian was rounded to 0.
    (June, 2, 2013)

        sage: a=AngleMeasure(value_degree=-(3.47548077273962e-14)/pi + 360)
        sage: a.degree
        360
        sage: a.radian
        2*pi

    """
    # TODO : take into account the following thread:
    # http://ask.sagemath.org/question/332/add-a-personnal-coercion-rule
    def __init__(self,angle_measure=None,value_degree=None,value_radian=None,keep_negative=False):
        dep_value_degree=value_degree
        dep_value_radian=value_radian

        # 'CircleGraph' creates its angleI like that :
        #    self.angleI = AngleMeasure(value_degree=angleI,keep_negative=True)
        #  in this case, 'value_degree' can be either a number, either a 'AngleMeasure' because the user has choice when writing something like
        #     cir=Circle(O,A,angleI=...,angleF=...)
        for k in [value_degree,value_radian]:
            if isinstance(k,AngleMeasure):
                angle_measure=k
                value_degree=None
                value_radian=None
        for k in [value_degree,value_radian]:
            if isinstance(k,PolarCoordinates):
                angle_measure=k
                value_degree=None
                value_radian=None
        if angle_measure :
            value_degree=angle_measure.degree
            value_radian=angle_measure.radian
        else:
            from Utilities import degree
            from Utilities import radian
            if value_degree is not None:
                value_radian=radian(value_degree,keep_max=True)
                if keep_negative and value_degree < 0 and value_radian > 0:
                    print("This is strange ...")
                    value_radian=value_radian-2*pi
            if value_degree == None :
                value_degree=degree(value_radian,keep_max=True)
                if keep_negative and value_radian < 0 and value_degree > 0:
                    print("This is strange ...")
                    value_degree=value_degree-360

        # From here 'value_degree' and 'value_radian' are fixed and we make some checks.
        s=numerical_approx(value_degree)
        k=abs(s).frac()
        if k<0.00000001 :
            value_degree=s.integer_part()

        self.degree=value_degree
        self.radian=value_radian
        if self.degree>359 and self.radian < 0.1:
            print "Problem with an angle : ",self.degree,self.radian
            print "dep degree",dep_value_degree,numerical_approx(dep_value_degree)
            print "dep_radian",dep_value_radian,numerical_approx(dep_value_radian)
            print "final degree",numerical_approx(value_degree)
            print "final radian",numerical_approx(value_radian)
            raise ValueError
        if self.degree==None or self.radian==None:
            raise ValueError,"Something wrong"
    def positive(self):
        """
        If the angle is negative, return the corresponding positive angle.

        EXAMPLES::

            sage: from phystricks.SmallComputations import *
            sage: a=AngleMeasure(value_degree=-30)
            sage: a.positive().degree
            330
        """
        if self.degree >= 0 :
            return self
        if self.degree < 0 :
            return AngleMeasure(value_degree=360+self.degree)
    def __mul__(self,coef):
        from Utilities import degreeUnit
        from Utilities import radianUnit
        if isinstance(coef,degreeUnit) or isinstance(coef,radianUnit):
            return self
        return AngleMeasure(value_radian=coef*self.radian)
    # The following is floordiv to be used with //
    # I do not know why __div__ does not work. I use it in FractionPieDiagramGraph
    def __floordiv__(self,coef):
        return AngleMeasure(value_radian=self.radian/coef)
    def __rmul__(self,coef):
        return self*coef
    def __sub__(self,other):
        return self+(-other)
        return AngleMeasure(value_radian=self.radian-other.radian)
    def __add__(self,other):
        """
        return the sum of two angles.

        EXAMPLES::

            sage: from phystricks.SmallComputations import *
            sage: a=AngleMeasure(value_degree=45)
            sage: b=AngleMeasure(value_radian=pi/3)
            sage: a.degree,a.radian
            (45, 1/4*pi)
            sage: b.degree,b.radian
            (60, 1/3*pi)
            sage: (a+b).degree,(a+b).radian
            (105, 7/12*pi)

        If you add with a number, guess if you are speaking of degree or radian ::

            sage: a=AngleMeasure(value_degree=45)
            sage: (a+pi/2).degree
            135
            sage: (a+45).degree
            90
        """
        try :
            return AngleMeasure(value_radian=self.radian+other.radian)
        except AttributeError :
            if other in ZZ :
                return AngleMeasure(value_degree=self.degree+other)
            elif "pi" in repr(other) :
                return AngleMeasure(value_radian=self.radian+other)
            else :
                raise TypeError, "I do not know how to add {0} with {1}".format(type(self),type(other))
    def __neg__(self):
        return AngleMeasure(value_degree=-self.degree)
    def __call__(self):
        return self.degree
    def __div__(self,coef):
        return AngleMeasure(value_radian=self.radian/coef)
    def __cmp__(self,other):
        if isinstance(other,AngleMeasure):
            if self.degree > other.degree :
                return 1
            if self.degree < other.degree :
                return -1
            if self.degree == other.degree :
                return 0
    def __str__(self):
        return "AngleMeasure, degree=%s,radian=%s"%(str(numerical_approx(self.degree)),str(self.radian))
    def __repr__(self):
        return self.__str__()

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
        1. values that are all the integer multiple of 
                <frac>*self.numerical_value 
            between mx and Mx
        2. the multiple of the basis unit.

        Give <frac> as literal real. Recall that python evaluates 1/2 to 0. If you pass 0.5, it will be converted back to 1/2 for a nice display.
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
                text="$"+latex(pos).replace("TheTag",self.latex_symbol)+"$"  # This risks to be Sage-version dependent.
                if "mathit" in text:
                    print("ooPCTPooVMczXp",text)
                    print(pos)
                    print(latex(pos))
                l.append((x,text))
        return l
