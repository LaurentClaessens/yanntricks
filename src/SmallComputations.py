###########################################################################
#   This is part of the module yanntricks
#
#   yanntricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   yanntricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with yanntricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2010,2011,2013-2015,2017, 2019
# email: laurent@claessens-donadello.eu

"""
This submodule contains some auxiliary computations that have to be performed 
by yanntricks but that are not geometry.
"""

import os

from sage.all import find_root, floor, ceil, solve, numerical_approx, pi
from sage.all import SR, cos, atan, tan
import codecs


def MultipleBetween(Dx, mx, Mx, mark_origin=True):
    """
    Return the list of values that are all the integer multiple of Dx between mx and Mx.

    If <mark_origin> is True, the list includes 0 if applicable.
    """
    ni = ceil(float(mx)/Dx)
    nf = floor(float(Mx)/Dx)
    l = [i*Dx for i in range(ni, nf+1)]
    if not mark_origin:
        try:
            l.remove(0)
        except ValueError:
            pass
    return l


def SubGridArray(mx, Mx, Dx, num_subX):
    """ Provides the values between mx and Mx such that there are num_subX-1 numbers between two integer separated by Dx """
    dx = float(Dx)/num_subX
    valeurs = []
    base = MultipleLower(mx, Dx)
    # The range is designed by purpose to be sure to be too wide
    for i in range(0, ceil((Mx-mx)*num_subX/Dx)+3*num_subX):
        tentative = base + float(i)*dx
        if (tentative < Mx) and (tentative > mx) and (i % num_subX != 0):
            valeurs.append(tentative)
    return valeurs


def MainGridArray(mx, Mx, Dx):
    """
    Return the list of number that are
    1. integer multiple of Dx
    2. between mx and Mx

    If mx=-1.4 and Dx=0.5, the first element of the list will be -1
    If mx=-1.5 and Dx=0.5, the first element of the list will be -1.5
    If mx=0 and Dx=1, the first element of the list will be 0.
    """
    m = mx/Dx
    if not m.is_integer():
        m = floor(mx/Dx - 1)
    M = Mx/Dx
    if not M.is_integer():
        M = ceil(Mx/Dx + 1)
    a = []
    # These two lines are cancelling all the previous ones.
    m = floor(mx/Dx - 1)
    M = ceil(Mx/Dx + 1)
    for i in range(m, M):
        tentative = i*Dx
        if (tentative >= mx) and (tentative <= Mx):
            a.append(tentative)
    return a


class CalculSage(object):
    # I cannot merge the function for solving with respect to one or more variables because Sage returns like that:
    # If 1 and 2 are the solutions for one variable : [x == 1,x==2]
    # If (1,2) and (3,4) are solutions of a two variable equation : [ [x==1,y==2],[x==3,y==4] ]
    # The list nesting structure is different. Do I have to read the doc ?
    def solve_one_var(self, eqs, var):
        """
        Solve the equations with respect to the given variable

        Returns a list of numerical values.
        """
        liste = solve(eqs, var, explicit_solutions=True)
        a = []
        for soluce in liste:
            a.append(numerical_approx(soluce.rhs()))
        return a

    def solve_more_vars(self, eqs, *vars):
        """
        Solve the equations with respect to the given variables

        Returns a list like [  [1,2],[3,4] ] if the solutions are (1,2) and (3,4)
        """
        liste = solve(eqs, vars, explicit_solutions=True)
        a = []
        for soluce in liste:
            sol = []
            for variable in soluce:
                sol.append(numerical_approx(variable.rhs()))
            a.append(sol)
        return a

# TODO : this class should not exist.


class Fichier(object):
    def __init__(self, filename):
        self.NomComplet = filename
        self.chemin = self.NomComplet
        self.nom = os.path.basename(self.chemin)
        self.filename = filename

    def open_file(self, opt):
        self.file = codecs.open(self.chemin, encoding="utf8", mode=opt)

    def close_file(self):
        self.file.close()

    def write(self, texte, opt):
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


