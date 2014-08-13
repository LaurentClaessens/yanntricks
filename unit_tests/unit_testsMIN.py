# -*- coding: utf8 -*-

from phystricks import *

def Test_Measure():
    r"""
    sage: O=Point(0,0)
    sage: A=Point(0.3,0)
    sage: U=Point(1,0)

    sage: measureOA=MeasureLength(Segment(O,A),0.1)
    sage: measureOA.put_mark(0.3,measureOA.advised_mark_angle,"$a$")
    sage: print unify_point_name(measureOA.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.150000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0,-0.100000000000000){Xaaab}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.150000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.300000000000000,-0.100000000000000){Xaaac}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaac}

    sage: measureAU=MeasureLength(Segment(A,U),0.1)
    sage: measureAU.put_mark(0.3,measureAU.advised_mark_angle,"$1-a$")
    sage: print unify_point_name(measureAU.pstricks_code())
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.650000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.300000000000000,-0.100000000000000){Xaaab}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaab}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](0.650000000000000,-0.100000000000000){Xaaaa}
    \pstGeonode[PointSymbol=none,linestyle=solid,linecolor=black](1.00000000000000,-0.100000000000000){Xaaac}
    \ncline[linestyle=solid,linecolor=black]{->}{Xaaaa}{Xaaac}
    """
