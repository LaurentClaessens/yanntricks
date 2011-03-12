from phystricks import *

"""
This file contains only doctests with output too long or not sufficiently interesting to be included in the code itself.
"""

def Test_Segment():
    """
    sage: v = Segment(Point(0,0),Point(2,0)).get_normal_vector()
    sage: print v.arrow_type
    vector
    sage: s= Segment(Point(1,1),Point(2,2))
    sage: v=s.get_normal_vector()
    sage: print v.I
    Point(1.5,1.5)
    sage: print v.F
    Point(1/2*sqrt(2) + 1.5,-1/2*sqrt(2) + 1.5)
    sage: print v.length()
    1

    sage: l = Segment(Point(0,0),Point(0,1))
    sage: v = AffineVector(Point(-1,1),Point(-2,3))
    sage: print v.equation
    x + 1/2*y + 1/2 == 0
    """

def Test_VectorField():
    """"
    sage: x,y=var('x,y')
    sage: F=VectorField(x,y).graph(xvalues=(x,1,2,3),yvalues=(y,-2,2,3))
    sage: unify_point_name(F.pstricks_code())
    '\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,-2.00000000000000){Xaaaa}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,-4.00000000000000){Xaaab}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,0){Xaaac}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,0){Xaaad}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaac}{Xaaad}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.00000000000000){Xaaae}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,4.00000000000000){Xaaaf}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaae}{Xaaaf}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.50000000000000,-2.00000000000000){Xaaag}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,-4.00000000000000){Xaaah}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaag}{Xaaah}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.50000000000000,0){Xaaai}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,0){Xaaaj}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaai}{Xaaaj}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.50000000000000,2.00000000000000){Xaaak}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,4.00000000000000){Xaaal}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaak}{Xaaal}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,-2.00000000000000){Xaaam}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,-4.00000000000000){Xaaan}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaam}{Xaaan}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,0){Xaaao}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,0){Xaaap}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaao}{Xaaap}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,2.00000000000000){Xaaaq}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](4.00000000000000,4.00000000000000){Xaaar}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaq}{Xaaar}'

    sage: G=VectorField(x,y).graph(draw_points=[Point(1,2),Point(3,4)])
    sage: unify_point_name(G.pstricks_code())
    '\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,2.00000000000000){Xaaaa}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](2.00000000000000,4.00000000000000){Xaaab}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](3.00000000000000,4.00000000000000){Xaaac}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](6.00000000000000,8.00000000000000){Xaaad}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaac}{Xaaad}'
"""

def Test_SingleAxe():
    """
    sage: axe = SingleAxe(Point(1,1),Vector(0,1),-2,2)
    sage: pspict=pspicture("MyTest")
    sage: unify_point_name(axe.pstricks_code(pspict))
    '\\pstGeonode[](0.400000000000000,-2.00000000000000){Xaaaa}\n\\rput(Xaaaa){\\rput(0;0){$-2$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,-2.00000000000000){aaaKMyTestTDZZZZZZZZZZZZZZ}\n\\pstGeonode[](0.400000000000000,-1.00000000000000){Xaaab}\n\\rput(Xaaab){\\rput(0;0){$-1$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,-1.00000000000000){aaaLMyTestODZZZZZZZZZZZZZZ}\n\\pstGeonode[](0.400000000000000,0){Xaaac}\n\\rput(Xaaac){\\rput(0;0){$0$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,0){aaaMMyTestZDZZZZZZZZZZZZZZZ}\n\\pstGeonode[](0.400000000000000,1.00000000000000){Xaaad}\n\\rput(Xaaad){\\rput(0;0){$1$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,1.00000000000000){aaaNMyTestODZZZZZZZZZZZZZZ}\n\\pstGeonode[](0.400000000000000,2.00000000000000){Xaaae}\n\\rput(Xaaae){\\rput(0;0){$2$}}\n\\pstGeonode[PointSymbol=|,dotangle=90.00000,linestyle=solid,linecolor=black](0,2.00000000000000){aaaOMyTestTDZZZZZZZZZZZZZZ}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,-1.00000000000000){Xaaaf}\n\\pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,3.00000000000000){Xaaag}\n\\ncline[linestyle=solid,linecolor=black]{->}{Xaaaf}{Xaaag}'
    """

