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


from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.Constructors import *


class MoustacheGraph(ObjectGraph):
    def __init__(self, minimum, Q1, M, Q3, maximum, h, delta_y=0):
        ObjectGraph.__init__(self, self)
        self.Q1 = Q1
        self.Q3 = Q3
        self.M = M
        self.h = h
        self.delta_y = delta_y
        self.minimum = minimum
        self.maximum = maximum

    def action_on_pspict(self, pspict):
        my = self.delta_y-self.h/2
        My = self.delta_y+self.h/2
        h1 = Segment(Point(self.minimum, my), Point(self.minimum, My))
        s1 = Segment(Point(self.minimum, self.delta_y),
                     Point(self.Q1, self.delta_y))
        box = Polygon(Point(self.Q1, my), Point(self.Q3, my),
                      Point(self.Q3, My), Point(self.Q1, My))
        med = Segment(Point(self.M, my), Point(self.M, My))
        med.parameters.color = "red"
        s2 = Segment(Point(self.Q3, self.delta_y),
                     Point(self.maximum, self.delta_y))
        h2 = Segment(Point(self.maximum, my), Point(self.maximum, My))
        pspict.DrawGraphs(h1, h2, s1, box, med, s2)

    def mark_point(self, pspict=None):
        return Point(self.maximum, self.delta_y)

    def _math_bounding_box(self, pspict):
        return self.bounding_box(pspict)

    def _bounding_box(self, pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        bb = BoundingBox()
        bb.addX(self.minimum)
        bb.addX(self.maximum)
        bb.addY(self.delta_y-self.h/2)
        bb.addY(self.delta_y+self.h/2)
        return bb

    def latex_code(self, language=None, pspict=None):
        return ""
