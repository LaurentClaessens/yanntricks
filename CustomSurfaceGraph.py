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
from Utilities import *
from Parameters import Parameters

class CustomSurfaceGraph(ObjectGraph):
    """
    INPUT:

    - args - A list or a tuple of graphs that can compose a \pscustom
    """
    def __init__(self,args):
        ObjectGraph.__init__(self,self)
        #self.add_option("fillstyle=vlines,linestyle=none")  
        self.add_option("fillstyle=none,linestyle=none")
        self.graphList=args
        self.edges=Parameters()
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        for obj in self.graphList :
            bb.AddBB(obj.bounding_box(pspict))
        return bb
    def math_bounding_box(self,pspict=None):
        bb=BoundingBox()
        for obj in self.graphList :
            bb.AddBB(obj.math_bounding_box(pspict))
        return bb
    def tikz_code(self,pspict=None):
        """
        If the CustomSurface has to be filled, we start by plotting the filling.

        Then we plot, separately, the lines forming the border. Thus we can have different colors and line style for the different edges.
        """
        # The color attribution priority is the following.
        # if self.parameters.color is given, then this will be the color
        # if an hatch or a fill color is given and no self.parameters.color, then this will be used
        a=[]
        color=None

        # It cannot be filled by default when a color is given because Rectangles and Polygon drop here
        #if self.parameters.color :
        #    if self.parameters._hatched==False:     # By default it will be filled if one give a color
        #        self.parameters._filled=True

        if self.parameters._filled and self.parameters.fill.color:
            color=self.parameters.fill.color
        if self.parameters._hatched and self.parameters.hatch.color:
            color=self.parameters.hatch.color
        if self.parameters._filled or self.parameters._hatched :
            l=[]
            for obj in self.graphList :
                try:
                    l.extend( [p.coordinates(numerical=True,digits=3,pspict=pspict) for p in obj.representativePoints()] )
                except AttributeError :
                    print("The object "+obj+" seems to have no 'representativePoints' method")
                    raise
                    obj_code=obj.latex_code(language="tikz",pspict=pspict)
                    l.append( draw_to_fill(obj_code) )
            l.append(" cycle;")
            code=" -- ".join(l)
            if self.parameters._hatched :
                # This is from
                # http://www.techques.com/question/31-54358/custom-and-built-in-tikz-fill-patterns
                # position 170321508
                def_hatching=r"""
% declaring the keys in tikz
\tikzset{hatchspread/.code={\setlength{\hatchspread}{#1}},
         hatchthickness/.code={\setlength{\hatchthickness}{#1}}}
% setting the default values
\tikzset{hatchspread=3pt,
         hatchthickness=0.4pt}
"""
                a.append(def_hatching)
                if color==None:
                    color="lightgray"
                options="color="+color
                options=options+",  pattern=custom north west lines,hatchspread=10pt,hatchthickness=1pt "
            if self.parameters._filled:
                options="color="+color
            a.append("\\fill [{}] ".format(options)+code)
    
        return "\n".join(a)
    def latex_code(self,language=None,pspict=None):
        """
        There are two quite different ways to get here. The first is to ask a surface under a function and the second is to ask for a rectangle or a polygon.

        if self.parameters.color is given, this will be the color of the edges

        If one wants to give different colors to edges, one has to ask explicitly using
        self.Isegment
        self.Fsegment
        self.curve1
        self.curve2
        in the case of surface between curves.

        If one wants the surface to be filled or hatched, on has to ask explicitly.
        """
        a=[]
        if language=="pstricks":
            raise DeprecationWarning
        if language=="tikz":
            a.append(self.tikz_code(pspict))
        if self._draw_edges :
            for obj in self.graphList :
                obj.parameters = self.edges.copy()
                a.append(obj.latex_code(language=language,pspict=pspict))
        return '\n'.join(a)
