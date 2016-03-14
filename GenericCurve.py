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

from sage.all import *
from Utilities import *
import Defaults

class GenericCurve(object):
    def __init__(self,pI,pF):
        """
        `pI` and `pF` are initial and final value of the parameters. 
        This is to abstract the notational problem between (mx,Mx) in the phyFunction
        and (llamI,llamF) in ParametricCurve.
        """
        self.linear_plotpoints=Defaults.LINEAR_PLOTPOINTS
        self.curvature_plotpoints=Defaults.CURVATURE_PLOTPOINTS
        self.added_plotpoints=[]
        self.pI=pI
        self.pF=pF
    def addPoint(self,x):
        self.added_plotpoints.append(x)
    def representativeParameters(self):
        initial = numerical_approx(self.pI) 
        final = numerical_approx(self.pF)
        if self.curvature_plotpoints :
            print("force smoothing ...")
            Llam=self.getRegularCurvatureParameter(initial,final,self.total_curvature()/self.curvature_plotpoints,initial_point=True,final_point=True)
            print("force smoothing ... done")
        if self.linear_plotpoints:
            import numpy
            # If not RR, the elements of Llam are type numpy.float64. In this case, computing the sqrt of negative return NaN instead of complex.
            # Then we cannot remove the probably fake imaginary part. It happens for the function sqrt(cos(x)) with x=3*pi/2. 
            Llam=[ RR(s) for s in  numpy.linspace(initial,final,self.linear_plotpoints)]
            Llam.sort()
            return Llam
    def representativePoints(self):
        rp=self.representativeParameters()
        pts = [ self.get_point(x,advised=False) for x in rp ]

        pl=[]
        for P in pts:
            isreal,Q=test_imaginary_part_point(P)
            if not isreal:
                print("There is a not so small imaginary part ... prepare to crash or something")
            pl.append(Q)
        print("Number of representative points : ",len(pl))
        return pl


