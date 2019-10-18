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

from yanntricks.src.ObjectGraph import ObjectGraph
from yanntricks.src.Constructors import *

class BoxDiagramGraph(ObjectGraph):
    def __init__(self,values,h,delta_y=0):
        ObjectGraph.__init__(self,self)

        import numpy
        from scipy.stats.mstats import mquantiles

        ms=mquantiles(values)
        self.average=numpy.mean(values)
        self.q1=ms[0]
        self.median=ms[1]
        self.q3=ms[2]
        self.minimum=min(values)
        self.maximum=max(values)
        self.h=h
        self.delta_y=delta_y
    def action_on_pspict(self,pspict):
        my=self.delta_y-self.h/2
        My=self.delta_y+self.h/2
        h1=Segment(Point(self.minimum,my),Point(self.minimum,My))
        s1=Segment(Point(self.minimum,self.delta_y),Point(self.q1,self.delta_y))
        box=Polygon( Point(self.q1,my),Point(self.q3,my),Point(self.q3,My),Point(self.q1,My) )
        med=Segment(Point(self.median,my),Point(self.median,My))
        med.parameters.color="red"

        #average=Segment(Point(self.average,my),Point(self.average,My))
        ave=Point( self.average,(my+My)/2 )
        ave.parameters.color="blue"

        s2=Segment(Point(self.q3,self.delta_y),Point(self.maximum,self.delta_y))
        h2=Segment(Point(self.maximum,my),Point(self.maximum,My))
        pspict.DrawGraphs(h1,h2,s1,box,med,s2,ave)
    def mark_point(self,pspict=None):
        return Point(self.maximum,self.delta_y)
    def _math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def _bounding_box(self,pspict):
        from yanntricks.src.BoundingBox import BoundingBox
        bb=BoundingBox()
        bb.addX(self.minimum)
        bb.addX(self.maximum)
        bb.addY(self.delta_y-self.h/2)
        bb.addY(self.delta_y+self.h/2)
        return bb
    def latex_code(self,language=None,pspict=None):
        return ""
