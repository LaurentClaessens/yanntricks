# -*- coding: utf8 -*-
from yanntricks import *
def DEIToomZFknFmn():
    pspict,fig = SinglePicture("DEIToomZFknFmn")
    pspict.dilatation(1)

    x=var('x')
    a=0.5
    b=pi
    f1=phyFunction(sin(x)+1).graph(a,b)
    f2=phyFunction(sin(x)+2).graph(a,b)

    surface=SurfaceBetweenFunctions(f1,f2)
    surface.parameters.filled()
    surface.parameters.fill.color="red"
    surface.curve1.parameters.style="solid"
    surface.curve1.parameters.color="blue"
    surface.curve2.parameters=surface.curve1.parameters

    pspict.DrawGraphs(surface)
    pspict.axes.no_numbering()
    pspict.DrawDefaultAxes()
    pspict.comment="The surface is filled in red, the curves are blue and the vertical segments are black."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
