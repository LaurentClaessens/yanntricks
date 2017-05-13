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

