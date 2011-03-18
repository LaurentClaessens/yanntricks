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
"""

#from __future__ import division
from sage.all import *
import codecs
import math, sys
from phystricks.BasicGeometricObjects import *
from phystricks.SmallComputations import *

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

        sage: latinize("/home/MyName/.sage/my_script11.py")
        'homeMyNameDsagemyscriptOODpy'

    ::

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

    names=PointsNameList()
    for m in rematch:
        name=names.next()
        s=s.replace("{%s}"%m,"{X%s}"%name).replace("(%s)"%m,"(X%s)"%name)

    return s

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

def string_number_comparison(s1,s2,epsilon=0.01,last_justification=""):
    """
    Compare two strings. 

    The comparison is True is the two string differ by numbers that are `epsilon`-close. 

    It return a tuple of a boolean and a string. The string is a justification of the result.

    INPUT:

    - ``s1`` - first string.

    - ``s2`` - second string.

    - ``epsilon`` - tolerance.

    OUTPUT:

    tuple (boolean,string).

    EXAMPLES:

    In the following, the comparison fails due to
    the first number::

        sage: s1="Point(-0.2,0.111)"
        sage: s2="Point(-0.3,0.111)"
        sage: string_number_comparison(s1,s2)
        (False, 'Distance between -0.2 and -0.3 is larger than 0.01.')

    In the following the comparison fails due to
    the second number::

        sage: s1="Point(-0.02,1)"
        sage: s2="Point(-0.03,2)"
        sage: string_number_comparison(s1,s2,epsilon=0.1)
        (False, 'd(-0.02,-0.03)=0.01;Distance between 1 and 2 is larger than 0.100000000000000.')

     Here the comparison succeed::

        sage: s1="Point(1.99,1.001)"
        sage: s2="Point(2,1.002)"
        sage: string_number_comparison(s1,s2,epsilon=0.1)
        (True, 'd(1.99,2)=-0.01;d(1.001,1.002)=-0.001;')

    """

    if s1 == s2:
        return True,last_justification
    pos=0
    while s1[pos] == s2[pos]:
        pos = pos+1
    v1,first1,last1=number_at_position(s1,pos)
    v2,first2,last2=number_at_position(s2,pos)

    #print "343 j'ai trouvé",v1,"dans"
    #print "---"
    #print s1
    #print "---"
    #print "343 j'ai trouvé",v2,"dans"
    #print "---"
    #print s2
    #print "---"


    if v1 == False or v2 == False :
        return False,"There is a difference outside a number"
    if abs(SR(v1)-SR(v2))<epsilon:
        justification=last_justification+"d(%s,%s)=%s\n"%(v1,v2,str(SR(v1)-SR(v2)))

        t1=s1[:first1]+v2+s1[last1:]

        #print "différence acceptée",v1,v2
        #print "je vais concaténer"
        #print s1
        #print s1[:first1]
        #print v2
        #print s1[last1:]

        t2=s2
        
        #print "371 récurence, je vais comparer"
        #print "---"
        #print t1
        #print "---"
        #print t2
        #print "---"

        return string_number_comparison(t1,t2,epsilon=epsilon,last_justification=justification)
    justification=last_justification+"Distance between %s and %s is larger than %s."%(str(v1),str(v2),str(epsilon))
    return False,justification
     

class TestPspictLaTeXCode(object):
    def __init__(self,pspict):
        self.pspict=pspict
        self.name=pspict.name
        self.notice_text="This is a testing file containing the LaTeX code of the figure %s."%(self.name)
        self.test_file=Fichier("test_pspict_LaTeX_%s.tmp"%(self.name))
    def create_test_file(self):
        """
        Write the LaTeX code of `pspict` in a file.

        The purpose is to compare that file with the code actually 
        produced later. This is a way to test changes in phystricks.

        INPUT:

        - ``pspict`` - a pspicture

        If the option `--create_test_file` is passed to the program, this function is called
        on each pspicture when concluding a :class:`figure`.
        """
        text=unify_point_name(self.notice_text+self.pspict.contenu_pstricks)
        self.test_file.write(text,"w")
    def test(self):
        print "---"
        print "Testing pspicture %s ..."%self.name
        obtained_text=unify_point_name(self.pspict.contenu_pstricks)
        expected_text=unify_point_name("".join(self.test_file.contenu()).replace(self.notice_text,""))
        boo,justification = string_number_comparison(obtained_text,expected_text)
        if not boo:
            print "Test failed"
            print "Expected:"
            print expected_text
            print "----"
            print "Got:"
            print obtained_text
            print "---"
            print justification
            raise ValueError,"The test of pspicture %s failed. %s"%(str(self.name),justification)
        print justification
        print "Successful test for pspicture %s"%self.name
        print "---"
    
sysargvzero = sys.argv[0][:]
def newwriteName():
    r"""
    This function provides the name of the \newwrite that will be used all long the script.

    Basically, that provides the name of the intermediate file that will
    be used by LaTeX for writing the box's sizes (and other counters).

    See the attribute pspict.newwriteDone and the method pspict.get_counter_value
    
    NOTE:
    We cannot use one different \newwrite for each counter because
    LaTeX is limited in the number of available \newwrite.

    Since we want two different scripts to use two different intermediates files, 
    the name of the \newwrite will be created on the basis of the script name,
    that is sys.argv[0]

    The idea is that for a LaTeX document containing 100 figures, 
    these will be created from the same script. If not, you'll get 100 different \newwrite
    and crash your LaTeX compilation.

    OUTPUT:
    A string containing "writeOf"+something_based_on_the_script_name
    """
    return "writeOf"+latinize(sysargvzero)
def counterName():
    r"""
    This function provides the name of the counter. 
    
    This has the same use of newwriteName, for the same reason of limitation.
    """
    return "counterOf"+latinize(sysargvzero)
def newlengthName():
    r"""
    This function provides the name of the length.
    
    This has the same use of newwriteName, for the same reason of limitation.
    """
    return "lengthOf"+latinize(sysargvzero)

class global_variables(object):
    def __init__(self):
        self.eps_exit = False
        self.pdf_exit = False
        self.test_exit = False
        self.make_tests = False
        self.pstricks_language = True
        self.list_exits = ["eps","pdf"]
    def special_exit(self):
        for sortie in self.list_exits :
            if self.__getattribute__(sortie+"_exit"):
                return True
        return False

class Fichier(object):
    def __init__ (self, filename):
        self.NomComplet = filename
        self.chemin = self.NomComplet               
        self.nom = os.path.basename(self.chemin)
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
        Return the list of the lines of the file, inlcuding the \n at the end of each line.
        """
        self.open_file("r")
        c = [l for l in self.file]
        self.close_file()
        return c

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

