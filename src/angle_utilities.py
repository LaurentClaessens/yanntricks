"""Some utilities to manipulate angles."""

from sage.all import SR, pi, sqrt, numerical_approx, arctan, var, solve, atan

from phystricks.src.MathStructures import DegreeAngleMeasure


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
