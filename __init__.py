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

COMMAND LINE ARGUMENTS:

    - ``--pdf`` - the picture arrives as an \includegraphics of a pdf. It also creates the `pdf` file.

    - ``--eps`` - the picture arrives as an \includegraphics of a eps. It also creates the `eps` file.

    - ``--png`` - the picture arrives as an \includegraphics of a png. It also creates the `png` file.

    - ``--create-png`` - create the png file, but does not change the `.pstricks`
                         file. Thus the LaTeX output will not be modified.
                         
                         See :class:`TestPspictLaTeXCode` and the function :func:`create_png_file`
                         in :class:`PspictureToOtherOutputs`

    NOTE:

    Here we are really speaking about pspicture. There will be one file of one 
    \includegraphics for each pspicture. This is not figure-wise.

    - ``--create_tests`` - create a `tmp` file in which the pspicture is written.

    - ``--tests`` - compares the produced pspicture with the corresponding `tmp` file and
                    raises a ValueError if it does not correspond.
                    If this option is set, nothing is written on the disk.

                    See :class:`TestPspictLaTeXCode`

KNOWN BUGS

    - The figure "Custon units on the Y axe". The distance between the marks and the axe is not correct.

    - The figure "A single axe". The bounding box is too small when compiled with pdflatex.
    
    - The figure "Some points on a parametric curve" is not centred. Idem dans GeomAnal.

    - It is now hard to print the axes over the picture. One difficulty is that the axes of a pspicture
        are computed when the content of the pspicture is known. It is thus nonsense to write something like
        `pspict.DrawGraph(pspict.axes)`

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

