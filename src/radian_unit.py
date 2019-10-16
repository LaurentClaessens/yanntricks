

from yanntricks.src.polar_coordinates import PolarCoordinates

class radianUnit(object):
    def __call__(self, x, number=False, keep_max=None, keep_large=False, converting=True, numerical=False):
        from yanntricks.src.AngleMeasure import AngleMeasure
        from yanntricks.src.conversion_angles import RadianConversions
        if isinstance(x, PolarCoordinates) or isinstance(x, AngleMeasure):
            return x.radian
        return RadianConversions.conversion(x, number=number, keep_max=keep_max, keep_large=keep_large, converting=converting, numerical=numerical)

    def __rmul__(self, x):
        from yanntricks.src.AngleMeasure import AngleMeasure
        return AngleMeasure(value_radian=x)


radian = radianUnit()
