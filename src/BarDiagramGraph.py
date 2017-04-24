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

# copyright (c) Laurent Claessens, 2010-2016
# email: laurent@claessens-donadello.eu

from ObjectGraph import ObjectGraph
from Constructors import *

class BarDiagramGraph(ObjectGraph):
    def __init__(self,X,Y):
        ObjectGraph.__init__(self,self)
        self.X=X
        self.Y=Y
        self.linewidth=1    # width of the lines (in centimetrs)
        self.numbering=True
        self.numbering_decimals=2

        # Definition of the default bars to be drawn.
        self.lines_list=[]
        for i,x in enumerate(self.X):
            y=self.Y[i]
            l=Segment(Point(x,0),Point(x,y)  )
            l.parameters.color="blue"
            l.parameters.add_option("linewidth","{}cm".format(self.linewidth))
            self.lines_list.append(l)
    def numbering_marks(self,pspict):
        nb=[]
        if self.numbering:
            for i,h in enumerate(self.Y):
                P=Point(self.X[i],h)
                P.parameters.symbol=""
                P.put_mark(0.2,text="\({{:.{}f}}\)".format(self.numbering_decimals).format(h),pspict=pspict,position="S")
                nb.append(P)
        return nb
    def action_on_pspict(self,pspict):
        for P in self.numbering_marks(pspict):
            pspict.DrawGraphs(P)
        for l in self.lines_list:
            l.parameters.other_options["linewidth"]="{}cm".format(self.linewidth)
            pspict.DrawGraphs(l)
        for P in self.numbering_marks(pspict):
            pspict.DrawGraphs(P)
    def math_bounding_box(self,pspict):
        bb=BoundingBox()
        for l in self.lines_list:
            bb.append(l,pspict)
        return bb
    def bounding_box(self,pspict):
        bb=self.math_bounding_box(pspict)
        for P in self.numbering_marks(pspict):
            bb.append(P,pspict)
        return bb
    def latex_code(self,language=None,pspict=None):
        return ""
