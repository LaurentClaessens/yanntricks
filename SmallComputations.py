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

# copyright (c) Laurent Claessens, 2010,2011,2013-2015
# email: moky.math@gmai.com

"""
This submodule contains some auxiliary computations that have to be performed 
by phystricks but that are not geometry.
"""


from __future__ import division # Used in MultipleBigger and MultipleLower

from sage.all import *
import codecs

from phystricks import WrapperStr

var=WrapperStr(var)

def MultipleBetween(Dx,mx,Mx,mark_origin=True):
    """
    Return the list of values that are all the integer multiple of Dx between mx and Mx.

    If <mark_origin> is True, the list includes 0 if applicable.
    """
    ni=ceil(float(mx)/Dx)
    nf=floor(float(Mx)/Dx)
    l = [i*Dx for i in range(ni,nf+1)]
    if not mark_origin :
        try :
            l.remove(0)
        except ValueError :
            pass
    return l


def SubGridArray(mx,Mx,Dx,num_subX):
    """ Provides the values between mx and Mx such that there are num_subX-1 numbers between two integer separated by Dx """
    dx = float(Dx)/num_subX
    valeurs = []
    base = MultipleLower(mx,Dx)
    for i in range(0,ceil((Mx-mx)*num_subX/Dx)+3*num_subX):     # The range is designed by purpose to be sure to be too wide
        tentative = base + float(i)*dx
        if (tentative < Mx) and (tentative > mx) and ( i % num_subX <> 0 ) :
            valeurs.append(tentative)
    return valeurs

def MainGridArray(mx,Mx,Dx):
        """
        Return the list of number that are
        1. integer multiple of Dx
        2. between mx and Mx

        If mx=-1.4 and Dx=0.5, the first element of the list will be -1
        If mx=-1.5 and Dx=0.5, the first element of the list will be -1.5
        If mx=0 and Dx=1, the first element of the list will be 0.
        """
        #for y in range(MultipleBigger(self.BB.my,self.Dy),MultipleLower(self.BB.My,self.Dy)+1,self.Dy):
        m=mx/Dx
        if not m.is_integer():
            m = floor(mx/Dx - 1)
        M=Mx/Dx
        if not M.is_integer():
            M = ceil(Mx/Dx + 1)
        a=[]
        # These two lines are cancelling all the previous ones.
        m = floor(mx/Dx - 1)
        M = ceil(Mx/Dx + 1)
        for i in range(m,M):
            tentative=i*Dx
            if (tentative >= mx) and (tentative <= Mx):
                a.append(tentative)
        return a

class CalculSage(object):
    # I cannot merge the function for solving with respect to one or more variables because Sage returns like that:
    # If 1 and 2 are the solutions for one variable : [x == 1,x==2]
    # If (1,2) and (3,4) are solutions of a two variable equation : [ [x==1,y==2],[x==3,y==4] ]
    # The list nesting structure is really different. Do I have to read the doc ?
    def solve_one_var(self,eqs,var):
        """
        Solve the equations with respect to the given variable

        Returns a list of numerical values.
        """
        liste = solve(eqs,var,explicit_solutions=True)
        a = []
        for soluce in liste :
            a.append(numerical_approx(soluce.rhs()))
        return a
    def solve_more_vars(self,eqs,*vars):
        """
        Solve the equations with respect to the given variables

        Returns a list like [  [1,2],[3,4] ] if the solutions are (1,2) and (3n4)
        """
        liste = solve(eqs,vars,explicit_solutions=True)
        a = []
        for soluce in liste :
            sol = []
            for variable in soluce :
                sol.append( numerical_approx(variable.rhs()))
            a.append(sol)
        return a

# TODO : this class should not exist.
class Fichier(object):
    def __init__ (self, filename):
        self.NomComplet = filename
        self.chemin = self.NomComplet
        self.nom = os.path.basename(self.chemin)
        self.filename=filename
    def open_file(self,opt):
        self.file = codecs.open(self.chemin,encoding="utf8",mode=opt)
    def close_file(self):
        self.file.close()
    def write(self,texte,opt):
        """ Write in a file following the option """
        self.open_file(opt)
        self.file.write(texte)
        self.close_file()
    def contenu(self):
        r"""
        Return the list of the lines of the file, including the \n at the end of each line.
        """
        self.open_file("r")
        c = [l for l in self.file]
        self.close_file()
        return c

