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

from sage.all import pi, sqrt, SR

from yanntricks.src.Visual import visual_polar
from yanntricks.src.degree_unit import degree
from yanntricks.src.ObjectGraph import Options
from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.MathStructures import AxesUnit
from yanntricks.src.SmallComputations import RemoveLastZeros
from yanntricks.src.affine_vector import AffineVector
from yanntricks.src.segment import Segment


class SingleAxe(ObjectGraph):
    """
    Describe an axe.

    INPUT:

    - ``C`` - the center of the axe. This is the point corresponding to the "zero" coordinate
    - ``base`` - the unit of the axe. This indicates

                1. the direction
                2. the size of "1"

        A mark will be added at each integer multiple of that vector 
        (but zero) including negative.
    - ``mx`` - the multiple of ``base`` at which the axe begins.
                This is typically negative
    - ``Mx`` -  the multiple of ``base`` at which the axe ends. 
                This is typically positive

    The axe goes from ``C+mx*base`` to ``C-Mx*base``. 

    OTHER CONTROLS :

    The default behaviour can be modified by the following attributes.

    - ``self.Dx`` - (default=1) A mark is written each multiple of ``self.Dx*base``.
    - ``self.mark_angle`` - the angle in degree under which the mark are written. By default this is orthogonal
                        to the direction given by ``self.base``.

        If an user-defined axes_unit is given, the length of ``base`` is "forgotten"
        """
    def __init__(self, C, base, mx, Mx, pspict=None):
        ObjectGraph.__init__(self, self)
        self.C = C
        self.base = base
        self.mx = mx
        self.Mx = Mx
        self.pspict = pspict
        self.options = Options()
        self.IsLabel = False
        self.axes_unit = AxesUnit(self.base.length, "")
        self.Dx = 1
        self.arrows = "->"
        self.graduation = True
        self.numbering = True
        self.imposed_graduation = []
        self.mark_origin = True
        self.mark = None
        self.mark_angle = degree(base.angle().radian-pi/2)
        self.enlarge_size = 0.5

        # The `conclude` method performs the last computations before
        # to be drawn. The graduation bars are added there.
        self._already_concluded = False

    # SingleAxe.segment cannot be a lazy attribute because
    # we use it for some projections before to compute the bounding box.
    def segment(self, projection=False, pspict=None):
        if self.mx == 0 and self.Mx == 0:
            # I think that we only pass here in order either to do
            # a projection either to create an initial bounding box.
            # If xunit or yunit are very low, then returning something like
            #   Segment(self.C-self.base.visual_length(1,pspict=pspict),self.C+self.base.visual_length(1,pspict=pspict))
            # causes bounding box to be too large.
            # This is why I return a small segment.

            if projection:
                return Segment(self.C, self.C.translate(self.base))
            else:
                return Segment(self.C.translate(-self.base.normalize(1)), self.C.translate(self.base.normalize(1)))

        # The axes have to cross at (0,0)
        if self.mx > 0:
            self.mx = 0
        return Segment(self.C.translate(self.mx*self.base),
                       self.C.translate(self.Mx*self.base))

    def add_option(self, opt):
        self.options.add_option(opt)

    def mark_point(self, pspict=None):
        return self.segment().F

    def no_numbering(self):
        self.numbering = False

    def no_graduation(self):
        self.graduation = False

    def enlarge_a_little(self, l, xunit=None, yunit=None, pspict=None):
        """
        return the tuple (mx,Mx) that correspond to axes of length
        `l` more than self (in both directions)
        """
        if pspict:
            xunit = pspict.xunit
            yunit = pspict.yunit
        seg = self.segment(pspict=pspict)
        # The aim is to find the multiple of the base vector
        # that has length `l`.
        vx = self.base.F.x
        vy = self.base.F.y

        k = l/sqrt((vx*xunit)**2+(vy*yunit)**2)
        mx = self.mx-k
        Mx = self.Mx+k
        return mx, Mx

    def graduation_bars(self, pspict):
        """
        Return the list of bars that makes the graduation of the axes

        By default, it is one at each multiple of self.base. If an user-defined axes_unit is given, then self.base is modified.

        This function also enlarges the axe by half a *visual* centimeter.
        """
        # bars_list contains in the same time marks (for the numbering) and segments (for the bars itself)
        if not self.graduation:
            return []
        bars_list = []
        bar_angle = SR(self.mark_angle).n(digits=7)  # Latex does not accept
        # too much digits.
        for x, symbol in self.axes_unit.place_list(self.mx, self.Mx, self.Dx, self.mark_origin):
            P = (x*self.base).F
            if self.numbering:
                # The 0.2 here is hard coded in Histogram, see 71011299

                mark_angle = self.mark_angle
                if self.segment().is_horizontal:
                    position = "N"
                    mark_angle = None
                if self.segment().is_vertical:
                    position = "E"
                    mark_angle = None
                m = P.get_mark(0.2, mark_angle, symbol, pspict=pspict,
                               position=position)
                bars_list.append(m)

            a = visual_polar(P, 0.1, bar_angle, pspict)
            b = visual_polar(P, 0.1, bar_angle+180, pspict)
            seg = Segment(a, b)
            bars_list.append(seg)
        return bars_list

    def _bounding_box(self, pspict):
        # One cannot take into account the small enlarging here because
        # we do not know if this is the vertical or horizontal axe,
        # so we cannot make the fit of the drawn objects.
        BB = self.math_bounding_box(pspict)

        for graph in self.added_objects[pspict]:
            BB.append(graph, pspict)
        return BB

    def _math_bounding_box(self, pspict):
        # The math_bounding box does not take into account the things
        # that are inside the picture (not even if this are default axes)
        from yanntricks.src.BoundingBox import BoundingBox
        bb = BoundingBox()
        for x, symbol in self.axes_unit.place_list(self.mx, self.Mx,
                                                   self.Dx, self.mark_origin):
            P = (x*self.base).F
            bb.addX(P.x)
            bb.addY(P.y)
        return bb

    def conclude(self, pspict):
        """
        From the possibility of drawing default axes, the parameters like
        the length of the axes are unknown up to the last moment. The axe is 
        created in the same time as the picture, but the mark bars for example
        can only be computed after all the other objects.
        So we need to make some ultimate settings before to be drawn.
        This function is called by `Picture._DrawGraph`, right before
        to compute and add the bounding box and to call `action_on_pspict`.
        """
        if self.mark:
            self.added_objects.append(pspict, self.mark)
        if self.graduation:
            for graph in self.graduation_bars(pspict):
                self.added_objects.append(pspict, graph)
        self._already_concluded = True

    def action_on_pspict(self, pspict):
        sDx = RemoveLastZeros(self.Dx, 10)
        self.add_option("Dx="+sDx)
        v = AffineVector(self.segment(pspict=pspict))
        pspict.DrawGraphs(v, separator_name="AXES")

    def __str__(self):
        return "<SingleAxeGraph: C={0} base={1} mx={2} Mx={3}>".format(
            self.C, self.base, self.mx, self.Mx)
