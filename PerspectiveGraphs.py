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
import Defaults

class Circle3DGraph(ObjectGraph):
    def __init__(self,op,O,A,B,angleI=0,angleF=0):
        """
        The circle passing trough A and B with center O.

        `A`, `B` and `O` are tuples of numbers
        """
        ObjectGraph.__init__(self,self)
        self.op=op
        self.O=O
        self.A=A
        self.B=B
        self.center=Vector3D(O[0],O[1],O[2])
        self.u=Vector3D( A[0]-O[0],A[1]-O[1],A[2]-O[2]  )
        self.v=Vector3D( B[0]-O[0],B[1]-O[1],B[2]-O[2]  )
        self.radius_u=sqrt( sum([k**2 for k in self.u])  )
        self.radius_v=sqrt( sum([k**2 for k in self.v])  )
        self.parameters.plotpoints=10*max(self.radius_u,self.radius_v)
        self.angleI=angleI
        self.angleF=angleF
        self.divide=False
        self.linear_plotpoints=Defaults.CIRCLE3D_LINEAR_PLOTPOINTS
    @lazy_attribute
    def points_list(self):
        l=[]
        import numpy
        ai=numerical_approx(self.angleI)
        af=numerical_approx(self.angleF)
        angles=numpy.linspace(ai,af,self.linear_plotpoints)
        for a in angles:
            l.append( self.get_point(a) )
        return l
    @lazy_attribute
    def curve2d(self):
        proj_points_list=[]
        for P in self.points_list:
            t=self.op.point(P.x,P.y,P.z)
            proj_points_list.append(t)
        curve=InterpolationCurve(proj_points_list)
        curve.parameters=self.parameters.copy()
        return curve
    def xmin(self):
        """
        return the visually --in the sense of the projection on the screen, not in the sense of xunit,yunit-- minimal x point of the circle
        """
        return min(  self.curve2d.points_list,key=lambda P:P.x  )
    def xmax(self):
        """
        return the visually --in the sense of the projection on the screen, not in the sense of xunit,yunit-- maximal x point of the circle
        """
        return max(  self.curve2d.points_list,key=lambda P:P.x  )
    def get_point(self,angle):
        return self.center+cos(angle)*self.u+sin(angle)*self.v  
    def get_point2d(self,angle):
        return self.op.point(self.get_point(angle))
    def graph(self,angleI,angleF):
        C = Circle3DGraph(self.op,self.O,self.A,self.B,angleI,angleF)
        C.parameters=self.parameters.copy()
        return C
    def bounding_box(self,pspict=None):
        return self.curve2d.bounding_box(pspict)
    def math_bounding_box(self,pspict=None):
        return self.curve2d.math_bounding_box(pspict)
    def specific_action_on_pspict(self,pspict):
        if not self.divide:
            pspict.DrawGraphs(self.curve2d)
        if self.divide:
            c1=self.graph(0,pi)
            c2=self.graph(pi,2*pi)
            c1.parameters.style="dashed"
            pspict.DrawGraphs(c1,c2)

class CuboidGraph(object):
    def __init__(self,op,P,a,b,c):
        self.op=op
        self.P=P
        self.Px=P[0]
        self.Py=P[1]
        self.a=a
        self.b=b
        self.c=c
        self.transparent=True

        self.A=[Point(self.Px,self.Py+b),Point(self.Px+a,self.Py+b),Point(self.Px+a,self.Py),Point(self.Px,self.Py)]

        # The points on the first and second rectangle
        self.c1=[ self.op.point(P.x,P.y,0) for P in self.A ]
        self.c2=[ self.op.point(P.x,P.y,self.c) for P in self.A ]

        self.A=self.c1[0]
        self.B=self.c1[1]
        self.C=self.c1[2]
        self.D=self.c1[3]
        self.E=self.c2[0]
        self.F=self.c2[1]
        self.G=self.c2[2]
        self.H=self.c2[3]

        for P in self.c1:
            P.parameters.symbol="none"
        for P in self.c2:
            P.parameters.symbol="none"

        # The edges.
        self.segP=[ Segment( self.c1[i],self.c2[i] ) for i in range(0,len(self.c1))  ]
        self.segc1=[ Segment(self.c1[i],self.c1[(i+1)%len(self.c1)]) for i in range(0,len(self.c1)) ]
        self.segc2=[ Segment(self.c2[i],self.c2[(i+1)%len(self.c2)]) for i in range(0,len(self.c2)) ]

        if op.alpha < 90 :
            self.segP[3].parameters.style="dashed"
            self.segc2[2].parameters.style="dashed"
            self.segc2[3].parameters.style="dashed"
        else :
            self.segP[2].parameters.style="dashed"
            self.segc2[2].parameters.style="dashed"
            self.segc2[1].parameters.style="dashed"
    def put_vertex_mark(self,pspict=None):
        self.A.put_mark(0.2,135,"\( A\)",automatic_place=pspict)
        self.B.put_mark(0.2,90,"\( B\)",automatic_place=pspict)
        self.C.put_mark(0.2,-45,"\( C\)",automatic_place=pspict)
        self.D.put_mark(0.2,180,"\( D\)",automatic_place=pspict)
        self.E.put_mark(0.2,135,"\( E\)",automatic_place=pspict)
        self.F.put_mark(0.2,0,"\( F\)",automatic_place=pspict)
        self.G.put_mark(0.2,0,"\( G\)",automatic_place=pspict)
        self.H.put_mark(0.2,135,"\( H\)",automatic_place=pspict)
    def make_opaque(self):
        self.transparent=False
    def bounding_box(self,pspict=None):
        bb=BoundingBox()
        for s in self.c1:
            bb.append(s,pspict)
        for s in self.c2:
            bb.append(s,pspict)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def action_on_pspict(self,pspict):
        for P in self.c1:
            pspict.DrawGraphs(P)
        for P in self.c2:
            pspict.DrawGraphs(P)
        for s in self.segP:
            pspict.DrawGraphs(s)
        for s in self.segc2:
            pspict.DrawGraphs(s)
        for s in self.segc1:
            pspict.DrawGraphs(s)
        if not self.transparent :
            surface1=Polygon( self.c1 )
            surface1.parameters.filled()
            surface2=Polygon( self.c1[0],self.c1[1],self.c2[1],self.c2[0] )
            surface2.parameters.filled()
            if self.op.alpha<90:
                surface3=Polygon(self.c1[1],self.c2[1],self.c2[2],self.c1[2])
            else :
                surface3=Polygon(self.c1[0],self.c2[0],self.c2[3],self.c1[3])
            surface3.parameters.filled()
            pspict.DrawGraphs(surface1,surface2,surface3)
    def latex_code(self,language=None,pspict=None):
        return ""   # Everything is in action_on_pspict

class Vector3DGraph(object):
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.c_list=[x,y,z]
    def __add__(self,other):
        return Vector3D( self.x+other.x,self.y+other.y,self.z+other.z  )
    def __rmul__(self,r):
        return Vector3D(r*self.x,r*self.y,r*self.z)
    def __getitem__(self,i):
        return self.c_list[i]


