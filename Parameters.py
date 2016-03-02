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

class FillParameters(object):
    """
    Represent the parameters of filling a surface.
    """
    def __init__(self):
        self.color = "lightgray"
        self.style = "solid"
    def add_to_options(self,opt):
        """
        add `self` to a set of options.

    
        INPUT:

        - ``opt`` - an instance of :class:`Options`.

        OUTPUT:

        Return `opt` with added properties.

        """
        if self.color :
            opt.add_option("fillcolor=%s"%str(self.color))
        if self.style :
            opt.add_option("fillstyle=%s"%str(self.style))

class HatchParameters(object):
    """Same as FillParameters, but when one speaks about hatching"""
    def __init__(self):
        self.color = None
        self._crossed = False
        self.angle = -45
    def crossed(self):
        self._crossed=True
    def add_to_options(self,opt):
        opt.add_option("hatchangle=%s"%str(self.angle))
        if self._crossed:
            opt.add_option("fillstyle=crosshatch")
        else:
            opt.add_option("fillstyle=vlines")
        if self.color :
            opt.add_option("hatchcolor=%s"%str(self.color))

class Parameters(object):
    def __init__(self):
        self.color = None           # I take into account in SurfaceBetweenParametricCurves that the default values are None
        self.symbol = None
        self.style = None
        self.plotpoints=None
        self.dotangle=None
        self.fill=FillParameters()
        self.hatch=HatchParameters()
        self.other_options={}
        self._filled=False
        self._hatched=False
        self.visual=None        # If True, it means that one wants the object to be non deformed by xunit,yunit
        self.interesting_attributes=["color","symbol","style","plotpoints","dotangle","linewidth"]
        self.force_smoothing=None
        self.trivial=False   # For Interpolation curve, only draw a piecewise affine approximation.
        self.linewidth=None
    def copy(self):
        cop=Parameters()
        cop.visual=self.visual
        cop._hatched=self._hatched
        cop._filled=self._filled
        cop.hatch=self.hatch
        cop.fill=self.fill
        cop.plotpoints=self.plotpoints
        cop.style=self.style
        cop.symbol=self.symbol
        cop.color=self.color
        cop.dotangle=self.dotangle
        cop.linewidth=self.linewidth
        return cop
    def filled(self):
        self._filled=True
    def hatched(self):
        self._hatched=True
    def add_option(self,key,value):
        # TODO : This method should be used as the other "add_option" methods in other classes.
        """
        Add options that will be added to to code.

            sage: from phystricks.BasicGeometricObjects import *
            sage: seg=Segment(Point(0,0),Point(1,1))
            sage: seg.parameters.add_option("linewidth","1mm")

        However the better way to add something like
        linewidth=1mm
        to a graph object `seg` is to use
        seg.add_option("linewidth=1mm")
        """
        self.other_options[key]=value
    def add_to_options(self,opt):
        """
        Add to the object `opt` (type Option) the different options that correspond to the parameters.

        In an imaged way, this method adds `self` to the object `opt`.
        """
        if self.color :
            opt.add_option("linecolor=%s"%str(self.color))
        if self.style :
            opt.add_option("linestyle=%s"%str(self.style))
        if self.symbol :
            opt.add_option("PointSymbol=%s"%str(self.symbol))
        if self._filled:
            self.fill.add_to_options(opt)
        if self._hatched:
            self.hatch.add_to_options(opt)
    def add_to(self,parameters,force=False):
        """
        Add `self` to `parameters`.

        Where `self` has non-trivial or non-default values, put these values to `parameters`

        By default, it only fills the "empty" slots (None and False). 
        If `force` is True, it fills all.
        """
        for attr in parameters.interesting_attributes:
            if (parameters.__getattribute__(attr) in [None,False]) or force :
                parameters.__dict__[attr]=self.__getattribute__(attr)
        parameters.fill=self.fill
        parameters.hatch=self.hatch
    def replace_to(self,parameters):
        """
        The same as :func:`add_to`, but replace also non-trivial parameters

        EXAMPLES::

            sage: from phystricks.BasicGeometricObjects import *
            sage: p1=Parameters()
            sage: p1.color="red"
            sage: p1.symbol="A"

            sage: p2=Parameters()
            sage: p2.style="solid"
            sage: p2.symbol="B"
            sage: p2.filled()
            sage: p2.fill.color="cyan"

            sage: p2.replace_to(p1)
            sage: print p1.color,p1.style,p1.symbol,p1._filled,p1.fill.color
            red solid B True cyan

        Notice that here `p1.style` is replace while it was not replaced by the function 
        :func:`add_to`.
        """
        for attr in parameters.__dict__.keys():
            candidate=self.__getattribute__(attr)
            if candidate is not None :
                parameters.__dict__[attr]=candidate
        parameters.fill=self.fill
        parameters.hatch=self.hatch

class Waviness(object):
    """
    This class contains the informations about the waviness of a curve. It takes as argument a phyFunctionGraph and the parameters dx, dy of the wave.
    
    - Waviness.get_wavy_points      
            returns a list of points which are disposed around the graph of the curve. These are the points to be joined by a bezier or something in order to get the wavy graph of the function.
    """
    def __init__(self,graph,dx,dy):
        self.graph = graph
        self.dx = dx
        self.dy = dy
        self.obj = self.graph.obj
        try:
            self.Mx = self.graph.Mx
            self.mx = self.graph.mx
        except AttributeError :
            pass
    def get_wavy_points(self):
        if type(self.obj) == phyFunction :
            return self.obj.get_wavy_points(self.mx,self.Mx,self.dx,self.dy)
        if type(self.obj) == Segment :
            return self.obj.get_wavy_points(self.dx,self.dy)
