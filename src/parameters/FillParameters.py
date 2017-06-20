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

class FillParameters(object):
    """
    Represent the parameters of filling a surface.
    """
    def __init__(self):
        self.color = "lightgray"
        self.style = "solid"
    def add_to_options(self,opt):
        """
        add `self` to a set of options.

    
        INPUT:

        - ``opt`` - an instance of :class:`Options`.

        OUTPUT:

        Return `opt` with added properties.

        """
        if self.color :
            opt.add_option("fillcolor=%s"%str(self.color))
        if self.style :
            opt.add_option("fillstyle=%s"%str(self.style))
    def copy(self):
        cop=FillParameters()
        cop.color=self.color
        cop.style=self.style
        return cop
