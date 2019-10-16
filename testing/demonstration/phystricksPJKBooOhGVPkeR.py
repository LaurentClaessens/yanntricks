# -*- coding: utf8 -*-
from yanntricks import *
def PJKBooOhGVPkeR():
    pspict,fig = SinglePicture("PJKBooOhGVPkeR")

    x=var('x')
    s=phyFunction(x**2-1).fit_inside(xmin=-2,xmax=2,ymin=-0.5,ymax=3)

    pspict.DrawGraphs(s)
    pspict.DrawDefaultGrid()
    pspict.DrawDefaultAxes()
    pspict.comment="Le graphe de \( x^2-1\) dans la boite  xmin=-2,xmax=2,ymin=-0.5,ymax=3"

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
