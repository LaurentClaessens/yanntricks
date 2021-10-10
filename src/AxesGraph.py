# copyright (c) Laurent Claessens, 2010-2017, 2019, 2021
# email: laurent@claessens-donadello.eu

from yanntricks.src.SingleAxeGraph import SingleAxe
from yanntricks.src.ObjectGraph import Options
from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.MathStructures import AxesUnit
from yanntricks.src.SmallComputations import RemoveLastZeros


dprint = print


class Axes(ObjectGraph):
    def __init__(self, C, bb, pspict=None):
        # if a pspicture is passed, these axes will be considered as the
        # default axes system of `pspict`. This has an influence in the
        # computation of the bounding box.
        from yanntricks.src.Constructors import Vector
        ObjectGraph.__init__(self, self)
        self.take_math_BB = False
        self.C = C

        self.BB = bb.copy()

        self.pspict = pspict
        self.options = Options()
        self.Dx = 1
        self.Dy = 1
        self.arrows = "->"
        self.separator_name = "AXES"
        self.graduation = True
        self.numbering = True
        # Since the size of the axe is given in multiple of self.base,
        # one cannot give mx=-1000 as "minimal value".
        self.single_axeX = SingleAxe(
            self.C, Vector(1, 0), 0, 0, pspict=self.pspict)
        self.single_axeX.mark_origin = False
        self.single_axeX.axes_unit = AxesUnit(1, "")
        self.draw_single_axeX = True
        self.single_axeY = SingleAxe(
            self.C, Vector(0, 1), 0, 0, pspict=self.pspict)
        self.single_axeY.mark_origin = False
        self.single_axeY.axes_unit = AxesUnit(1, "")
        self.single_axeY.mark_angle = 180
        self.draw_single_axeY = True
        self.single_axeX.Dx = self.Dx
        self.single_axeY.Dx = self.Dy
        self.already_enlarged = False
        self.enlarge_size = 0.5
        self.do_enlarge = True
        self.do_mx_enlarge = True
        self.do_my_enlarge = True
        self.do_Mx_enlarge = True
        self.do_My_enlarge = True

    def enlarge_a_little(self, length, pspict):
        from yanntricks.src.Exceptions import AlreadyEnlargedException
        if self.already_enlarged:
            raise AlreadyEnlargedException("I'm already enlarged")
        self.already_enlarged = True
        mx, Mx = self.single_axeX.enlarge_a_little(length, pspict=pspict)
        if self.do_mx_enlarge:
            self.single_axeX.mx = mx
        if self.do_Mx_enlarge:
            self.single_axeX.Mx = Mx

        my, My = self.single_axeY.enlarge_a_little(length, pspict=pspict)
        if self.do_my_enlarge:
            self.single_axeY.mx = my
        if self.do_My_enlarge:
            self.single_axeY.Mx = My

    def add_bounding_box(self, BB, pspict):
        """
        Modify the mx and Mx of each single axes X and Y in order to
        fit the given BB.

        This is only supposed to work with automatic axes because
        if assumes that these are vertical and horizontal.
        """
        if not BB.take_math_BB:
            return
        axeX = self.single_axeX
        axeY = self.single_axeY

        axeX.mx = min((BB.xmin-axeX.C.x)/axeX.base.F.x, axeX.mx)
        axeX.Mx = max((BB.xmax-axeX.C.x)/axeX.base.F.x, axeX.Mx)
        axeY.mx = min((BB.ymin-axeY.C.y)/axeY.base.F.y, axeY.mx)
        axeY.Mx = max((BB.ymax-axeY.C.y)/axeY.base.F.y, axeY.Mx)


    def add_option(self, opt):
        self.options.add_option(opt)

    def no_graduation(self):
        self.single_axeX.no_graduation()
        self.single_axeY.no_graduation()

    def no_numbering(self):
        self.single_axeX.no_numbering()
        self.single_axeY.no_numbering()

    def _bounding_box(self, pspict=None):
        """
        return the bounding box of the axes.

        If `self` is a default axe, it take into account the
        content of the pspicture and update the mx,my of the
        single axes X and Y.
        """
        from yanntricks.src.BoundingBox import BoundingBox
        BB = BoundingBox()
        BB.append(self.single_axeX.bounding_box(pspict), pspict)
        BB.append(self.single_axeY.bounding_box(pspict), pspict)

        if self.pspict:
            BB.append(self.pspict.math_bounding_box(), pspict)
        # Update the single axes taking the content of pspict into account.
        self.add_bounding_box(BB, pspict)
        BB.check_too_large()
        return BB

    def _math_bounding_box(self, pspict=None):
        from yanntricks.src.BoundingBox import BoundingBox
        BB = BoundingBox()
        BB.append(self.single_axeX.bounding_box(pspict), pspict)
        BB.append(self.single_axeY.bounding_box(pspict), pspict)

        if self.pspict:
            BB.append(self.pspict.math_bounding_box(), pspict)
        # Updates the single axes taking the content of pspict into account.
        self.add_bounding_box(BB, pspict)
        BB.check_too_large()
        return BB

    def action_on_pspict(self, language=None, pspict=None):
        sDx = RemoveLastZeros(self.Dx, 10)
        sDy = RemoveLastZeros(self.Dy, 10)
        self.add_option("Dx="+sDx)
        self.add_option("Dy="+sDy)

        self.single_axeX.Mx = self.BB.xmax
        self.single_axeX.mx = self.BB.xmin
        self.single_axeY.Mx = self.BB.ymax
        self.single_axeY.mx = self.BB.ymin

        if self.do_enlarge:
            self.enlarge_a_little(self.enlarge_size, pspict=pspict)
        if self.draw_single_axeX:
            pspict.DrawGraphs(self.single_axeX, separator_name="AXES")
        if self.draw_single_axeY:
            pspict.DrawGraphs(self.single_axeY, separator_name="AXES")
