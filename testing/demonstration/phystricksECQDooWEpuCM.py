# -*- coding: utf8 -*-
from phystricks import *
def ECQDooWEpuCM():
    pspict,fig = SinglePicture("ECQDooWEpuCM")
    pspict.dilatation_X(1)
    pspict.dilatation_Y(1)


    A=Point(0,0)
    B=Point(4,-1)   # était : 4,-1
    C=Point(4,2)

    triangle=Polygon(A,B,C)
    triangle.put_mark(0.3,["$KLLL\Omega$","$BBB$","$C$"],pspict=pspict)

    pspict.DrawGraphs(triangle)

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
