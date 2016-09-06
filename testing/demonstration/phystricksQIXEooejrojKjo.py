# -*- coding: utf8 -*-
from phystricks import *
def QIXEooejrojKjo():
    pspict,fig = SinglePicture("QIXEooejrojKjo")
    pspict.dilatation(0.3)

    l=10
    A=Point(l,l)
    B=Point(-l,-l)

    pspict.DrawGraphs(A,B)

    pspict.axes.single_axeX.Dx=5
    pspict.axes.single_axeY.Dx=5

    pspict.DrawDefaultAxes()
    pspict.comment="The numbering on the axes are not too far, not too close from the axis although there is a dilatation"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
