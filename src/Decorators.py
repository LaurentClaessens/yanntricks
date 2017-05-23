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

# copyright (c) Laurent Claessens, 2017
# email: laurent@claessens-donadello.eu

def copy_parameters(f):
    """
    Many objects can produce other objects,
    like a segment has an orthogonal segment
    or a circle has its parametric curve.

    This decorator makes a copy of the parameters 
    of the old object to the new one.

    EXAMPLE

    Suppose the following in the class 'circle'

    @copy_parameters
    def parametric_curve(self,x):
        # compute the parametric curve 
        return curve

    'circle.parametric_curve(x)' will return a parametric
    curve with the same parameters as the initial circle. 
    Like color, dashed, style, etc.
    """
    def g(*arg,**kw):
        self=arg[0]
        obj=f(*arg,**kw)
        obj.parameters=self.parameters.copy()
        return obj
    return g

## The function `Intersection` has to return only points with real coordinates
# and have to sort these points. This leads to code duplication because we create
# the point list in several different manners (with 'return' between them)
# depending on the passed parameters.
def sort_and_assert_real(f):
    def g(*arg,**kw):
        pts=f(*arg,**kw)

        pts.sort(key=lambda S:S.x)
        for P in pts:
            if "I" in P.coordinates():
                from Exception import ImaginaryPartException
                raise ImaginaryPartException("There seem to be an imaginary part in "+P.coordinates())
        return pts

    return g
