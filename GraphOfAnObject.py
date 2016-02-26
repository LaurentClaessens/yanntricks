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

from Parameters import Parameters

class GraphOfAnObject(object):
    """ This class is supposed to be used to create other "GraphOfA..." by inheritance. It is a superclass. """
    # self.record_add_to_bb is a list of points to be added to the bounding box.
    # Typically, when a point has a mark, one can only know the size of the box at the end of the picture 
    #(because of xunit, yunit that change when using dilatation)
    # Thus if one wants to draw the bounding box, it has to be done at the end.
    def __init__(self,obj):
        self.obj = obj
        self.parameters = Parameters()
        self.wavy = False
        self.waviness = None
        self.options = Options()
        self.marque = False
        self.draw_bounding_box=False
        self.add_option("linecolor=black")
        self.add_option("linestyle=solid")
        self.record_add_to_bb=[]         
        self.separator_name="DEFAULT"
        self.in_math_bounding_box=True
        self.in_bounding_box=True
        self._draw_edges=False
        self.added_objects=[]
    def draw_edges(self):
        self._draw_edges=True
    def wave(self,dx,dy):                   # dx is the wave length and dy is the amplitude
        self.wavy = True
        self.waviness = Waviness(self,dx,dy)
    def get_mark(self,dist,angle,text,mark_point=None,automatic_place=False,added_angle=None,pspict=None):

        """
        If you want to put a mark on an object
        P.put_mark(0.1,-90,"text",automatic_place=(pspict,"N"))

        mark_point is a function which returns the position of the mark point.

        If you give no position (i.e. no "S","N", etc.) the position will be automatic regarding the angle.
        """
        if automatic_place==False:
            if pspict:
                automatic_place=(pspict,"")
            else :
                raise "You have to pass a pspicture"
        if self.marque:
            print("This is a second (or more) mark on the same point")
        self.marque = True
        autom=automatic_place
        third=None
        if not isinstance(autom,tuple):
            print("You should not use 'automatic_place' like that")
            pspict=autom
            position=""
        else :
            pspict=automatic_place[0]
            position=automatic_place[1]
            if position=="for axes":
                third=automatic_place[2]

        if angle is None :
            try :
                angle=self.advised_mark_angle(pspict=pspict)
            except AttributeError :
                angle=self.angle().degree+90

        if added_angle:
            angle=angle+added_angle
        if position=="" :
            position="corner"
            if isinstance(self,GraphOfAnAngle):
                position="center"
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
        mark=Mark(self,dist,angle,text,automatic_place=(pspict,position,third),mark_point=mark_point)

        # We need to immediately add the LaTeX lines about box sizes, no waiting fig.conclude. This is to allow several pictures
        # to use the same points and marks.
        # By the way, one cannot compute the self.mark.central_point() here because the axes are not yet computed.

        if not isinstance(pspict,list):
            pspict=[pspict]
        if automatic_place :
            for psp in pspict:
                dimx,dimy = psp.get_box_size(text)
        return mark

        # No more like that   (September, 21, 2014)
        #self.mark._central_point=self.mark.central_point()
        #if not self.mark._central_point :
        #    print(self)
        #    raise
    def put_mark(self,dist,angle,text,mark_point=None,automatic_place=False,added_angle=None,pspict=None):
        mark=self.get_mark(dist,angle,text,mark_point=None,automatic_place=automatic_place,added_angle=added_angle,pspict=pspict)
        self.added_objects.append(mark)
        self.mark=mark
    def add_option(self,opt):
        self.options.add_option(opt)
    def get_option(opt):
        return self.options.DicoOptions[opt]
    def remove_option(opt):
        self.options.remove_option(opt)
    def merge_options(self,graph):
        """
        takes an other object GraphOfA... and merges the options as explained in the documentation
        of the class Options. That merge takes into account the attributes "color", "style", wavy
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
        for opt in oo.keys():
            self.add_option(opt+"="+oo[opt])
        self.parameters.add_to_options(self.options)
    def params(self,language,refute=[]):
        self.conclude_params()
        l=[]
        for attr in [x for x in self.parameters.interesting_attributes if x not in refute]:
            value=self.parameters.__getattribute__(attr)
            if value != None:
                if attr=="linewidth":
                    l.append("linewidth="+str(value)+"pt")
                else:
                    l.append(attr+"="+str(value))
        code=",".join(l)
        if language=="tikz":
            code=code.replace("plotpoints","samples")
            code=code.replace("linewidth","line width")
        return code
        #return self.options.code(language=language)
    def action_on_pspict(self,pspict):
        for obj in self.added_objects :
            pspict.DrawGraphs(obj)
        # One cannot make try ... except AttributeError since it should silently pass a real AttributeError in the implementation if specific_action_on_pspict
        if "specific_action_on_pspict" in dir(self):
            self.specific_action_on_pspict(pspict)
    def math_bounding_box(self,pspict):
        return self.bounding_box(pspict)
    def latex_code(self,pspict,language=None):
        return ""
