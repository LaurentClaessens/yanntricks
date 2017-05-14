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

# copyright (c) Laurent Claessens, 2010,2011,2013-2015,2017
# email: laurent@claessens-donadello.eu

##
# We put here some small numerical comparison functions "up to epsilon"

from __future__ import division
from sage.all import numerical_approx

def are_almost_equal(a,b,epsilon=0.0001):
    ## \brief Says if `a` and `b` are equal up to epsilon
    aN=numerical_approx(a)
    bN=numerical_approx(b)
    if abs(aN-bN)<0.0001:    # epsilon
        return True
    return False

def numerical_min(x,y,epsilon=None):
    ##
    # \brief return the minimum of `x` and `y`
    # 
    # Compute numerical approximations of `x` and `y` and return the min
    #
    # If `epsilon` is given, raise an exception if the difference is
    # smaller than `epsilon`.
    #
    #    The reason is that Sage cannot always determine the min or the max of
    #    expressions like ```1000``` of type `int` and ```cos(0.0823552493237255*pi)```  of type `sage.symbolic.expression.Expression`
    nx=numerical_approx(x)
    ny=numerical_approx(y)

    if epsilon is not None :
        if abs(nx,ny)>epsilon:
            raise ValueError

    return min(nx,ny)

def numerical_max(x,y,epsilon=None):
## Same as `numerical_min` with ad-hoc changes
    nx=numerical_approx(x)
    ny=numerical_approx(y)

    if epsilon is not None :
        if abs(nx,ny)>epsilon:
            raise ValueError

    return max(nx,ny)

def is_almost_zero(x,epsilon=0.0001):
    """
    Try to say if Abs(x)<epsilon.

    It is not always possible because
    - x could be an expression on which Sage cannot compute abs
    - the precision on x could be lower than epsilon, so that Sage will complain. In this case we check is x is the smaller possible in its precision and `epsilon` is not used.

        sage: from phystricks.SmallComputations import numerical_isZero
        sage: numerical_isZero(-pi)
        False
    """
    try :
        return abs(x) < epsilon
    except:
        raise

def numerical_is_negative(x):
    """
    try to say if `x` is numerically negative.

    I got difficulties on the following :
    sage:radian =arctan(1/sin(1.2000000000000002*pi))
    sage: if radian< 0:
        print("ok")
        ....:   
    results in an OverflowError: Python int too large to convert to C long.
    """
    try :
        return x.is_negative()
    except AttributeError:
        pass
    return numerical_approx(x)<0
