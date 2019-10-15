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
from yanntricks.src.Utilities import make_psp_list
from yanntricks.src.segment import Segment
from yanntricks.src.BoundingBox import BoundingBox


# \brief the graph of a polygon
#
# In order to change the parameters of the polygon (line style, color, ...)
# you have to change
# * `poly.edges_parameters` for the parameters of the edge.
# * `poly.hatch_parameters` for the hatching parameters
# * `poly.fill_parameters` for the filling parameters
# In particular, the edge color, the hatch color and the filling color are
# independent. Yes, you can hatch and fill; in this case, the hatch is *over*
# the filling.
class PolygonGraph(ObjectGraph):
    def __init__(self, points_list):
        ObjectGraph.__init__(self, self)
        self.edges = []
        self.vertices = points_list
        self.points_list = self.vertices

        for i in range(0, len(self.points_list)):
            segment = Segment(
                self.points_list[i], self.points_list[(i+1) % len(self.points_list)])
            self.edges.append(segment)
        self.draw_edges = True
        self.independent_edge = False
        self.parameters = None

        from yanntricks.src.parameters.Parameters import Parameters
        from yanntricks.src.parameters.HatchParameters import HatchParameters
        from yanntricks.src.parameters.FillParameters import FillParameters

        self.edges_parameters = Parameters(self)
        self.hatch_parameters = HatchParameters()
        self.fill_parameters = FillParameters()
        self._hatched = False
        self._filled = False

    def hatched(self):
        self._hatched = True

    def filled(self):
        self._filled = True

    def rotation(self, angle):
        pts = [P.rotation(angle) for P in self.points_list]
        return Polygon(pts)

    def make_edges_independent(self):
        """
        make the edges customisation independent the one to the other.
        """
        self.independent_edge = True

    def no_edges(self):
        """
        When X.no_edges() is used, the edges of the polygon will not be drawn.

        The argument `points_name` override `text_list`.
        """
        self.draw_edges = False

    def put_mark(self, dist, text_list=None, points_names=None,
                 mark_point=None, pspict=None, pspicts=None):
        from Visual import visual_vector, polar_to_visual_polar

        pspicts = make_psp_list(pspict, pspicts)

        n = len(self.points_list)
        if not text_list and not points_names:
            import string
            text_list = ["\({}\)".format(x)
                         for x in string.ascii_uppercase[0:n]]
        # One can do :
        # polygon.put_mark(0.2,points_names=" B ",pspict=pspict)
        # or
        # polygon.put_mark(0.3,text_list=["","\( F\)","\( E\)"],pspict=pspict)
        # where 'polygon' is a triangle.
        # In both cases we have an empty string as mark and then a box
        # of size zero.
        # We thus have to following error
        # TypeError: cannot evaluate symbolic expression numerically
        # on the second pass, because the size of the box being zero,
        # the line equations somehow trivializes themselves and Sage
        # founds infinitely many intersections.
        # This is why we do not something like :
        # text_list=[ "\( {} \)".format(x) for x in points_names ]
        if text_list:
            for i in range(len(text_list)):
                if text_list[i] == "":
                    text_list[i] = None
        if points_names:
            text_list = []
            for x in points_names:
                if x == " ":
                    text_list.append(None)
                else:
                    text_list.append("\( {} \)".format(x))
        for i, P in enumerate(self.points_list):
            text = text_list[i]
            if text is not None:
                A = self.points_list[(i-1) % n]
                B = self.points_list[(i+1) % n]
                v1 = AffineVector(A, P).fix_origin(P).normalize(1)
                v2 = AffineVector(B, P).fix_origin(P).normalize(1)

                # 'direction' is a vector based at 'P' that points
                # in the direction as external to the angle as possible.
                # This is the "external" angle bisector
                # Why not `direction=v1+v2` ? Because we are victim
                # of the problem described
                # in the comment of AffineVectorGraph.__add__
                direction = v1.extend(v2)
                angle = direction.angle()
                for psp in pspicts:
                    P.put_mark(dist=dist, angle=angle, added_angle=0, text=text,
                               position="center_direction", pspict=psp)
                    self.added_objects.append(psp, P)

    def _math_bounding_box(self, pspict=None):
        bb = BoundingBox()
        bb.is_math = True
        for P in self.points_list:
            bb.append(P, pspict=pspict)
        return bb

    def _bounding_box(self, pspict=None):
        return self.math_bounding_box(pspict)

    def action_on_pspict(self, pspict):
        """If one wants to fill or hatch, one has to ask explicitly."""
        from yanntricks.src.CustomSurfaceGraph import CustomSurface
        if self._filled:
            custom = CustomSurface(self.edges)
            custom.parameters.filled()
            custom.parameters.fill = self.fill_parameters.copy()
            pspict.DrawGraphs(custom)
        if self._hatched:
            custom = CustomSurface(self.edges)
            custom.parameters.hatched()
            custom.parameters.hatch = self.hatch_parameters.copy()
            pspict.DrawGraphs(custom)
        if self.draw_edges:
            for edge in self.edges:
                if not self.independent_edge:
                    edge.parameters = self.edges_parameters.copy()
                pspict.DrawGraphs(edge)