def RemoveLastZeros(x, n):
    """
    Cut the number `x` to n decimals and then remove the last zeros.

    If there remain no decimals, also remove the dot.
    We only cut a given number of decimals; if the integer part has more digits, we keep them.

    The output is a string, not a number.

    INPUT:

    - ``x`` - a number.

    - ``n`` - the number of decimals we want to keep.

    OUTPUT:
    A string.

    EXAMPLES::

        sage: from yanntricks.SmallComputations import *
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
    s = "%.15f" % x
    t = s[:s.find(".")+n+1]
    k = len(t)-1
    while t[k] == "0":
        k = k-1
    u = t[:k+1]
    if u[-1] == ".":
        return u[:-1]
    return u


def number_at_position(s, n):
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

        sage: from yanntricks.SmallComputations import *
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
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    number_elements = digits+["-", "."]
    s = str(s)
    if s[n] not in number_elements:
        return False, 0, 0
    i = n
    while s[i] in number_elements:
        i = i-1
    first = i+1
    i = n
    while s[i] in number_elements:
        i = i+1
    last = i
    # When treating the string read in the test file,
    # the string is an unicode. SR does not work with unicode
    return str(s[first:last]), first, last


def get_line(s, pos):
    r"""
    return the line containing `s[pos]`

    INPUT:

    - ``s`` - a srting.

    - ``pos`` - integer.

    EXAMPLES::

        sage: from yanntricks.SmallComputations import *
        sage: s="Hello\n how do you do ? \n See you"
        sage: print get_line(s,10)
        how do you do ?

    """
    a = s.rfind("\n", 0, pos)
    b = s.find("\n", pos, len(s))
    return s[a+1:b]


def string_number_comparison(s1, s2, epsilon=0.01, last_justification=""):
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

        sage: from yanntricks.SmallComputations import *
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
        return True, last_justification
    pos = 0
    while s1[pos] == s2[pos]:
        pos = pos+1
    v1, first1, last1 = number_at_position(s1, pos)
    v2, first2, last2 = number_at_position(s2, pos)

    if v1 == False or v2 == False:
        line1 = get_line(s1, pos)
        line2 = get_line(s2, pos)
        justification = "There is a difference outside a number\nExpected:\n%s\nGot:\n %s" % (
            line2, line1)
        return False, justification
    if abs(SR(v1)-SR(v2)) < epsilon:
        justification = last_justification + \
            "d(%s,%s)=%s\n" % (v1, v2, str(SR(v1)-SR(v2)))
        t1 = s1[:first1]+v2+s1[last1:]
        t2 = s2
        return string_number_comparison(t1, t2, epsilon=epsilon, last_justification=justification)
    justification = last_justification + \
        "Distance between %s and %s is larger than %s." % (
            str(v1), str(v2), str(epsilon))
    return False, justification


def around(x, decimals):
    """
    return `x` truncated after a certain number of decimals.

    INPUT:

        - ``x`` - a number
        - ``deciamsl`` - integer

        OUTPUT:

        A number.

        EXAMPLES::

            sage: from yanntricks.SmallComputations import *
            sage: around(100.6867867,3)
            100.687

    """
    from numpy import around as numpy_around
    a = [x]
    return numpy_around(a, decimals=decimals)[0]


def MultipleLower(x, m):
    """ return the biggest multiple of m which is lower or equal to x"""
    return floor(x/m)*m


def MultipleBigger(x, m):
    """
    Return the lower multiple of m which is bigger or equal to x

    EXAMPLES ::

        sage: from yanntricks.SmallComputations import *
        sage: MultipleBigger(11.0,2)
        12
    """
    return ceil(x/m)*m


def visualPolarCoordinates(r, theta, xunit=1, yunit=1):
    """
    return the polar coordinated that you have to give
    in such a way the it *visually* appears `(r,theta)`
    when `xunit` and `yunit` are given.

    The input and output angles are in radian.

    INPUT:

    - ``r`` - the distance you want to see.

    - ``theta`` - the angle you want to see (radian or AngleMeasure).
                    If the angle is passed as 'AngleMeasure', the answer
                    will also be AngleMeasure

    - ``xunit`` - the dilatation factor in the `x` direction.

    - ``yunit`` - the dilatation factor in the `y` direction.

    OUTPUT:

    a tuple `(distance,angle)`

    EXAMPLES::

        sage: from yanntricks.SmallComputations import *
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
    from MathStructures import AngleMeasure

    arg_is_angle_measure = False
    orig_theta = theta
    if isinstance(theta, AngleMeasure):
        theta = numerical_approx(theta.radian)
        arg_is_angle_measure = True
    else:
        theta = numerical_approx(theta)

    if cos(theta) == 0:
        return (r/yunit, orig_theta)
    if cos(theta) == 1:
        return (r/xunit, orig_theta)
    if cos(theta) == -1:
        return (r/xunit, orig_theta)

    # For Sage, atan : R -> [-pi/2,pi/2]
    # thus one has to check the angle after having done atan( ... tan(...)  )
    # Here we assume that the deformed angle is next to the original one
    if xunit == yunit:
        alpha = theta
    else:
        alpha = atan((xunit/yunit)*tan(theta))
        if theta > pi/2 and theta < 3*pi/2:
            alpha = alpha+pi

    rp = (r/xunit)*(cos(theta)/cos(alpha))

    if rp < 0:
        rp = -rp
        alpha = alpha+pi
    if arg_is_angle_measure:
        alpha = AngleMeasure(value_radian=alpha)
    return (rp, alpha)


def split_list(starting_list, fun, cut_ymin, cut_ymax):
    ldel = []
    l = []
    for i, k in enumerate(starting_list):
        try:
            on = fun(k) > cut_ymin and fun(k) < cut_ymax
        except ValueError:      # Happens when 1/x and x=0.
            on = False
        if on:
            l.append(k)
        else:
            ldel.append(l)
            l = []
    ldel.append(l)
    while [] in ldel:
        ldel.remove([])
    s = [(l[0], l[-1]) for l in ldel]
    return s


def find_roots_recursive(f, a, b, tol=0.000000000001):
    """
    Return the roots of the function 'f' between 'a' and 'b' as a list.

    We assume two roots are always separated by more than `tol`.

    The list is sorted.
    """
    # The method was proposed by ndomes in http://ask.sagemath.org/question/8886/obtaining-all-numerical-roots-of-a-function-in-an-interval/
    L = []
    try:
        x0 = find_root(f, a, b)
    except RuntimeError:
        return []
    L.append(x0)
    L += find_roots_recursive(f, a, x0-tol, tol)
    L += find_roots_recursive(f, x0+tol, b, tol)
    L.sort()
    return L
