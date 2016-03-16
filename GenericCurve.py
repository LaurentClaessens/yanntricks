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

from __future__ import division

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
        self._representativeParameters=None
    def addPoint(self,x):
        self.added_plotpoints.append(x)
    def getFunctionIntegral( self,fun,  lmin=None,lmax=None ):
        """
        Return the integral of 'fun' from 'lmin' to 'lmax'.
        """
        if lmin==None:
            lmin=self.pI
        if lmax==None:
            lmax=self.pF
        return numerical_integral(fun,lmin,lmax)[0]
    def total_curvature(self):
        return self.getFunctionIntegral(self.curvature)
    def getNextRegularFunctionParameters( self, lmin,lmax,fun,df,xunit=1,yunit=1 ):
        """
        Return a value 'nl' of the parameter such that the integral of 'fun' from 'lmin' to 'nl' is 'df'.

        `lmax` - is the maximal value of the parameter. If the interval [lmin,lmax]  reveals to be too small, return 'None'

        """
        # Vcurve is the curve as visually seen taking the dilatation into account.
        x=var('x')
        Vf1=phyFunction(self.f1(xunit*x))
        Vf2=phyFunction(self.f2(yunit*x))
        Vcurve=ParametricCurve(Vf1,Vf2)

        prop_precision = float(df)/100      # precision of the interval
        if prop_precision == 0:
            raise ValueError,"prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. dl=%s"%str(dl)

        # We'll perform a dichotomy method.
        # 'too_large' is a value of the parameter we know to be too large
        # 'too_small' is a value of the parameter we know to be too small
        # 'ell' is the median value on which the condition is tested. 
        # The dichotomy method consist to make 'too_large' or 'too_small' become 'ell' and to recalculate a new 'ell'

        too_small=lmin
        too_large=lmax
        if Vcurve.getFunctionIntegral(fun,too_small,too_large) < df:
            return None

        max_iter=100
        done_iter=0
        while done_iter<max_iter :
            ell=(too_large+too_small)/2
            done_iter+=1
            integral=Vcurve.getFunctionIntegral(fun,lmin,ell)
            if abs(integral-df)<prop_precision :
                return ell
            if integral>df:
                too_large=ell
            if integral<df:
                too_small=ell
        raise ShouldNotHappenException("I give up with this dichotomy")

    def getRegularFunctionParameters( self, lmin,lmax,fun,df,initial_point=False,final_point=False,xunit=1,yunit=1 ):
        """
        `fun` - is a function on the curve, expressed by the parameter.

        We return a list of points  x_i on the curve such that the integral of 'fun' from x_i to x_{i+1} is df.

        This is a visual function in the sense that the curve is first transformed in order to take the dilatation into account.

        EXAMPLE :

        Taking as 'fun' the norm of the tangent vector, one consider the arc length
        """
        prop_precision = float(df)/100      # precision of the interval
        if prop_precision == 0:
            raise ValueError,"prop_precision is zero. Something sucks. You probably want to launch me in an infinite loop. dl=%s"%str(dl)

        # Vcurve is the curve as visually seen taking the dilatation into account.
        Vcurve=self.visualParametricCurve(xunit,yunit)

        PIs = []            # The list of selected values of the parameter
        if initial_point:
            PIs.append(lmin)
        if final_point:
            PIs.append(lmax)
        ll=lmin
        while ll is not None :
            ll=Vcurve.getNextRegularFunctionParameters(ll,lmax,fun,df,xunit=1,yunit=1)
            if ll is not None:
                PIs.append(ll)
        return PIs
    def getRegularLengthParameters(self,mll,Mll,dl,initial_point=False,final_point=False,xunit=1,yunit=1):
        """ 
        return a list of values of the parameter such that the corresponding points are equally spaced by dl.
        Here, we compute the distance using the method arc_length.

        INPUT:

        - ``mll,Mll`` - the initial and final values of the parameters.

        - ``dl`` - the arc length distance between the points corresponding
                    to the returned values.

        - ``initial_point`` - (default=False) it True, return also the initial parameters (i.e. mll).

        - ``final_point`` - (default=False) it True, return also the final parameter (i.e. Mll)

        """
        return self.getRegularFunctionParameters(mll,Mll,self.speed,dl,initial_point=initial_point,final_point=final_point,xunit=xunit,yunit=yunit)
    def getRegularCurvatureParameter(self,mll,Mll,dl,initial_point=False,final_point=False,xunit=1,yunit=1):
        """ 
        Same thing as `getRegularLengthParameters`, but with the curvature instead of the arc length.
        """
        return self.getRegularFunctionParameters(mll,Mll,self.curvature,dl,initial_point=initial_point,final_point=final_point,xunit=xunit,yunit=yunit)
    def representativeParameters(self):
        if self._representativeParameters :
            return self._representativeParameters

        initial = numerical_approx(self.pI) 
        final = numerical_approx(self.pF)
        curvature_Llam=[]
        linear_Llam=[]
        if self.curvature_plotpoints :
            print("Taking "+str(self.curvature_plotpoints)+" curvature points (can take a long time) ...")
            curvature_Llam=self.getRegularCurvatureParameter(initial,final,self.total_curvature()/self.curvature_plotpoints,initial_point=True,final_point=True)
            print("... done")
        if self.linear_plotpoints:
            import numpy
            # If not RR, the elements of Llam are type numpy.float64. In this case, computing the sqrt of negative return NaN instead of complex. Then we cannot remove the probably fake imaginary part. It happens for the function sqrt(cos(x)) with x=3*pi/2. 



            # We can remove this try-except (but not the line in the try).
            # March 15, 2016
            try :
                linear_Llam=[ RR(s) for s in  numpy.linspace(initial,final,self.linear_plotpoints)]
            except TypeError:
                print("ooNZKKooUpyYBn -- woops")
                print("initial : ",initial)
                print("finale : ",final)
                print("linear_plotpoints : ",self.linear_plotpoints)
                print("self : ",str(self),type(self))
                for s in numpy.linspace(initial,final,self.linear_plotpoints):
                    print(s,type(s))
                    print(RR(s))
                raise



            Llam=[]
            Llam.extend(self.added_plotpoints)
            Llam.extend(linear_Llam)
            Llam.extend(curvature_Llam)
            Llam.sort()
            self._representativeParameters = Llam
            return Llam
    def representativePoints(self):
        rp=self.representativeParameters()
        pts = [ self.get_point(x,advised=False) for x in rp ]

        pl=[]
        for P in pts:
            isreal,Q=test_imaginary_part_point(P)
            if not isreal:
                print("There is a not so small imaginary part ... Prepare to crash or something")
            pl.append(Q)
        return pl


