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

# copyright (c) Laurent Claessens, 2010,2011,2013-2017, 2019
# email: laurent@claessens-donadello.eu

from sage.all import numerical_approx, SR, pi


class AngleMeasure(object):
    """
    Describe an angle.

    This class is an attempt to abstract the degree/radian problem.

    EXAMPLES::

        sage: from yanntricks.SmallComputations import *
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

    If the numerical approximation of an angle in degree is
    close to an integer up to less than 1e-10, we round it.
    The reason is that in some case I got as entry such a number : 
    -(3.47548077273962e-14)/pi + 360
    Then the computation of radian gave 0 and we are left with degree 
    around 359.9999 while the radian was rounded to 0.
    (June, 2, 2013)

    sage: a=AngleMeasure(value_degree=-(3.47548077273962e-14)/pi + 360)
    sage: a.degree
    360
    sage: a.radian
    2*pi
    """
    # TODO : take into account the following thread:
    # http://ask.sagemath.org/question/332/add-a-personnal-coercion-rule

    def __init__(self, angle_measure=None, value_degree=None, value_radian=None, keep_negative=False):
        from yanntricks.src.polar_coordinates import PolarCoordinates
        from yanntricks.src.degree_unit import degree
        from yanntricks.src.radian_unit import radian

        given_value_degree = value_degree
        given_value_radian = value_radian

        for k in [value_degree, value_radian]:
            if isinstance(k, AngleMeasure):
                angle_measure = k
                value_degree = None
                value_radian = None
        for k in [value_degree, value_radian]:
            if isinstance(k, PolarCoordinates):
                angle_measure = k
                value_degree = None
                value_radian = None
        if angle_measure:
            value_degree = angle_measure.degree
            value_radian = angle_measure.radian
        else:

            if value_degree is not None:
                # If the fractional part of the given degree is too small,
                # we round it.

                # We have to test is 'value_degree' is None because
                # `numerical_approx(None)` is the complex number 0.00000

                s = numerical_approx(value_degree)

                k = abs(s).frac()
                if k < 0.000001:
                    value_degree = s.integer_part()

            if value_degree is not None:
                value_radian = radian(value_degree, keep_max=True)
                if keep_negative and value_degree < 0 and value_radian > 0:
                    print("This is strange ...")
                    value_radian = value_radian-2*pi
            if value_degree == None:
                value_degree = degree(value_radian, keep_max=True)
                if keep_negative and value_radian < 0 and value_degree > 0:
                    print("This is strange ...")
                    value_degree = value_degree-360

        # From here 'value_degree' and 'value_radian' are fixed and
        # we perform some checks.

        self.degree = value_degree
        self.radian = value_radian

        if self.degree > 359 and self.radian < 0.1:
            print("Problem with an angle : ", self.degree, self.radian)
            print("dep degree", given_value_degree, numerical_approx(
                given_value_degree))
            print("dep_radian", given_value_radian, numerical_approx(
                given_value_radian))
            print("final degree", numerical_approx(value_degree))
            print("final radian", numerical_approx(value_radian))
            raise ValueError
        if self.degree == None or self.radian == None:
            raise ValueError("Something wrong")

    def positive(self):
        """
        If the angle is negative, return the corresponding positive angle.
        """
        if self.degree >= 0:
            return self
        if self.degree < 0:
            return AngleMeasure(value_degree=360+self.degree)

    def __mul__(self, coef):
        from yanntricks.src.src.degree_unit import degreeUnit
        from yanntricks.src.src.radian_unit import radianUnit
        if isinstance(coef, degreeUnit) or isinstance(coef, radianUnit):
            return self
        return AngleMeasure(value_radian=coef*self.radian)
    # The following is floordiv to be used with //
    # I do not know why __div__ does not work. I use it in FractionPieDiagramGraph

    def __floordiv__(self, coef):
        return AngleMeasure(value_radian=self.radian/coef)

    def __rmul__(self, coef):
        return self*coef

    def __sub__(self, other):
        try:
            s = AngleMeasure(value_radian=self.radian-other.radian)
        except AttributeError:
            from yanntricks.src.NoMathUtilities import logging
            logging("Are you trying to add an 'AngleMesasure' with something else ?")
            logging("'other's type is "+str(type(other)))
            raise
        return s

    def __add__(self, other):
        ##
        # return the sum of two angles.
        # The return type is `AngleMeasure`

        try:
            return AngleMeasure(value_radian=self.radian+other.radian)
        except AttributeError:
            from yanntricks.src.NoMathUtilities import logging
            logging("Are you trying to add an 'AngleMeasure' with something else ?")
            logging("The other's type is "+str(type(other)))
            raise

    def __neg__(self):
        return AngleMeasure(value_degree=-self.degree)

    def __div__(self, coef):
        return AngleMeasure(value_radian=self.radian/coef)

    def __lt__(self, other):
        if isinstance(other, AngleMeasure):
            if self.degree < other.degree:
                return True
            if self.degree >= other.degree:
                return False
        return NotImplemented

    def __le__(self, other):
        if self < other:
            return True
        if self == other:
            return True
        return False

    def __eq__(self, other):
        if isinstance(other, AngleMeasure):
            if self.degree == other.degree:
                return True
            if self.radian == other.radian:
                return True
            return False
        return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return "AngleMeasure, degree=%s,radian=%s" % (str(numerical_approx(self.degree)), str(self.radian))

    def __repr__(self):
        return self.__str__()


def DegreeAngleMeasure(x):
    return AngleMeasure(value_degree=x)


def RadianAngleMeasure(x):
    return AngleMeasure(value_radian=x)
