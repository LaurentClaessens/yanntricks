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
    def __init__(self,text,line,column,matrix):
        self.text=text
        self.line=line
        self.column=column
        self.matrix=matrix
        self.central_point=None
    def getColumn(self):
        return self.matrix.getColumn(self.column)
    def getLine(self):
        return self.matrix.getLine(self.line)
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
        ymin=self.central_point.y-text_height/2
        ymax=self.central_point.y+text_height/2
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    def getFirstBox(self,pspict):
        text_box=self.getTextBox(pspict)
        xmin=text_box.xmin-Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER
        xmax=text_box.xmax+Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER
        ymin=text_box.ymin-Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER
        ymax=text_box.ymax+Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    def getSecondBox(self,pspict):
        import Defaults
        first_box=self.getFirstBox(pspict)
        xmin=text_box.xmin-Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER
        xmax=text_box.xmax+Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER
        ymin=text_box.ymin-Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER
        ymax=text_box.ymax+Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)

class MatrixLineColumn(object):
    def __init__(self,number,matrix):
        self.number=number
        self.matrix=matrix
        self._height=None
        self._width=None
        self.elements=None
    def getHeight(self,pspict):
        import Defaults
        if self._height==None:
            h=max( [  el.getTextHeight(pspict) for el in self ])
            self._height=h+2*(Defaults.MATRIX_ELEMENT_FIRST_BOX_Y_BORDER+Defaults.MATRIX_ELEMENT_SECOND_BOX_Y_BORDER)
        return self._height
    def getWidth(self,pspict):
        import Defaults
        if self._width==None:
            h=max( [  el.getTextWidth(pspict) for el in self ])
            self._width=h+2*(Defaults.MATRIX_ELEMENT_FIRST_BOX_X_BORDER+Defaults.MATRIX_ELEMENT_SECOND_BOX_X_BORDER)
        return self._width
    def __iter__(self):
        return self.elements.__iter__()

class MatrixGraph(ObjectGraph):
    """
    Lines and column are numbered from 1 to nlines/ncolumns
    """
    def __init__(self,nlines,ncolumns):
        ObjectGraph.__init__(self,self)
        self.nlines=nlines
        self.ncolumns=ncolumns
        self.elements={}
        self.lines={}
        self.columns={}
        for i in range(1,self.nlines+1):
            for j in range (1,self.ncolumns+1):
                self.elements[i,j]=MatrixElement("$({},{})$".format(i,j),line=i,column=j,matrix=self)
        for i in range(1,self.nlines+1):
            line=MatrixLineColumn(i,self)
            line.elements=[  self.elements[i,j] for j in range(1,self.ncolumns+1)  ]
            self.lines[i]=line
        for j in range(1,self.ncolumns+1):
            col=MatrixLineColumn(j,self)
            col.elements=[  self.elements[i,j] for i in range(1,self.nlines+1)  ]
            self.columns[j]=col
    def getMidPoint(self,pspict):
        bb=self.elements[1,1].getTextBox(pspict)
        xmin=self.elements[1,1].getTextBox(pspict).xmin
        xmax=self.elements[1,self.ncolumns].getTextBox(pspict).xmax
        ymin=self.elements[1,1].getTextBox(pspict).ymin
        ymax=self.elements[self.nlines,self.ncolumns].getTextBox(pspict).ymax
        return Point((xmin+xmax)/2,(ymin+ymax)/2)
    def getLine(self,n):
        return self.lines[n]
    def getColumn(self,m):
        return self.columns[m]
    def computeCentralPoints(self,pspict):
        y=0
        for i in range(1,self.nlines+1):
            y=y-self.getLine(i).getHeight(pspict)/2
            x=0
            for j in range (1,self.ncolumns+1):
                x=x+self.getColumn(j).getWidth(pspict)/2
                self.elements[i,j].central_point=Point(x,y)
                x=x+self.getColumn(j).getWidth(pspict)/2
            y=y-self.getLine(i).getHeight(pspict)/2


    def action_on_pspict(self,pspict):
        self.computeCentralPoints(pspict)
        for i in range(1,self.nlines+1):
            for j in range (1,self.ncolumns+1):
                P=self.elements[i,j].central_point
                P.put_mark(0,angle=0,text=self.elements[i,j].text,automatic_place=(pspict,"center"))
                P.parameters.symbol=""
                pspict.DrawGraphs(P)

        l=[]
        for i in range(1,self.nlines+1):
            l.append("&".join( [  "\\text{"+el.text+"}" for el in self.getLine(i)  ]  ))
        matrix_code="\\\\".join(l)
        P=self.getMidPoint(pspict)
        fake_matrix=r"""$
        \begin{pmatrix}
        \phantom{
        \begin{matrix}
        MATRIX_CODE
        \end{matrix}
        }
        \end{pmatrix}$
        """.replace("MATRIX_CODE",matrix_code)
        P.put_mark(0,angle=0,text=fake_matrix,automatic_place=(pspict,"center"))
        pspict.DrawGraphs(P)
