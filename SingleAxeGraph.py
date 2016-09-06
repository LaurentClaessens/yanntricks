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

from phystricks.ObjectGraph import ObjectGraph
from phystricks.ObjectGraph import Options
from MathStructures import AxesUnit
from Utilities import *
from SmallComputations import RemoveLastZeros

from Utilities import logging

class SingleAxeGraph(ObjectGraph):
    def __init__(self,C,base,mx,Mx,pspict=None):
        ObjectGraph.__init__(self,self)
        self.C=C
        self.base=base
        self.mx=mx
        self.Mx=Mx
        self.pspict=pspict
        self.options=Options()
        self.IsLabel=False
        self.axes_unit=AxesUnit(self.base.length,"")
        self.Dx=1
        self.arrows="->"
        self.graduation=True
        self.numbering=True
        self.imposed_graduation=[]
        self.mark_origin=True
        self.mark=None
        self.mark_angle=degree(base.angle().radian-pi/2)
        self.enlarge_size=0.5
    
    # SingleAxe.segment cannot be a lazy attribute because we use it for some projections before to compute the bounding box.
    def segment(self,projection=False,pspict=None):
        if self.mx == 0 and self.Mx == 0 :
            # I think that we only pass here in order either to do a projection either to create an initial bounding box.
            # If xunit or yunit are very low, then returning something like
            #   Segment(self.C-self.base.visual_length(1,pspict=pspict),self.C+self.base.visual_length(1,pspict=pspict))      
            # causes bounding box to be too large.
            # This is why I return a small segment.
            if projection :
                return Segment(self.C,self.C+self.base)
            else :
                return Segment(self.C-self.base.fix_size(1),self.C+self.base.fix_size(1))      

                # raising an error here makes impossible to draw pictures with only vertical stuff. As an example, the following 
                # was crashing :

                #P=Point(0,0)
                #pspict.DrawGraphs(P)
                #pspict.DrawDefaultAxes()
                #pspict.dilatation(1)
                #fig.conclude()
        return Segment(self.C+self.mx*self.base,self.C+self.Mx*self.base)
    def add_option(self,opt):
        self.options.add_option(opt)
    def mark_point(self,pspict=None):
        return self.segment().F
    def no_numbering(self):
        self.numbering=False
    def no_graduation(self):
        self.graduation=False
    def enlarge_a_little(self,l,xunit=None,yunit=None,pspict=None):
        """
        return the tuple (mx,Mx) that correspond to axes of length `l` more than self
        (in both directions)
        """
        if pspict:
            xunit=pspict.xunit
            yunit=pspict.yunit
        seg=self.segment(pspict=pspict)
        # The aim is to find the multiple of the base vector that has length `l`.
        vx=self.base.F.x
        vy=self.base.F.y
        k=l/sqrt(  (vx*xunit)**2+(vy*yunit)**2  )
        mx=self.mx-k
        Mx=self.Mx+k
        return mx,Mx
    def graduation_bars(self,pspict):
        """
        Return the list of bars that makes the graduation of the axes

        By default, it is one at each multiple of self.base. If an user-defined axes_unit is given, then self.base is modified.

        This function also enlarges the axe by half a *visual* centimeter.
        """
        # bars_list contains in the same time marks (for the numbering) and segments (for the bars itself)
        if not self.graduation:
            return []
        bars_list=[]
        bar_angle=SR(self.mark_angle).n(digits=7) # Latex does not accept 
                                                  # too much digits.
        for x,symbol in self.axes_unit.place_list(self.mx,self.Mx,self.Dx,self.mark_origin):
            P=(x*self.base).F
            P.psName="ForTheBar"   
            if self.numbering :
                # The 0.2 here is hard coded in Histogram, see 71011299

                if self.segment().horizontal :
                    position="N"
                if self.segment().vertical :
                    position="E"
                P.put_mark(0.2,self.mark_angle,symbol,pspict=pspict,position=position)
                bars_list.append(P.mark)

            a=visual_polar(P,0.1,bar_angle,pspict)
            b=visual_polar(P,0.1,bar_angle+180,pspict)

            seg=Segment(a,b)
            bars_list.append(seg)
        return bars_list
    def bounding_box(self,pspict):
        # One cannot take into account the small enlarging here because
        # we do not know if this is the vertical or horizontal axe,
        # so we cannot make the fit of the drawn objects.
        BB=self.math_bounding_box(pspict)
        for graph in self.graduation_bars(pspict):
            BB.append(graph,pspict)
        return BB
    def math_bounding_box(self,pspict):
        # The math_bounding box does not take into account the things that are inside the picture (not even if this are default axes)
        bb=BoundingBox()
        for x,symbol in self.axes_unit.place_list(self.mx,self.Mx,self.Dx,self.mark_origin):
            P=(x*self.base).F
            bb.addX(P.x)
            bb.addY(P.y)
        return bb
    def action_on_pspict(self,pspict):
        """
        Return the pstricks code of the axe.
        """
        sDx=RemoveLastZeros(self.Dx,10)
        self.add_option("Dx="+sDx)
        if self.mark :
            pspict.DrawGraphs(self.mark,separator_name="AXES")
        if self.graduation :
            for graph in self.graduation_bars(pspict):
                pspict.DrawGraphs(graph,separator_name="AXES")
        v=AffineVector(self.segment(pspict=pspict))
        pspict.DrawGraphs(v,separator_name="AXES")
    def __str__(self):
        return "<SingleAxeGraph: C={0} base={1} mx={2} Mx={3}>".format(self.C,self.base,self.mx,self.Mx)
