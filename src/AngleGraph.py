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
from Visual import visual_polar_coordinates, visual_length,visual_vector
from NoMathUtilities import logging
from Decorators import copy_parameters
from Exceptions import MissingPictureException

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
    @copy_parameters
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
    def put_arrow(self,pspict=None):
        """
        Add a small arrow at the end of the angle,
        so one can visualize the sense of the angle ('from A to B')
        """
        if pspict is None :
            raise MissingPictureException("The method 'put_arrow' needs a picture as argument. Typical use is 'myobject.put_arrow(pspict=pspict)'")
        arrow=self.circle(pspict=pspict).get_arrow(self.angleF.degree)
        arrow.parameters=self.parameters.copy()
        self.added_objects.append(pspict,arrow)
    def mark_point(self,pspict=None):
        ama=self.advised_mark_angle(pspict)
        return self.circle(visual=True,pspict=pspict).get_point(ama)
    def _getOCvector(self,dimx,dimy,pspict=None):
        """
        Return a vector 
        O -> central point of the box
        such that the box of size (dimx,dimy) will not intersect the lines of the angle self.

          In fact we use this vector to translate from the mark_point (not the center of the angle).
          Thus we are sure that the mark will in the same time
          - not intersect the lines
          - be further than the code.

        """

        if self.angleA.degree == 0:
            x=dimy/tan(self.measure.radian)
            K=Point(self.O.x+x+dimx/2,self.O.y+dimy/2)
            return AffineVector( self.O, K )
        if 0<self.angleA.degree < 90 and 0<self.angleB.degree < 90 :
            # In this case, the mark will be attached
            # - by the upper left to the line OB (let X be that point)
            # - by the lower right to the line OA   (let Y be that point)
            # We consider 'd', the diagonal of the mark that join OA to OB
            # The triangle OXY has angle 'alpha' at O and 'beta' at Y.
            # We consider the altitude 'h' of OXY from X.
            # Let 'sigma' be the angle made by the diagonal of the box.
            # beta = self.angleA + sigma
            # Using Pythagoras'theorem and some trigonometry, we can determine all the lengths and angles.
            # The one we are interested in is OX. Trigonometry then provides the coordinates of X. 
            # Then the center of the mark's box is easy to compute as a translation by (dimx/2 , -dimy/2)

            d=sqrt(dimx**2+dimy**2)     # diagonal of the box
            sigma = arctan(dimy/dimx)
            beta = self.angleA.radian+sigma

            alpha=self.measure.radian

            h=d*sin(beta)
            l=h/sin(alpha)          # length OX

            # Here are the coordinates of X (with respect to O)
            x=l*cos(self.angleB.radian)
            y=l*sin(self.angleB.radian)

            # This is the vector O->central_point

            return AffineVector( self.O, Point( x+dimx/2,y-dimy/2) )   

        # In each case, the computed vector 'v' is the vector
        #  O -> center of the box containing the text.
        if 0<self.angleA.degree < 90 and ( self.angleB.degree==90 or self.angleB.radian==pi/2  ):
            x=0
            y=dimx/tan(self.measure.radian)
            Q=self.O+(0,y)
            return AffineVector(self.O,Q+(-dimx/2,dimy/2))

        if 0<self.angleA.degree < 90 and 90<self.angleB.degree < 180 :
            h=dimx*sin(self.angleA.radian)
            l=h/sin(self.measure.radian)
            gamma=pi-self.angleB.radian
            x=l*cos(gamma)
            y=l*sin(gamma)

            Q=self.O+(-x,y)     # lower left angle of the box
            return AffineVector(self.O, Q+(dimx/2,dimy/2) )

        if (self.angleA.radian==pi/2 or self.angleA.degree==90) and 90<self.angleB.degree<180 :
            l=dimx/tan(self.measure.radian)
            Q=self.O+(0,l)
            return AffineVector(self.O,Q+(-dimx/2,dimy/2))
            
        if 90<self.angleA.degree < 180 and 90<self.angleB.degree < 180 :
            d=sqrt(dimx**2+dimy**2)
            beta=pi-self.angleB.radian
            alpha=atan(dimy/dimx)
            gamma=alpha+beta
            sigma=2*pi-self.measure.radian-gamma
            h=d*sin(sigma)
            l=h/sin(self.measure.radian)
            tau=2*pi-self.angleB.radian

            x=l*cos(tau)
            y=l*sin(tau)
            Q=self.O+(-x,y)
            return AffineVector(self.O,Q+(-dimx/2,dimy/2))

        if 90<self.angleA.degree < 180 and (self.angleB.degree==180 or self.angleB.radian==pi) :
            l=dimy/sin(self.measure.radian)
            x=l*cos(self.measure.radian)
            y=dimy
            Q=self.O+(-x,y)
            return AffineVector( self.O, Q+(-dimx/2,-dimy/2) )

        if 90<self.angleA.degree < 180 and 180<self.angleB.degree < 270 :
            alpha=3*pi/2-self.angleB.radian
            h=dimy*sin(alpha)
            l=h/sin(self.measure.radian)
            gamma=self.angleA.radian-pi/2
            x=l*sin(gamma)
            y=l*cos(gamma)
            Q=self.O+(-x,y)
            return AffineVector(self.O,Q+(-dimx/2,-dimy/2))

        if (self.angleA.degree==180 or self.angleA.radian==pi) and  180<self.angleB.degree < 270:
            alpha=pi/2-self.measure.radian
            x=dimy*tan(alpha)
            Q=self.O+(-x,0)
            return AffineVector(self.O,Q+(-dimx/2,-dimy/2))

        if 180<self.angleA.degree < 270 and (self.angleB.degree==270 or self.angleB.radian==3*pi/2) :
            y=dimx/tan(self.measure.radian)
            Q=self.O+(0,-y)

            return AffineVector(self.O,Q+(-dimx/2,-dimy/2)  )

        if 180<self.angleA.degree < 270 and 270<self.angleB.degree < 360 :
            alpha=self.angleA.radian-pi
            h=dimx*cos(alpha)
            beta=pi/2-self.measure.radian
            l=h/cos(beta)
            gamma=2*pi-self.angleB.radian
            x=l*cos(gamma)
            y=l*sin(gamma)
            Q=self.O+(x,-y)
            return AffineVector(self.O,Q+(-dimx/2,-dimy/2))

        if 270<self.angleA.degree < 360 and 0<self.angleB.degree<90:
            alpha=self.angleB.radian
            l=dimy*cos(alpha)
            beta=pi/2-alpha
            x=l*sin(beta)
            y=l*cos(beta)
            Q=self.O+(x,y)
            return AffineVector(self.O,Q+(dimx/2,-dimy/2))

        if (self.angleA.radian==3*pi/2 or self.angleA.degree==270) and 270<self.angleB.degree<360 :
            l=dimx/tan(self.measure.radian)
            x=0
            y=l
            Q=self.O+(x,-y)
            return AffineVector(self.O,Q+(dimx/2,-dimy/2))

        if 180<self.angleA.degree < 270 and 180<self.angleB.degree<270:
            d=sqrt(dimx**2+dimy**2)
            alpha=atan(dimy/dimx)
            beta=self.angleA.radian-pi
            gamma=alpha+beta
            h=d*sin(gamma)
            l=h/cos(self.measure.radian)
            sigma=3*pi/2-self.angleB.radian
            x=l*sin(sigma)
            y=l*cos(sigma)
            Q=self.O+(-x,-y)
            return AffineVector(self.O,Q+(-dimx/2,dimy/2))

        if 180<self.angleA.degree < 270 and 270<self.angleB.degree<360:
            alpha=self.measure.radian-pi
            h=dimx*sin(alpha)
            l=h/sin(self.measure.radian)
            beta=self.angleA.radian-3*pi/2
            x=l*sin(beta)
            y=l*cos(beta)
            Q=self.O+(x,-y)
            return AffineVector( self.O,Q+(-dimx/2,-dimy/2)  )

        if 270<self.angleA.degree < 360 and 270<self.angleB.degree<360:
            alpha=2*pi-self.angleA.radian
            beta=arctan(dimy/dimx)
            sigma=alpha+beta
            d=sqrt(dimx**2+dimy**2)
            h=d*sin(sigma)
            l=h/sin(self.measure.radian)
            gamma=self.angleA.radian-3*pi/2
            x=l*sin(gamma)
            y=l*cos(gamma)
            Q=self.O+(x,-y)
            return AffineVector(self.O,Q+(dimx/2,dimy/2))

        if 270<self.angleA.degree < 360 and (self.angleB.degree==360 or self.angleB.radian==2*pi or self.angleB.radian==0 or self.angleB.degree==0) :
            l=dimy/tan(self.measure.radian)
            Q=self.O+(l,0)
            return AffineVector(self.O,Q+(dimx/2,-dimy/2))

        if 260<self.angleA.degree < 360 and ( self.angleB.degree>360 or 0<self.angleB.degree<90):
            alpha=self.angleA.radian-pi/2
            h=dimy*sin(alpha)
            l=h/sin(self.measure.radian)
            beta=pi/2-self.angleB.radian
            x=l*sin(beta)
            y=l*cos(beta)
            Q=self.O+(x,y)
            return AffineVector(self.O,Q+(dimx/2,-dimy/2))

        else :
            raise ValueError("Not yet implemented for angles :",numerical_approx(self.angleA.degree),numerical_approx(self.angleB.degree))

    def get_mark(self,dist=None,angle=None,text="",mark_point=None,added_angle=None,position=None,pspict=None):
        """
        The mark on an angle is determined in the following way.

        A vector 'v' is computed in such a way that placing
        the center of the mark at
        self.O+v
        makes the mark being just  in the angle 

        Then the center of the mark is placed at 
        self.mark_point+v

        Thus the mark should be ok.

        If you give the optional argument "dist", the vector 'v' is replaced by
        v.fix_size(dist)
        In this case you have to fix a correct value of 'dist' by hand.

        """

        mark_point=self.mark_point(pspict)

        if self.measure.degree>90 or self.measure.degree<-90 : 
            if dist is None:
                dist=0.2
            return mark_point.get_mark(dist=dist,angle=self.advised_mark_angle(pspict),text=text,position=position,pspict=pspict)

        if position != None:
            print("The mark of an angle should be given without position argument")
            raise
        
        # The default can be any value different than zero. It serves to 
        # avoid a division by zero during the first compilation.
        dimx,dimy = pspict.get_box_size(text,default_value="3pt")  

        # Now there are a lot of cases depending on the angles of the two lines determining the angle AOB.
        # We will detail the computations for the case
        #  0<self.angleA.degree < 90 and 0<self.angleB.degree < 90 
        # The other cases are the same kind of trigonometry.
        # I just let you know that if you know 3 angles and one length in a triangle, you know everything : 
        # just draw the altitude and use Pythagoras along with some trigonometry.

        # The cases are tested in the demo file 'OMPAooMbyOIqeA'

        v=self._getOCvector(dimx,dimy,pspict=pspict)

        if dist is not None :
            if dist<v.length :
                logging("The distance you give is {} while I computed the minimal to be {}".format(dist,v.length),pspict=pspict)
            v=v.normalize(dist)

        v=visual_vector(v,pspict=pspict)
        C=mark_point+v
        return Mark(self,dist=None,angle=None,text=text,mark_point=None,central_point=C,position=None,pspict=pspict)

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
        if self.d1.I.isNumericallyEqual(self.d2.I) or self.d1.I.isNumericallyEqual(self.d2.F) or self.d1.F.isNumericallyEqual(self.d2.I) or self.d1.F.isNumericallyEqual(self.d2.F):
            self.d1=d1.dilatation(1.5)
            self.d2=d2.dilatation(1.5)

        self.r=r
        self.n1=n1
        self.n2=n2
        self.intersection=Intersection(d1,d2)[0]

        # If the intersection point is one of the given points, there will be troubles.
        # For then angle between AB and CD at point I, we need A,B,C,D and I to be five different points. 
        if self.intersection.isNumericallyEqual(self.d1.I) or self.intersection.isNumericallyEqual(self.d1.F):
            self.d1=d1.dilatation(1.5)
        if self.intersection.isNumericallyEqual(self.d2.I) or self.intersection.isNumericallyEqual(self.d2.F):
            self.d2=d2.dilatation(1.5)

    def inter_point(self,I,F,n,pspict):
        v1=AffineVector(I,F)
        v=visual_length(v1,l=1,pspict=pspict)

        if n==0:
            P1=I - self.r*v
        if n==1:
            P1=I + self.r*v
        
        return P1
    def action_on_pspict(self,pspict):

        # self.intersection is the point where the angle is located.

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
