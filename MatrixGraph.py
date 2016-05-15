# -*- coding: utf8 -*-

###########################################################################
#   This is part of the module phystricks
#
#   phystricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   phystricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with phystricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2016
# email: laurent@claessens-donadello.eu

from __future__ import division

from sage.all import *

from ObjectGraph import ObjectGraph
from Constructors import *

class MatrixElement(object):
    """
    A matrix element has three boxes.
    - text box : the bounding box of the text itself
    - first box : slightly larger box than the text box. If you want to draw a square around a part of the matrix, you should use this one
    - second box : slightly larger that the first one. The limit of the second box of one element is the same as the limit of the second box of the next element.
    """
    def __init__(self,text):
        self.text=text
        self.central_point=Point(0,0)
    def getTextSize(self,pspict):
        return pspict.get_box_size(self.text)
    def getTextHeight(self,pspict):
        return self.getTextSize(pspict)[1]
    def getTextWidth(self,pspict):
        return self.getTextSize(pspict)[0]
    def getTextBox(self,pspict):
        text_width,text_height=self.getTextSize(pspict)
        xmin=self.central_point.x-text_width/2
        xmax=self.central_point.x+text_width/2
        ymin=self.central_point.y-text_width/2
        ymax=self.central_point.y+text_width/2
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    def getFirstBox(self,pspict):
        text_box=self.getTextBox(pspict)
        xmin=text_box.xmin-Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        xmax=text_box.xmax+Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        ymin=text_box.ymin-Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        ymax=text_box.ymax+Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    def getSecondBox(self,pspict):
        import Defaults
        first_box=self.getFirstBox(pspict)
        xmin=text_box.xmin-Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        xmax=text_box.xmax+Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        ymin=text_box.ymin-Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        ymax=text_box.ymax+Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)


class MatrixGraph(ObjectGraph):
    """
    Lines and column are numbered from 1 to nlines/ncolumns
    """
    def __init__(self,nlines,ncolumns):
        ObjectGraph.__init__(self,self)
        self.nlines=nlines
        self.ncolumns=ncolumns
        self.elements={}
        self.column_width={}
        self.line_heigth={}
        for i in range(1,self.nlines+1):
            self.line_heigth[i]=None
        for i in range(1,self.ncolumns+1):
            self.column_width[i]=None
        for i in range(1,self.nlines+1):
            for j in range (1,self.ncolumns+1):
                self.elements[i,j]=MatrixElement("$({},{})$".format(i,j))

    def getLine(self,n):
        """ return the list of matrix elements on line number 'n' """
        return [  self.elements[n,j] for j in range(1,self.nlines+1)  ]
    def getColumn(self,m):
        """ return the list of matrix elements on line number 'n' """
        return [  self.elements[i,m] for i in range(1,self.ncolumns+1)  ]
    def getLineHeigth(self,n,pspict):
        import Defaults
        if self.line_heigth[n] == None:
            h=max( [  el.getTextHeight(pspict) for el in self.getLine(n)  ])
            self.line_heigth[n]=h+2*(Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER+Defaults.MATRIX_ELEMENT_SECOND_BOX_BORDER)
        return self.line_heigth[n]
    def getColumnWidth(self,m,pspict):
        import Defaults
        if self.column_width[m] == None:
            h=max( [  el.getTextWidth(pspict) for el in self.getColumn(m)  ])
            self.column_width[m]=h+2*(Defaults.MATRIX_ELEMENT_FIRST_BOX_BORDER+Defaults.MATRIX_ELEMENT_SECOND_BOX_BORDER)
        return self.column_width[m]

    def action_on_pspict(self,pspict):
        P=Point(0,0)
        pspict.DrawGraphs(P)