def get_line(s,pos):
    """
    return the line containing `s[pos]`

    INPUT:

    - ``s`` - a srting.

    - ``pos`` - integer.

    EXAMPLES:

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
        justification="There is a difference ouside a number\nExpected:\n%s\nGot:\n %s"%(line2,line1)
        return False,justification
    if abs(SR(v1)-SR(v2))<epsilon:
        justification=last_justification+"d(%s,%s)=%s\n"%(v1,v2,str(SR(v1)-SR(v2)))
        t1=s1[:first1]+v2+s1[last1:]
        t2=s2
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

        If the option `--create-tests` is passed to the program, this function is called
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
    """
    Some global variables

    - ``create_formats`` - dictionary which says the exit files we want to produce. These can be

                    * eps,pdf,pfd : I think that these names are self-explaining.

                    * test : outputs a `tmp` file 

    - ``exit_format`` - the format one wants to use in the LaTeX file. By default it is pstricks.

    - ``perform_tests`` - (default=False) If True, perform the tests. 

    The difference between `create_formats` and `exit_format` is that `create_format` says 
    what files are going to be _produced_ while `exit_format` is the format that LaTeX will see.

    Notice that `create_formats` is a plural while `exit_format` is a singlular. This is 
    not a joke ;)
    """
    def __init__(self):
        self.create_formats={"eps":False,"pdf":False,"png":False,"test":False}
        self.exit_format="pstricks"
        self.perform_tests = False
    def special_exit(self):
        for sortie in self.create_formats.values():
            if sortie:
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
    """ Return the tuple of pspicture and figure that one needs in 90% of the cases. """
    fig = GenericFigure(name)
    pspict=fig.new_pspicture(name)
    return pspict,fig

def MultiplePictures(name,n):
    r"""
    return a figure with multiple subfigures. This is the other 10% of cases.

    INPUT:

    - `name` - the name of the figure.

    - `n` - the number of subfigures.

    You have to think about naming the subfigures.

    EXAMPLE::

        sage: pspict,fig = MultiplePictures("MyName",3)
        The result is on figure \ref{LabelFigMyName}.                                                                                                                                                             
        \newcommand{\CaptionFigMyName}{<+Type your caption here+>}                                                                                                                                                
        \input{Fig_MyName.pstricks}                                                                                                                                                                               
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName0}                                                                                                                                           
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName1}                                                                                                                                           
        See also the subfigure \ref{LabelFigMyNamessLabelSubFigMyName2}
        sage: pspict[0].mother.caption="My first subfigure"
        sage: pspict[1].mother.caption="My second subfigure"
        sage: pspict[2].mother.caption="My third subfigure"

    Notice that a caption is related to a figure or a subfigure, not to a pspicture.
    """
    fig = GenericFigure(name)
    pspict=[]
    for i in range(n):
        subfigure=fig.new_subfigure("name"+str(i),"LabelSubFig"+name+str(i))
        picture=subfigure.new_pspicture(name+"pspict"+str(i))
        pspict.append(picture)
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
        self.separator_list=SeparatorList()
        self.separator_list.new_separator("ENTETE FIGURE")
        self.separator_list.new_separator("WRITE_AND_LABEL")
        self.separator_list.new_separator("BEFORE SUBFIGURES")
        self.separator_list.new_separator("SUBFIGURES")
        self.separator_list.new_separator("AFTER SUBFIGURES")
        self.separator_list.new_separator("DEFAULT")
        self.separator_list.new_separator("BEFORE PSPICTURE")
        self.separator_list.new_separator("PSPICTURE")
        self.separator_list.new_separator("AFTER PSPICTURE")
        self.separator_list.new_separator("AFTER ALL")
        add_latex_line_entete(self)

        self.add_latex_line("\\begin{figure}[ht]","BEFORE SUBFIGURES")
        self.add_latex_line("\centering","BEFORE SUBFIGURES")
    def new_separator(self,title):
        raise DeprecationWarning
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
        self.separator_list[separator_name].add_latex_line(ligne)
    def IncrusteLigne(self,ligne,n):
        print "The method picture.IncrusteLigne() is depreciated."
        self.code[n:n]=ligne+"\n"
    def AjouteCode(self,liste_code):
        self.code.extend(liste_code)
    def conclude(self):
        for pspict in self.record_pspicture :
            # What has to be written in the WRITE_AND_LABEL part of the picture is written now
            self.add_latex_line(pspict.separator_list["WRITE_AND_LABEL"].latex_code,"WRITE_AND_LABEL")
            pspict.separator_list["WRITE_AND_LABEL"].latex_code=[]
            self.add_latex_line(pspict.contenu(),"PSPICTURE")           # Here, what is added depends on --eps, --pdf, --png and so on.
            if global_vars.perform_tests:
                TestPspictLaTeXCode(pspict).test()
        if not global_vars.special_exit() :
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
        self.contenu = self.separator_list.code()
    def write_the_file(self):
        """
        Write the figure in the file.

        Does not write if we are testing.
        """
        to_be_written=self.contenu
        if not global_vars.perform_tests :
            self.fichier.open_file("w")
            self.fichier.file.write(to_be_written)
            self.fichier.file.close()
            
# Le \subfigure[caption]{ ne se met pas dans le code de la classe subfigure parce que dans la classe figure, je numérote les sous-figures.
# Typiquement, une sousfigure sera juste créée en ajoutant une pspicture d'un coup, et puis c'est tout.
class subfigure(object):
    """
    This is a subfigure.

    If no label are given, a default one will be set when included in the figure.
    
    EXAMPLES

    .. literalinclude:: phystricksSubFigure.py
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigFirstPICTFirstPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigSecondPICTSecondPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigThirdPICTthirdPoint-for_eps.png
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
        self.file_png = Fichier(self.file_eps.chemin.replace(".eps",".png"))
        self.input_code_eps = "\includegraphics{%s}"%(self.file_eps.nom)
        self.input_code_pdf = "\includegraphics{%s}"%(self.file_pdf.nom)
        self.input_code_png = "\includegraphics{%s}"%(self.file_png.nom)
    def latex_code_for_eps(self):
        code = ["\documentclass{article}\n","\usepackage{pstricks,pst-eucl,pstricks-add}\n","\usepackage{pst-plot}\n","\usepackage{pst-eps}\n","\pagestyle{empty}\n\usepackage{calc}\n"]
        # Allows to add some lines, like packages or macro definitions required. This is useful when one add formulas in the picture
        # that need packages of personal commands.
        code.append(self.pspict.specific_needs)     
        code.extend(["\\begin{document}\n","\\begin{TeXtoEPS}"])
        code.append(self.pspict.contenu_pstricks)
        code.extend(["\end{TeXtoEPS}\n","\end{document}\n"])
        return "".join(code)
    def create_test_file(self):
        TestPspictLaTeXCode(self.pspict).create_test_file()
    def create_eps_file(self):
        """ Create an eps file by the chain latex/dvips """
        file_tex = self.file_for_eps
        file_tex.write(self.latex_code_for_eps(),"w")
        commande_e = "latex %s"%self.file_for_eps.chemin
        print commande_e
        os.system(commande_e)
        commande_e = "dvips -E %s -o %s -q"%(self.file_dvi.chemin,self.file_eps.chemin)
        print commande_e
        os.system(commande_e)
    def create_png_file(self):
        """
        Creates a png file by the chain latex->eps->png

        The last step is done by convert.

        NOTE :

        It is also possible to use inkscape in order to produce svg but
        on my computer inkscape crashes on a segmentation fault
        when launched from a script :(
        """
        # TODO: check if inkscape is present. If not use convert. If convert
        # is not present, prendi la f-parola.
        self.create_eps_file()
        x_cmsize=100*numerical_approx(self.pspict.bounding_box().xsize()*self.pspict.xunit)
        y_cmsize=100*numerical_approx(self.pspict.bounding_box().ysize()*self.pspict.yunit)
        commande_e = "convert -density 1000 %s -resize %sx%s %s"%(self.file_eps.chemin,str(x_cmsize),str(y_cmsize),self.file_png.chemin)
        #commande_e = "inkscape -f %s -e %s -D -d 600"%(self.file_pdf.chemin,self.file_png.chemin)
        #inkscape -f test.pdf -l test.svg
        print commande_e
        os.system(commande_e)
    def create_pdf_file(self):
        """ Creates a pdf file by the chain latex/dvips/epstopdf """
        self.create_eps_file()
        commande_e = "epstopdf %s --outfile=%s"%(self.file_eps.chemin,self.file_pdf.chemin)
        print commande_e
        os.system(commande_e)

