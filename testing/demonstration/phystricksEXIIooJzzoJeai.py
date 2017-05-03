# -*- coding: utf8 -*-

from __future__ import division

from phystricks import *
def EXIIooJzzoJeai():
    pspicts,fig = MultiplePictures("EXIIooJzzoJeai",4)
    pspicts[1].mother.caption="adding smart plotpoints"
    pspicts[0].mother.caption="Normal (50 points)"
    pspicts[3].mother.caption="with curvature plotpoints = 50"
    pspicts[2].mother.caption="more points (5000)"

    for psp in pspicts:
        psp.dilatation_X(1)
        psp.dilatation_Y(1)

    xmin=0.05
    x=var('x')
    f1=phyFunction( sin(1/x) ).graph(xmin,6)
    f2=phyFunction( sin(1/x) ).graph(xmin,6)
    f3=phyFunction( sin(1/x) ).graph(xmin,6)
    f4=phyFunction( sin(1/x) ).graph(xmin,6)

    f2.added_plotpoints=[2/(k*pi) for k in range(1,13)]  
    f3.linear_plotpoints=5000
    f4.curvature_plotpoints=50

    pspicts[0].DrawGraphs(f1)
    pspicts[1].DrawGraphs(f2)
    pspicts[2].DrawGraphs(f3)
    pspicts[3].DrawGraphs(f4)

    for psp in pspicts:
        psp.axes.no_numbering()
        psp.DrawDefaultAxes()

    fig.conclude()
    fig.write_the_file()