def RemoveLastZeros(x,n):
    """
    Cut the number x to n decimals and then remove the last zeros.

    If there remain no decimals, also remove the dot.
    We only cut a given number of decimals; if the integer part has more digits, we keep them.
    
    The output is a string, not a number.

    INPUT:

    - ``x`` - a number.

    - ``n`` - the number of decimals we want to keep.

    OUTPUT:
    A string.

    EXAMPLES::

        sage: from phystricks.SmallComputations import *
        sage: RemoveLastZeros(1.000,4)
        '1'
        sage: RemoveLastZeros(3/4,1)
        '0.7'
        sage: RemoveLastZeros(3/4,3)
        '0.75'
        sage: RemoveLastZeros(3/4,4)
        '0.75'
        sage: RemoveLastZeros(pi,4)
        '3.1415'
        sage: RemoveLastZeros(130*e,2)
        '353.37'

    NOTE :
    Part of the algorithm comes from
    http://www.java2s.com/Code/Python/Development/StringformatFivedigitsafterdecimalinfloat.htm
    """
    s="%.15f"%x
    t=s[:s.find(".")+n+1]
    k=len(t)-1
    while t[k]=="0":
        k=k-1
    u=t[:k+1]
    if u[-1]==".":
        return u[:-1]
    return u

def latinize(word):
    """
    return a "latinized" version of a string.

    From a string, return something that can be used as point name, file name.
    In particular, remove the special characters, put everything in lowercase,
    and turn the numbers into letters.

    This function is used in order to turn the script name into a
    string that can be a filename for the LaTeX's intermediate file.

    INPUT:

    - ``word`` - string

    OUTPUT:
    string
    
    EXAMPLES::

        sage: from phystricks.SmallComputations import *
        sage: latinize("/home/MyName/.sage/my_script11.py")
        'homeMyNameDsagemyscriptOODpy'

    ::

        sage: from phystricks.SmallComputations import *
        sage: latinize("/home/MyName/.sage/my_script13.py")
        'homeMyNameDsagemyscriptOThDpy'
    """
    latin = ""
    for s in word:
        if s.lower() in "abcdefghijklmnopqrstuvwxyz" :
            latin = latin+s
        if s=="1":
            latin = latin+"O"
        if s=="2":
            latin = latin+"T"
        if s=="3":
            latin = latin+"Th"
        if s=="4":
            latin = latin+"F"
        if s=="5":
            latin = latin+"Fi"
        if s=="6":
            latin = latin+"S"
        if s=="7":
            latin = latin+"Se"
        if s=="8":
            latin = latin+"H"
        if s=="9":
            latin = latin+"N"
        if s=="0":
            latin = latin+"Z"
        if s==".":
            latin = latin+"D"
    return latin


def number_at_position(s,n):
    """
    return the number being at position `n` in `s`
    as well as the first and last positions of that number in `s`.

    Return False is the position `n` is not part of a number.

    INPUT:

    - ``s`` - a string.

    - ``n`` - a number.

    OUTPUT:

    a tuple (string,integer,integer)

    EXAMPLES:

        sage: from phystricks.SmallComputations import *
        sage: s="Point(-1.3427,0.1223)"
        sage: number_at_position(s,9)
        ('-1.3427', 6, 13)
        sage: number_at_position(s,6)
        ('-1.3427', 6, 13)

        sage: number_at_position(s,3)
        (False, 0, 0)

        sage: s="\\begin{pspicture}(-0.375000000000000,-1.94848632812500)(3.00000000000000,1.94860839843750)"
        sage: number_at_position(s,20)
        ('-0.375000000000000', 18, 36)

        sage: number_at_position(s,27)
        ('-0.375000000000000', 18, 36)

        sage: number_at_position(s,60)
        ('3.00000000000000', 56, 72)

        sage: number_at_position(s,80)
        ('1.94860839843750', 73, 89)

    That allows to make cool replacements. In the following, we replace
    the occurrence of "0.12124" that is on position 4::

        sage: s="Ps=0.12124 and Qs=0.12124"
        sage: v,first,last=number_at_position(s,4)
        sage: print s[:first]+"AAA"+s[last:]
        Ps=AAA and Qs=0.12124

    NOTE:

    We cannot return the number since the aim is to substitute it *as string* in the
    function :func:`string_number_comparison`.

    The problem in returning a number is the following::

        sage: SR(str('1.94848632812500'))
        1.94848632812

    """
    digits=["0","1","2","3","4","5","6","7","8","9"]
    number_elements = digits+["-","."]
    s=str(s)
    if s[n] not in number_elements :
        return False,0,0
    i=n
    while s[i] in number_elements:
        i=i-1
    first=i+1
    i=n
    while s[i] in number_elements:
        i=i+1
    last=i
    # When treating the string read in the test file,
    # the string is an unicode. SR does not work with unicode
    return str(s[first:last]),first,last

def get_line(s,pos):
    r"""
    return the line containing `s[pos]`

    INPUT:

    - ``s`` - a srting.

    - ``pos`` - integer.

    EXAMPLES::

        sage: from phystricks.SmallComputations import *
        sage: s="Hello\n how do you do ? \n See you"
        sage: print get_line(s,10)
        how do you do ?

    """
    a=s.rfind("\n",0,pos)
    b=s.find("\n",pos,len(s))
    return s[a+1:b]


