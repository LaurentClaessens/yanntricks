# -*- coding: utf8 -*-
from phystricks import *
def BHESoofmkTbbZR():
    pspict,fig = SinglePicture("BHESoofmkTbbZR")
    pspict.dilatation(4)

    x=var('x')

    eps=0.001
    f=phyFunction(sin(1/x)).graph(eps,1)

    pspict.DrawGraphs(f)
    pspict.DrawDefaultAxes()
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

