# -*- coding: utf8 -*-

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

# copyright (c) Laurent Claessens, 2016
# email: laurent@claessens-donadello.eu

from ObjectGraph import ObjectGraph
from Constructors import *

class EllipseGraph(ObjectGraph):
    def __init__(self,O,A,B):
        ObjectGraph.__init__(self,self)
        self.O=O
        self.A=A
        self.B=B
        self.angleI=0
        self.angleF=2*pi
    def graph(self,a,b):
        curve = EllipseOAB(self.O,self.A,self.B)
        curve.angleI=a
        curve.angleF=b
        return curve
    def _bounding_box(self,pspict):
        return BoundingBox()

    def action_on_pspict(self,pspict):
        f1=self.A-self.O
        f2=self.B-self.O

        curve=NonAnalyticPointParametricCurve( lambda x:self.O+cos(x)*f1+sin(x)*f2,self.angleI,self.angleF  )
        curve.mode="trivial"

        pspict.DrawGraphs(curve)
