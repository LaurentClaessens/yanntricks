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

import Defaults

class Plotpoints(object):
    def __init__(self,graph):
        self.graph=graph
        self.linear=Default.LINEAR_PLOTPOINTS
        self.curvature=Default.CURVATURE_PLOTPOINTS
        self.added_plotpoints=[]
    def addPoint(self,x):
        self.added_plotpoints.append(x)

    def representative_points(self):
        initial = numerical_approx(self.graph.llamI)      # Avoid the string "pi" in the latex code.
        final = numerical_approx(self.llamF)
        plotpoints=self.parameters.plotpoints
        if plotpoints==None :
            plotpoints=50
        if self.parameters.force_smoothing :
            print("force smoothing ...")
            Llam=self.getRegularCurvatureParameter(initial,final,self.total_curvature()/plotpoints,initial_point=True,final_point=False)
            print("force smoothing ... done")
        else :
            import numpy
            # If not RR, the elements of Llam are type numpy.float64. In this case, computing the sqrt of negative return NaN instead of complex.
            # Then we cannot remove the probably fake imaginary part. It happens for the function sqrt(cos(x)) with x=3*pi/2. 
            Llam=[ RR(s) for s in  numpy.linspace(initial,final,plotpoints)]
        pts = [ self.get_point(x,advised=False) for x in Llam ]

        pl=[]
        for P in pts:
            isreal,Q=test_imaginary_part_point(P)
            if not isreal:
                print("There is a not so small imaginary part ... prepare to crash or something")
            pl.append(Q)
        print("Number of representative points : ",len(pl))
        return pl


