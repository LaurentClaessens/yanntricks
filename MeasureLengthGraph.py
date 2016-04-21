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

from sage.all import *

from ObjectGraph import ObjectGraph
from Constructors import *
from Utilities import *
from SegmentGraph import SegmentGraph

class MeasureLengthGraph(SegmentGraph):
    def __init__(self,seg,dist=0.1):
        try :
            self.segment=seg.segment
        except AttributeError :
            self.segment=seg
        self.dist=dist
        self.delta=seg.rotation(-90).fix_size(self.dist)
        self.mseg=seg.translate(self.delta)
        SegmentGraph.__init__(self,self.mseg.I,self.mseg.F)
        self.mI=self.mseg.I
        self.mF=self.mseg.F
    def advised_mark_angle(self,pspict=None):
        return self.delta.angle()
    def math_bounding_box(self,pspict=None):
        return BoundingBox()
        # I return a "empty" bounding box because I don't want to
        # take the measures in consideration when creating the axes.
        #return self.mseg.math_bounding_box(pspict)
        #return BoundingBox()
    def bounding_box(self,pspict=None):
        bb=self.mseg.bounding_box(pspict)
        for ob in self.added_objects :
            bb.AddBB(ob.bounding_box(pspict))
        if self.marque:
            C=self.mseg.center()
            C.marque=self.marque
            C.mark=self.mark
            C.mark.graph=C
            bb.AddBB(C.bounding_box(pspict))
        return bb
    def mark_point(self,pspict=None):
        return self.mseg.center()
    def latex_code(self,language=None,pspict=None):
        a=[]
        C=self.mseg.center()
        vI=AffineVector(C,self.mI)
        vF=AffineVector(C,self.mF)
        vI.parameters=self.parameters.copy()
        vF.parameters=self.parameters.copy()
        a.append(vI.latex_code(language=language,pspict=pspict))
        a.append(vF.latex_code(language=language,pspict=pspict))
        return "\n".join(a)
