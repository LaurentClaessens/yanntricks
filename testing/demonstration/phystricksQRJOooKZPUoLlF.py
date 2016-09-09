# -*- coding: utf8 -*-
from phystricks import *
def QRJOooKZPUoLlF():
    """
    Copied from  LLVMooWOkvAB in mazhe
    """
    pspict,fig = SinglePicture("QRJOooKZPUoLlF")
    pspict.dilatation(3)

    x=var('x')
    f1=phyFunction(x)
    f2=phyFunction(x**2)

    surface=SurfaceBetweenFunctions(f1,f2,mx=0,Mx=1)
    surface.parameters.hatched()
    surface.parameters.color="green"
    surface.curve2.put_arrow(0.5)
    surface.curve1.put_arrow(0.5)
    surface.curve1.record_arrows[0]=-surface.curve1.record_arrows[0]

    pspict.DrawGraphs(surface)
    pspict.DrawDefaultAxes()
    pspict.comment="lines in green, one arrow in each sense and area hatched in grey."
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
