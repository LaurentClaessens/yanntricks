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
from Utilities import *

class InterpolationCurveGraph(ObjectGraph):
    def __init__(self,points_list,context_object=None,mode=None):
        ObjectGraph.__init__(self,self)
        self.parameters.color="brown"

        self.points_list=points_list

        self.I=self.points_list[0]
        self.F=self.points_list[-1]
        self.context_object=context_object
        if self.context_object is None:
            self.contex_object=self
        self.mode=mode
    def representativePoints(self):
        return self.points_list
    def get_minmax_data(self):
        """
        Return a dictionary whose keys give the xmin, xmax, ymin, and ymax
        data for this graphic.

        EXAMPLES::

        sage: from phystricks import *
        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).get_minmax_data()
        {'xmax': 1.0, 'xmin': -1.0, 'ymax': 1.0, 'ymin': -1.0}

        """
        xmin=min([P.x for P in self.points_list])
        xmax=max([P.x for P in self.points_list])
        ymin=min([P.y for P in self.points_list])
        ymax=max([P.y for P in self.points_list])
        if dict:
            from SmallComputations import MyMinMax
            return MyMinMax({'xmin':xmin, 'xmax':xmax,'ymin':ymin, 'ymax':ymax})
        else:
            return xmin,xmax,ymin,ymax
    def xmin(self):
        return self.get_minmax_data()['xmin']
    def xmax(self):
        return self.get_minmax_data()['xmax']
    def ymin(self):
        return self.get_minmax_data()['ymin']
    def ymax(self):
        return self.get_minmax_data()['ymax']
    def mark_point(self,pspict=None):
        return self.points_list[-1]
    def bounding_box(self,pspict=None):
        """
        Return the bounding box of the interpolation curve

        EXAMPLES::

        sage: from phystricks import *
        sage: print InterpolationCurve([Point(0,0),Point(1,1)]).bounding_box()
        <BoundingBox xmin=0.0,xmax=1.0; ymin=0.0,ymax=1.0>

        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: print InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).bounding_box()
        <BoundingBox xmin=-1.0,xmax=1.0; ymin=-1.0,ymax=1.0>

        NOTE::

        Since the bounding box is computed from the give points while the curve is an interpolation,
        this bounding box is incorrect to the extend that \pscurve does not remains in the convex hull
        of the given points.

        EXAMPLE:
        sage: F=InterpolationCurve([Point(-1,1),Point(1,1),Point(1,-1),Point(-1,-1)])
        sage: print F.bounding_box()
        <BoundingBox xmin=-1.0,xmax=1.0; ymin=-1.0,ymax=1.0>

        """
        bb = BoundingBox( Point(self.xmin(),self.ymin()),Point(self.xmax(),self.ymax())  )
        return bb
    def math_bounding_box(self,pspict=None):
        """
        return the bounding box corresponding to the curve without decorations.

        See InterpolationCurve.bounding_box()
        """
        return self.bounding_box(pspict)
    def pstricks_code(self,pspict=None):
        raise DeprecationWarning
        """
        return the pstricks code of the interpolation curve trough the given points

        EXAMPLES::

        sage: from phystricks import *
        sage: C=Circle(Point(0,0),1)
        sage: F=InterpolationCurve([Point(0,0),Point(1,1)])
        sage: print F.pstricks_code()
        \pscurve[linestyle=solid,linecolor=brown](0,0)(1.00000000000000,1.00000000000000)
        sage: H=InterpolationCurve([Point(-1,1),Point(1,1),Point(1,-1),Point(-1,-1)])
        sage: print H.pstricks_code()
        \pscurve[linestyle=solid,linecolor=brown](-1.00000000000000,1.00000000000000)(1.00000000000000,1.00000000000000)(1.00000000000000,-1.00000000000000)(-1.00000000000000,-1.00000000000000)
        """

        # Explanation of 295815047.
        # It seems to me that very large lines like the ones describing a curve cause   ! TeX capacity exceeded, sorry [pool size=6179214].

        l = []
        try:
            params=self.context_object.params(language="pstricks")
        except AttributeError :
            params=self.params()
        l.append("\pscurve["+params+"]")
        for p in self.points_list:
            l.append(p.coordinates(numerical=True,pspict=pspict))
        return "".join(l)
    def tikz_code(self,pspict=None):
        pl=self.points_list
        if self.mode=="trivial":
            # One cannot draw each segment separately : this causes the parameters.style='dashed' to not work for example.
            import numpy
            a=[]
            sublen=max(len(pl)/500,1)   # We draw packs of 100 points
            list_of_list=numpy.array_split(pl,sublen)
            for spl in list_of_list :
                # digits is computed in such a way to have a precision of 0.001 (3 digits after the dot)
                l=[abs(P.x) for P in spl]
                l.extend(  [abs(P.y) for P in spl]  )
                namax=max(l)
                digits=3+ceil(  log(namax,10) )
                params=self.params(language="tikz")
                a.append("\draw [{0}] {1};".format(params,"--".join(   [x.coordinates(numerical=True,digits=digits,pspict=pspict) for x in spl]  ) ))
            return "\n".join(a)
        elif self.mode=="quadratic":
            pieces=[]
            par=LagrangePolynomial(  pl[0],pl[1],pl[2]).graph(pl[0].x,pl[1].x)
            pieces.append(par)
            for i in range(1,len(pl)-1):
                p1=pl[i-1]
                p2=pl[i]
                p3=pl[i+1]
                par=LagrangePolynomial(  p1,p2,p3).graph(p1.x,p2.x)
                par.parameters=self.parameters.copy()
                pieces.append(par)
            par=pieces[-1]
            mx=par.mx
            Mx=pl[-1].x
            pieces[-1]=par.graph(mx,Mx)
            return "\n".join(  [   par.latex_code(language="tikz",pspict=pspict) for par in pieces  ]   )
        elif isinstance(self.mode,int):
            n=self.mode
            a=[]
            if n%2==1:
                print("You need a even degree")
                raise ValueError
            for i in range(0,len(pl)-1):
                pts=[]
                if (n-2)/2>i:
                    pts=pl[0:n]
                elif i>n-(n-2)/2:
                    pts=pl[-n:]
                else:
                    mid=int(n/2)
                    pts=pl[ i-mid+1:i+mid+1  ]     # Here we assume 'n' to be even
                K=LagrangePolynomial(pts).graph( pl[i].x,pl[i+1].x )
                K.parameters=self.parameters.copy()
                a.append(  K.latex_code(language="tikz",pspict=pspict)  )
            return "\n".join(a)
        else :
            print("Really, there is no mode here ?")
            raise DeprecationWarning
            l = []
            params=self.params(language="tikz")
            l.append("\draw [{0}] plot [smooth,tension=1] coordinates {{".format(params))
            for p in pl:
                l.append(p.coordinates(numerical=True,digits=3,pspict=pspict))  # see 295815047.
            l.append("};")
            return "".join(l)
        raise
    def latex_code(self,language,pspict=None):
        if language=="pstricks":
            raise DeprecationWarning
            return self.pstricks_code(pspict)
        if language=="tikz":
            return self.tikz_code(pspict)
    def __str__(self):
        """
        Return a string representation

        EXAMPLES::

        sage: from phystricks.BasicGeometricObjects import *
        sage: print InterpolationCurve([Point(0,0),Point(1,1)])
        <InterpolationCurve with points ['<Point(0,0)>', '<Point(1,1)>']>
        """
        return "<InterpolationCurve with points %s>"%(str([str(P) for P in self.points_list]))

