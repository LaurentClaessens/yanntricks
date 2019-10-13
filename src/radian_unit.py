

class radianUnit(object):
    def __call__(self, x, number=False, keep_max=None, keep_large=False, converting=True, numerical=False):
        if isinstance(x, PolarCoordinates) or isinstance(x, AngleMeasure):
            return x.radian
        return RadianConversions.conversion(x, number=number, keep_max=keep_max, keep_large=keep_large, converting=converting, numerical=numerical)

    def __rmul__(self, x):
        return AngleMeasure(value_radian=x)


radian = radianUnit()
