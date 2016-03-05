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
# email: moky.math@gmai.com

from __future__ import division
from __future__ import unicode_literals

from sage.all import *

from ObjectGraph import ObjectGraph
from Constructors import *
from Utilities import *


class SurfaceBetweenLines(ObjectGraph):
    def __init__(self,curve1,curve2):
        """
        Give the graph of the surface between the two lines.

        The lines are needed to have a starting and ending point
        that will be joined by straight lines.
        """
        # By convention, the first line goes from left to right and the second one to right to left.

        ObjectGraph.__init__(self,self)

        if curve1.I.x > curve1.F.x:
            curve1=curve1.reverse()
        if curve2.I.x > curve2.F.x:
            curve2=curve2.reverse()

        self.curve1=curve1
        self.curve2=curve2

        self.I1=curve1.I
        self.I2=curve2.I

        self.F1=curve1.F
        self.F2=curve2.F

        self.Isegment=Segment(self.I1,self.I2)
        self.Fsegment=Segment(self.F1,self.F2)
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        bb.append(self.curve1,pspict)
        bb.append(self.curve2,pspict)
        return bb
    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        a=[]
       
        c1=self.curve1
        c2=self.curve2.reverse()

        custom=CustomSurface(c1,self.Fsegment,c2,self.Isegment)
        self.parameters.add_to(custom.parameters)     # This curve is essentially dedicated to the colors
        custom.options=self.options
        
        a.append("%--- begin of Surface between lines ---")
        a.append("% Custom surface")
        a.append(custom.latex_code(language=language,pspict=pspict))

        a.append("% Curve 1")
        a.append(self.curve1.latex_code(language=language,pspict=pspict))
        a.append("% Curve 2")
        a.append(self.curve2.latex_code(language=language,pspict=pspict))
        a.append("% Isegment")
        a.append(self.Isegment.latex_code(language=language,pspict=pspict))
        a.append("% Fsegment")
        a.append(self.Fsegment.latex_code(language=language,pspict=pspict))
        a.append("%--- end of Surface between lines ---")
        return "\n".join(a)

# Since all type of surfaces have to be specializations of SurfaceBetweenParametricCurves,
# we have to unify the names of the segments.
# x.Isegment is the segment joining the first point of the first curve
# c.Fsegment is the other one.
# May, 1, 2011

# For the same reason, all type of surfaces have to be functions instead of classes.
# These functions return an object SurfaceBetweenParametricCurvesGraph 
# with the right particularization.

class SurfaceBetweenParametricCurvesGraph(ObjectGraph):
    def __init__(self,curve1,curve2,interval1=(None,None),interval2=(None,None),reverse1=False,reverse2=True):
        # TODO: I think that the parameters reverse1 and reverse2 are no more useful
        #   since I enforce the condition curve1 : left -> right by hand.
        ObjectGraph.__init__(self,self)

        self.curve1=curve1
        self.curve2=curve2

        #self.f1=self.curve1       # TODO: Soon or later, one will have to fusion these two
        #self.f2=self.curve2        

        self.mx1=interval1[0]
        self.mx2=interval1[1]
        self.Mx1=interval2[0]
        self.Mx2=interval2[1]
        for attr in [self.mx1,self.mx2,self.Mx1,self.Mx2]:
            if attr == None:
                raise TypeError,"At this point, initial and final values have to be already chosen"
        self.curve1.llamI=self.mx1
        self.curve1.llamF=self.Mx1
        self.curve2.llamI=self.mx2
        self.curve2.llamF=self.Mx2

        self.draw_Isegment=True
        self.draw_Fsegment=True
        self.Isegment=Segment(self.curve2.get_point(self.mx2,advised=False),self.curve1.get_point(self.mx1,advised=False))
        self.Fsegment=Segment(self.curve1.get_point(self.Mx1,advised=False),self.curve2.get_point(self.Mx2,advised=False))

        self.add_option("fillstyle=vlines") 
        self.parameters.color=None       

    def bounding_box(self,pspict=None):
        if pspict==None:
            raise ValueError, "You have to provide a pspict"
        bb=BoundingBox()
        bb.append(self.curve1,pspict)
        bb.append(self.curve2,pspict)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def action_on_pspict(self,pspict=None):
       
        c1=self.curve1.graph(self.mx1,self.Mx1)
        c2=self.curve2.graph(self.mx2,self.Mx2)

        # By convention, the first line goes from left to right and the second one to right to left.
        # The same is followed in SurfaceBetweenLines

        if c1.I.x > c1.F.x:
            c1=c1.reverse()
        if c2.I.x < c2.F.x:
            c2=c2.reverse()

        reIsegment=Segment(c2.F,c1.I)
        reFsegment=Segment(c1.F,c2.I)
        reIsegment.parameters=self.Isegment.parameters
        reFsegment.parameters=self.Fsegment.parameters

        if self.parameters._filled or self.parameters._hatched :
            custom=CustomSurface(c1,reFsegment,c2,reIsegment)
            custom.parameters=self.parameters.copy()
            pspict.DrawGraph(custom)
        else :
            raise ShouldNotHappenException("You are speaking of a surface but you don't want neither to fill it neither to hatch it ?")

        if self.parameters.color!=None :
            self.Isegment.parameters.color=self.parameters.color
            self.Fsegment.parameters.color=self.parameters.color
            self.curve1.parameters.color=self.parameters.color
            self.curve2.parameters.color=self.parameters.color

        pspict.DrawGraphs(self.curve1,self.curve2)

        if self.draw_Isegment :
            pspict.DrawGraph(reIsegment)
        if self.draw_Fsegment :
            pspict.DrawGraph(reFsegment)
    def latex_code(self,language=None,pspict=None):
        return ""