class CalculPolynome(object):
    """
    This class should disappear when I learn how to perform euclidian divisions with Sage.
    """
    # La méthode calcul donne la sortie de maxima en brut. Pour traiter l'information, il faudra encore des tonnes de manipulations, et on peut déjà en mettre dans filtre
    def calcul(self,ligne,filtre):
        commande =  "maxima --batch-string=\"display2d:false; "+ligne+";\""+filtre 
        return commands.getoutput(commande)
    # reponse donne ce que calcule donne, après extraction de la partie intéressante, c'est à dire prise de grep o2 et enlevure de "o2" lui-même.
    def reponse(self,ligne):
        ligne = self.calcul(ligne,"|grep o2")
        return ligne.replace("(%o2)","").replace(" ","")
    def DivPoly(self,P,Q):
        l = []
        m = []
        for i in range(0,P.deg-Q.deg+1):
            ligne =  "coeff( expand( divide("+P.maxima+","+Q.maxima+"))[1],x,"+str(P.deg-Q.deg-i)+")"
            l.append(  int( self.reponse(ligne) ) )
        for i in range(0,Q.deg+1): 
            ligne =  "coeff( expand( divide("+P.maxima+","+Q.maxima+"))[2],x,"+str(Q.deg-i)+")"
            m.append( int (self.reponse(ligne) ) )
        return [Polynome(l),Polynome(m)]
    def MulPoly(self,P,Q):
        l = []
        for i in range(0,P.deg+Q.deg+1):
            ligne = "coeff( expand(("+P.maxima+")*("+Q.maxima+")),x,"+str(P.deg+Q.deg-i)+")"    
            l.append( int( self.reponse(ligne)) )
        return Polynome(l)
    # Cette méthode est exactement la même que la précédente, au changement près de * vers +. Y'a peut être moyen de factoriser ...
    def sub_polynome(self,P,Q):
        l = []
        for i in range(0,P.deg+Q.deg+1):
            ligne =   "coeff( expand(("+P.maxima+")-("+Q.maxima+")),x,"+str(P.deg+Q.deg-i)+")"    
            rep = self.reponse(ligne) 
            if rep <> "":
                l.append(int(rep))
        return Polynome(l)


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
        1. integer multiple of Dy
        2. between mx and Mx

        If mx=-1.4 and Dx=0.5, the first element of the list will be -1
        If mx=-1.5 and Dx=0.5, the first element of the list will be -1.5
        """
        #for y in range(MultipleBigger(self.BB.my,self.Dy),MultipleLower(self.BB.My,self.Dy)+1,self.Dy):
        a=[]
        m = floor(mx/Dx - 1)
        M = ceil(Mx/Dx + 1)
        for i in range(m,M):
            tentative=i*Dx
            if (tentative >= mx) and (tentative <= Mx):
                a.append(tentative)
        return a

class Triangle(object):
    def __init__(self,A,B,C):
        self.A = A
        self.B = B
        self.C = C

def Graph(X,*arg):
    """This function is supposed to be only used by the end user."""
    print "The function Graph should not be used"
    raise TypeError
    try :
        return X.default_associated_graph_class()(X,arg)
    except TypeError,datay :
        return X.default_associated_graph_class()(X)
    except AttributeError,data :
        raise
        if type(X) == phyFunction :
            return GraphOfAphyFunction(X,arg[0],arg[1])
        if type(X) == ParametricCurve :
            return GraphOfAParametricCurve(X,arg[0],arg[1])
        if type(X) == Segment :
            return GraphOfASegment(X)
        if type(X) == AffineVector :
            return GraphOfAVector(X)
        if type(X) == Circle :
            return GraphOfACircle(X)
        if type(X) == Point :
            return GraphOfAPoint(X)
    
class GrapheDesphyFunctions(object):
    def __init__(self,L):
        self.liste_GraphOfAphyFunction = L
    def add_option(opt):
        for gf in self.liste_fonctions :
            gf.add_option(opt)

def SubstitutionMathMaxima(exp):
    a = exp
    for i in range(1,10):
        a = a.replace("math.log"+str(i),"log("+str(i)+")^(-1)*log")
    return a.replace("math.log","log").replace("math.tan","tan").replace("math.pi","%pi").replace("math.","")

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

        sage: grid=Grid( BoundingBox() )
        sage: grid.main_horizontal.parameters.color = "red"

    """
    def __init__(self,bb):
        self.BB = bb
        self.options = Options()
        self.separator_name="GRID"
        self.add_option({"Dx":1,"Dy":1})        # Default values, have to be integer.
        self.Dx = self.options.DicoOptions["Dx"]
        self.Dy = self.options.DicoOptions["Dy"]
        self.num_subX = 2
        self.num_subY = 2
        self.draw_border = False
        self.main_horizontal = GraphOfASegment(Segment(Point(0,1),Point(1,1)))  # Ce segment est bidon, c'est juste pour les options de tracé.
        self.main_horizontal.parameters.color="gray"
        self.main_horizontal.parameters.style = "solid"
        self.main_vertical = GraphOfASegment(Segment(Point(0,1),Point(1,1)))    
        self.main_vertical.parameters.color="gray"
        self.main_vertical.parameters.style = "solid"
        self.sub_vertical = GraphOfASegment(Segment(Point(0,1),Point(1,1))) 
        self.sub_vertical.parameters.color="gray"
        self.sub_vertical.parameters.style = "dotted"
        self.sub_horizontal = GraphOfASegment(Segment(Point(0,1),Point(1,1)))   
        self.sub_horizontal.parameters.color="gray"
        self.sub_horizontal.parameters.style = "dotted"
        self.border = GraphOfASegment(Segment(Point(0,1),Point(1,1)))   
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

        Please give <frac> as litteral real. Recall that python evaluates 1/2 to 0. If you pass 0.5, it will be converted to 1/2 for a nice display.
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
                text="$"+latex(pos).replace("\mbox{TheTag}",self.latex_symbol)+"$"  # This risk to be Sage-version dependant.
                l.append((x,text))
        return l

