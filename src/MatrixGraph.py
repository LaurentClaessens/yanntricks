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

# copyright (c) Laurent Claessens, 2016-2017, 2019
# email: laurent@claessens-donadello.eu

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.Constructors import *


class MatrixElement(object):
    """
    A matrix element has three boxes.
    - text box : the bounding box of the text itself
    - first box : slightly larger box than the text box. If you want to draw a square around a part of the matrix, you should use this one
    - second box : slightly larger that the first one. The limit of the second box of one element is the same as the limit of the second box of the next element.
    """

    def __init__(self, text="", line=None, column=None, matrix=None):
        self.text = text
        if self.text == "":
            self.text = "$({},{})$".format(line, column)
        self.line = line
        self.column = column
        self.matrix = matrix
        self.central_point = None

    def getColumn(self):
        return self.matrix.getColumn(self.column)

    def getLine(self):
        return self.matrix.getLine(self.line)

    def getTextSize(self, pspict):
        return pspict.get_box_size(self.text)

    def getTextHeight(self, pspict):
        return self.getTextSize(pspict)[1]

    def getTextWidth(self, pspict):
        return self.getTextSize(pspict)[0]

    def getTextBox(self, pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        text_width, text_height = self.getTextSize(pspict)
        xmin = self.central_point.x-text_width/2
        xmax = self.central_point.x+text_width/2
        ymin = self.central_point.y-text_height/2
        ymax = self.central_point.y+text_height/2
        return BoundingBox(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    def getFirstBox(self, pspict):
        import Defaults
        from yanntricks.src.BoundingBox import BoundingBox
        text_box = self.getTextBox(pspict)
        xmin = text_box.xmin-Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER
        xmax = text_box.xmax+Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER
        ymin = text_box.ymin-Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER
        ymax = text_box.ymax+Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER
        return BoundingBox(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    def getSecondBox(self, pspict):
        import Defaults
        from yanntricks.src.BoundingBox import BoundingBox
        first_box = self.getFirstBox(pspict)
        xmin = first_box.xmin-Defaults.MATRIX_ELEMENT_SECOND_BOX_X_BORDER
        xmax = first_box.xmax+Defaults.MATRIX_ELEMENT_SECOND_BOX_X_BORDER
        ymin = first_box.ymin-Defaults.MATRIX_ELEMENT_SECOND_BOX_Y_BORDER
        ymax = first_box.ymax+Defaults.MATRIX_ELEMENT_SECOND_BOX_Y_BORDER
        return BoundingBox(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)


class MatrixLineColumn(object):
    def __init__(self, number, matrix):
        self.number = number
        self.matrix = matrix
        self._height = None
        self._width = None
        self.elements = {}

    def getHeight(self, pspict):
        import Defaults
        if self._height == None:
            h = max([el.getTextHeight(pspict) for el in self])
            self._height = h+2*(Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER +
                                Defaults.MATRIX_ELEMENT_SECOND_BOX_Y_BORDER)
        return self._height

    def getWidth(self, pspict):
        import Defaults
        if self._width == None:
            h = max([el.getTextWidth(pspict) for el in self])
            self._width = h+2*(Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER +
                               Defaults.MATRIX_ELEMENT_SECOND_BOX_X_BORDER)
        return self._width

    def getFirstBox(self, pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        xmin = min([el.getFirstBox(pspict).xmin for el in self])
        ymin = min([el.getFirstBox(pspict).ymin for el in self])
        xmax = max([el.getFirstBox(pspict).xmax for el in self])
        ymax = max([el.getFirstBox(pspict).ymax for el in self])
        return BoundingBox(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    def getSecondBox(self, pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        xmin = min([el.getSecondBox(pspict).xmin for el in self])
        ymin = min([el.getSecondBox(pspict).ymin for el in self])
        xmax = max([el.getSecondBox(pspict).xmax for el in self])
        ymax = max([el.getSecondBox(pspict).ymax for el in self])
        return BoundingBox(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    def __iter__(self):
        return self.elements.values().__iter__()


class MatrixGraph(ObjectGraph):
    """
    Lines and column are numbered from 1 to nlines/ncolumns
    """

    def __init__(self, nlines, ncolumns):
        ObjectGraph.__init__(self, self)
        self.nlines = nlines
        self.ncolumns = ncolumns
        self._computed_central_points = False
        self.elements = {}
        self._lines = {}
        self._columns = {}
        self.matrix_environment = "pmatrix"
        for i in range(1, nlines+1):
            for j in range(1, ncolumns+1):
                self.elements[i, j] = MatrixElement(line=i, column=j)

        # Line constructions
        for i in range(1, nlines+1):
            self._lines[i] = MatrixLineColumn(i, self)
            for j in range(1, ncolumns+1):
                self.getLine(i).elements[j] = self.getElement(i, j)
        # Column constructions
        for j in range(1, ncolumns+1):
            self._columns[j] = MatrixLineColumn(j, self)
            for i in range(1, nlines+1):
                self.getColumn(j).elements[i] = self.getElement(i, j)

    # \brief set the (LaTeX) environment of the matrix
    #
    # \param m_env (string) the name of the desired environment.
    #
    # This will typically be `pmatrix` (default), `vmatrix`
    # or something like that.
    def set_matrix_environment(self, m_env):
        self.matrix_environment = m_env

    def getElement(self, i, j):
        return self.elements[i, j]

    def getElements(self):
        return self.elements.values()

    def getLine(self, n):
        return self._lines[n]

    def getColumn(self, m):
        return self._columns[m]

    def getMidPoint(self, pspict):
        xmin = self.getColumn(1).getSecondBox(pspict).xmin
        xmax = self.getColumn(self.ncolumns).getSecondBox(pspict).xmax
        ymax = self.getLine(1).getSecondBox(pspict).ymax
        ymin = self.getLine(self.nlines).getSecondBox(pspict).ymin
        return Point((xmin+xmax)/2, (ymin+ymax)/2)

    def getSecondBox(self, pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        bb = BoundingBox()
        bb.append(self.getLine(1).getSecondBox(pspict), pspict=pspict)
        bb.append(self.getLine(self.nlines).getSecondBox(
            pspict), pspict=pspict)
        bb.append(self.getColumn(1).getSecondBox(pspict), pspict=pspict)
        bb.append(self.getColumn(self.ncolumns).getSecondBox(
            pspict), pspict=pspict)
        return bb

    def square(self, a, b, pspict):
        """
        'a' and 'b' are tuples (i,j) of integers.
        """
        self.computeCentralPoints(pspict)
        min_line = min(a[0], b[0])
        min_col = min(a[1], b[1])
        max_line = max(a[0], b[0])
        max_col = max(a[1], b[1])
        xmin = self.getColumn(min_col).getFirstBox(pspict).xmin
        ymin = self.getLine(max_line).getFirstBox(pspict).ymin
        xmax = self.getColumn(max_col).getFirstBox(pspict).xmax
        ymax = self.getLine(min_line).getFirstBox(pspict).ymax
        A = Point(xmin, ymax)
        B = Point(xmax, ymax)
        C = Point(xmax, ymin)
        D = Point(xmin, ymin)
        return Polygon(A, B, C, D)

    def computeCentralPoints(self, pspict):
        if not self._computed_central_points:
            y = 0
            for i in range(1, self.nlines+1):
                y = y-self.getLine(i).getHeight(pspict)/2
                x = 0
                for j in range(1, self.ncolumns+1):
                    x = x+self.getColumn(j).getWidth(pspict)/2
                    self.elements[i, j].central_point = Point(x, y)
                    x = x+self.getColumn(j).getWidth(pspict)/2
                y = y-self.getLine(i).getHeight(pspict)/2
        self._computed_central_points = True

    def _bounding_box(self, pspict=None):
        from yanntricks.src.BoundingBox import BoundingBox
        return BoundingBox()

    def action_on_pspict(self, pspict):
        self.computeCentralPoints(pspict)

        # The parenthesis of the matrix will be adapted to the second box.
        # Thus we create them as a pmatrix (in the LaTeX sense)
        # that contains a rule of the computed dimensions.
        second_box = self.getSecondBox(pspict)
        Vx = second_box.xmax-second_box.xmin
        Vy = second_box.ymax-second_box.ymin
        matrix_code = r"""\rule{{ {}  }}{{{}}}""".format(
            str(Vx)+"cm",
            str(Vy)+"cm")

        P = self.getMidPoint(pspict)
        P.parameters.symbol = ""
        fake_matrix = r"""$
        \begin{MATRIX_ENV}
        \phantom{
        \begin{matrix}
        MATRIX_CODE
        \end{matrix}
        }
        \end{MATRIX_ENV}$
        """.replace("MATRIX_CODE", matrix_code).replace("MATRIX_ENV", self.matrix_environment)
        P.put_mark(0, angle=0, text=fake_matrix,
                   pspict=pspict, position="center")
        pspict.DrawGraphs(P)

        for i in range(1, self.nlines+1):
            for j in range(1, self.ncolumns+1):
                P = self.elements[i, j].central_point
                P.put_mark(
                    0, angle=0, text=self.elements[i, j].text, pspict=pspict, position="center")
                P.parameters.symbol = ""
                pspict.DrawGraphs(P)
