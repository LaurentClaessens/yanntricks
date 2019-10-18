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

# copyright (c) Laurent Claessens, 2010-2016, 2019
# email: laurent@claessens-donadello.eu


from yanntricks.src.ObjectGraph import ObjectGraph


class FractionPieDiagramGraph(ObjectGraph):
    def __init__(self, center, radius, a, b):
        """
        The pie diagram for the fraction 'a/b' inside the circle of given center and radius.

        2/4 and 1/2 are not treated in the same way because 2/4 divides the pie into 4 parts (and fills 2) while 1/2 divides into 2 parts (and fills 1).
        """
        from yanntricks.src.Constructors import Circle
        ObjectGraph.__init__(self, self)
        self.center = center
        self.radius = radius
        self.numerator = a
        self.denominator = b
        if a > b:
            raise ValueError("Numerator is larger than denominator")
        self.circle = Circle(self.center, self.radius)
        self._circular_sector = None

    def circular_sector(self):
        if not self._circular_sector:
            FullAngle = AngleMeasure(value_degree=360)
            cs = CircularSector(self.center, self.radius, 0,
                                self.numerator*FullAngle//self.denominator)
            cs.parameters.filled()
            cs.parameters.fill.color = "lightgray"
            self._circular_sector = cs
        return self._circular_sector

    def _bounding_box(self, pspict):
        return self.circle.bounding_box(pspict)

    def action_on_pspict(self, pspict):
        from yanntricks.src.Constructors import Circle
        from yanntricks.src.segment import Segment
        if self.denominator == self.numerator:
            cs = Circle(self.center, self.radius)
            cs.parameters.filled()
            cs.parameters.fill.color = "lightgray"
            l = [cs]
        else:
            import numpy
            l = [self.circular_sector()]
            for k in numpy.linspace(0, 360, self.denominator, endpoint=False):
                s = Segment(self.circle.get_point(k), self.center)
                s.parameters.style = "dashed"
                l.append(s)
            l.append(self.circle)
        pspict.DrawGraphs(l)