class SingleAxe(object):
    """
    Describe an axe.
    
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
    def __init__(self,C,base,mx,Mx):
        self.C=C
        self.base=base
        self.mx=mx
        self.Mx=Mx
        self.options=Options()
        self.IsLabel=False
        self.axes_unit=AxesUnit(self.base.length(),"")
        self.Dx=1
        self.arrows="->"
        self.graduation=True
        self.numbering=True
        self.mark_origin=True
        self.mark_angle=degree(base.angle().radian-pi/2)
        #self.vertical=base.vertical
        #self.horizontal=base.horizontal
    def segment(self):
        return Segment(self.C+self.mx*self.base,self.C+self.Mx*self.base)
    def add_option(self,opt):
        self.options.add_option(opt)
    def add_label(self,dist,angle,marque):
        self.IsLabel = True
        self.Label = marque
        self.DistLabel = dist
        self.AngleLabel = angle
    def no_numbering(self):
        self.numbering=False
    def no_graduation(self):
        self.graduation=False
    def graduation_points(self,pspict):
        """
        Return the list of points that makes the graduation of the axes

        By defaut, it is one at each multiple of self.base. If an user-defined axes_unit is given, then self.base is modified.
        """
        if self.graduation :
            points_list=[]
            bar_angle=SR(self.mark_angle+90).n(digits=7)    # pstricks does not accept too large numbers
            for x,symbol in self.axes_unit.place_list(self.mx,self.Mx,self.Dx,self.mark_origin):
                P=(x*self.base).F
                P.parameters.symbol="|"
                P.add_option("dotangle=%s"%str(bar_angle))
                #P.psName=P.psName+pspict.name+latinize(str(numerical_approx(x)))   # Make the point name unique.
                P.psName="ForTheBar"   # Since this point is not supposed to
                                       # be used, all of them have the same ps name.
                if self.numbering :
                    P.put_mark(0.4,self.mark_angle,symbol)      # TODO : use the size of the box as distance
                                            # I do not understand why I don't have to multiply 0.4 by xunit or yunit
                points_list.append(P)
            return points_list
        else :
            return []
    def bounding_box(self,pspict):
        BB=self.math_bounding_box(pspict)
        for P in self.graduation_points(pspict):
            BB.append(P,pspict)
        return BB
    def math_bounding_box(self,pspict):
        return self.segment().bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        """
        Return the pstricks code of the axe.
        """
        sDx=RemoveLastZeros(self.Dx,10)
        self.add_option("Dx="+sDx)
        #bgx = self.BB.mx
        #if self.BB.mx == int(self.BB.mx):      # Avoid having end of axes on an integer coordinate for aesthetic reasons.
        #   bgx = self.BB.mx + 0.01
        #self.BB.mx = bgx
        c=[]
        if self.IsLabel :
            P = self.segment().F
            P.parameters.symbol="none"
            P.put_mark(self.DistLabel,self.AngleLabel,self.Label)
            c.append(P.pstricks_code())
        if self.graduation :
            for P in self.graduation_points(pspict):
                c.append(P.pstricks_code(pspict,with_mark=True))
        h=AffineVector(self.segment())
        c.append(h.pstricks_code(pspicture))
        return "\n".join(c)

class Axes(object):
    """
    Describe a system of axes (two axes).

    By default they are orthogonal.
    """
    def __init__(self,C,bb):
        self.C = C                      
        self.BB = bb.copy()
        self.options = Options()
        self.Dx = 1
        self.Dy = 1                     # Ce sont les valeurs par défaut.
        self.arrows = "->"
        self.separator_name="AXES"
        self.graduation=True
        self.numbering=True
        self.single_axeX=SingleAxe(self.C,Vector(1,0),self.BB.mx,self.BB.Mx)
        self.single_axeX.mark_origin=False
        self.single_axeX.axes_unit=AxesUnit(1,"")
        self.single_axeY=SingleAxe(self.C,Vector(0,1),self.BB.my,self.BB.My)
        self.single_axeY.mark_origin=False
        self.single_axeY.axes_unit=AxesUnit(1,"")
        self.single_axeY.mark_angle=180
        self.single_axeX.Dx=self.Dx
        self.single_axeY.Dx=self.Dy
    def update(self):
        self.single_axeX.mx,self.single_axeX.Mx=self.BB.mx,self.BB.Mx
        self.single_axeY.mx,self.single_axeY.Mx=self.BB.my,self.BB.My
    def add_label_X(self,dist,angle,marque):
        raise DeprecationWarning,"Use self.single_axeX.add_label instead"
        self.IsLabelX = True
        self.LabelX = marque
        self.DistLabelX = dist
        self.AngleLabelX = angle
    def add_label_Y(self,dist,angle,marque):
        raise DeprecationWarning,"Use self.single_axeY.add_label instead"
        self.IsLabelY = True
        self.LabelY = marque
        self.DistLabelY = dist
        self.AngleLabelY = angle
    def add_option(self,opt):
        self.options.add_option(opt)
    def no_graduation(self):
        self.single_axeX.no_graduation()
        self.single_axeY.no_graduation()
    def no_numbering(self):
        self.single_axeX.no_numbering()
        self.single_axeY.no_numbering()
    def AjusteCircle(self,Cer):
        self.BB.AddCircle(Cer)
    def bounding_box(self,pspict=None):
        self.update()
        BB=BoundingBox()
        BB.append(self.single_axeX.bounding_box(pspict))
        BB.append(self.single_axeY.bounding_box(pspict))
        if BB.Mx==1000: 
            raise ValueError
        return BB
    def math_bounding_box(self,pspict=None):
        self.update()
        BB=BoundingBox()
        BB.append(self.single_axeX.math_bounding_box(pspict))
        BB.append(self.single_axeY.math_bounding_box(pspict))
        return BB
    def pstricks_code(self,pspict=None):
        sDx=RemoveLastZeros(self.Dx,10)
        sDy=RemoveLastZeros(self.Dy,10)
        self.add_option("Dx="+sDx)
        self.add_option("Dy="+sDy)
        bgx = self.BB.mx
        bgy = self.BB.my
        if self.BB.mx == int(self.BB.mx):       # Avoid having end of axes on an integer coordinate for aesthetic reasons.
            bgx = self.BB.mx + 0.01
        if self.BB.my == int(self.BB.my):
            bgy = self.BB.my +0.01
        self.BB.mx = bgx
        self.BB.my = bgy
        c=[]
        self.update()
        c.append(self.single_axeX.pstricks_code(pspict))
        c.append(self.single_axeY.pstricks_code(pspict))
        return "\n".join(c)

def CircleInterLigne(Cer,Ligne):
    raise DeprecationWarning, "This function is depreciated. Please use Intersection instead"
    if type(Ligne) == phyFunction :
        soluce = maxima().solve( [Cer.maxima,"y="+Ligne.maxima],["x","y"] )
    else :
        soluce = maxima().solve( [Cer.maxima,Ligne.maxima],["x","y"] )
    if len(soluce) == 0:
        return [Point(0,0),Point(0,0)]
    if len(soluce) == 1:
        return [Point(soluce[0][0],soluce[0][1]),Point(0,0)]
    if len(soluce) == 2:
        return [Point(soluce[0][0],soluce[0][1]),Point(soluce[1][0],soluce[1][1])]

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

def CircleInterphyFunction(Cer,f):
    raise AttributeError,"This is depreciated, use LineInterLine instead"       #(15 oct 2010)
    return CircleInterLigne(Cer,f)

def phyFunctionInterphyFunction(f,g):
    raise AttributeError,"This is depreciated, use LineInterLine instead"       #(15 oct 2010)
    var('x,y')
    eq1 = y == f.sage(x)
    eq2 = y == g.sage(x)
    soluce = CalculSage().solve( [eq1,eq2],[x,y] )
    a = []
    print "Nombre de solutions : "+str(len(soluce))
    for s in soluce :
        a.append( Point(s[0],s[1]) )
    return a

def LineInterLine(l1,l2):
    var('x,y')
    eq1 = l1.equation
    eq2 = l2.equation
    soluce = CalculSage().solve_more_vars( [eq1,eq2],x,y )
    s = soluce[0]
    return Point( s[0],s[1] )
    
def SinglePicture(name):
    """ Return the tuple of pspicture and figure that one needs in 90% of the cases """
    fig = GenericFigure(name)
    pspict=fig.new_pspicture(name)
    return pspict,fig

def GenericFigure(nom):
    """
    This function returns a figure with some default values. It creates coherent label, file name and prints the lines to be appended in the LaTeX file to include the figure.
    """
    label = "LabelFig"+nom
    caption = "\CaptionFig"+nom
    nFich = "Fig_"+nom+".pstricks"
    print "The result is on figure \\ref{"+label+"}."
    print "\\newcommand{"+caption+"}{<+Type your caption here+>}"
    print "\\input{Fig_"+nom+".pstricks}"
    return  figure(caption,label,nFich)

class figure(object):
    def __init__(self,caption,name,fich):
        self.caption = caption
        self.name = name
        self.xunit = 1
        self.yunit = 1
        self.code = []
        self.record_subfigure = []
        self.record_pspicture=[]
        self.fichier = Fichier (fich)

        # The order of declaration is important, because it is recorded in the Separator.number attribute.
        self.separator_dico = {}            
        self.separator_number = 0
        self.new_separator("ENTETE")
        self.new_separator("WRITE_AND_LABEL")
        self.new_separator("BEFORE SUBFIGURES")
        self.new_separator("SUBFIGURES")
        self.new_separator("AFTER SUBFIGURES")
        self.new_separator("DEFAULT")
        self.new_separator("BEFORE PSPICTURE")
        self.new_separator("PSPICTURE")
        self.new_separator("AFTER PSPICTURE")
        self.new_separator("AFTER ALL")
        add_latex_line_entete(self)

        self.add_latex_line("\\begin{figure}[ht]","BEFORE SUBFIGURES")
        self.add_latex_line("\centering","BEFORE SUBFIGURES")
    def new_separator(self,title):
        self.separator_number = self.separator_number + 1
        self.separator_dico[title]=Separator(title,self.separator_number)
    def dilatation_X(self,fact):
        """ Makes a dilatation of the whole picture in the X direction. A contraction if the coefficient is lower than 1 """
        self.xunit = self.xunit * fact
    def dilatation_Y(self,fact):
        self.yunit = self.yunit * fact
    def dilatation(self,fact):
        """ dilatations or contract that picture in both directions with the same coefficient """
        self.dilatation_X(fact)
        self.dilatation_Y(fact)
    def new_subfigure(self,caption,name=None):
        """
        Create a subfigure in the figure and return it.

        The end-user should use this instead of append_subfigure
        """
        if name==None:
            number=len(self.record_subfigure)
            name="sub"+latinize(str(number))
        ssfig=subfigure(caption,self.name+"ss"+name)
        ssfig.mother=self
        self._append_subfigure(ssfig)
        return ssfig
    def _append_subfigure(self,ssFig):      # This function was initially named AjouteSSfigure
        self.record_subfigure.append(ssFig)
        suffixe = "ssFig"+str(len(self.record_subfigure))
        if not ssFig.name:
            ssFig.name=self.name+suffixe
        #ssFig.pspicture.name=self.name+"pspict"+suffixe    (no more useful 15 oct 2010)
        print r"See also the subfigure \ref{%s}"%ssFig.name
    def new_pspicture(self,name=None,pspict=None):
        if name==None:
            number=len(self.record_pspicture)
            name="sub"+latinize(str(number))
        if pspict==None:
            pspict=pspicture("FIG"+self.name+"PICT"+name)
        self._add_pspicture(pspict)
        return pspict
    def _add_pspicture(self,pspict):
        pspict.mother=self      # This was in self.new_pspicture
        self.record_pspicture.append(pspict)
    def add_pspicture(self,pspict):
        raise DeprecationWarning,"Use fig.new_pspicture instead."
    def append_subfigure(self,pspict):
        raise DeprecationWarning,"Use fig.new_subfigure instead."
    def add_latex_line(self,ligne,separator_name="DEFAULT"):
        self.separator_dico[separator_name].add_latex_line(ligne)
    def IncrusteLigne(self,ligne,n):
        print "The method picture.IncrusteLigne() is depreciated."
        self.code[n:n]=ligne+"\n"
    def AjouteCode(self,liste_code):
        self.code.extend(liste_code)
    def conclude(self):
        for pspict in self.record_pspicture :
            # What has to be written in the WRITE_AND_LABEL part of the picture is written now
            self.add_latex_line(pspict.separator_dico["WRITE_AND_LABEL"].latex_code,"WRITE_AND_LABEL")
            pspict.separator_dico["WRITE_AND_LABEL"].latex_code=[]
            self.add_latex_line(pspict.contenu(),"PSPICTURE")           # Here, what is added depends on --eps
            if globals_vars.make_tests:
                TestPspictLaTeXCode(pspict).test()
            if globals_vars.test_exit:
                TestPspictLaTeXCode(pspict).create_test_file()
        if not globals_vars.special_exit() :
            self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+"}","BEFORE SUBFIGURES")
        for f in self.record_subfigure :
            self.add_latex_line("\subfigure["+f.caption+"]{%","SUBFIGURES")
            self.add_latex_line(f.subfigure_code(),"SUBFIGURES")
            self.add_latex_line("\label{%s}"%f.name,"SUBFIGURES")
            self.add_latex_line("}                  % Closing subfigure "+str(self.record_subfigure.index(f)+1),"SUBFIGURES")
            self.add_latex_line("%","SUBFIGURES")
        after_all=r"""\caption{%s}\label{%s}
            \end{figure}
            """%(self.caption,self.name)
        self.add_latex_line(after_all,"AFTER ALL")
        self.contenu = DicoSeparatorToCode(self.separator_dico)
    def write_the_file(self):                   # Nous sommes dans la classe figure.
        self.fichier.open_file("w")
        self.fichier.file.write(self.contenu)
        self.fichier.file.close()
            
# Le \subfigure[caption]{ ne se met pas dans le code de la classe subfigure parce que dans la classe figure, je numérote les sous-figures.
# Typiquement, une sousfigure sera juste créée en ajoutant une pspicture d'un coup, et puis c'est tout.
class subfigure(object):
    """
    This is a subfigure.

    If no label are given, a default one will be set when included in the figure.
    """
    def __init__(self,caption,name=None):
        self.caption = caption
        self.name = name
        self.record_pspicture=[]
        self.mother=None
    def add_latex_line(self,ligne,separator_name):
        self.mother.add_latex_line(ligne,separator_name)
    def new_pspicture(self,name=None):
        if name==None:
            number=len(self.record_pspicture)
            name="sub"+latinize(str(number))
        pspict=pspicture("FIG"+self.name+"PICT"+name)
        pspict.mother=self
        self._add_pspicture(pspict)
        return pspict
    def subfigure_code(self):
        a=[]
        for pspict in self.record_pspicture :
            a.append(pspict.contenu())
        return "\n".join(a)
    def _add_pspicture(self,pspicture):
        self.record_pspicture.append(pspicture)
    def add_pspicture(self,pspicture):
        raise DeprecationWarning,"use subfigure.new_pspicture instead"

class PspictureToOtherOutputs(object):
    """
    contains the informations about the transformation of a pspicture into an eps/pdf file
    The method to produce the eps file is taken from the documentation of the package pst-eps, and from some fruitful discussions on fctt
        http://archive.cs.uu.nl/mirror/CTAN/graphics/pstricks/contrib/pst-eps/pst-eps-doc.pdf
        http://groups.google.fr/group/fr.comp.text.tex/browse_thread/thread/a5c4a67c457c46b8?hl=fr#

    self.file_for_eps is the file in which we will put the LaTeX code needed to create the eps file
    self.input_code_eps
    self.input_code_pdf is the code to be input in the file that contains the picture. This is what replaces the pstricks code in the final figure.
    """
    def __init__(self,pspict):
        self.pspict = pspict
        self.name = self.pspict.name
        self.file_for_eps = Fichier("Picture_%s-for_eps.tex"%(self.name))
        self.file_dvi = Fichier(self.file_for_eps.chemin.replace(".tex",".dvi"))
        self.file_eps = Fichier(self.file_dvi.chemin.replace(".dvi",".eps"))
        self.file_pdf = Fichier(self.file_eps.chemin.replace(".eps",".pdf"))
        self.input_code_eps = "\includegraphics{%s}"%(self.file_eps.nom)
        self.input_code_pdf = "\includegraphics{%s}"%(self.file_pdf.nom)
    def latex_code_for_eps(self):
        code = ["\documentclass{article}\n","\usepackage{pstricks,pst-eucl,pstricks-add}\n","\usepackage{pst-plot}\n","\usepackage{pst-eps}\n","\pagestyle{empty}\n\usepackage{calc}\n"]
        # Allows to add some lines, like packages or macro definitions required. This is useful when one add formulas in the picture
        # that need packages of personal commands.
        code.append(self.pspict.specific_needs)     
        code.extend(["\\begin{document}\n","\\begin{TeXtoEPS}"])
        code.append(self.pspict.contenu_pstricks)
        code.extend(["\end{TeXtoEPS}\n","\end{document}\n"])
        return "".join(code)
    def create_eps_file(self):
        """ Creates an eps file by the chain latex/dvips """
        file_tex = self.file_for_eps
        file_tex.write(self.latex_code_for_eps(),"w")
        commande_e = "latex %s"%self.file_for_eps.chemin
        print "J'execute"
        print commande_e
        os.system(commande_e)
        commande_e = "dvips -E %s -o %s -q"%(self.file_dvi.chemin,self.file_eps.chemin)
        print "J'execute"
        print commande_e
        os.system(commande_e)
    def create_pdf_file(self):
        """ Creates a pdf file by the chain latex/dvips/epstopdf """
        self.create_eps_file()
        commande_e = "epstopdf %s --outfile=%s"%(self.file_eps.chemin,self.file_pdf.chemin)
        print "J'execute"
        print commande_e
        os.system(commande_e)

def add_latex_line_entete(truc,position="ENTETE"):
    truc.add_latex_line("% This file is automatically generated by phystricks",position)
    truc.add_latex_line("% See the documentation ",position)
    truc.add_latex_line("% http://student.ulb.ac.be/~lclaesse/phystricks-doc.pdf ",position)
    truc.add_latex_line("% and the projects phystricks and phystricks-doc at ",position)
    truc.add_latex_line("% http://gitorious.org/~moky\n",position)

def DicoSeparatorToCode(separator_dico):
    """"takes a dictionary of Separator as argument and return the glued code"""
    list_separator = separator_dico.values()
    list_separator.sort()
    a = []
    for sep in list_separator :
        a.append(sep.code())
    return "".join(a)

