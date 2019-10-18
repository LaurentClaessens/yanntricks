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

# copyright(c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu


# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=fixme


from sage.all import numerical_approx  # pylint:disable=import-error
from sage.all import cos, sin  # pylint:disable=import-error

from yanntricks.src.Exceptions import ShouldNotHappenException
from yanntricks.src.Utilities import point_to_box_intersection
from yanntricks.src.ObjectGraph import ObjectGraph

# The marks are not taken into account in the computation of the
# mathematical bounding box. In particular not for the computations
# of the axes size.
# See also `AxesGraph.add_bounding_box`


class MarkGraph(ObjectGraph):
    """
    Describe a mark on an object.

    That is, most of the time, the mathematical name to be written
    next to the object.
    """

    def __init__(self, graph, dist, angle, text, mark_point=None,
                 central_point=None, position=None, pspict=None):
        from yanntricks.src.AngleMeasure import AngleMeasure
        from yanntricks.src.radian_unit import radian
        ObjectGraph.__init__(self, self)

        self.take_math_BB = False

        self._central_point = central_point
        self.mark_point = mark_point
        self.graph = graph
        self.parent = graph

        self.angle = None
        if isinstance(angle, AngleMeasure):
            self.angle = angle
        else:
            if angle is not None:
                self.angle = AngleMeasure(value_degree=angle)

        self.dist = dist
        self.text = text

        self.position = position
        self.pspict = pspict

        if angle is not None:
            alpha = radian(angle)
            if isinstance(alpha, AngleMeasure):
                self.x = self.dist*cos(alpha.radian)
                self.y = self.dist*sin(alpha.radian)
            else:
                self.x = self.dist*cos(alpha)
                self.y = self.dist*sin(alpha)

    def central_point(self, pspict=None):
        """
        Return the central point of the mark, that is the point where
        the mark arrives.

        The central point of the mark is computed from
        self.graph.mark_point()
        Thus an object that wants to accept a mark needs a method
        mark_point that returns the point on which the mark will be put.
        """
        from yanntricks.src.Constructors import Vector
        if self._central_point:
            return self._central_point
        if self.mark_point:
            mark_point = self.mark_point
        else:
            try:
                mark_point = self.graph.mark_point(pspict=pspict)
            except TypeError:
                # Happens when mark_point is redefined as a
                # 'lambda' function
                mark_point = self.graph.mark_point()

        # We are now going to compute the affine vector from the mark point
        # to the center of the mark.
        # It will be 'center_vector'
        # In a first time we compute it as there were no dilatations,
        # and then we will deform it to take xunit,yunit into account.

        if self.position:

            pspict = self.pspict
            position = self.position

            # The idea here is to allow to use the same point
            # in several pictures and to ask each figure to
            # remember the box size.
            if not isinstance(pspict, list):
                pspict = [pspict]

            for psp in pspict:
                dimx, dimy = psp.get_box_size(self.text, default_value="30pt")

            if position == "center":
                angle = self.angle.radian
                center_vector = Vector(
                    self.dist*cos(angle), self.dist*sin(angle))

            elif position == "corner":

                angle = numerical_approx(self.angle.radian)
                v = Vector(self.dist*cos(angle), self.dist*sin(angle))
                co = numerical_approx(cos(self.angle.radian))
                si = numerical_approx(sin(self.angle.radian))
                # The case co==0 or si==0 should not happen because
                # we already dealt with these angles and turned them
                # into "position=N,S,E,W" with angle==None.
                if co > 0:
                    lx = dimx/2
                else:
                    lx = -dimx/2
                if si > 0:
                    ly = dimy/2
                else:
                    ly = -dimy/2
                if self.dist < 0:
                    lx = -lx
                    ly = -ly
                center_vector = v+(lx, ly)
            elif position == "N":
                center_vector = Vector(0, -self.dist-dimy/2)
            elif position == "S":
                center_vector = Vector(0, self.dist+dimy/2)
            elif position == "W":
                center_vector = Vector(self.dist+dimx/2, 0)
            elif position == "E":
                center_vector = Vector(-self.dist-dimx/2, 0)

            elif position == "center_direction":

                # The algorithm is :
                # - we put the center of the box randomly on the right line
                #    (this is point Q)
                # - not completely at random : sufficiently far for the
                # box do not include the mark_point (this is the role of 'r')
                # - the vector 'w' joins 'mark_point' to the box
                # - in an ideal world, the length of 'w' would be 'dist'
                # - it is not because the box was put at random
                # - dist/w.length is the multiplicative factor for 'w'

                from yanntricks.src.BoundingBox import BoundingBox
                from yanntricks.src.affine_vector import AffineVector
                r = dimx+dimy
                v = Vector(r*cos(self.angle.radian), r*sin(self.angle.radian))
                Q = mark_point.translate(v)
                box = BoundingBox(xmin=Q.x-dimx/2, xmax=Q.x+dimx/2,
                                  ymin=Q.y-dimy/2, ymax=Q.y+dimy/2)

                I = point_to_box_intersection(mark_point, box)[0]
                IQ = AffineVector(I, Q)
                w = AffineVector(mark_point, I)

                factor = self.dist/w.length
                # 'new_w' this is the correct intersection between the line
                # and the box
                new_w = factor*w

                # 'IQ' is the correct vector from the intersection
                # to the center.

                # So the vector from the mark_point to the center of the box
                # is obtained putting 'IQ' at the end of 'new_w'
                center_vector = new_w.extend(IQ)

            else:
                raise ShouldNotHappenException(
                    "Something wrong. I think the 'position'\
argument is not good :"+position)

        else:      # if 'position' is not given
            center_vector = Vector(self.dist*cos(self.angle.radian),
                                   self.dist*sin(self.angle.radian))

        # Now we convert the 'center_vector' into a visual vector.

        # The following is completely arbitrary.
        # TODO : each mark should be associated with a picture.
        #        and here, 'pspict' should never be a list.
        if isinstance(pspict, list):
            xunit = pspict[0].xunit
            yunit = pspict[0].yunit
        else:
            xunit = pspict.xunit
            yunit = pspict.yunit
        visual_center_vector = Vector(center_vector.Dx/xunit,
                                      center_vector.Dy/yunit)

        cp = mark_point.translate(visual_center_vector)
        return cp

    def _math_bounding_box(self, pspict=None):
        # pylint:disable=no-self-use
        # pylint:disable=unused-argument
        from yanntricks.src.BoundingBox import BoundingBox
        return BoundingBox()

    def _bounding_box(self, pspict=None):  # pylint:disable=arguments-differ
        from yanntricks.src.point import Point
        from yanntricks.src.BoundingBox import BoundingBox
        central_point = self.central_point(pspict)
        if not central_point:
            raise TypeError("No central point. Parent =", self.parent)
        bb = BoundingBox(central_point, central_point)
        dimx, dimy = pspict.get_box_size(self.text)

        dimx = float(dimx)/pspict.xunit
        dimy = float(dimy)/pspict.yunit

        pt1 = Point(central_point.x-dimx/2, central_point.y-dimy/2)
        pt2 = Point(central_point.x+dimx/2, central_point.y+dimy/2)
        bb.add_object(pt1, pspict)
        bb.add_object(pt2, pspict)
        bb.parent = self
        return bb

    def tikz_code(self, pspict=None):
        """Return the tikz code of self in the given pspict."""
        central_point = self.central_point(pspict)

        code = r"\draw " + \
            central_point.coordinates(
                digits=5, pspict=pspict)+" node {"+self.text+"};"
        return code

    def latex_code(self, pspict, language=None):
        """Return the latex code of self in the given pspict."""
        if language == "tikz":
            return self.tikz_code(pspict)
        raise ValueError("We only do tikz here.")
