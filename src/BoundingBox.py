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

# copyright(c) Laurent Claessens, 2010-2017
# email: laurent@claessens-donadello.eu

from Constructors import *

class BoundingBox_class(object):
    r"""
    Represent the bounding box of something.

    INPUT:

    - ``xmin`` the coordinate of the left border (same for xmax,ymin and ymax)

    - ``mother`` - the object of which this is the bounding box.

    By default, the bounding box has `mx=1000`, `Mx=-1000` and the same for `y`.

    The attribute `parent` is used for drawing the bounding boxes that can vary with
    the dilatation. The usual way for drawing the bounding bow of the mark of an object is to put
    `P.mark.bounding_box(pspict)` in `pspict.DrawGraph`.

    The problem arises when one dilates the figure after the call to `DrawGraph`.
    Indeed the bounding box of the mark will be the LaTeX's size of the box
    containing the text. In order to be correct one has to take into account the 
    parameters `xunit`/`yunit` that are not yet fixed at the time of `DrawGraph`.

    If 'math' is True, it always tries to include 'math_bounding_box' instead of 'bounding_box'
    """
    def __init__(self,P1=None,P2=None,xmin=1000,xmax=-1000,ymin=1000,ymax=-1000,parent=None,mother=None,math=False):
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.mother=mother
        self.math=math
        if P1 :
            self.add_math_object(P1,check_too_large=False)
            self.add_math_object(P2,check_too_large=False)
        self.take_math_BB=False
        self.take_BB=True
    # Because I do not want BoundingBox to inherit from ObjectGraph
    def _draw_added_objects(self,pspict):
        pass
    def add_object(self,obj,pspict=None,fun="bounding_box",check_too_large=True):
        if self.math:
            fun="math_bounding_box"
        try :
            bb=obj.__getattribute__(fun)(pspict=pspict)
        except AttributeError,message :
            if obj:     # If obj is None, we are not surprised.
                print "The attribute {1} of the object {0} seems to have problems".format(obj,fun)
                print "The message was :"
                print message
                import main
                raise main.NoMathBoundingBox(obj,fun)
        else :
            if check_too_large :
                bb.check_too_large(pspict)
            self.AddBB(bb)
    def add_math_object(self,obj,pspict=None,check_too_large=True):
        try :
            self.add_object(obj,pspict=pspict,fun="math_bounding_box",check_too_large=check_too_large)
        except TypeError :
            print("I got a TypeError with")
            print("Object",obj)
            print("of type",type(obj))
    def check_too_large(self,pspict=None):
        """
        Raise a ValueError if the bounding box is too large.
        """
        from Utilities import check_too_large
        check_too_large(self,pspict=pspict)

    def getEdge(self,pos):
        if pos=="NORTH":
            return Segment(self.getVertex("NW"),self.getVertex("NE"))
        if pos=="SOUTH":
            return Segment(self.getVertex("SW"),self.getVertex("SE"))
        if pos=="EAST":
            return Segment( self.getVertex("NE"),self.getVertex("SE") )
        if pos=="WEST":
            return Segment( self.getVertex("NW"),self.getVertex("SW") )
    def getVertex(self,pos):
        if pos=="NE":
            return Point(self.xmax,self.ymax)
        if pos=="NW":
            return Point(self.xmin,self.ymax)
        if pos=="SE":
            return Point(self.xmax,self.ymin)
        if pos=="SW":
            return Point(self.xmin,self.ymin)
    def N(self):
        return Segment(self.getVertex("NW"),self.getVertex("NE")).midpoint()
    def S(self):
        return Segment(self.getVertex("SW"),self.getVertex("SE")).midpoint()
    def coordinates(self,pspict=None):
        return self.getVertex("SW").coordinates(pspict=pspict)+self.getVertex("NE").coordinates(pspict=pspict)
    def xsize(self):
        return self.xmax-self.xmin
    def ysize(self):
        return self.ymax-self.ymin
    def extraX_left(self,l):
        """Enlarge the bounding box of a length l on the left"""
        self.xmin=self.xmin-l
    def extraX_right(self,l):
        """Enlarge the bounding box of a length l on the right"""
        self.xmax=self.xmax+l
    def extraX(self,l):
        """Enlarge the bounding box of a length l on both sides"""
        self.extraX_left(l)
        self.extraX_right(l)
    def addX(self,x):
        self.xmin=min(self.xmin,x)
        self.xmax=max(self.xmax,x)
    def addY(self,y):
        self.ymin=min(self.ymin,y)
        self.ymax=max(self.ymax,y)
    def AddBB(self,bb):
        from SmallComputations import numerical_min
        from SmallComputations import numerical_max
        self.xmin = numerical_min(self.xmin,bb.xmin)
        self.ymin = numerical_min(self.ymin,bb.ymin)
        self.xmax = numerical_max(self.xmax,bb.xmax)
        self.ymax = numerical_max(self.ymax,bb.ymax)
    def append(self,graph,pspict=None):
        if isinstance(graph,list):
            raise KeyError,"%s is a list"%graph
        if not pspict :
            raise MissingPictureException("You should provide a pspict in order to add this object to a bounding box.")

        if self.math:
            self.AddBB(graph.math_bounding_box(pspict=pspict))
        else :
            self.AddBB(graph.bounding_box(pspict=pspict))
    def add_math_graph(self,graphe,pspict=None):
        try :
            self.addBB(graphe.math_bounding_box(pspict))
        except NoMathBoundingBox,message :
            print message
            self.addBB(graphe.bounding_box(pspict))
    def AddAxes(self,axes):
        self.AddPoint( axes.BB.getVertex("SW") )
        self.AddPoint( axes.getVertex("NE") )
    def latex_code(self,language=None,pspict=None):
        return ""
    def conclude(self,pspict):
        pass
    def action_on_pspict(self,pspict=None):
        rect=Rectangle(self.getVertex("SW"),self.getVertex("NE"))
        rect.parameters.color="cyan"
        pspict.DrawGraphs(rect)
    def bounding_box(self,pspict=None):
        return self
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict)
    def copy(self):
        return BoundingBox(xmin=self.xmin,ymin=self.ymin,xmax=self.xmax,ymax=self.ymax)
    def __str__(self):
        return "<BoundingBox xmin={0},xmax={1}; ymin={2},ymax={3}>".format(self.xmin,self.xmax,self.ymin,self.ymax)
    def __eq__(self,other):
        if self.xmin!=other.xmin:
            return False
        if self.xmax!=other.xmax:
            return False
        if self.ymin!=other.ymin:
            return False
        if self.ymax!=other.ymax:
            return False
        return True
    def __ne__(self,other):
        return not self.__eq__(other)
    def __contains__(self,P):
        """
        Return True if the point P belongs to self and False otherwise.

        Allow to write
        if P in bb :
            do_something 

        from http://www.rafekettler.com/magicmethods.html
        """
        if P.x <= self.xmax and P.x>=self.xmin and P.y<=self.ymax and P.y>=self.ymin:
            return True
        return False
