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


"""
NonAnalyticParametricCurveGraph  describe a parametric curve for which we don't know an analytic form of the components. The given components functions 'f1' and 'f2' are functions in the Python sense.

NonAnalyticPointParametricCurveGraph describe a parametric curve for which we don't know an analytic form of the components. The given function 'f' is a function in the Python sense that return a Point.
"""

from ObjectGraph import ObjectGraph
from Constructors import *

class NonAnalyticParametricCurveGraph(ObjectGraph):
    def __init__(self,f1,f2,mx,Mx):
        ObjectGraph.__init__(self,self)
        self.f1=f1
        self.f2=f2
        self.mx=mx
        self.Mx=Mx
        self.I=self.get_point(mx)
        self.F=self.get_point(Mx)

        self.parameters.plotpoints=100

        from numpy import linspace
        if self.mx is not None and self.Mx is not None:
            self.drawpoints=linspace(self.mx,self.Mx,self.parameters.plotpoints,endpoint=True)
    def curve(self):
        interpolation = InterpolationCurve([self.get_point(x) for x in self.drawpoints])
        self.parameters.add_to(interpolation.parameters,force=True)     # This curve is essentially dedicated to the colors
        return interpolation
    def get_point(self,x,advised=False):
        return Point(self.f1(x),self.f2(x))
    def reverse(self):
        """
        Return the curve [mx,Mx] -> R^2 that makes
        the inverse path.
        """
        f1=lambda x:self.f1(self.mx+self.Mx-x)
        f2=lambda x:self.f2(self.mx+self.Mx-x)
        return NonAnalyticParametricCurve(f1,f2,self.mx,self.Mx)
    def _math_bounding_box(self,pspict=None):
        return self.curve().math_bounding_box(pspict)
    def _bounding_box(self,pspict=None):
        return self.curve().bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        return self.curve().latex_code(language=language,pspict=pspict)
    def __call__(self,x):
        return self.get_point(x)

class NonAnalyticPointParametricCurveGraph(ObjectGraph):
    def __init__(self,f,mx,Mx):
        ObjectGraph.__init__(self,self)
        self.f=f
        self.mx=mx
        self.Mx=Mx
        self.I=self.get_point(mx)
        self.F=self.get_point(Mx)

        self.parameters.plotpoints=100

        from numpy import linspace
        if self.mx is not None and self.Mx is not None:
            self.drawpoints=linspace(numerical_approx(self.mx),numerical_approx(self.Mx),self.parameters.plotpoints,endpoint=True)
        self._curve=None
        self.mode=None
    def curve(self):
        if not self._curve :
            interpolation = InterpolationCurve([self.get_point(x) for x in self.drawpoints])
            interpolation.parameters=self.parameters.copy()
            interpolation.mode=self.mode
            self._curve=interpolation
        return self._curve
    def get_point(self,x,advised=False):
        return self.f(x)
    def reverse(self):
        """
        Return the curve [mx,Mx] -> R^2 that makes
        the inverse path.
        """
        f1=lambda x:self.f(self.mx+self.Mx-x)
        return NonAnalyticPointParametricCurve(f1,self.mx,self.Mx)
    def _math_bounding_box(self,pspict=None):
        return self.curve().math_bounding_box(pspict)
    def _bounding_box(self,pspict=None):
        return self.curve().bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        return self.curve().latex_code(language=language,pspict=pspict)
    def __call__(self,x):
        return self.get_point(x)

class NonAnalyticFunctionGraph(ObjectGraph):
    """
    Represent a function for which one has no analytic form.

    As long as one can evaluate it at points, one can draw an interpolation curve.
    """
    def __init__(self,fun,mx=None,Mx=None):
        ObjectGraph.__init__(self,fun)
        self.mx=mx
        self.Mx=Mx
        self.fun=fun
        self.parameters.plotpoints=100
        self.old_mx=None    # Will be used in order to simulate a lazy_attribute in self.get_minmax_data
        self.old_Mx=None
        self.minmax_result=None
        from numpy import linspace
        if self.mx is not None and self.Mx is not None:
            self.drawpoints=linspace(self.mx,self.Mx,self.parameters.plotpoints,endpoint=True)
        self.parameters.color="blue"
    def parametric_curve(self,mx=None,Mx=None):
        if mx == None:
            mx=self.mx
        if Mx == None:
            Mx=self.Mx
        x=var('x')
        return NonAnalyticParametricCurve(x,self,mx,Mx)
    def reverse(self):
        new = lambda x: self.fun(self.Mx+self.mx-x)
        return NonAnalyticFunction(new,self.mx,self.Mx)
    def curve(self,drawpoints):
        """
        Return the interpolation curve corresponding to self.

        Since it could be cpu-consuming, this is a lazy_attribute. For that reason it should not be called by the end-user but only during the computation of the bounding box and the tikz code.
        """
        points_list=[self.get_point(x) for x in self.drawpoints]
        return InterpolationCurve(points_list,context_object=self)
    def get_point(self,x):
        return general_function_get_point(self,x,advised=False)
    def graph(self,mx,Mx):
        return NonAnalyticFunction(self.fun,mx,Mx)
    def _math_bounding_box(self,pspict=None):
        xmin=self.get_minmax_data(self.mx,self.Mx)["xmin"]
        xmax=self.get_minmax_data(self.mx,self.Mx)["xmax"]
        ymin=self.get_minmax_data(self.mx,self.Mx)["ymin"]
        ymax=self.get_minmax_data(self.mx,self.Mx)["ymax"]
        return BoundingBox(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    def _bounding_box(self,pspict=None):
        return self.math_bounding_box(pspict)
    def latex_code(self,language=None,pspict=None):
        return self.curve(self.drawpoints).latex_code(language=language,pspict=pspict)
    def __call__(self,x):
        return self.fun(x)
