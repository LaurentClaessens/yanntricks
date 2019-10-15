
from sage.all import numerical_approx, sqrt, arctan, pi
from yanntricks.src.Numerical import numerical_is_negative
from yanntricks.src.AngleMeasure import AngleMeasure

class PolarCoordinates(object):
    def __init__(self, r, value_degree=None, value_radian=None):
        self.r = r
        self.measure = AngleMeasure(
            value_degree=value_degree, value_radian=value_radian)
        self.degree = self.measure.degree
        self.radian = self.measure.radian

    def __str__(self):
        return "PolarCoordinates, r=%s,degree=%s,radian=%s" % (str(self.r), str(self.degree), str(self.radian))


def PointToPolaire(P=None, x=None, y=None, origin=None, numerical=True):
    """
    Return the polar coordinates of a point.
    """
    if origin:
        Ox = origin.x
        Oy = origin.y
    if not origin:
        Ox = 0
        Oy = 0
    if P:
        Px = P.x
        Py = P.y
    else:
        Px = x
        Py = y
    Qx = Px-Ox
    Qy = Py-Oy
    if numerical:
        Qx = numerical_approx(Qx)
        Qy = numerical_approx(Qy)
    r = sqrt(Qx**2+Qy**2)
    if abs(Qx) < 0.001:   # epsilon
        if Qy > 0:
            radian = pi/2
        else:
            radian = 3*pi/2
    else:
        radian = arctan(Qy/Qx)
    if Qx < 0:
        if Qy > 0:
            radian = radian+pi
        if Qy <= 0:
            radian = pi+radian
    # Only positive values (February 11, 2015)
    if numerical_is_negative(radian):
        radian = radian+2*pi
    return PolarCoordinates(r, value_radian=radian)
