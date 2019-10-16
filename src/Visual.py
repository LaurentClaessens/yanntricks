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

# copyright (c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu

# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring

from sage.all import sqrt, sin, cos, pi     #pylint:disable=import-error
from yanntricks.src.point import Point
from yanntricks.src.Numerical import numerical_is_negative


def visual_length(v, l, xunit=None, yunit=None, pspict=None):
    """
    Return a vector which as the requested *visual* length.

    Return a vector in the direction of v that has *visual* length
    l taking xunit and yunit into account.
    """
    from yanntricks.src.affine_vector import AffineVector
    if pspict:
        xunit = pspict.xunit
        yunit = pspict.yunit
    Dx = v.Dx
    Dy = v.Dy
    if not v.is_vertical:
        slope = v.slope
        x = l/sqrt(xunit**2+slope**2*yunit**2)

        if numerical_is_negative(Dx):
            x = -x
        y = slope*x
    else:
        x = 0
        y = l/yunit
        if numerical_is_negative(Dy):
            y = -l/yunit
    return AffineVector(v.I, v.I+(x, y))


def visual_polar(P, r, theta, pspict=None):
    """
    Return a point at VISUAL coordinates (r,theta) from the point P.

    theta is given in degree.
    """
    from yanntricks.src.Constructors import Vector
    xunit = pspict.xunit
    yunit = pspict.yunit
    alpha = pi*theta/180

    v = Vector(cos(alpha)/xunit, sin(alpha)/yunit)
    w = visual_length(v, r, pspict=pspict)

    return P.translate(w)


def polar_to_visual_polar(r, theta, pspict=None):
    """
    From '(r,theta)', return the (s,alpha) such that the point
    (s,alpha) visually appears as (r,theta).
    """
    P = visual_polar(Point(0, 0), r, theta, pspict)
    return P.polar_coordinates()


def visual_polar_coordinates(P, pspict=None):
    """
    return the visual polar coordinates of 'P'
    """
    if pspict is None:
        return P.polar_coordinates()
    if isinstance(pspict, list):
        xu = pspict[0].xunit
        yu = pspict[0].xunit
        xunits = [psp.xunit == xu for psp in pspict]
        yunits = [psp.yunit == yu for psp in pspict]
        if sum(xunits) == len(xunits) and sum(yunits) == len(yunits):
            xunit = xu
            yunit = yu
        else:
            print("Probably more than one picture with different dilatations ...")
            raise ValueError
    else:
        xunit = pspict.xunit
        yunit = pspict.yunit
    Q = Point(xunit*P.x, yunit*P.y)
    return Q.polar_coordinates()


def visual_vector(v, pspict=None, xunit=None, yunit=None):
    """
    Return a vector which will be visually `self`.

    Return a vector at the same base as 'v' but such that
    it will visually appears as 'v'
    """
    from yanntricks.src.NoMathUtilities import logging
    from yanntricks.src.affine_vector import AffineVector
    if pspict is None and (xunit is None or yunit is None):
        logging("Trying to make visual_vector with no pspict ?")
        raise DeprecationWarning
    if pspict:
        xunit = pspict.xunit
        yunit = pspict.yunit
    I = v.I
    F = I+(v.Dx/xunit, v.Dy/yunit)
    return AffineVector(I, F)

# return the coordinates where
# the point `P` will be.


def inverse_visual_point(P, pspict):
    return Point(P.x*pspict.xunit, P.y*pspict.yunit)

# return the coordinates where
# a point has to be placed to arrive at `P` after taking
# into account the dilatations.


def visual_point(P, pspict):
    return Point(P.x/pspict.xunit, P.y/pspict.yunit)


def inverse_visual_angle(angle, pspict):
    """
    Return the 'visual' self.

    We compute a new triple of points `A'O'B'` :
    where A',B' and C' are the points where the angle will be after
    the dilatations.
    """
    from yanntricks.src.Constructors import AngleAOB
    Ap = inverse_visual_point(angle.A, pspict)
    Op = inverse_visual_point(angle.O, pspict)
    Bp = inverse_visual_point(angle.B, pspict)
    return AngleAOB(Ap, Op, Bp, r=angle.r)
