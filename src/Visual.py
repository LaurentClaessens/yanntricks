# -*- coding: utf8 -*-

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

# copyright (c) Laurent Claessens, 2010-2017
# email: laurent@claessens-donadello.eu

from sage.all import *
from Constructors import Vector,Point

from Debug import dprint,testtype

def visual_length(v,l,xunit=None,yunit=None,pspict=None):
    """
    Return a vector in the direction of v that has *visual* length
    l taking xunit and yunit into account.
    """
    if pspict:
        xunit=pspict.xunit
        yunit=pspict.yunit
    Dx=v.Dx
    Dy=v.Dy
    if not v.vertical :
        slope=v.slope
        x=l/sqrt(xunit**2+slope**2*yunit**2)

        if numerical_is_negative(Dx):
            x=-x
        y=slope*x
    else:
        x=0
        y=l/yunit
        if numerical_is_negative(Dy):
            y=-l/yunit
    if hasattr(v,"I"):
        from phystricks import AffineVector
        from phystricks import Vector
        return AffineVector(v.I,v.I+Vector(x,y))
    else:
        from phystricks import Vector
        return Vector(x,y)

def visual_polar(P,r,theta,pspict=None):
    """
    Return a point at VISUAL coordinates (r,theta) from the point P.

    theta is given in degree.
    """
    xunit=pspict.xunit
    yunit=pspict.yunit
    alpha=pi*theta/180
    v=Vector( cos(alpha)/xunit,sin(alpha)/yunit  )
    w=visual_length(v,r,pspict=pspict)
    return P+w

def polar_to_visual_polar(r,theta,pspict=None):
    """
    From '(r,theta)', return the (s,alpha) such that the point
    (s,alpha) visually appears as (r,theta).
    """
    P=visual_polar( Point(0,0),r,theta,pspict  )
    return P.polar_coordinates()

def visual_polar_coordinates(P,pspict=None):
    """
    return the visual polar coordinates of 'P'
    """
    if isinstance(pspict,list):
        xu=pspict[0].xunit
        yu=pspict[0].xunit
        xunits=[ psp.xunit==xu for psp in pspict ]
        yunits=[ psp.yunit==yu for psp in pspict ]
        if sum(xunits)==len(xunits) and sum(yunits)==len(yunits):
            xunit=xu
            yunit=yu
        else :
            print("Probably more than one picture with different dilatations ...")
            raise ValueError
    else :
        xunit=pspict.xunit
        yunit=pspict.yunit
    Q=Point(xunit*P.x,yunit*P.y)
    return Q.polar_coordinates()

def visual_vector(v,pspict=None):
    """
    return a vector at the same base as 'v' but such that
    it will visually appears as 'v'
    """
    from NoMathUtilities import logging
    from Constructors import AffineVector
    if pspict is None:
        logging("Trying to make visual_vector with no pspict ?")
        return v
    xunit=pspict.xunit
    yunit=pspict.yunit
    I=v.I
    F=I+(v.Dx/xunit,v.Dy/yunit)
    return AffineVector(I,F)
