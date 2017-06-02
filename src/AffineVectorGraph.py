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

# copyright (c) Laurent Claessens, 2017
# email: laurent@claessens-donadello.eu

from sage.all import lazy_attribute,numerical_approx

from ObjectGraph import ObjectGraph
from Constructors import Segment,AffineVector,Vector,Point
from NoMathUtilities import logging
from Decorators import copy_parameters

from Debug import dprint

class AffineVectorGraph(ObjectGraph):
    def __init__(self,I,F):
        ObjectGraph.__init__(self,self)
        self.I = I
        self.F = F
        self.segment=Segment(self.I,self.F)
    @lazy_attribute
    def Dx(self):
        return self.F.x-self.I.x
    @lazy_attribute
    def Dy(self):
        return self.F.y-self.I.y
    @lazy_attribute
    def is_horizontal(self):
        return self.segment.is_horizontal
    @lazy_attribute
    def is_vertical(self):
        return self.segment.is_vertical
    @lazy_attribute
    def slope(self):
        return self.segment.slope
    @lazy_attribute
    def length(self):
        """
        Return a numerical approximation of the length.
        """
        return self.segment.length
    def fix_visual_size(self,l,xunit=None,yunit=None,pspict=None):
        s=self.segment.fix_visual_size(l,xunit,yunit,pspict)
        return AffineVector(s.I,s.F)
    def exact_length(self):
        return self.segment.exact_length
    def angle(self):
        return self.segment.angle()
    def numerical_approx(self):
        I=Point( numerical_approx(self.I.x),numerical_approx(self.I.y) )
        F=Point( numerical_approx(self.F.x),numerical_approx(self.F.y) )
        return AffineVector(I,F)
    def orthogonal(self):
        ortho_seg=self.segment.orthogonal()
        return AffineVector(ortho_seg)
    def rotation(self,angle):
        s=self.segment.rotation(angle)
        return AffineVector(s)
    def projection(self,seg):
        """
        Return the projection of 'self' on the segment 'seg' (you can also
        pass a vector).
        """
        I=self.I.projection(seg)
        F=self.F.projection(seg)
        return AffineVector(I,F)

    ##
    # Return the decomposition of `self` into a `v`-component and
    # a normal (to v) component.
    #
    #        INPUT:
    #
    #        - ``v`` - a segment or a vector
    #
    #        OUTPUT:
    #
    #        A tuple :
    #        - the first element is the orthogonale component 
    #        - the second element is the parallel component
    #
    #        NOTE:
    #
    #        The result does not depend on `v`, but only on the direction of `v`.
    def decomposition(self,seg):
        # we make the computations with vectors based at (0,0)
        # and then translate the answer.
        s0=self.fix_origin( Point(0,0) )
        if isinstance(seg,AffineVectorGraph):
            v=seg.segment()
        seg0=seg.fix_origin( Point(0,0) )

        A=s0.F.projection(seg0)
        paral0=Vector(A)

        perp0=s0-paral0

        ans_paral=paral0.fix_origin(self.I)
        ans_perp=perp0.fix_origin(self.I)

        return ans_perp,ans_paral
    def inner_product(self,other):
        from Utilities import inner_product
        return inner_product(self,other)
    def copy(self):
        return AffineVector(self.I,self.F)
    def translate(self,v):
        return AffineVector(self.I.translate(v),self.F.translate(v))
    def advised_mark_angle(self,pspict=None):
        return self.segment.advised_mark_angle(pspict)
    def midpoint(self,advised=True):
        return self.segment.midpoint(advised)
    @copy_parameters
    def fix_origin(self,P):
        """
        Return the affine vector that is equal to 'self' but attached
        to point P.
        """
        return AffineVector(P,Point(P.x+self.Dx,P.y+self.Dy))
    def normalize(self,l=1):
        """
        Return a new affine vector with
        - same starting point
        - same direction (if 'l' is negative, change the direction)
        - size l

        By default, normalize to 1.
        """
        L=self.length
        if L<0.001:     # epsilon
            logging("This vector is too small to normalize. I return a copy.")
            return self.copy()
        return (l*self).__div__(L)     
    def _bounding_box(self,pspict):
        return self.segment.bounding_box(pspict=pspict)
    def __str__(self):
        return "<AffineVectorGraph I=%s F=%s>"%(str(self.I),str(self.F))

    ## \brief put the vector `other` on the end of `self`
    #
    # This is the usual vector sum, but here we accept two vector that have
    # not the same initial point.
    #
    # \return a vector with same initial point as `self`.
    def extend(self,other):
        I=self.I
        F=self.F.translate(other.Dx,other.Dy)
        return AffineVector(I,F)

        
    ## \brief add two vectors based on the same point.
    # 
    # The function checks if the vectors `self` and `other` are based
    # on the same point. Sometimes, it causes strange problems. When 
    # one of the coordinates has the form
    # a=3.00000000000000*cos(0.111111111111111*pi)
    # Checking equalities with that kind of numbers causes 
    # OverflowError: Python int too large to convert to C long
    #
    # If you know that `v1` and `v2` have the same origin and want to sum them
    # you can also do `v1.extend(v2)`
    def __add__(self,other):
        if isinstance(other,tuple):
            if len(other)==2:
                I=self.I
                Dx=self.Dx+other[0]
                Dy=self.Dy+other[1]
                return AffineVector(self.I,self.I.translate( Vector(Dx,Dy) ))
        if other.I != self.I :
            from Exceptions import OperationNotPermitedException
            raise OperationNotPermitedException("You can only add vectors\
                            with same base point.")
        I=self.I
        Dx=self.Dx+other.Dx
        Dy=self.Dy+other.Dy
        return AffineVector(self.I,self.I.translate( Vector(Dx,Dy) ))
    def __sub__(self,other):
        return self+(-other)
    def __mul__(self,coef):
        I=self.I
        nx=self.I.x+self.Dx*coef
        ny=self.I.y+self.Dy*coef
        F=Point(nx,ny)
        return AffineVector(I,F)
    def __rmul__(self,coef):
        return self*coef
    def __div__(self,coef):
        return self*(1/coef)
    def __neg__(self):
        """
        return -self. 

        That is an affine vector attached to the same point, but
        with the opposite direction.
        """
        nx=self.I.x-self.Dx
        ny=self.I.y-self.Dy
        return AffineVector(self.I, Point(nx,ny)  )
    def __eq__(self,other):
        if self.I != other.I:
            return False
        if self.F != other.F:
            return False
        return True
    def is_almost_equal(self,other):
        if not self.I.is_almost_equal(other.I):
            return False
        if not self.F.is_almost_equal(other.F):
            return False
        return True
    def __ne__(self,other):
        return not self==other
    def mark_point(self,pspict=None):
        return self.F.copy()
    def tikz_code(self,pspict=None):
        params=self.params(language="tikz")
        params=params+",->,>=latex"
        I_coord = self.I.coordinates(numerical=True,pspict=pspict)
        F_coord = self.F.coordinates(numerical=True,pspict=pspict)
        a = "\draw [{0}] {1} -- {2};".format(params,I_coord,F_coord,pspict=pspict)
        return a
    def latex_code(self,language=None,pspict=None):
        if self.parameters.style=="none":
            return ""
        if language=="tikz":
            return self.tikz_code(pspict=pspict)
