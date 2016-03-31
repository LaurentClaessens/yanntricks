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

# copyright (c) Laurent Claessens, 2016
# email: laurent@claessens-donadello.eu

# This file contains some functions used for testing purpose.

def roundingMinMax( d ):
    """
    From a dictionary of "xmin,..." return the dictionary of three-digit rounded values
    """
    new={}
    for p in ["xmax","xmin","ymax","ymin"]:
        s=numerical_approx(d[p],digits=3)
        new[p]=s
    return new

def roundingForTest( obj  ):
    if isinstance(obj,dict):
        if "xmax" in obj.keys():
            return roundingMinMax(obj)


