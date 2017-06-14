# -*- coding: utf8 -*-
from phystricks import *
def WWPPooTSxdXI():
    pspict,fig = SinglePicture("WWPPooTSxdXI")

    A=Point(1,2)
    B=A+(-1,-2)
    C=A+(2,-2)

    trig=Polygon(A,B,C)

    s=Segment(Point(0,0),Point(1,1))
    s.parameters.style="dashed"
    trig.edges_parameters.style="dashed"

    pspict.DrawGraphs(trig,s)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
