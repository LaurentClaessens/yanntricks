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

# copyright (c) Laurent Claessens, 2009-2017, 2019
# email: laurent@claessens-donadello.eu

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.segment import Segment
from yanntricks.src.point import Point



class GridGraph(ObjectGraph):
    """
    A grid. This is main lines to appear at regular interval on the picture.

    ATTRIBUTES:

    - ``self.BB`` - the bounding box of the grid : its size.

    - ``self.Dx,self.Dy`` - the step of main subdivision along `X` and `Y` directions (have to be integers).

    - ``self.num_subX,self.num_subY`` - number of subdivision within each main subdivision of length Dx or Dy. When it is zero, there are no subdivisions.

    It draws lines on the integer multiples of `Dx`. It begins at the closest integer multiple of `Dx` from the lower left corner.
    It finishes before to reach the upper right corner if `Dx` the size.
    Subdivisions are drawn following the same rule.

    - ``self.draw_border`` - (default=False) If True, the border is drawn even if it does not  arrives on an integer multiple of Dx.
                                        It turns out that for aestetical reasons, this is a bad idea to turn it True.


    - ``self.main_horizontal`` : an objet of type :class:`SegmentGraph`. This is the archetype of the horizontal lines
                                 of the main grid will be drawn.

    As an example, in order to have red main horizontal lines::

        sage: from yanntricks import *
        sage: grid=Grid()
        sage: grid.main_horizontal.parameters.color = "red"

    """

    def __init__(self, bb=None):
        from yanntricks.src.BoundingBox import BoundingBox
        if bb is None:
            bb = BoundingBox()
        ObjectGraph.__init__(self, self)
        self.BB = bb
        self.separator_name = "GRID"
        # Default values, have to be integer.
        self.add_option({"Dx": 1, "Dy": 1})
        self.Dx = self.options.DicoOptions["Dx"]
        self.Dy = self.options.DicoOptions["Dy"]
        self.num_subX = 2
        self.num_subY = 2
        self.draw_border = False
        self.draw_horizontal_grid = True
        self.draw_vertical_grid = True
        self.main_horizontal = Segment(Point(0, 1), Point(1, 1))
        self.main_horizontal.parameters.color = "gray"
        self.main_horizontal.parameters.style = "solid"
        self.main_vertical = Segment(Point(0, 1), Point(1, 1))
        self.main_vertical.parameters.color = "gray"
        self.main_vertical.parameters.style = "solid"
        self.sub_vertical = Segment(Point(0, 1), Point(1, 1))
        self.sub_vertical.parameters.color = "gray"
        self.sub_vertical.parameters.style = "dotted"
        self.sub_horizontal = Segment(Point(0, 1), Point(1, 1))
        self.sub_horizontal.parameters.color = "gray"
        self.sub_horizontal.parameters.style = "dotted"
        self.border = Segment(Point(0, 1), Point(1, 1))
        self.border.parameters.color = "gray"
        self.border.parameters.style = "dotted"

    # This method is for the sake of "Special cases aren't special enough to break the rules."
    def _bounding_box(self, pspict=None):
        return self.BB

    def _math_bounding_box(self, pspict=None):
        return self.bounding_box(pspict)

    def add_option(self, opt):
        self.options.add_option(opt)

    def optionsTrace(self):
        from yanntricks.src.BasicGeometricObjects import OptionsStyleLigne
        return self.options.sousOptions(OptionsStyleLigne())

    def optionsParams(self):
        return self.options.sousOptions(["Dx", "Dy"])

    def action_on_pspict(self, pspict):
        from yanntricks.src.SmallComputations import MainGridArray
        from yanntricks.src.SmallComputations import SubGridArray
        a = []
        # ++++++++++++ Border ++++++++
        if self.draw_border:
            # Right border
            if self.draw_vertical_grid:
                if self.BB.xmax != int(self.BB.xmax):
                    S = self.BB.east_segment()
                    S.merge_options(self.border)
                    a.append(S)
            # Left border
            if self.draw_vertical_grid:
                if self.BB.xmin != int(self.BB.xmin):
                    S = self.BB.west_segment()
                    S.merge_options(self.border)
                    a.append(S)
            # Upper border
            if self.draw_horizontal_grid:
                if self.BB.ymax != int(self.BB.ymax):
                    S = self.BB.north_segment()
                    S.merge_options(self.border)
                    a.append(S)
            # Lower border
            if self.draw_horizontal_grid:
                if self.BB.ymin != int(self.BB.ymin):
                    S = self.BB.south_segment()
                    S.merge_options(self.border)
                    a.append(S)
        if self.draw_vertical_grid:
            # ++++++++++++ Principal vertical lines ++++++++
            for x in MainGridArray(self.BB.xmin, self.BB.xmax, self.Dx):
                S = Segment(Point(x, self.BB.ymin), Point(x, self.BB.ymax))
                S.merge_options(self.main_vertical)
                a.append(S)
            # ++++++++++++ The vertical sub grid ++++++++
            if self.num_subX != 0:
                for x in SubGridArray(self.BB.xmin, self.BB.xmax, self.Dx, self.num_subX):
                    S = Segment(Point(x, self.BB.ymin), Point(x, self.BB.ymax))
                    S.merge_options(self.sub_vertical)
                    a.append(S)
        if self.draw_horizontal_grid:
            # ++++++++++++ The horizontal sub grid ++++++++
            if self.num_subY != 0:
                for y in SubGridArray(self.BB.ymin, self.BB.ymax, self.Dy, self.num_subY):
                    S = Segment(Point(self.BB.xmin, y), Point(self.BB.xmax, y))
                    S.merge_options(self.sub_horizontal)
                    a.append(S)
            # ++++++++++++ Principal horizontal lines ++++++++
            for y in MainGridArray(self.BB.ymin, self.BB.ymax, self.Dy):
                S = Segment(Point(self.BB.xmin, y), Point(self.BB.xmax, y))
                S.merge_options(self.main_horizontal)
                a.append(S)
        pspict.DrawGraphs(a, separator_name=self.separator_name)
