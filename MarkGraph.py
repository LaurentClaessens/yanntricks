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

# copyright(c) Laurent Claessens, 2010-2016
# email: moky.math@gmai.com

from phystricks.ObjectGraph import ObjectGraph
from Constructors import *
from Utilities import *

class MarkGraph(object):
    def __init__(self,graph,dist,angle,text,mark_point=None,automatic_place=False):
        self._central_point=None
        self.mark_point=mark_point
        self.graph = graph
        self.parent = graph
        self.angle = angle
        self.dist = dist
        self.text = text
        self.angle = angle
        self.automatic_place=automatic_place
        alpha=radian(angle)
        if isinstance(alpha,AngleMeasure):
            self.x=self.dist*cos(alpha.radian)
            self.y=self.dist*sin(alpha.radian)
        else :
            self.x=self.dist*cos(alpha)
            self.y=self.dist*sin(alpha)

    def central_point(self,pspict=None):
        """
        Return the central point of the mark, that is the point where the mark arrives.

        The central point of the mark is computed from self.graph.mark_point()
        Thus an object that wants to accept a mark needs a method mark_point that returns the point on which the mark will be put.
        """
        if self._central_point:
            return self._central_point
        if self.mark_point :
            graph_mark_point=self.mark_point
        else :
            try :
                graph_mark_point=self.graph.mark_point(pspict=pspict)
            except TypeError :          # Happens when mark_point is redefined as a 'lambda' function
                graph_mark_point=self.graph.mark_point()
   
        default=graph_mark_point.get_polar_point(self.dist,self.angle,pspict)

        if self.automatic_place :
            pspict=self.automatic_place[0]
            position=self.automatic_place[1]

            # The idea here is to allow to use the same point in several pictures and to ask
            # each figure to remember the box size.
            if not isinstance(pspict,list):
                pspict=[pspict]

            for psp in pspict:
                dimx,dimy = psp.get_box_size(self.text)
                dimx=float(dimx)/psp.xunit
                dimy=float(dimy)/psp.yunit

            # See some explanations at 104835555
            if position=="for axes":
                seg=self.automatic_place[2]
                alpha=seg.angle().radian
                d=self.dist+0.5*max(dimx*sin(alpha),dimy*cos(alpha))
                beta=degree(-pi/2+alpha)
                beta=self.angle
                return graph_mark_point.get_polar_point(d,beta)

            if position=="center":
                return default

            if position=="corner":
                if self.x>=0:
                    lx=dimx*0.5
                if self.x<0:
                    lx=-dimx*0.5
                if self.y>=0:
                    ly=dimy*0.5
                if self.y<0:
                    ly=-dimy*0.5
                return default.translate(lx,ly)
            if position=="N":
                return default.translate(0,-dimy*0.5)
            if position=="S":
                return default.translate(0,dimy*0.5)
            if position=="W":
                return default.translate(dimx*0.5,0)
            if position=="E":
                return default.translate(-dimx*0.5,0)
            print("Something wrong. I think the 'position' argument is not good :",position)
            raise ValueError
        else :
            return default
    def math_bounding_box(self,pspict=None):
        """
        Return the mathematics bounding box of its base object.

        A mark has non own math_bounding_box because we do not want the axes to fit the marks.
        This is the deep difference between math_bounding_box and bounding_box. We want the
        marks to be fit in the bounding_box since if not the mark risks to be cut
        in the pdf/png version.
        """
        return self.graph.math_bounding_box(pspict)
    def bounding_box(self,pspict=None):
        central_point=self.central_point(pspict)
        if not central_point:
            print("No central point. Parent =",self.parent)
            raise
        bb=BoundingBox(central_point,central_point)
        dimx,dimy=pspict.get_box_size(self.text)
        try :
            dimx=float(dimx)/pspict.xunit
            dimy=float(dimy)/pspict.yunit
        except AttributeError:
            print "Try to pass a pspicture when computing the bounding box of",type(self)
        pt1=Point(central_point.x-dimx/2,central_point.y-dimy/2) 
        pt2=Point(central_point.x+dimx/2,central_point.y+dimy/2)
        bb.add_object(pt1,pspict)
        bb.add_object(pt2,pspict)
        bb.parent=self
        return bb
    def action_on_pspict(self,pspict=None):
        pass
    def pstricks_code(self,pspict=None):
        raise DeprecationWarning
        l=[]
        central_point=self.central_point(pspict)
        #TODO : Use create_PSpoint instead of \pstGeonode.
        l.append("\pstGeonode[]"+central_point.coordinates(numerical=True,pspict=pspict)+"{"+central_point.psName+"}")
        l.append(r"\rput({0}){{\rput({1};{2}){{{3}}}}}".format(central_point.psName,"0",0,self.text))
        return "\n".join(l)
    def tikz_code(self,pspict=None):
        central_point=self.central_point(pspict)
        code="\draw "+central_point.coordinates(numerical=True,pspict=pspict)+" node {"+self.text+"};"
        return code
    def latex_code(self,language=None,pspict=None):
        if language=="pstricks":
            raise DeprecationWarning
            return self.pstricks_code(pspict=pspict)
        if language=="tikz":
            return self.tikz_code(pspict=pspict)
