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
        #self.mark_angle=self.media
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
    def measure(self):
        return AngleMeasure(value_degree=self.angleF.degree-self.angleI.degree)
    def graph(self):
        return AngleGraph(self)
    def set_mark_angle(self,theta):
        """
        theta is degree or AngleMeasure
        """
        self._mark_angle=AngleMeasure(value_degree=theta)
        #self._advised_mark_angle=degree(theta,number=True,converting=False)
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def bounding_box(self,pspict=None):
        C= self.circle(visual=True,pspict=pspict)
        bb=C.bounding_box(pspict)
        return self.circle(visual=True,pspict=pspict).bounding_box(pspict)
    def advised_mark_angle(self,pspict):
        if self._mark_angle:
            return self._mark_angle
        visualI,visualF=self.visual_angleIF(pspict=pspict)
        return (visualI.degree+visualF.degree)/2
    def mark_point(self,pspict=None):
        ama=self.advised_mark_angle(pspict)
        return self.circle(visual=True,pspict=pspict).get_point(ama)
    def action_on_pspict(self,pspict):
        circle=self.circle(visual=True,pspict=pspict)
        circle.parameters=self.parameters.copy()
        pspict.DrawGraph(circle)
    def latex_code(self,language=None,pspict=None):
        return ""

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
        # in 'specific_action_on_pspict' does not work.
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

    def specific_action_on_pspict(self,pspict):
    
        if False :          # No more used (April 23, 2015)
            circle=Circle(self.intersection,self.r)
            K=Intersection(circle,self.d1)
            K.sort(key=lambda P:Distance_sq(P,self.d1.I))
            L=Intersection(circle,self.d2)
            L.sort(key=lambda P:Distance_sq(P,self.d2.I))
            if self.n1==0:
                P1=K[0]
            if self.n1==1:
                P1=K[1]
            if self.n2==0:
                P2=L[0]
            if self.n2==1:
                P2=L[1]

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
