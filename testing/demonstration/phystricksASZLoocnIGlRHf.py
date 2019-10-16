# -*- coding: utf8 -*-
from yanntricks import *

def ASZLoocnIGlRHf():
    pspict,fig = SinglePicture("ASZLoocnIGlRHf")
    pspict.dilatation_X(2.3)
    pspict.dilatation_Y(0.7)
    pspict.dilatation(1)

    x=var('x')
    P=Point(1,1)
    O=Point(0,0)
    P.put_mark(dist=0.2,text="\( N\)",position="N",pspict=pspict)
    P.put_mark(dist=0.2,text="\( E\)",position="E",pspict=pspict)
    P.put_mark(dist=0.2,text="\( W\)",position="W",pspict=pspict)
    P.put_mark(dist=0.2,text="\( S\)",position="S",pspict=pspict)

    pspict.DrawGraphs(P,O)
    pspict.DrawDefaultAxes()
    pspict.comment="The marks are positionned as written"
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
