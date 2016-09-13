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

class PolygonGraph(ObjectGraph):
    """
    INPUT:

    - ``args`` - a tuple of points.

    NOTE:

    This class is not intended to be used by the end-user. The latter has to use :func:`Polygon`.
    """
    def __init__(self,points_list):
        ObjectGraph.__init__(self,self)
        self.edges=[]
        self.vertices=points_list
        self.points_list=self.vertices

        # edge_model is a dummy segment that serve to model the 
        # parameters of the edges.
        # In other words, by default the edges of the polygon will have the
        # parameters of self.edge_model
        self.edge_model=Segment(Point(0,0),Point(1,1))
        for i in range(0,len(self.points_list)):
            segment=Segment(self.points_list[i],self.points_list[(i+1)%len(self.points_list)])
            self.edges.append(segment)
        self.draw_edges=True
        self.independent_edge=False
    def rotation(self,angle):
        pts=[  P.rotation(angle) for P in self.points_list  ]
        return Polygon(pts)
    def make_edges_independent(self):
        """
        make the edges customisation independent the one to the other.
        """
        for s in self.edges :
            s.parameters=self.edge_model.parameters.copy()
        self.independent_edge=True
    def no_edges(self):
        """
        When X.no_edges() is used, the edges of the polygon will not be drawn.
        """
        self.draw_edges=False
    def put_mark(self,dist,text_list=None,points_names=None,mark_point=None,pspict=None):
        n=len(self.points_list)
        if not text_list and not points_names:
            import string
            text_list=["\( {} \)".format(x) for x in string.ascii_uppercase[0:n]]
        if points_names :
            text_list=[    "\( {} \)".format(x) for x in points_names   ]
        for i,P in enumerate(self.points_list):
            text=text_list[i]
            A=self.points_list[(i-1)%n]
            B=self.points_list[(i+1)%n]
            v1=AffineVector(A,P).fix_origin(P).normalize(1)
            v2=AffineVector(B,P).fix_origin(P).normalize(1)
            vect=(v1+v2).normalize(dist)
            Q=P+vect
            angle=Segment(P,Q).angle()
            P.put_mark(dist,angle,text,pspict=pspict,position="center")
            self.added_objects.append(pspict,P)
    def math_bounding_box(self,pspict=None):
        bb=BoundingBox()
        for P in self.points_list:
            bb.append(P,pspict)
        return bb
    def bounding_box(self,pspict=None):
        return self.math_bounding_box(pspict)
    def action_on_pspict(self,pspict):
        """
        If self.parameters.color is not None, it will be the color of the edges.

        If one wants to fill or hatch, one has to ask explicitly.
        """
        if self.parameters._hatched or self.parameters._filled :
            custom=CustomSurface(self.edges)
            custom.parameters=self.parameters.copy()
            pspict.DrawGraphs(custom)
        if self.parameters.color!=None:
            self.draw_edges=True
            for edge in self.edges:
                edge.parameters.color=self.parameters.color
        if self.draw_edges:
            for edge in self.edges:
                if not self.independent_edge :
                    edge.parameters=self.edge_model.parameters.copy()
                    if self.parameters.color!=None:
                        edge.parameters.color=self.parameters.color
                pspict.DrawGraphs(edge)