def string_number_comparison(s1,s2,epsilon=0.01,last_justification=""):
    r"""
    Compare two strings. 

    The comparison is True is the two string differ by numbers that are `epsilon`-close.

    It return a tuple of a boolean and a string. The string is a justification of the result.

    INPUT:

    - ``s1`` - first string.

    - ``s2`` - second string.

    - ``epsilon`` - tolerance.

    OUTPUT:

    tuple (boolean,string). The boolean says if the two strings are equal up to `epsilon`-close numbers.
                            The string provides a short explanation.

    EXAMPLES:

    In the following, the comparison fails due to
    the first number::

        sage: from phystricks.SmallComputations import *
        sage: s1="Point(-0.2,0.111)"
        sage: s2="Point(-0.3,0.111)"
        sage: string_number_comparison(s1,s2)
        (False, 'Distance between -0.2 and -0.3 is larger than 0.01.')

    In the following the comparison fails due to the second number::

        sage: s1="Point(-0.02,1)"
        sage: s2="Point(-0.03,2)"
        sage: string_number_comparison(s1,s2,epsilon=0.1)
        (False, 'd(-0.02,-0.03)=0.01\nDistance between 1 and 2 is larger than 0.100000000000000.')

    Here the comparison succeed::

        sage: s1="Point(1.99,1.001)"
        sage: s2="Point(2,1.002)"
        sage: string_number_comparison(s1,s2,epsilon=0.1)
        (True, 'd(1.99,2)=-0.01\nd(1.001,1.002)=-0.001\n')

    """

    if s1 == s2:
        return True,last_justification
    pos=0
    while s1[pos] == s2[pos]:
        pos = pos+1
    v1,first1,last1=number_at_position(s1,pos)
    v2,first2,last2=number_at_position(s2,pos)

    if v1 == False or v2 == False :
        line1=get_line(s1,pos)
        line2=get_line(s2,pos)
        justification="There is a difference outside a number\nExpected:\n%s\nGot:\n %s"%(line2,line1)
        return False,justification
    if abs(SR(v1)-SR(v2))<epsilon:
        justification=last_justification+"d(%s,%s)=%s\n"%(v1,v2,str(SR(v1)-SR(v2)))
        t1=s1[:first1]+v2+s1[last1:]
        t2=s2
        return string_number_comparison(t1,t2,epsilon=epsilon,last_justification=justification)
    justification=last_justification+"Distance between %s and %s is larger than %s."%(str(v1),str(v2),str(epsilon))
    return False,justification

def around(x,decimals):
    """
    return `x` truncated after a certain number of decimals.

    INPUT:

        - ``x`` - a number
        - ``deciamsl`` - integer

        OUTPUT:

        A number.

        EXAMPLES::

            sage: from phystricks.SmallComputations import *
            sage: around(100.6867867,3)
            100.687

    """
    from numpy import around as numpy_around
    a=[x]
    return numpy_around(a,decimals=decimals)[0]

def MyMinMax(dico_sage,decimals=3):
    """
    return the dictionary with numbers cut to `decimals` digits.

    INPUT:

    - ``dico_sage`` - a dictionary with number values

    - ``decimals`` - (default=3) the number of digits after the unity to keep

    OUTPUT:

    A dictionary. The keys are `str`, not unicode.

    EXAMPLES:

        sage: from phystricks.SmallComputations import *
        sage: d={'xmin': -0.3456475, 'ymin': -1.94565, 'ymax': 1.7895, 'xmax': 3.0000124}
        sage: MyMinMax(d,decimals=2)
        {'xmin': -0.34999999999999998, 'ymin': -1.95, 'ymax': 1.79, 'xmax': 3.0}


    """
    return dict(   [ (str(k),around(numerical_approx(dico_sage[k]),decimals=decimals)) for k in dico_sage.keys()  ]   )

def MultipleLower(x,m):
    """ return the biggest multiple of m which is lower or equal to x"""
    return floor(x/m)*m

def MultipleBigger(x,m):
    """
    Return the lower multiple of m which is bigger or equal to x
    
    EXAMPLES ::

        sage: from phystricks.SmallComputations import *
        sage: MultipleBigger(11.0,2)
        12
    """
    return ceil(x/m)*m

def enlarge_a_little_up(x,m,epsilon):
    """
    see the description of the function enlarge_a_little of the class BoundingBox.
    This function makes the job for one number.
    """
    raise DeprecationWarning
    if int(x/m) == x/m:
        return x+epsilon
    else : 
        return MultipleBigger(x,m)+epsilon
        
