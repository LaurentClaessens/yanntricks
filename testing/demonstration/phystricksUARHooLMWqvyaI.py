# -*- coding: utf8 -*-
from phystricks import *
def UARHooLMWqvyaI():
    pspict,fig = SinglePicture("UARHooLMWqvyaI")
    pspict.dilatation(1)
    x=var('x')
    f=phyFunction(x-floor(x)).graph(0,5)
    f.parameters.plotpoints=1000
    eps=0.01
    surf=SurfaceUnderFunction(f,1,2-eps)
    surf.parameters.filled()
    surf.parameters.fill.color="green"

    pspict.DrawGraphs(surf,f)
    pspict.DrawDefaultAxes()
    pspict.comment="The mantisse function : f(x)=x-floor(x).  On of the triangles is filled in green."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
