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

# copyright (c) Laurent Claessens, 2010,2011,2013-2017, 2019
# email: laurent@claessens-donadello.eu

from sage.all import numerical_approx, SR, pi

class AngleMeasure(object):
    """
    Describe an angle.

    This class is an attempt to abstract the degree/radian problem.

    EXAMPLES::

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

    If the numerical approximation of an angle in degree is close to an integer
    up to less than 1e-10, we round it.
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

        from Utilities import PolarCoordinates

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

            from Utilities import degree
            from Utilities import radian
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
            from NoMathUtilities import logging
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
            from NoMathUtilities import logging
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


class PolarCoordinates(object):
    def __init__(self, r, value_degree=None, value_radian=None):
        self.r = r
        self.measure = AngleMeasure(
            value_degree=value_degree, value_radian=value_radian)
        self.degree = self.measure.degree
        self.radian = self.measure.radian

    def __str__(self):
        return "PolarCoordinates, r=%s,degree=%s,radian=%s" % (str(self.r), str(self.degree), str(self.radian))


def DegreeAngleMeasure(x):
    return AngleMeasure(value_degree=x)


def RadianAngleMeasure(x):
    return AngleMeasure(value_radian=x)

class ConversionAngles(object):
    """
    Simplify and convert angle units.

    This class serves to factorise conversion degree -> radian and degree -> degree
    INPUT:
    - ``conversion_factor`` - the conversion factor from the considered unit to the other (radian->degree or the contrary)
    - ``max_value`` - the maximal value (360 or 2*pi)
    """

    def __init__(self, conversion_factor, max_value, exit_attribute=None, create_function=None):
        self.conversion_factor = conversion_factor
        self.max_value = max_value
        self.exit_attribute = exit_attribute
        self.create_function = create_function

    def simplify(self, angle, keep_max=False, keep_large=False, number=False, numerical=False):
        """
        Simplify the angles modulo the maximum (if 'keep_large'=False, which is default). 

        If what is given is a number, return a number. If what is given is a AngleMeasure, return a new AngleMeasure.

        Keep the negative numbers to negative numbers. The return interval is
        [-2 pi,2pi]
        which could be open or closed following the `keep_max` boolean.

        INPUT:

        - ``angle`` - an angle that can be an instance of AngleMeasure or a number.  if it is a number, the simplify modulo self.max_value if it is a AngleMeasure, then first extract the value of the angle using self.exit_attribute .

        - ``keep_max`` - (default=False) If True, does not simplify the angle with max value.  Typically, keeps 2*pi as 2*pi.  This is used in order to keep track of the difference between 0 and 2*pi in the context of drawing an full circle.
        - ``keep_large`` - (default=False)  If True, an angle larger than 2pi remains large than 2pi.

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
            number = True
        if isinstance(angle, AngleMeasure):
            x = angle.__getattribute__(self.exit_attribute)
            gotMeasure = True
        else:
            x = angle
            gotMeasure = False
        if keep_max and (x == self.max_value or x == -self.max_value):
            if gotMeasure and number == False:
                return angle
            else:
                if numerical:
                    return numerical_approx(x)
                else:
                    return x

        if not keep_large:
            while x >= self.max_value:
                x = x-self.max_value
            while x <= -self.max_value:
                x = x+self.max_value

        if gotMeasure and number == False:
            return self.create_function(x)
        else:
            if numerical:
                return numerical_approx(x)
            else:
                return x

    def conversion(self, theta, number=False, keep_max=False, keep_large=False, converting=True, numerical=False):
        """
        Makes the conversion and simplify.

        INPUT:

        - ``theta`` - the angle to be converted.
        - ``number`` - (default =False) If true, return a number. Not to be confused with <numerical>.
        - ``keep_max`` - (default False) If true, does not convert the max value into the minimal value.  Typically, leaves 2*pi as 2*pi instead of returning 0.
        - ``keep_large`` - (default False) if an angle larger that 2pi is given, return an angle larger than 2pi.
        - ``converting`` - (defaut = True) If False, make no conversion.
        - ``numerical`` - (default = False) boolean. If True, return a numerical approximation.  If <numerical>=True, then <number> is automatically switched to True.

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
            number = True
        if isinstance(theta, AngleMeasure):
            angle = self.simplify(
                theta, keep_max=keep_max, keep_large=keep_large)
            if number:
                x = angle.__getattribute__(self.exit_attribute)
                if numerical:
                    return numerical_approx(x)
                else:
                    return x
            else:
                return angle
        else:
            if converting:
                return self.simplify(self.conversion_factor*theta, keep_max=keep_max, keep_large=keep_large, numerical=numerical)
            else:
                raise ShouldNotHappenException(
                    "You are in a converting function with argument converting=false. WTF ? Sincerely, I'm trying to figure out what I had in mind when I wrote this case.")
                return self.simplify(theta, keep_max=keep_max, keep_large=keep_large, numerical=numerical)


DegreeConversions = ConversionAngles(
    SR(180)/pi,
    360,
    exit_attribute="degree",
    create_function=DegreeAngleMeasure)

RadianConversions = ConversionAngles(
    pi/180,
    2*pi,
    exit_attribute="radian",
    create_function=RadianAngleMeasure)


class degreeUnit(object):
    """
    For degreeUnit and radianUnit

    - `keep_large` (boolean, default=False). When False, an angle larger than 2pi (360 degree) is automatically converted into an angle between 0 and 2pi. When true, keep angle larger than 2pi. 
    """

    def __call__(self, x, number=False, keep_max=None, keep_large=False, converting=True, numerical=False):
        if isinstance(x, PolarCoordinates) or isinstance(x, AngleMeasure):
            return x.degree
        return DegreeConversions.conversion(x, number=number, keep_max=keep_max, keep_large=keep_large, converting=converting, numerical=numerical)

    def __rmul__(self, x):
        return AngleMeasure(value_degree=x)


class radianUnit(object):
    def __call__(self, x, number=False, keep_max=None, keep_large=False, converting=True, numerical=False):
        if isinstance(x, PolarCoordinates) or isinstance(x, AngleMeasure):
            return x.radian
        return RadianConversions.conversion(x, number=number, keep_max=keep_max, keep_large=keep_large, converting=converting, numerical=numerical)

    def __rmul__(self, x):
        return AngleMeasure(value_radian=x)


degree = degreeUnit()
radian = radianUnit()

simplify_degree = DegreeConversions.simplify
simplify_radian = RadianConversions.simplify
