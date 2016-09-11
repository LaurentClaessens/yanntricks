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

# copyright (c) Laurent Claessens, 2016
# email: laurent@claessens-donadello.eu

from sage.all import lazy_attribute

from ObjectGraph import ObjectGraph
from Constructors import Segment,AffineVector,Vector,Point

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
    def horizontal(self):
        return self.segment.horizontal
    @lazy_attribute
    def vertical(self):
        return self.segment.vertical
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
    def decomposition(self,v):
        """
        return the decomposition of `self` into a `v`-component and
        a normal (to v) component.

        INPUT:

        - ``v`` - a segment or a vector

        OUTPUT:

        a tuple of vectors that are the decomposition of `self` 
        into `v` and `v-perp` directions

        NOTE:

        The result does not depend on `v`, but only on the direction of `v`.

        EXAMPLES::

            sage: from phystricks import *
            sage: v=Vector(2,3)
            sage: vx,vy = v.decomposition(Segment(Point(0,0),Point(0,1)))
            sage: print vx
            <vector I=<Point(0,0)> F=<Point(0,3)>>
            sage: print vy
            <vector I=<Point(0,0)> F=<Point(2,0)>>

        .. literalinclude:: phystricksExDecomposition.py
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition0PICTExDecompositionpspict0-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition1PICTExDecompositionpspict1-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition2PICTExDecompositionpspict2-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition3PICTExDecompositionpspict3-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition4PICTExDecompositionpspict4-for_eps.png
        .. image:: Picture_FIGLabelFigExDecompositionssLabelSubFigExDecomposition5PICTExDecompositionpspict5-for_eps.png
        """
        O=Point(0,0)

        # Vector based at O which represents 'self'
        v0=Vector(self.Dx,self.Dy)      

        A=v0.F.projection(v)
        v1=Vector(A)
        v2=v0-v1
        return v1,v2
    def advised_mark_angle(self,pspict=None):
        return self.segment.advised_mark_angle(pspict)
    def midpoint(self,advised=True):
        return self.segment.midpoint(advised)
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
    def __str__(self):
        return "<vector I=%s F=%s>"%(str(self.I),str(self.F))
    def __add__(self,other):
        return AffineVector(self.I,self.F+other)
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
        if language=="pstricks":
            raise DeprecationWarning
        if language=="tikz":
            return self.tikz_code(pspict=pspict)
