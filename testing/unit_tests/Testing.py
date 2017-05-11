# -*- coding: utf8 -*-

###########################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2016-2017
# email: laurent@claessens-donadello.eu

# This file contains some functions used for testing purpose.

from __future__ import division
from sage.all import *

def roundingMinMax( d ):
    """
    From a dictionary of "xmin,..." return the dictionary of three-digit rounded values
    """
    new={}
    for p in ["xmax","xmin","ymax","ymin"]:
        s=numerical_approx(d[p],digits=3)
        new[p]=s
    return new


def assert_true(b,failure_message=""):
    """
    Raise a FailedAssertException if the boolean is False.
    """
    if b is False :
        from Exceptions import FailedAssertException
        raise FailedAssertException(failure_message)

def assert_equal(e1,e2,failure_message=""):
    """
    Raise a FailedAssertException if the two expressions 'e1' and 'e2' 
    are not equal.
    """
    if not e1==e2 :
        from Exceptions import FailedAssertException
        raise FailedAssertException(str(e1)+" is not equal to "+str(e2))

def assert_almost_equal(e1,e2,epsilon=0.0001,failure_message=""):
    """
    Raise a FailedAssertException if the two expressions 'e1' and 'e2' 
    are not equal up to 'epsilon'

    First try to use
    ```
    e1.is_almost_equal(e2,epsilon)
    ```
    because some objects in 'phystricks' have that method.

    If `e1` has not that method :
    - assume that `e1` and `e2` are numerical
    - compute a numerical approximation
    - fail if the absolute value of the difference
        is larger than `epsilon`
    """
    if hasattr(e1,'is_almost_equal'):
        if not e1.is_almost_equal(e2,epsilon):
            from Exceptions import FailedAssertException
            raise FailedAssertException(str(e1)+" is not equal to "+str(e2)+" up to "+str(epsilon))
        return True
        
    v1=numerical_approx(e1)
    v2=numerical_approx(e2)
    d=abs(v1-v2)
    if not d<epsilon :
        from Exceptions import FailedAssertException
        raise FailedAssertException(str(e1)+" is not equal to "+str(e2)+" up to "+str(epsilon))

def echo_function(text):
    print("  "+text)
def echo_single_test(text):
    print("    "+text)
