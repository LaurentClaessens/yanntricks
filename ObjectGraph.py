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

class Options(object):
    """
    Describe the drawing options of an objects.

    ATTRIBUTES :
        self.DicoOptions : dictionnary which contains the options
    METHODS :
        self.merge_options(opt) : opt is an other object of the class Options. The method merges the two in the sense that opt is not
                        changed, but 
                        1. if opt contains a key more, it is added to self
                        2. if a key of opt is different of the one of self, self is changed
    """
    def __init__(self):
        self.DicoOptions = {}
    # One adds an option using for example
    # LineColor=blue,LineStyle=dashed
    # or via a dictionary :
    # {"Dx":1,"Dy":3}
    def add_option(self,opt):
        if opt :            # If the argument is empty.
            try:
                for op in opt.split(","):
                    s = op.split("=")
                    self.DicoOptions[s[0]] = s[1]
            except AttributeError :
                for op in opt.keys():
                    self.DicoOptions[op] = opt[op]

    def remove_option(self,opt):
        del(self.DicoOptions[opt])
    def merge_options(self,opt):
        for op in opt.DicoOptions.keys():
            self.add_option({op:opt[op]})
    def extend_options(self,Opt):
        for opt in Opt.DicoOptions.keys():
            self.add_option(opt+"="+Opt.DicoOptions[opt])
    # Afiter est une liste de noms d'options, et cette méthode retourne une instance de Options qui a juste ces options-là, avec les valeurs de self.
    def sousOptions(self,AFiter):
        O = Options()
        for op in self.DicoOptions.keys() :
            if op in AFiter : O.add_option(op+"="+self.DicoOptions[op])
        return O
    def style_ligne(self):
        return self.sousOptions(OptionsStyleLigne())
    def code(self,language=None):
        a = []
        if language=="pstricks":
            raise DeprecationWarning,"No more pstricks supported"
            for op in self.DicoOptions.keys():
                a.append(op+"="+self.DicoOptions[op])
                a.append(",")
            del a[-1:]
            return "".join(a)
        if language=="tikz":
            a=[]
            for at in ["linecolor","linestyle"]:
                k=self.DicoOptions[at]
                if k and k!="none" :
                    a.append(k)
            return ",".join(a)
    def __getitem__(self,opt):
        return self.DicoOptions[opt]

class ObjectGraph(object):
    """ This class is supposed to be used to create other "<Foo>Graph" by inheritance. It is a superclass. """
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
    def wave(self,dx,dy):     # dx is the wave length and dy is the amplitude
        from Parameters import Waviness
        self.wavy = True
        self.waviness = Waviness(self,dx,dy)
    def get_mark(self,dist,angle,text,mark_point=None,automatic_place=False,added_angle=None,pspict=None):

        """
        If you want to put a mark on an object
        P.put_mark(0.1,-90,"text",automatic_place=(pspict,"N"))

        mark_point is a function which returns the position of the mark point.

        If you give no position (i.e. no "S","N", etc.) the position will be automatic regarding the angle.
        """
        from AngleGraph import AngleGraph
        from Constructors import Mark
        from MathStructures import AngleMeasure
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
            if isinstance(self,AngleGraph):
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

        # We need to immediately add the LaTeX lines about box sizes, no waiting fig.conclude. This is to allow several pictures to use the same points and marks.  
        # By the way, one cannot compute the self.mark.central_point() here because the axes are not yet computed.

        if not isinstance(pspict,list):
            pspict=[pspict]
        if automatic_place :
            for psp in pspict:
                dimx,dimy = psp.get_box_size(text)
        return mark
    def put_mark(self,dist,angle,text,mark_point=None,automatic_place=False,added_angle=None,pspict=None):

        """
        - ``angle`` is given in degree.
        """
        mark=self.get_mark(dist,angle,text,mark_point=mark_point,automatic_place=automatic_place,added_angle=added_angle,pspict=pspict)
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
        Take an other object <Foo>Graph and merges the options as explained in the documentation of the class Options. That merge takes into account the attributes "color", "style", wavy
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