def add_latex_line_entete(truc,position=""):
    if position == "" :
        if isinstance(truc,pspicture):
            position="ENTETE PSPICTURE"
        if isinstance(truc,figure):
            position="ENTETE FIGURE"
    truc.add_latex_line("% This file is automatically generated by phystricks",position)
    truc.add_latex_line("% See the documentation ",position)
    truc.add_latex_line("% http://student.ulb.ac.be/~lclaesse/phystricks-doc.pdf ",position)
    truc.add_latex_line("% http://student.ulb.ac.be/~lclaesse/phystricks-documentation/_build/html/index.html ",position)
    truc.add_latex_line("% and the projects phystricks and phystricks-doc at ",position)
    truc.add_latex_line("% http://gitorious.org/~moky\n",position)

def DicoSeparatorToCode(separator_dico):
    raise DeprecationWarning,"Everything should use SeparatorList"
    """"takes a dictionary of Separator as argument and return the glued code"""
    list_separator = separator_dico.values()
    list_separator.sort()
    a = []
    for sep in list_separator :
        a.append(sep.code())
    return "".join(a)

class SeparatorList(object):
    """
    represent a dictionary of :class:`Separator`
    """
    def __init__(self):
        self.separator_list=[]
    def title_list(self):
        return [x.title for x in self.separator_list]
    def new_separator(self,title,number=None):
        for separator in self.separator_list :
            if separator.title == title :
                raise ValueError, "A new separator cannot have the same title as an old one: %s"%title
        separator=Separator(title)
        if number:
            self.separator_list.insert(number,separator)
        else:
            self.separator_list.append(separator)
    def code(self):
        return "".join(separator.code() for separator in self.separator_list)
    def fusion(self,title_list,new_title):
        """
        Remove of the list the separators whose names are in the `title_list`
        and add a new separator with the fusion code at the place
        where the *first* one was.

        INPUT :

        - ``title_list`` - a list of `str` that are name of separators
                           supposed to be part of `self.separator_list`

        - ``new_title`` - the title of the new separator that will be
                            created.

        Schematically,

        "ONE": "first code"
        "TWO": "second code"
        "THREE": "third code"
        "FOUR": "fourth code"

        If one fusion the second and third with the name "NEW", we get

        "ONE": "first code"
        "NEW" : "second code third code"
        "FOUR": "fourth code"

        NOTE:

        It respect the order. So if the `title_list` comes in the order `["THREE","TWO"]`, it first orders
        the list to `["TWO","THREE"]`

        """

        # One has to remove duplicates. If not the LaTeX code
        # will be written more than once.
        short_list=[]
        for title in title_list:
            if title not in short_list:
                short_list.append(title)

        # On has to sort the list in order the code to appear in
        # the right order. As an example, we want the axes first.
        # The order to be respected is basically the one furnished in
        # __init__ of pspicture and figure.
        short_list.sort(lambda x,y:(self.title_list().index(x)-self.title_list().index(y)))

        new_code=""
        new_place=len(self.separator_list)
        concerned_separators=[]
        for title in short_list:
            separator=self[title]
            concerned_separators.append(separator)
            new_code=new_code+separator.code()
            new_place=min(new_place,self.separator_list.index(separator))

        self.new_separator(new_title,new_place)
        self[new_title].add_latex_line(new_code)
        for sep in concerned_separators:
            self.separator_list.remove(sep)
        
    def __getitem__(self,i):
        """
        One can call a separator by its title or its number.
        """
        if isinstance(i,str):
            for separator in self.separator_list :
                if separator.title == i :
                    return separator
            raise IndexError,"No separator with title %s"%i
        return self.separator_list[i]

