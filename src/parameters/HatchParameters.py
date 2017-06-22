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


class HatchParameters(object):
    """Same as FillParameters, but when one speaks about hatching"""
    def __init__(self):
        self.color = None
        self._crossed = False
        self.angle = -45
    def crossed(self):
        self._crossed=True
    def add_to_options(self,opt):
        opt.add_option("hatchangle=%s"%str(self.angle))
        if self._crossed:
            opt.add_option("fillstyle=crosshatch")
        else:
            opt.add_option("fillstyle=vlines")
        if self.color :
            opt.add_option("hatchcolor=%s"%str(self.color))
    def copy(self):
        cop=HatchParameters()
        cop.color=self.color
        cop.angle=self.angle
        cop._crossed=self._crossed
        return cop
