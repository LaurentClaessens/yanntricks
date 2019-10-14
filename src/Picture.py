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


#pylint: disable=invalid-name
#pylint: disable=missing-function-docstring
#pylint: disable=missing-module-docstring
#pylint: disable=too-many-arguments
#pylint: disable=too-many-public-methods
#pylint: disable=fixme

import os
import collections
from sage.all import numerical_approx

from phystricks.src.Separator import SeparatorList
from phystricks.src.ObjectGraph import DrawElement
from phystricks.src.Constructors import Axes, Grid
from phystricks.src.point import Point
from phystricks.src.AuxFile import AuxFile
from phystricks.src.BoundingBox import BoundingBox
from phystricks.src.phyFunctionGraph import phyFunctionGraph
from phystricks.src.Exceptions import NotObjectGraphException
from phystricks.src.Utilities import sublist
from phystricks.src.Exceptions import ShouldNotHappenException
from phystricks.src.Utilities import add_latex_line_entete
from phystricks.src.NoMathUtilities import SubdirectoryFilenames


class Picture(object):
    r"""
    Describe a Picture

    METHODS:

    - `self.latex_code()` - contains the tikz code of what has to be between \begin{tikz} and \end{tikz}. This is not the environment itself, neither the definition of xunit, yunit.

    - `self.latex_code_for_eps()` - the LaTeX code that produces the eps file. This function calls `self.contenu_pstricks`

    - `self.latex_code_for_png()` - the same.

    - `self.latex_code_for_contenu_pdf()` - the same.

    The name of the pspict is used to produce intermediate filesnames, and other names.
    """

    def __init__(self, name="CAN_BE_A_PROBLEM_IF_TRY_TO_PRODUCE_EPS_OR_PDF"):
        r"""

        - `self.BB` is the bounding box for LaTeX purpose.

        - `self.math_BB` is the bounding box of objects that are "mathematically relevant". This bounding box does not take into account
            marks of points and thinks like that. This is the bounding box that is going to be used for the axes and the grid.
            When a graph object has a method math_bounding_box, this is the one taken into account in the math_BB here.
        """
        self.name = name
        # for the intermediate files.

        # A comment. This is not used to create the picture;
        # the purpose is to remember a specific feature to be
        # tested when recompiling.
        self.comment = ""

        self.tikzfilename = SubdirectoryFilenames("tikz"+self.name).from_here()

        self.mother = None
        self.figure_mother = None
        self.language = "tikz"
        self.pstricks_code_list = []
        self.newwriteDone = False

        # self.interWriteFile is redefined in MultiplePictures

        self.record_marks = []
        self.record_bounding_box = []
        self.record_draw_graph = []
        self.record_draw_bb = []
        self.record_force_math_bounding_box = []
        # self.record_math_BB=[]
        # self.record_BB=[]
        self.counterDone = False
        self.newlengthDone = False
        self.listePoint = []
        self.xunit = 1
        self.yunit = 1
        self.xsize = None
        self.ysize = None
        self.rotation_angle = None
        self.LabelSep = 1
        self.BB = BoundingBox(mother=self)
        self.math_BB = BoundingBox(is_math=True)
        # self.BB and self.math_BB serve to add some objects by hand.
        # If you need the bounding box, use self.bounding_box()
        # or self.math_bounding_box()
        self.axes = Axes(Point(0, 0), BoundingBox(), pspict=self)
        self.single_axeX = self.axes.single_axeX
        self.single_axeY = self.axes.single_axeY
        self.single_axeX.pspict = self
        self.single_axeY.pspict = self
        self.draw_default_axes = False

        self.mx_acceptable_BB = -100
        self.my_acceptable_BB = -100
        self.Mx_acceptable_BB = 100
        self.My_acceptable_BB = 100

        self.grid = Grid(BoundingBox())

        # The order of declaration is important, because it is recorded in the Separator.number attribute.
        self.separator_list = SeparatorList()
        self.separator_list.new_separator("ENTETE PSPICTURE")
        self.separator_list.new_separator("OPEN_WRITE_AND_LABEL")
        self.separator_list.new_separator("WRITE_AND_LABEL")
        self.separator_list.new_separator("CLOSE_WRITE_AND_LABEL")
        self.separator_list.new_separator("BEFORE PSPICTURE")
        # This separator is supposed to contain only \begin{pspicture}
        self.separator_list.new_separator("BEGIN PSPICTURE")
        self.separator_list.new_separator("GRID")
        self.separator_list.new_separator("AXES")
        self.separator_list.new_separator("OTHER STUFF")
        self.separator_list.new_separator("DEFAULT")
        self.separator_list.new_separator("END PSPICTURE")
        self.separator_list.new_separator("AFTER PSPICTURE")

        self.entete_position = "ENTETE PSPICTURE"

        self.auxiliary_file = AuxFile(self.name, picture=self)

        # self.add_latex_line(self.name,"AFTER PSPICTURE")        # testing

    def tikz_code(self):
        """
        It also remove the tikz externalize file.
        """
        self.create_latex_code(language="tikz", pspict=self)
        add_latex_line_entete(self)
        self.add_latex_line("\\tikzsetnextfilename{{{0}}}".format(
            self.tikzfilename), "BEGIN PSPICTURE")
        self.add_latex_line("\\begin{{tikzpicture}}[xscale={0},yscale={1},inner sep=2.25pt,outer sep=0pt]".format(
            1, 1), "BEGIN PSPICTURE")
        self.add_latex_line("\\end{tikzpicture}", "END PSPICTURE")

        self.xsize = self.bounding_box(pspict=self).xsize()
        self.ysize = self.bounding_box(pspict=self).ysize()
        return self.separator_list.code()

    def visual_xsize(self):
        return numerical_approx(self.xsize*self.xunit)

    def visual_ysize(self):
        return numerical_approx(self.ysize*self.yunit)

    def create_latex_code(self, language=None, pspict=None):
        """
        Fix the bounding box and create the separator "PSTRICKS CODE".

        NOTES :

        - This function is not supposed to be used twice. In fact, this is
          supposed to be called only from `lazy_attributes`

        """
        # Here we are supposed to be  sure of the xunit, yunit, so we can compute the BB's needed for the points with marks.
        # For the same reason, all the marks that were asked to be drawn are added now.
        # Most of the difficulty is when the user use pspicture.dilatation_X and Y with different coefficients.
        # TODO : take it into account.

        list_to_be_drawn = [a for a in self.record_draw_graph if a.take_graph]

        # The following is only for testing purpose :
        for a in self.record_draw_graph:
            if not a.take_graph:
                raise

        list_used_separators = []

        # STEP : update the bounding box
        for x in list_to_be_drawn:
            self.BB.append(x.graph, self)

            # The math_BB is updated in DrawGraph    February 21, 2015
            # This allow to enlarge the BB by hand with something like
            #    pspict.math_BB.ymax+=1
            # placed after DrawGraph

        # STEP : add the LaTeX code of each element
        for x in list_to_be_drawn:
            graph = x.graph

            # If the graph is a bounding box of a mark, we recompute it
            # because a dilatation of the figure could have
            # changed the bounding box.
            # Same for the bounding box of the pspicture, since it is not know before now
            if isinstance(graph, BoundingBox):
                if graph.mother:
                    print("I'm drawing the bounding box of ", graph.mother)
                    graph = graph.mother.bounding_box(self)
            separator_name = x.separator_name
            try:
                self.add_latex_line(ligne=graph.latex_code(
                    language=self.language, pspict=self), separator_name=separator_name)
                list_used_separators.append(separator_name)
            except AttributeError as data:
                if not "latex_code" in dir(graph):
                    print(
                        "phystricks error: object %s has no pstricks_code method" % (str(graph)))
                raise
        self.separator_list.fusion(list_used_separators, "PSTRICKS CODE")

    def test_dilatation_first(self, fact):
        """
        Return True if nothing is already done on the picture.

        The dilatation has to be the first information given to a pictute. The aim of this function is to raise an exception when one tries to use
        pspict.dilatation(...)
        after having used 'DrawGraphs'
        """
        if not self.record_draw_graph == [] and fact != 1:
            raise ShouldNotHappenException("Dilatation has to be \
given right after the creation of the picture.")

    def dilatation(self, fact):
        self.dilatation_X(fact)
        self.dilatation_Y(fact)

    def dilatation_X(self, fact):
        self.test_dilatation_first(fact)
        self.xunit = self.xunit * fact

    def dilatation_Y(self, fact):
        self.test_dilatation_first(fact)
        self.yunit = self.yunit * fact

    def rotation(self, angle):
        self.rotation_angle = angle

    def fixe_tailleX(self, l):
        self.dilatation_X(l/self.BB.tailleX())

    def fixe_tailleY(self, l):
        self.dilatation_Y(l/self.BB.tailleY())

    def AddPoint(self, P):
        self.add_latex_line(self.CodeAddPoint(P))

    def math_bounding_box(self, pspict=None):
        """
        Update and return the math bounding box of the picture.
        """
        pspict= pspict or self
        math_list = [x.graph for x in self.record_draw_graph]
        math_list.extend(self.record_force_math_bounding_box)
        for a in [g for g in math_list if g.take_math_BB]:
            self.math_BB.AddBB(a.math_bounding_box(pspict=pspict))
        return self.math_BB

    def bounding_box(self, pspict=None):
        """Update and return the bounding box of the picture."""
        # The math bounding box of the picture has to be computed in the
        # function 'DrawDefaultAxes'. But the axes themselves have
        # to be taken into account in the bounding box of the picture.
        pspict = pspict or self

        self.BB.append(self.math_bounding_box(), pspict=pspict)

        def condition(x):
            if x.take_BB:
                return True
            if x.take_math_BB:
                return True
            return False

        for a in sublist(self.record_draw_graph, condition):
            self.BB.AddBB(a.graph.bounding_box(pspict=pspict))
        return self.BB

    def DrawBoundingBox(self, obj=None):
        """Draw the bounding box of the object.

        Draw the bounding box of the object when it
        has a method bounding_box

        If not, assume that the object is the bounding box to be drawn.
        If no object are given, draw its own bounding box
        """
        if not obj:
            obj = self
        self.record_bounding_box.append(obj)

    def deal_with_graph(self, gr, separator_name):
        from phystricks.src.ObjectGraph import AddedObjects
        if isinstance(gr, AddedObjects):
            self.DrawGraphs(gr[self])
            return None
        if isinstance(gr, collections.Iterable):
            for h in gr:
                self.DrawGraphs(h, separator_name=separator_name)
            return None
        self._DrawGraph(gr, separator_name=separator_name)
        return None

    def DrawGraphs(self, *args, **arg):
        """
        The function DrawGraphs basically takes a list of objects and performs
        different kind of operation following the type of each "object" :

        If the object it iterable, its elements are re-passed to DrawGraphs
        If the object is an instance of "ObjectGraph", it is passed to
        _DrawGraph
        If the object is 'AddedObject', the list corresponding to 'self' is
        re-passed to DrawGraphs.

    """
        if "separator_name" not in arg:
            separator_name = "DEFAULT"
        else:
            separator_name = arg["separator_name"]

        # Here is why objects intended to be drawn cannot be iterable.
        # Position 30282-11562
        for gr in args:
            self.deal_with_graph(gr, separator_name)

    def _DrawGraph(self, graph, separator_name=None):
        """
        Draw an object of type `<Something>Graph`.

        More generally, it can draw anything that has the methods

            1. bounding_box
            2. tikz_code

        The first one should return a bounding box and the second one should return a valid tikz code as string.

        NOTE:

        More precisely, it does not draw the object now, but it add it (and its mark if applicable) to ``self.record_draw_graph`` which is the list of objects to be drawn. Thus it is still possible to modify the object later (even if extremely discouraged).
        """
        from phystricks.src.ObjectGraph import ObjectGraph
        if not isinstance(graph, ObjectGraph):
            raise NotObjectGraphException(graph)

        if isinstance(graph, phyFunctionGraph):
            if graph.mx is None or graph.Mx is None:
                raise TypeError("You cannot draw phyFunction but only graph.")
        if separator_name is None:
            try:
                separator_name = graph.separator_name
            except AttributeError:
                separator_name = "DEFAULT"
        x = DrawElement(graph, separator_name)
        self.record_draw_graph.append(x)

        # If an object has a mark, it the latter is already
        # in the 'added_objects' list and the mark is already passed
        # to a DrawGraph. Adding here the mark to the "record_draw_graph"
        # list make pass twice by the computation of its bounding box
        # (and draw it twice)
        # Augustus 8, 2016
        # See position 3598-30738

        graph.conclude(self)
        self.math_BB.append(graph, self)
        graph._draw_added_objects(self) # pylint:disable=protected-access
        graph.action_on_pspict(pspict=self)

    def DrawDefaultAxes(self):
        """
        This function computes the bounding box of the axes and add
        them to the list to be drawn.

        The length of the axes is computed here
        (via self.math_bounding_box).

        Sometimes you want the axes to be slightly larger. You can impose
        the length of the axes.
        """
        self.axes.BB = self.math_bounding_box(pspict=self)
        self.DrawGraphs(self.axes)

    def DrawDefaultGrid(self):
        self.grid.BB = self.math_bounding_box(pspict=self)
        Dx = self.grid.Dx
        Dy = self.grid.Dy
        # Make the grid end on its "big" subdivisions.
        from SmallComputations import MultipleLower, MultipleBigger
        self.grid.BB.xmin = MultipleLower(self.grid.BB.xmin, Dx)
        self.grid.BB.xmax = MultipleBigger(self.grid.BB.xmax, Dx)
        self.grid.BB.ymin = MultipleLower(self.grid.BB.ymin, Dy)
        self.grid.BB.ymax = MultipleBigger(self.grid.BB.ymax, Dy)
        self.DrawGraphs(self.grid)

    def get_box_size(self, tex_expression, default_value="0pt"):
        return self.auxiliary_file.get_box_size(tex_expression, default_value)

    def add_latex_line(self, ligne, separator_name="DEFAULT", add_line_jump=True):
        """
        Add a line in the pstricks code. The optional argument <position> is the name of a marker like %GRID, %AXES, ...
        """
        if separator_name is None:
            separator_name = "DEFAULT"
        self.separator_list[separator_name].add_latex_line(
            ligne, add_line_jump=add_line_jump)

    def force_math_bounding_box(self, g):
        """
        Add an object to the math bounding box of the pspicture. This object will not be drawn, but the axes and the grid will take it into account.
        """
        self.record_force_math_bounding_box.append(g)

    def test_if_test_file_is_present(self):
        from SmallComputations import Fichier
        test_file = Fichier(
            "test_pspict_LaTeX_%s.tmp" % (self.name))
        return os.path.isfile(test_file.filename)

    def latex_code(self):
        """Return the LaTeX code of the pspicture"""
        self.add_latex_line(
            self.auxiliary_file.open_latex_code(), "OPEN_WRITE_AND_LABEL")
        self.add_latex_line(
            self.auxiliary_file.latex_code(), "WRITE_AND_LABEL")
        self.add_latex_line(
            self.auxiliary_file.close_latex_code(), "CLOSE_WRITE_AND_LABEL")
        if self.language == "tikz":
            return self.tikz_code()
        raise NameError(f"Unknown language {self.language}."
                        f" tikz is the only one.")