def enlarge_a_little_low(x,m,epsilon):
    """
    see the description of the function enlarge_a_little of the class BoundingBox.
    This function makes the job for one number.
    """
    raise DeprecationWarning
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
    describe an angle.

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

        # 'GraphOfACircle' creates its angleI like that :
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

        # From here 'value_degree' and 'value_radian' are fixed and we make some check.

        s=numerical_approx(value_degree)
        k=abs(s).frac()
        if k<0.00000001 :
            #print "dep degree",dep_value_degree,numerical_approx(dep_value_degree)
            #print "dep_radian",dep_value_radian,numerical_approx(dep_value_radian)
            value_degree=s.integer_part()

        self.degree=value_degree
        self.radian=value_radian
        if self.degree>359 and self.radian < 0.1:
            print "DBwRgm",self.degree,self.radian
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
        if isinstance(coef,degreeUnit) or isinstance(coef,radianUnit):
            return self
        return AngleMeasure(value_radian=coef*self.radian)
    # The following is floordiv to be used with //
    # I do not know why __div__ does not work. I use it in GraphOfAFractionPieDiagram
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
            #if isinstance(other,sage.rings.integer.Integer) or isinstance(other,int):
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
                return -1       # Here was 1 up to November, 8, 2012
            if self.degree == other.degree :
                return 0
    def __str__(self):
        return "AngleMeasure, degree=%s,radian=%s"%(str(numerical_approx(self.degree)),str(self.radian))
    def __repr__(self):
        return self.__str__()


class PolarCoordinates(object):
    def __init__(self,r,value_degree=None,value_radian=None):
        self.r = r
        self.measure=AngleMeasure(value_degree=value_degree,value_radian=value_radian)
        self.degree=self.measure.degree
        self.radian=self.measure.radian
    def __str__(self):
        return "PolarCoordinates, r=%s,degree=%s,radian=%s"%(str(self.r),str(self.degree),str(self.radian))

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
            # This is an error corrected on September, 10, 2014
            #radian=pi/2-radian
            radian=radian+pi
        if Qy<=0:
            radian=pi+radian
    # Only positive values (February 11, 2015)
    if radian < 0 :
        radian=radian+2*pi
    return PolarCoordinates(r,value_radian=radian)

    # The following is the old version, before fusion with GraphOfAPoint.polar_coordinates()
    raise DeprecationWarning
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

def polar_with_dilatation(r,theta,xunit=1,yunit=1):
    """
    return the polar coordinated that you have to give
    in such a way the it *visually* appears `(r,theta)`
    when `xunit` and `yunit` are given.

    The input and output angles are in radian.

    INPUT:

    - ``r`` - the distance you want to see.

    - ``theta`` - the angle you want to see (radian).

    - ``xunit`` - the dilatation factor in the `x` direction.

    - ``yunit`` - the dilatation factor in the `y` direction.

    OUTPUT:

    a tuple `(distance,angle)`

    EXAMPLES::

        sage: from phystricks.SmallComputations import *
        sage: polar_with_dilatation(2,pi,2,1)
        (1, pi)
        sage: polar_with_dilatation(1,pi/4,2,2)
        (1/2, 1/4*pi)

    Notice the difference between::

        sage: polar_with_dilatation(1,pi/2,2,1/2)
        (2, 1/2*pi)

    and::

        sage: polar_with_dilatation(1,pi/2,2,0.5)
        (2.00000000000000, 1/2*pi)
    """
    if cos(theta)==0:
        return (r/yunit,theta)
    alpha=atan( (xunit/yunit)*tan(theta) )
    rp=(r/xunit)*(cos(theta)/cos(alpha))

    if rp < 0:
        rp=-rp
        alpha=alpha+pi
    return (rp,alpha)
    

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
#degree=DegreeConversions.conversion
#radian=RadianConversions.conversion
FullAngle=AngleMeasure(value_degree=360)

def split_list(starting_list,fun,cut_ymin,cut_ymax):
    ldel=[]
    l=[]
    for i,k in enumerate(starting_list):
        try:
            on=fun(k) > cut_ymin and fun(k) < cut_ymax
        except ValueError:      # Happens when 1/x and x=0.
            on=False
        if on :
            l.append(k)
        else:
            ldel.append(l)
            l=[]
    ldel.append(l)
    while [] in ldel:
        ldel.remove([])
    s=[  (l[0],l[-1])  for l in ldel  ]
    return s

def find_roots_recursive(f,a,b,tol=0.000000000001):
    """
    Return the roots of the function 'f' between 'a' and 'b' as a list.

    The list is sorted.
    """
    # The method was proposed by ndomes in http://ask.sagemath.org/question/8886/obtaining-all-numerical-roots-of-a-function-in-an-interval/
    L = []
    try:
        x0 = find_root(f,a,b)
    except RuntimeError :
        return []
    L.append(x0)
    L += find_roots_recursive(f,a,x0-tol,tol)       
    L += find_roots_recursive(f,x0+tol,b,tol)       
    L.sort()
    return L
