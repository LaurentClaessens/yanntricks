# -*- coding: utf8 -*-
from phystricks import *
def LARGooSLxQTdPC():
    pspict,fig = SinglePicture("LARGooSLxQTdPC")
    pspict.dilatation(1)

    x=var('x')
    f1=phyFunction( sin(2*x)  )
    f2=phyFunction( cos(3*x) )
    curve=ParametricCurve(f1,f2,interval=(0,2*pi))

    pspict.DrawGraphs(curve)
    pspict.DrawDefaultAxes()

    fig.conclude()
    fig.write_the_file()