class Separator(object):
    def __init__(self,title,number):
        self.title = title
        self.number = number
        self.latex_code=[]
        self.add_latex_line("%"+title)
    def add_latex_line(self,line):
        try:
            text=line.code()
        except AttributeError:
            text = "".join(line)        # In some case, the line can in fact be a list of lines.
        self.latex_code.append(text+"\n")
    def code(self):
        return "".join(self.latex_code)
    def __cmp__(self,other):
        if self.number < other.number :
            return -1
        if self.number == other.number :
            raise "Two separators should not have the same number, you're trying to make me crazy."
        if self.number > other.number :
            return 1

class DrawElement(object):
    # The attributes take_xxx are intended to say what we have to take into account in the element.
    # If you put take_graph=False, this element will not be drawn, but its bounding boxes are going to be taken into account.
    def __init__(self,graphe,separator_name,take_graph=True,take_BB=True,take_math_BB=True,*args):
        self.take_graph=take_graph
        self.take_BB=take_BB
        self.take_math_BB=take_math_BB
        self.graph=graphe
        self.separator_name=separator_name
        self.st_args=args

class pspicture(object):
    r"""
    Describe a pspicture

    METHODS:

    - `self.pstricks_code` - contains the pstricks code of what has to be between \begin{pspicture} and \end{pspicture}. This is not the environment itself, neither the definition of xunit, yunit.

    - `self.contenu_pstricks` - is the whole code including the x/yunit. This is in fact a `lazy_attribute`

    - `self.contenu_eps()` - contains the line to be added in order to include the eps file

    EXAMPLES:

    Creating a new pspicture::

        sage: pspict=pspicture("ThisIsMyName")
        sage: pspict.name
        'ThisIsMyName'

    The name of the pspict is used to produce intermediate filesnames, and other names.
    """
    NomPointLibre = PointsNameList()

    def __init__(self,name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS_OR_PDF"):
        r"""
        A name is required for producing intermediate files. This is the case when one wants to produce eps/pdf files of one wants to 
           make interactions with LaTeX (see pspict.get_counter_value).

           self.BB is the bounding box for LaTeX purpose.
            Graph object need to have a method bounding_box
           self.math_BB is the bounding box of objects that are "mathematically relevant". This bounding box does not take into account
            marks of points and thinks like that. This is the bounding box that is going to be used for the axes and the grid.
            When a graph object has a method math_bounding_box, this is the one taken into account in the math_BB here.
        """
        self.name = name        # self.name is used in order to name the intermediate files when one produces the eps file.
        self.mother=None
        self.pstricks_code = []
        self.specific_needs = ""    # See the class PspictureToOtherOutputs
        self.newwriteDone = False
        self.interWriteFile = newwriteName()+".pstricks.aux"
        self.NomPointLibre = PointsNameList()
        self.record_marks=[]
        self.record_bounding_box=[]
        self.record_draw_graph=[]
        self.record_force_math_bounding_box=[]
        #self.record_math_BB=[]
        #self.record_BB=[]
        self.counterDone = False
        self.newlengthDone = False
        self.listePoint = []
        self.xunit = 1
        self.yunit = 1
        self.LabelSep = 1
        self.BB = BoundingBox(Point(1000,1000),Point(-1000,-1000))
        self.math_BB = BoundingBox(Point(1000,1000),Point(-1000,-1000))     # self.BB and self.math_BB serve to add some objects by hand.
                                            # If you need the bounding box, use self.bounding_box()
                                            # or self.math_bounding_box()
        self.axes = Axes( Point(0,0),BoundingBox(Point(1000,1000),Point(-1000,-1000))  )
        self.single_axeX=self.axes.single_axeX
        self.single_axeY=self.axes.single_axeY
        self.grid = Grid(BoundingBox())
        # We add the "anchors" %GRID and %AXES in order to force the axes and the grid to be written at these places.
        #    see the functions DrawAxes and DrawGrid and the fact that they use IncrusteLigne

        # The order of declaration is important, because it is recorded in the Separator.number attribute.
        self.separator_dico = {}            
        self.separator_number = 0
        self.new_separator("ENTETE")
        self.new_separator("BEFORE PSPICTURE")
        self.new_separator("WRITE_AND_LABEL")
        self.new_separator("BEGIN PSPICTURE")
        self.new_separator("GRID")
        self.new_separator("AXES")
        self.new_separator("OTHER STUFF")
        self.new_separator("DEFAULT")
        self.new_separator("AFTER PSPICTURE")

    @lazy_attribute
    def contenu_pstricks(self):                
        r"""
        The LaTeX of `self` including xunit,yunit and \begin{pspicture} ... \end{pspicture}

        This is a lazy_attribute because this has to be used independently at more than one place while this function
        adds non trivial code in `self`.

        NOTE :

        One has to declare the xunit,yunit before to give the bounding box.
        
        The value of LabelSep is the distance between an angle and the lable of the angle. It is by default 1, but if there is a dilatation, the visual effect is bad.
        """
        if self.LabelSep == 1 : 
            self.LabelSep = 2/(self.xunit+self.yunit)
        add_latex_line_entete(self)
        self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+",LabelSep="+str(self.LabelSep)+"}","BEFORE PSPICTURE")
        self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}\n","BEFORE PSPICTURE")
        self.add_latex_line("\\begin{pspicture}%s%s\n"%(self.bounding_box(self).SW().coordinates(numerical=True),self.bounding_box(self).NE().coordinates(numerical=True)),"BEGIN PSPICTURE")
        self.add_latex_line("\end{pspicture}\n","AFTER PSPICTURE")
        self.add_latex_line(self.pstricks_code,"OTHER STUFF")
        return DicoSeparatorToCode(self.separator_dico)

    def default_figure(self,name=None):
        """
        Create and return a Figure object that contains self.

        Example. If pspict is in class pspicture :
        fig=pspict.default_figure
        fig.conclude()
        fig.write_the_file()
        """
        if name == None :
            figname= "DefaultFig"+self.name
        else:
            figname = name
        fig=GenericFigure(figname)
        fig._add_pspicture(self)
        return fig
    def write_the_figure_file(self,name):
        """
        Produce a file that contains self in a default figure.

        To be used if you have a figure at hand and you just want to use it in a figure without particular needs.

        If you want to use the figure outside a figure, use self.write_the_file instead.
        """
        fig=self.default_figure(name+self.name)
        fig.conclude()
        fig.write_the_file()
    def new_separator(self,title):
        self.separator_number = self.separator_number + 1
        self.separator_dico[title]=Separator(title,self.separator_number)
    def initialize_newwrite(self):
        if not self.newwriteDone :
            code = r""" \makeatletter 
                \@ifundefined{%s}           
                {\newwrite{\%s}
                \immediate\openout\%s=%s
                }
                \makeatother"""%(newwriteName(),newwriteName(),newwriteName(),self.interWriteFile)
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.newwriteDone = True
    def initialize_counter(self):
        if not self.counterDone:
            code = r""" \makeatletter 
                \@ifundefined{c@%s}         
                {\newcounter{%s}}
                \makeatother
                """%(counterName(),counterName())           # make LaTeX test if the counter exist before to create it.
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.counterDone = True
    def initialize_newlength(self):
        if not self.newlengthDone :
            code =r"""
            \makeatletter
            \@ifundefined{%s}{\newlength{\%s}}
            \makeatother
            """%(newlengthName(),newlengthName())
            self.add_latex_line(code,"WRITE_AND_LABEL")
            self.newlengthDone = True
    def add_write_line(self,Id,value):
        r"""Writes in the standard auxiliary file \newwrite an identifier and a value separated by a «:»"""
        interWriteName = newwriteName()
        self.initialize_newwrite()
        self.add_latex_line(r"\immediate\write\%s{%s:%s:}"%(interWriteName,Id,value),"WRITE_AND_LABEL")
    def get_Id_value(self,Id,counter_name="NO NAME ?",default_value=0):
        try :
            f=open(self.interWriteFile)
        except IOError :
            print "Warning: the auxiliary file seems not to exist. Compile your LaTeX file."
            return default_value
        text = f.read().replace('\n','').split(":")
        try:
            return text[text.index(Id)+1]           
        except ValueError :
            print "Warning: the auxiliary file does not contain the id «%s». Compile your LaTeX file."%Id
            return default_value
    def get_counter_value(self,counter_name,default_value=0):
        """
        return the value of the (LaTeX) counter <name> at this point of the LaTeX file 

        Makes LaTeX write the value of the counter in an auxiliary file, then reads the value in that file.
        (needs several compilations to work)
        """
        # Make LaTeX write the value of the counter in a specific file
        interCounterId = "counter"+self.name+self.NomPointLibre.next()
        print "J'ai le ID",interCounterId
        self.initialize_counter()
        self.add_write_line(interCounterId,r"\arabic{%s}"%counter_name)
        # Read the file and return the value
        return self.get_Id_value(interCounterId,"counter «%s»"%counter_name,default_value)

    def get_box_dimension(self,tex_expression,dimension_name):
        """
        Return the dimension of the LaTeX box corresponding to the LaTeX expression tex_expression.

        dimension_name is a valid LaTeX macro that can be applied to a LaTeX expression and that return a number. Like
        widthof, depthof, heightof, totalheightof
        """
        interId = dimension_name+self.name+self.NomPointLibre.next()
        self.initialize_newlength()
        self.add_latex_line(r"\setlength{\%s}{\%s{%s}}"%(newlengthName(),dimension_name,tex_expression),"WRITE_AND_LABEL")
        self.add_write_line(interId,r"\the\%s"%newlengthName())
        read_value =  self.get_Id_value(interId,"dimension %s"%dimension_name,default_value="0pt") 
        dimenPT = float(read_value.replace("pt",""))
        return dimenPT/30           # 30 is the conversion factor : 1pt=(1/3)mm
    def get_box_size(self,tex_expression):
        """
        return as 2-uple the dimensions of a LaTeX box containing an expression.

        INPUT:
        - ``tex_expression`` - a valid LaTeX expression.

        OUTPUT:
        - ``width,height`` - the dimensions of the box in centimeter.

        EXAMPLE:
        Type the following  in a script :
        text = "$A_i=\int_a^bf_i$"
        dimx,dimy=pspict.get_box_size(text)
        print "The dimensions of the LaTeX text %s is (%s,%s)"%(text,str(dimx),str(dimy))

        After having LaTeX-compiled the document containing the pspicture, a second
        execution of the script should print :
        The dimensions of the LaTeX text $A_i=\int_a^bf_i$ is (1.66653833333,0.46667)   

        NOTE:
        As far as the problem is concerned from a LaTeX point of view, it was discussed here:
        http://groups.google.fr/group/fr.comp.text.tex/browse_thread/thread/8431f21588b81530?hl=fr

        This functionality creates an intermediate file.
        """
        height = self.get_box_dimension(tex_expression,"totalheightof")
        width = self.get_box_dimension(tex_expression,"widthof")
        return width,height

    def dilatation(self,fact):
        self.dilatation_X(fact)
        self.dilatation_Y(fact)
    def dilatation_X(self,fact):
        self.xunit = self.xunit * fact
    def dilatation_Y(self,fact):
        self.yunit = self.yunit * fact
    def fixe_tailleX(self,l):
        self.dilatation_X(l/self.BB.tailleX())
    def fixe_tailleY(self,l):
        self.dilatation_Y(l/self.BB.tailleY())
    def AddPoint(self,P):
        self.add_latex_line(self.CodeAddPoint(P))
    def bounding_box(self,pspict=None):
        bb=self.BB
        for a in [x.graph.bounding_box(self) for x in self.record_draw_graph if x.take_math_BB or x.take_BB] :
            bb.AddBB(a)
        return bb
    def DrawBB(self):
        self.DrawBoundingBox(self.BB)
    def DrawBoundingBox(self,obj=None,color="cyan"):
        """Draw the bounding box of an object when it has a method bounding_box

        If not, assume that the object is the bounding box to be drawn.
        If no object are given, draw its own bounding box
        """
        if not obj:
            obj=self
        self.record_bounding_box.append(obj)
    #def TraceNuage_de_Points(self,nuage,symbol,params):
    #   self.add_latex_line("% ---------Nuage de point--------")
    #   for P in nuage.listePoints :
    #       self.DrawPoint(P,symbol,params)

    def MarqueAngle(self,A,B,C,label,params):
        self.add_latex_line("\pstMarkAngle["+params+"]{"+A.psName+"}{"+B.psName+"}{"+C.psName+"}{"+label+"}")
    def TraceCourbeParametrique(self,f,mx,Mx,params):
        raise AttributeError,"The method TraceCourbeParametrique is depreciated"
        self.BB.AddParametricCurve(f,mx,Mx)
        self.add_latex_line("\parametricplot[%s]{%s}{%s}{%s}" %(params,str(mx),str(Mx),f.pstricks()))
    def DrawGraphs(self,*args):
        for gr in args:
            try :
                for h in gr:
                    self.DrawGraph(h)
            except TypeError:
                self.DrawGraph(gr)
    def DrawGraph(self,graph,separator_name=None):
        """
        Draw an object of type `GraphOfASomething`.

        More generally, it can draw anything that has the methods

            1. bounding_box
            2. pstricks_code

        The first one should return a bounding box and the second one should return a valid pstricks code as string. 
        If the pstricks code is not valid, LaTeX will get angry but no warning are given here.

        NOTE:

        More precisely, it does not draw the object now, but it add it (and its mark if applicable) to ``self.record_draw_graph``
        which is the list of objects to be drawn. Thus it is still possible to modify the object later (even if discouraged).
        """
        if separator_name==None:
            try :
                separator_name=graph.separator_name
            except AttributeError :
                separator_name="DEFAULT"
        x=DrawElement(graph,separator_name)
        self.record_draw_graph.append(x)
        try :
            if graph.marque:
                x=DrawElement(graph.mark,separator_name)
                self.record_draw_graph.append(x)
        except AttributeError,msg :
            pass            # This happens when the graph has no mark; that is most of the time.
    def DrawGrid(self,grid):
        raise DeprecationWarning,"This is depreciated. The grid has to be drawn with DrawGraph as everyone"
    def TraceTriangle(self,tri,params):
        raise DeprecationWarning, "Method TraceTriangle is depreciated"
        self.BB.AddPoint(tri.A)
        self.BB.AddPoint(tri.B)
        self.BB.AddPoint(tri.C)
        self.add_latex_line("\pstTriangle["+params+",PointSymbol=none]"+tri.A.coordinates(numerical=True)+"{A}"+tri.B.coordinates(numerical=True)+"{B}"+tri.C.coordinates(numerical=True)+"{C}")
    def TraceGrid(self,grille):
        raise DeprecationWarning, "I think TraceGrid should no more be used"
        self.IncrusteLigne(grille.code(self),2)
    def AjusteGrid(self,grille):
        raise DeprecationWarning, "I think AjusteGrid should no more be used"
        grille.BB = self.BB
    def DrawAxes(self,axes):
        raise DeprecationWarning, "This method is depreciated"
    def DrawDefaultAxes(self):
        self.axes.BB = self.math_bounding_box()
        self.axes.BB.AddPoint(Point(0,0))
        epsilonX=float(self.axes.Dx)/2
        epsilonY=float(self.axes.Dy)/2
        self.axes.BB.enlarge_a_little(self.axes.Dx,self.axes.Dy,epsilonX,epsilonY)
        self.axes.update()
        self.DrawGraph(self.axes)
    def DrawDefaultGrid(self):
        self.grid.BB = self.math_bounding_box()
        Dx=self.grid.Dx
        Dy=self.grid.Dy
        epsilonX=0
        epsilonY=0
        self.grid.BB.enlarge_a_little(Dx,Dy,epsilonX,epsilonY)  # Make the grid end on its "big" subdivisions.
        self.DrawGraph(self.grid)
    def add_latex_line(self,ligne,separator_name="DEFAULT"):
        """
        Add a line in the pstricks code. The optional argument <position> is the name of a marker like %GRID, %AXES, ...
        """
        if separator_name==None:
            separator_name="DEFAULT"
        if separator_name=="WRITE_AND_LABEL" and self.mother :
            self.mother.add_latex_line(ligne,separator_name)
        else :
            self.separator_dico[separator_name].add_latex_line(ligne)
    def IncrusteLigne(self,ligne,n):
        raise DeprecationWarning, "The method pspicture.IncrusteLigne() is depreciated."
        self.pstricks_code[n:n]=ligne+"\n"
    def contenu_eps(self):
        to_eps = PspictureToOtherOutputs(self)
        to_eps.create_eps_file()
        return to_eps.input_code_eps
    def contenu_pdf(self):
        to_pdf = PspictureToOtherOutputs(self)
        to_pdf.create_pdf_file()
        return to_pdf.input_code_pdf

    def force_math_bounding_box(self,g):
        """
        Add an object to the math bounding box of the pspicture. This object will not be drawn, but the axes and the grid will take it into account.
        """
        self.record_force_math_bounding_box.append(g)
    def math_bounding_box(self):
        """
        Return the current BoundingBox, that is the BoundingBox of the objects that are currently in the list of objects to be drawn.
        """
        bb = self.math_BB.copy()
        for graphe in [x.graph for x in self.record_draw_graph if x.take_math_BB]:
            try :
                bb.AddBB(graphe.math_bounding_box(self))
            except AttributeError:
                print "Warning: it seems to me that object <%s> (type :%s) has no method math_boundig_box"%(str(graphe),type(graphe))
                bb.append(graphe,self)
        return bb
    def contenu(self):
        """
        Notice that if the option --eps/pdf is given, this method launches some compilations when creating contenu_eps/pdf 
        """
        # Here we are supposed to be sure of the xunit, yunit, so we can compute the BB's needed for the points with marks.
        # For the same reason, all the marks that were asked to be drawn are added now.
        # Most of the difficulty is when the user use pspicture.dilatation_X and Y with different coefficients. TODO : take it into account.
        list_to_be_drawn = [a.graph for a in self.record_draw_graph if a.take_graph]
        for graph in list_to_be_drawn:
            try :
                if graph.draw_bounding_box:
                    bb=graph.bounding_box(self)
                    rect = Rectangle(bb.SW(),bb.NE())
                    rect.parameters.color="cyan"
                    self.DrawGraph(rect)
            except AttributeError :
                pass
        list_to_be_drawn = [a for a in self.record_draw_graph if a.take_graph]
        for x in list_to_be_drawn:
            graph=x.graph
            separator_name=x.separator_name
            try :
                self.BB.append(graph,self)
                self.add_latex_line(graph.pstricks_code(self),separator_name)
            except AttributeError,data:
                if not "pstricks_code" in dir(graph):
                    print "phystricks error : object %s has no pstricks_code method"%(str(graph))
                    raise 
                raise
        for sortie in globals_vars.list_exits:
            if globals_vars.__getattribute__(sortie+"_exit"):
                print "I've to make an exit : %s"%sortie
                return self.__getattribute__("contenu_"+sortie)()
        return self.contenu_pstricks
    # Important de pouvoir produire des fichiers qui ne contiennent qu'une pspicture parce que ça peut être inséré directement 
    # à l'intérieur d'une ligne en LaTeX. J'utilise ça pour des diagrammes de Dynkin par exemple.
    def write_the_file(self,f):                 # Nous sommes dans la classe pspicture
        self.fichier = Fichier(f)
        #self.fichier.open_file("w")
        self.fichier.file.write(self.contenu())
        self.fichier.file.close()

globals_vars = global_variables()
if "--eps" in sys.argv :
    globals_vars.eps_exit = True
if "--pdf" in sys.argv :
    globals_vars.pdf_exit = True
if "--create_tests" in sys.argv :
    globals_vars.test_exit = True
if "--tests" in sys.argv :
    globals_vars.make_tests = True