class Separator(object):
    def __init__(self,title):
        self.title = title
        self.latex_code=[]
        self.add_latex_line("%"+self.title)
    def add_latex_line(self,line):
        if isinstance(line,Separator):
            text=line.code()
        else :
            text = "".join(line)        # Notice that "".join(x) also works when x is a string.
        self.latex_code.append(text+"\n")
    def code(self):
        return "".join(self.latex_code)

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

    - `self.pstricks_code()` - contains the pstricks code of what has to be between \begin{pspicture} and \end{pspicture}. This is not the environment itself, neither the definition of xunit, yunit.

    - `self.contenu_pstricks` - is the whole code including the x/yunit and \begin{pspicture}...\end{pspicture}.
                                This is in fact a `lazy_attribute`. 
                                
                                This has not to be used for creating other outputs than pure pstricks.
                               
    - `self.latex_code_for_eps()` - the LaTeX code that produces the eps file. This function calls `self.contenu_pstricks`

    - `self.latex_code_for_png()` - the same.

    - `self.latex_code_for_contenu_pdf()` - the same.

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
        self.pstricks_code_list = []
        self.specific_needs = ""    # See the class PspictureToOtherOutputs
        self.newwriteDone = False
        #self.interWriteFile = newwriteName()+".pstricks.aux"
        self.interWriteFile = "phystricks.aux"
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
        self.separator_list = SeparatorList()
        self.separator_list.new_separator("ENTETE PSPICTURE")
        self.separator_list.new_separator("BEFORE PSPICTURE")
        self.separator_list.new_separator("WRITE_AND_LABEL")
        self.separator_list.new_separator("BEGIN PSPICTURE")        # This separator is supposed to contain only \begin{pspicture}
        self.separator_list.new_separator("GRID")
        self.separator_list.new_separator("AXES")
        self.separator_list.new_separator("OTHER STUFF")
        self.separator_list.new_separator("DEFAULT")
        self.separator_list.new_separator("END PSPICTURE")
        self.separator_list.new_separator("AFTER PSPICTURE")

    @lazy_attribute
    def contenu_pstricks(self):                
        r"""
        The LaTeX of `self` including xunit,yunit and \begin{pspicture} ... \end{pspicture}

        This is a `lazy_attribute` because it has to be used more than once while it adds non
        trivial code to `self`.

        NOTE :

        One has to declare the xunit,yunit before to give the bounding box.
        
        The value of LabelSep is the distance between an angle and the lable of the angle. It is by default 1, but if there is a dilatation, the visual effect is bad.
        """
        self.create_pstricks_code
        if self.LabelSep == 1 : 
            self.LabelSep = 2/(self.xunit+self.yunit)
        add_latex_line_entete(self)
        self.add_latex_line("\psset{xunit="+str(self.xunit)+",yunit="+str(self.yunit)+",LabelSep="+str(self.LabelSep)+"}","BEFORE PSPICTURE")
        self.add_latex_line("\psset{PointSymbol=none,PointName=none,algebraic=true}\n","BEFORE PSPICTURE")
        self.add_latex_line("\\begin{pspicture}%s%s\n"%(self.bounding_box(self).SW().coordinates(numerical=True),self.bounding_box(self).NE().coordinates(numerical=True)),"BEGIN PSPICTURE")
        self.add_latex_line("\end{pspicture}\n","END PSPICTURE")
        self.add_latex_line(self.pstricks_code_list,"OTHER STUFF")
        return self.separator_list.code()

    @lazy_attribute
    def create_pstricks_code(self):
        """
        Fix the bounding box and create the separator "PSTRICKS CODE"

        This function is not supposed to be used twice. In fact, this is 
        supposed to be called only from `lazy_attributes`
        """
        # Here we are supposed to be  sure of the xunit, yunit, so we can compute the BB's needed for the points with marks.
        # For the same reason, all the marks that were asked to be drawn are added now.
        # Most of the difficulty is when the user use pspicture.dilatation_X and Y with different coefficients.
        # TODO : take it into account.

        # Creating the bounding box
        list_to_be_drawn = [a.graph for a in self.record_draw_graph if a.take_graph]
        for graph in list_to_be_drawn:
            try :
                if graph.draw_bounding_box:
                    raise AttributeError,"I don't think that the attribute `draw_bounding_box` still exists"
                    # It seems to me that we can safely remove all this part. March, 29, 2011.
                    bb=graph.bounding_box(self)
                    rect = Rectangle(bb.SW(),bb.NE())
                    rect.parameters.color="cyan"
                    self.DrawGraph(rect)
            except AttributeError :
                pass

        list_to_be_drawn = [a for a in self.record_draw_graph if a.take_graph]

        # Produce the code in the sense that if writes everything in the separators.
        list_used_separators=[]
        for x in list_to_be_drawn:
            graph=x.graph

            # If the graph is a bounding box of a mark, we recompute it
            # because a dilatation of the figure could have
            # changed the bounding box.
            if isinstance(graph,BoundingBox):
                if graph.parent:
                    if isinstance(graph.parent,Mark):
                        graph=graph.parent.bounding_box(self)

            # If the graph is a mark, then one has to recompute
            # its position because of possible xunit,yunit.
            #if isinstance(graph,Mark):
            #    print "1651 central point",graph.central
            #    if graph.parent:
            #        graph = Mark(graph.parent,graph.dist,graph.angle,graph.text,graph.automatic_place)

            separator_name=x.separator_name
            try :
                self.BB.append(graph,self)
                self.add_latex_line(graph.pstricks_code(self),separator_name)
                list_used_separators.append(separator_name)
            except AttributeError,data:
                if not "pstricks_code" in dir(graph):
                    print "phystricks error: object %s has no pstricks_code method"%(str(graph))
                raise
        self.separator_list.fusion(list_used_separators,"PSTRICKS CODE")

    @lazy_attribute
    def pstricks_code(self):
        r"""
        Return the pstricks code that has to appears between \begin{pspicture} and \end{pspicture}.

        This is a lazy_attribute and perform non trivial task changing the state
        of many other attributes of `self`.
        Among other it changes the bounding box.

        This is called by :func:`contenu_pstricks`
        """
        self.create_pstricks_code
        return self.separator_list["PSTRICKS CODE"].code()

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
        raise DeprecationWarning
        self.separator_number = self.separator_number + 1
        self.separator_dico[title]=Separator(title,self.separator_number)
    def initialize_newwrite(self):
        if not self.newwriteDone :
            code = r""" \makeatletter 
                \@ifundefined{%s}           
                {\newwrite{\%s}
                }
                \makeatother"""%(newwriteName(),newwriteName())
                # I was adding the following line in the \@ifundefined :
                # \immediate\openout\%s=%s
                # Thus I had that more in the string formating :
                # newwriteName(),self.interWriteFile)
            self.add_latex_line(code,"WRITE_AND_LABEL")
            code = r"""\makeatletter
                \@ifundefined{phystricksAppendToFile}{
                \newcommand{\phystricksAppendToFile}[1]{
                \CatchFileDef \phystricksContent {%s}{}
                \immediate\openout\%s=%s
                \immediate\write\%s{\phystricksContent}
                \immediate\write\%s{#1}
                \immediate\closeout\%s
                }
                }
                \makeatother"""%(self.interWriteFile,newwriteName(),self.interWriteFile,newwriteName(),newwriteName(),newwriteName())
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
        #self.add_latex_line(r"\immediate\write\%s{%s:%s:}"%(interWriteName,Id,value),"WRITE_AND_LABEL")
        self.add_latex_line(r"\phystricksAppendToFile{%s:%s-}"%(Id,value),"WRITE_AND_LABEL")

    @lazy_attribute
    def id_values_dict(self):
        """
        Build the dictionary of stored values in the auxiliary file
        and rewrite that file.
        """
        d={}
        try :
            f=open(self.interWriteFile,"r")
        except IOError :
            print "Warning: the auxiliary file seems not to exist. Compile your LaTeX file."
            return d
        idlist = f.read().replace('\n','').replace(' ','').replace('\\par','').split("-")
        f.close()

        for els in idlist[0:-1]:
            key=els.split(":")[0]
            value=els.split(':')[1]
            d[key]=value

        f=open(self.interWriteFile,"w")
        for k in d.keys():
            f.write("%s:%s-"%(k,d[k]))
        f.close()
        return d

    def get_Id_value(self,Id,counter_name="NO NAME ?",default_value=0):
            if Id not in self.id_values_dict.keys():
                print "Warning: the auxiliary file does not contain the id «%s». Compile your LaTeX file."%Id
                return default_value
            return self.id_values_dict[Id]
    def get_counter_value(self,counter_name,default_value=0):
        """
        return the value of the (LaTeX) counter <name> at this point of the LaTeX file 

        Makes LaTeX write the value of the counter in an auxiliary file, then reads the value in that file.
        (needs several compilations to work)
        """
        # Make LaTeX write the value of the counter in a specific file
        interCounterId = "counter"+self.name+self.NomPointLibre.next()
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
            self.separator_list[separator_name].add_latex_line(ligne)
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
    def contenu(self):              # pspicture
        r"""
        return the LaTeX code of the pspicture
        
        Also creates the files corresponding to the `exit_format`.

        This is of the form \begin{pspicture} ... \end{pspicture} if
        the global variable `exit_format` is "pstricks".

        In the other cases, this is \includegraphics{...}.
        """
        to_other = PspictureToOtherOutputs(self)
        create_dico=global_vars.create_formats
        # Create files for the requested formats, including tests
        for k in create_dico.keys():
            if create_dico[k] :
                to_other.__getattribute__("create_%s_file"%k)()
        # return the LaTeX code of self
        if global_vars.exit_format=="pstricks":
            return self.contenu_pstricks
        return to_other.__getattribute__("input_code_"+global_vars.exit_format)

    def write_the_file(self,f):             
        """
        Writes the LaTeX code of the pspict.

        This function is almost never used because most of time we want to pspicture
        to be included in a figure.
        """
        self.fichier = Fichier(f)
        self.fichier.file.write(self.contenu())
        self.fichier.file.close()

global_vars = global_variables()
if "--eps" in sys.argv :
    global_vars.exit_format="eps"
    global_vars.create_formats["eps"] = True
if "--png" in sys.argv :
    global_vars.exit_format="png"
    global_vars.create_formats["png"] = True
if "--pdf" in sys.argv :
    global_vars.exit_format="pdf"
    global_vars.create_formats["pdf"] = True
if "--create-png" in sys.argv :
    global_vars.create_formats["png"] = True
if "--create-pdf" in sys.argv :
    global_vars.create_formats["pdf"] = True
if "--create-eps" in sys.argv :
    global_vars.create_formats["eps"] = True
if "--create-tests" in sys.argv :
    global_vars.create_formats["test"] = True
if "--tests" in sys.argv :
    global_vars.perform_tests = True
