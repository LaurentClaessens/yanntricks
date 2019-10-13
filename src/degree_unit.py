
from phystricks.src.conversion_angles import DegreeConversions

class degreeUnit(object):
    """
    For degreeUnit and radianUnit

    - `keep_large` (boolean, default=False). When False, an angle larger than 2pi (360 degree) is automatically converted into an angle between 0 and 2pi. When true, keep angle larger than 2pi. 
    """

    def __call__(self, x, number=False, keep_max=None, keep_large=False, converting=True, numerical=False):
        from phystricks.src.polar_coordinates import PolarCoordinates
        from phystricks.src.AngleMeasure import AngleMeasure
        if isinstance(x, PolarCoordinates) or isinstance(x, AngleMeasure):
            return x.degree
        return DegreeConversions.conversion(x, number=number, keep_max=keep_max, keep_large=keep_large, converting=converting, numerical=numerical)

    def __rmul__(self, x):
        return AngleMeasure(value_degree=x)

degree = degreeUnit()
