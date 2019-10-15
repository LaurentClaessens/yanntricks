###########################################################################
#   This is part of the module yanntricks
#
#   yanntricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   yanntricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with yanntricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2010-2017, 2019
# email: laurent@claessens-donadello.eu

from sage.all import lazy_attribute
from yanntricks.src.ObjectGraph import ObjectGraph


class InterpolationCurve(ObjectGraph):
    r"""
    determine an interpolation curve from a list of points.

    INPUT:
    - ``points_list`` - a list of points that have to be joined.

    OPTIONAL INPUT:

    - ``context_object`` -  the object that is going to use the InterpolationCurve's latex code.
                            ImplicitCurve and wavy curves are using InterpolationCurve as "backend" for the latex code.  Here we use the context_object in order to take this one into account when determining the parameters (color, ...).

    EXAMPLES:

    This example is valid, but will not plot the expected line (this is a feature of `\pscurve`)::

        sage: from yanntricks import *
        sage: F=InterpolationCurve([Point(0,0),Point(1,1)])

    If you want to plot the small segment, you have to add a point in the center::

        sage: F=InterpolationCurve([Point(0,0),Point(0.5,0.5),Point(1,1)])

    The following draws a circle::

        sage: C=Circle(Point(0,0),1)
        sage: G=InterpolationCurve([C.get_point(2*pi/i,advised=False) for i in range(1,100)])

    Notice in the lase example the use of advised=False in order to speed up the computation.

    NOTE:

    InterpolationCurve is used in order to produce implicit plot and wavy functions.
    """


    def __init__(self, points_list, context_object=None, mode=None):
        ObjectGraph.__init__(self, self)
        self.parameters.color = "brown"

        self.points_list = points_list

        self.I = self.points_list[0]
        self.F = self.points_list[-1]
        self.context_object = context_object
        if self.context_object is None:
            self.contex_object = self
        self.mode = mode
        self._minmax_data = None

    def representative_points(self):
        return self.points_list

    @lazy_attribute
    def get_minmax_data(self):
        """
        Return a dictionary whose keys give the xmin, xmax, ymin, and ymax
        data for this graphic.

        EXAMPLES::

        sage: from yanntricks import *
        sage: C=Circle(Point(0,0),1)
        sage: n=400
        sage: InterpolationCurve([C.get_point(i*SR(360)/n,advised=False) for i in range(n)]).get_minmax_data()
        {'xmax': 1.0, 'xmin': -1.0, 'ymax': 1.0, 'ymin': -1.0}
        """
        xmin = min([P.x for P in self.points_list])
        xmax = max([P.x for P in self.points_list])
        ymin = min([P.y for P in self.points_list])
        ymax = max([P.y for P in self.points_list])

        return {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}

    def xmin(self):
        return self.get_minmax_data['xmin']

    def xmax(self):
        return self.get_minmax_data['xmax']

    def ymin(self):
        return self.get_minmax_data['ymin']

    def ymax(self):
        return self.get_minmax_data['ymax']

    def mark_point(self, pspict=None):
        return self.points_list[-1]

    def bounding_box(self, pspict=None):
        """
        Return the bounding box of the interpolation curve

        EXAMPLES::

        sage: from yanntricks import *
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
        bb = BoundingBox(Point(self.xmin(), self.ymin()),
                         Point(self.xmax(), self.ymax()))
        return bb

    def math_bounding_box(self, pspict=None):
        """
        return the bounding box corresponding to the curve without decorations.

        See InterpolationCurve.bounding_box()
        """
        return self.bounding_box(pspict)

    def tikz_code(self, pspict=None):
        # LaTeX cannot parse too long lines (few thousand of letters). But
        # if we draw 1000 points of a curve with 15 digits for each coordinate
        # we easily break that limit of line length.
        # Thus we only ask for 3 digits after the point.
        pl = self.points_list
        if self.mode == "trivial":
            # One cannot draw each segment separately :
            # this causes the parameters.style='dashed'
            # to not work for example.
            import numpy
            a = []
            sublen = max(len(pl)/500, 1)   # We draw packs of 100 points
            list_of_list = numpy.array_split(pl, sublen)
            for spl in list_of_list:
                l = [abs(P.x) for P in spl]
                l.extend([abs(P.y) for P in spl])
                namax = max(l)  # Largest coordinate present in the curve.

                # The absolute value is for the case where the whole
                # curve is in the ball of radius 0.001 for example.

                #digits=3+abs(ceil(  log(namax,10) ))
                digits = 5
                params = self.params(language="tikz")
                a.append("\draw [{0}] {1};".format(
                    params, "--".join([x.coordinates(digits=digits, pspict=pspict) for x in spl])))
            return "\n".join(a)
        elif self.mode == "quadratic":
            pieces = []
            par = LagrangePolynomial(
                pl[0], pl[1], pl[2]).graph(pl[0].x, pl[1].x)
            pieces.append(par)
            for i in range(1, len(pl)-1):
                p1 = pl[i-1]
                p2 = pl[i]
                p3 = pl[i+1]
                par = LagrangePolynomial(p1, p2, p3).graph(p1.x, p2.x)
                par.parameters = self.parameters.copy()
                pieces.append(par)
            par = pieces[-1]
            mx = par.mx
            Mx = pl[-1].x
            pieces[-1] = par.graph(mx, Mx)
            return "\n".join([par.latex_code(language="tikz", pspict=pspict) for par in pieces])
        elif isinstance(self.mode, int):
            n = self.mode
            a = []
            if n % 2 == 1:
                print("You need a even degree")
                raise ValueError
            for i in range(0, len(pl)-1):
                pts = []
                if (n-2)/2 > i:
                    pts = pl[0:n]
                elif i > n-(n-2)/2:
                    pts = pl[-n:]
                else:
                    mid = int(n/2)
                    # Here we assume 'n' to be even
                    pts = pl[i-mid+1:i+mid+1]
                K = LagrangePolynomial(pts).graph(pl[i].x, pl[i+1].x)
                K.parameters = self.parameters.copy()
                a.append(K.latex_code(language="tikz", pspict=pspict))
            return "\n".join(a)
        else:
            l = []
            params = self.params(language="tikz")
            l.append(
                "\draw [{0}] plot [smooth,tension=1] coordinates {{".format(params))
            for p in pl:
                l.append(p.coordinates(digits=5, pspict=pspict))
            l.append("};")
            return "".join(l)
        raise

    def latex_code(self, language, pspict=None):
        if language == "pstricks":
            raise DeprecationWarning
        if language == "tikz":
            return self.tikz_code(pspict)

    def __str__(self):
        """
        Return a string representation

        EXAMPLES::

        sage: from yanntricks.BasicGeometricObjects import *
        sage: print InterpolationCurve([Point(0,0),Point(1,1)])
        <InterpolationCurve with points ['<Point(0,0)>', '<Point(1,1)>']>
        """
        return "<InterpolationCurve with points %s>" % (str([str(P) for P in self.points_list]))
