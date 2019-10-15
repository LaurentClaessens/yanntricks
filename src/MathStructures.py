##########################################################################
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
##########################################################################

# copyright (c) Laurent Claessens, 2010,2011,2013-2017, 2019
# email: laurent@claessens-donadello.eu

# pylint: disable=invalid-name

from sage.rings.rational import Rational
from sage.all import latex, SR

from yanntricks.src.SmallComputations import MultipleBetween


class AxesUnit(object):
    def __init__(self, numerical_value, latex_symbol=""):
        try:
            numerical_value = Rational(numerical_value)
        except TypeError:
            pass
        self.numerical_value = numerical_value
        self.latex_symbol = latex_symbol

    def symbol(self, x):
        return latex(x)+self.latex_symbol

    def place_list(self, mx, Mx, frac=1, mark_origin=True):
        """
        return a tuple of 
        1. values that are all the integer multiple of 
                <frac>*self.numerical_value 
            between mx and Mx
        2. the multiple of the basis unit.

        Give <frac> as literal real. Recall that python evaluates 1/2 to 0. If you pass 0.5, it will be converted back to 1/2 for a nice display.
        """
        try:
            # If the user enters "0.5", it is converted to 1/2
            frac = Rational(frac)
        except TypeError:
            pass
        if frac == 0:
            raise ValueError(
                "frac is zero in AxesUnit.place_list(). Maybe you ignore that python evaluates 1/2 to 0 ? (writes literal 0.5 instead) \n Or are you trying to push me in an infinite loop ?")
        l = []
        k = SR.var("TheTag")
        for x in MultipleBetween(frac*self.numerical_value, mx, Mx, mark_origin):
            if self.latex_symbol == "":
                l.append((x, "$"+latex(x)+"$"))
            else:
                pos = (x/self.numerical_value)*k
                # This risks to be Sage-version dependent.
                text = "$"+latex(pos).replace("TheTag", self.latex_symbol)+"$"
                l.append((x, text))
        return l
