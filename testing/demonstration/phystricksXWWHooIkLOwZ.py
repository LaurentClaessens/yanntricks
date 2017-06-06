# -*- coding: utf8 -*-
from phystricks import *
def XWWHooIkLOwZ():
    pspict,fig = SinglePicture("XWWHooIkLOwZ")
    pspict.dilatation_X(1)
    pspict.dilatation_Y(1)

    O=Point(0,0)
    A=Point(-3,-2)
    B=Point(4,-1)

    trig=Polygon(O,A,B)

    a1=AngleAOB(A,O,B)
    a1.put_mark(text="mmmmmmmm",pspict=pspict)

    pspict.DrawGraphs(trig,a1)
    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
