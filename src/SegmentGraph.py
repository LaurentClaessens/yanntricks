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

# copyright (c) Laurent Claessens, 2010-2017
# email: laurent@claessens-donadello.eu

from sage.all import *

from ObjectGraph import ObjectGraph,AddedObjects
from Constructors import *
from Utilities import *
from NoMathUtilities import logging

from PointGraph import PointGraph

class SegmentGraph(ObjectGraph):
    def __init__(self,A,B):
        self.I = A
        self.F = B
        if not isinstance(A,PointGraph) or not isinstance(B,PointGraph):
            from NoMathUtilities import testtype
            logging("Building a segment from something that is not\
                                a point. Here are the given objects :")
            raise TypeError
        ObjectGraph.__init__(self,self)
        self.measure=None
    @lazy_attribute
    def Dx(self):
        return self.F.x-self.I.x
    @lazy_attribute
    def Dy(self):
        return self.F.y-self.I.y
    @lazy_attribute
    def slope(self):        # It was before named "coefficient"
        """
        return the angular coefficient of line.

        This is the coefficient a in the equation
        y = ax + b

        This is not the same as the coefficient a in self.equation
        ax + by + c == 0
        
        of the points.

        OUTPUT:
        a number

        EXAMPLES::

            sage: from phystricks import *
            sage: Segment(Point(0,0),Point(1,1)).slope
            1
            sage: Segment(Point(1,1),Point(0,0)).slope
            1
            sage: Segment(Point(1,2),Point(-1,8)).slope
            -3

        NOTE:

        If the line is vertical, raise a ZeroDivisionError
        """
        return SR(self.Dy)/self.Dx
    @lazy_attribute
    def independent(self):
        """
        return the b in the equation
        y = ax + b

        If the line is vertical, raise an ZeroDivisionError

        EXAMPLES::

            sage: from phystricks import *
            sage: s = Segment(Point(0,3),Point(6,-1))
            sage: s.independent
            3

        sage: Segment(Point(1,2),Point(-1,1)).independent
        3/2
        """
        return self.I.y-self.I.x*(self.slope)
    def get_point(self,x):
        """
        Return the point of abscisses 'x' on the line.
        """
        return Point(x,self.slope*x+self.independent)
    @lazy_attribute
    def is_vertical(self):
        from Numerical import are_almost_equal
        return are_almost_equal(self.I.x,self.F.x,epsilon=0.0001)
    @lazy_attribute
    def is_horizontal(self):
        from Numerical import are_almost_equal
        return are_almost_equal(self.I.y,self.F.y,epsilon=0.0001)
    @lazy_attribute
    def equation(self):
        """
        return the equation of the line under the form
        x + by + c = 0

        Coefficients 'b' and 'c' are numerical approximations. 
        See Utilities.Intersection

        EXAMPLES::

            sage: from phystricks import *
            sage: Segment(Point(0,0),Point(1,1)).equation
            x - y == 0
            sage: Segment(Point(1,0),Point(0,1)).equation
            x + y - 1 == 0
        """
        if self.is_vertical :
            self.coefs = [1,0,-self.I.x]
        if self.is_horizontal :
            self.coefs = [0,1,-self.I.y]
        if not (self.is_vertical or self.is_horizontal) :
            self.coefs = [1,-1/self.slope,self.independent/self.slope]
        x,y=var('x,y')
        Ix=numerical_approx(self.I.x)
        Iy=numerical_approx(self.I.y)
        Fx=numerical_approx(self.F.x)
        Fy=numerical_approx(self.F.y)
        coefs=[ numerical_approx(s) for s in self.coefs  ]
        return coefs[0]*x+coefs[1]*y+coefs[2] == 0
    @lazy_attribute
    def length(self):
        """
        return (a numerical approximation of) the length of the segment

        EXAMPLES::

            sage: from phystricks import *
            sage: Segment(Point(1,1),Point(2,2)).length
            sqrt(2)

        """
        return numerical_approx(self.exact_length)
    @lazy_attribute
    def exact_length(self):
        """
        return the length of the segment.
        """
        return distance(self.I,self.F)
    def advised_mark_angle(self,pspict=None):
        return self.angle()+AngleMeasure(value_degree=90)
    def phyFunction(self):
        if self.is_horizontal:
            # The trick to define a constant function is explained here:
            # http://groups.google.fr/group/sage-support/browse_thread/thread/e5e8775dd79459e8?hl=fr?hl=fr
            x=var('x')
            fi = SR(A.y).function(x)
            return phyFunction(fi)
        if not (self.is_vertical or self.is_horizontal) :
            x=var('x')
            return phyFunction( self.slope*x+self.independent )
    def symmetric_by(self,O):
        """
        return a segment which is symmetric to 'self' with respect to the point 'O'
        """
        A=self.I.symmetric_by(O)
        B=self.F.symmetric_by(O)
        return Segment(A,B)
    def inside_bounding_box(self,bb=None,xmin=None,xmax=None,ymin=None,ymax=None):
        """
        Return a segment that is the part of self contained inside the given bounding box.
        """
        if bb:
            xmin=bb.xmin
            xmax=bb.xmax
            ymin=bb.ymin
            ymax=bb.ymax
        if self.is_vertical:
            return Segment( Point(self.I.x,ymin),Point(self.I.y,ymax)  )
        if self.is_horizontal:
            return Segment( Point(xmin,self.I.y),Point(xmax,self.I.y)  )
        bxmin=Segment( Point(xmin,-1),Point(xmin,1) )
        bxmax=Segment( Point(xmax,-1),Point(xmax,1) )
        bymin=Segment( Point(-1,ymin),Point(1,ymin) )
        bymax=Segment( Point(-1,ymax),Point(1,ymax) )
        # We compute the intersections of self with the four lines describing the window.
        # Two of them will be the initial and final point of the searched segment.
        Ixmin=Intersection(self,bxmin)[0]
        Ixmax=Intersection(self,bxmax)[0]
        Iymin=Intersection(self,bymin)[0]
        Iymax=Intersection(self,bymax)[0]
        l=[]
        if Ixmin.y>= ymin and Ixmin.y <= ymax :
            l.append(Ixmin)
        if Ixmax.y>= ymin and Ixmax.y <= ymax :
            l.append(Ixmax)
        if Iymin.x>= xmin and Iymin.x <= xmax :
            l.append(Iymin)
        if Iymax.x >= xmin and Iymax.x <= xmax :
            l.append(Iymax)
        if len(l) == 0:     # this is the case in which the line does not cross the window.
            return None
        if len(l) != 2:
            if Ixmin==Iymax and Ixmin in l:
                l.remove(Ixmin)
            if Ixmax==Iymax and Ixmax in l:
                l.remove(Ixmax)
            if Ixmax==Iymin and Ixmax in l:
                l.remove(Ixmax)
            if Ixmin==Iymin and Ixmin in l:
                l.remove(Ixmin)
        if len(l) != 2:
            print("We found {} points".format(len(l)))
            for p in l :
                print(p)
            print("The segment is {}, with equation {} ".format(self,self.equation))
            print("and the intersection points are :")
            for P in [Ixmin,Ixmax,Iymin,Iymax]:
                print(   "({},{})".format(P.x,P.y)  )
            raise ValueError
        return Segment(  l[0],l[1]  )
    def segment(self,projection=False):
        """
        serves to transform a vector into a segment
        """
        return Segment(self.I,self.F)
    def fit_inside(self,xmin,xmax,ymin,ymax):
        """
        return the largest segment that fits into the given bounds
        """
        if self.is_horizontal:
            k=self.I.y
            return Segment(  Point(xmin,k),Point(xmax,k)  )
        if self.is_vertical:
            k=self.I.x
            return Segment(  Point(x,ymin),Point(x,ymax)  )

        x=var("x")
        f=self.phyFunction()
        x1=solve( [ f(x)==ymax ],x )[0].rhs()
        x2=solve( [ f(x)==ymin ],x )[0].rhs()
        x1=QQ(x1)
        x2=QQ(x2)
        X=[xmin,x1,x2,xmax]
        X.sort()
        A=Point(  X[1],f(X[1]) ) 
        B=Point(X[2],f(X[2]))
        return Segment(   Point(  X[1],f(X[1]) )  ,Point(X[2],f(X[2]))  )
    def parametric_curve(self):
        """
        Return the parametric curve corresponding to `self`.

        The starting point is `self.I` and the parameters is the arc length.
        The parameter is positive on the side of `self.B` and negative on the
        opposite side.

        EXAMPLES::

            sage: from phystricks import *
            sage: segment=Segment(Point(0,0),Point(1,1))
            sage: curve=segment.parametric_curve()
            sage: print curve(0)
            <Point(0,0)>
            sage: print curve(1)
            <Point(1/2*sqrt(2),1/2*sqrt(2))>
            sage: print curve(segment.length)
            <Point(1,1)>
        """
        x=var('x')
        l=self.length
        f1=phyFunction(self.I.x+x*(self.F.x-self.I.x)/l)
        f2=phyFunction(self.I.y+x*(self.F.y-self.I.y)/l)
        return ParametricCurve(f1,f2,(0,l))
    def copy(self):
        return Segment(self.I,self.F)
    def get_regular_points(self,dx):
        """
        Notice that it does not return the last point of the segment, unless the length is a multiple of dx.
           this is why we add by hand the last point in GetWavyPoint
        """
        n = floor(self.length/dx)
        return [self.get_point_proportion(float(i)/n) for i in range(0,n)]
    def get_wavy_points(self,dx,dy):
        """
        Return a list of points that make a wave around the segment.
        The wavelength is dx and the amplitude is dy.
        The first and the last points are self.I and self.F and are then *on* the segment. Thus the wave begins and ends on the segment.
        """
        normal = self.get_normal_vector().normalize(dy)
        PI = self.get_regular_points(dx)
        PIs = [self.I]
        PIs.extend( [  PI[i].translation(normal*(-1)**i) for i in range(1,len(PI))  ] )
        PIs.append(self.F)
        return PIs
    def get_point_length(self,d,advised=True):
        """
        Return a point on the segment at distance 'd' from the initial point (in the direction of the final point)
        """
        return self.get_point_proportion(d/self.length,advised=advised)
    def get_point_proportion(self,p,advised=True):
        """
        Return a point on the segment which is at the position
        (p-1)*I+p*F
        if I and F denote the initial and final point of the segment.
        """
        P = self.I*(1-p) + self.F*p
        if advised:
            P._advised_mark_angle=self.angle().degree+90
        return P
    def put_arrow(self,position=0.5,size=0.01,pspict=None):
        """
        Add a small arrow at the given position. 
        `position` is a number between 0 and 1.

        The arrow is pointed from self.I to self.F and is by
        default put at the middle of the segment.

        The arrow is a vector of size (by default) 0.01. 
        """
        P=self.get_point_proportion(position,advised=False)
        v=AffineVector(P,self.F).normalize(size)
        self.added_objects.append(pspict,v)
    def put_measure(self,measure_distance,mark_distance,mark_angle=None,\
                            text="",position=None,pspict=None,pspicts=None):
        pspicts=make_psp_list(pspict,pspicts)
        for psp in pspicts:
            measure=self.get_measure(measure_distance,mark_distance,mark_angle,\
                    text,position=position,pspict=psp)
            self.added_objects.append(psp,measure)
    def get_measure(self,measure_distance,mark_distance, mark_angle=None,\
                    text=None,position=None,pspict=None,pspicts=None):
        """
        The difference between 'put_measure' and 'get_measure'
        is that 'get_measure' returns the measure graph while
        'put_measure' adds the measure graph to the segment.

        This allows constructions like
        mesL=Segment(F,D).get_measure(-0.2,0.1,90,"\( 10\)",pspict=pspict,position="S")
        and then draw mesL. The Segment(F,D) object is not drawn.

        If 'mark_angle' is 'None', then the angle
        will be perpendicular to 'self'
        """
        pspicts=make_psp_list(pspict,pspicts)

        if mark_angle==None and position not in ["N","S","E","W"]:
            mark_angle=self.angle()+90*degree
        measure=MeasureLength(self,measure_distance)

        measure.put_mark(mark_distance,mark_angle,text,\
                position=position,pspicts=pspicts)
        return measure
    def put_code(self,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
        """
        add small line at the center of the segment.

        'n' add 'n' small lines. Default is 1
        'd' is the distance between two of them
        'l' is the (visual) length of the segment
        'angle' is the angle with 'self'.
        """
        ao=self.get_code(n=n,d=d,l=l,angle=angle,pspict=pspict)
        self.added_objects.extend(pspict,ao)
    def get_code(self,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
        #TODO : the angle given here should be visual
        ao=[]
        vect=AffineVector(self.I,self.F).normalize(d)
        center=self.midpoint(advised=False)
        positions=[]
        if n%2==1:
            for k in range( int(-(n-1)/2),int((n-1)/2)+1 ):
                positions.append(center.translation(k*vect))
        if n%2==0:
            import numpy
            for k in numpy.linspace(-n/2+0.5,n/2-0.5,n):
                positions.append(center.translation(k*vect))
        mini1=self.rotation(angle).fix_visual_size(l)
        for P in positions:
            mini=mini1.translation(AffineVector(mini1.midpoint(),P))
            ao.append(mini)
        return ao
    def get_divide_in_two(self,n=1,d=0.1,l=0.1,angle=45\
                            ,pspict=None,pspicts=None):
        pspicts=make_psp_list(pspict,pspicts)
        M=self.midpoint()
        s1=Segment(self.I,M)
        s2=Segment(M,self.F)
        a=AddedObjects()
        for psp in pspicts:
            s1.put_code(n=n,d=d,l=l,pspict=psp)
            s2.put_code(n=n,d=d,l=l,pspict=psp)
            a.fusion(s1.added_objects)
            a.fusion(s2.added_objects)
        return a
    def divide_in_two(self,n=1,d=0.1,l=0.1,angle=45,pspict=None,pspicts=None):
        pspicts=make_psp_list(pspict,pspicts)
        for psp in pspicts:
            a=self.get_divide_in_two(n=n,d=d,l=l,angle=angle,pspicts=pspicts)
            self.added_objects.fusion(a)
    def Point(self):
        """
        Return the point X such that as free vector, 0->X == self

        More precisely, if self is the segment A->B, return the point B-A
        """
        return self.F-self.I
    def midpoint(self,advised=True):
        P = self.get_point_proportion(0.5,advised)
        return P
    def AffineVector(self):
        return AffineVector(self.I,self.F)
    def get_normal_vector(self,origin=None):
        """
        returns a normalized normal vector at the center of the segment

        - `origin` (optional). If given, the vector will 
            be attached to that point.
        """
        if self.is_vertical :
            v = Point(-1,0).Vector().fix_origin(self.midpoint())
        else :
            P = Point(self.slope,-1)
            v = P.Vector().normalize().fix_origin(self.midpoint())
        if origin:
            v=AffineVector(origin,origin.translation(v))
        return v
    def get_tangent_vector(self):
        """
        return a tangent vector at center of the segment
        """
        C=self.midpoint()
        v=self.AffineVector()
        return v.fix_origin(self.midpoint()).normalize(1)
    def polaires(self):
        return PointToPolaire(self.Point())
    def angle(self):
        """
        return the angle of the segment.

        This is the angle between the segment and the horizontal axe. 
        The returned angle is positive.

        EXAMPLES::

            sage: from phystricks import *
            sage: S=Segment(Point(1,1),Point(2,2))
            sage: type(S.angle())
            <class 'phystricks.SmallComputations.AngleMeasure'>
            sage: S.angle().degree
            45
            sage: S.angle().radian
            1/4*pi

            sage: S=Segment(Point(1,1),Point(2,0))
            sage: S.angle().degree
            315
        """
        return self.polaires().measure.positive()
    def direction(self):
        return self.F-self.I
    def projection(self,segment,advised=False):
        """
        Return the projection of self on the given segment

        It also works with vectors

        INPUT:
        - ``segment`` - the line on which we want to project

        EXAMPLES::

            sage: from phystricks import *
            sage: l = Segment(Point(0,0),Point(0,1))
            sage: v = AffineVector(Point(-1,1),Point(-2,3))
            sage: print v.equation
            x + 1/2*y + 1/2 == 0
            sage: print v.projection(l)
            <vector I=<Point(0,1)> F=<Point(0,3)>>
            sage: print l.projection(v)
            <segment I=<Point(-2/5,-1/5)> F=<Point(-4/5,3/5)>>
        
            sage: l = Segment(Point(0,0),Point(1,2))
            sage: s = Segment(Point(-2,1),Point(-3,4))
            sage: print s.projection(l)
            <segment I=<Point(0,0)> F=<Point(1,2)>>
        """
        v = Segment(self.I.projection(segment),self.F.projection(segment))
        if advised:
            v._advised_mark_angle=self.angle().degree+90
        return v
    def bisector(self,code=None):
        """
        return the segment which is orthogonal to the center of 'self'.
        """
        normal=self.get_normal_vector()
        M=self.midpoint()
        P1=M.translation(normal)
        P2=M.translation(-normal)
        seg=Segment(P1,P2)
        if code:
            s1=Segment(self.I,M)
            s2=Segment(M,self.F)
            s1.put_code(n=code[0],d=code[1],l=code[2],angle=code[3],pspict=code[4])
            s2.put_code(n=code[0],d=code[1],l=code[2],angle=code[3],pspict=code[4])
            seg.added_objects.append(code[4],s1)
            seg.added_objects.append(code[4],s2)
        return seg
    def orthogonal(self,point=None):
        """
        return the segment with a rotation of 90 degree.
        The new segment is, by default, still attached to the same point.

        If 'point' is given, the segment will be attached to that point

        Not to be confused with self.get_normal_vector
        """
        new_Dx=-self.Dy
        new_Dy=self.Dx
        ortho=Segment(self.I,Point(self.I.x+new_Dx,self.I.y+new_Dy))
        if not point:
            return ortho
        return ortho.fix_origin(point)
    def orthogonal_trough(self,P):
        """
        return a segment orthogonal to self passing trough P.

        The starting point is 'P' and the final point is the 
        intersection with 'self'

        If these two points are the same --when d^2(P,Q)<0.001 
        (happens when 'P' belongs to 'self'), the end point is not guaranteed.

        By the way, when you want
        Segment(A,B).orthogonal_trough(B)
        you can use
        seg=Segment(B,A).orthogonal()
        instead.
        """
        s=self.orthogonal().fix_origin(P)
        Q=Intersection(s,self)[0]
        if (P.x-Q.x)**2+(P.y-Q.y)**2 <0.001 :
            return s
        else :
            return Segment(P,Q)
    def parallel_trough(self,P):
        """ 
        return a segment parallel to self passing trough P
        """
        v=self.F-self.I
        Q=P.translation(v)
        return Segment(P,Q)

    ## \brief Return true is `self` and `other` are orthogonal segments 
    #
    # The answer is exact, so you can be surprised if some numerical 
    # approximations were made before.
    # 
    # \see `is_almost_orthogonal`
    def is_orthogonal(self,other):
        if self.is_vertical:
            return other.is_horizontal
        if self.is_horizontal:
            return other.is_vertical
        if self.slope==-1/other.slope:
            return True
        return False
    ## \brief Return true is `self` and `other` are orthogonal segments 
    #
    # The answer is based on numerical approximations of the slopes.
    # If \f$ k \f$ is the slope of `self`, check if the slope of the other
    # is \f$ -1/k \f$ up to `epsilon`. 
    # 
    # \see `is_orthogonal`
    def is_almost_orthogonal(self,other,epsilon=0.001):
        if self.is_vertical:
            return other.is_horizontal
        if self.is_horizontal:
            return other.is_vertical

        s_slope=numerical_approx(self.slope)
        o_slope=numerical_approx(other.slope)

        if abs(s_slope+1/o_slope)<epsilon :
            return True
        return False

    ##  \brief translate the segment with the given vector
    # 
    # If two arguments are given, we assume that they are the coordinates of
    # the translation vector.
    # If only one argument is given, we assume that this is the vector.
    #
    # So there are two way to use :
    #    ```
    #    segment.tranlate(v)
    #    ```
    #    and
    #    ```
    #   segment.tranlate(x,y)
    #    ```
    # In the first case `v` is a vector and in the second case, `x` and `y` are 
    # numbers.
    kkslmdfklm
    def translate(self,a,b=None):
        if b is not None :
            vector=AffineVector(Point(0,0),Point(a,b))
        else :
            vector=a
        v = Segment(self.I.translate(vector),self.F.translate(vector))
        return v
    def fix_origin(self,a,b=None):
        """
        Return the segment fixed at `P`. This is the translation of `self`  by `P-self`.  In other words, it returns the segment which is parallel to self trough the given point.

        Typically it is used in the framework of affine vector..

        INPUT:

        - ``P`` - The point on which we want to "attach" the new segment.

        or 

        - two numbers that are the coordinates of the "attach" point.

        OUTPUT:

        A new segment (or vector) with initial point at `P`

        EXAMPLES:
    
        We can fix the origin by giving the coordinates of the new origin::

            sage: from phystricks import *
            sage: v=AffineVector( Point(1,1),Point(2,2) )
            sage: w=v.fix_origin(3,5)
            sage: w.I.coordinates(),w.F.coordinates()
            ('(3,5)', '(4,6)')
        
        We can also give a point::    

            sage: P=Point(-1,-pi)
            sage: u=w.fix_origin(P)
            sage: u.I.coordinates(),u.F.coordinates()
            ('(-1,-pi)', '(0,-pi + 1)')
        """
        if b is not None:
            P=Point(a,b)
        else:
            P=a
        I=P
        F=P.translate(self.Dx,self.Dy)
        s=Segment(I,F)

        return s
    def inverse(self):
        """
        Return the segment BA instead of AB.

        Not to be confused with (-self). The latter is a rotation
        of 180 degree of self.
        """
        v = Segment(self.F,self.I)
        return v
    def rotation(self,angle):
        """
        Return the segment attached to the same point but with
        a rotation of angle.

        INPUT:

        - ``angle`` - the value of the rotation angle (degree or AngleMeasure)

        """
        a=angle
        if isinstance(angle,AngleMeasure):
            a=angle.degree
        v = PolarSegment(self.I,self.polaires().r,self.polaires().degree+a)
        return v
    def get_visual_length(self,xunit=None,yunit=None,pspict=None):
        """
        Return the visual length of self. That is the length
        taking xunit and  yunit into account
        """
        if pspict:
            xunit=pspict.xunit
            yunit=pspict.yunit
        Dx=(self.F.x-self.I.x)*xunit
        Dy=(self.F.y-self.I.y)*yunit
        if self.is_vertical:
            return Dy
        else: 
            return sqrt(Dx**2+Dy**2)
    def fix_visual_size(self,l,xunit=None,yunit=None,pspict=None):
        """
        return a segment with the same initial point, but with visual length  `l`
        """
        from Visual import visual_length
        if pspict:
            xunit=pspict.xunit
            yunit=pspict.yunit
        if xunit==None or yunit==None:
            return self.fix_size(l)
        return visual_length(self,l,xunit,yunit,pspict)
    def add_size_extremity(self,l):
        """
        Add a length <l> at the extremity of the segment. Return a new object.
        """
        L=self.length
        coef=(l+L)/L
        v = coef*self
        return v
    def fix_size(self,l,only_F=False,only_I=False):
        """
        return a new segment with size l.

        This function has not to be used by the end user. 
        Use self.normalize() instead.
        """
        L=self.length
        if only_F and only_I:
            print("You cannot ask both only F and only I")
            raise ValueError
        if L <  0.001 :     # epsilon
            print "fix_size problem: this vector has a norm equal to zero"
            return self.copy()
        if only_F==False and only_I==False:
            v = self.dilatation(l/self.length)
        if only_F :
            v=self.add_size( lF= l-L  )
        if only_I :
            v=self.add_size( lI= l-L  )
        return v
    def add_size(self,lI=0,lF=0):
        """
        Return a new Segment with extra length lI at the initial side and lF at the final side. 
        """
        F=self.add_size_extremity(lF).F
        I=self.inverse().add_size_extremity(lI).F
        v = Segment(I,F)
        return v
    def dilatation(self,coef):
        """
        Return a Segment which is dilated by the coefficient coef 

            This adds the same length at both extremities.
            The segment A --> B dilated by 0.5 returns
            a segment C --> D where [CD] is the _central_ half of [AB].
            If you want to add some length to one
            of the extremities, use
            self.add_size
            or
            l*self
            with a scalar l.

        INPUT:
        - ``coef`` - a number. This is the dilatation coefficient

        OUTPUT:
        a new segment

        EXAMPLES::

            sage: from phystricks import *
            sage: S=Segment(Point(-2,-2),Point(2,2))
            sage: print S.dilatation(0.5)           
            <segment I=<Point(-1.00000000000000,-1.00000000000000)> F=<Point(1.00000000000000,1.00000000000000)>>

        But ::

            sage: v=AffineVector(Point(-2,-2),Point(2,2))
            sage: print v.dilatation(0.5)                
            <vector I=<Point(-2,-2)> F=<Point(0.000000000000000,0.000000000000000)>>
        """
        d=0.5*self.length*(coef-1)
        return self.add_size(d,d)
    def dilatationI(self,coef):
        """
        return a dilated segment, but only enlarges at the initial extremity.
        """
        v=AffineVector(self)
        w=-v
        wp=w*coef
        return Segment(wp.F,v.F)
    def dilatationF(self,coef):
        """
        return a dilated segment, but only enlarges at the final extremity.
        """
        v=self.AffineVector()
        v=v*coef
        return Segment(v.I,v.F)
    def normalize(self,l=1):
        """
        Normalize the segment to <l> by dilating in both extremities

        NOTES:
        * If self is of length zero, return a copy of self.
        * If not length is given, normalize to 1.
        * If the given new length is negative, 
            if self is a segment, consider the absolute value

        INPUT:
        - ``l`` - (default=1) a number, the new length

        OUTPUT:
        A segment or a vector

        EXAMPLES::

            sage: from phystricks import *
            sage: s=Segment(Point(0,0),Point(1,0))
            sage: print s.normalize(2)
            <segment I=<Point(-0.5,0)> F=<Point(1.5,0)>>
            sage: print s.normalize(-1)
            <segment I=<Point(0,0)> F=<Point(1,0)>>

        """
        if l<0 : 
            l=-l
        v = self.fix_size(l)
        return v
    def graph(self,mx=None,Mx=None):
        if not mx:
            C = SegmentGraph(self.I,self.F)
        else :
            C = SegmentGraph(self.get_point(mx),self.get_point(Mx))
        C.parameters=self.parameters.copy()
        return C
    def default_associated_graph_class(self):
        """Return the class which is the Graph associated type"""
        return SegmentGraph
    def __mul__(self,coef):
        """
        multiply the segment by a coefficient.

        INPUT:
        - ``coef`` - the multiplying coefficient

        OUTPUT:
        A new segment.

        EXAMPLES::

            sage: s=Segment(Point(1,1),Point(2,2))
            sage: print 3*s
            <segment I=<Point(1,1)> F=<Point(4,4)>>

        The initial point stays the same (this is not the same behaviour as in self.normalize !)
        """
        if coef<=0:
            coef=-coef
        v = Segment(self.I,Point(self.I.x+self.Dx*coef,self.I.y+self.Dy*coef))
        return v
    def translation(self,v):
        return Segment(self.I.translation(v),self.F.translation(v))
    def __add__(self,other):
        """
        If the other is a vector, return the translated segment

        INPUT:
        - ``other`` - an other segment

        OUTPUT:
        A new  segment that has the same origin as `self`.

        EXAMPLES::

            sage: from phystricks import *
            sage: a=Vector(1,1)
            sage: b=Vector(2,3)
            sage: print a+b
            <vector I=<Point(0,0)> F=<Point(3,4)>>
        """
        print("If you want to translate something you should\
                probably use '.translation' instead.") 
        raise DeprecationWarning
        from AffineVectorGraph import AffineVectorGraph
        from PointGraph import PointGraph
        if isinstance(other,AffineVectorGraph):
            return Segment(   self.I+other,self.F+other  )
        if isinstance(other,PointGraph):
            return self+Vector(other)
        if isinstance(other,tuple):
            if len(other)!=2:
                raise TypeError("You can add a SegmentGraph with a tuple\
                        of length 2, not "+str(len(other)))
            return self+Vector(other)
        else:
            raise TypeError,"I do not know how to sum %s with %s"%(self,other)
    def __sub__(self,other):
        raise
        return self+(-other)
    def __rmul__(self,coef):
        return self*coef
    def __neg__(self):
        return Segment(self.F,self.I)
    def __div__(self,coef):
        return self * (1/coef)
    def __div__(self,coef):
        return self * (1/coef)
    def __str__(self):
        return "<segment I=%s F=%s>"%(str(self.I),str(self.F))
    def mark_point(self,pspict=None):
        """
        return the point on which a mark has to be placed
        if we use the method put_mark.  
        If we have a segment, the mark is at center 
        """
        return self.midpoint().copy()
    def _bounding_box(self,pspict):
        if self.in_bounding_box:
            return BoundingBox(self.I,self.F)
        else :
            return BoundingBox()
    def _math_bounding_box(self,pspict=None):
        if self.in_math_bounding_box:
            return self.bounding_box(pspict)
        else :
            return BoundingBox()
    def representative_points(self):
        return [self.I,self.F]
    def latex_code(self,language=None,pspict=None):
        if self.parameters.style=="none":
            return ""
        if self.wavy:
            waviness = self.waviness
            curve=InterpolationCurve(self.get_wavy_points(waviness.dx,waviness.dy),context_object=self)
            curve.parameters=self.parameters.copy()
            return curve.latex_code(language=language,pspict=pspict)
        else:
            if language=="tikz":
                a=[]
                c1=self.I.coordinates(numerical=True,digits=3,pspict=pspict)
                c2=self.F.coordinates(numerical=True,digits=3,pspict=pspict)
                if 'I' in c1 or "I" in c2 :
                    from Exception import ImaginaryPartException
                    raise ImaginaryPartException(
                        "Probably an imaginary part in "+str(c1)+" or "+str(c2))
                a.append("\draw [{2}] {0} -- {1};".format(
                                        c1,c2,self.params(language="tikz")))

        return "\n".join(a)
    def tikz_code(self,pspict=None):
        return self.latex_code(language="tikz",pspict=pspict)
