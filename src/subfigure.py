#########################################################################
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
#########################################################################

# copyright (c) Laurent Claessens, 2009-2017, 2019
# email: laurent@claessens-donadello.eu


# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=fixme

from yanntricks.src.Picture import Picture
from yanntricks.src.Utilities import latinize


class SubFigure:
    """
    This is a subfigure.

    If no label are given, a default one will be set when
    included in the figure.

    EXAMPLES

    .. literalinclude:: yanntricksSubFigure.py
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigFirstPICTFirstPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigSecondPICTSecondPoint-for_eps.png
    .. image:: Picture_FIGLabelFigSubFiguressLabelssFigThirdPICTthirdPoint-for_eps.png
    """

    def __init__(self, caption, name=None):
        self.caption = caption
        self.name = name
        self.record_pspicture = []
        self.mother = None

    def add_latex_line(self, ligne, separator_name):
        self.mother.add_latex_line(ligne, separator_name)

    def new_pspicture(self, name=None, pspict=None):
        if name is None:
            number = len(self.record_pspicture)
            name = "sub"+latinize(str(number))
        if pspict is None:
            pspict = Picture("FIG"+self.name+"PICT"+name)
        pspict.mother = self
        # The mother of a pspict inside a subfigure is the figure (not the subfigure)
        pspict.figure_mother = self.mother
        pspict.subfigure_mother = self
        self.add_pspicture(pspict)
        return pspict

    def subfigure_code(self):
        a = []
        for pspict in self.record_pspicture:
            a.append(pspict.latex_code())
        return "\n".join(a)

    def add_pspicture(self, pspicture):
        self.record_pspicture.append(pspicture)
