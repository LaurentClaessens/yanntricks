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

from __future__ import division

from phystricks.ObjectGraph import ObjectGraph
from Constructors import *
from Utilities import *

class AngleGraph(ObjectGraph):
    """
    self.mark_angle is the angle at which self.mark_point will be placed. By default it is at the middle. 
        If you want to change it, use
        self.set_mark_angle(x).
        It will set both the mark_angle and the advised_mark_angle to to x in the same time.

        We have to make a choice between the two angles that can be deduced from 3 points. Here the choice is
        the angle from the first given point to the second one.
    """
    def __init__(self,A,O,B,r=None):
        self.A=A
        self.O=O
        self.B=B
        if r==None:
            r=0.5           # Does not depend on the radius because we are giving a 'visual' length.
        self.r=r
        self.angleA=AffineVector(O,A).angle()
        self.angleB=AffineVector(O,B).angle()

        # I think that one does not have to check and fix what angle is first here
        # because the angles are re-computed in self.circle.

        self.angleI=self.angleA
        self.angleF=self.angleB

        ObjectGraph.__init__(self,self)
        self._mark_angle=None
    def visual_angleIF(self,pspict):
        aI1=visual_polar_coordinates(Point( cos(self.angleI.radian),sin(self.angleI.radian) ),pspict).measure
        aF1=visual_polar_coordinates(Point( cos(self.angleF.radian),sin(self.angleF.radian) ),pspict).measure

        a=numerical_approx(aI1.degree)
        b=numerical_approx(aF1.degree)
        if a > b:
            a=a-360
            aI2=AngleMeasure(value_degree=a)
        else :
            aI2=aI1
        aF2=aF1
        return aI2,aF2
    def circle(self,visual=False,pspict=None):
        visualI,visualF=self.visual_angleIF(pspict)
        return Circle(self.O,self.r,visual=visual,pspict=pspict).graph(visualI,visualF)
    @lazy_attribute
    def measure(self):
        return AngleMeasure(value_degree=self.angleF.degree-self.angleI.degree)
    def graph(self):
        return AngleGraph(self)
    def set_mark_angle(self,theta):
        """
        theta is degree or AngleMeasure
        """
        self._mark_angle=AngleMeasure(value_degree=theta)
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        C= self.circle(visual=True,pspict=pspict)
        bb=C.bounding_box(pspict)
        return self.circle(visual=True,pspict=pspict).bounding_box(pspict)
    def advised_mark_angle(self,pspict):
        if self._mark_angle is None :
            visualI,visualF=self.visual_angleIF(pspict=pspict)
            self._mark_angle = (visualI.degree+visualF.degree)/2
        return self._mark_angle
    def mark_point(self,pspict=None):
        ama=self.advised_mark_angle(pspict)
        return self.circle(visual=True,pspict=pspict).get_point(ama)
    def get_mark(self,dist=None,angle=None,text="",mark_point=None,added_angle=None,position=None,pspict=None):
        """
        The mark on an angle is determined in the following way.
        - if 'dist' and 'angle' are given, the center will be placed there (discouraged) -- in fact an exception is raised
        If they are not given :

        - the *center* of the mark is on the bisector at such a distance that the bounding box of the text will not intersect the lines that are defining the angle.
        """


        P=self.mark_point(pspict)
        if self.measure.degree>90 :
            return P.get_mark(dist=0.3,angle=self.advised_mark_angle,text=text,position=position,pspict=pspict)

        if dist != None :
            print("marks on angle should be all default")
            raise
        if position != None:
            print("The mark of an angle should be given without position argument")
            raise

        # The default can be any value different than zero. It serves to 
        # avoid a division by zero during the first compilation.
        dimx,dimy = pspict.get_box_size(text,default_value="3pt")  

        if self.angleA.degree == 0:
            x=dimy/tan(self.measure.radian)
            C=Point(self.O.x+x+dimx/2,self.O.y+dimy/2)
            mark=Mark(self,dist=None,angle=None,text=text,mark_point=None,central_point=C,position=None,pspict=pspict)
            return mark
        
        if 0<self.angleA.degree < 90 and 0<self.angleB.degree < 90 :


        raise "Under construction for your case ..."

    def action_on_pspict(self,pspict):
        circle=self.circle(visual=True,pspict=pspict)
        circle.parameters=self.parameters.copy()
        pspict.DrawGraphs(circle)

class RightAngleGraph(ObjectGraph):
    def __init__(self,d1,d2,r,n1,n2):
        """
        two lines and a distance.

        n1 and n2 are 0 or 1 and indicating which sector has to be marked.
        'n1' if for the intersection with d1. If 'n1=0' then we choose the intersection nearest to d1.I
        Similarly for n2
        """
        ObjectGraph.__init__(self,self)
        self.d1=d1
        self.d2=d2

        # If the intersection point is one of the initial or final point of d1 or d2, then the sorting
        # in 'action_on_pspict' does not work.
        # This happens in RightAngle(  Segment(D,E),Segment(D,F),l=0.2, n1=1,n2=1 ) because the same point 'D' is given
        # for both d1 and d2.
        # We need d1.I, d1.F, d2.I and d2.F to be four distinct points.
        if self.d1.I==self.d2.I or self.d1.I==self.d2.F or self.d1.F==self.d2.I or self.d1.F==self.d2.F:
            self.d1=d1.dilatation(1.5)
            self.d2=d2.dilatation(1.5)

        self.r=r
        self.n1=n1
        self.n2=n2
        self.intersection=Intersection(d1,d2)[0]
    def inter_point(self,I,F,n,pspict):
        v1=AffineVector(I,F)
        v=visual_length(v1,l=1,pspict=pspict)
        if n==0:
            P1=I - self.r*v
        if n==1:
            P1=I + self.r*v
        
        rv=self.r*v
        return P1
    def action_on_pspict(self,pspict):
        P1=self.inter_point(self.intersection,self.d1.F,self.n1,pspict)
        P2=self.inter_point(self.intersection,self.d2.F,self.n2,pspict)

        Q=P1+P2-self.intersection
        l1=Segment(Q,P1)
        l2=Segment(Q,P2)
        
        l1.parameters=self.parameters.copy()
        l2.parameters=self.parameters.copy()
        pspict.DrawGraphs(l1,l2)
    def bounding_box(self,pspict):
        return BoundingBox()
    def math_bounding_box(self,pspict):
        return BoundingBox()
    def latex_code(self,language=None,pspict=None):
        return ""
