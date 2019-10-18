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

from yanntricks.src.Constructors import *
from yanntricks.src.PolygonGraph import PolygonGraph


class RectangleGraph(PolygonGraph):
    """
    The parameters of the four lines are by default the same, but they can be adapted separately.

    graph_N returns the north side as a yanntricks.Segment object
    """

    def __init__(self, NW, SE):
        self.NW = NW
        self.SE = SE
        self.SW = Point(self.NW.x, self.SE.y)
        self.NE = Point(self.SE.x, self.NW.y)
        PolygonGraph.__init__(self, [self.SW, self.SE, self.NE, self.NW])
        self.mx = self.NW.x
        self.Mx = self.SE.x
        self.my = self.SE.y
        self.My = self.NW.y
        self.rectangle = self.obj

        self.segment_N = Segment(self.NW, self.NE)
        self.segment_S = Segment(self.SW, self.SE)
        self.segment_E = Segment(self.NE, self.SE)
        self.segment_W = Segment(self.NW, self.SW)

        # Putting the style of the edges to none makes the
        # CustomSurface (and then filling and hatching) not work
        # because the edges'LaTeX code is use to create the tikz path
        # defining the surface.
    def polygon(self):
        polygon = Polygon(self.NW, self.NE, self.SE, self.SW)
        polygon.parameters = self.parameters.copy()
        return polygon

    def first_diagonal(self):
        return Segment(self.NW, self.SE)

    def second_diagonal(self):
        return Segment(self.SW, self.NE)

    def center(self):
        return self.first_diagonal().midpoint()

    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return RectangleGraph

    def _segment(self, side):
        bare_name = "graph_"+side
        return self.__dict__[bare_name]
