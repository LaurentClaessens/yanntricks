# -*- coding: utf8 -*-

from __future__ import division
from phystricks import *

def JSYWooQYduLVLS():
    pspict,fig = SinglePicture("JSYWooQYduLVLS")
    #pspict.dilatation_X(1)
    #pspict.dilatation_Y(1)
    pspict.dilatation(1)

    O=Point(1,1)
    A=Point(3,4)
    B=Point(2,1-2/3)

    curve=EllipseOAB(O,A,B).graph(0,pi/2)

    pspict.DrawGraphs(curve)
    pspict.comment="A quarter of ellipse"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()

