# -*- coding: utf8 -*-
from phystricks import *
def QNHAooSYgkWVhJ():
    pspict,fig = SinglePicture("QNHAooSYgkWVhJ")
    pspict.dilatation(1)
    x=var('x')
    f=phyFunction(x-floor(x)).graph(0,5)
    f.parameters.plotpoints=1000
    eps=0.01
    surf=SurfaceUnderFunction(f,1,2-eps)
    surf.parameters.filled()
    surf.parameters.fill.color="green"
    #surf.Fsegment.parameters.style="none"

    pspict.DrawGraphs(surf,f)
    pspict.DrawDefaultAxes()
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
