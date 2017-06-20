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

from FillParameters import FillParameters
from HatchParameters import HatchParameters

class Parameters(object):
    def __init__(self,graph=None):
        # These are the "bracket" attributes, that is the ones that are
        # subject to be put there :  \draw [  *here*  ]  (...)
        # See the code position 1935811332
        self.color = None   
        self.symbol = None
        self.style = None
        self.dotangle=None
        self.linewidth=None
        self.bracket_attributes=["color","symbol","style","dotangle","linewidth"]

        # Other attributes :
        self.fill=FillParameters()
        self.hatch=HatchParameters()
        self.other_options={}
        self._filled=False
        self._hatched=False
        self.visual=None        # If True, it means that one wants the object to be non deformed by xunit,yunit
        self.trivial=False   # For Interpolation curve, only draw a piecewise affine approximation.
        self.graph=graph
    def bracketAttributesDictionary(self):
        """
        Return a dictionary for the bracket attributes and their values.
        See also the position 1935811332
        """
        d={}
        for attr in self.bracket_attributes:
            value=self.__getattribute__(attr)
            d[attr]=value
        return d
    def copy(self):
        cop=Parameters()
        cop.visual=self.visual
        cop._hatched=self._hatched
        cop._filled=self._filled
        cop.hatch=self.hatch
        cop.fill=self.fill
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
        for attr in parameters.__dict__.iterkeys():
            candidate=self.__getattribute__(attr)
            if candidate is not None :
                parameters.__dict__[attr]=candidate
        parameters.fill=self.fill
        parameters.hatch=self.hatch

