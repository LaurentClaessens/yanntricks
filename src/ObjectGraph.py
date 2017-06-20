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

from __future__ import division

from sage.all import *

from parameters.Options import Options
from parameters.Parameters import Parameters
from Exceptions import ShouldNotHappenException
from NoMathUtilities import logging
from AddedObjects import AddedObjects

##
# This class is supposed to be used to create other "<Foo>Graph"
# by inheritance. 
#
# Objects that are going to be drawn have to derive from `ObjectGraph`.
# When creating you own class,
# - do not override `bounding_box` nor `math_bounding_box` 
# - create the functions `_bounding_box` and eventually `_math_bounding_box`
# - consider the attributes `take_BB` and `take_math_BB`.
class ObjectGraph(object):
    def __init__(self,obj):
        self.obj = obj
        self.parameters = Parameters(self.obj)
        self.wavy = False
        self.waviness = None
        self.options = Options()
        self.draw_bounding_box=False

        self.already_computed_BB={}
        self.already_computed_math_BB={}

        self.record_add_to_bb=[]         
        self.separator_name="DEFAULT"
        self.in_math_bounding_box=True
        self.in_bounding_box=True
        self._draw_edges=False
        self.added_objects=AddedObjects()

        self.take_BB=True
        self.take_math_BB=True

        self.mark=None

    def draw_edges(self):
        self._draw_edges=True
    def wave(self,dx,dy):     # dx is the wave length and dy is the amplitude
        from parameters.Waviness import Waviness
        self.wavy = True
        self.waviness = Waviness(self,dx,dy)
    def get_arrow(self,llam):
        """
        return a small arrow at position 'llam'.

        This only works if one has a 'get_tangent_vector' method.

        - `llam` could be radian, degree or something else, depending on the 
            actual object on which you are using this.
        """
        try :
            v = self.get_tangent_vector(llam)
        except AttributeErrror :
            print("you are using 'get_arrow' (probably from a 'put_arrow' on your part) on an object that does not support 'get_tangent_vector'")
        v=v.normalize(0.01)
        return v
    def get_mark(self,dist,angle=None,text=None,mark_point=None,\
            added_angle=None,position=None,pspict=None):
        """
        - `angle` is degree or AngleMeasure
        
        In the internal representation of the mark, 
        the angle type will be `AngleMeasure`
        """
        from AngleGraph import AngleGraph
        from Constructors import Mark
        from MathStructures import AngleMeasure

        self.marque = True
        third=None

        if position in ["N","S","E","W"] and angle is not None:
            angle=None
            logging("When you want a position like N,S,E, or W, the mark\
 angle should not be given.",pspict=pspict)


        if angle is None and position not in ["N","S","E","W"] :
            try :
                angle=self.advised_mark_angle(pspict=pspict)
            except AttributeError :
                a=self.angle()
                angle=self.angle().degree+90

        if position=="center_direction":
            # In this case we assume 'self' is a point
            angle=angle.degree

        if isinstance(angle,AngleMeasure):
            angle=angle.degree

        # At this point, 'angle' has to be degree,
        # - for the possibility of "added_angle"
        # - the constructor of 'mark' expects degree or AngleMeasure

        if added_angle: 
            angle=angle+added_angle
        if  position==None :        
            position="corner"
            alpha=AngleMeasure(value_degree=angle).positive()
            deg=alpha.degree
            if deg==0:
                position="W"
            if deg==90:
                position="S"
            if deg==180:
                position="E"
            if deg==180+90:
                position="N"

        if position in ["N","S","E","W"] :
            angle=None

        mark=Mark(graph=self,dist=dist,angle=angle,central_point=None,\
                text=text,mark_point=mark_point,position=position,pspict=pspict)

        # In each .psttricks file we need the lines that make compute
        # the size of the text. Thus we call "get_box_size" for each.
        if not isinstance(pspict,list):
            pspict=[pspict]
        for psp in pspict:
            dimx,dimy = psp.get_box_size(text)

        return mark

    ##  \brief put a mark on an object
    #       
    #
    # If you want to put a mark on an object
    # P.put_mark(0.1,text="foobar",pspict=pspict,position="N")
    #
    #        mark_point is a function which returns the position of the mark point.
    #
    #        If you give no position (i.e. no "S","N", etc.) the position will
    #       be automatic regarding the angle.
    #
    #        - ``angle`` is given in degree.
    # set `position` to "center" is dangerous because it puts the center of
    # the box at given angle and distance. Thus the text can be ill placed, 
    # especially if the given `dist` is lower than the half of the box size.
    #
    # `center_direction` : the mark is placed in such a way that the center is
    # at given angle, and the box's border at given distance.
    def put_mark(self,dist=None,angle=None,text="",\
            mark_point=None,added_angle=None,position=None,\
            pspict=None,pspicts=None):

        from NoMathUtilities import ensure_unicode
        from Utilities import make_psp_list
        text=ensure_unicode(text)
        pspicts=make_psp_list(pspict,pspicts)

        for psp in pspicts:
            mark=self.get_mark(dist,angle,text,mark_point=mark_point,
                        added_angle=added_angle,position=position,pspict=psp)

            if position in ["N","S","E","W"] and angle is not None :
                logging( "When you want a position like N,S,E, or W,\
                        the mark angle should not be given.")
            self.added_objects.append(psp,mark)

        self.mark=mark

    def add_option(self,opt):
        self.options.add_option(opt)
    def get_option(opt):
        return self.options.DicoOptions[opt]
    def remove_option(opt):
        self.options.remove_option(opt)
    def merge_options(self,graph):
        """
        Take an other object <Foo>Graph and merges the options as explained in the documentation of the class Options. 
        That merge takes into account the attributes "color", "style", wavy
        """
        self.parameters = graph.parameters
        self.options.merge_options(graph.options)
        self.wavy = graph.wavy
        self.waviness = graph.waviness
    def conclude_params(self):
        """
        However the better way to add something like
        linewidth=1mm
        to a graph object `seg` is to use
        seg.add_option("linewidth=1mm")
        """
        oo=self.parameters.other_options
        for opt in oo.iterkeys():
            self.add_option(opt+"="+oo[opt])
        self.parameters.add_to_options(self.options)
    def params(self,language,refute=[]):
        return self.bracketAttributesText(language=language,refute=refute)
    def bracketAttributesText(self,language,refute=[]):
        from BasicGeometricObjects import genericBracketAttributeToLanguage
        self.conclude_params()

        # Create the text  a1=va,a2=v2, etc.
        # 1935811332
        l=[]
        bracket_attributes=self.parameters.bracketAttributesDictionary()
        for attr in [x for x in bracket_attributes.iterkeys() if x not in refute]:
            value=bracket_attributes[attr]
            l_attr=genericBracketAttributeToLanguage(attr,language)
            if value != None:
                if attr=="linewidth":
                    l.append(l_attr+"="+str(value)+"pt")
                else:
                    l.append(l_attr+"="+str(value))
        code=",".join(l)
        return code
    def action_on_pspict(self,pspict):
        pass
    def conclude(self,pspict):
        """
        The `conclude` function allows an object to make its ultimate
        settings before to be drawn.
        This is used for objects like axes that have a list of added objects
        (the graduation bars) that can depend on the other objects in the 
        picture.
        """
        pass
    def _draw_added_objects(self,pspict):
        # position 3598-30738
        for obj in self.added_objects[pspict] :
            pspict.DrawGraphs(obj)
        
    # We could be tempted to furnish here a default 
    # '_bounding_box(self,pspict)'
    # Indeed, some are uniquely build from 'action_on_pspict', so that the
    #bounding box is not important to know since the building block 
    # have theirs.
    def bounding_box(self,pspict=None):
        try:
            return self.already_computed_BB[pspict]
        except KeyError :
            pass
        bb=self._bounding_box(pspict)
        self.already_computed_BB[pspict]=bb
        return bb
    def math_bounding_box(self,pspict):
        try:
            return self.already_computed_math_BB[pspict]
        except KeyError :
            pass
        try:
            bb=self._math_bounding_box(pspict)
        except AttributeError:
            bb=self.bounding_box(pspict=pspict)
        bb.is_math=True
        self.already_computed_math_BB[pspict]=bb
        return bb
    def latex_code(self,pspict,language=None):
        return ""

class DrawElement(object):
    # The attributes take_xxx are intended to say what we have to take into account in the element.
    # If you put take_graph=False, this element will not be drawn, but its bounding boxes are going to be taken into account.
    def __init__(self,graphe,separator_name,take_graph=True,take_BB=True,take_math_BB=True,*args):
        self.take_graph=take_graph
        self.take_BB=take_BB
        self.take_math_BB=take_math_BB
        self.graph=graphe
        self.separator_name=separator_name
        self.st_args=args

