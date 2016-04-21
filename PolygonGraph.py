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
        self.edge=Segment(Point(0,0),Point(1,1))    # This is an arbitrary segment that only serves to have a
                                                    # "model" for the parameters.
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
            s.parameters=self.edge.parameters.copy()
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
            text_list=[   "\( {} \)".format(x) for x in  string.ascii_uppercase[0:n]  ]
        if points_names :
            text_list=[    "\( {} \)".format(x) for x in points_names   ]
        for i,P in enumerate(self.points_list):
            text=text_list[i]
            A=self.points_list[(i-1)%n]
            B=self.points_list[(i+1)%n]
            v1=AffineVector(A,P).fix_origin(P).fix_size(1)
            v2=AffineVector(B,P).fix_origin(P).fix_size(1)
            vect=(v1+v2).fix_size(dist)
            Q=P+vect
            angle=Segment(P,Q).angle()
            P.put_mark(dist,angle,text,automatic_place=(pspict,"center"))
            self.added_objects.append(P)
    def math_bounding_box(self,pspict=None):
        bb=BoundingBox()
        for P in self.points_list:
            bb.append(P,pspict)
        return bb
    def bounding_box(self,pspict=None):
        return self.math_bounding_box(pspict)
    def specific_action_on_pspict(self,pspict):
        """
        If self.parameters.color is not None, it will be the color of the edges.

        If one wants to fill or hatch, one has to ask explicitly.
        """
        if self.parameters._hatched or self.parameters._filled :
            custom=CustomSurface(self.edges)
            custom.parameters=self.parameters.copy()
            pspict.DrawGraph(custom)
        if self.parameters.color!=None:
            self.draw_edges=True
            for edge in self.edges:
                edge.parameters.color=self.parameters.color
        if self.draw_edges:
            for edge in self.edges:
                if not self.independent_edge :
                    edge.parameters=self.edge.parameters
                    if self.parameters.color!=None:
                        edge.parameters.color=self.parameters.color
                pspict.DrawGraph(edge)

class RectangleGraph(PolygonGraph):
    """
    The parameters of the four lines are by default the same, but they can be adapted separately.

    graph_N returns the north side as a phystricks.Segment object
    The parameters of the four sides have to be set independently.

    The drawing is done by \psframe, so that, in principle, all the options are available.
    """
    def __init__(self,NW,SE):
        #ObjectGraph.__init__(self,self)
        self.NW = NW
        self.SE = SE
        self.SW = Point(self.NW.x,self.SE.y)
        self.NE = Point(self.SE.x,self.NW.y)
        PolygonGraph.__init__(self,[self.SW,self.SE,self.NE,self.NW])
        self.mx=self.NW.x
        self.Mx=self.SE.x
        self.my=self.SE.y
        self.My=self.NW.y
        self.rectangle = self.obj

        self.segment_N=Segment(self.NW,self.NE)
        self.segment_S=Segment(self.SW,self.SE)
        self.segment_E=Segment(self.NE,self.SE)
        self.segment_W=Segment(self.NW,self.SW)

        # Use self.edges instead of self.segments (September, 18, 2014)
        #self.segments=[self.segment_N,self.segment_S,self.segment_E,self.segment_W]

        # Putting the style of the edges to none makes the 
        # CustomSurface (and then filling and hatching) not work because the edges'LaTeX code is use to create the tikz path
        # defining the surface.
        #for s in self.edges:
        #    s.parameters.style="none"
    def polygon(self):
        polygon= Polygon(self.NW,self.NE,self.SE,self.SW)
        polygon.parameters=self.parameters.copy()
        return polygon
    def first_diagonal(self):
        return Segment(self.NW,self.SE)
    def second_diagonal(self):
        return Segment(self.SW,self.NE)
    def center(self):
        return self.first_diagonal().center()
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return RectangleGraph

    def _segment(self,side):
        bare_name = "graph_"+side
        if not bare_name in self.__dict__.keys():
            line = self.__getattribute__("segment_"+side)()
            #line.parameters=self.parameters.copy()
            self.__dict__[bare_name]=line
        return  self.__dict__[bare_name]
    def __getattr__(self,attrname):
        if "graph_" in attrname:
            return self._segment(attrname[6])
        raise AttributeError
