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

from ObjectGraph import ObjectGraph
from Constructors import *

class HistogramBox(ObjectGraph):
    """
    describes a box in an histogram.
    """
    def __init__(self,a,b,n,histo):
        """
        It is given by the initial value, the final value and the "surrounding" histogram
        """
        ObjectGraph.__init__(self,self)
        self.d_xmin=a
        self.d_xmax=b
        self.n=n
        self.histo=histo
        self.size=self.d_xmax-self.d_xmin
        self.th_height=self.n/self.size
        self.length=None
        self.height=None
    @lazy_attribute
    def rectangle(self):
        xmin=self.histo.xscale*self.d_xmin
        xmax=self.histo.xscale*self.d_xmax
        ymin=0
        ymax=self.histo.yscale*self.th_height
        rect=Rectangle(mx=xmin,Mx=xmax,my=ymin,My=ymax)
        rect.parameters=self.parameters.copy()
        return rect
    def bounding_box(self,pspict=None):
        return self.rectangle.bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        # The put_mark can only be done here (and not in self.rectangle()) because one needs the pspict.
        return self.rectangle.latex_code(language=language,pspict=pspict)


class HistogramGraph(ObjectGraph):
    def __init__(self,tuple_box_list):
        ObjectGraph.__init__(self,self)
        self.tuple_box_list=tuple_box_list
        self.box_list=[]
        for t in self.tuple_box_list:
            self.box_list.append(HistogramBox(t[0],t[1],t[2],self))
        self.n=sum( [b.n for b in self.box_list] )
        self.length=12  # Visual length (in centimeter) of the histogram
        self.height=6  # Visual height (in centimeter) of the histogram
        self.d_xmin=min([b.d_xmin for b in self.box_list])       # min and max of the data
        self.d_xmax=max([b.d_xmax for b in self.box_list])
        self.d_ymax=max([b.n for b in self.box_list])       # max of the data ordinate.
        self.xsize=self.d_xmax-self.d_xmin
        self.ysize=self.d_ymax              # d_ymin is zero (implicitly)
        self.legende=None
        # TODO : For sure one can sort it easier.
        # The problem is that if several differences x.th_height-y.th_height are small, 
        # int(...) always returns 1 (or -1), so that the sorting gets wrong.
        self.xscale=self.length/self.xsize
        classement = self.box_list[:]
        facteur=10
        for x in classement :
            for y in classement :
                try :
                    facteur=max(facteur,10/(x.th_height-y.th_height))
                except ZeroDivisionError :
                    pass
        classement.sort(lambda x,y:int((x.th_height-y.th_height)*facteur))
        self.yscale=self.height/classement[-1].th_height
        self.height/self.ysize
    def IF_x(self):
        """
        return the list of I and F points without repetitions.

        This is the list of "physical values" (i.e. the ones of the histogram), not the ones
        of the pspict coordinates.
        """
        x_list=[]
        for b in self.box_list:
            if b.d_xmin not in x_list :
                x_list.append(b.d_xmin)
            if b.d_xmax not in x_list :
                x_list.append(b.d_xmax)
        return x_list
    def specific_action_on_pspict(self,pspict):
        raise
        pspict.axes.no_graduation()
        pspict.axes.do_mx_enlarge=False
        pspict.axes.do_my_enlarge=False
        if self.legende :
            pspict.axes.single_axeX.put_mark(0.5,-90,self.legende,pspict=pspict,position="N")
        else :
            print "Are you sure that you don't want a legend on your histogram ?"
        # The construction of the list 'values' is created in such a way not to have '1.0' instead of '1'.
        # By the way, you have to know that the values in numpy.arange are type numpy.float64
        import numpy
        un=numpy.arange(self.d_xmin,self.d_xmax+0.1,step=int(self.xsize/10))
        values=[]
        for xx in un :
            if int(xx)==xx:
                values.append(int(xx))
            else :
                values.append(xx)
        for xx in values:
            P=Point(xx*self.xscale,0)
            P.parameters.symbol="|"
            P.put_mark(0.2,-90,str(xx),pspict=pspict,position="N")    # see 71011299 before to change this 0.2
            pspict.DrawGraphs(P)
        for box in self.box_list :
            P=box.rectangle.segment_N.mark_point()
            P.put_mark(0.2,90,"$"+str(box.n)+"$",pspict=pspict,position="S")
            P.parameters.symbol=""
            pspict.DrawGraphs(P)
    def bounding_box(self,pspict):
        bb=BoundingBox()
        for b in self.box_list:
            bb.append(b,pspict)
        return bb
    def math_bounding_box(self,pspict=None):
        return self.bounding_box(pspict=pspict)
    def latex_code(self,language=None,pspict=None):
        a=["% Histogram"]
        a.extend([x.latex_code(language=language,pspict=pspict) for x in self.box_list])
        return "\n".join(a)
